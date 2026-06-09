---
tags: [data-n-ai, concept, agents, prompt-engineering]
sources: ["raw/data-n-ai/articles/How Anthropic enables self-service data analytics with Claude.md"]
updated: 2026-06-09
---

# Claude Skills

A **skill** in Claude Code is a folder of markdown the agent reads **on demand**. Where [sources of truth](semantic-layer.md) are an agent's *declarative* knowledge (what a metric *means*), a skill is its **procedural** knowledge: which sources to consult in what order, how to navigate ambiguous data, and what a finished piece of work looks like.

Skills are the single biggest accuracy lever in Anthropic's [agentic analytics](agentic-analytics.md) stack — they attack the **retrieval-failure** mode by narrowing a million-field warehouse to a few dozen curated files *before* a query is ever written.

> **Without skills, Claude's analytics accuracy didn't exceed 21%. With skills: consistently >95% in aggregate, ~99% in some domains.**

A skill's frontmatter carries an explicit invocation trigger — `IF the user asks to query the warehouse for [domains] — THEN invoke; DO NOT invoke for [adjacent tasks]` — so the agent loads the right procedural knowledge for the task and nothing else.

---

## The pairwise pattern

Anthropic builds most skills as a **pair**:

- **Knowledge skill** — a thin top-level **router**. "Try the semantic layer first; if there's no coverage, here are ~30 reference files for this domain describing the relevant tables, columns, joins, and gotchas." This router *is* the answer to retrieval failure: it collapses the search space to a curated shortlist instead of letting the agent grep a vast warehouse.
- **Unbook skill** — encodes the **process a senior analyst follows**: clarify the question → find sources (via the knowledge skill) → run the query → loop the result through adversarial-review sub-agents. It bundles ~a dozen reusable analysis patterns (retention curves, rate decomposition, funnel analysis) so common requests aren't reinvented.

---

## Reference docs written for LLM retrieval

The knowledge skill points at reference docs whose job is to be *found and correctly used by an LLM*, not read front-to-back by a human. They describe:
- **Tables** — grain, scope, exclusions.
- **Gotcha mechanics** — "exclude known free-email domains, but keep custom ones like anthropic.com."
- **Explicit routing triggers** — "IF the question is about experiment lift… DO NOT use for raw event counts."

…and deliberately avoid prescriptive recipes that go stale. The article's reference-doc skeleton: Quick Reference (business context, entity grain, standard hygiene filter) → Dimensions → Key Tables (grain/scope/usage) → Gotchas → Best Practices / Common Query Patterns → Cross-References.

The warehouse-skill skeleton layers the same idea: a "Semantic Layer (REQUIRED first step)" section with a *["Don't bail early"](semantic-layer.md#dont-bail-early)* list, a MUST-KNOW part (red flags, out-of-scope escalation, entity disambiguation, data-integrity NEVER/ALWAYS), a HOW-TO part (mandatory adversarial SQL-review sub-agent, provenance footer), and a DATA-REFERENCES part (one entry per domain, field-naming gotchas).

---

## Maintenance is the hard part

Skill docs describe a data model that changes daily, so **without active maintenance they're wrong within weeks.** Anthropic watched offline accuracy **drift from ~95% at launch to ~65% over a month** before treating drift as an engineering problem. The fixes:

- **Colocate** skill markdown in the same repo as the transformation models, so the PR that changes a model is the PR that updates the doc describing it.
- A **code-review hook** flags any reporting-model change that doesn't touch a skill file. **~90% of data-model PRs now include a skill change in the same diff.**
- **Prune** scaffolding as models improve and old failure modes stop applying.

This is the same **drift / colocation** problem named in [AGENTS.md](agents-md.md) and [Context Engineering](context-engineering.md) — except skills solve it with tooling (the hook + same-repo colocation) rather than leaving it as the "unsolved problem" that AGENTS.md docs cite.

---

## One source, every surface

The same skill *must* give the same answer in Slack, the IDE, a dashboard tool, and standalone sessions. Anthropic keeps one canonical source (the data repo); on merge the skill **auto-syncs** to a plugin marketplace (for IDE users), to cloud-storage blobs (for hosted apps reading a single file), and is served directly as resources over **MCP**. They designed for portability up front — no hardcoded repo paths, no surface-specific namespaces.

---

## Skills vs AGENTS.md

Both are markdown context for agents, both live by progressive disclosure and reference docs, both die from drift. The differences:

| | **Skill** | **[AGENTS.md](agents-md.md)** |
|---|---|---|
| Domain | Analytics / any task domain | Coding |
| Loading | On-demand, trigger-gated by frontmatter | Auto-discovered (100%) up the dir tree |
| Shape | Router + process pair + reference folder | Single file + module overrides |
| Knowledge type | Procedural (how to work) | Mostly constraints + non-inferable facts |
| Drift fix | CI hook + repo colocation (largely solved) | Discipline + trimming (unsolved) |

---

## Related Pages

- [Agentic Analytics](agentic-analytics.md) — the 21%→95% result in context
- [Semantic Layer](semantic-layer.md) — what skills route to first
- [AGENTS.md](agents-md.md) — the coding cousin
- [Context Engineering](context-engineering.md) — progressive disclosure, drift, structure-not-access
- [Iterative Repair Loops](iterative-repair-loops.md) — the adversarial-review sub-agent loop
- [Anthropic](../entities/anthropic.md)
- [Source: How Anthropic Enables Self-Service Data Analytics with Claude](../sources/2026-06-03-anthropic-self-service-analytics.md)
