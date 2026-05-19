---
tags: [data-n-ai, entity, streaming, etl, pipelines]
sources: [raw/data-n-ai/articles/The Modern Data Stack is Overcomplicated Data Ingestion.md]
updated: 2026-05-19
---

# Confluent

Commercial company built on [Apache Kafka](kafka.md). Provides Confluent Cloud (fully managed Kafka), Confluent Platform (self-managed enterprise distribution), and the widely-adopted Schema Registry. Founded by the original creators of Kafka.

## Confluent Cloud

- Fully managed Kafka-as-a-service
- Throughput-based pricing (pay for what you stream)
- Removes the operational overhead of broker management, partition rebalancing, upgrades
- "Almost always the right call for a small team" compared to self-hosted Kafka

## Pricing Model

Confluent Cloud bills on throughput — predictable, but can add up quickly at high volumes. The trade-off vs. self-hosted: operational cost in engineering time vs. direct infrastructure cost.

## Schema Registry

Confluent's Schema Registry is a widely-adopted central store for Kafka event schemas. Enforces Avro, Protobuf, or JSON Schema contracts between producers and consumers, preventing breaking schema changes from silently corrupting downstream consumers.

## See Also

- [Kafka](kafka.md)
- [Event-Driven Architecture](../concepts/event-driven-architecture.md)
- [Data Ingestion](../concepts/data-ingestion.md)
