---
tags: [data-n-ai, entity, streaming, etl, pipelines]
sources: [raw/data-n-ai/articles/The Modern Data Stack is Overcomplicated Data Ingestion.md]
updated: 2026-05-19
---

# Apache Kafka

Open-source distributed event streaming platform. The dominant implementation of [event-driven architecture](../concepts/event-driven-architecture.md) for high-volume, low-latency data pipelines. Originally developed at LinkedIn, now an Apache project.

## What Kafka Is

A durable, partitioned, distributed log. Producers write events to named topics; consumers read from those topics independently, at their own pace, from any historical offset. The log retains events for a configurable retention period — consumers can replay past events.

## Key Concepts

| Concept | Description |
|---------|-------------|
| Topic | Named category of events |
| Partition | Subdivision of a topic; unit of parallelism and ordering |
| Consumer group | Set of consumers sharing the work of reading a topic |
| Offset | Consumer's position in a partition |
| Schema registry | Central store of event schemas (enforces contracts) |
| Dead letter queue | Destination for unprocessable events; prevents pipeline stalls |

## When to Use Kafka

- High-volume operational data (order events, user activity, financial transactions)
- Event-driven architectures where downstream systems react in real time
- Multiple consumers with different needs from the same event stream
- Need for event replay, audit trails, or historical processing

## When Not to Use Kafka

- Sources that update once a day or less
- Small teams without dedicated platform engineers
- Analytics use cases where a 9am batch job meets the actual need
- "Using Kafka because it sounds cool rather than actually needing it will outlast the initial enthusiasm"

## Operational Reality

Self-hosted Kafka is a full-time operational job: broker management, partition rebalancing, schema evolution, consumer lag monitoring, dead letter queue processing, and upgrade coordination. The operational surface is wide. Unless a team has specific requirements and dedicated bandwidth, self-hosted is rarely the right call.

Managed Kafka via [Confluent](confluent.md) is "almost always the right call for a small team."

## See Also

- [Event-Driven Architecture](../concepts/event-driven-architecture.md)
- [Confluent](confluent.md)
- [Data Ingestion](../concepts/data-ingestion.md)
- [Source: Modern Data Stack — Data Ingestion](../sources/modern-data-stack-ingestion.md)
