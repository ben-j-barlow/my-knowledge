---
tags: [data-n-ai, concept, agents, etl, pipelines]
sources: [wiki/sources/spati-correctness-layer-agents.md]
updated: 2026-07-21
---

# Correctness Layer

An architectural pattern separating **probabilistic reasoning** (LLM agent doing creative work: reading intent, drafting solutions, recovering from errors) from **deterministic validation** (compiler-like checks: parsing, validation, equivalence checking, lineage tracking).

The deterministic layer ensures that factual questions (Does this column exist? Are these two queries equivalent? What is the full lineage?) are answered by proof rather than model confidence. The agent never *decides* — it calls a function that proves it against the parsed AST and schema.

## Architecture (Altimate Code Example)

Three layers:

```
┌────────────────────────────────────────────┐
│  Probabilistic Agent (LLM)                 │
│  Reads intent, drafts SQL, summarizes      │
└────────────┬─────────────────────────────┘
             │
┌────────────▼─────────────────────────────┐
│  Deterministic Harness (TypeScript)       │
│  Intercepts tool calls, routes to handlers│
└────────────┬─────────────────────────────┘
             │
┌────────────▼─────────────────────────────┐
│  Deterministic Core (Rust)                │
│  AST parsing, validation, transpilation   │
│  Equivalence checking, column lineage     │
│  (all sub-millisecond, all deterministic) │
└─────────────────────────────────────────┘
```

## What the Deterministic Core Does

Pure functions over ASTs and schemas (wired via napi-rs bindings):

- **Parsing**: Convert SQL to abstract syntax tree
- **Validation**: Column exists? Types match? Joins valid?
- **Transpilation**: SQL dialect A → dialect B with guaranteed semantics
- **Query equivalence**: Prove two queries are semantically identical
- **Column lineage**: Trace a column back to its source
- **Schema diffing**: What changed between two schemas?

Each operation returns the same answer on the same input, every time. No guessing, no confidence intervals.

## Why It Matters for Data Engineering

Data engineering has one correct answer per question — no probabilistic acceptable range like generative tasks. A wrong join order silently loads incorrect metrics. An off-by-one in a deduplication key silently inflates counts. The agent sounds confident, the query runs green, and the dashboard shows wrong numbers.

The correctness layer removes guessing from the critical path:
- **Equivalence checks**: Can't accidentally change query semantics during optimization
- **Lineage tracking**: Know exactly what downstream depends on a column before renaming it ([[blast-radius]] analysis)
- **Validation**: Catch impossible joins, type mismatches, missing columns at author time, not at query time

## Token Economics

Cost-per-token is the wrong optimization (the meter itself moves with model releases). **Cost-per-task** is right. Deterministic functions bypass the model entirely for factual checks — parsing, validation, equivalence never touch the LLM. This reduces token exposure and volatility, and often reduces overall cost despite the added infrastructure.

Example: transpiling SQL from Postgres to Snowflake is better done via an AST (sub-millisecond, guaranteed correct) than via an LLM prompt (seconds, probabilistic, high token cost).

## Distinction from Confidence-Based Review

A wrong query that the model is confident about:
- No error message (the query runs)
- No way for a human to verify without deep inspection
- Silent corruption that propagates downstream

A wrong query caught by the correctness layer:
- Explicit failure (equivalence check fails, validation rejects it)
- Reason is deterministic (missing column in schema, type mismatch)
- Agent sees the error, fixes it, retries

The second is "more wrong in a good way" — failure is loud and actionable.

## Implementation Challenges

Building a deterministic core is expensive (Rust infrastructure, AST handling, bindings to multiple SQL dialects). It scales well (amortized cost per query falls as volume rises) but isn't suitable for every task. The tradeoff: agent freedom (you can prompt-engineer anything) vs. correctness (only deterministic facts).

Data engineering tooling (dbt, SQL linting, query optimization) is a natural place to build correctness layers because the problem space is bounded (SQL, schemas, DAGs) and the cost of being wrong is high (silent data corruption).

## Related Concepts

- [[data-contracts]] — the spec being validated by the correctness layer
- [[write-audit-publish]] — the contract assertions are part of the correctness gate
- [[agents-in-data-engineering]] — the pattern for safely deploying agent-written DE code
- [[blast-radius]] (not yet in wiki) — practical application: lineage proves impact before change
