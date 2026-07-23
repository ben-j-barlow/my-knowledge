---
tags: [data-n-ai, concept, streaming, pipelines, cdc, architecture]
sources: [wiki/sources/write-ahead-intent-log.md]
updated: 2026-07-23
---

# Intent Log Pattern

Architectural approach to CDC and mutation handling that decouples *intent* (what changed) from *payload* (full state), enabling independent schema evolution and database abstraction.

## Components

**Dumb Producer (Proxy)**
- Accepts mutations from application
- Writes intent (dirty keys + operation + metadata) to Kafka
- Writes mutation to database
- Knows nothing about schema or data model
- Decoupled from database technology

**Smart Consumer**
- Polls intent from Kafka
- Verifies state in database (read-your-write)
- Fetches payload from database
- Applies schema validation and business logic
- Publishes full state to event bus
- Owns all complexity; can evolve independently

**Schema Repository**
- Kept outside data plane (not in critical path)
- Consulted by consumer for validation rules
- Can evolve without affecting CDC operations
- Single source of truth for data contracts

## Advantages Over Traditional CDC

| | Traditional CDC | Intent Log |
|---|---|---|
| **Database coupling** | Tightly coupled to database CDC internals | Decoupled via proxy abstraction |
| **Schema evolution** | Schema changes break connectors | Schema lives in registry, independent of pipeline |
| **Scalability** | Simple setup hits bottleneck; scale requires rearchitecture | Scaling is config-driven (Kafka partitions, consumer pools, connection pools) |
| **Ecosystem lock-in** | Dependent on database's CDC features and maturity | Flexible to swap components, databases, streaming layer |
| **State vs deltas** | Emits pre-image/post-image diffs | Emits intent only; consumer fetches current state from DB |

## Tradeoffs

**Read-your-write latency**: For each mutation, consumer must query database to verify state; adds read load  
**Verification timeout**: How long to retry if state isn't visible? (Configurable; default ~10s)  
**Multiple writes racing**: Consumer captures state, not delta history—multiple rapid writes coalesce to final state  
**Not a silver bullet**: Complexity doesn't disappear; it moves from producer to consumer

## Scaling Levers (Dynamic Traffic Reshaping)

- Increase Kafka partitions for hot tables → attach more consumers
- Increase connection pool on consumer → scale database reads independently
- Move tables to separate Kafka brokers → eliminate noisy neighbor issues
- Scale sinks independently (push-based event bus decouples from partition topology)

## See Also

- [[Change Data Capture]] — CDC concept overview
- [[Write-Audit-Publish]] — safety gate often paired with intent-log mutations
- [[Event-Driven Architecture]] — intent logs sit atop event streaming platforms
