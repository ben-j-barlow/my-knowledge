---
tags: [data-n-ai, entity, etl, performance]
sources: ["raw/data-n-ai/articles/2026-10-24-datafusion-point-queries-best-practices.md"]
updated: 2026-11-05
---

# Apache DataFusion

Extensible query engine toolkit written in Rust, using [Apache Arrow](apache-arrow.md) as its in-memory format. The project describes it as part of "deconstructed database" architectures: new systems built from fast, modular components rather than one tightly integrated system. Usually seen as an analytical engine, but it can also serve sub-millisecond point lookups when tuned.

## Notes from ingested sources

- Reads Parquet with row-group/page pruning from min/max statistics; Parquet metadata is cached by default since v50.0.0.
- Defaults (1M-row row groups, 20k-row pages, dictionary on, `zstd`, `pushdown_filters` off) favour scans; the point-query post shows tuned settings.
- Prepared statements reuse only the logical plan; physical-plan reuse is an open issue (#26706).
- `datafusion-cli` and the Python library ship with `mimalloc`.

## See Also

- [Point-Query Optimization](../concepts/point-query-optimization.md)
- [Nuno Faria](nuno-faria.md)
- [DuckDB](duckdb.md) — comparable embeddable analytical engine (C++)
- [Source: Best Practices for Single Row Lookups in DataFusion](../sources/datafusion-point-queries.md)
