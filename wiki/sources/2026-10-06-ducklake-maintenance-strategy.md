---
tags: [data-n-ai, source, etl, pipelines, lakehouse]
sources: ["raw/data-n-ai/articles/2026-10-06-ducklake-in-production-maintenance-strategy.md"]
updated: 2026-10-17
---

# Source: DuckLake in Production: Maintenance Strategy

**Author**: Hoyt Emerson (The Full Data Stack)
**Published**: 2026-10-06 · **URL**: https://thefulldatastack.substack.com/p/ducklake-in-production-maintenance
**Type**: Practitioner tutorial; part 3 of a "production DuckLake" mini-series. Sponsored by MotherDuck (uses MotherDuck Flights for scheduling).

## Core Claim

Getting a DuckLake running is easy; keeping it healthy needs an explicit maintenance strategy, driven by two things: **ingestion pattern** and **time-travel policy**. As AI makes non-technical stakeholders query data directly ("Claude Pilled" orgs), small teams can no longer treat maintenance as someone else's job — open-source lakehouses don't hide it the way BigQuery does.

## Key Claims

- **Catalog-in-a-database changes the maintenance profile.** Deletes are recorded in the catalog separately from Parquet; queries use catalog metadata to skip deleted rows. See [DuckLake](../concepts/ducklake.md).
- **Data inlining**: inserts under 10 rows by default go into catalog tables, not Parquet files (avoids small files), until flushed by `ducklake_flush_inlined_data` or `CHECKPOINT`. Streaming / tiny inserts → flush; otherwise a Postgres catalog eventually struggles reading inlined data.
- **Batch appends (>10 rows)** → no flush needed, but run **compaction** to keep a few large Parquet files.
- **Time-travel policy** = how long to keep snapshots *and* their data files. Expiring snapshots and deleting files ends time travel to those versions.

## The Six Maintenance Functions

`ducklake_flush_inlined_data`, `ducklake_expire_snapshots`, `ducklake_merge_adjacent_files`, `ducklake_rewrite_data_files`, `ducklake_cleanup_old_files`, `ducklake_delete_orphaned_files` — all runnable at once via `CHECKPOINT`, or à la carte.

## Worked Example (SMB on AWS)

Setup: S3 data + Supabase Postgres catalog; users get local credentials and use DuckDB CLI/UI; Postgres replica and gold table **recreated daily** (drop + create), scheduled by MotherDuck Flights. Result: one live data file, but many snapshots and old Parquet files in S3.

Policy: 7-day rolling window. Daily routine after the gold build:

1. `CALL ducklake_expire_snapshots('my_ducklake', older_than => now() - INTERVAL '7 days');`
2. `CALL ducklake_cleanup_old_files('my_ducklake', dry_run => false, older_than => now() - INTERVAL '1 hour');` — the 1-hour grace stops in-flight queries on older snapshots losing files.
3. `CALL ducklake_delete_orphaned_files('my_ducklake', dry_run => false);` — removes files no longer tracked by the catalog (the author found one he didn't know existed).

All functions take `dry_run => true` — run it first. The author's "production-grade" step is to hand these commands to an agent to build the scheduled pipeline.

## Caveats

- Sponsored; one small-team, daily-batch, full-refresh scenario. No guidance on append-heavy tables (compaction/rewrite are listed but not demonstrated) or concurrent writers.
- Daily drop-and-recreate sidesteps small-file growth; results won't transfer directly to incremental pipelines.

## See Also

- [DuckLake](../concepts/ducklake.md) · [DuckDB](../entities/duckdb.md)
- [Source: DuckLake Tech Review](2025-10-10-ducklake-tech-review.md)
- [Source: My DuckDB + AI Workflow](2026-09-13-duckdb-ai-workflow.md) — same author; production DuckLake = Postgres catalog + S3
