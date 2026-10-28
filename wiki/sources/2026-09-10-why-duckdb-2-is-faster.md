---
tags: [data-n-ai, source, etl, pipelines, analytics]
sources: ["raw/data-n-ai/articles/Why DuckDB 2.0 is faster.md"]
updated: 2026-10-28
---

# Source: Why DuckDB 2.0 Is Faster

**Author**: MotherDuck (blog; first-person hands-on writer, unnamed in clip)
**Published**: 2026-09-10 · **URL**: https://motherduck.com/blog/why-duckdb-20-is-faster/
**Type**: Vendor hands-on benchmark of the **2.0 alpha vs 1.5.5**. All numbers from one M5 laptop and home internet to S3 us-east-1 — the author says to run your own before quoting.

## Core Claim

2.0 is faster, but to get the speedup you must understand how your data is shaped and sometimes how to model it.

## Results

**Async I/O (S3)** — nothing in the query changes; a separate download pool reads ahead of decode workers (`read_ahead_depth`, default `-1` = auto, `0` = old behaviour).

| Workload | 1.5.5 | 2.0 alpha |
|----------|-------|-----------|
| One 2.2 GB Parquet, one column | 18.8 s | 7.7 s |
| 23 large Parquet files, 13.6 GB | 11.8 s | 3.9 s |
| One 1.7 GB CSV | 116 s | 55 s |
| 30 × ~1 MB Parquet files | 3.7 s | 3.3 s |

Takeaway: 2–3× on large files; **no rescue for many tiny files** (per-file round trips dominate).

**Recursive CTEs** — engine rewritten: table read once, parent-column lookup built once, rounds touch only new rows. Git-ancestry walk over 20,000 commits: 1.8–16 s (1.5.5) → 0.10 s. Shallow hierarchies (org charts) gain little. Advice: keep integer-id parent/child tables; use `USING KEY` when carrying depth/cost. Team claims 40× on graph reachability.

**VARIANT** (5M events, three storage layouts):

| | JSON string | VARIANT 2.0 | VARIANT 1.5.5 | Typed columns |
|-|-|-|-|-|
| Size | 224 MB | 85 MB | 81 MB | 45 MB |
| Filter on 2 fields | 366 ms | 63 ms | 4.96 s | 52 ms |
| Sum by country | 408 ms | 61 ms | 5.28 s | 51 ms |
| List contains | 357 ms | **1.96 s** | 4.65 s | 67 ms |

Shredding pulls consistently-typed fields into real columns and leaves rare/mixed-type fields in a binary remainder. ~2.7× smaller than JSON, ~6× faster on shredded fields; **list casts are slower than JSON in the alpha**. A field that is `231` in one row and `"231ms"` in the next falls into the remainder — keep value kinds consistent. Rule: model what you know; promote hot fields to real columns.

**Quick hits**: triggers for history tables; nested schemas; `DELETE ... RETURNING` in a CTE feeding `INSERT` (atomic move); `dialect_compatibility_mode = 'spark'`; `external_file_cache_spill` (second read of an 854 MB S3 Parquet under 300 MB memory: 23.9 s → 0.35 s); CLI SQL formatter and queryable history; `read_json` keeps ISO-8601 offsets as `TIMESTAMPTZ`; scoped secrets `CREATE SECRET ... IN CONNECTION`.

## Caveats

- Alpha, single laptop, vendor author (MotherDuck sells hosted DuckDB). Final 2.0 numbers may differ.
- Confirms the [Parquet small-files](../concepts/data-layout.md) lesson holds on DuckDB too.

## See Also

- [DuckDB 2.0](../concepts/duckdb-2-0.md) · [Source: DuckDB 2.0 Release](2026-10-21-duckdb-2-0-release.md) · [MotherDuck](../entities/motherduck.md)
