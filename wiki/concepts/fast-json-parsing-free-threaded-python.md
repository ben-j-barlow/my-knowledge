---
tags: [data-n-ai, concept, python, performance, json]
sources: ["raw/data-n-ai/articles/2026-10-12-parsing-json-gigabytes-per-second-python.md"]
updated: 2026-10-28
---

# Fast JSON Parsing in Free-Threaded Python

Pattern from [Lemire's benchmark](../sources/parsing-json-gigabytes-per-second-python.md): reach tens of GB/s of NDJSON in a single Python process by combining three things.

1. **SIMD parsing** (simdjson via `fastsimdjson`) instead of the stdlib parser.
2. **Lazy views** (`lazy=True`): parse structurally, create Python objects only for fields you touch. Avoids the dominant cost of building objects that are discarded. msgspec's typed structs give a similar skip-unneeded-fields effect but need a schema up front.
3. **Free-threaded Python 3.14t**: with no GIL, `map_many(fn, data, format="lines", threads=N)` runs the callback on many threads. Use per-thread accumulators (`threading.local`) and merge at the end.

## Numbers

Stdlib 0.18 GB/s one core → fastsimdjson lazy 2.13 GB/s (≈12×) → 65.7 GB/s on 64 threads (≈31× scaling). See source page for the full table.

## When to Use

Selective field extraction from large NDJSON logs/event archives where staying in Python is preferred. If the work is SQL-shaped, [DuckDB](../entities/duckdb.md) reading NDJSON is the alternative (not benchmarked against here).

## Limits

Gains depend on touching few fields and on a many-core machine; benchmark is author-run on one dataset.
