---
tags: [data-n-ai, concept, agents, pipelines, operations]
sources: [wiki/sources/self-healing-data-architecture-barriers.md]
updated: 2026-07-23
---

# Self-Healing Architecture Requirements

Autonomous data pipelines require seven foundational capabilities. Without all seven, agents can't self-recover; they become expensive fix-generators instead.

## The Seven Pillars

**1. Context & Failure Recall**
- Agents need domain knowledge (workarounds, quirks, why things work)
- Can't be purely inferred from code/logs
- Example: "API fails without retry between 2:47-3:12am" only exists in someone's head
- Solution: Structured knowledge capture (evals, documentation, playbooks) that agents can retrieve

**2. Elastic Infrastructure**
- Infrastructure must have APIs agents can call (not just horizontal scaling)
- On-prem locked K8s clusters are not elastic; EC2 alone is not elastic
- SaaS is inherently agent-friendly (APIs exist, no manual intervention)
- Solution: Adopt SaaS or build comprehensive IaC/API layer

**3. Quality Data Source**
- Agents can't fix pipelines corrupted by upstream human error (missing source data, bad values)
- Can't hallucinate data to fill gaps
- Example: Finance person overwrites Google Sheet with garbage → pipeline fails → agent has nothing to fix
- Solution: Operational agents for catching fat-finger errors + quality gates at source

**4. Git for Data**
- Agents can't be trusted to modify production without staging environment
- Need zero-copy clones (to avoid cost explosion)
- Need time travel/rollback (to revert bad agent fixes)
- Example: Agent modifies Salesforce staging → validates against rest of pipeline → switches in safely
- Solution: Iceberg (time travel + rollback + branching), Snowflake (zero-copy clones), MotherDuck

**5. Ecosystem API Support**
- All tools in the pipeline must expose agent-callable APIs
- Can't coordinate Fivetran→dbt→Salesforce fix if tools don't support it
- Example: Silent schema change in Fivetran → agent needs to update job, test staging, switch data
- Solution: Pressure on vendors (Fivetran, dbt, Salesforce) to support agentic workflows

**6. Agent Sandboxes + New Orchestrators**
- Legacy orchestrators (Airflow, Dagster) run agents in same infra as data jobs = security disaster
- Agents can be prompt-injected; need isolated execution environments
- Agents need DAG access, credentials, monitoring—but safely
- Solution: New orchestration layer (Cloudflare Workers model) with sandboxed agent runtime

**7. Proxy + MCP Standards**
- Agents need controlled access to secrets/APIs without embedding credentials in agent context
- Proxy service enforces authentication, rate limits, audit
- MCP servers define which tools/endpoints agents can reach
- Solution: Standardized proxy architecture + MCP server definitions

## What Breaks Without Each Pillar

| Missing Pillar | Failure Mode |
|---|---|
| Context | Agent can't distinguish transient from real failures; fixes wrong things |
| Elastic infra | Agent can't recover infrastructure issues; pipeline stays down |
| Quality data | Agent fixes logic but data is still garbage; results wrong |
| Git for data | Agent modifies production without test; breaks data for entire org |
| Ecosystem APIs | Agent can't coordinate multi-tool fixes; stalled mid-recovery |
| Sandboxes | Prompt injection compromises all credentials; security breach |
| Proxy/MCP | Agent has all credentials in context; sprawl, audit trail impossible |

## The "Single Pane of Glass"

When all seven are in place, agents operate autonomously:
- Detect failures (via incident detection, evals)
- Understand root cause (via context layer)
- Test fix (via git-for-data staging)
- Deploy safely (via proxy + limited tool access)
- Rollback if needed (via time travel)

Result: human operators only intervene for non-technical decisions.

## Reality Check

**Databricks Genie ZeroOps** (2026) shows partial implementation:
- ✓ Has context (Unity Catalog metadata)
- ✗ Locked to Unity only (missing external data)
- ✗ Always-on (control/security concerns)
- ✗ Skills definition unclear
- ✗ No proper event orchestration

## See Also

- [[Self-Healing Pipelines]] — 6-layer autonomous recovery pattern
- [[Agents in Data Engineering]] — maturity levels and operational disciplines
- [[Write-Audit-Publish]] — safety gate for agent-written data
- [[Data Contracts]] — formalize what "healthy" means
