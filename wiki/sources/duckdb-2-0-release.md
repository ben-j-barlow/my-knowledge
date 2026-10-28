---
tags: [data-n-ai, source, etl, pipelines, agents, lakehouse]
sources: ["raw/data-n-ai/articles/2026-10-21-announcing-duckdb-2-0-0-lts-cinnamon-teal.md"]
updated: 2026-10-28
---

# Source: Announcing DuckDB 2.0.0 LTS "Cinnamon Teal"

**Author**: The DuckDB team
**Published**: 2026-10-21 · **URL**: https://duckdb.org/2026/10/21/announcing-duckdb-200
**Type**: Official release announcement (primary source). ~20,000 commits since 1.5. Summarised on [DuckDB 2.0](../concepts/duckdb-2-0.md).

## Core Claim

2.0 is "above all a feature release" (1.0 was about stability): server mode, async I/O, first-class VARIANT, agent mode, triggers and a new parser.

## Key Points

- **Quack + `CONNECT`**: the client-server protocol (introduced 1.5.3, May 2026) ships polished; `quack_serve(token=...)`, `ATTACH 'quack:host'`, `CONNECT`. Server listens on localhost only by default; remote access should sit behind a TLS reverse proxy. `CONNECT` also works for Postgres/MySQL with a remote pushdown optimizer. CLI: `duckdb -serve` / `-connect`.
- **Async I/O** for Parquet, CSV and native storage: I/O scales independently of query processing; big wins on `s3://`.
- **VARIANT** fully integrated: auto-detects common structure and "shreds" it; shredded Parquet read/write; `variant_*` functions.
- **Agent mode** in the CLI: auto-detected; compact Markdown tables, explicit truncation notices, runaway-query stopping, JSON errors, expected cost reported before long queries. On TPC-H it cut output the model had to read by **59%** (vendor experiment). `-agent` / `-no-agent` flags.
- **PEG parser** default (replacing the Postgres-derived YACC/Bison one); extensions can add syntax; `enable_legacy_parser` fallback.
- **Extensions**: C API v2 (feedback requested, not yet stable); self-hosted signed extension repositories (`CREATE EXTENSION REPOSITORY`, WIP syntax).
- **Core extensions**: DuckLake 1.1 released (new spec + reference implementation); Iceberg extension adds REST-catalog ATTACH options; Delta extension adds `CREATE TABLE`, time travel.
- **Triggers**: `BEFORE`/`AFTER`, row/statement level, transition tables; audit tables and incrementally maintained summaries (a step toward materialized views); some combinations unsupported.
- **SQL additions**: `$var` shorthand, data-modifying CTEs, `NEAREST` joins, nested schemas, JSON mutation functions, `FETCH FIRST`, defined `MERGE`/`UPDATE ... FROM` semantics for multi-match.
- **Internals**: C++17 required, Clang builds, ICU removed (native timezones/calendars/collations).

## Migration and Support

- **Storage format**: versions before 2.0 **cannot read files created by 2.0**; 2.0 can read/write existing files, which stay readable by older versions. Test on a shadow system; mission-critical users may wait for the first patch (November 2026).
- Support: 2.0 until ≥ Oct 2027; 1.4 until 17 Nov 2026; 1.5 extended to Mar 2027 (effectively LTS).
- Deprecated: single-arrow lambdas (`x -> x+1`, removed in 2.1; use `lambda x: ...`), amalgamation builds, `osx_amd64` (dropped in 2.1; community extensions best-effort).

## Notes for This Wiki

- Vendor primary source: benchmark/feature claims are the team's own; independent numbers in [Source: Why DuckDB 2.0 Is Faster](why-duckdb-2-is-faster.md) (alpha, MotherDuck).
- Updates earlier wiki statements that Quack was "in progress" (Sept 2026) — it now ships. Concurrent-writer limitations are therefore worth re-checking.
- A follow-up post, "Gems of DuckDB 2.0.0", exists but is not ingested.

## See Also

- [DuckDB](../entities/duckdb.md) · [CLI Tools for Agents](../concepts/cli-tools-for-agents.md) · [DuckLake](../concepts/ducklake.md)
