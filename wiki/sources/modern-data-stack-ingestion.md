---
tags: [data-n-ai, source, etl, pipelines, streaming]
sources: [raw/data-n-ai/articles/The Modern Data Stack is Overcomplicated Data Ingestion.md]
updated: 2026-05-19
---

# The Modern Data Stack is Overcomplicated: Data Ingestion

> Source: https://lukewhittaker.substack.com/p/the-modern-data-stack-is-overcomplicated-5ff
> Author: Luke Whittaker
> Published: 2026-05-13

## Summary

Part 2 of a 10-part series on the modern data stack. Covers the three main data ingestion approaches — managed connectors, event streaming, and custom pipelines — with honest assessments of what each is like to live with, including the hidden costs that only appear 6+ months in. Core argument: start with the simplest option that meets actual requirements; most teams over-engineer for latency they don't need.

## Key Claims

### The Three Approaches

**Managed connectors** (Fivetran, Airbyte):
- Best for standard SaaS sources (Shopify, Stripe, NetSuite, CRM, finance, marketing)
- Fivetran: polished, reliable, row-based pricing — expensive at volume but "set it and forget it"
- Airbyte: open-source, flexible, cheaper; quality variable on non-Airbyte-approved marketplace connectors
- Watch out for: less popular connectors, false sense of security

**Event streaming** (Kafka, Confluent):
- When you need it, "nothing else quite comes close" — high-volume operational data, event-driven architectures, sub-second latency
- The problem: "real-time" sounds great in planning meetings; then someone proposes Kafka for a source that updates once a day
- Managed Kafka (Confluent) is "almost always the right call for a small team"; self-hosted is a full-time job
- Watch out for: operational overhead, using it because it sounds cool

**Custom pipelines**:
- Niche or legacy sources where no connector exists or works properly
- No vendor to blame; you own every bug, every schema change, every retry, forever
- "Free" to run but expensive in engineering time to build, test, monitor, maintain
- Watch out for: accumulating dozens of half-maintained scripts

### Hidden Costs
- **Engineering time** is the big one — "free" tools aren't free; setup, maintenance, and debugging erode sprint velocity
- **Connector churn**: one API change by an upstream provider derails a sprint and loses stakeholder trust
- **Schema drift**: silent column changes, data type changes — managed connectors handle it; custom pipelines only know what you planned for
- **Over-engineering latency**: "real-time analytics" usually means "I want fresh data when I look at the dashboard at 9am" — that's batch

### Decision Framework

| Factor | Managed connector | Event streaming | Custom pipeline |
|--------|------------------|-----------------|-----------------|
| Standard SaaS source | ✓ | | |
| High-volume, sub-minute latency genuinely needed | | ✓ | |
| Niche/legacy source, no connector exists | | | ✓ |
| Solo/small team | ✓ | | |
| Large platform team | Any | Any | Any |

- "Daily batch is fine for 95% of analytics use cases"
- "Start from the simplest option that meets your actual requirements"

### The Hybrid Reality
Most real platforms end up with all three: managed connectors for SaaS → Kafka for high-volume transactional events → custom pipelines for the niche cases.

## Related Wiki Pages

- [Data Ingestion](../concepts/data-ingestion.md)
- [Event-Driven Architecture](../concepts/event-driven-architecture.md)
- [Kafka](../entities/kafka.md)
- [Confluent](../entities/confluent.md)
- [Fivetran](../entities/fivetran.md)
- [Airbyte](../entities/airbyte.md)
