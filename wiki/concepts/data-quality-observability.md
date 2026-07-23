---
tags: [data-n-ai, concept, pipelines, observability, data-quality]
sources: [wiki/sources/data-quality-traffic-lights.md, wiki/sources/halodoc-self-healing-pipelines.md]
updated: 2026-07-23
---

# Data Quality Observability

Making data health visible across pipelines. Enables data teams to detect, diagnose, and recover from failures—and surfaces trust signals to downstream consumers and automated systems.

## Three Dimensions

**Detection**: Identify failures across multiple modes (test failures, volume anomalies, staleness, schema breaks, etc.)

**Context**: Calculate impact scope (lineage, blast radius, affected consumers) so teams know what to fix and who to notify

**Communication**: Surface signals where decisions happen (dashboards, catalogs, agents, services) not just in logs/alerts

## Observability Stack

| Layer | Purpose | Example |
|-------|---------|---------|
| **Metrics** | Volume written, row counts, column distributions | TimesFM anomalies, dbt test pass rates |
| **Logs** | Detailed execution traces (run results, errors, timing) | dbt Cloud run logs, Spark executor logs |
| **Lineage** | Dependency graph and blast radius | dbt manifest + Looker LookML extraction |
| **Incidents** | Structured failure records with lifecycle (active/resolved/expired) | Test failure incident spanning Mon–Wed |
| **Trust signals** | User-facing health status at point of consumption | Traffic light badge in dashboard |

## Key Patterns

**Traffic lights** — Red/yellow/green status badges showing data health at consumption points

**Incident deduplication** — Group repeated failures into single incident with clear start/end times; reduces alert fatigue

**Self-healing gates** — Automatic checks before critical operations (agent queries, ML retraining, service startup) that degrade gracefully if data is unhealthy

**Historical incident tracking** — Retain all incidents post-resolution to analyze trends (which teams, which domains, which failure types are most common)

## Tradeoffs

**Accuracy vs tuning**: ML-based anomaly detection requires per-table configuration for seasonality/holidays; not fire-and-forget

**Real-time vs batch**: Lineage updates can be batch (daily); incident detection should be near real-time

**Ownership**: Traffic lights tell *that* data is broken, but context (team ownership, remediation links, investigation tips) makes them actionable

## See Also

- [[Data Quality Traffic Lights]] — implementation pattern: visual trust signals at consumption points
- [[Self-Healing Pipelines]] — using observability to drive automatic recovery
- [[Data Contracts]] — formalize what "healthy" means for each dataset
