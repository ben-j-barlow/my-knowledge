---
tags: [data-n-ai, concept, pipelines, observability, data-quality]
sources: [wiki/sources/data-quality-traffic-lights.md]
updated: 2026-07-23
---

# Data Quality Traffic Lights

Visual trust signals (red/yellow/green) embedded in dashboards, data catalogs, and automated systems to surface data health in real-time. Answers the question: *Can I trust this data right now?*

## Three States

- **Green** (✓): All upstream dependencies healthy; safe to consume
- **Yellow** (⚠): Warnings active (volume anomalies, minor issues); use with caution
- **Red** (✗): Critical failures (test failures, run crashes, stale data); unreliable

## Core Pattern

```
Incident Detection → Lineage Mapping → Trust Signal Display
       ↓                    ↓                   ↓
(What broke?)      (What's affected?)    (Where users work)
```

**Detection** identifies failures across a structured taxonomy (test failures, run failures, freshness violations, volume anomalies, manual incidents).

**Lineage** calculates blast radius—which tables, models, and dashboards inherit each incident—enabling precise scoping of impact.

**Display** surfaces signals where consumption happens: dashboard headers, data catalog asset pages, agent decision points, service startup checks.

## Why It Works

- **Trust before use**: Users see warnings *before* acting on metrics
- **Reduces silent failures**: Volume anomalies and freshness violations caught automatically
- **Automates escalation**: Platform team sees incidents proactively, not via user complaints
- **Informs agents**: ML agents check health before training; SQL agents check before querying
- **Reduces alert fatigue**: Consolidate 100 individual test failures into one incident spanning failure period

## Design Decisions

**Batch vs real-time**: Lineage updates daily (sufficient for DAG changes); incident detection near real-time
**State machine**: Active → Resolved (first success after fail) → Expired (30d no execution) → Manually Closed
**Tuning matters**: Per-table configuration for anomaly detection (weekend suppression, seasonality, sensitivity)
**Lineage is hard**: Invest here first; detection is easier than calculating accurate blast radius

## Failure Modes

| Mode | Detection | Recovery Signal |
|------|-----------|-----------------|
| Test failure | dbt test runner | First passing run after failure |
| Run crash | Audit log mismatch (planned vs executed models) | Successful completion |
| Stale source | dbt source freshness checks | Source data updates |
| Volume anomaly | ML time-series forecasting | Data volume returns to expected range |
| Manual incident | Streamlit ops interface | Manual resolution or auto-expire (30d) |

## See Also

- [[Data Quality Observability]] — broader strategy for monitoring data pipeline health
- [[Change Data Capture]] — streaming approach to feeding downstream dependencies
- [[Write-Audit-Publish]] — deterministic validation gate that can feed traffic light status
