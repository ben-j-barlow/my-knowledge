---
tags: [data-n-ai, source, pipelines, observability, data-quality]
sources: [raw/data-n-ai/articles/Data quality traffic lights.md]
updated: 2026-07-23
---

# Source: Data Quality Traffic Lights

**Author**: Robert Sahlin (Nordnet)  
**Key idea**: Visual trust signals (red/yellow/green badges) in dashboards + data catalog, informed by automated incident detection and blast-radius calculation.

## Three Pillars

**Detection** — Catch 5 failure modes:
- Failed dbt tests (deduped by incident boundaries: when did fail *start*, when did it *end*)
- Failed transformation runs (including *silent* midway crashes detected via audit logs)
- Source freshness violations (upstream systems stopped updating)
- Data volume anomalies (ML-based via BigQuery TimesFM; tunable per table for weekend/holiday suppression)
- Manual incidents (Streamlit UI for ops team)

**Lineage** — Calculate blast radius:
- Extract dbt lineage from manifest (table-to-table dependencies)
- Extract Looker lineage from LookML (which tables feed each explore)
- Stitch together to answer: if table X broke, which dashboards are affected?

**Communication** — Surface in three places:
- Per-dashboard badge (green ✓ / yellow ⚠ / red ✗)
- Platform health dashboard (centralized ops view, sorted by severity)
- Queryable incident table (for agents, services, ML pipelines to check before consuming data)

## Implementation Choices

| Decision | Why |
|----------|-----|
| **Batch lineage** (daily refresh) | DAG changes rarely; 24h staleness acceptable; simpler than real-time |
| **Incident state in SQL** | Window functions + QUALIFY; no external state management |
| **TimesFM for anomalies** | Handles seasonality/trends automatically; low maintenance; runs in BigQuery |
| **Per-table tuning** | User-driven tables natural weekend dips; system tables don't; suppress appropriately |

## Impact Beyond Dashboards

- **Agents**: Check incident status before generating queries; warn if data is unreliable
- **ML models**: Abort retraining if source data has active incidents; prevent garbage-in
- **Operational services**: Make graceful degradation decisions (pricing, reporting)
- **Data catalog**: Enrich asset metadata with current health status

## See Also

- [[Data Quality Observability]] — observing data health across the pipeline
- [[Blast Radius]] — calculating impact scope of failures
- [[Event-Driven Architecture]] — incident status as a queryable event stream
