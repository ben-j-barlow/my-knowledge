---
tags: [data-n-ai, entity, etl, pipelines, agents, harness-engineering]
sources: ["wiki/sources/harness-engineering-agentic-data-engineering.md"]
updated: 2026-10-02
---

# Apache SeaTunnel

An open-source data integration engine (batch + CDC sync) cited as a worked example of exposing a deterministic tool as an agent **Skill** rather than a bare Tool API — see [Harness Engineering](../concepts/harness-engineering.md).

## Skill Shape

SeaTunnel's CLI is organized around discrete, structured capabilities rather than one monolithic "run a job" call: source/schema/table/field discovery, automatic job generation, batch and CDC sync, structured feedback (status, logs, row counts, errors), and error-driven repair/retry.

Illustrative Skill set from the source article: `DiscoverSource()`, `InspectSchema()`, `CreateBatchSync()`, `CreateCDC()`, `ValidateMapping()`, `RunSyncJob()` — each with defined inputs/outputs rather than free-form parameters.

## The Loop

`Execute → Logs → Repair → Retry` — the agent calls a Skill, reads structured logs/status back, diagnoses a failure, and retries or repairs rather than re-prompting blind.

## Future Direction (per source)

Context-aware field mapping, a broader "Data Flow" Skill, self-healing integration, and AI-ready pipelines generally.

## Related Pages

- [Harness Engineering](../concepts/harness-engineering.md) — the pattern this is a case study of
- [Apache DolphinScheduler](apache-dolphinscheduler.md) — the complementary orchestration-layer case study
- [Change Data Capture](../concepts/change-data-capture.md) — the sync mechanism SeaTunnel's CDC mode implements
- [Source: Rebuilding Data Engineering with Harness Engineering](../sources/harness-engineering-agentic-data-engineering.md)
