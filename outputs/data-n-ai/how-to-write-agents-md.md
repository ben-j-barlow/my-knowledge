---
tags: [data-n-ai, synthesis, agents, prompt-engineering]
sources: [wiki/concepts/agents-md.md, wiki/concepts/context-engineering.md]
updated: 2026-06-05
---

# How to Write a Good AGENTS.md

A reusable master template for writing `AGENTS.md` files — the context file coding agents (Claude Code, Codex, Cursor, Copilot) read to learn your project's conventions. Written to be read by both **humans** and **the agent itself**.

Synthesised from the empirical findings in [agents-md](../../wiki/concepts/agents-md.md) and [context-engineering](../../wiki/concepts/context-engineering.md).

## How to use this

1. Copy **Part B** (the skeleton) into your project root as `AGENTS.md`.
2. Fill in the `<!-- Insert ... -->` slots, following the guidance in **Part A**. Leave any slot blank if it doesn't apply — don't pad it.
3. Reference this guide from your project's `CLAUDE.md` so an agent updates `AGENTS.md` after finishing work (snippet at the very end).

---

# Part A — The Guidance

## Why it's worth getting right

The stakes are asymmetric — this is why restraint matters more than coverage:

- A **good** `AGENTS.md` gives a quality jump equivalent to a model upgrade (Haiku → Opus).
- A **bad** one is *worse than having no file at all* — it pulls the agent into over-reading and produces less complete work.
- It costs **~20% inference overhead either way**. Only careful human curation buys the upside; **auto-generating and committing gives negative returns** (worse output at higher cost).

So: **hand-write it, keep it lean, and treat it like code** (version-control it, review changes, prune rules that no longer match reality).

## The one rule

> **Write only what the agent cannot infer from the codebase.**

Everything else follows from this. The agent already knows your language and can read your code to understand structure; documenting that just adds cost and triggers over-exploration.

| Include ✅ | Exclude ❌ |
|---|---|
| Custom build/run commands not documented elsewhere | Codebase or architecture overviews (agents find these themselves) |
| Specific tooling choices (`pixi` not `pip`, `pnpm` not `npm`) | Anything already in the README or existing docs |
| Counterintuitive patterns + *the mechanism* behind them | General design rationale / "why we built it this way" |
| Domain rules that are specific and enforceable | Long lists of vague warnings |
| "Don't touch" zones, secrets rules, permission boundaries | Stale directory/structure listings that drift out of date |

## Length & shape

- Target **100–150 lines** plus a handful of focused reference files the agent loads on demand (**progressive disclosure** — outline *what* is in each reference, go no deeper).
- Gains reverse past ~150 lines. **Split into subdirectory `AGENTS.md` files at ~150–200 lines** — the agent reads the file closest to what it's editing, and more deeply nested files win on conflict.

## The six core sections

1. **Stack** — framework + **exact versions**, package manager, runtime version. Without this the agent defaults to whatever conventions dominate its training data.
2. **Commands** — install / build / typecheck / lint / test, **with full flags**. Place early; the agent references them repeatedly.
3. **Conventions** — **one real code snippet beats three paragraphs.** Spend your words on the *counterintuitive* convention (e.g. "`client.api` never throws — `try/catch` around it is always wrong") and explain the mechanism so the agent generalises.
4. **Testing** — exact test commands; determinism and mocking rules.
5. **Boundaries** — a three-tier hierarchy: `✅ Always` / `⚠️ Ask first` / `🚫 Never`. "Never commit secrets" is the single most valuable constraint across thousands of repos.
6. **Non-standard tooling** — highest ROI for tools underrepresented in training data. Skip standard tools (npm, pytest, cargo) — the agent already knows them.

## 7 patterns that work

| Pattern | Moves | How |
|---|---|---|
| Progressive disclosure | Context rot ↓ | Cover common cases; push detail into reference files |
| Procedural numbered workflow | Wiring of big features ↑ | Step-by-step for multi-file tasks (e.g. "add an integration") |
| Decision table | Convention adherence ↑ | When 2–3 valid approaches exist, force the choice up front |
| Real prod-code examples | Code reuse ↑ | A few 3–10 line snippets from actual code |
| Domain-specific rules | Gotcha handling ↑ | Specific + enforceable only (e.g. `Decimal` not `float` for money) |
| Pair every "don't" with a "do" | Over-exploration ↓ | `Don't instantiate HTTP clients` → `Use lib/http's apiClient` |
| Keep it modular | All metrics ↑ | Module-level files beat one giant root file |

## Failure modes to avoid

- **Over-exploration (context rot)** — the most common failure. Triggers: too much architecture overview, or many bare "don'ts." The agent reads dozens of files before touching code and ships less. *Fix: cut architecture to the* what *not the* why*; pair every "don't" with a "do."*
- **Rule bloat** — a new rule after every mistake, none ever removed. More rules ≠ better. *Fix: add rules only in response to observed failure; prune regularly.*
- **Stale structural references** — directory/architecture listings actively mislead once the code moves. *Fix: don't document structure the agent can see for itself.*
- **Silent dropout** — in long sessions, mid-file rules get ignored ("lost in the middle"). *Fix: keep it short, put critical rules early, start fresh sessions for new tasks.*
- **The surrounding-docs trap** — a lean `AGENTS.md` sitting on 500K of spec sprawl won't save the agent; it reads the sprawl anyway. *Fix the documentation environment, not just the entry point.*

## Pre-submit checklist

- [ ] Under ~150 lines?
- [ ] Only non-inferable content (nothing the agent could read from the code or README)?
- [ ] No architecture / codebase overview section?
- [ ] Every "don't" paired with a "do"?
- [ ] Commands include full flags?
- [ ] Counterintuitive patterns documented *with their mechanism*?
- [ ] References outlined, not inlined (progressive disclosure)?
- [ ] **Gold standard:** ran a representative task with and without the file and confirmed it actually helps?

---

# Part B — Copy-Paste AGENTS.md Skeleton

Lift this block into your project root as `AGENTS.md` and fill the slots. Delete any section that doesn't earn its place.

```markdown
# AGENTS.md — <project name>

## Stack
<!-- Insert: language, framework + EXACT versions, package manager, runtime version.
     e.g. "Next.js 15 (App Router), TypeScript, pnpm (never npm), Node 22.x required" -->

## Commands
<!-- Insert: install / dev / build / typecheck / lint / test — WITH full flags.
     Place the ones the agent runs most often first. -->

## Conventions
<!-- Insert: ONE representative code snippet from this codebase, then any
     counterintuitive patterns WITH the mechanism that makes them correct.
     Skip anything obvious from reading the code. -->

## Testing
<!-- Insert: exact test command(s); determinism + mocking rules. -->

## Boundaries
### ✅ Always
<!-- e.g. run lint before committing; list only human authors in commits -->
### ⚠️ Ask first
<!-- e.g. schema changes; adding/removing dependencies; deleting files -->
### 🚫 Never
<!-- e.g. commit .env / secrets; force-push to main; modify vendor/ or generated code -->

## Non-standard tooling
<!-- Insert: ONLY tools underrepresented in training data (custom CLIs, pixi, etc.).
     Omit standard tools — the agent already knows npm/pytest/cargo. -->
```

## Reference this guide from your CLAUDE.md

Add a short pointer so the agent maintains `AGENTS.md` as part of finishing work:

```markdown
## Maintaining AGENTS.md
After completing a feature, check whether AGENTS.md needs updating. Follow the guide
at docs/how-to-write-agents-md.md — keep it under ~150 lines, document only what
can't be inferred from the code, and pair every "don't" with a "do".
```

---

## Further reading

- [AGENTS.md (concept)](../../wiki/concepts/agents-md.md) — the full empirical findings
- [Context Engineering (concept)](../../wiki/concepts/context-engineering.md) — the cost/benefit numbers and context-rot theory
- [Source: A Good AGENTS.md Is a Model Upgrade](../../wiki/sources/2026-04-23-good-agents-md-model-upgrade.md)
- [Source: How to Build Your AGENTS.md (2026)](../../wiki/sources/2026-04-01-how-to-build-agents-md.md)
