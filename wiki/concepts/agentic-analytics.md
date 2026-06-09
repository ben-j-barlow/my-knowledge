---
tags: [data-n-ai, concept, agents, etl, prompt-engineering]
sources: ["raw/data-n-ai/articles/How Anthropic enables self-service data analytics with Claude.md"]
updated: 2026-06-09
---

# Agentic Analytics

**Agentic analytics** is using an LLM agent to answer business analytics questions against a data warehouse on behalf of non-expert stakeholders — self-service analytics where the agent, not the analyst, maps a question to data and writes the SQL.

The defining insight (from Anthropic's internal system — see [source](../sources/2026-06-03-anthropic-self-service-analytics.md)): **accuracy is a context and verification problem, not a code-generation one.** The hard part is mapping a user's question to the correct, current entity in the data model; once that mapping is right, the SQL is trivial. This is the inverse of coding agents, where the solution space is open-ended and tests/docs are natural guardrails. Analytics usually has **one correct answer from one correct source, with no deterministic way to prove it.**

Anthropic reports **95% of business analytics queries automated at ~95% aggregate accuracy** (≈99% in mature domains) — but warns that naïvely pointing an agent at a warehouse "creates a false sense of precision" and cuts stakeholders off from the curated datasets and expertise that used to steer them.

---

## Why analytics is harder than coding for agents

| | Coding agents | Analytics agents |
|---|---|---|
| Solution space | Open-ended; rewards creativity | Single correct answer |
| Guardrails | Tests, types, compiler, docs | None deterministic |
| Failure | Often visible (test fails) | Often **silent** (plausible but wrong) |
| Bottleneck | Generation | **Context** — entity resolution & retrieval |

---

## The three failure modes

Almost all inaccurate responses trace to one of three:

1. **Concept ↔ entity ambiguity** — hundreds of plausible fields; the agent can't pick the one that answers the question. *"Active users": which actions count? include fraud? what lookback window?*
2. **Data staleness** — sources, definitions, and schemas change constantly; data assets and the agent's encoded knowledge rot and return subtly wrong answers.
3. **Retrieval failure** — the right, well-annotated information exists, but the search space is so large the agent never finds it.

The whole stack below is organized around attacking these three.

---

## The agentic analytics stack

Standard data engineering (dimensional modeling, shift-left testing, freshness/completeness checks) is *as important as ever*. What changes is the consumer: the agent acts for a non-expert who **cannot validate correctness**. Four layers, each mapped to a failure mode:

| Layer | Attacks | What it is |
|---|---|---|
| **Data foundations** | Ambiguity (+ staleness) | Canonical datasets, enforcement (tooling/CI/mandate), colocation, [metadata as a product](#metadata-as-a-product) |
| **[Sources of truth](#sources-of-truth)** | Ambiguity | Semantic layer › lineage › query corpus › business context |
| **[Claude Skills](claude-skills.md)** | Retrieval | Knowledge-router + process skill; LLM-targeted reference docs |
| **[Validation](#validation)** | All three | Offline evals, ablation, online adversarial review + provenance |

### Data foundations
Collapse a concept into a **single governed answer** before the agent ever searches: if *revenue* resolves to one dataset, not forty candidates, ambiguity disappears.
- **Canonical datasets** — few, heavily governed, clearly owned, consumption-ready; aggressively deprecate near-duplicates. Physical rollups derive *mechanically* from canonical models, never live beside them as alternatives.
- **Enforcement** via *tooling* (agent routed there first), *CI* (bypasses fail review), *mandate* (downstream builds on the governed layer or explains why not). Governance without enforcement decays back to multiple candidates.
- **Colocation** — modeling, semantic layer, reference docs, and dashboard definitions in one repo; CI flags a modeling change that breaks a downstream dashboard so the fix ships in the same PR.

#### Metadata as a product
Codebases work for agents because they're *legible* (READMEs, type signatures, docstrings). A warehouse can be too — column/table descriptions, metric definitions, grain docs, valid ranges, lineage, ownership, model tiering — but only if maintained with the rigor of the transforms. This is [Context Engineering](context-engineering.md) applied to a warehouse.

### Sources of truth
Reference surfaces the agent consults, in descending order of trust:
1. **Semantic layer** — compiled metric/dimension definitions; one question → one number, the same everywhere. Agent is *structurally required* to try it first. See [Semantic Layer](semantic-layer.md).
2. **Lineage / transformation graph** — table ranking by reference count tells the agent which governed model to aggregate, which are deprecated, which share grain.
3. **Query corpus** — historical SQL. *Low value as raw retrieval* (see null result); use it as raw material to curate into reference docs, not a source the agent reads directly.
4. **Business context** — the most-skipped, most-underrated layer. A company knowledge graph (docs, roadmaps, decision logs, org structure) lets the agent resolve ambient references ("the Q2 launch") and ask better clarifying questions. *An agent that doesn't understand the business answers what was asked, not what was meant.*

### Validation
- **Offline evals** — Q/A pairs (dashboard-based, Claude-generated + human-validated; plus long-tail generated from business context); harvest every stakeholder correction as a candidate eval. Anchor ground truth to a snapshot so it can't drift; store runs as telemetry (skill version, git SHA, model ID, per-assertion pass/fail) so "did that change help?" is a query; gate per-domain launches on a threshold.
- **Ablation** — vary one component, hold the eval set fixed, ~1 hr/run; ablate at PR granularity with the delta in the description; keep a short list of what didn't work.
- **Online** — adversarial-review sub-agent (+6% accuracy, +32% tokens, +72% latency); [provenance footer](#the-provenance-footer); passive monitoring (share resolving through the semantic layer; share of responses with correction language); active correction harvesting (scheduled agent drafts a reference-doc PR).

---

## The structure-not-access principle

The most consequential finding. Anthropic gave the agent grep access to **thousands** of prior SQL files and verified it read them — accuracy moved **<1 point.** The answer was present in the corpus ~80% of the time on questions it got wrong, but "answer present" didn't predict "now correct."

> The bottleneck is **structure** (mapping a question to the right entity), not **access** to prior work.

This is the same lesson as the [AGENTS.md](agents-md.md) / [Context Engineering](context-engineering.md) work and the ETH Zurich null result: dumping more material into context doesn't help; *curating it into a navigable structure* does. It redirected months of roadmap away from retrieval and toward canonical datasets + the semantic layer.

A corollary: **generate documentation with the LLM, but let a human own the definition.** Auto-generating the semantic layer was net-negative — it "encoded the very ambiguities we were trying to eliminate."

---

## The provenance footer

Because failures are silent, every response carries a footer: **source tier** (semantic layer › curated reference › raw table), **data freshness**, and **model owner**. It doesn't make the answer more correct; it lets the consumer calibrate trust. "raw table, freshness unknown" = verify before forwarding upstream. One of the few mitigations for the silent-failure mode (wrong but plausible, used without objection), alongside human sign-off on leadership-bound answers and a daily KPI sanity-check against the blessed dashboard.

---

## Minimum viable stack

> A handful of canonical datasets, a few dozen offline evals, and a thin [knowledge skill](claude-skills.md) capture most of the upside. Everything else is what you add once those exist.

Calibrate the rest by asking: how important is a correct answer *now* vs once models improve? how complex is the business? how technical is the audience? how much will you pay for accuracy (adversarial review is expensive)? what's your access-control posture (one agent or many scoped)?

---

## Related Pages

- [Semantic Layer](semantic-layer.md) — the highest-trust source of truth
- [Claude Skills](claude-skills.md) — the procedural layer; the 21%→95% lever
- [Context Engineering](context-engineering.md) — structure-not-access, metadata legibility, doc drift
- [AGENTS.md](agents-md.md) — the coding-agent analogue
- [Iterative Repair Loops](iterative-repair-loops.md) — adversarial review as a closed loop
- [Human-in-the-Loop](human-in-the-loop.md) — humans own definitions, curation, sign-off
- [Anthropic](../entities/anthropic.md)
- [Source: How Anthropic Enables Self-Service Data Analytics with Claude](../sources/2026-06-03-anthropic-self-service-analytics.md)
