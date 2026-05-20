---
tags: [data-n-ai, entity, etl, pipelines]
sources: [raw/data-n-ai/articles/Lakehouse statistics and why query engines get lost.md, raw/data-n-ai/articles/Why Spark joins are expensive - and what to do about it.md]
updated: 2026-05-20
---

# FloeDB

Database technology company building a new cloud query engine and lakehouse statistics tooling. Publishes the "Database Doctor" technical blog series on query engine internals (Spark join strategies, lakehouse statistics, etc.).

## Products

**Floecat** (open-source): fixes the missing/incomplete statistical metadata problem in Delta Lake and Iceberg. Guarantees accurate statistical metadata that query planners can rely on while remaining compatible with open standards. Available at github.com/eng-floe/floecat.

**FloeScan** (in development, not yet announced as of May 2026): extends statistical metadata coverage.

**New query engine**: FloeDB is building a database engine for the cloud designed to produce better query plans and use modern hardware as intended.

## Why They Exist

Statistical metadata is optional in both Iceberg and Delta Lake specs, is stored differently between the two ecosystems, and is frequently not populated by data producers. This causes query planners to guess — producing wrong join order, wrong join strategies, excessive memory spilling, and queries that never finish. See [Lakehouse Statistics](../concepts/lakehouse-statistics.md).

## See Also

- [Lakehouse Statistics](../concepts/lakehouse-statistics.md)
- [Query Optimization](../concepts/query-optimization.md)
- [Apache Spark](apache-spark.md)
- [Databricks](databricks.md)
