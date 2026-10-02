---
tags: [data-n-ai, entity, etl, pipelines, agents, harness-engineering]
sources: ["wiki/sources/harness-engineering-agentic-data-engineering.md"]
updated: 2026-10-02
---

# Apache DolphinScheduler

An open-source workflow orchestrator cited as a worked example of orchestration exposed as an agent Skill under policy — see [Harness Engineering](../concepts/harness-engineering.md).

## Skill Shape

Generates workflow DAGs and auto-establishes task dependencies; creates real versioned assets (Definitions, Instances, Versions) rather than throwaway scripts; executes and monitors; repairs failed workflows and reruns individual nodes; exposes a GUI specifically for human review of generated plans.

## Agentic Workflow

`human goal → agent plan → policy check → DolphinScheduler executes → agent repairs / human reviews` — the policy check and human-review surface are what distinguish this from an agent just calling a scheduler API directly; it's the orchestration-layer half of the [Harness](../concepts/harness-engineering.md) pattern that [Apache SeaTunnel](apache-seatunnel.md) exposes for data sync.

## Future Direction (per source)

Policy-aware orchestration, built-in human review gates, self-healing workflows, multi-agent coordination.

## Related Pages

- [Harness Engineering](../concepts/harness-engineering.md) — the pattern this is a case study of
- [Apache SeaTunnel](apache-seatunnel.md) — the complementary data-integration case study
- [Source: Rebuilding Data Engineering with Harness Engineering](../sources/harness-engineering-agentic-data-engineering.md)
