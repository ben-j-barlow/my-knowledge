---
tags: [data-n-ai, concept, etl, pipelines]
sources: ["raw/data-n-ai/articles/Why Spark joins are expensive - and what to do about it.md", "raw/data-n-ai/articles/DuckDB Internals Why is DuckDB Fast?.md", "raw/data-n-ai/articles/Lakehouse statistics and why query engines get lost.md"]
updated: 2026-05-20
---

# Query Optimization

The process by which a database engine transforms a logical query plan into an efficient physical execution plan. Covers join strategy selection, predicate/filter pushdown, join order, data skipping, and the role of statistics in making good decisions.

## Distributed Join Strategies

The most consequential optimizer decision in distributed systems. The wrong join strategy can make a query 5–20x slower.

| Strategy | How it works | Memory | Network | Time complexity | Best for |
|---------|-------------|--------|---------|----------------|---------|
| **Broadcast hash join** | Copy small table to every worker; each worker joins its share of the large table against its local copy | High (copy per node) | Low (only small side moved) | O(\|B\|+\|P\|) | Small table fits in per-node memory |
| **Shuffle hash join** | Hash-partition both tables by join key; shuffle to distribute matching keys to same worker; build hash table on partitioned data | Low (partitioned across cluster) | High (both sides shuffled) | O(\|B\|+\|P\|) | Can't broadcast; memory available per partition |
| **Sort/merge join** | Hash-partition and shuffle both sides; sort each partition; merge sorted streams | Low | High (both sides shuffled + sorted) | O(\|B\|log\|B\|+\|P\|log\|P\|) | Memory-scarce; pre-sorted data |

**Rule of thumb**: Broadcast when you have the memory — saves network. Shuffle hash when you can't broadcast. Avoid sort/merge in nearly all cases on modern hardware.

### Sort/Merge Is Spark's Problematic Default
Spark defaults to sort/merge for inputs over 10MB — a threshold calibrated for old, memory-constrained hardware. On modern clusters with gigabytes per node:

| Query | Spark (sort/merge) | Photon (shuffle hash) | Penalty |
|-------|--------------------|-----------------------|---------|
| 1 join (with payload) | 119s | 23s | **5.2x** |
| 2 joins (with payload) | 518s | 27s | **19.2x** |

Sort/merge compounds with additional joins: the large probe table must be sorted once per join. Two joins = O(2\|P\|log\|P\|+...).

### Overriding in Spark
```sql
SELECT /*+ BROADCAST(dim_table) */ ...     -- force broadcast
SELECT /*+ SHUFFLE_HASH(dim, fact) */ ...  -- force shuffle hash
```
Global: `spark.sql.autoBroadcastJoinThreshold` (default 10MB — raise this on modern clusters).

### Adaptive Query Execution (AQE)
Databricks Photon uses runtime statistics to adapt mid-execution: even if the optimizer planned a shuffle hash join, if the build side is small enough at runtime, it switches to broadcast. Inspectable in the Databricks Query History.

## Filter Pushdown / Predicate Pushdown

Move WHERE predicates as close to the data scan as possible — prune rows before they enter later operators (joins, aggregations). The earlier rows are eliminated, the less work downstream operators do.

In DuckDB: the `filter_pushdown` optimizer pass first pulls filters to the top of the plan (to combine and reorganize), then pushes them as far down as possible.

**Dynamic filter pushdown**: after building the hash table for a join, push min/max bounds of the build-side join key back into the probe-side scan as a runtime filter. Row groups outside that range can be skipped before reading.

## Join Order Optimization

The order in which joins execute determines the size of intermediate results. For 6 tables: 30,240 possible tree shapes. Difference between best and worst order: orders of magnitude.

Good join order requires estimating intermediate row counts, which depends on:
- Table sizes
- Predicate selectivity
- Column cardinality

DuckDB uses dynamic programming (DPhyp / DPccp algorithms): solve the best ordering for subsets of tables, then reuse those solutions when extending to larger subsets. The full optimization phase typically completes in ~1ms.

**Without statistics**: the planner guesses from row counts alone → wrong join order → large intermediate results → excessive memory and slow execution. See [Lakehouse Statistics](lakehouse-statistics.md).

## Data Skipping and Zone Maps

Columnar stores organize data into **row groups** (DuckDB: 122,880 rows; Parquet row groups). Each row group carries a **zone map**: min value, max value, null count per column.

On a predicate like `WHERE event_date > '2026-01-01'`, the engine checks each row group's max before reading any data. Row groups with max ≤ the predicate value are skipped entirely.

Zone map effectiveness depends on data ordering:
- Sorted / naturally ordered columns → narrow min-max spans → highly effective skipping
- Randomly scattered values → wide spans → skipping rarely helps

Equivalent techniques: Snowflake "micro-partition pruning", BigQuery "block pruning", ClickHouse `minmax` indexes.

For granular skipping beyond min/max: Bloom filters (definitely not present), Frequent Items sketches (detect skew), quantile sketches (estimate predicate selectivity). See [Lakehouse Statistics](lakehouse-statistics.md).

## The Role of Statistics

Statistics feed every major optimizer decision: join order (cardinality), join strategy (hash table size), predicate selectivity (filter effectiveness), skew handling (MCV). When statistics are missing, the planner guesses — and guesses produce wrong-shaped plans.

In lakehouses (Iceberg, Delta Lake), statistical metadata is largely optional and often not populated. This is the primary reason lakehouse query engines frequently produce suboptimal plans. See [Lakehouse Statistics](lakehouse-statistics.md).

## See Also

- [Lakehouse Statistics](lakehouse-statistics.md)
- [DuckDB](../entities/duckdb.md)
- [Apache Spark](../entities/apache-spark.md)
- [Databricks](../entities/databricks.md)
- [Source: Spark Join Strategies](../sources/spark-join-strategies.md)
- [Source: DuckDB Internals Part 1](../sources/duckdb-internals-part1.md)
