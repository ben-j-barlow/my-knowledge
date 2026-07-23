---
tags: [data-n-ai, concept, etl, pipelines, lakehouse]
sources: [wiki/sources/hive-to-iceberg-migration.md]
updated: 2026-07-23
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

## See Also

- [[Hive-Style Data Lake Limitations]] — problems Iceberg solves
- [[Data Layout]] — partitioning tradeoffs across formats
- [[Change Data Capture]] — Iceberg enables CDC-heavy pipelines
