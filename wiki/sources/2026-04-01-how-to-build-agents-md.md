---
tags: [data-n-ai, source, agents, prompt-engineering, llm]
sources: ["raw/data-n-ai/articles/How to Build Your AGENTS.md (2026) The Context File That Makes AI Coding Agents Actually Work.md"]
updated: 2026-06-05
---

# Source: How to Build Your AGENTS.md (2026)

**Author:** Ani Galstian ([Augment Code](../entities/augment-code.md))
**Published:** 2026-04-01
**URL:** https://www.augmentcode.com/guides/how-to-build-agents-md

A how-to guide, anchored on the **ETH Zurich study** (arXiv:2602.11988) on context-file effectiveness and synthesizing GitHub's 2,500-repo analysis and OpenAI's Codex docs. Thesis: the question isn't whether to write an `AGENTS.md`, but whether yours improves performance or just adds token overhead — and that line is determined by writing only non-inferable detail, hand-curating (not auto-generating), and accepting a ~20% inference cost.

## Key claims

### The ETH Zurich quality threshold
- **LLM-generated context files hurt:** in 5/8 settings reduced success, +2.45–3.92 steps/task, +20–23% cost, −0.5% (SWE-bench Lite) to −2% (AGENTbench) success.
- **Developer-written files help modestly:** ~+4 points on AGENTbench, up to +19% cost.
- A follow-up that stripped all other repo docs first found LLM-generated files *then* helped +2.7% — proving they are **redundant with docs the agent already reads independently.**

### Write only the non-inferable
Include: custom build commands, specific tooling choices (`pixi` not `pip`), counterintuitive patterns, "don't touch" zones. Exclude: codebase/architecture overviews, anything already in README. Architectural overviews "do not provide effective overviews" — removing them keeps behavior identical at lower token budget.

### Core sections (GitHub + OpenAI convergence)
1. Stack definition with exact versions (e.g. "always pnpm, never npm; Node 22.x required").
2. Executable commands with full flags (placed early; Codex treats them as advisory pre-finish checks).
3. Coding conventions — one real snippet > three paragraphs; document the counterintuitive (e.g. NetCore's "`client.api` never throws → `try/catch` is always wrong").
4. Testing rules — exact commands for complex builds.
5. "Don't touch" zones — three-tier `✅ Always / ⚠️ Ask First / 🚫 Never`. "Never commit secrets" was the most common helpful constraint across 2,500+ repos.
6. Non-standard tooling — highest ROI for tools underrepresented in training data.

### Tool variants & interop
`AGENTS.md` converging as a cross-tool standard (donated to the Agentic AI Foundation under the Linux Foundation, Dec 2025, alongside MCP and Goose). Claude Code uses `CLAUDE.md` + auto-memory; Cursor uses `.cursor/rules/` with YAML frontmatter + glob scoping; Copilot uses `.github/copilot-instructions.md`. Symlink pattern keeps them from diverging: "CLAUDE.md is a symlink to AGENTS.md."

### Modular org & cost
Single root file until 150–200 lines, then split into subdirectory files (deeper files win on conflict). Cost: ~20% overhead regardless of source; **prompt caching (cache reads ~90% cheaper) is the primary mitigation.** Verdict: writing manually is worth the overhead; auto-generating and committing is not.

### Failure patterns
Auto-generated files worse than none; bloat (rules added on every mistake, never removed); silent rule dropout ("lost in the middle"); stale structural references actively mislead.

## Notable quotes

> "LLM-generated context files are redundant with existing documentation that agents already access independently. Duplicating that content adds cost without adding signal."

> "The 'Non-Obvious Patterns' section is where AGENTS.md delivers the highest signal-to-noise ratio."

## Caveats

Vendor content with heavy "Build with Intent" CTAs throughout. The ETH Zurich citation and the GitHub/OpenAI convergence are the durable parts; the Intent "living specs" pitch is marketing. Includes a complete copy-paste `AGENTS.md` template.

## Related Pages

- [AGENTS.md](../concepts/agents-md.md)
- [Context Engineering](../concepts/context-engineering.md) — ETH Zurich cost/benefit numbers
- [Augment Code](../entities/augment-code.md)
- [Source: A Good AGENTS.md Is a Model Upgrade](2026-04-23-good-agents-md-model-upgrade.md) — companion empirical study
