---
tags: [data-n-ai, source, etl, pipelines, lakehouse]
sources: ["raw/data-n-ai/articles/Debunking 8 data layout myths why Liquid Clustering outperforms partitioning.md"]
updated: 2026-06-05
---

# Source: Debunking 8 Data Layout Myths — Why Liquid Clustering Outperforms Partitioning

**Authors:** Jeffrey Gong, Yu Xu, Rahul Mahadev (Databricks)
**Published:** 2026-06-01
**URL:** https://www.databricks.com/blog/debunking-8-data-layout-myths-why-liquid-clustering-outperforms-partitioning

> ⚠️ **Vendor content.** Databricks advocating its own Liquid Clustering feature; benchmarks are self-reported and partitioning is shown at its worst. The *mechanism* claims are architecturally sound and vendor-independent; treat the magnitudes as best-case.

## Thesis

For 15+ years, Hive-style partitioning was the standard way to physically lay out lakehouse data. It forces an irreversible choice at table-creation time and **over-partitions / creates small files in >75% of cases**. [Liquid Clustering](../concepts/data-layout.md) treats clustering keys as a hint the engine uses to organise files (changeable anytime, or auto-selected), removing the cardinality constraint and the small-file problem. In 2026, with agents and real-time pipelines generating query patterns faster than humans can re-partition, layout *should* be an implementation detail of the table.

## The 8 myths (and the rebuttals)

1. **Directory pruning** — doesn't exist on Delta/Iceberg. Pruning is against per-file stats in the transaction log, at file granularity. No directory shortcut to lose.
2. **Low-cardinality filters** — Liquid auto-detects low cardinality (single-value-per-file) and uses higher-cardinality keys for finer in-file sorting. Benchmark: 35% lower clustering time, 22% faster queries.
3. **Metadata-only ops** — Liquid supports metadata-only DELETE/COUNT/DISTINCT/GROUP BY via the same min/max stats. ~90% faster DELETEs; up to 27× on aggregates.
4. **PB scale** — dozens of PB-scale Liquid tables in prod. OPTIMIZE planning cut 12h → 23min on a 10 PB table; execution 5× faster.
5. **Only Databricks readers benefit** — it's a write-side optimisation producing standard Parquet + stats; any reader (OSS Spark, DuckDB) skips files using them.
6. **Concurrent ETL needs partitioning** — row-level concurrency lets two writers touch different rows in the same file without conflict; no need to partition for write boundaries.
7. **Z-Ordering saves partitioning** — Z-Order has poor clustering quality (wide per-file ranges) and rewrites already-clustered data on each rerun. Liquid clusters incrementally.
8. **Selective overwrites need Dynamic Partition Overwrite** — `REPLACE USING` / `REPLACE ON` work on any layout, any compute (classic/SQL/Serverless), atomically.

## Success stories

- **Arctic Wolf** — 3.8 PB security telemetry, 1T+ events/day. Partition→Liquid: 90-day queries 51s→6.6s (7.7×); files 4M→2M; freshness hours→minutes.
- **Bolt** — TB-scale CDC, in-place Liquid Conversion (Private Preview, `ALTER TABLE ... REPLACE PARTITIONED BY WITH CLUSTER BY`): write throughput +138%; reads −21% avg (−63% peak).
- **Databricks internal** — 1.1 PB; date/hour partitioning → date/hour/source/id clustering: 406s→70s (5.9×); bytes read 3.5 TB→0.48 TB (−86%); size 1.1 PB→0.8 PB (−27%).

## What's coming

- **Co-clustered joins** (Private Preview): Liquid-to-Liquid joins on clustering columns avoid full shuffle — ~51% faster (28→14 min), 87% less shuffle (1.2 TiB→150 GiB).
- **Easy Liquid Conversion** (Private Preview): convert partitioned tables in-place, minimising downtime/rewrites.

## Notable quote

> "In 2026, the layout *should* be an implementation detail of the table, with every engine that reads or writes benefitting from it."

## Related Pages

- [Data Layout](../concepts/data-layout.md)
- [Query Optimization](../concepts/query-optimization.md)
- [Lakehouse Statistics](../concepts/lakehouse-statistics.md)
- [Databricks](../entities/databricks.md)
