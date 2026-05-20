---
tags: [data-n-ai, source, etl, pipelines]
sources: [raw/data-n-ai/articles/Why Spark joins are expensive - and what to do about it.md]
updated: 2026-05-20
---

# Why Spark Joins Are Expensive — And What To Do About It

> Source: https://floedb.ai/blog/why-spark-joins-are-expensive-and-what-to-do-about-it
> Author: Database Doctor (FloeDB)
> Published: 2026-05-14

## Summary

"Joins are expensive" in Spark is largely a myth created by Spark's conservative default configuration (sort-merge join for anything over 10MB). The join itself isn't expensive — Spark's default algorithm choice is. Switching to broadcast or shuffle hash join delivers 2–19x improvements depending on the workload. Databricks Photon handles this automatically by preferring shuffle hash and adapting at runtime.

## Key Claims

### Three Join Strategies

| Strategy | Network | Memory | Time complexity | When to use |
|---------|---------|--------|----------------|-------------|
| Broadcast hash join | Low (small side only) | High (copy of hash table on every node) | O(\|B\|+\|P\|) | Small table fits in memory on each node |
| Shuffle hash join | High (both sides shuffled) | Low (partitioned across cluster) | O(\|B\|+\|P\|) | Can't broadcast; memory available for hash table |
| Sort/merge join | High (both sides sorted + shuffled) | Low | O(\|B\|log\|B\|+\|P\|log\|P\|) | Memory-scarce systems; pre-sorted data |

### Benchmarks on TPC-DS (2.8B row `store_sales`, 4-worker cluster)

| Query | Spark (sort/merge) | Databricks Photon |
|-------|--------------------|------------------|
| Join with `item` (2.4MB) | 6.1s | 5.8s |
| Join with `customer` (96MB) | 38s | **8.7s** |
| 1 join (with payload) | 119s | 23s |
| **2 joins (with payload)** | **518s** | **27s** |

- Sort/merge penalty: **5.2x** for 1 join, **19.2x** for 2 joins
- Sort/merge requires sorting `P` (the large table) once per join — cost compounds with join count

### Sort/Merge Is Bad for Most Cases
- Interacts poorly with CPU branch predictor and has bad memory access patterns
- Spark's default broadcast threshold: **10MB** — vastly too conservative for modern hardware
- Most Spark clusters have gigabytes of memory per node, not megabytes
- Hypothesis: the "joins are expensive" belief among Spark users is an artifact of running with this default configuration, not an inherent property of joins

### Databricks Photon Advantages
- Prefers shuffle hash join by default (not sort/merge)
- **Adaptive**: runtime plan may switch from planned shuffle hash to broadcast if possible (shown in Query History)
- `PhotonShuffledHashJoin` vs Spark's `SortMergeJoin` — same logical query, dramatically different execution

### How to Override in Spark

```sql
-- Force broadcast join
SELECT /*+ BROADCAST(DC) */ SUM(ss_sales_price)
FROM store_sales JOIN customer DC ON ss_customer_sk = c_customer_sk;

-- Force shuffle hash join  
SELECT /*+ SHUFFLE_HASH(DC, F) */ SUM(ss_sales_price)
FROM store_sales F JOIN customer DC ON ss_customer_sk = c_customer_sk;
```

Also configurable globally: `spark.sql.autoBroadcastJoinThreshold` (default: 10MB, usually should be raised).

### Rule of Thumb
> "When you have the memory — pick broadcast and save your network. If low on memory, pick shuffle hash. Avoid sort/merge in nearly all cases."

## Related Wiki Pages

- [Apache Spark](../entities/apache-spark.md)
- [Databricks](../entities/databricks.md)
- [Query Optimization](../concepts/query-optimization.md)
- [Lakehouse Statistics](../concepts/lakehouse-statistics.md)
- [FloeDB](../entities/floedb.md)
