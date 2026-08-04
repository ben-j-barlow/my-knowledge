---
tags: [data-n-ai, concept, agents, prompt-engineering, testing]
sources: [wiki/sources/lecture-09-premature-completion.md]
updated: 2026-08-04
---

# Premature Completion Declaration

The failure mode where an agent asserts a task is done while unmet correctness requirements remain — because it judges completion from local, code-level confidence ("I wrote the code, tests are green") rather than global, system-level verification ("the feature actually works end-to-end"). The fix is to externalize the termination judgment to the harness, using runtime evidence instead of the agent's self-report.

The behavioral root cause is not agent-specific carelessness: **modern neural networks are systematically overconfident** (Guo et al., ICML 2017 — reported confidence exceeds actual accuracy). Coding agents inherit the same miscalibration, and it worsens on complex, multi-file tasks where the gap between self-reported confidence and actual quality becomes consistently positive.

---

## Why Passing Unit Tests Isn't Enough

Unit tests isolate the unit under test via mocks — the exact property that makes them blind to cross-component failures:

- **Interface mismatch** — two components' contracts silently disagree (e.g. one passes a relative path, the other expects absolute); each side's mocked unit test passes independently.
- **State propagation errors** — a schema migration invalidates a cache layer that unit tests never see, because unit tests always run against a fresh mock, never accumulated real state.
- **Environment dependency** — code passes against mocks but fails against real config, real network latency, or a real unavailable service.

Information is lost at every hop from task spec → implementation → runtime behavior; each skipped verification layer compounds the gap between "looks done" and "is done."

## The Three-Layer Termination Check

| Layer | Checks | Cost/Information |
|---|---|---|
| 1. Syntax & static analysis | Lint, typecheck | Lowest cost, least information — necessary but not sufficient |
| 2. Runtime behavior verification | Tests actually execute, app reaches a ready state, critical paths run | Core evidence of completion — not just written, but runnable |
| 3. System-level confirmation | End-to-end tests, integration validation, user-scenario simulation | Last line of defense — not just runnable, but correct |

Gating rule: don't attempt layer *N* until layer *N-1* passes. This is the **verification-validation dual gate** — verification confirms code implements the specified behavior; validation confirms system-level behavior meets end-to-end requirements. Both are required; neither substitutes for the other.

## "Refactoring While We're at It" Is Poison to Completion Judgment

A specific, named anti-pattern (observed in Claude Code): the agent starts refactoring, optimizing performance, or improving style **before core functionality has passed verification.**

Why this is actively harmful rather than merely premature: refactoring shifts the boundary between verified and unverified code. Code paths that were implicitly correct (because they hadn't been touched since the last known-good state) are now back in question, and the agent has no fresh verification for them — the very thing it was trying to establish gets undermined by the "improvement." This is Knuth's "premature optimization is the root of all evil," applied not to human engineering taste but to a harness state machine: the risk isn't wasted effort, it's a state-tracking failure that reopens correctness questions.

**Completion priority constraint**: verify functional correctness → then performance → then style. No refactoring is permitted until core functionality is verified. This is a harness rule, enforced the same way [Feature Lists](feature-lists.md) enforce pass-state gating — not a style preference left to the agent's discretion.

## Self-Evaluation Is Structurally Biased — Separate Worker from Checker

Anthropic's 2026 research: when the same agent that produced work is asked to evaluate it, it systematically rates it more positively than a human observer would. Most severe on subjective judgment calls (design aesthetics: "is this layout polished?") but still degrades outcomes on objectively verifiable tasks. The bias is structural — the same model generating and evaluating is inherently inclined to be generous with itself — so **prompting for more objectivity does not fix it.**

The fix: an architecturally separate, independently-tuned evaluator — deliberately "nitpicky" — replacing self-assessment.

Cited experiment (identical model — Opus 4.5 — identical prompt, "build a 2D retro game editor"):

| Architecture | Runtime | Cost | Core features working? |
|---|---|---|---|
| Single agent (bare run) | 20 min | $9 | No — game entities unresponsive to input |
| Planner → generator → evaluator (Playwright click-testing) | 6 hours | $200 | Yes — fully playable |

The only variable was harness structure, not model capability.

## Practical Prescriptions

1. **Externalize the definition of done** in CLAUDE.md/AGENTS.md as an ordered, gated checklist:
   ```
   ## Definition of Done
   - Feature complete = end-to-end verification passed, not "code is written"
   - Required verification levels:
     1. Unit tests pass
     2. Integration tests pass
     3. End-to-end flow verification passes
   - Do not proceed to level 2 if level 1 fails
   - Do not proceed to level 3 if level 2 fails
   ```
2. **Actionable error feedback** (OpenAI/Codex pattern) — failures must carry repair instructions, not just a failure notice: `"Test failed: POST /api/reset-password returned 500. Check that the email service config exists in environment variables. Template should be at templates/reset-email.html."` — lets the agent self-correct without a human round-trip.
3. **Capture runtime signals as the actual evidence base** — did the app reach a ready state; did critical feature paths execute; were side effects (DB writes, file operations) correct; were temp resources cleaned up. These, not the agent's confidence, are what the harness gates on.

---

## Relationship to Other Patterns

- [Feature Lists](feature-lists.md) — the data-structure implementation of the same principle: a feature can't be marked `passing` by the agent's own judgment, only by a successful verification-command run. Premature completion declaration is exactly the failure feature-list pass-state gating exists to prevent.
- [Ralph Loop](ralph-loop.md) — addresses the same root failure (the agent cannot be trusted to self-declare done) via a different mechanism: an external test gate re-prompts with the same goal until tests pass, rather than a layered termination check the agent must satisfy once.
- [Human-in-the-Loop](human-in-the-loop.md) — the worker/checker separation is a *fully automated* analogue of HITL's "independent reconciliation" pattern (two agents process independently, a separate step compares). Both replace a single agent's self-report with an independent second opinion; HITL keeps that second opinion human, this pattern makes it a dedicated evaluator agent.
- [Session Continuity](session-continuity.md) — verification records (which tests passed/failed and why) are one of the state-persistence artifacts session continuity recommends carrying across sessions; premature completion declaration is what happens when that record is never actually generated in the first place.

## Related Pages

- [Feature Lists](feature-lists.md)
- [Ralph Loop](ralph-loop.md)
- [Human-in-the-Loop](human-in-the-loop.md)
- [Session Continuity](session-continuity.md)
- [Source: Lecture 9 — Preventing Agents from Declaring Victory Too Early](../sources/lecture-09-premature-completion.md)
