---
tags: [data-n-ai, source, etl, pipelines, lakehouse]
sources: [raw/data-n-ai/articles/Why We Moved from Hive-Style Data Lakes to Apache Iceberg?.md]
updated: 2026-07-23
---

# Source: Why We Moved from Hive-Style Data Lakes to Apache Iceberg

**Author**: Naidu Rongali (Sr Data & AI Engineer, Patent Holder)  
**Context**: Four-year hive-style data lake journey at scale; migration decision triggered by AWS ecosystem convergence on Iceberg.

## Architecture Started With

```
Athena/Spark/Trino
       ↓
   AWS Glue Catalog
       ↓
Hive-style Partitions
       ↓
Parquet Files on S3
```

Worked well for years: simple, open, cost-effective. But...

## Seven Problems With Hive

1. **Directory-based file discovery doesn't scale** — 50,000 files = 50 S3 LIST requests (1,000 keys/response max); query planning itself becomes expensive
2. **Partition structure couples metadata to layout** — changing partition strategies requires massive rewrites; can't decouple partitioning from storage
3. **Partition evolution requires data rewrites** — daily vs monthly partitioning change? Rewrite petabytes
4. **Readers see partial writes** — queries arriving mid-write observe incomplete data; no snapshot isolation
5. **Schema evolution is fragile** — column renames/drops/adds cause query failures; position/name-based matching breaks across schema versions
6. **Designed for append-only, not ACID** — updates/deletes/merges require workarounds; GDPR compliance is painful
7. **No time travel** — can't access historical versions; recovery and auditing are difficult

## How Iceberg Differs

Not a file format replacement; a **metadata architecture** for managing data lakes.

- **Metadata layer** tracks schemas, partitions, snapshots, file statistics, locations
- **Column IDs** (not names/positions) decouple schema evolution from physical rewrites
- **Snapshot-based ACID** — all readers see complete snapshot; no partial writes
- **Partition specs in metadata** — can evolve without touching old data
- **Copy-on-Write or Merge-on-Read** — row-level mutations without full rewrite
- **Time travel** — all snapshots retained for auditing/recovery/reproducibility

## Operational Tradeoffs

| Approach | Control | Effort |
|----------|---------|--------|
| Self-Managed Iceberg | High | High |
| Iceberg + AWS Glue Maintenance | Medium | Medium |
| Amazon S3 Tables (fully managed) | Low | Low |

## See Also

- [[Hive-Style Data Lake Limitations]] — detailed breakdown of each problem
- [[Apache Iceberg]] — iceberg mechanics and capabilities
- [[Data Layout]] — partitioning/clustering comparison
