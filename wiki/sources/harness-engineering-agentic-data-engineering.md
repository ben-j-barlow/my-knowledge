---
tags: [data-n-ai, source, agents, etl, pipelines, harness-engineering]
sources: ["raw/data-n-ai/articles/2026-09-27-harness-engineering-agentic-data-engineering.md"]
updated: 2026-10-02
---

# Source: Rebuilding Data Engineering with Harness Engineering

Nie Lifeng (HackerNoon, 2026-09-27). Opinion/thought-leadership piece (AI-assisted per HackerNoon's label); ingested from a paraphrased summary (the original article text and diagrams were not directly accessible — summarized via Claude).

## Thesis

The Modern Data Stack was built for humans, who silently fill gaps (business terms, ambiguity, accountability) that agents can't fill. As generative AI commoditizes SQL/code/DAG production, the scarce resources become context, verification, governance, and accountability. The most dangerous agent failure isn't a crash — it's a wrong result that executes successfully in production (Wrong Data → Wrong Decision → Wrong Action). The missing piece between agent intelligence and safe production use is an engineering system the article calls the **[Harness](../concepts/harness-engineering.md)**.

## Key Contributions

**Seven sign-off gates** — a production-readiness checklist (intent verified, context complete, plan reviewable, execution controlled, results validated, failures recoverable, actions auditable) framed as "when is it safe to delegate," not as product features. The article's own case study flags gates 5 (validate results) and 7 (audit) as the ones most real pipelines skip.

**Five-layer Agentic Data Stack** (L5 Business Intent → L4 Orchestration Control Plane → L3 Semantic & Knowledge → L2 Data Engineering Harness → L1 Deterministic Execution/Runtime), with the rule that agents never call underlying tools directly — everything routes through the Harness, gated by L3 context and L4 policy.

**Skill vs Prompt vs Tool API** — a three-way distinction: a Prompt shapes how an agent responds, a Tool API exposes a raw operation and leaves failure handling to the caller, a Skill is the structured unit (Input, Context, Policy, Execution, Validation, Rollback, Output) that determines whether an action can execute *safely*.

**Risk-tiered human-in-the-loop** — Low (auto-execute) / Medium (execute + notify) / High (human approval) / Critical (block or dual approval), explicitly reframing HITL as protecting risk boundaries rather than reviewing every step.

**Case studies** — Apache SeaTunnel (data integration as a Skill) and Apache DolphinScheduler (orchestration under policy) as concrete open-source implementations of the L1/L2 Harness pattern, each exposing a discovery → generate → execute → observe → repair loop.

## How This Extends the Existing Wiki

This source gives a name and a structural frame — the **Harness** and the **5-layer stack** — to a pattern this wiki already had scattered across several pages:

- [Correctness Layer](../concepts/correctness-layer.md)'s probabilistic-agent / deterministic-core split is this article's L1 (Runtime) vs the agent, with the Harness itself as the L2 gateway in between.
- [Data Contracts](../concepts/data-contracts.md) and [Write-Audit-Publish](../concepts/write-audit-publish.md) are concrete implementations of sign-off gates 2 (context) and 5 (validate results).
- [Claude Skills](../concepts/claude-skills.md) is a worked example of "Skill vs Prompt" — Anthropic's skill pairs (router + process) are Harness Skills in this article's sense, not prompts.
- [Semantic Layer](../concepts/semantic-layer.md) is a concrete instance of L3 (Semantic & Knowledge).
- [Agents in Data Engineering](../concepts/agents-in-data-engineering.md)'s three maturity levels map roughly onto this article's three adoption stages (Collaborative Assistance → Controlled Execution → Governed Autonomy).

The genuinely new material: the **seven sign-off gates** as an explicit checklist, the **risk-tiered HITL table**, and the **Skill vs Prompt vs Tool API** three-way distinction (the wiki previously only had Skill vs AGENTS.md). See [Harness Engineering](../concepts/harness-engineering.md) for the consolidated concept page.

## Caveats

- AI-assisted opinion piece, not a primary engineering account (contrast with the MotherDuck/Späti/Anthropic sources, which describe real production systems in detail). Treat the seven gates and five layers as a useful organizing framework, not a vetted architecture.
- Diagrams in the original were not visible during summarization; all content here is from the paraphrased text.
- The SeaTunnel/DolphinScheduler "Skill set" function signatures (`DiscoverSource()`, etc.) are illustrative, not quoted API.

## Source

[raw/data-n-ai/articles/2026-09-27-harness-engineering-agentic-data-engineering.md](../../raw/data-n-ai/articles/2026-09-27-harness-engineering-agentic-data-engineering.md)
