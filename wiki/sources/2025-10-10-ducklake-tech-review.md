---
tags: [data-n-ai, source, etl, pipelines, lakehouse]
sources: ["raw/data-n-ai/articles/Tech Review DuckLake - From Parquet to Powerhouse.md"]
updated: 2026-10-17
---

# Source: Tech Review: DuckLake — From Parquet to Powerhouse

**Author**: Hoyt Emerson (The Full Data Stack)
**Published**: 2025-10-10 · **URL**: https://thefulldatastack.substack.com/p/tech-review-ducklake-from-parquet
**Type**: Hands-on tutorial / enthusiastic review (DuckLake CLI, local, clean synthetic dataset; no benchmarks)

## Core Claim

[DuckLake](../concepts/ducklake.md) delivers lakehouse features — ACID transactions, time travel, schema evolution, commit history — over plain folders of Parquet with almost no infrastructure, positioned as a far simpler alternative to [Apache Iceberg](../concepts/apache-iceberg.md) for teams with modest data volumes.

## Walkthrough (what the author demonstrates)

| Step | Command / behaviour |
|------|---------------------|
| Create | `INSTALL ducklake; ATTACH 'ducklake:my_ducklake.ducklake' AS my_ducklake;` — metadata in a DuckDB file (SQLite, Postgres, MySQL also supported) |
| Load | `CREATE TABLE t AS FROM 'path'` — file type inferred (CSV here); Parquet written to `<name>.ducklake.files/` |
| Update | Plain `UPDATE ... SET` works on what is physically a Parquet folder |
| Snapshots | `FROM ducklake_snapshots('my_ducklake')`; time travel with `FROM t AT (VERSION => 1)` |
| Schema evolution | `ALTER TABLE ADD/DROP COLUMN` (incl. defaults) each create a snapshot |
| Commit metadata | `BEGIN; ...; CALL my_ducklake.set_commit_message(author, message, extra_info => ...); COMMIT;` fills the author/message columns of the snapshot |
| Partitioning | `ALTER TABLE t SET PARTITIONED BY (year(ts), month(ts))` — Hive-style layout; applies only to **newly written** data, not existing Parquet |

## Key Claims

- Snapshots are "the heart of a lakehouse" and give time travel, lineage/governance, error recovery, historical analysis.
- Partitioning is usually unnecessary until data is large, and over-partitioning creates the small-file problem (consistent with [Data Layout](../concepts/data-layout.md)).
- Author declines to re-check whether Iceberg got easier, because DuckLake "will meet the needs that I have with my data volumes" — a small-data framing.

## Caveats

- Vendor-adjacent enthusiasm ("AMAZING!", "magical"); the dataset is "clean and perfect on purpose".
- Single-user local demo: no concurrency, scale, or cost evidence. Maintenance (compaction, snapshot expiry) is not covered — see [DuckLake in Production: Maintenance Strategy](2026-10-06-ducklake-maintenance-strategy.md).
- Dated 2025-10, so earlier than the DuckLake dates cited elsewhere in the wiki (see note on [DuckLake](../concepts/ducklake.md)).

## See Also

- [DuckLake](../concepts/ducklake.md) · [DuckDB](../entities/duckdb.md)
- [Hive-Style Data Lake Limitations](../concepts/hive-style-data-lake-limitations.md)
