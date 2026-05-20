---
tags: [data-n-ai, concept, etl, pipelines]
sources: [raw/data-n-ai/articles/Lakehouse statistics and why query engines get lost.md]
updated: 2026-05-20
---

# Lakehouse Statistics

Statistical metadata that describes the data within a lakehouse table — distinct from structural metadata (schema, partitioning, versioning). Query planners and storage engines depend on this metadata to make efficient decisions. When it's missing, planners guess, producing wrong-shaped query plans, excessive memory spilling, and queries that never finish.

## Two Types of Table Metadata

| Type | What it describes | State of the art |
|------|------------------|-----------------|
| **Structural** | Schema, partitioning, versioning, snapshots, file locations | Well-handled by Iceberg/Delta specs |
| **Statistical** | Data characteristics within files for query planning | Poorly standardised; largely optional; often missing |

## Types of Statistical Metadata

### Simple Counts
- Null value counts, record counts, data size
- Average and max value lengths (used to estimate memory for aggregates and joins)
- **Column cardinality**: number of distinct values — essential for correct join ordering and hash table sizing. Often unpopulated in Iceberg.

### Probabilistic Sketches

Compact summaries (tens of KB) that allow approximate answers over terabytes of data, used primarily by query planners:

| Sketch | What it answers | Primary use |
|--------|----------------|------------|
| **HyperLogLog (HLL)** | Approximate cardinality (distinct value count) | Size hash tables for joins and aggregates |
| **Theta sketch** | Set operations (union, intersection) on data; approximate resulting row counts | Estimate output size from joins and set operations; preferred over HLL for mergeability |
| **KLL** | Quantile sketch — data distribution, predicate selectivity, values in a range | Estimate how many rows a WHERE predicate will return; incrementally mergeable |
| **T-Digest** | Quantile sketch weighted toward extremes (e.g. 99th percentile) | Accurate tail estimates for latency/SLA analysis |
| **Frequent Items / Most Common Values (MCV)** | Lists most common values and their counts | Detect data skew; select correct parallel execution strategy for skewed join keys |
| **Bloom filter** | Definitively states a value is NOT in a dataset (no false negatives) | Skip irrelevant files before reading them |

Additional emerging structures: SuRF (succinct range filter for ranges), prefix bloom filters (useful for URLs/strings).

### Range (Min/Max) Values
Smallest and largest value within a column and row range. The most common data-skipping mechanism.

**Resolution matters**:
- File-level range (Iceberg catalogue): coarse. If a file contains ages 22–64, a predicate for age=40 still reads the entire file.
- Row-group-level range (Parquet optional): finer. Can skip individual row groups.
- Page-level range: finest granularity available.

Iceberg stores range data in the catalogue at file level only — and even that's optional. More granular data is optional in the underlying Parquet files. The result: queries with selective predicates read far more data than necessary.

## The Problem: Everything Is Optional

> "When a query planner has no statistics to count on, it falls back to 'guessing' and will produce wrongly shaped plans, causing long execution times, excessive memory usage and spilling. Some queries may never finish."

- Cardinality statistics: often missing in Iceberg → planner guesses join order from row counts alone → wrong join shape
- MCVs / Frequent Items: often missing → planner can't detect skew → wrong parallel execution strategy
- Range values: only at file level in Iceberg → storage engine reads and discards far too much data
- Bloom filters: rarely present → no file-level skip on point lookups

### Ecosystem Fragmentation
Stats stored in different places between engines:
- **Databricks/Delta Lake**: Delta log + Unity Catalog (API-only access)
- **Iceberg**: "Puffin files" — serialised binary blobs that may be missing or incompatible between engines

The same statistic that one engine writes may not be readable by another engine querying the same table.

## Impact on Query Performance

| Missing stat | Consequence |
|-------------|-------------|
| Cardinality | Wrong join order → large intermediate results → excessive memory, slow execution |
| MCVs | Skew-unaware parallel execution → some workers overwhelmed, others idle |
| Granular range values | Read and discard most data; I/O-bound rather than compute-bound |
| Bloom filters | Can't skip irrelevant files; unnecessary I/O at scan |

## Relationship to Query Optimization

Statistical metadata is the input that makes join ordering, join strategy selection, and data skipping correct rather than approximate. See [Query Optimization](query-optimization.md) for how planners use these statistics.

## The FloeDB Approach

[FloeDB](../entities/floedb.md) is building tools to fix this:
- **Floecat** (open-source): guarantees accurate statistical metadata for Delta Lake and Iceberg, compatible with open standards
- **FloeScan** (in development): extends coverage

## See Also

- [Query Optimization](query-optimization.md)
- [DuckDB](../entities/duckdb.md)
- [Apache Spark](../entities/apache-spark.md)
- [Databricks](../entities/databricks.md)
- [FloeDB](../entities/floedb.md)
- [Source: Lakehouse Statistics and Why Query Engines Get Lost](../sources/lakehouse-statistics-query-planning.md)
