---
tags: [data-n-ai, concept, etl, pipelines, lakehouse]
sources: ["raw/data-n-ai/articles/2025-10-10-tech-review-ducklake-from-parquet-to-powerhouse.md", "raw/data-n-ai/articles/2026-10-06-ducklake-in-production-maintenance-strategy.md", "raw/data-n-ai/articles/2026-09-13-my-duckdb-ai-workflow.md", "raw/data-n-ai/articles/2026-09-11-duckdb-400k-skill.md"]
updated: 2026-10-17
---

# DuckLake

Open lakehouse table format from the [DuckDB](../entities/duckdb.md) team: **data in Parquet files on object storage or local disk, all metadata in a SQL database** (DuckDB, SQLite, Postgres, or MySQL). Provides ACID transactions, snapshots/time travel, schema evolution and commit history using standard SQL, with no catalog service or cluster.

## How It Differs from Iceberg

[Apache Iceberg](apache-iceberg.md) keeps metadata in files (manifests, metadata JSON) next to the data and usually needs a separate catalog service. DuckLake puts the catalog in a relational database, so:

- Deletes are rows in the catalog referencing data/delete files; queries consult the catalog to skip deleted rows.
- Setup is `INSTALL ducklake; ATTACH 'ducklake:...'` — locally a single file; production is typically **Postgres catalog + S3 data** (e.g. Supabase + S3).
- Small inserts (<10 rows by default) are **inlined** into catalog tables rather than written as tiny Parquet files, to avoid the small-file problem.
- Maintenance concerns shift to the catalog DB and object store (below).

## Core Features

| Feature | Notes |
|---------|-------|
| Snapshots / time travel | `ducklake_snapshots()`, `AT (VERSION => n)`; every DDL/DML creates a snapshot |
| Commit metadata | `set_commit_message(author, message, extra_info)` inside a transaction |
| Schema evolution | `ADD/DROP COLUMN` with defaults, no rewrite of existing Parquet |
| Partitioning | Hive-style, applies only to newly written data; usually unnecessary at small scale |
| Updates/deletes | Plain SQL `UPDATE`/`DELETE` over Parquet |

## Production Maintenance

Maintenance is on you in open-source lakehouses. Design it around **ingestion pattern** (streaming/tiny inserts → flush inlined data; batch appends → compact files) and **time-travel policy** (how long to retain snapshots *and* their files). Functions: `ducklake_flush_inlined_data`, `ducklake_expire_snapshots`, `ducklake_merge_adjacent_files`, `ducklake_rewrite_data_files`, `ducklake_cleanup_old_files`, `ducklake_delete_orphaned_files`, or all via `CHECKPOINT`. Always `dry_run => true` first; keep a grace window on file cleanup so in-flight queries aren't broken. Worked 7-day-window example in [the maintenance source](../sources/2026-10-06-ducklake-maintenance-strategy.md).

## Agent Angle

A Postgres-catalog DuckLake lets multiple agents/processes read concurrently, unlike a single DuckDB file (one connection) — see [DuckDB for Agents](duckdb-for-agents.md) and [CLI Tools for Agents](cli-tools-for-agents.md). Persistent DuckDB secrets let an agent `ATTACH` the lake without seeing credentials. The author's suggested production step is to give the maintenance commands to an agent to schedule.

## Limits and Open Questions

- Evidence is practitioner tutorials from one author (one piece sponsored by MotherDuck); no benchmarks or large-scale/concurrent-writer reports in the wiki.
- **Date discrepancy**: the [$400K-skill source](../sources/duckdb-400k-skill.md) (and the DuckDB page) date DuckLake to April 2026, but Emerson's tech review is dated 2025-10-10, so it existed at least by then. Treat the April 2026 date as unverified (possibly a later milestone/release).

## See Also

- [Hive-Style Data Lake Limitations](hive-style-data-lake-limitations.md) · [Data Layout](data-layout.md) · [Lakehouse Statistics](lakehouse-statistics.md)
- [Guide: Building a DuckLake from Scratch](../../outputs/data-n-ai/2026-10-21-building-a-ducklake-from-scratch.md) — catalog choice, setup, maintenance, dashboard read patterns
- [Data Versioning and Branching](data-versioning-and-branching.md) — DuckLake snapshots vs Iceberg branches vs native-DuckDB `differential` branches
- [Source: DuckLake Tech Review](../sources/2025-10-10-ducklake-tech-review.md)
- [Source: DuckLake in Production: Maintenance Strategy](../sources/2026-10-06-ducklake-maintenance-strategy.md)
- [DuckDB 2.0](duckdb-2-0.md) — DuckLake 1.1 (new spec + reference implementation) released alongside 2.0, 2026-10-21; not yet ingested in detail
