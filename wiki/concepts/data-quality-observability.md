---
tags: [data-n-ai, concept, pipelines, observability, data-quality, agents]
sources: [wiki/sources/data-quality-traffic-lights.md, wiki/sources/halodoc-self-healing-pipelines.md, wiki/sources/lecture-11-runtime-observability.md]
updated: 2026-09-11
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

## Agent Harness Observability (Same Principle, Applied to Agent Runs)

The pipeline-observability idea above — surface health where decisions get made, don't leave it in logs — has a direct analogue in AI coding-agent harnesses, where the "data" being observed is the agent's own run. Without it, reliability becomes an evidence-free guessing exercise: agents can't distinguish "correct" from "looks correct" (code review shows what was *written*, runtime tracing shows what actually *ran*), evaluation becomes irreproducible ("doesn't feel right" from one evaluator, "looks fine" from another), retries become blind, and session handoffs lose 30–50% of their time to redundant re-diagnosis of state nobody recorded.

The harness needs two layers, mirroring detection+context above:

- **Runtime observability** — system-level signals: logs, traces, process events, health checks, resource utilization, full error context. Answers "what did the system do."
- **Process observability** — visibility into the harness's own decision artifacts: plans, **sprint contracts** (a short-term scope/verification/exclusions agreement negotiated *before* coding starts, so the evaluator isn't rejecting work for foreseeable reasons), and **evaluator rubrics** (dimension-by-dimension structured scoring that makes two different evaluators converge on the same score for the same output). Answers "why should this change be accepted."

Anthropic's March 2026 three-agent (planner/generator/evaluator) experiment building a browser-based DAW is the worked example: sprint contracts plus a scoring rubric plus runtime traces took a dark-mode-style task from 3–4 blind retry rounds (~45 min) to one iteration with specific, evidence-backed feedback (~15 min) — a 3x efficiency gain with observability as the only changed variable. Neither layer substitutes for the other: agents can't produce sprint contracts or rubrics just by "printing more logs" — those are structured harness artifacts, not incidental output.

## See Also

- [[Data Quality Traffic Lights]] — implementation pattern: visual trust signals at consumption points
- [[Self-Healing Pipelines]] — using observability to drive automatic recovery
- [[Data Contracts]] — formalize what "healthy" means for each dataset
- [Premature Completion Declaration](premature-completion-declaration.md) — the failure mode sprint contracts and evaluator rubrics are designed to prevent
- [Feature Lists](feature-lists.md) — the state-machine analogue for agent task scope
- [Source: Lecture 11 — Making the Agent's Runtime Observable](../sources/lecture-11-runtime-observability.md)
