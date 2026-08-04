---
tags: [data-n-ai, source, agents, prompt-engineering, testing]
sources: [raw/data-n-ai/articles/2026-08-04-lecture-09-premature-completion.md]
updated: 2026-08-04
---

# Source: Lecture 9 — Preventing Agents from Declaring Victory Too Early

Course lecture from *Learn Harness Engineering* (walkinglabs.github.io), the same series as [Lecture 05](lecture-05-context-continuity.md) and [Lecture 08](lecture-08-feature-lists.md). Argues that agents are systematically overconfident about task completion, and that the harness — not the agent — must own the termination judgment.

## Key Claims

- **Agents are systematically overconfident.** Cites Guo et al. 2017 (ICML): modern neural networks report confidence significantly higher than actual accuracy. The article treats AI coding agents as inheriting this same miscalibration — they "feel" done well before they actually are.
- **Confidence calibration bias** is worse on complex multi-file tasks: the gap between self-reported completion confidence and actual quality is *positive and systematic*, not random noise.
- **Passing unit tests ≠ task complete.** Unit tests isolate the tested unit via mocks — which is exactly what makes them blind to cross-component failures:
  - **Interface mismatch**: a renderer passes a relative path, a preload script expects absolute; both sides' mocked unit tests pass; only end-to-end testing catches it.
  - **State propagation errors**: a DB migration changes schema but an ORM cache still holds old-schema entries — invisible to unit tests that always run in a fresh mock environment.
  - **Environment dependency**: code passes in a fully-mocked test environment but fails in the real one (config, network, service availability).
- **The three-layer termination check**: (1) syntax/static analysis — lowest cost, least information, but mandatory; (2) runtime behavior verification — tests actually executing, app reaching a ready state; (3) system-level confirmation — end-to-end/integration tests, user-scenario simulation. All three must pass; layer *N* is not attempted until layer *N-1* passes.
- **Verification-validation dual gate**: verification checks the code implements specified behavior; validation checks system-level behavior meets end-to-end requirements. Both gates required.

## "Refactoring While We're at It" Is Poison to Completion Judgment

A named failure pattern specific to Claude Code (per the article): the agent starts refactoring, optimizing performance, or improving style **before** core functionality has passed verification. The article's framing of why this is actively harmful, not just wasted effort: refactoring shifts the boundary between verified and unverified code, potentially breaking code paths that were previously *implicitly* correct — you lose the baseline you were trying to confirm. It applies Knuth's "premature optimization is the root of all evil" to the agent harness context, and prescribes a **completion priority constraint**: verify functional correctness first, then performance, then style — no refactoring permitted until core functionality is verified.

## Systematic Bias in Self-Evaluation (Worker/Checker Separation)

Anthropic's 2026 research (per the article): when an agent evaluates its own work, it systematically rates it more positively than a human observer would — especially on subjective tasks (design aesthetics), but the bias degrades performance even on tasks with objectively verifiable outcomes. Because the same model both generates and evaluates, it is structurally inclined to be generous to itself.

**The fix is architectural, not a "be more objective" prompt**: separate the worker from the checker. An independent evaluation agent tuned to be deliberately nitpicky outperforms self-evaluation.

Cited experiment (same model, same prompt — "build a 2D retro game editor," Opus 4.5):

| Architecture | Runtime | Cost | Core features working? |
|---|---|---|---|
| Single agent (bare run) | 20 min | $9 | No — game entities unresponsive to input |
| Three agents (planner → generator → evaluator using Playwright click-testing) | 6 hours | $200 | Yes — fully playable |

## Practical Prescriptions

1. **Externalize termination judgment** — spell out a "Definition of Done" in CLAUDE.md/AGENTS.md as an ordered, gated checklist (unit → integration → e2e, no skipping ahead on failure).
2. **Actionable error feedback** (OpenAI/Codex pattern) — error messages must include repair instructions, not just failure notices. `"Test failed: POST /api/reset-password returned 500. Check that the email service config exists in environment variables..."` rather than `"Test failed."` Lets the agent self-correct without human intervention.
3. **Capture runtime signals** — did the app reach a ready state; did critical paths execute; were side effects (DB writes, file ops) correct; were temp resources cleaned up.

## Real-World Case

Password-reset feature: agent modifies schema, writes endpoint, adds email template, unit tests all green, declares done. Actual state: end-to-end flow never run, DB migration failed partway leaving inconsistent schema, email service config missing. Harness intervention (starting the app, running the full flow, checking DB consistency) caught all three defects within the session — claimed savings of 5–10x versus post-hoc discovery.

## Sources Cited by the Article

- Guo et al., [On Calibration of Modern Neural Networks](https://arxiv.org/abs/1706.04599) (ICML 2017)
- Anthropic: [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- Anthropic: [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- OpenAI: [Harness Engineering](https://openai.com/index/harness-engineering/)
- Myers, *The Art of Software Testing*

## Metadata

- Source: [Lecture 9, Learn Harness Engineering](https://walkinglabs.github.io/learn-harness-engineering/en/lectures/lecture-09-why-agents-declare-victory-too-early/)
- Type: course lecture (teaching material, synthesizes an ICML paper + Anthropic/OpenAI harness-engineering posts)
- Ingested: 2026-08-04

## Related Pages

- [Premature Completion Declaration](../concepts/premature-completion-declaration.md)
- [Feature Lists](../concepts/feature-lists.md)
- [Ralph Loop](../concepts/ralph-loop.md)
- [Human-in-the-Loop](../concepts/human-in-the-loop.md)
