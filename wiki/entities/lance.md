---
tags: [data-n-ai, entity, etl, lakehouse, file-formats, vector-databases]
sources: ["raw/data-n-ai/articles/A file format claims to be 100x faster than Parquet.md", "raw/data-n-ai/articles/Lance v2 A New Columnar Container Format.md"]
updated: 2026-10-28
---

# Lance (and LanceDB)

Open-source columnar data format for machine learning and multimodal AI, launched ~2022 by **LanceDB** (YC W22). Designed to fix Parquet's weakness on random access, very large values (embeddings, images) and very wide schemas. Lance v2 is described as a "columnar container format": no row groups, encodings and statistics as extensions, independent per-column metadata.

- Claimed "100x faster than Parquet for random access" (vendor claim; not benchmarked in the ingested sources).
- Reference readers/writers use the Arrow type system; Python API `LanceFileReader` / `LanceFileWriter`.
- Authors cited: Weston Pace, Chang She, Lei Xu, Will Jones and others (arXiv 2504.15247, 2025).

Details: [Columnar File Formats for Random Access](../concepts/columnar-file-formats-for-random-access.md).

## Sources

- [A File Format Claims to Be 100x Faster Than Parquet](../sources/2026-10-22-lance-100x-faster-than-parquet.md)
- [Lance v2: A New Columnar Container Format](../sources/2026-03-31-lance-v2-columnar-container-format.md)
