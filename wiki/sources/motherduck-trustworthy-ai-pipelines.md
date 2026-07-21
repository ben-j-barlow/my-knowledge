---
tags: [data-n-ai, source, pipelines, agents, prompt-engineering, testing]
sources: [raw/data-n-ai/articles/Code that runs is not code that's correct 4 ways to trust an AI-written data pipeline.md]
updated: 2026-07-21
---

# Source: Code That Runs Is Not Code That's Correct — 4 Ways to Trust an AI-Written Data Pipeline

**Author:** MotherDuck  
**Published:** 2026-07-15  
**URL:** https://motherduck.com/blog/robust-data-pipelines-with-ai/

## Core Claim

Running code and correct code are different things. AI is non-deterministic (same prompt yields different implementations) and can't see data/metadata (schema, units, quality flags), so it guesses—silently. Four disciplines turn a lucky one-shot prompt into a trustworthy production pipeline.

## Key Points

### 1. Foundations Still Matter
Old data engineering discipline didn't disappear; it's more important now that AI generates code at scale. The naive NOAA example hardcodes the year, uses CREATE OR REPLACE (expensive), and misses three problems: unit conversion (tenths-of-degree), quality flags (Q_FLAG), and reproducibility. Solutions: parameterize the year, use incremental loads, **inspect data first**.

### 2. Give AI Eyes on Data & Metadata
Connect the agent to the real database via MCPs. MotherDuck MCP lets the agent query the S3 data and discover: values are in tenths of a degree, data partitioned by year/element, presence of Q_FLAG. Once the agent has seen the data, the transform becomes sophisticated — it encodes the contract (tenths-to-Celsius, QA filters, dedupe keys) and the tests mock real risk cases. Local unit tests run sub-second on DuckDB; no network required.

### 3. Make the Goal a Contract, Not a Prompt
Write the contract as a docstring: what table exists, what one row means, every term defined exactly. The KPI (same-station mean TMAX per year holding station set fixed) is the real check — average across all US stations drifts down (cooling) because the network grew into colder places; hold the station set fixed and it flips to warming. The contract becomes an assertion (Write-Audit-Publish pattern): build → check against contract → publish only if it passes. Range checks catch unit bugs automatically (if you forget `/10`, values exceed any real air temperature).

### 4. Package It So It Happens Every Time
Encode all four disciplines in a markdown skill file: parameters, idempotency, data inspection, contracts, local tests, Write-Audit-Publish. Every new pipeline inherits the discipline. MotherDuck publishes agent skills for DuckDB/MotherDuck; patterns port to other stacks.

## Concrete Example

NOAA GHCN daily max temperatures → MotherDuck table. The final prompt weaves all four threads (inspection, contract, parameters, idempotency, WAP) into one dense spec. Agent runs it, reads `get_flight_logs`, fixes, retries until the contract passes. Bonus: agent builds a Dive (dashboard in pure JavaScript) visualizing the trend.

## Notable Quotes

> "A flight that errors is far better than one that silently loads with wrong numbers. Always fail loudly."

> "Same data, opposite conclusions." (Cooling vs warming depending on whether you hold the station set fixed — illustrates how contracts enforce the right KPI.)

## Tags / Themes

- **Data contracts** as executable specs, not documentation
- **Write-Audit-Publish** as the canonical safe-deployment pattern
- **Local vs. cloud data** — unit tests on local DuckDB, no network dependency for correctness checks
- **Agents need eyes** — MCP access to schema/sample data outweighs architectural design docs
- **Skills/AGENTS.md** as the persistence mechanism for discipline

## Connected Concepts

- [[data-contracts]]
- [[write-audit-publish]]
- [[local-vs-cloud-data]]
- [[agents-in-data-engineering]]
- [[claude-skills]]
