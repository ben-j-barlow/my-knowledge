---
title: "Data quality traffic lights"
source: "https://robertsahlin.substack.com/p/data-quality-traffic-lights?utm_source=tldrdata"
author:
  - "[[Robert Sahlin]]"
published: 2026-06-17
created: 2026-07-23
description: "Building trust for dashboards, agents and ML pipelines"
tags:
  - "clippings"
---
## The trust problem

When you open a dashboard showing revenue metrics or customer counts, how do you know the numbers are accurate? In a data platform with hundreds of transformations and dependencies, the answer is often **you don’t**.

Data pipelines fail in obvious ways (a test fails, a SQL job crashes) but they also fail silently. Data arrives but is three days old. Volume drops by 80% but the pipeline runs successfully. An upstream table breaks and silently corrupts everything downstream and users discover these problems only after making decisions based on bad data.

This problem becomes more acute as data platform adoption grows. As more people rely on data for daily decisions, the need for clear trust signals becomes critical. A dashboard used by 5 people may tolerate occasional quality issues, a dashboard used by 50 cannot.

Last fall, we (the data platform engineering team at Nordnet) set out to solve this and this spring, we launched a Data Quality Health Badge that surfaces near real-time trust signals directly in Looker dashboards. This is the story of how we built it and what we learned.

## The architecture

The health badge rests on three pillars: detecting incidents, tracking lineage and surfacing trust signals to users.

### Detecting incidents

Our incident detection system watches for five distinct failure modes across the platform.

![](https://substackcdn.com/image/fetch/$s_!BgdO!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4ad3501c-ef94-4750-a9c0-563a66f9649c_2280x1534.png)

#### Failed tests

We run dbt Core as scheduled Cloud Run jobs. After each execution, the job uploads detailed run results to BigQuery. These tables capture every node execution with its status, timing and any error messages.

We built SQL models that process these run results into structured incidents. The clever part is detecting incident boundaries, i.e. when did a failure ***start*** (first failure after success), and when did it ***end*** (first success after failure)? Using window functions and state tracking, we identify these transitions and create incident records with clear start and end timestamps.

For example, if a uniqueness test starts failing on Monday and doesn’t pass again until Wednesday, we create a single incident spanning those three days rather than one incident per failed run. This prevents alert fatigue and gives a true picture of incident duration.

#### Failed runs

When scheduled transformation jobs fail to execute, we capture both standard failures and silent failures. Silent failures are particularly deceptive, the Cloud Run job terminates early due to timeouts, infrastructure quotas or crashes without reporting which specific models failed.

To catch these, we log which models are *planned* to run at the start of each execution. Then we cross-reference this plan with BigQuery audit logs to see which models actually completed. If a model was planned but never shows up in the audit logs (or shows up as failed), we know the job crashed midway through. These *midway fails* get surfaced as incidents just like explicit failures.

#### Source freshness violations

When external data sources don’t update on schedule, dbt’s source freshness checks fail. These get captured alongside test failures, but we treat them specially because they indicate problems *outside* our control (upstream systems have stopped delivering data).

#### Data volume anomalies

Silent failures often manifest as volume changes: a daily batch that normally loads 50,000 rows suddenly loads 200 rows. Everything runs *successfully* but the data is incomplete.

We analyze BigQuery’s audit logs to track how many bytes get written to each table over time. For anomaly detection, we use BigQuery’s TimesFM model, a foundation model for time series forecasting. TimesFM makes advanced ML-based anomaly detection remarkably straightforward. It requires minimal configuration, handles seasonality and trends automatically and runs directly in BigQuery without external infrastructure. The model delivers good accuracy while remaining low maintenance.

The tuning here was crucial. User-behavior-driven tables (login events, search queries) naturally dip on weekends, while system-driven tables (account balances, positions) remain consistent. We built per-table configuration to suppress weekend anomalies where appropriate and adjust sensitivity thresholds based on each table’s characteristics. For a deep dive into how we implemented volume anomaly detection with TimesFM, see our [separate post on the topic](https://robertsahlin.substack.com/p/your-pipeline-succeeded-your-data).

#### Manual incidents

Sometimes humans need to get involved. We built a Streamlit app that gives us a UI for managing incidents. Through this app, we can manually create incidents for known issues not caught by automation, close or resolve existing incidents and override automated detections with custom severity, end time or description.

The app provides a simple interface for incident management without requiring direct BigQuery access. We can acknowledge false positives, document planned outages or add context to automated incidents. All manual changes are logged with timestamps and user information for audit purposes.

Beyond active incident management, all incidents (both automated and manual) are kept historically. This historical record enables analysis over time: how many incidents were opened per day, which teams or domains have the most incidents, what types of failures are most common and how incident patterns change as the platform evolves.

### Building the lineage graph

Detecting incidents is only half the problem. The critical question is: *what else is affected?* If a core customer table is broken, which downstream models and dashboards inherit that problem?

![](https://substackcdn.com/image/fetch/$s_!98Cs!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ad3da0c-af4c-4f6c-9e88-ab3ecf192bda_2280x1250.png)

#### Extracting dbt lineage

Every day at 3 AM, a GitHub Actions workflow downloads the production dbt manifest from cloud storage and parses it. The manifest is a JSON file that dbt generates during compilation, containing the complete dependency graph of every model, seed and source in the project.

We wrote a Python script that walks this graph and for each table, we identify its complete downstream dependency tree (not just immediate children, but all descendants, recursively). This gets uploaded to BigQuery as a table mapping each table to the full list of tables that depend on it.

#### Extracting Looker lineage

Dbt lineage tells us about table-to-table dependencies, but users consume data through Looker explores and dashboards, not raw BigQuery tables. We needed to bridge this gap.

We built a second extractor that parses LookML files to identify which BigQuery tables feed each explore. For every explore definition, we extract the base view and any joins, then trace each view back to its underlying BigQuery table. This mapping gets uploaded to BigQuery, allowing us to answer: if a specific table has an incident, which Looker explores are affected?

#### Stitching it together

Currently, we maintain separate lineage graphs for the warehouse layer (dbt) and the Looker layer, then stitch them together in our incident models. This works well but requires maintaining two parsers. In the future, we’re hoping to leverage GCP Knowledge Catalog’s lineage capabilities once it fully supports Looker assets. This would give us a unified lineage graph without manual stitching.

#### Calculating blast radius

With both lineage graphs in hand, our incident models join them together. For every incident, we now know exactly which tables and BI explores inherit that incident. A single upstream failure might cascade to dozens of downstream assets and we surface every one.

![](https://substackcdn.com/image/fetch/$s_!lR9O!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb4eea64b-98ec-4a4f-b178-5bc8652371bf_2280x1272.png)

### Surfacing trust signals

The final piece is making this intelligence visible where users actually work, in Looker dashboards.

We built a custom Looker visualization in TypeScript that queries our explore health status model. When you load any dashboard, the health badge appears prominently at the top, showing one of three states:

- **Green checkmark**: All upstream data is healthy
- **Yellow triangle**: Active warnings (e.g., volume anomalies flagged but not critical)
- **Red triangle**: Active errors (failed tests, run failures, critical anomalies)

Click the badge and it expands to show detailed incident information: which upstream tables are broken, what type of incident occurred, which team owns the affected data, when it started, and links to investigate further.

#### Dashboard-specific filtering

A nice feature we added is the ability to filter the health badge to show only the explores that power a specific dashboard. Instead of showing the status of all explores platform-wide, you can add the health badge tile to a dashboard and configure it to only display incidents affecting the explores actually used on that dashboard.

![](https://substackcdn.com/image/fetch/$s_!eaJt!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F08c2e5c3-d055-49c7-8d51-b3631529af1e_932x638.png)

Currently this requires manually specifying which explores to monitor, but we’re planning on making the badge automatically understand which Looker explores a dashboard depends on, eliminating the need for manual configuration. This keeps the signal highly relevant to what users are looking at.

#### The platform dashboard

Beyond per-dashboard badges, we also built a centralized health dashboard showing the status of *every* explore on the platform. This gives us a bird’s-eye view of data quality across the organization.

The dashboard lists all explores sorted by severity (errors first, warnings second, healthy explores last). Expanding an explore reveals the full incident tree: which specific upstream tables are causing problems, detailed descriptions of each incident, team ownership and timestamps. Instead of waiting for users to report problems, platform teams can proactively spot incidents and coordinate remediation.

![](https://substackcdn.com/image/fetch/$s_!z-dX!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd25a1b3d-9ac1-4e49-9949-a84ac10a2b8d_845x738.png)

## From MVP to production

We built this in two major iterations spanning fall through spring.

The first iteration established the foundation. We automated lineage extraction from both the dbt manifest and Looker’s LookML files, set up ingestion of test and run failures, built the core incident models and created the initial health badge visualization. By late fall, we could detect loud failures (tests failing, runs crashing) and show which explores were affected.

The second iteration added sophistication. We implemented source freshness monitoring, volume anomaly detection and silent failure detection to catch incidents that don’t explicitly report errors. We added manual incident management workflows so operations could report known issues or override automated detections. We improved actionability by enriching incidents with team ownership and adding WARNING status alongside ERROR. We also spent some time tuning anomaly detection (per-table configuration, weekend suppression for user-driven data and public holiday awareness).

Throughout spring, we continuously refined the system based by making the health badge UI more intuitive, auto-closing orphaned incidents when tests are renamed or removed, optimizing query performance with partition filters and fine-tuning anomaly sensitivity to reduce false positives.

## Technical decisions that shaped the system

#### Batch lineage

We refresh lineage once per day rather than triggering updates in real-time. Production code deployments that change the DAG happen infrequently, so staleness up to 24 hours is acceptable. Daily batch is simpler and hasn’t caused any issues in practice.

#### How we model incident lifecycle

Incidents exist in one of four states: *active* (end time is null or in the future), *resolved* (first successful run after failure), *expired* (no execution for 30 days, likely the test was renamed or removed), or *manually closed* (overridden by operations).

We implement this entirely in SQL using window functions and QUALIFY clauses. This finds the first success after each failure, or auto-expires incidents after 30 days. No external state management required.

#### ML-based anomaly detection made practical

We use BigQuery’s TimesFM model for volume anomaly detection. While ML-based anomaly detection sounds complex, TimesFM made it remarkably practical: it runs directly in BigQuery (no external infrastructure), handles seasonality automatically, requires minimal tuning and delivers excellent accuracy out of the box. The key was choosing a foundation model that abstracts away the complexity while giving us sophisticated time series forecasting capabilities. This proved more effective than simple statistical thresholds while remaining low maintenance.

## Impact

Users now see trust signals *before* acting on metrics. When a dashboard shows a yellow or red badge, they know to verify findings or wait for resolution rather than trusting numbers blindly. This helps increasing confidence in data across the organization.

Incident response is faster because blast radius is immediately visible. When a test fails on an upstream table, we now know which downstream explores are affected (no manual dependency tracing required). Teams can scope impact and prioritize fixes appropriately.

The platform dashboard gives us a proactive monitoring layer. Instead of learning about incidents through user complaints, the team sees them as they occur. Incidents affecting high-visibility explores get immediate attention.

We’ve also reduced alert fatigue through intelligent consolidation. Rather than separate alerts for each failed run of the same test, users see a single incident spanning the full failure period. Anomaly detection auto-closes after 2 days to prevent stale warnings from cluttering the view.

Historical incident tracking gives us platform-level observability. By retaining all incidents (even after they’re resolved), we can analyze trends over time: which teams have the most data quality issues, which domains are most stable, how incident frequency changes after infrastructure changes, and whether resolution times are improving. This data informs where to invest in platform improvements and helps quantify the impact of reliability initiatives.

## Beyond dashboards

The incident status data we generate has proven valuable beyond just the health badge visualization. By making incident status queryable and accessible, it becomes a foundational primitive that any data consumer can leverage.

#### Enriching GCP Knowledge Catalog

We can use the incident status to enrich asset metadata in GCP Knowledge Catalog. When users browse tables or explores in the catalog, they could see not just schema and documentation, but also current health status. This helps data producers and consumers understand data quality at discovery time, not just consumption time.

#### Analytics agents and LLM workflows

When an LLM-powered agent is about to generate a SQL query to answer a user question, it can first check if any of the tables it plans to use are currently affected by incidents. The agent can warn the user that results may be unreliable, suggest alternative data sources, or explain what specific incident is affecting the data. This ensures agents don’t just generate correct SQL (they understand whether the query will produce trustworthy results).

#### Deterministic services and data consumers

Any service that consumes data from the platform can query incident status before using it. A pricing service that reads from rate tables can check for incidents before serving quotes. An automated report generator can defer sending reports if source data has active incidents. Operational systems can make intelligent degradation decisions rather than blindly consuming potentially corrupt data.

#### Machine learning model retraining

ML models that retrain daily on fresh data can check incident status before each training run. If the training data has active incidents (volume anomalies, failed tests, stale sources), the retraining process can abort and keep the previous model version in production. This prevents weird model behavior caused by training on incomplete or corrupt data. The model only updates when data quality is verified, creating a safety gate in the ML pipeline.

This creates a comprehensive feedback loop where incident status informs decisions across the entire data platform: human dashboards, AI agents, operational services, and ML pipelines all make quality-aware choices.

## Lessons learned

#### Lineage is the hard part

Detection is relatively straightforward (parse run results, analyze write patterns, flag anomalies). But calculating accurate blast radius requires complete, up-to-date lineage graphs. We invested in making lineage extraction robust and reliable before building on top of it.

#### Tune relentlessly

Anomaly detection shipped with too many false positives. User-driven tables showing natural weekend dips got flagged as incidents. We added per-table configuration, weekend suppression, holiday awareness, and adjustable sensitivity thresholds. Expect to iterate continuously based on feedback.

#### Actionability matters more than accuracy

Early versions showed *“There’s an incident”* without context. Users didn’t know what to do with that information. Adding team ownership, communication channels, incident descriptions and links to investigate made the badge actually useful rather than just informative.

#### Automation is non-negotiable

Daily lineage publishing, incident detection and badge refreshes all run automatically. Zero manual intervention after initial setup. Any system requiring daily human involvement won’t last.

#### Choose tools that reduce complexity

We initially worried that ML-based anomaly detection would be too complex to maintain. Using BigQuery’s TimesFM model proved otherwise, sophisticated time series forecasting with minimal configuration and no external infrastructure. The right tool can make advanced techniques accessible without adding operational burden.

#### Start simple and add complexity gradually

We launched with test failures and run failures only. Volume anomalies came later. Manual overrides came later. Silent failure detection came later. Each iteration added one new capability rather than trying to build everything at once.

## What’s next

We’re exploring several enhancements for the next iteration.

#### Unified lineage via GCP Knowledge Catalog

As mentioned earlier, we currently stitch together dbt and Looker lineage manually. We’re waiting for GCP Knowledge Catalog to fully (GA) support Looker assets in its lineage graph. Once that’s available, we can shift from parsing and stitching to simply querying the catalog’s unified lineage API. This would reduce our maintenance burden and give us column-level lineage as a bonus.

#### Column-level incident scoping

Today we show *“this table is broken”* but we can’t yet say *“the revenue column is affected but customer\_count is fine.”* Column-level lineage would enable more precise scoping and reduce false concern about unrelated columns.

#### Automatic dashboard dependency resolution

Currently, when you add a health badge to a dashboard, you need to manually configure which explores it should monitor. We’re planning on making the badge automatically understand which Looker explores a dashboard depends on by analyzing the dashboard’s tiles and resolving their underlying data sources. This would make health badges zero-configuration, drop the visualization on a dashboard and it automatically shows the right incidents without any manual setup.

#### Proactive alert notifications

Currently, the health badge is a pull model (users see incidents when they visit dashboards). We plan to add push notifications that actively alert teams when incidents occur. This could include sending messages to team communication channels when high-severity incidents affect their data, notifying dashboard owners when their explores have active incidents, or escalating incidents that remain unresolved for extended periods. Smart notifications would reduce mean time to detection while avoiding alert fatigue through intelligent routing and severity filtering.

#### Self-service incident management

We currently have a Streamlit app for manual incident management, but it requires platform team access. Expanding self-service capabilities would allow data producers to resolve or acknowledge incidents directly. This would decentralize ownership and reduce bottlenecks on the platform team.

#### Deeper agent integration

Beyond just checking incident status, agents could learn from historical incident patterns. If a table frequently has weekend volume anomalies, the agent could suggest waiting until Monday for reliable results. If a test consistently fails but gets manually overridden, the agent might learn that this particular alert is low-priority.

## Conclusion

The Data Quality Health Badge is a start. By combining incident detection, automated lineage tracking and clear visual signaling, we’ve begun making data quality transparent and actionable. Users now have a trust signal they didn’t have before and the platform team has proactive visibility into issues.

But the real potential lies ahead. As our data platform adoption continues to grow and as we integrate incident status into analytics agents and the data catalog, we’re building toward a future where both humans and machines can make accurate decisions with confidence in the underlying data. The health badge creates the foundation, enriching every data asset with near real-time quality context that informs consumption, discovery, and automated decision-making.

Building it taught us that trust in data rests on three pillars: *detection* (knowing what broke), *context* (knowing what’s affected), and *communication* (telling the right people at the right time). Get these three right, and you create the infrastructure for programmatic trust.

If you’re building a similar system, our advice is this. Invest in lineage infrastructure first, choose tools that reduce maintenance burden and tune continuously based on real-world feedback. Data quality monitoring is a journey, not a destination, but a health badge is an excellent place to start.

**A note of gratitude** - This system was built by my data platform engineering team at Nordnet. A great team of skilled engineers who are also wonderful people to work with. I will miss them all as I start my own company ([Supercargo.dev](https://supercargo.dev/)) in August. I’ll carry forward the lessons learned not just about building data platforms, but about building teams that do great work together.

## What about you?

1\. How does your organization currently handle data quality visibility? Do users know when data is unreliable before they use it?

2\. Have you built similar trust signals into your data platform? What worked well, and what would you do differently?

3\. What’s your biggest data quality pain point right now? Silent failures, test fatigue, lack of lineage, something else?

4\. Are you integrating data quality signals into agents or other automated systems? What’s working and what’s challenging?

---

*I’m committed to keeping this content free and accessible for everyone interested in data platform engineering. If you find this post valuable, the most helpful way you can support this effort is by giving it a like, leaving a comment, or sharing it with others via a restack or recommendation. It truly helps spread the word and encourage future content!*