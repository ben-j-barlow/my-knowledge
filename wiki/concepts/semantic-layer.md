---
tags: [data-n-ai, concept, etl, pipelines, agents]
sources: ["raw/data-n-ai/articles/How Anthropic enables self-service data analytics with Claude.md"]
updated: 2026-06-09
---

# Semantic Layer

A **semantic layer** is the set of compiled, governed **metric and dimension definitions** that sit between raw warehouse tables and the people (or agents) querying them. A consumer asks for "weekly active users" and the layer resolves it to one specific, governed entity — the joins, grain, and filters are baked in — so the same number is produced by every surface in the company (BI tool, notebook, Slack bot, agent).

It is the **highest-trust [source of truth](agentic-analytics.md#sources-of-truth)** in an [agentic analytics](agentic-analytics.md) stack and the primary defense against **concept ↔ entity ambiguity**: if a question maps cleanly to a defined metric, the agent calls a function and gets one number rather than choosing among forty plausible tables.

---

## Why it matters most for agents

Standard data engineering already valued consistent metric definitions. What raises the stakes with agents is that the consumer **can't validate correctness** — a non-expert asking via an agent has no way to know the agent picked the wrong "revenue." The semantic layer removes the choice: there is one governed metric, so there is nothing to get wrong.

At Anthropic, agents are **structurally required (by skill instruction) to try the semantic layer first.** Raw SQL via reference docs is an explicit *fallback*, used only after the semantic-layer path is shown not to cover the ask. A passive-monitoring signal they track in production is **the share of agent queries that resolve through the semantic layer** — a proxy for how often answers are governed vs improvised.

---

## Generate the docs, not the definitions

A tempting shortcut that **failed** at Anthropic: bootstrapping the semantic layer by having an LLM auto-generate metric definitions from raw tables and query logs. It produced "plausible-looking definitions that encoded the very ambiguities we were trying to eliminate," and was **net-negative on evals** versus a smaller, human-curated layer.

> The rule: **generate the *documentation* with Claude; a human owns the *definition*.**

This is a specific instance of the broader [structure-not-access](agentic-analytics.md#the-structure-not-access-principle) principle — the value is in the human-curated structure, not in volume of auto-generated material. A bigger machine-generated layer is worse than a smaller hand-owned one.

---

## "Don't bail early"

Agents reliably invent excuses to skip the semantic layer and drop to raw SQL — "I need custom date filtering," "this needs a join," "I need a cohort." Anthropic's warehouse skill pre-rebuts these in a **"Don't bail early"** block (custom dates → covered by time-dimension specs; joins → already encapsulated in the metric layer; etc.). The dominant wrong-answer mode they cite is hand-rolling `WHERE` clauses for population filters instead of using the layer's **named segments** (canonical population filters), so the skill instructs the agent to *always check segments*.

---

## Where it sits

- **Above:** raw and modeled warehouse tables ([data foundations](agentic-analytics.md)).
- **Beside, lower trust:** lineage / transformation graph, then the curated query corpus, then business context.
- **Consulted by:** [Claude Skills](claude-skills.md), which route the agent to the semantic layer first and to reference docs only on a miss.
- **Recorded in provenance:** the top tier of the [provenance footer](agentic-analytics.md#the-provenance-footer) (semantic layer › curated reference › raw table). An "offline eval should be ~100%" check at Anthropic also expects **every correct answer to be hitting the semantic layer.**

---

## Related Pages

- [Agentic Analytics](agentic-analytics.md) — the stack this anchors
- [Claude Skills](claude-skills.md) — route the agent here first
- [Context Engineering](context-engineering.md) — curate, don't auto-generate
- [Substrait](substrait.md) — a complementary lower-level query representation for LLMs
- [Source: How Anthropic Enables Self-Service Data Analytics with Claude](../sources/2026-06-03-anthropic-self-service-analytics.md)
