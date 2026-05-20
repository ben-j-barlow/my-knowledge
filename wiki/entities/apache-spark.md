---
tags: [data-n-ai, entity, etl, pipelines]
sources: [raw/data-n-ai/articles/Why Spark joins are expensive - and what to do about it.md]
updated: 2026-05-20
---

# Apache Spark

Distributed data processing framework. The dominant engine for large-scale batch and streaming data transformations across a cluster of workers. Written primarily in Scala/Java; exposed via Python (PySpark), SQL (SparkSQL), and other language APIs.

## Core Concepts

- **Driver**: the process that plans the query and coordinates workers
- **Executor/Worker**: the processes that actually process data; each gets a share of the input and memory
- **Shuffle**: redistributing data across workers by partitioning on a key — the dominant source of network I/O in Spark jobs
- **DataFrame / Dataset**: the structured data abstraction; SparkSQL queries compile to the same physical plan

## Join Strategies

Spark's join strategy selection is the most consequential performance variable for analytical queries. See [Query Optimization](../concepts/query-optimization.md) for full comparison.

| Strategy | Spark default? | Notes |
|---------|--------------|-------|
| Sort/merge join | Yes, for inputs >10MB | Sorts and shuffles both sides; bad memory access patterns; degrades badly with multiple joins |
| Broadcast hash join | Only for inputs ≤10MB | Best performance when small side fits in per-node memory; Spark's 10MB threshold is too conservative |
| Shuffle hash join | Not default | Databricks Photon prefers this; faster than sort-merge when memory is available |

### The 10MB Problem
Spark's default `spark.sql.autoBroadcastJoinThreshold` is **10MB**. On a 4-worker cluster with gigabytes of RAM per node, a 96MB dimension table still gets sort-merge join by default. Raising this threshold or using query hints is almost always worth doing.

### Query Hints
```sql
SELECT /*+ BROADCAST(dim) */ ...       -- force broadcast
SELECT /*+ SHUFFLE_HASH(dim, fact) */ ... -- force shuffle hash
```

### Adaptive Query Execution (AQE)
When enabled, Spark can switch join strategies at runtime based on actual data statistics, rather than just planned estimates. Databricks Photon uses this aggressively.

## Self-Healing Integration

Spark jobs are a common source of OOM failures in data pipelines. Self-healing systems intercept Airflow retry callbacks to detect OOM errors and progressively scale executor memory (+25%/+40%/+60%) before re-dispatch. See [Self-Healing Pipelines](../concepts/self-healing-pipelines.md).

## See Also

- [Databricks](databricks.md)
- [Query Optimization](../concepts/query-optimization.md)
- [Lakehouse Statistics](../concepts/lakehouse-statistics.md)
- [Self-Healing Pipelines](../concepts/self-healing-pipelines.md)
- [Source: Spark Join Strategies](../sources/spark-join-strategies.md)
