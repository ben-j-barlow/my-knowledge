---
tags: [data-n-ai, entity, etl, pipelines, lakehouse]
sources: ["raw/data-n-ai/articles/2026-05-04-duckdb-internals-why-is-duckdb-fast.md", "raw/data-n-ai/articles/2026-09-11-duckdb-400k-skill.md"]
updated: 2026-10-17
---

# DuckDB

In-process analytical SQL database. No server, no daemon, no TCP socket — DuckDB loads as a library (`libduckdb`) directly into the calling process. Originated as a research project at CWI Amsterdam in 2019; now one of the most widely adopted single-node analytical engines.

## What "In-Process" Means

Most analytical databases (Snowflake, Postgres, BigQuery, Redshift) run as servers. Queries cross a network boundary; results are serialized into a wire protocol and deserialized on the client. The 2017 paper *Don't Hold My Data Hostage* (Raasveldt & Mühleisen) showed this client-protocol overhead is often the **slowest single step** in a query — dwarfing the compute time.

DuckDB eliminates this entirely. Results live in the same process memory. No encoding, no TCP, no per-row function calls. On Python DataFrames, DuckDB can use **replacement scans** to query the dataframe directly without copying it, and can read Arrow-backed data in a zero-copy path when memory layouts align.

## Why DuckDB Is Fast

1. **In-process**: no serialization/network overhead
2. **Columnar storage with zone maps**: row groups of 122,880 rows; each carries min/max/null-count per column for predicate-based row group skipping
3. **33-pass optimizer**: filter pushdown, subquery unnesting (correlated subqueries rewritten as joins), dynamic join-filter pushdown, join order optimization (DPhyp dynamic programming), statistics propagation — all inspectable via `SELECT * FROM duckdb_optimizers()`
4. **Pipeline execution**: streaming operators (filter, projection, hash join probe side) run as assembly-line pipelines across all cores; pipeline breakers (ORDER BY, GROUP BY, hash join build side) separate pipelines; each thread uses thread-local state with no lock contention during sinks
5. **Parquet integration**: reads Parquet row group statistics identically to native zone maps; HTTP range requests fetch only relevant bytes from remote files
6. **Arrow integration**: [Apache Arrow](apache-arrow.md) data is already in DuckDB's preferred columnar layout — zero-copy path available

## Key Specs

- Single binary, <20MB, no external dependencies
- Install: `pip install duckdb`, `brew install duckdb`, or link `libduckdb`
- Opens Parquet, CSV, JSON, XLSX files as SQL tables without import
- Chunk size: 2048 rows (vectorized execution unit)

## Who Uses DuckDB

| Company | Use |
|---------|-----|
| MotherDuck | Cloud data warehouse built on DuckDB |
| Hex, Omni, Evidence | In-app query engine and analytics cache |
| Fivetran | Data lake writer for merging and compaction (Managed Data Lake Service) |
| Rill | Open-source BI built on DuckDB |
| Greybeam | Multi-engine routing layer |

## Iceberg Write Support (v1.5.3, May 2026)

Before v1.5.3, DuckDB could *read* [Apache Iceberg](../concepts/apache-iceberg.md) tables but not write them — every Iceberg write workflow still required a Spark cluster (96% of Iceberg users ran Spark as their write engine circa early 2026). v1.5.3 shipped `MERGE INTO`, `ALTER TABLE`, partition transforms, and Iceberg V3 format support, collapsing that requirement into a 30MB binary. Combined with [**DuckLake**](../concepts/ducklake.md) (dated April 2026 here, but a review of it exists from Oct 2025 — see that page) — which embeds the Iceberg catalog in SQLite/Postgres instead of a distributed catalog service — this closed the last gap in running a full local lakehouse (DuckDB + Iceberg + dbt Core) without any cloud infrastructure. AWS acquired the DuckLabs team in August 2026.

Known limitation: DuckDB still enforces single-writer semantics — concurrent multi-process writes serialize or fail. The "Quack protocol" and DuckLake both had fixes in progress as of the source's writing (Sept 2026). **Update (Oct 2026):** Quack shipped polished in [DuckDB 2.0](../concepts/duckdb-2-0.md) (client-server, `CONNECT`) — whether it fully resolves multi-writer use is unverified.

## DuckDB 2.0 (Oct 2026)

LTS release with async I/O, first-class VARIANT, CLI agent mode, triggers, PEG parser and a storage-format change (2.0 files unreadable by older versions). See [DuckDB 2.0](../concepts/duckdb-2-0.md).

## DuckDB CLI with Agents

The DuckDB CLI is a favored agent tool: agents understand it well, iterate quickly on SQL and errors, avoid generated Python (where hallucinations are likelier), and use the persistent secrets manager so credentials never reach the agent. A single DuckDB file allows one connection, so parallel agents should read Parquet/CSV or a DuckLake with a Postgres catalog. See [CLI Tools for Agents](../concepts/cli-tools-for-agents.md).

## Trade-offs

- **Single-node**: does not distribute across a cluster; for datasets that exceed a single machine's resources, Spark or a cloud warehouse is needed
- **OLAP, not OLTP**: optimized for analytical scans, aggregations, joins — not high-throughput point reads/writes
- **Single-writer**: no stable concurrent-write story yet (see above)

## See Also

- [Apache Arrow](apache-arrow.md)
- [Apache Iceberg](../concepts/apache-iceberg.md)
- [Query Optimization](../concepts/query-optimization.md)
- [Lakehouse Statistics](../concepts/lakehouse-statistics.md)
- [Apache Spark](apache-spark.md)
- [DuckDB for Agents](../concepts/duckdb-for-agents.md)
- [Source: DuckDB Internals Part 1](../sources/duckdb-internals-part1.md)
- [Source: DuckDB Just Put a $400K/Year Skill on Your Laptop](../sources/duckdb-400k-skill.md)
- [CLI Tools for Agents](../concepts/cli-tools-for-agents.md)
- [DuckLake](../concepts/ducklake.md)
- [Source: DuckLake Tech Review](../sources/2025-10-10-ducklake-tech-review.md)
- [Source: DuckLake in Production: Maintenance Strategy](../sources/2026-10-06-ducklake-maintenance-strategy.md)
- [Source: My DuckDB + AI Workflow](../sources/2026-09-13-duckdb-ai-workflow.md)
- [duckdb-differential](duckdb-differential.md) — community extension for snapshots, branches and clones of native DuckDB files
- [Tobias Müller](tobias-mueller.md) — blogs extensively on DuckDB (tobilg.com)
- [Data Versioning and Branching](../concepts/data-versioning-and-branching.md)
- [DuckDB 2.0](../concepts/duckdb-2-0.md) · [MotherDuck](motherduck.md)
- [Source: DuckDB 2.0 Release](../sources/2026-10-21-duckdb-2-0-release.md)
- [Source: Why DuckDB 2.0 Is Faster](../sources/2026-09-10-why-duckdb-2-is-faster.md)
