---
tags: [data-n-ai, source, pipelines, etl]
sources: [raw/data-n-ai/articles/Building Self-Healing Data Pipelines at Halodoc.md]
updated: 2026-05-20
---

# Building Self-Healing Data Pipelines at Halodoc

> Source: https://blogs.halodoc.io/building-self-healing-data-pipelines-at-halodoc/
> Author: Dana Rabba (Halodoc)
> Published: 2026-05-04

## Summary

Halodoc decomposed data pipeline failure modes into six targeted recovery layers, each with its own automated recovery mechanism. The shift: from paging engineers at 2am to a platform that handles routine failures autonomously and surfaces only what genuinely needs human judgment. CDC recovery time dropped from 45+ minutes to under 5 minutes; on-call alert volume dropped from ~5/week to ~1/week.

## Key Claims

### Design Principles
- **Alert first, act second**: automation always notifies before and after acting, creating an audit trail even on auto-fixed failures
- **Fix the foundation before downstream**: early implementations triggered downstream backfills before fixing the source data — fixed downstream tables built on inconsistent upstream data just propagated the problem
- **One recovery mechanism per failure mode**: generic "retry everything" can't safely handle CDC checkpoint math, memory-aware batching, lock deduplication, and dependency traversal simultaneously

### Six Recovery Layers

| Layer | Failure mode | Recovery mechanism |
|-------|-------------|-------------------|
| 1. CDC Auto-Recovery | CDC task fails (binary log rotation, memory, network) | Detect failed tasks, apply 3-gate eligibility check (task type, current state, error classification), calculate safe checkpoint with configurable buffer, restart |
| 2. Source-vs-Lake Consistency | Data stalls between layers; dashboards show stale data | Scheduled comparison of source and destination (row counts, unique IDs); trigger bronze-to-silver backfill first, then downstream |
| 3. Mini-Batch Processing | Backlog exceeds executor memory after outage | File-size-aware batching (cumulative size, not count/time window); process sequential 2GB batches; checkpoint after each batch |
| 4. Smart Memory Scaling | OOM from transformation complexity (joins, shuffles) | Airflow `on_retry_callback` inspects failure reason; if OOM: +25%/+40%/+60% memory on retries 1/2/3+ |
| 5. Warehouse Lock Management | Orphaned queries from failed runs block new writes | SQL comment watermarks on every ETL statement; scan running-queries view before execution; cancel orphans before proceeding |
| 6. Cascading Dependency Recovery | Backfill of one table requires rerunning all dependents | BFS dependency traversal; layer-by-layer execution (all tables in layer N in parallel, layer N+1 waits); backfill and clear modes |

### Layers 3 vs 4 Are Complementary
- Layer 3 addresses OOM from **input data volume** (bronze layer, file accumulation)
- Layer 4 addresses OOM from **transformation complexity** (silver layer, joins and shuffles)

### CDC Eligibility Gate (Layer 1)
Three checks that evolved to reduce false restarts to near zero:
1. Task type: only incremental CDC qualifies (full-load needs human review)
2. Current state: still failed (avoid interrupting manual fixes in progress)
3. Error classification: only restart for known recoverable errors

### Dependency Recovery Details (Layer 6)
Tables placed at their **maximum depth** in the BFS tree, not first-seen depth — ensures correct execution when a table is reachable via multiple paths.

### Results

| Metric | Before | After |
|--------|--------|-------|
| Mean time to recover CDC failures | 45+ minutes | <5 minutes (auto) |
| Manual interventions for memory failures | Daily | Weekly |
| Warehouse lock incidents | Daily | Near-zero |
| Cascading backfill setup time | 4–8 hours | <15 minutes |
| On-call alert volume | ~5/week | ~1/week |

## Related Wiki Pages

- [Self-Healing Pipelines](../concepts/self-healing-pipelines.md)
- [Data Ingestion](../concepts/data-ingestion.md)
- [Event-Driven Architecture](../concepts/event-driven-architecture.md)
