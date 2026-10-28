---
tags: [data-n-ai, concept, agents, pipelines, lakehouse]
sources: ["raw/data-n-ai/articles/2026-10-15-duckdb-snapshots-time-travel-and-writable-branches.md"]
updated: 2026-10-28
---

# Data Versioning and Branching

Keeping known states of a dataset so you can read an old one (**time travel**) or do independent work from it (**branches**) without disturbing readers of the original. Needed for import validation, reproducible reports, scenario analysis, migration tests, and giving each agent attempt its own workspace.

## Vocabulary

| Term | Meaning |
|------|---------|
| Snapshot | Retained, read-only state at a point in time |
| Branch | Writable continuation from a snapshot, same database identity |
| Clone | New database identity with its own history, sharing unchanged data |
| Restore | Adopt a whole earlier/candidate state as current; not a merge |

## Where It Lives: Three Layers in the Wiki

| Approach | Versions | Branches | Notes |
|----------|----------|----------|-------|
| [Apache Iceberg](apache-iceberg.md) | Table snapshots in file metadata | Branches/tags (per author's comparison) | Interop-first; needs catalog |
| [DuckLake](ducklake.md) | Catalog snapshots in a SQL DB | Not covered in wiki sources | Time travel via `AT (VERSION => n)`; retention = maintenance policy |
| [duckdb-differential](../entities/duckdb-differential.md) | Chunk-level snapshots of a native `.duckdb` file | Writable branches and clones, S3 export | Experimental; keeps constraints/indexes/catalog; no merge |

Delta Lake (DuckDB's Delta extension gains time travel and `CREATE TABLE` in 2.0) is a fourth option. Note: `duckdb-differential` targeted DuckDB 1.5.6; 2.0 changes the storage format ([DuckDB 2.0](duckdb-2-0.md)).

## Patterns

- **Branch-based write-audit-publish**: load to a branch, validate, snapshot, then adopt by restore. Same idea as the [correctness layer](correctness-layer.md) but with a whole-database candidate rather than a staging table.
- **Report reproducibility**: store `(database identity, snapshot number, code version)`; materialise external inputs since snapshots don't freeze them.
- **Branch per agent attempt**: controller creates branch, worker mutates, controller reviews candidate snapshot, keep or discard. See [DuckDB for Agents](duckdb-for-agents.md).

## Cross-Cutting Caveats

- **Retention is a policy**: every retained version costs storage; expiring versions ends time travel to them (same trade as [DuckLake maintenance](ducklake.md)).
- **No merge** in the DuckDB-native option: reconciling diverged branches is explicit SQL.
- **Data isolation ≠ security isolation**: branches do not sandbox untrusted agents.
- Evidence base is thin: one self-published tool announcement.

## See Also

- [Source: DuckDB Snapshots, Time Travel and Writable Branches](../sources/duckdb-differential-snapshots-branches.md)
- [Hive-Style Data Lake Limitations](hive-style-data-lake-limitations.md) — lack of snapshot isolation / time travel motivates this whole area
