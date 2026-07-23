---
tags: [data-n-ai, source, streaming, pipelines, cdc]
sources: [raw/data-n-ai/articles/Write-Ahead Intent Log a Foundation for Efficient CDC at Scale.md]
updated: 2026-07-23
---

# Source: Write-Ahead Intent Log — a Foundation for Efficient CDC at Scale

**Authors**: Vinay Chella (DoorDash), Akshat Goel (DoorDash)  
**Format**: QCon San Francisco 2026 talk + transcript  
**Key claim**: Traditional CDC breaks at scale; a dumb-producer/smart-consumer architecture with intent decoupling solves abstraction, scaling, and ecosystem lock-in problems.

## Core Innovation

**Write-Ahead Intent Log (WAIL)** separates *intent* (dirty keys + operation + metadata) from *payload* (full row state):
- **Dumb producer (proxy)**: writes intent to Kafka and database; knows nothing about schema or data model
- **Smart consumer**: reads intent, verifies state against database, publishes full state to event bus; owns all validation logic
- **Schema repository**: lives outside the data plane; can evolve independently of CDC operations

## Why Traditional CDC Fails

| Problem | Why It Matters |
|---------|---|
| **Abstraction**: Each database dialect (Postgres logical replication, Cassandra commit logs, Scylla) forces connectors to expose internals | No unified contract; platform teams become database translators |
| **Scalability trap**: Simple connectors hit bottlenecks; production scale needs distributed components but requires upfront investment | Often not visible until after tech selection (Debezium struggled at DoorDash) |
| **Ecosystem friction**: Uneven connector maturity, features behind paywalls, vendor lock-in (DynamoDB), licensing constraints | Long-term architecture flexibility suffers |
| **Fragility**: Too many moving parts (connector, sinks, consumers); schema changes break connectors; recovery is painful at petabyte scale | System only as good as weakest component |

## Design Principles

1. **Decouple from database technology** — CDC shouldn't be a translator between database dialects
2. **Start simple, let complexity evolve** — don't build for scale day-one
3. **Break free from licensing/ecosystem lock-in** — flexibility to swap components
4. **Contracts evolve independently** — schema changes shouldn't force CDC redesign

## Key Tradeoffs

- **Read-your-write semantics**: Must verify state post-write; adds read load but enables idempotency and recovery
- **Captures state, not deltas**: Most consumers want latest state, not change history
- **Transactional vs independent failures**: Applications choose whether Kafka failure ≠ DB failure
- **Verification latency**: How long to wait for state to be visible? (Default: 10s, configurable)

## See Also

- [[Change Data Capture]] — general CDC concept and patterns
- [[Intent Log Pattern]] — architectural pattern at scale
- [[Event-Driven Architecture]] — WAIL sits atop event logs
