---
tags: [data-n-ai, entity, etl, pipelines]
sources: ["raw/data-n-ai/articles/DuckDB Internals Why is DuckDB Fast?.md"]
updated: 2026-05-20
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

## Trade-offs

- **Single-node**: does not distribute across a cluster; for datasets that exceed a single machine's resources, Spark or a cloud warehouse is needed
- **OLAP, not OLTP**: optimized for analytical scans, aggregations, joins — not high-throughput point reads/writes

## See Also

- [Apache Arrow](apache-arrow.md)
- [Query Optimization](../concepts/query-optimization.md)
- [Lakehouse Statistics](../concepts/lakehouse-statistics.md)
- [Apache Spark](apache-spark.md)
- [Source: DuckDB Internals Part 1](../sources/duckdb-internals-part1.md)
