---
tags: [data-n-ai, concept, etl, performance, file-formats, lakehouse]
sources: ["raw/data-n-ai/articles/2026-10-24-datafusion-point-queries-best-practices.md"]
updated: 2026-11-05
---

# Point-Query Optimization

Making single-row lookups (random reads by key) fast on an engine built for analytical scans. The goal flips from scanning large data efficiently to finishing each tiny query quickly (target < 1 ms), because there are many more queries. The evidence here is one [DataFusion](../entities/apache-datafusion.md) benchmark series on a 100M-row Parquet file.

## Two layers of tuning

**1. Storage layout (biggest lever)**
- **Sort by the lookup key.** Min/max statistics on row groups and pages only prune when the file is ordered; unsorted, a lookup touched ~122 pages, sorted just one (6000x throughput difference).
- **Drop metadata that doesn't help.** For a unique sorted key, dictionary encoding and bloom filters add overhead; min/max already suffices.
- **Smaller row groups and pages** (~128k / ~1k rows vs. 1M / 20k defaults) for point reads; ~2–4k-row pages are a reasonable compromise if the same file also serves scans.
- **Compression** is a speed/space tradeoff: `lz4` fastest, `zstd` best balance, `snappy` offered no advantage in this test.

**2. Engine execution**
- Fewer partitions for small reads; more for large scans (workload-dependent, settable at runtime).
- Push filters into the Parquet scan; keep the metadata cache on.
- **Planning dominates tiny queries** (~60% of CPU in logical + physical planning), so reuse plans via prepared statements. Reusing the *physical* plan was worth 2–3x but isn't available in DataFusion yet.
- Use a fast allocator (`mimalloc`) and consider a separate single-threaded runtime per client for many concurrent point queries.

## Cumulative result (single client)

| Step | Reads/s |
|---|---|
| Sorted file | 698 |
| + No dictionary | 1,062 |
| + Row group / page sizing | 1,370 |
| + Target partitions | 1,553 |
| + Pushdown filters | 1,616 |
| + Prepared statements (physical plan) | 4,606 |
| + mimalloc | 5,192 |
| + Single-threaded runtimes | 5,433 |

## Why it matters here

- It is the **tuned-Parquet counterpoint** to the Lance argument in [Columnar File Formats for Random Access](columnar-file-formats-for-random-access.md): Parquet's page-as-read-unit and row-group limits are real, but sorting plus right-sized pages gets sub-millisecond lookups without changing format. The Lance sources report no benchmarks to compare against.
- The same pruning mechanism (per-file/page min/max stats) underlies [Data Layout](data-layout.md) and [Query Optimization](query-optimization.md): clustering quality determines how much can be skipped.
- Relevant to agent workloads that issue many small lookups; compare the latency-over-throughput framing in [DuckDB for Agents](duckdb-for-agents.md).

## Caveats

Single dataset and schema, one cloud VM, author-run, cumulative (not isolated) effects. Sorting by one key helps only queries on that key. Settings like dictionary and bloom filters should be revisited for non-unique or multi-column predicates.

## Sources

- [Source: Best Practices for Single Row Lookups in DataFusion](../sources/datafusion-point-queries.md)
