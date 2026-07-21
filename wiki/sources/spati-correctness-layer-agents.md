---
tags: [data-n-ai, source, agents, etl, pipelines, testing]
sources: [raw/data-n-ai/articles/Where AI Agents Belong in Data Engineering The Correctness Layer.md]
updated: 2026-07-21
---

# Source: Where AI Agents Belong in Data Engineering — The Correctness Layer

**Author:** Simon Späti  
**Published:** 2026-07-08  
**URL:** https://www.ssp.sh/blog/where-agents-belong-in-de/

## Core Claim

AI agents in data engineering have three maturity levels (chat-phase, autonomous, dedicated tooling), and the best outcomes come from **deterministic correctness layers** underneath probabilistic LLMs. The deterministic core (parsing, validation, equivalence checks, lineage) ensures outputs are provably correct rather than just confidently-wrong.

## Key Points

### Three Levels of AI Agents in DE

1. **Chat-phase:** Prompting Claude or ChatGPT with context, high token cost, broad-but-shallow understanding
2. **Autonomous:** Agent with CLI access (psql, DuckDB, S3), can verify queries and data; higher-quality output, still probabilistic
3. **Dedicated tooling:** Purpose-built agents with domain-specific tools (dbt, SQL transpilation, query equivalence checks); deterministic where it matters

### Blast Radius Analysis

Before renaming a column or adding a join, know the downstream impact. The example: `fct_orders` join logic changes grain — orders with multiple line items get counted once per item, revenue inflates silently. Altimate Code maps full impact automatically: what breaks, what's safe, what needs sign-off.

### The Correctness Layer (Altimate Code Architecture)

Three-layer stack:

1. **Probabilistic agent** (LLM): reads intent, drafts SQL, summarizes, recovers from errors
2. **Deterministic harness** (TypeScript): intercepts tool calls, routes to native handlers
3. **Deterministic core** (Rust `altimate-core` via napi-rs): AST parsing, validation, transpilation, query equivalence, column lineage, schema diffing — all sub-millisecond, all deterministic

Like a compiler proving a program type-checks rather than guessing, the agent calls a function that proves two queries are equivalent against the parsed AST and schema.

### Engineering Discipline for Working with AI

To safely use agents in large projects or orgs, need:

1. **Clear project structure** — deterministic workflows (e.g., `uv init` always the same) use fewer tokens and improve alignment
2. **Clear instructions** — agentic skills, CLIs, API docs; the work upfront is brainstorming and documenting, not letting the agent run down the wrong path
3. **Modular setup** — agents can't break the whole project if they make one change; avoid dependency hell
4. **Declarative approach** — configuration files describing the *what*, not the *how*, so you can collaborate with agents, version, revert, decouple business logic from implementation

### Token Economics

Cost-per-token is the wrong optimization target; the meter moves with each model release (same prompt, 1.4X tokens between Opus 4.6→4.7). **Cost-per-task** is the right metric. Deterministic functions (parsing, validation) bypass the model entirely, reducing token exposure and volatility.

### Use Cases in DE Lifecycle

- Start a new project from scratch
- Extend an existing warehouse (add pipelines)
- Maintain current setup (verify it still works)
- Migration (one database/tool to another)
- Finding blind spots (wrong join keys, missing data in nightly loads, duplicates)

## Concrete Example: Renaming Column from Cents to Dollars

Prompt: change unit from cents to dollars in an ecommerce repo (staging → intermediate → marts layers). Agent autonomously:
1. Recognized dbt and invoked `dbt-analyze`
2. Generated a full blast-radius report
3. Showed what's safe, what's not, fixed order to address breaking changes
4. No mention of blast analysis or dbt-analyze in the original prompt — it did it on its own

## Notable Quotes

> "Bare agent use might be cheap, but only until they're wrong, and then the cost is unbounded."

> "The key is to get use out of AI, not to get more work."

> "Correctness over confidence. When output touches production, a dashboard, a nightly job, a number someone makes a decision on, you want the deterministic core underneath it, not just a model that sounds confident."

## Tags / Themes

- **Correctness layer** as the architecture that bridges probabilistic (LLM) and deterministic (compiler-like) reasoning
- **Blast radius** analysis as a practical application of determinism — know impact before change
- **Deterministic validation** replacing confidence guessing
- **Project structure and discipline** matter more than model selection
- **Cost-per-task**, not cost-per-token, is the right optimization

## Connected Concepts

- [[correctness-layer]]
- [[agents-in-data-engineering]]
- [[data-contracts]]
- [[agents-md]]
