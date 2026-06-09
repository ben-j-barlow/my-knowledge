---
tags: [data-n-ai, source, agents, etl, prompt-engineering]
sources: ["raw/data-n-ai/articles/How Anthropic enables self-service data analytics with Claude.md"]
updated: 2026-06-09
---

# Source: How Anthropic Enables Self-Service Data Analytics with Claude

**Authors:** Chen Chang, Clement Peng, Justin Leder, Johanne Jiao, Josh Cherry (Anthropic Data Science & Data Engineering team), with thanks to Michael Segner.
**Published:** ~2026-06-03 · claude.com/blog · surfaced via TLDR Data.

The definitive Anthropic write-up of the internal stack that automates **95% of business analytics queries at ~95% aggregate accuracy** (and ~99% in mature domains), freeing the data science team for causal modeling, forecasting, and ML. Distilled from meeting dozens of Anthropic's top Claude Code users.

---

## Central thesis: data is not software

LLM generative ability is a double-edged sword — the same mechanism that solves novel problems hallucinates. Comparing analytics agents to coding agents exposes why analytics is harder:

- **Coding** is an open-ended solution space that *rewards* creativity; docs and tests are natural guardrails against hallucination.
- **Analytics** usually has a **single correct answer from a single correct source, with no deterministic way to prove correctness.**

So accuracy is **a context and verification problem, not a code-generation one.** The hard part is mapping a user's question to the right, up-to-date entity in the data model and knowing how to work with it. *Once that mapping is right, the SQL is trivial.* Pointing Claude at a warehouse and letting it execute creates "a false sense of precision" and separates stakeholders from the documentation and expertise that used to steer them to curated datasets.

---

## The three failure modes (≈all inaccuracy)

1. **Concept ↔ entity ambiguity** — hundreds of viable options (out of millions of fields); agent can't pick the field that answers the question. *"Active users": which actions count? include fraud? what lookback?*
2. **Data staleness** — sources, definitions, schemas change constantly; assets and agent knowledge rot and start returning subtly wrong answers.
3. **Retrieval failure** — the right, properly-annotated info exists, but the search space is so vast the agent never finds it.

---

## The agentic analytics stack (each layer attacks a failure mode)

> Standard data engineering — dimensional modeling, shift-left testing, freshness/completeness checks — is *as important as ever.* What changes: the end user of your data model is now an **agent acting on behalf of a non-expert**, who cannot validate correctness because they don't know enough to.

### 1. Data foundations → ambiguity (+ first staleness defense)
The warehouse itself: models, transforms, tests, tables, and metadata. If *revenue* resolves to one governed dataset instead of forty candidates, the problem disappears before the agent searches.
- **Create canonical datasets** — few, heavily governed, single-source-of-truth, clearly owned, consumption-ready; aggressively deprecate near-duplicates. Physical rollups derive *mechanically* from canonical models, never live alongside as alternatives.
- **Enforce standards** via *tooling* (agent structurally routed to them first), *CI* (bypasses fail review), and *mandate* (downstream builds on the governed layer or explains why not). Governance without enforcement decays back to multiple-candidates.
- **Colocate artifacts** — nearly all data code (modeling, semantic layer, reference docs, dashboard definitions) in one repo, with CI protecting cross-layer integrity: a modeling change that breaks a dashboard is flagged and fixed in the same PR.
- **Treat metadata as a first-class product** — column/table descriptions, metric definitions, grain docs, value ranges, lineage, ownership, model tiering maintained with the rigor of the transforms. Codebases work for agents because they're *legible*; warehouses can be too.

### 2. Sources of truth → concept↔entity ambiguity (descending order of trust)
- **Semantic layer** — compiled metric/dimension definitions. Maps a question to one number, the same every surface produces. Agents are *structurally required by skill instruction* to try it first.
- **Lineage / transformation graph** — when the semantic layer doesn't cover the ask, lineage + table ranking (by reference count) tell the agent which upstream model to aggregate, which are deprecated, which share grain. Backbone of freshness/provenance signals.
- **Query corpus** — historical SQL. *Counterintuitively low value as raw retrieval* (see null result). Use as **raw material to curate** into per-domain reference docs and reusable patterns — not a source the agent reads directly.
- **Business context** — the layer most teams skip and underrate longest. An agent that doesn't understand the business answers what was asked, not what was meant. Anthropic pipes in a **company knowledge graph** (indexed docs, roadmaps, decision logs, org structure) so the agent resolves ambient references ("the Q2 launch") and asks better clarifying questions.

Common failure across all four: **poor or stale documentation.** Claude is excellent at *closing* the gap (drafting descriptions, proposing metric docs, flagging undocumented models in CI); humans own **curation and definition**.

### 3. Skills → retrieval failure
Skills are the agent's **procedural** knowledge (which sources, in what order; what a finished analysis looks like) vs sources of truth as **declarative** knowledge. A Claude Code skill is a folder of markdown the agent reads on demand.

> **Without skills, accuracy didn't exceed 21%. With skills, consistently >95%, ~99% in some domains.**

- **Pairwise skills.** A ***knowledge*** skill is a thin top-level router ("try the semantic layer first; else here are ~30 reference files for this domain") — narrowing a million-field warehouse to a few dozen curated files before any query is written. An ***unbook*** skill encodes the senior-analyst process (clarify → find sources via knowledge skill → query → loop through adversarial review sub-agents) and bundles ~a dozen reusable patterns (retention curves, rate decomposition, funnel analysis).
- **Reference docs written for LLM retrieval** — describe tables (grain, scope, exclusions), gotcha mechanics ("exclude known free-email domains but keep custom ones like anthropic.com"), and explicit routing triggers ("IF about experiment lift… DO NOT use for raw event counts"). No prescriptive recipes that go stale.
- **Skill maintenance is first-class.** Offline accuracy **drifted 95% → 65% over a month** untreated. Fix: colocate skill markdown with transformation models so the PR changing a model updates the doc; a **code-review hook flags any reporting-model change that doesn't touch a skill file**. ~90% of data-model PRs now include a skill change. Prune scaffolding as models improve.
- **Consistent experience across surfaces** — the same skill gives the same answer in Slack, IDE, dashboard tool, and standalone sessions. One canonical source (data repo); on merge it syncs to a plugin marketplace (IDE), cloud-storage blobs (hosted apps), and is served as resources over MCP. Designed for portability (no hardcoded paths / surface-specific namespaces).

### 4. Validation → catches what still leaks
**Offline evals** (Q/A pairs; like offline ML testing — reveal gaps, not online performance):
- **Dashboard-based evals** (Claude-generated, human-validated, common questions) + **long-tail evals** (feed Claude business context, have it generate plausible questions) + continuous harvesting of every stakeholder correction in a thread.
- **Anchor ground truth so it can't drift** — pin to a snapshot date / stable fact table, or grade the *query* not the *number*; wire into CI.
- **Store results like telemetry** — every run to a warehouse table (skill version, git SHA, model ID, per-assertion pass/fail, tokens, wall-clock) → "did that change help?" is a query; catches slow regressions.
- **Gate launches per domain** — owner can't announce to stakeholders until their eval slice clears a threshold (started ~90%).
- **Right number of evals** — scales with business + data-model complexity; diminishing returns past a few dozen per topic; the ceiling drops each model generation.
- **Offline accuracy should be ~100%**, with every correct answer hitting the semantic layer.

**Ablation methodology** — vary one component, hold the eval set fixed, compare pass rates; ~1 hour per run, "replaces a lot of arguments."
- **Design for null results** (see below).
- **Ablate at PR granularity** — before/after on the relevant slice, delta in the PR description; keeps "I improved the docs" honest and catches well-intentioned regressions.
- **Keep a short list of what didn't work** — e.g. stacking doc-refinement rounds past ~3 (docs got longer, not better); swapping the adversarial reviewer to a cheaper model (lost most accuracy wins for no real speedup).

**Online validation:**
- **Adversarial review** sub-agent challenging all assumptions: **+6% accuracy, +32% tokens, +72% latency.**
- **Provenance footer** on every response — source tier (semantic layer › curated reference › raw table), data freshness, model owner. Doesn't improve correctness; helps the consumer judge trust. "raw table, freshness unknown" = verify before forwarding. One of few mitigations for silent failures.
- **Data quality checks** — right field used correctly can still be wrong if the data is wrong.
- **Passive monitoring** — share of queries resolving through the semantic layer; share of responses with correction language ("wrong table," "missing the fraud filter"). Weekly dashboard alongside offline pass rate.
- **Active correction harvesting** — scheduled agent scans stakeholder channels every few hours for correction language, drafts a one-line reference-doc fix, opens a PR tagged to the domain owner (fix path deliberately boring: edit markdown → merge → auto-sync). Same corrections feed the offline eval set.

The **silent failure** (wrong but plausible, used without objection) is what none of this fully catches; mitigations are the provenance footer, human sign-off on leadership-bound answers, and a daily standing eval of each domain's top KPIs against the blessed dashboard. No robust solution yet.

---

## Standout empirical findings

- **The null-result ablation (redirected months of roadmap):** gave the agent grep access to thousands of dashboard/transformation/notebook SQL files, *verified in transcripts it read them before every answer.* Accuracy moved **<1 point.** For the questions it got wrong, the answer was present in the corpus ~80% of the time, but "answer present" did **not** predict "now gets it right" — the flip rate was flat. Conclusion: **the bottleneck is structure (mapping a question to the right entity), not access to prior work.**
- **Auto-generating the semantic layer was net-negative.** Having an LLM auto-generate metric definitions from raw tables + query logs produced "plausible-looking definitions that encoded the very ambiguities we were trying to eliminate." Rule: **generate the *documentation* with Claude; a human owns the *definition*.**
- **Raw query-corpus retrieval moved accuracy <1 point** — unstructured retrieval couldn't map a new question to the right precedent.

---

## Getting started (the team's own minimum)

> "A handful of canonical datasets, a few dozen offline evals, and a thin knowledge skill will capture most of the upside; everything else in this post is what we added once those were built."

Principles to align on first (not every practice fits every team):
- **Correct answer today vs in the future?** Models improve fast; building heavy infra to patch current shortfalls can become moot. Knowing where models fall short and waiting has less overhead — if risk tolerance allows.
- **How will business complexity change?** Much of this is overkill for little data / few consumers / a simple model.
- **How technical is the audience?** Building for data scientists who can spot wrong answers tolerates more error than building for non-experts.
- **How much will you pay for accuracy?** Adversarial validation buys accuracy at real cost/latency.
- **Access-control / privacy posture?** More context = more performant, but broad access cuts against governance — determines one agent vs many scoped ones.

---

## Appendix: skill skeletons

The article ships two anonymized templates worth keeping:
1. **Warehouse skill skeleton** — frontmatter with an IF/THEN/DO-NOT trigger; "Semantic Layer (REQUIRED first step)" with a *"Don't bail early"* list of pre-rebutted excuses agents use to skip it; PART 1 MUST KNOW (red flags, out-of-scope escalation, entity disambiguation, business terminology, data-integrity NEVER/ALWAYS), PART 2 HOW TO DO (mandatory adversarial SQL review sub-agent, provenance footer), PART 3 DATA REFERENCES (one `references/[domain].md` entry per domain, field-naming gotchas).
2. **Reference-doc skeleton** — Quick Reference (business context, entity grain, standard hygiene filter), Dimensions, Key Tables (grain/scope/usage), Gotchas, Best Practices / Common Query Patterns, Cross-References.

Both are reproduced verbatim in the raw source.

---

## Related Pages

- [Agentic Analytics](../concepts/agentic-analytics.md) — the stack and three failure modes
- [Semantic Layer](../concepts/semantic-layer.md)
- [Claude Skills](../concepts/claude-skills.md)
- [Anthropic](../entities/anthropic.md)
- [Context Engineering](../concepts/context-engineering.md) — metadata-as-product, doc drift, generate-docs-not-definitions
- [AGENTS.md](../concepts/agents-md.md) — the coding-agent cousin of skills
- [Iterative Repair Loops](../concepts/iterative-repair-loops.md) — adversarial review sub-agents
- [Human-in-the-Loop](../concepts/human-in-the-loop.md) — humans own definitions, curation, sign-off
