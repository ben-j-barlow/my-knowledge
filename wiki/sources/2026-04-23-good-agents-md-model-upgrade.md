---
tags: [data-n-ai, source, agents, prompt-engineering]
sources: ["raw/data-n-ai/articles/A good AGENTS.md is a model upgrade. A bad one is worse than no docs at all..md"]
updated: 2026-06-05
---

# Source: A Good AGENTS.md Is a Model Upgrade. A Bad One Is Worse Than No Docs at All.

**Author:** Slava Zhenylenko (Member of Technical Staff, [Augment Code](../entities/augment-code.md))
**Published:** 2026-04-23
**URL:** https://www.augmentcode.com/blog/how-to-write-good-agents-dot-md-files

Empirical study: Augment pulled dozens of `AGENTS.md` files from their monorepo and measured each one's effect on code generation using **AuggieBench** (run each task twice, with and without the file, score against the golden merged PR). Headline: the best files gave a quality jump "equivalent to upgrading from Haiku to Opus"; the worst were worse than no file at all.

## Key claims

- **The same file can help one task and hurt another by 30%.** One file boosted `best_practices` +25% on a routine bug fix and dropped `completeness` −30% on a complex feature in the same module. Different *blocks* of the document had opposite effects on different tasks — a decision table helped the bug fix; the reference sprawl pulled the feature task into overexploration.
- **Sweet spot: 100–150 line files + a handful of focused reference docs**, on mid-size modules (~100 core files). These delivered 10–15% gains across all metrics. Past ~150 lines, gains reverse.

### Patterns that work
1. **Progressive disclosure** beats comprehensive coverage (treat it like a skill).
2. **Procedural numbered workflows** — a six-step deploy workflow cut PRs with missing wiring files 40%→10%, correctness +25%, completeness +20%.
3. **Decision tables** for 2–3 reasonable options (React Query vs Zustand example) — +25% `best_practices`.
4. **Real 3–10 line examples** from prod code — +20% `code_reuse`.
5. **Domain-specific rules** (e.g. `Decimal` not `float` for money) — works when specific and enforceable.
6. **Pair every "don't" with a "do"** — warning-only docs underperform; 15+ bare "don'ts" cause overexploration.
7. **Keep modules and the doc modular** — module-level beats huge cross-cutting root files.

### Failure modes
- **The overexploration trap (= context rot)**, two triggers: too much architecture overview (agent reads 12 docs / ~80K tokens before a 2-line change, completeness −25%) and excessive warnings (30+ "don'ts" → PR takes 2× as long, 20% less complete). Fix: concise isolated architecture (the *what*, not the *why*); core gotchas in main file, rest in references.
- **New patterns break old documentation** — docs describing REST+polling steered the agent to build polling when the golden PR used WebSockets. Fix is spec-driven development, not a better file.
- **The surrounding-docs problem** — worst performers sat on top of doc sprawl (one module: 226 docs, 2MB+). Removing the `AGENTS.md` barely changed behavior because the agent kept reading the sprawl. *Fix the documentation environment, not just the entry point.*

### Discovery rates (traced across hundreds of sessions)
`AGENTS.md` 100% · references out of it >90% · directory README 80%+ (when working there) · nested READMEs ~40% · orphan `_docs/` <10%. **`AGENTS.md` is the only documentation location with reliable discovery.** Caveat: ~half of all search hits came from grep/semantic search, not references.

## Notable quotes

> "The best ones gave our coding agent a quality jump equivalent to upgrading from Haiku to Opus. The worst ones made the output worse than having no AGENTS.md at all."

> "If your AGENTS.md is good but your module has 500K of specs around it, the specs are what the agent is reading."

## Scope / caveats

One-shot trajectories only (agent finishing coding tasks without human intervention). Did **not** cover maintenance over time, or operational/interactive/analytics tasks. Vendor content (Augment) — but the empirical AuggieBench deltas are the durable contribution.

## Related Pages

- [AGENTS.md](../concepts/agents-md.md)
- [Context Engineering](../concepts/context-engineering.md)
- [Augment Code](../entities/augment-code.md)
- [Source: How to Build Your AGENTS.md (2026)](2026-04-01-how-to-build-agents-md.md) — the companion how-to guide
- [Human-in-the-Loop](../concepts/human-in-the-loop.md)
