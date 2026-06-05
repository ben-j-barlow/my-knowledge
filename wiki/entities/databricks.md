---
tags: [data-n-ai, entity, etl, pipelines]
sources: ["raw/data-n-ai/articles/Why Spark joins are expensive - and what to do about it.md", "raw/data-n-ai/articles/Debunking 8 data layout myths why Liquid Clustering outperforms partitioning.md"]
updated: 2026-06-05
---

# Databricks

Cloud data and AI platform built on [Apache Spark](apache-spark.md). Key differentiators: Photon (vectorized C++ execution engine), serverless SQL Warehouses, Delta Lake (open table format), and Unity Catalog (data governance).

## Photon Execution Engine

Databricks' proprietary vectorized execution engine, replacing the default JVM-based Spark executor. Written in C++ for better CPU cache utilisation and SIMD vectorization.

Key behavioral differences from vanilla Spark:
- **Prefers shuffle hash join** over sort/merge — dramatically better for most analytical workloads
- **Adaptive join selection at runtime**: even if the optimizer planned shuffle hash, Photon may switch to broadcast at runtime if actual data sizes warrant it (visible in Query History)
- Consistently 2–20x faster than vanilla Spark for join-heavy workloads (benchmark: 1 join 5.2x better, 2 joins 19.2x better vs Spark sort/merge)

## Serverless SQL Warehouses

Managed compute for SQL workloads. Spins up immediately (vs ~10 minutes for raw Spark clusters on spot instances). Billed in DBUs (Data Brownfield Units) per hour. Small warehouse (~4 workers) appropriate for TPC-DS scale factor 1000 queries.

## Delta Lake

Open table format for lakehouses. Provides ACID transactions, time travel (table history), schema enforcement, and efficient upserts (MERGE). Statistical metadata stored in the Delta log and Unity Catalog (API-only access).

Note: Delta Lake stats are stored separately from Iceberg's Puffin files — cross-engine stat sharing between Databricks and Iceberg-native engines is non-trivial. See [Lakehouse Statistics](../concepts/lakehouse-statistics.md).

## Liquid Clustering

Databricks' modern data-layout strategy and the proposed replacement for Hive-style partitioning. Clustering keys are treated as an *input the engine uses* to organise files (not baked into the directory structure), so keys can change at any time and cardinality isn't a constraint. GA in 2024. See [Data Layout](../concepts/data-layout.md) for the full partitioning-vs-clustering comparison.

Key properties:
- **No small-file problem / no cardinality limit** — always targets good file sizes; supports multi-dimensional clustering (e.g. time *and* identifier columns at once, replacing partition+Z-Order).
- **Incremental clustering** (including at write time) → lower write amplification, no periodic full rewrites the way `OPTIMIZE ZORDER BY` requires.
- **Row-level concurrency** — two writers updating different rows in the same file don't conflict, removing the need to partition just to separate writers ([deep dive](https://www.databricks.com/blog/deep-dive-how-row-level-concurrency-works-out-box)).
- **Write-side optimisation** — output is standard Parquet + min/max stats in Delta/Iceberg, so any compatible reader (OSS Spark, DuckDB) benefits, not just Databricks.
- **Automatic Liquid Clustering** — with UC managed tables + Predictive Optimization, the system selects clustering keys from observed query patterns.

Related features: `REPLACE USING` / `REPLACE ON` for selective overwrites on any layout/compute; **co-clustered joins** (Private Preview) that skip the shuffle on Liquid-to-Liquid joins (~51% faster, 87% less shuffle); in-place **Liquid Conversion** of partitioned tables (Private Preview).

## Predictive Optimization

Managed background optimisation for Unity Catalog managed tables — runs OPTIMIZE/clustering/vacuum automatically. Pairs with Automatic Liquid Clustering to keep layout optimal without manual tuning.

## Unity Catalog

Data governance layer: centralised metadata, lineage, access control across workspaces. Statistical metadata for Delta tables is stored here and accessible via API.

## See Also

- [Apache Spark](apache-spark.md)
- [Data Layout](../concepts/data-layout.md)
- [Query Optimization](../concepts/query-optimization.md)
- [Lakehouse Statistics](../concepts/lakehouse-statistics.md)
- [Source: Spark Join Strategies](../sources/spark-join-strategies.md)
- [Source: Debunking 8 Data Layout Myths (Liquid Clustering)](../sources/2026-06-01-liquid-clustering-vs-partitioning.md)
