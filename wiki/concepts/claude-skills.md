---
tags: [data-n-ai, concept, agents, prompt-engineering]
sources: ["raw/data-n-ai/articles/How Anthropic enables self-service data analytics with Claude.md", "raw/data-n-ai/articles/2026-09-11-wikiskill-agent-skill-evolution.md"]
updated: 2026-09-11
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

## Automated Skill Evolution (WikiSkill)

Anthropic's approach above is **human-maintained**: engineers write skills, and a CI hook keeps them from drifting out of sync with the code. Google Research's WikiSkill (2026) proposes the fully-automated counterpart — a framework that discovers and refines skills itself, with a structural twist that validates the maintenance strategy above from a different angle.

WikiSkill inserts a **persistent wiki layer between raw execution traces and the evolving skills**: a `raw/` layer of immutable execution traces, a `wiki/` layer of structured, compounding patterns (an evolution log plus an audit trail of every proposed skill diff and its accept/reject outcome), and a `skills/` layer of the active procedural skills actually injected into the agent's prompt. An ablation isolates the wiki's contribution precisely: giving the skill-proposing agent access to this persistent wiki raised average benchmark score by +15 points over an otherwise-identical setup with no persistent knowledge layer at all — recurring failure modes that a single iteration's traces can't resolve get resolved once the pattern has been seen and recorded across several iterations.

One result reframes what "skill quality" even means: skills evolved by one model **transferred to and sometimes outperformed** the skills a different model evolved for itself (e.g. a 9B model reached 50.5% on a spreadsheet benchmark using a 27B model's skills, vs. 33.6% with its own). The paper's conclusion — *skill discovery and skill execution are distinct capabilities* — cuts against the assumption that an agent's own experience is the best source of its own procedural knowledge.

The design rule that most directly echoes this knowledge base's own architecture: the **inference/execution agent is deliberately denied wiki access during training rollouts** — only the maintenance and skill-proposal agents read it. Letting the executing agent shortcut through the wiki directly (rather than through skills) made its traces *less* informative for skill development. This is the automated-loop analogue of "LLM reads raw/, never writes it" and "the wiki is LLM-owned curated knowledge, not a dumping ground the working agent free-associates into."

## Related Pages

- [Agentic Analytics](agentic-analytics.md) — the 21%→95% result in context
- [Semantic Layer](semantic-layer.md) — what skills route to first
- [AGENTS.md](agents-md.md) — the coding cousin
- [Context Engineering](context-engineering.md) — progressive disclosure, drift, structure-not-access
- [Iterative Repair Loops](iterative-repair-loops.md) — the adversarial-review sub-agent loop
- [Anthropic](../entities/anthropic.md)
- [Session Continuity](session-continuity.md) — the same persistent-knowledge-layer pattern applied to skill evolution instead of task handoff
- [Source: How Anthropic Enables Self-Service Data Analytics with Claude](../sources/2026-06-03-anthropic-self-service-analytics.md)
- [Source: WikiSkill — Compiling Agent Experience into Persistent Knowledge for Skill Evolution](../sources/wikiskill-agent-skill-evolution.md)
