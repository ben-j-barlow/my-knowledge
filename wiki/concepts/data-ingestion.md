---
tags: [data-n-ai, concept, etl, pipelines]
sources: [raw/data-n-ai/articles/The Modern Data Stack is Overcomplicated Data Ingestion.md]
updated: 2026-05-19
---

# Data Ingestion

Moving data from source systems into a central data store (warehouse, lake, lakehouse). The first layer of any data platform. Decisions here compound — silent connector failures, schema drift, and over-engineered streaming setups all become expensive problems 6+ months later.

## Three Approaches

### 1. Managed Connectors
Pre-built, vendor-maintained connectors for common SaaS sources.

**Best for**: Standard SaaS platforms (CRM, finance, marketing, e-commerce) where the connector is well-tested and maintained.

| Tool | Model | Notes |
|------|-------|-------|
| [Fivetran](../entities/fivetran.md) | Proprietary, row-based pricing | Polished, reliable, expensive at volume |
| [Airbyte](../entities/airbyte.md) | Open-source + managed cloud | Flexible, cheaper; variable quality on marketplace connectors |

**Watch out for**: Less popular connectors, false sense of security ("managed" ≠ infallible), pricing that scales badly with volume.

### 2. Event Streaming
Durable message logs with decoupled producers and consumers.

**Best for**: High-volume operational data where sub-minute latency genuinely matters.

| Tool | Notes |
|------|-------|
| [Kafka](../entities/kafka.md) | Dominant open-source; "when you need it, nothing else quite comes close" |
| [Confluent](../entities/confluent.md) | Managed Kafka; almost always the right call for small teams |

**Watch out for**: Operational overhead, and using streaming for sources that update daily.

### 3. Custom Pipelines
Hand-built connectors and scripts, often deployed as Lambda functions or containers.

**Best for**: Niche or legacy sources, APIs too new or obscure for any connector to support.

**Watch out for**: "Free" to run but expensive in engineering time. Needs the same discipline as any other production system: tests, monitoring, documentation, retry logic. Absent these, custom pipelines become a museum of half-maintained scripts nobody fully understands.

## The Hybrid Reality

Most real platforms use all three:
- Managed connectors → standard SaaS sources
- Event streaming → high-volume transactional core systems
- Custom pipelines → the niche exceptions

## Hidden Costs (Often Ignored)

| Cost | Description |
|------|-------------|
| **Engineering time** | "Free" tools cost setup, maintenance, and debugging — this erodes sprint capacity and is usually underestimated |
| **Connector churn** | Upstream API change → sprint derailed; stakeholder trust lost |
| **Schema drift** | Silent column additions, type changes, field removals — managed connectors handle it; custom pipelines only know what you planned for |
| **Over-engineering latency** | "Real-time analytics" usually means "fresh data when I open the dashboard at 9am" — that's batch |

## Decision Framework

1. **What's the source?** Standard SaaS → managed. High-volume + low-latency genuinely needed → streaming. Niche/legacy → custom.
2. **What latency do you actually need?** Daily batch covers 95% of analytics use cases.
3. **How big is your team?** Solo/small → lean on managed. Larger → more hybrid is viable.

> "Start from the simplest option that meets your actual requirements. You can always extend this. The cost of building wrong at the start is cheaper than over-engineering."

## Incremental Loads for Determinism

Full batch loads are non-deterministic when they include LLM-based processing — every re-run produces different output. Converting to incremental daily loads scopes the non-determinism problem:

- A re-run only re-introduces non-determinism into the **last day's** data
- Presumably you're re-running that day because something went wrong — a degree of non-determinism is acceptable in that case
- Incremental loads are also cheaper: each job operates on a fraction of total data

**Trade-off:** Incremental jobs require explicit state management — tracking what has run, managing incremental checkpoints. The engineering overhead is higher than a full load. This is a pre-existing concern independent of AI.

> "Move from full batch data processing to incremental batch data processing to help eschew some non-determinism." — Chris Riccomini

## See Also

- [Event-Driven Architecture](event-driven-architecture.md)
- [Self-Healing Pipelines](self-healing-pipelines.md)
- [Kafka](../entities/kafka.md)
- [Confluent](../entities/confluent.md)
- [Fivetran](../entities/fivetran.md)
- [Airbyte](../entities/airbyte.md)
- [Apache Arrow](../entities/apache-arrow.md)
- [Source: Modern Data Stack — Data Ingestion](../sources/modern-data-stack-ingestion.md)
- [Source: Plan Mode All the Time](../sources/2026-05-21-plan-mode-substrait-de-role.md)
