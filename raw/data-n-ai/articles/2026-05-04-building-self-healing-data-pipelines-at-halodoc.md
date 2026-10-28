---
title: "Building Self-Healing Data Pipelines at Halodoc"
source: "https://blogs.halodoc.io/building-self-healing-data-pipelines-at-halodoc/?utm_source=tldrdata"
author:
  - "[[Dana Rabba]]"
published: 2026-05-04
created: 2026-05-19
description: "At scale, data powers everything — from executive dashboards and operational analytics to financial reconciliation and customer-facing features. But as data platforms grow, one reality becomes unavoidable: pipelines break. What if the platform could heal itself?"
tags:
  - "clippings"
---
Data powers everything from executive dashboards and operational analytics to financial reconciliation and customer-facing features. But as data platforms grow, one reality becomes unavoidable: **pipelines break**. CDC tasks fail. Spark jobs run out of memory. Warehouse queries get stuck. Tables drift out of sync.

For a while, the answer was manual intervention: an engineer was paged, logged in, investigated, and fixed the issue. This works until it doesn't. As pipeline complexity grows, the operational burden becomes unsustainable. Teams spend more time firefighting than building, so we asked a different question: **What if the platform could heal itself** so we don't have to wake a data engineer up at 2 AM to fix the pipe failure?

This blog walks through how we designed a multi-layer self-healing system for our data platform, the problems we faced, the recovery mechanisms we built, and the lessons we learned along the way. While the examples draw from our experience, the patterns are applicable to any organization running distributed data pipelines at scale.

---

## The Reality: Failure Is Inevitable, Downtime Doesn't Have to Be

Modern data platforms are complex, distributed systems. On any given day, hundreds of orchestration jobs, replication tasks, and transformation processes run across multiple layers. Each component has its own failure mode:

| Component | Common Failure Mode | Business Impact |
| --- | --- | --- |
| CDC replication | Binary log rotation, memory exhaustion, network blips | Data stops flowing; downstream tables go stale |
| Bronze-to-silver ETL | Accumulated file volume exceeds executor memory | Backlogs grow; latency increases |
| Spark transformations | Complex joins or shuffles exhaust memory | Jobs fail repeatedly; retries burn resources |
| Warehouse ETL | Orphaned queries from failed runs block new writes | Lock contention; cascading delays |
| Downstream dependencies | Upstream failures silently propagate | Dashboards show stale or incorrect data |

These failures are diverse, but they share a common trait: they interrupt data flow without necessarily corrupting data. In most cases, the data itself remains intact, the system simply needs recovery. But that recovery should not require a human every time.

---

## Our Approach: Six Targeted Self-Healing Layers

We decomposed the problem into targeted recovery layers rather than building a single generalized solution. Each addresses a specific failure mode at its own layer of the stack:

![](https://blogs.halodoc.io/content/images/2026/04/Self-Healing-Page-2.drawio--3-.png)

```
┌─────────────────────────────────────────┐
│     Self-Healing Data Platform          │
├─────────────────────────────────────────┤
│ Layer 1 │ CDC Auto-Recovery             │
│ Layer 2 │ Source-vs-Lake Consistency    │
│ Layer 3 │ Mini-Batch Processing         │
│ Layer 4 │ Smart Memory Scaling          │
│ Layer 5 │ Warehouse Lock Management     │
│ Layer 6 │ Cascading Dependency Recovery │
└─────────────────────────────────────────┘
```

Each layer operates independently, alerts through standard notification channels, and follows a simple principle: **alert first, act second**. Engineers always see what happened, even when the system fixes it automatically.

---

## Layer 1: CDC Auto-Recovery, Restarting Streams Without Losing Data

### The Problem

Change Data Capture (CDC) pipelines stream row-level changes from operational databases into the data lake. When a CDC task fails, replication stops entirely. No new changes are captured. Downstream systems begin to drift from the source of truth.

Common causes:

- Binary log rotation on the source database
- Memory exhaustion during large transaction batches
- Transient network issues

Previously, recovery required manual steps: identify the failed task, calculate a safe restart checkpoint, rewind to avoid missing events, then restart via CLI or console. This took from 15 minutes to several hours, and every minute of delay meant more data to reconcile.

### How It Works

The recovery workflow runs on a schedule and follows a clear sequence:

1. **Detect failed tasks**: Query the CDC service API endpoints for tasks in a failed state.
2. **Alert immediately**: Notify the team before taking action creating an audit trail, regardless of the outcome.
3. **Validate eligibility**: Not every failure should be auto-restarted. We apply three checks:
	- Task type: Only incremental CDC tasks qualify (full-load tasks need human review)
		- Current state: Confirm the task is still failed (avoid interrupting manual fixes)
		- Error classification: Only restart for known recoverable errors (binary log gaps, memory issues, transient failures)
4. **Calculate a safe restart point**: Use a prioritized fallback:
	- Preferred: Last committed CDC position, rewound by a configurable buffer (e.g., 24 hours)
		- Fallback: Task stop timestamp with the same buffer
		- Last resort: Current time minus buffer (ensures coverage, may replay extra data)
5. **Execute and report**: Restart the task with the calculated checkpoint, then send a summary of successes and skips.
![](https://blogs.halodoc.io/content/images/2026/04/Screenshot-2026-04-21-at-08.31.46.png)

A common example of this failure mode is a binary log read error, where the CDC task can no longer continue due to log rotation or missing log segments on the source database. In this setup, failures are not handled in real time but are detected through a scheduled monitoring job that periodically scans for tasks in a failed state. Once identified, the system automatically calculates a safe restart checkpoint, typically by rewinding from the last known position with a buffer, and restarts the task. This approach ensures no data is missed while tolerating some duplicate processing, allowing the pipeline to recover reliably without requiring immediate human intervention.

### Key Insight

The three-gate eligibility check evolved through iteration. Early versions were too permissive and occasionally retried non-recoverable failures, creating noise. Adding error-pattern classification reduced false restarts to near zero.

> 💡 **Design principle**: Favor data completeness over duplicate risk. Downstream systems typically handle idempotency well; they handle data gaps poorly.

---

## Layer 2: Source-vs-Lake Consistency, Catching Gaps Before They Reach Dashboards

### The Problem

Even when the CDC is healthy, data can stall between layers. Raw files may land in the lake but fail to process into the silver layer. Downstream reporting tables then show stale data, often noticed only when business users raise concerns.

By the time this surfaces, the gap can be hours old. Tracing the root cause backward through multiple pipeline stages wastes valuable engineering time.

### How It Works

We built validation workflows that compare aggregated metrics between source and destination at key transition points:

1. **Run validation**: Execute comparison queries (e.g., row counts, checksums) between source and lake tables within a stable time window.
2. **Alert on mismatch**: Notify stakeholders immediately, visibility before action.
3. **Recover upstream first**: If silver-layer tables are inconsistent, trigger backfill of the bronze-to-silver pipeline *before* touching downstream reporting tables. Healing the foundation first prevents propagating bad data.
4. **Heal downstream selectively**: Route mismatched tables to appropriate recovery pipelines based on their purpose (e.g., standard reporting vs. financial reconciliation).
5. **Confirm resolution**: Send a final notification summarizing what was recovered.
![](https://blogs.halodoc.io/content/images/2026/04/Screenshot-2026-04-21-at-08.37.51.png)

This validation runs on a scheduled basis, where the system periodically compares records between the source (RDS) and the silver layer within a defined time window. Instead of relying solely on row counts, we validate using unique identifiers to ensure data completeness and correctness at a granular level. This approach allows us to detect subtle inconsistencies, such as missing or partially processed records, even when aggregate counts appear similar. When mismatches are identified, the system flags the affected tables and triggers targeted recovery workflows, ensuring that data discrepancies are resolved before they propagate further downstream.

### Key Insight

The ordering of recovery steps matters. Early implementations triggered downstream backfills immediately, occasionally "fixing" reporting tables built on inconsistent source data. The rule we now follow: **always fix the foundation before fixing the layers built on top of it**.

---

## Layer 3: Mini-Batch Processing, Handling Backlogs Without Memory Errors

### The Problem

The bronze-to-silver ingestion job serves as the backbone of data processing from the raw (bronze) layer. Under normal conditions, it processes files on a determined schedule. But after any disruption, such as a CDC restart, cluster outage, or network event, files accumulate. The layer 3 recovery system is working under the bronze layer.

The original design had a hard limitation in raw layer processing: Spark can only process what fits in executor memory, simply because of **data volume accumulation**, not transformation complexity. If a table accumulated 10GB of pending files but executors had 8GB of memory, the job would fail. Recovery became fragile: the longer a table was offline, the more likely recovery would fail with an out-of-memory (OOM) error.

### How It Works

We embedded a file-size-aware mini-batch system directly into the transformation job:

1. **Calculate batch assignments**: Before processing, query metadata to group pending files by cumulative size (e.g., 2GB batches) using a window function ordered by arrival time.
2. **Process sequentially**: For each batch:
	- Load only that batch's files into memory.
		- Apply schema evolution checks.
		- Write to the silver layer using upsert semantics.
		- Explicitly release memory before proceeding to the next batch.
3. **Track progress**: Update watermarks and file status after each batch. If the job fails mid-run, completed batches are preserved; the next run picks up only the remaining files.

### Concrete Example

A table accumulates 15GB of CDC files during a 12-hour outage. With 8GB executors and a 2GB batch threshold:

- **Without batching**: Job attempts to load all 15GB → hits OOM → enters a retry spiral → engineer intervention required.
- **With batching**: Job processes 8 sequential 2GB batches → completes reliably → no manual work.
![](https://blogs.halodoc.io/content/images/2026/04/Screenshot-2026-04-21-at-08.42.27-1.png)

In practice, the mini-batch mechanism operates by first calculating the cumulative size of incoming files from the bronze layer, then assigning a batch ID once a predefined threshold is reached. Each file (S3 object) is grouped based on this cumulative progression, ensuring that every batch stays within a safe processing limit. The job then processes data batch-by-batch by selecting the corresponding S3 file keys for each batch ID, rather than loading all pending files at once. This approach guarantees controlled memory usage, preserves ingestion order, and enables reliable recovery, as partially completed batches are checkpointed and only unprocessed batches are retried in subsequent runs.

### Key Insight

The cumulative-size approach to batch assignment proved most robust. Alternatives like count-based or time-window batching broke down because file sizes and arrival rates vary dramatically. This layer ensures that backlog recovery remains deterministic and does not degrade as data volume increases.

---

## Layer 4: Smart Memory Scaling, Making Retries Actually Work

### The Problem

In our architecture, Layer 3 operates in the **bronze (raw) layer**, while Layer 4 operates in the **silver (processed) layer**, addressing different failure modes. Unlike Layer 3, which mitigates input size issues, Layer 4 handles memory pressure caused by transformation logic such as joins, shuffles, and aggregations. Airflow’s default retry mechanism reruns failed tasks with identical resource configurations, making it ineffective for memory-related failures. Teams were burning the retry quota on predictably failing executions, delaying resolution.

### How It Works

Before applying incremental scaling on retries, the system first leverages dynamic right-sizing principles to determine an optimal baseline configuration for each Spark job. By analyzing historical runtime metrics, such as input data size, shuffle volume, executor memory usage, and spill behavior, the system estimates a “right-sized” resource profile that balances performance and cost. This ensures that most jobs start with sufficient resources without over-provisioning by default (For more details on dynamic right-sizing, read [**here**](https://blogs.halodoc.io/apache-spark-dynamic-right-sizing/)).

However, since real-world workloads can still be unpredictable (e.g., data skew or sudden spikes in cardinality), this initial sizing is not always perfect. When a job still encounters memory pressure despite being right-sized, the incremental scaling mechanism acts as a safety net, progressively increasing resources across retries to guarantee eventual completion.

We intercept retries using Airflow's `on_retry_callback` to inspect failure reasons and adjust resources dynamically:

1. **Classify the failure**: Query runtime metrics to determine if the failure was OOM-related (vs. spot interruption, script error, etc.).
2. **Scale progressively**: For confirmed OOM failures, progressively scale resources relative to the original baseline configuration:
	- 1st retry: +25% memory
		- 2nd retry: +40%
		- 3rd+ retry: +60%
3. **Alert and track**: Notify the team of resource adjustments. Repeated OOM alerts on the same job signal a need for permanent configuration updates.
![](https://blogs.halodoc.io/content/images/2026/04/Screenshot-2026-04-21-at-08.54.54.png)

In practice, this looks like: a Spark task fails due to memory exhaustion, the callback intercepts the pending retry, queries the runtime metrics store to confirm OOM as the root cause, and scales executor memory before re-dispatch, bumping from **16G to 26,214M** on a third retry, consistent with the +60% scaling tier. A notification lands immediately in the team's alert channel with the before-and-after configuration. This audit trail also serves a secondary purpose: recurring OOM alerts on the same task are a reliable signal that its baseline configuration needs a permanent increase, not just a one-time retry boost.

### Key Insight

Together, Layer 3 and Layer 4 form a complementary system: one ensures data can be processed, the other ensures it can be computed. Smart scaling handles OOM from *computation* (transformations that generate large intermediate data).

> ⚠️ **Current limitation**: We detect executor-side OOM reliably; driver-side memory issues still require manual investigation.

---

## Layer 5: Warehouse Lock Management Enforcing Single-Writer Integrity

### The Problem

Orchestration systems sometimes mark a task as failed while its underlying warehouse query is still running, typically due to heartbeat loss from network instability. When the task retries, both the orphaned query and the new attempt write to the same table simultaneously. This causes lock contention, data inconsistency, and cascading failures.

### How It Works

We embed a watermark-based duplicate detection system into every warehouse ETL operation:

1. **Tag queries**: Every SQL statement includes a structured comment watermark (e.g., `-- ETL_INCREMENTAL__schema__table --`).
2. **Detect duplicates**: Before executing, query the warehouse's running-queries view for active sessions with the same watermark (excluding the current session).
3. **Cancel orphans**: For each duplicate found:
	- Send a cancellation signal.
		- Log details and alert the team.
		- Wait briefly for locks to release.
		- Verify cancellation before proceeding.
![](https://blogs.halodoc.io/content/images/2026/04/Screenshot-2026-04-21-at-08.54.01.png)

When Airflow loses its heartbeat connection to a running task, typically surfaced as ERROR - Job heartbeat failed, it marks the task as failed and schedules a retry, while the underlying warehouse query continues running unaware. The retrying task then finds an orphaned session still holding a lock on the table, identifies the conflict through its watermark scan, and cancels the blocking process before executing its own write. A notification lands in the team's alert channel confirming what was terminated and on which table, giving engineers full context after the fact, without needing to manually query session history or piece together warehouse logs. The failure resolves itself before most teams would even notice it occurred.

### Key Insight

Watermarks prevent false positives. Incremental and backfill operations use distinct watermarks, allowing them to run concurrently on the same table when appropriate. The approach proved more robust than trying to manage concurrency solely at the orchestration layer.

---

## Layer 6: Cascading Dependency Recovery, Automating Complex Backfills

### The Problem

When a source table in the presentation layer requires a backfill due to schema changes, data fixes, or upstream corrections, the work does not stop there. Every dependent table, and every table depending on *those*, also needs to be rerun. Dependency chains can span 3–4 layers with dozens of tables.

Manually tracing dependencies, determining execution order, and triggering jobs sequentially could take 4–8 hours of active engineering time.

### How It Works

We built a dedicated workflow that automates discovery, ordering, and execution:

1. **Discover dependencies**: Using breadth-first search, traverse configuration tables to build a complete dependency tree (up to a configurable depth).
2. **Execute by layer**: Process tables layer-by-layer, running all tables within a layer in parallel. A gate ensures all tables in layer *N* are complete before layer *N+1* begins.
3. **Support multiple modes**:
	- *Backfill mode*: Trigger new runs for each table with traceable metadata
		- *Clear mode*: Re-run existing failed executions without creating duplicates
4. **Enable selective targeting**: Allow operators to specify which layers to process, avoiding unnecessary wide reprocessing.
![](https://blogs.halodoc.io/content/images/2026/04/Screenshot-2026-04-21-at-08.56.25.png)

When a source table requires correction, the system automatically builds the full dependency tree through Breadth-First Search (BFS) traversal and produces a layered execution plan. All direct dependents run in parallel within the same layer, their children execute only after that layer completes. A single trigger is all that is needed. Once the cascade finishes, a completion notification confirms the start table, the mode used, and which layers were processed — as shown above, where a listener issue on a presentation table triggered a full clear across all five downstream layers automatically.

For the simplified dependency tree sample, here is a clean version:

```json
{
  "start_table": "schema.source_table",
  "layers": [
    [
      "schema.child_table_a",
      "schema.child_table_b",
      "schema.child_table_c"
    ],
    [
      "schema.grandchild_table_x",
      "schema.grandchild_table_y"
    ]
  ]
}
```

### Key Insight

Placing tables at their *maximum* depth in the dependency tree, rather than at first-seen depth. It ensures correct execution order. A table reachable via multiple paths won't run until its deepest upstream dependency completes.

---

## Results: From Firefighting to Focus

The impact of these mechanisms is measurable across both operational efficiency and system reliability. Since implementing these six mechanisms, we have seen measurable improvements:

| Metric | Before | After |
| --- | --- | --- |
| Mean time to recover CDC failures | 45+ minutes | <5 minutes (auto) |
| Manual interventions for memory failures | Daily | Weekly |
| Warehouse lock incidents | Daily | Near-zero |
| Cascading backfill setup time | 4–8 hours | <15 minutes |
| On-call alert volume | 5 alert/week | 1 alert/week |

Beyond these metrics, engineers spend significantly less time on reactive firefighting. The platform handles routine failures automatically, alerts transparently, and escalates only what truly needs human judgement.

---

## What's Next: Evolving the Self-Healing Platform

Self-healing is not a destination, it is a design principle. Areas we are actively exploring:

- **Driver OOM detection**: Extending smart scaling to cover driver-side memory failures.
- **Predictive scaling**: Using historical metrics to pre-scale jobs trending toward OOM *before* the first failure.
- **Adaptive batching**: Dynamically calculating optimal batch sizes based on current resources and historical overhead.
- **Cross-layer orchestration**: Coordinating recovery across layers when failures are causally linked (e.g., a warehouse lock causing lake inconsistency).

---

## Closing Thoughts

Building self-healing infrastructure is not about eliminating human judgement. It is about reserving human judgement for problems that actually need it. The failures we have automated away were never interesting engineering challenges. They were interruptions.

If you are running a data platform at scale and still relying on engineers to manually restart failed tasks, consider this framework:

1. **Start with recurring failures**: Identify failure modes that happen most often.
2. **Build targeted recovery**: One focused mechanism per failure type.
3. **Alert transparently**: Always notify, even when auto-fixing.
4. **Measure impact**: Track reduction in manual interventions.
5. **Iterate**: Move to the next layer once the current one is stable.

The key insight that drove our design: **each failure mode deserves its own recovery logic**. A single generic "retry everything" system can't safely handle the nuances of CDC checkpoint calculation, memory-aware batching, progressive scaling, watermark-based deduplication, and dependency traversal simultaneously. Separating concerns into dedicated layers made each mechanism simpler, safer, and easier to reason about.

The goal is a platform that handles the ordinary, so your team can focus on the extraordinary.

---