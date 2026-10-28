---
title: "The Self-Organizing Data Stack"
source: "https://www.dataengineeringweekly.com/p/the-self-organizing-data-stack?utm_source=tldrdata"
author:
  - "[[Ananth Packkildurai]]"
published: 2026-10-14
created: 2026-10-28
description: "When agents answer the questions, they can maintain the data model. Here is what that demands from the orchestration engine."
tags:
  - "clippings"
---
### When agents answer the questions, they can maintain the data model. Here is what that demands from the orchestration engine.

![](https://substackcdn.com/image/fetch/$s_!Uk9w!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F95b8fb65-dfd7-4751-bae5-dfcfd9ce2fab_1672x941.png)

Today, a data engineer does two jobs: they decide which tables should exist(Data Modeling), and they hand-wire the orchestration engine—schedules, dependencies, retries, and backfills—to keep them current. When a new business requirement arrives a month later with a slightly different question, the engineer faces a choice: spend three days reverse-engineering someone else’s fragile DAG—learning its unwritten assumptions and risking silent downstream breakage—or copy-paste the SQL and build a new table.

Every rational engineer chooses to build a new table. Multiply that survival instinct across two hundred engineers and three years, and you get the modern data warehouse: high-entropy sprawl. A dozen versions of customer\_spend, thousands of models nobody dares refactor, and petabytes of zombie tables nobody dares drop.

Thus far, AI has only poured gasoline on this fire. By handing coding agents to engineers without changing the underlying orchestration model, we dropped the cost of generating a new pipeline to near-zero while leaving the risk of refactoring an existing one sky-high. The result is an explosion of AI-generated “slop pipelines”—each optimizing locally for a single prompt while accelerating global warehouse chaos.

We tolerated manual sprawl because data modeling was a human activity for human consumers. We design static star schemas and conformed dimensions so an analyst can navigate the warehouse well enough to answer another person’s question. Legibility is the model’s whole point.

Agents break that assumption—provided we move intelligence out of the IDE and into the runtime. When an AI agent consumes data and produces an answer, the physical model no longer needs to be shaped like a museum exhibit for human comprehension or maintained by human hands. The dependency graph stops being a rigid input engineers draw and becomes a dynamic output the orchestration engine maintains—optimizing for reuse, cost, and correctness as consumer needs shift.

What stays human is meaning. People still own the definitions, policies, and judgments the system must honor. I call this design the **self-organizing data stack**.

### How Order Emerges: The Asset Is the Contract

Look closely at any living system, and you notice a paradox: **individual parts are fragile, yet the whole remains deeply organized.** In his classic book *Sync*, mathematician Steven Strogatz asks how the universe pulls off this trick—how order emerges from chaos without a central conductor. How do thousands of fireflies along a riverbank begin flashing in perfect unison? How do individual pacemaker cells synchronize to generate a steady heartbeat?

To replace the central human choreographer with emergent order, we have to change what a data asset is. In a self-organizing stack, an asset is not a physical table sitting in storage; it is a persistent, logical data product with a stable identity. It declares its semantic meaning, grain, and **commitments** to each downstream consumer.

Assets don’t act or run rogue background LLM processes. They simply declare their boundaries, while the orchestration engine coordinates the graph through five core loops:

- **Synthesize:** Builds the physical tables and transformations a new request requires.
- **Consolidate:** Detects overlapping specifications and proposes sharing, splitting, or merging underlying work.
- **Verify and Repair:** Tests every graph change or failure repair against downstream contracts before shipping.
- **Coordinate:** Activates versioned changes atomically so no active consumer commitment is broken.
- **Escalate:** Brings a human owner one specific question, with evidence and trade-offs, whenever semantic ambiguity blocks progress.

One architectural split makes all five loops possible: **an asset keeps its identity while its physical implementation changes.** The contract belongs to the asset; the engine owns the physical machinery. That separation lets the platform continuously rewire the warehouse without forcing any downstream consumer to rewrite its integration.

### From Consumer Intent to Emergent Reuse

Watch how this works in practice. A sales application needs each customer’s spending over the previous 30 days. Whether typed by a person or sent by an agent via API, the request states only the outcome and the commitment:

> *Create customer\_spend\_30d. Return one row per customer with their spending over the previous 30 complete calendar days in UTC. Use our approved purchase amount and customer identity definitions. Include customers with no qualifying purchases. Reflect newly available source data within five minutes. Maintain this asset while the sales application depends on it.*customer\_spend\_30d

There is no mention of tables, join keys, or cron schedules. To interpret this intent without hallucinating, the engine relies on the **semantic layer**: authoritative sources, entity keys, units, approved calculations, and temporal rules. This is the load-bearing wall of the design. The system cannot turn a plausible guess about a column name into a business definition; when meaning is missing, it escalates an open question rather than guessing in SQL.

From the semantic layer, the planner compiles a formal specification and derives its own tests automatically: *one row per customer* enforces uniqueness; *including zero-spend customers* requires an outer join against the customer registry; *approved purchase amount* supplies reconciliation rules against the raw ledger. Because a direct transformation over raw purchases serves this first consumer cheaply within its five-minute SLA, the engine builds a simple, direct pipeline.

Now what happens a month later when a support agent asks for the same metric over **90 complete UTC days**?

In today’s stack, a coding copilot happily spins up a duplicate pipeline scanning raw purchases all over again. In a self-organizing stack, the planner looks past the physical tables to the specifications underneath. It sees that customer\_spend\_30d and the new 90-day request share the exact same DNA: same USD purchase definition, same customer identity rules, and—crucially—the same complete UTC day boundaries (since rolling windows ending at the current second couldn’t share an aggregate).

Without a human touching a keyboard, the system adapts:

1. It proposes a shared customer\_spend\_daily intermediate with 90 days of history.
2. It confirms source history exists, checks access policies, and backfills the daily rollup.
3. It creates the 90-day support asset on top of the daily table, and **quietly rewires the existing 30-day sales asset to read from the new daily intermediate.**

![Figure 1. A new consumer leads the engine to create a shared asset and rewire an existing one.
](https://substackcdn.com/image/fetch/$s_!9JRV!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4fec3ba3-8ba5-456d-abf6-6f9afe9fd740_2048x1344.png)

A new business requirement leads the engine to create a shared asset and rewire an existing one.

Any senior engineer could execute that refactor in ten minutes. The point is that nobody had to. The second request changed the optimal architecture, and the orchestration engine reorganized the graph while preserving the sales application’s contract.

### The Physics of Reuse (and Its Limits)

Consolidation is not a blind mandate. A different currency policy, customer definition, access scope, or fiscal calendar requires a separate implementation. Similar column names and matching sample rows never prove equivalence—only formal definitions can.

Even valid sharing carries a thermodynamic cost. A shared dependency widens the blast radius of a failure, and refreshing a heavy intermediate every five minutes to satisfy one real-time consumer might cost more than running two separate pipelines.

To avoid thrashing, the planner acts like a damped control system. It measures actual compute costs, requires a minimum expected savings threshold before reorganizing, and caps how often an asset can be refactored. When it finds true duplicates, it merges their physical implementation behind both existing interfaces until dependents migrate.

This changes what platform teams celebrate: not table counts or pipeline velocity, but fulfilled consumer contracts at optimal cost. Sometimes the best response to a new request is to build nothing at all.

### Turning the DAG Inside Out

Parts of this vision already exist. Kubernetes popularized the reconciliation loop (desired vs. actual state). Asset-oriented orchestrators shifted our mental model from task schedules to data assets. Warehouse dynamic tables and materialized views automate incremental refreshes.

Yet every one of these tools still expects a human to author the graph. The self-organizing stack moves **graph authorship itself** into the orchestration engine.

To do this safely, the runtime maintains a versioned view of **Desired State** (the outcomes and SLAs consumers have contracted for) and **Observed State** (the implementations, lineage, watermarks, and health that actually exist). When a new request, a failed check, or an expired commitment opens a gap between the two, the engine proposes a graph mutation.

![](https://substackcdn.com/image/fetch/$s_!jgTd!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6a9dd85b-4443-4299-b5b4-cbd926154b68_1720x2048.png)

The engine continuously compares intent with observed state and owns the full path from a proposed graph change to its outcome.

An LLM can help parse intent and draft candidate SQL, but **a model’s confidence never authorizes a graph change.** Drafts are confined to deterministic planners, type checks, access gates, cost controls, and independent verification.

Scheduling emerges directly from these decisions: daily rollups run when source watermarks advance; windowed views roll forward at UTC midnight. This turns the traditional pipeline DAG inside out. The DAG stops being the system’s durable source of truth and becomes a disposable execution artifact—a temporary plan generated for a single change. What persists are the assets, commitments, and decisions.

### Adversarial Verification and Atomic Cutover

Autonomy without verification is just automated chaos. Before the engine activates that shared daily spending table, it must prove the change won’t break the 30-day consumer’s contract.

Consider the classic trap that ruins data engineers’ weekends: **historical identity fan-out**. Suppose the customer identity source tracks historical account merges, and the approved attribution rule uses the mapping active *at the time of purchase*. If a candidate transformation carelessly joins on account\_id alone, any account with two historical mappings will count every purchase twice.

Look at what happens when you run standard syntactic tests on that broken table:

- Schema check? **Pass.**
- Null check? **Pass.**
- Primary key uniqueness after aggregation? **Pass.**

Every green light on a traditional dashboard will lie to you. The totals are simply wrong.

A self-organizing stack verifies against **semantic invariants**, not just syntax. A reconciliation check against the approved purchase definition immediately exposes the double-counted revenue and traces it to the proposed daily dependency. The engine revises the join to respect validity intervals and reruns verification—comparing old and new implementations on identical input snapshots while independently checking business invariants. An LLM that writes both a calculation and its test cannot certify its own assumptions.

Once verified, activation must handle concurrency. If a new consumer registers a dependency on the 30-day asset while testing is underway, the evidence is stale. To catch this, the coordinator binds each activation to strict revision numbers inside a transactional registry—staging the assets, verifying that no contracts shifted during testing, and atomically flipping the active pointers (or orchestrating a blue/green migration across separate storage backends). If a defect ever slips through, the recovery record names every downstream consumer that read bad data during the exposure window, because rolling back a table can’t undo an action an agent already took.

### Humans Own Meaning—and the Decision Record

If the orchestration engine maintains the physical model, where do people go to understand the system? **To the decisions, not the schemas.**

Suppose a third consumer asks for *household spending over 90 days*. The engine finds two approved household definitions: one groups people by physical residence, the other by linked billing accounts.

The engine doesn’t guess. It escalates one surgical question to the domain owner, showing how each definition groups customers, which existing assets each can reuse, and what each costs. The human chooses the meaning; the engine scopes that choice to the authorized domain and derives the graph.

Every clarification, specification, proposal, verification report, and deployment is linked into an immutable decision log. Every requirement on a live asset points directly to its causal origin:

```markup
asset_id: household_spend_90d

spec_version: 1

requirements:

  household_definition:

    ref: semantic:primary_residence_household@2

    source: decision:d17

  spending_definition:

    ref: semantic:purchase_amount_usd@4

    source: policy:approved_spending_semantics@4

  window:

    complete_calendar_days: 90

    timezone: UTC

    source: message:m3

change_proposal_ref: proposal:p28

verification_ref: verification:v91

deployment_ref: deployment:d44
```

Built on standards like W3C PROV and OpenLineage, this record replaces the cognitive job the star schema used to do. Instead of reverse-engineering SQL files to guess what a table means, you read *why* an asset exists, what it guarantees, and who authorized its definition. Human judgment accumulates as versioned data.

### Debugging at 3:00 A.M. and Metabolic Cleanup

When this breaks at 3:00 a.m., how do you debug a graph you didn’t draw? **Start from broken commitments, not failed tasks.**

In a traditional orchestrator, you debug by reading the DAG because the DAG is the design. Here, the design lives in specifications and decisions. Instead of tracing a red task box to see if anyone cares, the operator’s console answers four questions in order: which commitments are unmet, which consumers they affect, which recent graph changes touched them, and what repair the engine is testing. And because autonomy without brakes won’t survive its first incident, operators can freeze reorganization across a domain, pin an asset to a known-good version, or replay a proposal against historical inputs.

Just as importantly, a living stack cleans up after itself. In biology, bone grows where stress is applied and dissolves where load disappears. Data warehouses currently have no metabolism—they only accumulate mass.

In a self-organizing stack, when the sales application eventually drops its 30-day spend subscription, the engine retires customer\_spend\_30d while keeping the 90-day support asset alive. It doesn’t rely on naive query-log scraping—since a finance job might only run at quarter-end—but weighs explicit contract expiration, compliance retention policies, and reconstruction cost. It can demote a physical table to a virtual view, freeze compute while keeping history, or dissolve an intermediate table entirely once its last shared dependent is gone.

### Building the Platform for the Agentic Era

This design doesn’t remove data engineers; it elevates what we author. We stop acting as human compilers translating requests into brittle DAGs, and start designing the boundaries and laws of physics the runtime must obey.

You don’t have to replace your orchestrator overnight to start this transition. As Ian Macomber recently argued in **[The Post-AI Data Stack](https://www.iandmacomber.com/blog/post-ai-data-stack/)**, AI makes producing analysis cheap, which means *engineering consensus on reality* is the new bottleneck. The most practical stopgap today is standing up a dedicated **Context Pipeline** alongside your existing data pipelines—shifting from **[ETL to ECL (Extract, Contextualize, Link)](https://www.dataengineeringweekly.com/p/data-engineering-after-ai)**. Instead of burying business rules in 400-line SQL files that coding agents can’t see, a Context Pipeline extracts, versions, and links entity definitions and domain decisions into an authoritative layer. Once that context layer matures, it stops being just a reference for coding agents and becomes the orchestrator's control plane.

If you build data platforms or orchestration engines, start here:

1. **Make consumer commitments first-class.** Record who depends on each asset and what was promised, separately from the SQL that fulfills it.
2. **Invest in the semantic layer before the planner.** An engine can reorganize only what it can prove equivalent from formal definitions.
3. **Build adversarial verification.** Independently check outputs against approved definitions, grade the evidence, and never let an agent grade its own work.
4. **Treat decisions as data.** Capture every human clarification with its authority, scope, and links to the assets it shaped.

Today, a pipeline DAG is where a person writes down the data architecture. In the self-organizing stack, the orchestration engine keeps writing it. A new request creates the graph, an overlap reshapes it, a failed commitment triggers a repair, and an expired commitment simplifies it. Humans author the meaning; the engine authors the graph.

**That is the orchestration engine I want for the agentic era.**

---

*All rights reserved, Dewpeche Private Limited. I provide links for informational purposes and do not endorse them. All views expressed in this newsletter are my own and do not represent the opinions of any current, former, or future employers.*

---

∙