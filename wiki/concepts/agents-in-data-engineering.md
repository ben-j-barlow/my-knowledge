---
tags: [data-n-ai, concept, agents, etl, pipelines, prompt-engineering]
sources: [wiki/sources/motherduck-trustworthy-ai-pipelines.md, wiki/sources/spati-correctness-layer-agents.md]
updated: 2026-07-21
---

# Agents in Data Engineering

The use of AI agents to generate, validate, and maintain data pipelines. Data engineering is amenable to agentic workflows because:

1. **Bounded problem space**: SQL, schemas, DAGs, test coverage — well-defined, toolable
2. **Deterministic specification**: [[data-contracts]] and [[write-audit-publish]] gates make correctness checkable
3. **Clear success criteria**: "Query returns the right numbers" is verifiable (unlike open-ended code generation)

However, AI is non-deterministic and can't see data. Running pipelines ≠ correct pipelines. Successful agent-in-DE requires three maturity levels and specific discipline.

## Three Maturity Levels

### Level 1: Chat-Phase
Prompting Claude or ChatGPT with context. Good for:
- Exploratory queries on a dataset you'll review yourself
- Drafting queries you'll refactor by hand
- Learning what's possible

Limitations:
- High token cost
- Broad-but-shallow context understanding
- Probabilistic — same prompt yields different outputs
- No visibility into real data

### Level 2: Autonomous
Agent with CLI access (psql, DuckDB, S3), query verification tools, can inspect data and test locally. Good for:
- Backfill jobs with external test gates (RAG Loop pattern)
- Incremental pipeline development
- Small-to-medium datasets where the agent can verify

Limitations:
- Still probabilistic
- No deterministic equivalence checks
- Agent can sound confident about wrong answers

### Level 3: Dedicated Tooling
Purpose-built agents with domain-specific tools (dbt transpilation, SQL validation, [[correctness-layer]]), deterministic functions for parsing/validation/lineage. Best for:
- Production pipelines where wrong numbers are expensive
- Large enterprise projects with many downstream dependencies
- Changes that need blast-radius analysis

Examples: Altimate Code (deterministic harness + Rust core), dbt-native agents, SQL transpilers with native handlers.

## Three Critical Disciplines

### 1. Give the Agent Eyes on Data First
Connect the agent to the real database via MCPs *before* writing any transform.

Why: AI can't see data and metadata (schema, units, quality flags, null rates, duplicates). It guesses based on training data, silently encoding wrong assumptions.

How:
- MCPs for database (MotherDuck MCP, dbt commands, schema inspection)
- Agent queries the source, discovers schema + sample rows + null rates + duplicates
- Agent then encodes the real transform (unit conversion, QA filters, dedupe rules)

### 2. Write [[Data Contracts]], Not Prompts
A contract specifies the output, not the implementation steps.

Contract includes:
- Table name and schema
- Row semantics (grain, uniqueness, deduplication)
- Column transforms (units, ranges, null handling)
- KPI (what the data is meant to compute, including gotchas)
- Invariants and guardrails

Example: "Same-station mean TMAX per year; *must hold station set fixed* to avoid bias."

Why: Focuses the agent on the goal, not steps. Becomes testable (contract → assertions). Prevents the agent from optimizing the wrong thing.

### 3. Gate on [[Write-Audit-Publish]] (and Determinism Where It Matters)
Three-phase deployment:
- **Write**: Generate output in staging
- **Audit**: Assert output against contract (range checks, nulls, cardinality, uniqueness, lineage if deterministic core is available)
- **Publish**: Only if audit passes; fail loudly otherwise

For mission-critical transforms:
- Add a deterministic core for parse/validation/equivalence
- Lineage checks (what breaks if I rename this column?)
- Equivalence proofs (are these two queries semantically identical?)

### 4. Encode Discipline in Skills / AGENTS.md
Package the workflow (data inspection, contracting, WAP, testing) as a reusable skill file so every new pipeline inherits the discipline. MotherDuck agent skills repo has examples; patterns port to other stacks (dbt, Spark, etc.).

## Failure Modes

| Failure | Why | Prevention |
|---------|-----|-----------|
| Silent data corruption | Agent is non-deterministic, guesses on units/quality/grain | Data inspection (MCP), contracts + audit gates |
| Wrong join semantics | Grain changes silently (order w/ multiple line items counted once per item) | Contract defines grain; audit asserts cardinality; WAP gate |
| Duplicates leak through | Quality flags or dedup rules missed | Data inspection discovers Q_FLAG; contract encodes dedup rule; test case on duplicates |
| Stale assumptions | Pipeline works today, breaks when data changes | Contracts encode assumptions (units, ranges, rates); audit gates catch drift |

## Cross-Topic Connection

Data engineering agents feed the [[agentic-analytics]] and [[semantic-layer]] layers. Clean, trustworthy data pipelines are the foundation for agent-written analytics on top.

## Related Concepts

- [[data-contracts]] — the spec language for agent DE
- [[write-audit-publish]] — the safety gate for agent DE
- [[correctness-layer]] — the architecture for mission-critical DE
- [[claude-skills]] — the persistence mechanism
- [[agentic-analytics]] — the downstream use case
- [[local-vs-cloud-data]] — the tradeoff in where agent verification happens
