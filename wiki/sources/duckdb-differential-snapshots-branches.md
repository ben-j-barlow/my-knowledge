---
tags: [data-n-ai, source, agents, pipelines, lakehouse]
sources: ["raw/data-n-ai/articles/2026-10-15-duckdb-snapshots-time-travel-and-writable-branches.md"]
updated: 2026-10-28
---

# Source: DuckDB Snapshots, Time Travel and Writable Branches

**Author**: [Tobias Müller](../entities/tobias-mueller.md) (tobilg.com)
**Published**: 2026-10-15 · **URL**: https://tobilg.com/posts/differential-storage-for-duckdb/
**Type**: Tool announcement + use-case walkthrough for the [duckdb-differential](../entities/duckdb-differential.md) community extension (experimental; DuckDB 1.5.6, Linux/macOS).

## Core Claim

Versioning can live at the level of a **native `.duckdb` database file**, not a lakehouse table format. The extension adds snapshots, time travel, writable branches, clones and restore from plain SQL; versions share unchanged storage chunks. See [Data Versioning and Branching](../concepts/data-versioning-and-branching.md).

## Primitives

- **Snapshot** — retained checkpointed state (`differential_create_snapshot`); read via `ATTACH ... (SNAPSHOT_VERSION n)` or `AT (VERSION => n)`.
- **Branch** — writable continuation from a snapshot (`differential_create_branch`, `ATTACH ... (BRANCH 'x')`); one writer process per branch.
- **Clone** — separate database identity and snapshot history, sharing unchanged payloads.
- **Restore** — adopts a whole database state (requires detached target; preserves the replaced state; makes a new snapshot). **No automatic merge** — diverged histories must be reconciled with SQL.
- **S3 publication** — snapshot export to S3; readers query on demand via verified range fetches, or `differential_recover_export` into a new writable local database.

## Use Cases Walked Through

1. **Validate an import on a branch** before adopting it (a sign-flipped amount caught while `main` stays untouched) — a branch-based [write-audit-publish](../concepts/correctness-layer.md) loop; adopt via restore.
2. **Reproduce a report**: pin the input snapshot, keep querying it after live data changes. Record database identity + version + code version.
3. **Compare scenarios** (e.g. 10% discount) on branches from one baseline.
4. **Feature datasets** on fixed inputs, labelled via snapshot `extra_info` JSON.
5. **Migration test** on a clone; restore to snapshot 1 resets the workspace between attempts.
6. **Independent agent attempts**: controller creates a branch per attempt, worker transforms it, controller inspects the candidate snapshot and decides whether to keep it. `request_id` makes management calls retryable.
7. **Share/recover** via S3 — local commit and S3 publication are separate durability boundaries.

## Key Caveats (author's own)

- Experimental; benchmarks document specific workloads, not a general performance guarantee.
- Branches give data independence, **not a security sandbox** — repository access lets you address other branches; untrusted agents need OS/container isolation.
- Snapshots don't freeze external files, credentials or session state; nondeterministic computation isn't made repeatable.
- Retention is manual: dropping a branch doesn't expire snapshots; no automatic remote GC; local cleanup never deletes exported S3 data.
- Branch/clone creation cost scales with the chunk-map size; one updated row can touch several 64 KiB chunks.
- Consumers need the extension and a compatible DuckDB.

## Storage Design

DuckDB keeps handling SQL, transactions, indexes and catalog; Differential intercepts file operations, storing immutable ~64 KiB chunks (12 KiB header isolated) plus mappings in a local repository, coordinated by embedded SQLite. Writes sync with `FULL` synchronization (`F_FULLFSYNC` on macOS).

## Versus DuckLake / Iceberg

Author's positioning: DuckLake and Iceberg version a *lakehouse catalog/tables* and win when interoperability matters; Differential versions a *native database* (including its constraints, indexes and catalog) and adds writable workspaces. For one-off experiments a checkpointed file copy may suffice.

## Notes for This Wiki

- Single-author, self-published announcement of the author's own tool; no independent validation.
- Most relevant to the agent angle: cheap isolated branches per attempt, complementing [DuckDB for Agents](../concepts/duckdb-for-agents.md)' "agents branching" claim, which the earlier MotherDuck-sourced material did not explain mechanically.
- Compatibility with [DuckDB 2.0](../concepts/duckdb-2-0.md) (released 6 days later, new storage format) is unstated.

## See Also

- [DuckDB](../entities/duckdb.md) · [DuckLake](../concepts/ducklake.md) · [Apache Iceberg](../concepts/apache-iceberg.md)
- [Source: DuckLake in Production: Maintenance Strategy](ducklake-maintenance-strategy.md) — retention policy parallels
