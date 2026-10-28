---
tags: [data-n-ai, concept, etl, lakehouse, file-formats, vector-databases]
sources: ["raw/data-n-ai/articles/A file format claims to be 100x faster than Parquet.md", "raw/data-n-ai/articles/Lance v2 A New Columnar Container Format.md"]
updated: 2026-10-28
---

# Columnar File Formats for Random Access

Parquet is built for sequential scans of tabular data. AI workloads (embedding/semantic search, full-text search, multimodal blobs, feature stores) add **point lookups** and very large values, which expose structural limits. New formats — [Lance](../entities/lance.md) most prominently; BtrBlocks, Procella and Vortex are named as parallel efforts — redesign the file layout around them.

## Where Parquet struggles

| Limit | Mechanism | Consequence |
|---|---|---|
| Page = smallest read unit | Fetch + decompress + decode whole page for one row | Point-lookup latency grows with page size |
| Metadata not randomly accessible | Thrift/Protobuf FileMetadata for all columns | Wide schemas (thousands of columns) pay full deserialize per read |
| Row group = I/O unit | Writer buffers whole group; all columns share row count | OOM with big values; tiny groups → more metadata, GETs, worse compression |
| Fixed encodings / stats | New encoding or stat type needs reader changes | Ecosystem fragmentation, slow evolution |

## Design responses (Lance)

- **Small, sliceable chunks**: mini-block (small values) and full-zip (≥256 B values) with *transparent* encodings so a single value decodes alone; opaque encodings (delta) trade lookup speed for size.
- **Drop row groups**: per-column pages (≈8 MiB for object storage), written from per-column buffers; read parallelism splits at any row.
- **Independent per-column metadata** → O(1) projection regardless of column count.
- **Encodings and statistics as plugins** stored in metadata (protobuf `Any`), so the container format stays stable.

## How it relates to the lakehouse stack

- File format ≠ table format: [Apache Iceberg](apache-iceberg.md) and [DuckLake](ducklake.md) are metadata layers over (mostly) Parquet; Lance is a replacement for the *file* layer, with LanceDB adding table/index features. Table-level layout choices are covered in [Data Layout](data-layout.md).
- Per-encoding zone maps echo the structural-vs-statistical metadata split in [Lakehouse Statistics](lakehouse-statistics.md), but push stats into the file's encoding layer.
- Lance's reference implementation uses [Apache Arrow](../entities/apache-arrow.md) types; DuckDB's Parquet-centred stack ([DuckDB](../entities/duckdb.md), [DuckDB 2.0](duckdb-2-0.md)) is the contrasting analytical path.

## Open questions / caveats

- The "100x faster random access" headline is a vendor claim; neither ingested source reports benchmarks. Lance v2 post itself says parity with the best Parquet readers held only on poorly compressible data (early implementation).
- Sources are Lance-friendly; Parquet's ecosystem breadth and recent work are not weighed. The Lance arXiv paper (Pace et al. 2025) and Julien Le Dem's "Column Storage for the AI Era" are un-ingested follow-ups.
- Whether agent workloads (mostly analytical SQL over modest data) need this versus embeddings/vector retrieval is not addressed.

## Sources

- [A File Format Claims to Be 100x Faster Than Parquet](../sources/2026-10-22-lance-100x-faster-than-parquet.md)
- [Lance v2: A New Columnar Container Format](../sources/2026-03-31-lance-v2-columnar-container-format.md)
