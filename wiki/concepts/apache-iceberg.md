---
tags: [data-n-ai, concept, etl, pipelines, lakehouse]
sources: [wiki/sources/hive-to-iceberg-migration.md, wiki/sources/duckdb-400k-skill.md]
updated: 2026-09-11
---

# Apache Iceberg

**Not a file format; a metadata architecture** for managing data lakes. Still uses Parquet (or ORC/Avro) for data storage; innovation is in the metadata layer above.

## Metadata Hierarchy

```
Glue Catalog → metadata.json → Snapshot → Manifest List → Manifests → Parquet Files
```

- **Glue Catalog Table**: Pointer to current metadata file (metadata_location)
- **metadata.json**: Schema, partitions, snapshot history, current snapshot pointer, table properties
- **Snapshot**: Consistent table version at point-in-time (enables ACID, time travel)
- **Manifest List**: Index tracking which manifests belong to a snapshot
- **Manifest Files**: File locations + statistics (count, size, null counts, min/max values)
- **Parquet Data Files**: Actual table data (unchanged from Hive)

## Key Differences from Hive

| Aspect | Hive | Iceberg |
|--------|------|---------|
| **Metadata storage** | Directory paths | Manifest files + JSON |
| **File discovery** | List S3 directories | Read manifest metadata |
| **Schema matching** | Column names/positions | Column IDs (immutable) |
| **Partitioning** | Embedded in paths | In metadata; can evolve |
| **Consistency** | File-level visibility | Snapshot-based ACID |
| **Updates/Deletes** | Full-table rewrites | Copy-on-Write or Merge-on-Read |
| **Time travel** | Manual snapshots | Native snapshots |

## Core Capabilities

**Column IDs**: Every column gets permanent integer ID; decouples names from identity. Schema evolution doesn't require data rewrites.

**Snapshot isolation**: Every commit creates snapshot. All readers see consistent state; no partial writes.

**Partition evolution**: Change partition specs without rewriting old data; metadata tracks which spec applies to each file.

**ACID transactions**: Copy-on-Write (fast reads, slower writes) or Merge-on-Read (fast writes, slower reads); choose based on workload.

**Time travel**: Query historical snapshots for auditing, recovery, reproducibility.

## Operational Complexity

Iceberg introduces metadata maintenance responsibilities:
- **Compaction**: Merge small files to reduce query planning overhead
- **Snapshot expiration**: Prune old snapshots to control storage costs
- **Orphan cleanup**: Remove unreferenced metadata files

**Trade-off options**:
- Self-managed: full control, high effort
- AWS Glue maintenance: scheduled compaction/expiration
- S3 Tables: fully managed, lowest effort

## 2026 Adoption Notes

- **Apache Polaris** — a free, self-hostable REST catalog — graduated to a top-level Apache project in February 2026, removing "which catalog" as a blocker for local/self-managed Iceberg work.
- A Ryft survey of 252 senior data leaders (early 2026) found Iceberg had moved from "emerging option" to core enterprise data-platform infrastructure.
- **[DuckDB](../entities/duckdb.md) shipped Iceberg write support in v1.5.3** (May 2026) — `MERGE INTO`, `ALTER TABLE`, partition transforms, Iceberg V3 — ending the prior requirement that all Iceberg writes go through a Spark cluster. See [Source: DuckDB Just Put a $400K/Year Skill on Your Laptop](../sources/duckdb-400k-skill.md).
- Real-world operational failure modes cited alongside the above: manifest explosion (query planning 0.5s at 30 manifests → 4s+ at 300, before compaction) and small-file accumulation — both invisible at laptop scale, both live risks at production scale.

## See Also

- [[Hive-Style Data Lake Limitations]] — problems Iceberg solves
- [[Data Layout]] — partitioning tradeoffs across formats
- [[Change Data Capture]] — Iceberg enables CDC-heavy pipelines
- [DuckDB](../entities/duckdb.md) — now a viable local Iceberg write engine
- [Source: DuckDB Just Put a $400K/Year Skill on Your Laptop](../sources/duckdb-400k-skill.md)
