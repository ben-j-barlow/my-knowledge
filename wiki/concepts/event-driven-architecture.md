---
tags: [data-n-ai, concept, streaming, etl, pipelines]
sources: [raw/data-n-ai/articles/The Modern Data Stack is Overcomplicated Data Ingestion.md]
updated: 2026-05-19
---

# Event-Driven Architecture (EDA)

A design pattern where systems communicate by producing and consuming discrete events, rather than through direct calls or batch file transfers. Producers emit events to a durable log (e.g. a Kafka topic); consumers read from that log independently, at their own pace. The key property: producers and consumers are **decoupled** — neither knows about the other.

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Topic** | Named category/stream of events (e.g. `user.signed_up`, `order.placed`) |
| **Partition** | A topic is split into partitions for parallelism and ordering guarantees within a partition |
| **Producer** | System that writes events to a topic |
| **Consumer group** | One or more consumers that share the work of reading a topic; each partition is read by exactly one consumer in the group |
| **Offset** | Position of a consumer in a partition — consumers can replay from any past offset |
| **Schema registry** | Central store of event schemas; enforces contracts between producers and consumers |
| **Dead letter queue (DLQ)** | Destination for events a consumer couldn't process; prevents pipeline stalls |

## When EDA Is the Right Choice

- High-volume operational data (order events, user activity, financial transactions)
- Systems that need to react to changes in milliseconds
- Multiple downstream consumers with different needs from the same event stream
- Need for event replay or historical processing

## When EDA Is Not the Right Choice

The "real-time" label is frequently misused:

- If the source updates once a day, the operational overhead of a streaming system outweighs any latency benefit
- If the downstream use case is a dashboard that stakeholders check each morning, batch ingestion meets the actual need
- Small teams without dedicated platform engineers will find self-hosted Kafka consuming disproportionate operational bandwidth
- "Using Kafka because it sounds cool rather than actually needing it will outlast the initial enthusiasm"

## Operational Costs

Beyond infrastructure: topics, partitions, consumer groups, schema registries, dead letter queues, consumer lag monitoring, rebalancing behavior, and schema evolution rules all need ongoing attention. Self-hosted Kafka in particular is a full-time operational job; managed Kafka (Confluent Cloud) is almost always the right call for teams without dedicated platform engineers.

## Common Implementation

[Kafka](../entities/kafka.md) is the dominant implementation. [Confluent](../entities/confluent.md) is the leading managed Kafka offering.

## See Also

- [Kafka](../entities/kafka.md)
- [Confluent](../entities/confluent.md)
- [Data Ingestion](data-ingestion.md)
- [Source: Modern Data Stack — Data Ingestion](../sources/modern-data-stack-ingestion.md)
