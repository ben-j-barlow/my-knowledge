---
tags: [data-n-ai, source, etl, lakehouse, file-formats, vector-databases]
sources: ["raw/data-n-ai/articles/2026-10-22-a-file-format-claims-to-be-100x-faster-than-parquet.md"]
updated: 2026-10-28
---

# Source: A File Format Claims to Be 100x Faster Than Parquet

**Author**: Vu Trinh · **Published**: 2026-10-22 · **URL**: https://vutr.substack.com/p/free-a-file-format-claims-to-be-100x
**Type**: Explainer newsletter post (stated as unsponsored). Concept page: [Columnar File Formats for Random Access](../concepts/columnar-file-formats-for-random-access.md). Companion primary source: [Lance v2: A New Columnar Container Format](2026-03-31-lance-v2-columnar-container-format.md).

## Summary

AI workloads (embedding lookup, semantic search, multimodal data, 10,000-column feature tables) need **random access** as well as sequential scans. The post revisits Parquet internals, names three structural problems, then shows how [Lance](../entities/lance.md) avoids each. The "100x faster for random access" figure is Lance's own claim; the post gives **no benchmark numbers** — it is an architecture walkthrough.

## Parquet problems named

1. **Page is the smallest readable unit.** Fetching one row means fetching, decompressing and decoding the whole page; larger pages = higher latency.
2. **FileMetadata is Thrift/Protobuf-encoded, no random access.** The reader deserializes metadata for *all* columns to get one column's schema; cost scales with column count.
3. **Row-group constraint.** A row group is the physical I/O unit and must be buffered fully before flush → OOM with large values. Example: 4 KiB values in a 512 MB row group = 125,000 rows, and every other column is capped at 125,000 rows too (an Int32 column could hold 128 M). Many small row groups mean more metadata, more non-adjacent reads / object-store GETs, and worse compression.

## Lance design decisions

- **File layout**: data pages (located by absolute offset), per-column protobuf metadata, a column-metadata offset table, then an offset array and footer at the end.
- **Two page encodings by value size**: *mini-block* for small values (chunks ~4–8 KiB, ≤4,096 values; opaque encodings allowed) and *full-zip* for values ≥256 bytes (embeddings, images, large text; value metadata interleaved with data; **transparent encodings only**, so one value can be decoded alone).
- **Transparent vs opaque encoding**: dictionary is transparent (index → value); delta is opaque (value N needs all prior diffs). Opaque saves space but blocks single-value decode.
- **No row groups.** Pages (default 8 MB) are per column, so columns have independent page counts (1 M rows: boolean ≈128 KiB = 1 page; 3 KiB embeddings ≈3 GiB ≈ 384 pages). Writer buffers per column, not per row group. Readers can split a file at **any row boundary** because each page records its start row and its layout maps row ranges to byte ranges.
- **O(1) column metadata**: one protobuf message per column, reached through the offset table, so reading one column never decodes the others.

## Key quotes

- "Page is the smallest unit you can read in Parquet."
- "The Lance file structure abandons the row group concept completely."

## Caveats

- No measured results; the 100x claim is unverified here.
- Written from Lance's perspective; no discussion of Parquet's strengths (ecosystem, compression, engine support) or of newer Parquet work.
- Cites the Lance arXiv paper (Pace et al., 2025, *Adaptive Structural Encodings*) and Julien Le Dem's "Column Storage for the AI Era" — neither ingested.
