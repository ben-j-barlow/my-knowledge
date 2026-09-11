---
tags: [data-n-ai, source, agents, prompt-engineering, testing]
sources: [raw/data-n-ai/articles/2026-09-11-lecture-07-task-boundaries.md]
updated: 2026-09-11
---

# Source: Lecture 07 — Draw Clear Task Boundaries for Agents

Learn Harness Engineering course, lecture 7 of the series ([session continuity](lecture-05-context-continuity.md) is lecture 5, [feature lists](lecture-08-feature-lists.md) lecture 8, [premature completion](lecture-09-premature-completion.md) lecture 9). Diagnoses **overreach** — agents activating more work than a session can finish — as a harness problem, not a model-capability gap, and prescribes WIP=1 (work-in-progress limit of one) as the fix.

## Key Claims

- **Attention is a finite, dividable resource.** If context capacity is `C` and an agent activates `k` tasks at once, each gets roughly `C/k`. Below some threshold per task, none finish. Not a metaphor — treated as literally budget division.
- **Overreach and under-finish are the same failure, viewed from two ends**, and they compound: diluted attention → half-finished code → more system complexity → more overreach next round.
- **Measured effect**: agents using a "small next step" (WIP=1-equivalent) strategy showed a **37% higher completion rate** than broad-prompt agents (Anthropic). Lines of code generated correlates *negatively* with features actually completed.
- **Case study** (8-feature REST API, two runs): unconstrained mode activated 5 features in session 1, ~800 LOC across 12 files, 20% end-to-end pass rate, only 3/8 features done after 3 sessions. WIP=1 mode did one feature per session, ~200 LOC, 100% pass rate on what it touched, 7/8 features done after 4 sessions (8th blocked externally). **87.5% vs 37.5% completion**, with *less* total code (1200 vs 800 — WIP=1 used less).
- **Core primitives introduced**: Scope Surface (a DAG of work units — `not_started / active / blocked / passing`), Completion Evidence (an executable check, not "the code looks fine"), Completion Pressure (the harness force that keeps the agent from starting task N+1 before task N passes), Verified Completion Rate (VCR = verified / activated tasks; block new activations when VCR < 1.0).
- Frames the pattern as Kanban's WIP limit applied to agents, citing Little's Law (`L = λW` — more concurrent work inflates lead time per item) and Steve McConnell's *Rapid Development* finding that scope creep is the leading cause of project failure. The agent-specific twist: humans have an intuitive "I've done enough" signal; agents don't — generating the next "let me also fix this" costs the model almost nothing, so nothing stops it.

## Notable Quotes

> "Doing too many things at once almost guarantees none of them get done well."

> "'Do less but finish' always beats 'do more but leave half-done.'"

## Metadata

- **Source**: [Lecture 07 — Draw Clear Task Boundaries for Agents](https://walkinglabs.github.io/learn-harness-engineering/en/lectures/lecture-07-why-agents-overreach-and-under-finish/) (Learn Harness Engineering)
- **Cites**: Anthropic, "Effective harnesses for long-running agents"; OpenAI, "Harness Engineering"; David Anderson, *Kanban*; Steve McConnell, *Rapid Development*

## Relevant Wiki Pages

- [Feature Lists](../concepts/feature-lists.md) — where WIP=1, Scope Surface, and VCR are folded in as an extension of the same state-machine pattern
- [Session Continuity](../concepts/session-continuity.md)
- [Premature Completion Declaration](../concepts/premature-completion-declaration.md)
