---
tags: [data-n-ai, entity, agents]
sources: ["raw/data-n-ai/articles/A good AGENTS.md is a model upgrade. A bad one is worse than no docs at all..md", "raw/data-n-ai/articles/How to Build Your AGENTS.md (2026) The Context File That Makes AI Coding Agents Actually Work.md"]
updated: 2026-06-05
---

# Augment Code

Enterprise AI software-development platform centered on a "context engine" — semantic indexing of large codebases (hundreds of thousands of files) to feed coding agents. Publisher of both AGENTS.md source studies in this wiki, and the source of the AuggieBench eval methodology.

## Products

- **Auggie** — Augment's CLI coding agent (`auggie --print --quiet "..."`), used for summarization and agentic dev tasks.
- **Context Engine** — semantic index + dependency map across a codebase, usable as an MCP server alongside a manual `AGENTS.md`. Pitched as most useful during cross-service refactoring; maintains a live understanding of how files connect without manual updates.
- **Intent** — spec-driven development product. Instead of a static instruction file, introduces **living specs** that agents update as they work ("when an agent completes work, the spec updates to reflect reality"). Architecture: a *coordinator* agent drafts the spec and generates tasks; *implementor* agents execute in parallel waves (per-workspace git worktrees); a *verifier* agent checks results against the spec. Positioned as the answer to `AGENTS.md` drift/staleness at scale.

## AuggieBench (eval methodology)

Internal eval suite: start from high-quality merged PRs in a large repo, reconstruct the environment + prompt, have the agent redo the task, and score its output against the "golden PR" that actually landed after senior review. PRs with scope creep or known bugs are filtered out. Used in the AGENTS.md study to measure with-file vs without-file deltas (correctness, completeness, best_practices, code_reuse).

## Notable findings (their AGENTS.md study)

- A good `AGENTS.md` gave a quality jump "equivalent to upgrading from Haiku to Opus"; a bad one was worse than no file.
- The same file helped a routine bug fix (+25% best_practices) and hurt a complex feature (−30% completeness) in the same module.
- Documentation *discovery* is wildly uneven: `AGENTS.md` is read 100% of the time, references >90%, orphan `_docs/` <10%.

## Caveats / positioning

Both source pieces are vendor content with a clear funnel to Augment's Intent product (repeated "Build with Intent" CTAs). The empirical claims (AuggieBench deltas, discovery-rate traces) and the third-party ETH Zurich citation are the durable parts; the "living specs solve drift" framing is product marketing.

## Related Pages

- [AGENTS.md](../concepts/agents-md.md)
- [Context Engineering](../concepts/context-engineering.md)
- [Source: A Good AGENTS.md Is a Model Upgrade](../sources/2026-04-23-good-agents-md-model-upgrade.md)
- [Source: How to Build Your AGENTS.md (2026)](../sources/2026-04-01-how-to-build-agents-md.md)
