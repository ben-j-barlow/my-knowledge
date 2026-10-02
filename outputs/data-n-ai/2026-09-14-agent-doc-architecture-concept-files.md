---
tags: [data-n-ai, synthesis, agents, prompt-engineering, etl]
sources:
  - wiki/concepts/agents-md.md
  - wiki/concepts/context-engineering.md
  - wiki/concepts/agentic-analytics.md
  - wiki/concepts/semantic-layer.md
  - wiki/concepts/claude-skills.md
  - wiki/concepts/correctness-layer.md
  - wiki/concepts/data-contracts.md
  - wiki/concepts/agents-in-data-engineering.md
updated: 2026-09-14
---

# Where should cross-cutting concept files live relative to per-table docs?

**Question:** For a monorepo's agent-facing data documentation (per-table notes
under `docs/data-catalog/<layer>/<table>.md`, keyed by data location), where
should business/domain concept files that many tables depend on (index
rebalance methodology, fiscal calendar, corporate action conventions) live —
nested under the catalog (`docs/data-catalog/concepts/`), promoted to a
top-level sibling (`docs/concepts/`), or a stub-under-catalog pointing at a
top-level canonical file?

## Recommendation

**Option B — promote to a top-level `docs/concepts/` sibling, with table
frontmatter's `related_concepts` linking directly to it.** Treat Option C
(catalog-local stubs) as explicitly premature; do not build it until a
concrete case demands catalog-specific framing. Option A is the fallback only
if the repo's docs root cannot support a new top-level directory for some
non-documentation reason.

This knowledge base has ingested several independent studies of agent-facing
documentation design (AGENTS.md, Claude Skills, semantic layers, correctness
layers) that converge on principles directly applicable here.

## Why: the two load-bearing findings

**1. Discovery is trigger-mediated, not path-mediated, in this design — so
naming/location matters for humans wiring the triggers, not for grep.**
The [AGENTS.md](../../wiki/concepts/agents-md.md) discovery-rate data found
`AGENTS.md` itself auto-discovered 100% of the time, its direct references
read >90% of the time, but orphan docs nothing points to are read **<10%** of
the time. The mechanism that matters isn't file-system proximity, it's
**whether something is referenced from the entry point the agent already
consults for the task at hand.** In the proposed design, that entry point is
CLAUDE.md's trigger rule (anomaly language) for per-table docs, and — this is
the crux — whatever trigger rule fires for research/scenario-writing tasks.
A concept file under `docs/concepts/` is exactly as discoverable as one under
`docs/data-catalog/concepts/` *provided each task's trigger references it*.
The real risk Option A introduces is upstream of the agent: a human writing
the trigger rule for a research task is less likely to think to reference a
folder named for the data catalog than one named `docs/concepts/`, because
the label itself signals scope. Naming is a proxy for the mental model of
whoever writes the routing rule, not a grep-time cost.

**2. Single canonical definition beats indirection layers — this KB has seen
this exact tradeoff fail twice already.** [Semantic Layer](../../wiki/concepts/semantic-layer.md)
documents Anthropic's finding that a smaller, single, human-owned governed
definition beat a larger auto-generated or duplicated one — auto-generating
a second layer "encoded the very ambiguities it was meant to eliminate," and
was net-negative on evals versus the smaller curated one. [Claude Skills](../../wiki/concepts/claude-skills.md)
generalizes this to "generate documentation with the LLM, but let a human own
the definition." Option C's stub-plus-canonical structure is a second
indirection layer over the same concept — it doesn't eliminate ambiguity, it
adds a synchronization surface (stub vs. canonical: which one is "the"
definition when they diverge?) with no attacking failure mode behind it yet.
[Context Engineering](../../wiki/concepts/context-engineering.md)'s
structure-not-access principle applies directly: the fix for
"an agent might not find the right concept file" is *better structure at the
reference point* (a correct `related_concepts` backlink), not *more files to
route through*.

## Evaluated against the five axes

### Discoverability for non-catalog tasks
- **A (nested):** Weak by default. A research/strategy agent has no reason
  to look inside a folder literally named for the data catalog unless a
  human explicitly wires a cross-cutting reference into that task's trigger
  rule — and that's an easy thing to forget precisely because the path
  argues against it.
- **B (top-level sibling):** Strong. `docs/concepts/` reads as domain
  knowledge independent of any one consumer. Any task's CLAUDE.md trigger
  ("read relevant concept docs when working with index membership, rebalance
  dates, fiscal periods, corporate actions...") points to one place a human
  will naturally write it under.
- **C (stub + canonical):** Same as B *if* the agent is told to always follow
  the stub to the canonical file — but that's an unnecessary extra hop for
  every non-catalog task, which by definition never enters through the
  catalog stub at all. It doesn't help this axis; the top-level file it
  points to is what actually gets found.

### Duplication / drift risk
- **A:** No duplication (still one file), but topic-mislabeling risk: over
  time, contributors who think of a concept as "data catalog stuff" may start
  drafting catalog-flavored prose into it that doesn't serve the
  research/strategy consumer — a semantic drift risk rather than a literal
  file-duplication one.
- **B:** Lowest risk. One file, one owner, no second copy to fall out of
  sync. Matches the semantic-layer precedent directly: one governed
  definition, not one per consumer context.
- **C:** Highest risk of the three. Two files (stub + canonical) that must
  stay pointed at each other; if the stub ever accretes real content instead
  of staying a pure pointer (the AGENTS.md study's "bloat" failure mode —
  every future contributor is tempted to add "just a little catalog-specific
  note" to the stub rather than touch the canonical file), it silently
  forks into a second definition. This is the exact anti-pattern the
  semantic-layer finding warns against, self-inflicted.

### Maintenance burden
- **A:** One file to update per concept change; zero burden from this axis
  alone. Its cost is entirely on the discoverability axis, not here.
- **B:** Same as A — one file. When a new table depends on an existing
  concept, only that table's frontmatter `related_concepts` list needs a new
  entry; the concept file itself doesn't change.
- **C:** Two touch points minimum per concept change (verify the stub's
  pointer/framing still matches) and a standing question of *which* file a
  human should even edit when the concept changes — the kind of ambiguity
  [Data Contracts](../../wiki/concepts/data-contracts.md) and the
  [Correctness Layer](../../wiki/concepts/correctness-layer.md) exist
  specifically to eliminate in the data itself; it's self-defeating to
  reintroduce it in the docs describing the data.

### Progressive disclosure fit
- **A and B are equivalent here.** Both keep concept files out of the
  per-table load path by default — a table file is read on its own trigger,
  and only pulls in a concept file via `related_concepts` when relevant,
  exactly the pairwise router/reference-doc pattern [Claude Skills](../../wiki/concepts/claude-skills.md)
  describes for the knowledge-skill/reference-doc split. Directory placement
  doesn't change this; the backlink does the work.
- **C** actively hurts this axis for catalog-triggered reads: it inserts an
  extra file open (stub → canonical) on the *single most common* path — a
  table file's `related_concepts` link — for a benefit (catalog-specific
  framing) that doesn't exist yet. Extra indirection with no payload is pure
  overhead, the same "redundant, no signal" pattern the ETH Zurich
  auto-generated-context-file finding describes for LLM-authored files that
  duplicate what's discoverable elsewhere.

### Does the concept actually need catalog-specific framing?
No evidence in this KB — or in the prompt's own framing — that it does yet.
The prompt's own text flags this ("isn't a confirmed need yet"). The
AGENTS.md findings are explicit that rules/structure should respond to
**observed failure**, not be built speculatively: *"Rules added speculatively
bloat the window; rules added in response to a real failure carry signal."*
A stub layer built now, before any concept has shown a genuine
catalog-vs-general divergence, is exactly the speculative-structure pattern
this KB has already seen backfire twice (auto-generated semantic layer,
auto-generated context files).

## Bottom line

Go with **Option B**. Concrete shape:

```
docs/
  data-catalog/
    bronze/<table>.md
    silver/<table>.md
    gold/<table>.md
  concepts/
    index-rebalance-methodology.md
    fiscal-calendar.md
    corporate-actions.md
```

Table frontmatter carries `related_concepts: [index-rebalance-methodology]`
pointing directly at `docs/concepts/`. CLAUDE.md's trigger rule for
non-catalog tasks (research notes, strategy scenarios) references
`docs/concepts/` directly, independent of whether the task touches the data
catalog at all.

**Prerequisite for revisiting Option C:** only build the stub layer once a
concept demonstrably needs two different framings — e.g., an agent doing
catalog work needs a terse "here's the rebalance-date field mapping" capsule
while a strategy-research agent needs the full methodology narrative, and a
single file genuinely can't serve both without either bloating past a useful
length for one consumer or omitting detail the other needs. Until that's an
observed problem (not a hypothetical one), a single canonical file per
concept is sufficient, per every precedent this KB has on the topic.

**One gap worth flagging:** none of the ingested sources describe a drift
*enforcement* mechanism for concept files analogous to Anthropic's
skill-colocation CI hook ([Claude Skills](../../wiki/concepts/claude-skills.md))
that fails a PR touching a reporting model without touching its skill file.
Given `last_reviewed` / `unconfirmed`-tag freshness signals are already
planned for the per-table notes, the same colocation-plus-CI-hook idea (flag
a PR that changes rebalance logic without touching
`docs/concepts/index-rebalance-methodology.md`) is the natural next step once
this structure is in place — worth scoping as a follow-up, not a blocker to
adopting Option B now.
