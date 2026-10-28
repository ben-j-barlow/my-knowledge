---
tags: [data-n-ai, entity, agents, pipelines, lakehouse]
sources: ["raw/data-n-ai/articles/2026-10-15-duckdb-snapshots-time-travel-and-writable-branches.md"]
updated: 2026-10-28
---

# duckdb-differential

DuckDB community extension by [Tobias Müller](tobias-mueller.md) that versions a **native DuckDB database** from SQL: snapshots, time travel, writable branches, clones, restore, and optional S3 publication/recovery. Repo: https://github.com/tobilg/duckdb-differential.

- **Status**: experimental; targets DuckDB 1.5.6 on Linux and macOS.
- **Install**: `INSTALL differential FROM community; LOAD differential; SET differential_repository = '/abs/path'; ATTACH 'differential:<db>' AS x;`
- **Key calls**: `differential_create_snapshot`, `differential_create_branch`, `differential_clone_database`, `differential_restore`, `differential_import_database`, `differential_recover_export`, `differential_retry_export`.
- **Storage**: immutable ~64 KiB chunks + mappings in a local repository coordinated by embedded SQLite; unchanged chunks are shared across versions.
- **Concurrency**: one writer process per branch; optional `WRITERS 'shared'` mode for multi-host writes via conditional S3 head updates.
- **Limits**: no automatic merge, no security sandbox, manual retention, no remote GC.

Concepts and use cases: [Data Versioning and Branching](../concepts/data-versioning-and-branching.md); summary: [Source](../sources/2026-10-15-duckdb-differential-snapshots-branches.md). Part of the [DuckDB](duckdb.md) ecosystem.
