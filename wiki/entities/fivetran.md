---
tags: [data-n-ai, entity, etl, pipelines]
sources: [raw/data-n-ai/articles/The Modern Data Stack is Overcomplicated Data Ingestion.md]
updated: 2026-05-20
---

# Fivetran

Commercial managed data connector service. Pre-built, maintained connectors for hundreds of SaaS and database sources into data warehouses (Snowflake, BigQuery, Redshift, etc.). The dominant managed connector option — positioned as polished and reliable at a premium price.

## Positioning

"The tool you set up once and fully take for granted because it just works."

- Connectors for major SaaS platforms (Shopify, Stripe, NetSuite, Salesforce) are well-tested and reliable
- Less popular connectors can be less maintained and more prone to edge-case failures
- Row-based pricing: easy to forecast at low volume; harder to control at scale

## Pricing

Row-based model — you pay per row synced. Predictable early on, but becomes difficult to manage as data volumes grow. At high enough volume, teams start evaluating whether to rebuild connectors in-house.

## Fivetran vs Airbyte

| | Fivetran | Airbyte |
|-|---------|---------|
| Model | Proprietary SaaS | Open-source + managed cloud |
| Price | Higher, row-based | Cheaper; Airbyte Cloud available |
| Reliability | High for supported connectors | Variable on marketplace connectors |
| Flexibility | Constrained to what Fivetran builds | Extensible; build custom connectors |
| Right for | Teams that want zero maintenance | Teams with engineering bandwidth |

## DuckDB Inside Fivetran

Fivetran uses [DuckDB](duckdb.md) as the embedded engine inside its **Managed Data Lake Service** for merging and compaction operations — lake file merging is handled by DuckDB rather than requiring a separate Spark cluster.

## See Also

- [Airbyte](airbyte.md)
- [DuckDB](duckdb.md)
- [Data Ingestion](../concepts/data-ingestion.md)
- [Source: Modern Data Stack — Data Ingestion](../sources/modern-data-stack-ingestion.md)
- [Source: DuckDB Internals Part 1](../sources/duckdb-internals-part1.md)
