---
tags: [data-n-ai, concept, pipelines, etl]
sources: [raw/data-n-ai/articles/Building Self-Healing Data Pipelines at Halodoc.md]
updated: 2026-05-20
---

# Self-Healing Data Pipelines

Design pattern where a data platform automatically detects and recovers from common failure modes without human intervention. The goal is not to eliminate human judgment — it is to reserve it for failures that genuinely need it, and to stop waking engineers at 2am for routine restarts.

## Core Principles

1. **Alert first, act second**: automation notifies the team before and after acting. Engineers see what happened even when the system fixed it automatically — the audit trail is not optional.
2. **Fix the foundation before downstream**: healing dependent tables before fixing the upstream source they depend on propagates bad data, not a fix. Always resolve the earliest broken layer first.
3. **One mechanism per failure mode**: a generic "retry everything" system can't safely handle CDC checkpoint math, memory-aware batching, lock deduplication, and dependency traversal simultaneously. Separation of concerns makes each mechanism simpler and safer.
4. **Measure reduction in manual interventions**: the right metric is not system uptime — it is how much firefighting was eliminated.

## Six Recovery Layers

### Layer 1: CDC Auto-Recovery
**Failure mode**: CDC replication stops due to binary log rotation, memory exhaustion, or transient network issues.

**Recovery**: Scheduled scan for failed CDC tasks → three-gate eligibility check → safe checkpoint calculation (with configurable time buffer to avoid data gaps) → restart.

Three eligibility gates (evolved through iteration; without them, too many non-recoverable failures were retried):
1. Task type: only incremental CDC qualifies; full-load needs human review
2. Current state: confirm still failed; avoid interrupting an in-progress manual fix
3. Error classification: only restart for known recoverable error patterns

**Design principle**: favor data completeness over duplicate risk. Downstream systems typically handle idempotency well; they handle data gaps poorly.

### Layer 2: Source-vs-Lake Consistency
**Failure mode**: CDC is healthy but data stalls between layers; dashboards show stale data before anyone notices.

**Recovery**: Scheduled comparison of source vs. destination using unique identifier validation (not just row counts) → flag mismatched tables → backfill bronze-to-silver first, then downstream.

### Layer 3: Mini-Batch Processing (Volume OOM)
**Failure mode**: After an outage, files accumulate. The backlog exceeds executor memory. Recovery attempt itself OOMs. Cycle repeats.

**Recovery**: Before processing, assign batch IDs based on cumulative file size (e.g. 2GB threshold). Process sequentially, releasing memory between batches. Checkpoint after each batch — the next run picks up only remaining files.

**Example**: 15GB backlog, 8GB executor → without batching: OOM loop. With batching: 8 sequential 2GB batches → completes reliably.

**Why cumulative size, not count or time window**: file sizes and arrival rates vary dramatically; count-based and time-window batching broke down in practice.

### Layer 4: Smart Memory Scaling (Computation OOM)
**Failure mode**: OOM from transformation complexity (joins, shuffles, aggregations) — distinct from Layer 3's volume problem.

**Recovery**: Airflow `on_retry_callback` intercepts the retry. Query runtime metrics to confirm OOM (vs. spot interruption, script error). If OOM: scale executor memory progressively — +25% / +40% / +60% on retries 1/2/3+. Notify team with before/after config.

**Secondary use**: recurring OOM alerts on the same task signal its baseline configuration needs a permanent increase, not just one-time retry boosts.

**Known limitation**: executor-side OOM detection is reliable; driver-side memory issues still require manual investigation.

### Layer 5: Warehouse Lock Management
**Failure mode**: Airflow loses its heartbeat to a running task, marks it failed, schedules a retry — but the warehouse query is still running. Two concurrent writes to the same table → lock contention, data inconsistency.

**Recovery**: Tag every SQL statement with a structured comment watermark (e.g. `-- ETL_INCREMENTAL__schema__table --`). Before executing, scan running queries for sessions with the same watermark (excluding self). Cancel orphans → wait for lock release → proceed.

**Why watermarks over session management**: incremental and backfill operations use distinct watermarks and can run concurrently on the same table when appropriate. Cleaner than managing concurrency purely at the orchestration layer.

### Layer 6: Cascading Dependency Recovery
**Failure mode**: fixing one source table requires rerunning every downstream table, and every table depending on those. Dependency chains spanning 3–4 layers with dozens of tables. Without automation: 4–8 hours of active engineering.

**Recovery**: BFS traversal of dependency configuration tables → build a complete dependency tree → execute layer by layer (all tables within a layer in parallel; gate between layers). Backfill mode (new runs) and clear mode (re-run existing failed executions) both supported.

**Key implementation detail**: place tables at their maximum depth in the BFS tree, not first-seen depth. A table reachable via multiple paths won't run until its deepest upstream dependency completes.

## Results (Halodoc)

| Metric | Before | After |
|--------|--------|-------|
| Mean time to recover CDC failures | 45+ minutes | <5 minutes (auto) |
| Manual interventions for memory failures | Daily | Weekly |
| Warehouse lock incidents | Daily | Near-zero |
| Cascading backfill setup time | 4–8 hours | <15 minutes |
| On-call alert volume | ~5/week | ~1/week |

## See Also

- [Data Ingestion](data-ingestion.md)
- [Event-Driven Architecture](event-driven-architecture.md)
- [Source: Building Self-Healing Data Pipelines at Halodoc](../sources/halodoc-self-healing-pipelines.md)
