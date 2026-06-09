---
tags: [data-n-ai, concept, agents, prompt-engineering]
sources: ["raw/data-n-ai/articles/A good AGENTS.md is a model upgrade. A bad one is worse than no docs at all..md", "raw/data-n-ai/articles/How to Build Your AGENTS.md (2026) The Context File That Makes AI Coding Agents Actually Work.md"]
updated: 2026-06-05
---

# AGENTS.md

`AGENTS.md` is a Markdown file at a repository root (or any directory level) that gives AI coding agents persistent, project-specific operational guidance: build commands, conventions, testing rules, and constraints the agent **cannot infer from the codebase alone**. Think of it as a README written for agents instead of humans.

It is converging as a cross-tool standard. OpenAI pioneered the format for Codex; in December 2025 it was donated to the **Agentic AI Foundation** (a directed fund under the Linux Foundation), alongside Anthropic donating MCP and Block donating Goose. Claude Code natively reads `CLAUDE.md`; the common pattern is to symlink `CLAUDE.md → AGENTS.md` so one file serves all tools.

This page covers **what to put in it, what to leave out, the patterns that work, the failure modes, and the measured cost/benefit**. It is the applied counterpart to [Context Engineering](context-engineering.md) — `AGENTS.md` is the highest-leverage context-engineering surface because it is the only documentation location with reliable agent discovery.

---

## The core principle: only what the agent cannot infer

Both source studies converge on one rule: **write only non-inferable details.** The agent already knows how to write Python or TypeScript, and it can summarize your architecture by reading the code. What it cannot know:

| Content type | Include? | Reason |
|---|---|---|
| Custom build commands not documented elsewhere | ✅ Yes | Non-inferable |
| Highly specific tooling choices (e.g. `pixi` not `pip`, `pnpm` not `npm`) | ✅ Yes | Underrepresented in training data |
| Counterintuitive patterns (e.g. "`client.api` never throws — `try/catch` is always wrong") | ✅ Yes | Highest signal-to-noise in the whole file |
| "Don't touch" zones, secrets rules, permission boundaries | ✅ Yes | Non-inferable, high value |
| Codebase overviews / architecture summaries | ❌ No | Agents find these independently; trigger overexploration |
| Anything already in README or existing docs | ❌ No | Redundant; adds cost and reasoning steps without signal |

The ETH Zurich study (see [Context Engineering](context-engineering.md)) found that removing an "Architecture" section while keeping only commands, constraints, and non-standard patterns produced **the same agent behavior at lower token cost.** Architecture overviews "do not provide effective overviews."

---

## Patterns that work (Augment Code AuggieBench study)

Augment Code ran every task twice — with and without the file — and compared against golden PRs. The best files delivered a quality jump "equivalent to upgrading from Haiku to Opus." The patterns, in rough order of impact:

1. **Progressive disclosure beats comprehensive coverage.** Treat `AGENTS.md` like a skill: cover common cases at a high level, push details into reference files the agent loads on demand. **100–150 line** files with a handful of focused references were the top performers — 10–15% improvement across all metrics in mid-size modules (~100 core files). Past ~150 lines the gains reverse.
2. **Procedural workflows take agents from failing to finishing.** A numbered multi-step workflow was one of the strongest patterns measured. One six-step "deploy a new integration" workflow dropped PRs with missing wiring files from **40% → 10%**, raised correctness +25%, completeness +20%.
3. **Decision tables resolve ambiguity before the agent writes code.** When there are 2–3 reasonable ways to do something, a table forces the choice up front. (Example: React Query vs Zustand keyed on questions like "server is the only data source?") → +25% on `best_practices`. This is the pattern that most directly improved convention adherence.
4. **Real examples from the codebase improve reuse.** Short 3–10 line snippets from actual production code → +20% `code_reuse`. More than a few and the agent pattern-matches on the wrong thing.
5. **Domain-specific rules still matter.** e.g. "Use `Decimal` instead of `float` for all financial calculations." Works when the rule is specific and enforceable; stops working when you stack dozens.
6. **Pair every "don't" with a "do".** Warning-only docs consistently underperformed. `Don't instantiate HTTP clients directly` → pair with `Use the shared apiClient from lib/http with retry middleware`. A bare "don't" makes the agent cautious and exploratory; the pair tells it what to do and moves on. 15+ sequential "don'ts" with no "dos" causes overexploration.
7. **Keep code modular, and `AGENTS.md` too.** Module-level files describing relatively isolated submodules outperform huge cross-cutting root files.

### Map: pattern → metric

| To improve… | Use… |
|---|---|
| Reuse of existing code | Several relevant prod-code examples |
| Following established practices | Decision tables for components/libraries |
| Proper wiring of big features | Procedural numbered workflow |
| Handling of gotchas | "Don't" paired with "Do" |
| Context rot | Progressive disclosure via reference files |

---

## Failure modes

- **The overexploration trap (context rot).** The most common failure. Two triggers: (1) **too much architecture overview** — the agent reads a dozen doc files (~80K tokens) to "understand the architecture" before a two-line config change, then ships an incomplete fix (completeness −25%); (2) **excessive warnings** — 30+ "don'ts" make the agent check every rule for relevance and explore code it never needed to touch (PR took 2× as long, 20% less complete). Fix: concise, isolated architecture descriptions focused on the *what* not the *why*; core gotchas in the main file, the rest in references.
- **Bloat.** Every agent mistake tempts a new rule; rules are rarely removed. The file accumulates contradictory patches. More rules ≠ better performance. Rules should respond to *observed* failure, not be generated speculatively.
- **New patterns break old documentation.** If you're introducing an architecture that doesn't exist yet (e.g. WebSockets in a REST+polling codebase), the file steers the agent wrong. The fix isn't a better `AGENTS.md` — it's spec-driven development for net-new work.
- **Stale structural references actively mislead.** Docs describing repo structure become liabilities as the code changes. Drift is the central maintenance problem — and there's no automated staleness detector.
- **Silent rule dropout in long sessions.** The "lost in the middle" phenomenon. Keep files short, put critical rules early, start new sessions for new tasks.
- **The surrounding-docs problem.** A focused 150-line file sitting on top of 500K of surrounding specs won't save the agent — it finds and reads the sprawl anyway. *Fix the documentation environment, not just the entry point.*

---

## How agents actually discover docs

Augment traced documentation discovery across hundreds of sessions. Discovery rates are lopsided:

- `AGENTS.md` — auto-discovered **100%** of the time (every file up the hierarchy from the working dir).
- References out of `AGENTS.md` — read in **>90%** of sessions when the agent has a reason to pull them in.
- Directory-level `README.md` — **80%+** when working in that directory (not auto-loaded).
- Nested READMEs (dirs not currently in) — **~40%**.
- Orphan docs in `_docs/` that nothing references — **<10%**.

> `AGENTS.md` is the only documentation location with reliable discovery. If something must be seen, it lives there or is directly referenced from there.

Caveat: about half of all search-result hits in the traces came from grep/semantic search, not from `AGENTS.md` references — so legacy docs with searchable code examples still get found.

---

## Core sections (GitHub 2,500-repo + OpenAI convergence)

1. **Stack definition with exact versions** (without it the agent defaults to whatever API conventions dominate its training data).
2. **Executable commands with full flags** — place early; the agent references them repeatedly. Codex treats these as advisory programmatic checks it *may* run before finishing.
3. **Coding conventions** — one real snippet beats three paragraphs; document the *counterintuitive* convention.
4. **Testing rules** — exact commands for complex build systems.
5. **"Don't touch" zones / permission boundaries** — a three-tier `✅ Always / ⚠️ Ask First / 🚫 Never` hierarchy. "Never commit secrets" was the single most common helpful constraint across 2,500+ repos.
6. **Non-standard tooling** — highest ROI for tools underrepresented in training data.

## Modular organization

Start with a single root file. Split into subdirectory files when it exceeds **150–200 lines**. The agent reads the file closest to the file being edited; more deeply nested files take precedence on conflict. (Observed upper bound in the wild: the `maas` repo at 371 lines.)

```
project/
├── AGENTS.md          # org-wide standards, global commands
├── apps/web/AGENTS.md # web overrides
├── apps/api/AGENTS.md # api overrides
└── infra/AGENTS.md    # infra rules
```

---

## Bottom line

- **Hand-write it; never auto-generate-and-commit.** LLM-generated files give negative returns (worse performance at higher cost); human-curated files give ~4 points of improvement. See [Context Engineering](context-engineering.md) for the underlying ETH Zurich numbers.
- **Keep it ~100–150 lines.** Progressive disclosure, not comprehensive coverage.
- **The "Non-Obvious Patterns" section is where the file earns its keep.** Counterintuitive decisions with mechanism explanations generalize the agent to novel situations.
- **Treat it like code:** version-control it, review changes, and prune rules that no longer correspond to observed failures.
- **Drift is the unsolved problem.** Vendors (Augment's Intent/Context Engine) propose "living specs" that agents update as they work, but at the manual-file level the answer is discipline and aggressive trimming. *Anthropic's analytics team did partly solve it* for their analogous [skills](claude-skills.md): colocate the doc with the model it describes in one repo, and add a **CI/code-review hook that fails any model PR not touching its skill file** — ~90% of their data-model PRs now update the doc in the same diff. (See [Claude Skills](claude-skills.md) for the comparison.)

This is one instance of the broader [Ralph Loop](ralph-loop.md) / [Human-in-the-Loop](human-in-the-loop.md) theme: agents do best when the human encodes *direction and constraints* up front, not when they bury the agent in exhaustive reference material.

## Related Pages

- [Context Engineering](context-engineering.md) — the broader discipline; ETH Zurich cost/benefit study lives here
- [Claude Skills](claude-skills.md) — the analytics analogue: procedural, on-demand, drift solved with a CI hook
- [Agentic Analytics](agentic-analytics.md)
- [Augment Code](../entities/augment-code.md) — publisher of both source studies
- [Ralph Loop](ralph-loop.md)
- [Human-in-the-Loop](human-in-the-loop.md)
- [AI Org Operating Model](ai-org-operating-model.md)
- [Source: A Good AGENTS.md Is a Model Upgrade](../sources/2026-04-23-good-agents-md-model-upgrade.md)
- [Source: How to Build Your AGENTS.md (2026)](../sources/2026-04-01-how-to-build-agents-md.md)
