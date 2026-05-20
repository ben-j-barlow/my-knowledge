---
tags: [data-n-ai, source, etl, pipelines]
sources: [raw/data-n-ai/articles/Lakehouse statistics and why query engines get lost.md]
updated: 2026-05-20
---

# Lakehouse Statistics and Why Query Engines Get Lost

> Source: https://www.linkedin.com/pulse/lakehouse-statistics-why-query-engines-get-lost-neil-carson-agnac/
> Author: FloeDB Inc
> Published: 2026-05-11

## Summary

Statistical metadata in lakehouses is to SQL engines what maps are to delivery drivers. Without it, planners guess — and guessing produces wrong join order, wrong join strategy, excessive memory spilling, and queries that never finish. The problem: most statistical metadata is optional in Iceberg and Delta Lake specs, often not populated, stored differently between engines, and frequently incompatible. FloeDB's Floecat and FloeScan aim to fix this.

## Key Claims

### Two Metadata Categories
- **Structural metadata**: schema, partitioning, versioning, snapshots, how to find files — well-handled by Iceberg/Delta specs
- **Statistical metadata**: data characteristics used to plan queries optimally — poorly standardised, often missing

### Types of Statistical Metadata

**Simple counts**: null counts, record counts, data size, average/max value lengths — needed to estimate memory for aggregates and joins; cardinality needed to order joins correctly and size hash tables

**Probabilistic sketches** (10s of KB instead of TBs):
- **HyperLogLog (HLL)**: approximate cardinality (distinct value count) → sizes hash tables for joins and aggregates
- **Theta sketch**: set operations (union, intersection) on data → estimates row counts from multiple joins; preferred over HLL for ease of merging
- **KLL**: quantile sketch → estimates predicate selectivity, data distribution; can answer "how many values in range X–Y"; incrementally mergeable
- **T-Digest**: quantile sketch weighted toward extremes (99th percentile accuracy) vs whole range
- **Frequent Items / Most Common Values (MCV)**: lists most common values and counts → detects data skew, corrects parallel execution strategy for skewed keys
- **Bloom filter**: definitively states a value is NOT in a dataset (no false negatives, some false positives) → skip irrelevant files before reading

**Range (min/max) values**: smallest and largest value within a column and row range — the most common data skipping mechanism; can be stored at file level (coarse) or row group/page level (granular)

### The Problem: Everything Is Optional

> "When a query planner has no statistics to count on, it falls back to 'guessing' and will produce wrongly shaped plans, causing long execution times, excessive memory usage and spilling. Some queries may never finish."

- Most of the above is optional in Iceberg, Delta Lake, or both
- Cardinality statistics (needed for correct join ordering) are often unpopulated in Iceberg
- Range values in Iceberg are stored in the catalogue only at file level — not per row group or page
- Databricks stores stats in Delta log and Unity Catalog (API-only); Iceberg uses "Puffin files" (binary blobs that may be missing or incompatible between engines)
- "It's a mess" — same statistics stored in completely different places between engines

### Impact
Without cardinality → planner can only guess join order from row counts → wrong-shaped query plans  
Without MCVs → planner can't detect skew → wrong parallel execution strategy  
Without granular range values → storage engine reads far too much data → high cost, slow queries  
Without Bloom filters → can't skip irrelevant files → unnecessary I/O

### FloeDB's Solution
- **Floecat** (open-source, github.com/eng-floe/floecat): fixes statistical metadata for Delta Lake and Iceberg, guarantees accurate stats compatible with open standards
- **FloeScan** (not yet announced at publication): extends coverage

## Related Wiki Pages

- [Lakehouse Statistics](../concepts/lakehouse-statistics.md)
- [Query Optimization](../concepts/query-optimization.md)
- [FloeDB](../entities/floedb.md)
- [DuckDB](../entities/duckdb.md)
