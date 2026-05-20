---
tags: [data-n-ai, source, etl, pipelines]
sources: ["raw/data-n-ai/articles/DuckDB Internals Why is DuckDB Fast?.md"]
updated: 2026-05-20
---

# DuckDB Internals Part 1: Why is DuckDB Fast?

> Source: https://www.greybeam.ai/blog/duckdb-internals-part-1
> Author: Kyle Cheung (Greybeam)
> Published: 2026-05-04

## Summary

Part 1 of a 3-part deep dive into DuckDB internals. Covers the in-process execution model, query processing pipeline (parse → bind → optimize → physical plan), storage layout (columnar row groups with zone maps), and Parquet/CSV integration. The core performance insight: DuckDB wins partly by eliminating overheads that most databases treat as unavoidable — serialization, network I/O, per-row API calls.

## Key Claims

### In-Process Execution
- DuckDB is a library (`libduckdb`), not a server — no TCP, no daemon, no port
- The 2017 paper *Don't Hold My Data Hostage* (Raasveldt & Mühleisen) showed that client protocols (ODBC, JDBC) are often the slowest step in the entire query — slower than the compute itself
- ODBC/JDBC's row-by-row API means a separate function call per field per row — hundreds of millions of calls on large result sets
- DuckDB sidesteps this: result lives in the same process memory, no serialization
- **Replacement scans**: DuckDB reads Python DataFrames directly without copying them into an internal table, treating the dataframe as a virtual scan target; zero-copy when layouts align
- Arrow is the "cleanest version" of this — already a columnar typed format designed for sharing memory between systems

### Query Processing Pipeline
1. **Parse**: SQL → AST using a fork of the Postgres parser
2. **Bind**: resolve names against catalog; type-check; produce a typed tree
3. **Optimize**: 33 independent passes (inspectable and disableable via `SET disabled_optimizers`); key passes:
   - `filter_pushdown`: move WHERE predicates as early as possible
   - `join_order`: DPhyp/DPccp dynamic programming to find best join tree (up to 30,240 possible orderings for 6-table join)
   - `statistics_propagation`: propagate known value ranges through the plan
   - Dynamic join-filter pushdown: after building the hash table, push min/max bounds (or IN list for ≤50 distinct values) back into the probe-side scan to skip more row groups
   - Subquery unnesting: rewrites correlated subqueries as joins (avoids N×1 inner query executions)
4. **Physical plan**: map logical operators to physical implementations (hash join, sort-merge join, etc.)

### Pipeline Execution Model
- **Pipeline**: a chain of streaming operators that process a row independently (filter, projection, hash join probe side) — parallelize cleanly across cores
- **Pipeline breaker/sink**: operators that must see the full input before producing output (ORDER BY, GROUP BY, hash join build side) — end one pipeline, start the next
- **Sink phases**: sink (each thread writes to its own local state, no locks), combine (parallel merge across threads), finalize (output to next pipeline)
- Chunk size: 2048 rows per batch (vectorized)

### Storage: Row Groups and Zone Maps
- Data stored in **row groups** of up to 122,880 rows per column
- Each row group has a **zone map**: min value, max value, null count
- On `WHERE event_date > '2026-01-01'`, DuckDB checks each row group's max before reading any data — skips row groups entirely if max ≤ predicate value
- Zone map effectiveness depends on data ordering: sorted/naturally ordered columns give narrow min-max spans; randomly scattered columns give wide spans
- Analogy: Snowflake calls this "micro-partition pruning", BigQuery calls it "block pruning", ClickHouse uses `minmax` indexes

### Parquet Integration
- Parquet is columnar and stores min/max statistics per row group per column — DuckDB reads those statistics exactly like zone maps
- When querying remote Parquet: fetch only the footer (schema + statistics) → decide which row groups to read → HTTP range requests for only needed bytes
- Querying a directory of Parquet files without importing: `SELECT ... FROM read_parquet('s3://bucket/*.parquet')`

### Ecosystem
Used by: MotherDuck (cloud DW), Hex/Omni/Evidence (BI), Fivetran (data lake writer for merging/compaction), Rill (BI), Greybeam (multi-engine routing)

## Related Wiki Pages

- [DuckDB](../entities/duckdb.md)
- [Apache Arrow](../entities/apache-arrow.md)
- [Query Optimization](../concepts/query-optimization.md)
- [Lakehouse Statistics](../concepts/lakehouse-statistics.md)
