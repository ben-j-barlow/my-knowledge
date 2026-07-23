---
tags: [data-n-ai, source, agents, pipelines, operations]
sources: [raw/data-n-ai/articles/7 Crucial Barriers between Data Teams and Self-Healing Data Architecture.md]
updated: 2026-07-23
---

# Source: 7 Barriers Between Data Teams and Self-Healing Architecture

**Author**: Hugo Lu (DataOps Leadership)  
**Key distinction**: "Self-healing" ≠ "human-assisted fixes"; it means autonomous operation without human intervention.

## Seven Barriers (and What's Needed)

| Barrier | Problem | Solution Required |
|---------|---------|-------------------|
| **Context & failure recall** | Agents don't know domain-specific workarounds ("try API 2:47-3:12am", "multiply by 1.1", "only Bob knows key") | Domain knowledge capture system; humans document quirks once, agents reuse |
| **Elastic infrastructure** | EC2/locked K8s can't self-heal; agents need API-driven scaling | SaaS or fully API-managed infra (not on-prem locked boxes) |
| **Quality data source** | Can't fix pipelines if upstream data is garbage (Pete overwritten sheet, no rows); agents can't hallucinate | Operational agents for fat-finger fixes; quality gates upstream |
| **Git for data** | Can't trust agents modifying production without staging test; no rollback | Zero-copy clones + time travel (Iceberg, Snowflake, MotherDuck) + branching |
| **Ecosystem API support** | Can't coordinate across tools (Fivetran, dbt, Salesforce) without vendor support | All ETL/ELT tools must expose APIs for staging→validation→switch workflow |
| **Agent sandboxes + new orchestrators** | Legacy orchestrators (Airflow, Dagster) + agents in same infra = security nightmare; prompt injection attacks | New orchestration layer with sandboxed agent execution (Cloudflare Workers model) |
| **Proxy + MCP standards** | Agents need controlled access to secrets/APIs without embedding credentials | Proxy service architecture; standardized MCP server definitions; role-based tool access |

## Core Primitives Needed

**Git for data**: The foundation. Enables agents to branch, test, validate, and safely switch production data.

**Elastic infrastructure**: Agents can't fix what they can't control. Every component needs self-service APIs.

**Ecosystem adoption**: If Fivetran can't be updated via agent-driven APIs, the chain breaks.

**Sandboxes + security**: Agents in production can be compromised; isolation is non-negotiable.

## The "Single Pane of Glass"

When all seven are in place:
- Agents have context (domain knowledge captured)
- Agents have control (elastic infra + APIs)
- Agents have safety (git for data + sandboxes)
- Agents have reach (all tools support agent workflows)

Result: autonomous operation without human intervention.

## Current Reality Check

**Databricks Genie ZeroOps** shows promise but is "wanting in many ways":
- Credential management unclear
- Locked to Unity Catalog (no external data context)
- Skills not obvious how defined
- No proper event-based orchestration
- Always-on (control limited)

## See Also

- [[Self-Healing Pipelines]] — 6-layer recovery pattern for autonomous recovery
- [[Agents in Data Engineering]] — maturity levels and tooling requirements
- [[Data Contracts]] — formalize what "healthy" means for agents
