---
tags: [data-n-ai, source, etl, performance, file-formats, lakehouse]
sources: ["raw/data-n-ai/articles/2026-10-24-datafusion-point-queries-best-practices.md"]
updated: 2026-11-05
---

# Source: Best Practices for Single Row Lookups (Point Queries) in DataFusion

**Author**: Nuno Faria (INESC TEC, DataFusion committer) · **Published**: 2026-10-24 · **URL**: https://datafusion.apache.org/blog/2026/10/24/point-queries/
**Type**: Project blog post based on a Sept 2026 Boston DataFusion meetup talk. Concept page: [Point-Query Optimization](../concepts/point-query-optimization.md). Entity: [Apache DataFusion](../entities/apache-datafusion.md).

## Summary

[DataFusion](../entities/apache-datafusion.md) is usually seen as an analytical engine, but some users need sub-millisecond random lookups over large Parquet files. The post tunes one 100M-row Parquet file (`bigint` key, `varchar` value) on a 4-vCPU VM, applying one optimization at a time. Throughput rises from **698 to 5,433 reads/s (~8x)** and response time falls from 1.43 ms to 0.18 ms.

## Headline findings

- **Storage matters most.** A file sorted by the lookup key was 6000x faster than an unsorted one (1 page touched vs ~67 row groups / ~122 pages), because min/max statistics can then prune almost everything.
- **Parquet write settings:** disable dictionary encoding and bloom filters for a unique, sorted key; use smaller row groups and pages (~128k / ~1k rows vs defaults of 1M / 20k); ~2–4k-row pages serve both point reads and scans; `zstd` is the best space/speed tradeoff, `lz4` is faster.
- **Engine settings:** single partition for small reads (more partitions cost coalescing overhead); `pushdown_filters` helps small and large reads but is off by default; keep the Parquet metadata cache on (default since v50); `mimalloc` is the best overall allocator.
- **Planning is the hidden cost.** ~12% of CPU goes to logical planning and ~50% to physical planning. DataFusion's prepared statements reuse only the logical plan; a prototype reusing the physical plan doubled to tripled throughput. This is not yet in DataFusion.
- **Concurrency:** one single-threaded tokio runtime per client scaled better than a shared multi-threaded runtime, at the cost of single-threaded analytical queries.

## Caveats

- Author-run benchmarks on a single dataset, one VM type and one unique-key schema; the author notes the best compression and similar settings depend on the dataset.
- Each optimization builds on the previous one, so effects are not isolated.
- The `pushdown_filters` result for mid-sized reads (10k–100k rows) is unexplained by the author.
- The physical-plan prepared-statement result comes from the author's own prototype.
