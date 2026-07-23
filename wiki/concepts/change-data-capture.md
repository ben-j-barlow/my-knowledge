---
tags: [data-n-ai, concept, streaming, pipelines, cdc]
sources: [wiki/sources/write-ahead-intent-log.md, wiki/sources/modern-data-stack-ingestion.md, wiki/sources/halodoc-self-healing-pipelines.md]
updated: 2026-07-23
---

# Change Data Capture (CDC)

Real-time stream of all mutations (inserts, updates, deletes) from a source database, enabling downstream systems to stay in sync without polling.

## Why CDC Matters

- **Real-time consistency**: Derived datastores (search, cache, analytics) stay synchronized with source-of-truth database
- **Eliminates polling**: Removes load on source system and reduces latency
- **Alternative to dual-write**: Single mutation → CDC → multiple consumers (no inconsistency window)
- **Enables multiple architectures**: Outbox pattern, materialized views, heterogeneous datastore sync, business analytics

## Architecture Dimensions

**Producer side**: How does the database emit changes?
- Logical replication logs (Postgres, MySQL)
- Commit logs (Cassandra, DynamoDB Streams)
- Polling (fallback for databases without native CDC)

**Transport**: Kafka, Pulsar, or custom log systems

**Consumer side**: What do downstream systems do with changes?
- Sync derived datastores (search, cache)
- Trigger workflows
- Populate analytics warehouse
- Feed event bus for business logic

## Common Patterns

- **Write-Audit-Publish**: Staging → validation (contracts) → publish to production
- **Intent Log**: Separate intent (what changed) from payload (full state); enables independent schema evolution
- **Dual writes** (anti-pattern): Write to database and event system in separate transactions; breaks under failure

## Tradeoffs

**Abstraction cost**: Different databases have different CDC semantics and guarantees; no standard contract  
**Operational load**: Connectors can break (schema changes), sinks can lag, recovery is hard at scale  
**Ecosystem**: Features like exactly-once semantics often sit behind paywalls; connector maturity varies widely

## See Also

- [[Intent Log Pattern]] — architectural approach to CDC at scale
- [[Event-Driven Architecture]] — CDC as the transport layer
- [[Data Ingestion]] — CDC as one of three ingestion approaches
