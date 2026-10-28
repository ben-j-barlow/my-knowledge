---
tags: [data-n-ai, source, etl, lakehouse, file-formats, vector-databases]
sources: ["raw/data-n-ai/articles/2026-03-31-lance-v2-a-new-columnar-container-format.md"]
updated: 2026-10-28
---

# Source: Lance v2 — A New Columnar Container Format

**Author**: LanceDB Engineering (post written by Lance's lead file-format developer) · **Clip date**: 2026-03-31 · **URL**: https://www.lancedb.com/blog/lance-v2
**Type**: Vendor design post (primary source for the format). Note: the clip's date is a republish date; the Vu Trinh post cites it as a 2024 article and describes v2 as an early-stage implementation ("initial implementation… simple encodings"), so specifics may be stale. Concept page: [Columnar File Formats for Random Access](../concepts/columnar-file-formats-for-random-access.md). Entity: [Lance](../entities/lance.md). Secondary explainer: [A File Format Claims to Be 100x Faster Than Parquet](lance-100x-faster-than-parquet.md).

## Why a new format

Lance v1 and Parquet both struggle with modern AI/ML workloads. Use cases that drove v2:

- **Point lookups** — secondary-index queries (semantic search and full-text search both reduce to them). Parquet encodings aren't sliceable, so a whole page loads for one row; worse with large multimodal values where coalescing is hard.
- **Wide columns** — 4 KiB CLIP embeddings, images; "picking a good row group size is impossible" when one column is huge.
- **Very wide schemas** — column-per-ticker finance tables, feature stores with thousands of features; Parquet must still load schema metadata for all columns.
- **Flexible encodings** — adding an encoding to Parquet means changing every reader implementation, and Parquet development has slowed.
- **Flexible metadata** — Parquet encodings can only write to the data page, forcing e.g. a constant dictionary to be repeated in every row group, and blocking RLE skip tables in column metadata.

## The v2 design

1. **Encodings are extensions.** Reader/writer know no encodings (not even plain); descriptions are protobuf `Any` messages, so new encodings need no format change — hence "columnar *container* format" (like video containers). Unsupported encoding → helpful "reader not configured with a decoder" error.
   - **No type system** in the format: a column is pages-with-an-encoding, a page is buffers. Reference readers/writers use the Arrow type system ([Apache Arrow](../entities/apache-arrow.md)). Spec is "less than 50 lines of protobuf".
2. **Abolish row groups.** Pages in a column need not be adjacent; each column writer flushes a page when its own buffer fills (e.g. 8 MiB suits S3), so pages are never undersized except the last. Claimed "zero tradeoffs": maximal pages, minimal RAM in writer and reader. Row groups are a poor unit for threads (10 cores × 5 columns = 50 simultaneous IOPS; compute waits on all) and for multi-process parallelism "just make 10 files". Reader decouples I/O size from batch size (e.g. two 8 MiB pages arrive, launch 100 decode tasks of 10 Ki rows).
3. **Flexibility.** Columns can differ in length; write "an array at a time". Per-column metadata blocks enable **true column projection** ("hundreds of thousands or even millions of columns… no impact"). Dictionaries, RLE skip tables, null info can live in column metadata or file-wide buffers, chosen by the encoder. **Statistics are encoding metadata**: a zone map is a proxy layer in the encoding, so zone-map resolution is decoupled from page size and new stats types (histograms, bloom filters) need no format change — contrast [Lakehouse Statistics](../concepts/lakehouse-statistics.md).

## Status / claims

- Initial implementation used simple encodings only; "performance is on par with the best Parquet readers" but only on poorly compressible data (author expects broader parity with better encodings). Unverified claim.
- Alpha Python API shown (`LanceFileWriter` / `LanceFileReader`).
- Mentions BtrBlocks, Procella and Vortex as others who found similar Parquet issues.
