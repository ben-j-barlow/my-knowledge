---
tags: [data-n-ai, entity, etl, pipelines]
sources: [raw/data-n-ai/articles/Why Spark joins are expensive - and what to do about it.md]
updated: 2026-05-20
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

Advanced data clustering strategy that organizes data to improve range statistics and data skipping effectiveness. Alternative to static partition schemes that degrade over time as data patterns change.

## Unity Catalog

Data governance layer: centralised metadata, lineage, access control across workspaces. Statistical metadata for Delta tables is stored here and accessible via API.

## See Also

- [Apache Spark](apache-spark.md)
- [Query Optimization](../concepts/query-optimization.md)
- [Lakehouse Statistics](../concepts/lakehouse-statistics.md)
- [Source: Spark Join Strategies](../sources/spark-join-strategies.md)
