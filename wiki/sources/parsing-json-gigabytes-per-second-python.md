---
tags: [data-n-ai, source, python, performance, benchmarks, json]
sources: ["raw/data-n-ai/articles/2026-10-12-parsing-json-gigabytes-per-second-python.md"]
updated: 2026-10-28
---

# Source: Parsing JSON at Tens of Gigabytes per Second… in Python

**Author**: Daniel Lemire · **Published**: 2026-10-12
**URL**: https://lemire.me/blog/2026/10/12/parsing-json-at-tens-of-gigabytes-per-second-in-python/
**Type**: Benchmark blog post by the library's author (vendor-style bias: the winner is his own binding). Concept page: [Fast JSON Parsing in Free-Threaded Python](../concepts/fast-json-parsing-free-threaded-python.md).

## Setup

- Task: GH Archive NDJSON, 8 hours of 2024-03-13 → 7.6 GB decompressed, 2.2 M events (~3.4 kB each). Count events by type; for opened PRs, count by repo language. Result: 65,269 PRs opened (TypeScript 11,565; JavaScript 7,778; Python 7,057; Java 4,668; ~5,857 no language).
- Hardware: 2× Xeon Gold 6548N (64 cores), Python 3.14.6 (free-threaded `python3.14t`, no GIL), fastsimdjson 0.6.0, orjson 3.13.0, msgspec 0.22.0. Data decompressed in memory before timing; best of 7 runs (1 run for slow methods). Outputs verified identical.

## Results (GB/s)

| Method | 1 core | 64 threads |
|---|---|---|
| `json` stdlib | 0.18 | 3.17 |
| orjson | 0.42 | — |
| fastsimdjson `map_many` | 0.63 | 29.8 |
| msgspec (typed structs) | 1.29 | 24.6 |
| fastsimdjson `map_many`, `lazy=True` | 2.13 | **65.7** |

Stdlib takes 42 s single-core; lazy fastsimdjson takes 3.6 s on one core and ~0.12 s on 64 threads (31× scaling).

## Key Takeaways

- Materialising every value as Python objects dominates cost; methods that do so (json, orjson, non-lazy simdjson) are slow.
- **Lazy views** create Python objects only for accessed fields (idea from Tyler Kennedy's pysimdjson); msgspec gets a similar effect but needs a declared schema.
- Free-threaded Python makes thread parallelism real; per-thread accumulators (`threading.local`) avoid contention, then a tiny merge step.
- Even stdlib `json` scales only ~17× to 3 GB/s on 64 threads.

## Relevance

For agent/data work: shows that "Python is slow for data" depends on object materialisation, not the interpreter alone. Relates to the [CLI Tools for Agents](../concepts/cli-tools-for-agents.md) argument that agent-generated Python is often the weak link, and to [DuckDB](../entities/duckdb.md) as the SQL alternative for NDJSON. No DuckDB comparison is in the post.

## Caveats

64-core server, field-subset workload (the lazy advantage shrinks if you read most fields), single dataset, author-run benchmark.
