---
tags: [data-n-ai, synthesis, agents, llm, harness-engineering]
sources: ["raw/data-n-ai/articles/2026-09-19-the-inference-gap.md"]
updated: 2026-11-09
---

# Agentic Engineering Under Variable Inference

> **Status: inference, not source claim.** [The Inference Gap](../sources/the-inference-gap.md) offers almost no user-level advice (its recommendations target providers and regulators). Everything below was drawn in a Q&A discussion on 2026-11-09 by combining the article's findings with other wiki pages. Each point is a hypothesis; the source is a single user's data and the mechanism is unproven. Points marked **(wiki-supported)** are independently backed by other sources here.

**Premise:** if delivered reasoning is shallow, fragmented and drifts over time ([The Inference Gap](inference-gap.md), [Reasoning Dilution](reasoning-dilution.md)), then agentic engineering practice should (a) not depend on deep serial reasoning at every step, (b) not trust configured effort, and (c) be robust to bad days.

## General AI use

1. **Model name is an incomplete spec.** Pin model, version, prompt, effort *and* log the realized regime ([Inference Regime Observability](inference-regime-observability.md)).
2. **Evaluate in the deployed regime** and re-run periodically; vendor evals go stale.
3. **Budget for variance and measure cost per successful task** — hidden degradation appears as retries, bigger agent teams, extra review.
4. **Route by task difficulty.** If performance is log-linear in thinking, hard steps gain most from deep modes or fixed-budget models; easy steps do not.
5. **Diversify for critical work.** A weaker model you control (open-weight or self-hosted) may beat a stronger one delivered under a variable regime.
6. **Put regime transparency in procurement**: realized-vs-configured reasoning, change notification, remedies.

## Agentic software engineering

1. **Decompose to fit delivered depth.** Keep design/architecture decisions in a separate, short, focused step with only the relevant context; hand implementation a settled plan. Aligns with plan-mode-first practice in [Agents in Data Engineering](agents-in-data-engineering.md) **(wiki-supported)**.
2. **Keep context small and relevant**; prefer targeted reads, fresh sessions per task and short state artifacts over long scrollback ([Session Continuity](session-continuity.md), [Context Engineering](context-engineering.md)) **(wiki-supported)**.
3. **Prune instruction files; enforce critical rules mechanically.** Longer guideline files may lower adherence. Use hooks, linters, tests for hard rules ([Agent Configuration Audit](agent-configuration-audit.md)) **(wiki-supported)**.
4. **Verify with executed evidence.** Require test runs, command output and script-checked diffs; use a checker separate from the worker ([Premature Completion Declaration](premature-completion-declaration.md), [Ralph Loop](ralph-loop.md), [Feature Lists](feature-lists.md)) **(wiki-supported)**.
5. **Use fanout for breadth, not for hard reasoning.** Parallel agents suit independent modules, search and test generation. For a stubborn problem prefer one deep attempt: higher effort, clean context, narrow question.
6. **Instrument the harness**: reasoning tokens, zero-thinking share, longest span and invocations per turn; check these before rewriting prompts ([Harness Engineering](harness-engineering.md)).
7. **Make workflows idempotent and checkpointed** with deterministic gates, so a bad stretch costs a rerun, not corrupted state; keep a golden-task suite to detect bad days.
8. **Escalate by ladder**, not by loop: cheap model → high effort → fresh narrowed context → human. Repeated retries at a shallow regime mostly reproduce the failure.
9. **Spend human attention on design, invariants and security-sensitive decisions** ([Human-in-the-Loop](human-in-the-loop.md)); let the agent do mechanical work behind verification.
10. **Make cheap deterministic checks first-class** — types, tests, linters, contracts, schema validation ([Correctness Layer](correctness-layer.md), [Data Contracts](data-contracts.md)). They replace reasoning with mechanism.

## Highest-value, lowest-regret

Measurement (item 6 and the observability page) pays off whether or not the article's causal story holds: it turns "feels worse" into evidence.

## Caveats

- **Confound:** adaptive effort may rightly give simple steps little thinking; the harm may sit in a minority of hard turns. Establish *which* tasks degrade before restructuring workflows.
- **Untested:** none of these were validated against the article's data. Items marked wiki-supported are backed by other sources; the rest rely on the log-linear scaling extrapolation.
- **Incentives:** the author advocates disclosure and regulation; weigh interpretation separately from data.

## Related Pages

- [The Inference Gap](inference-gap.md)
- [Reasoning Dilution](reasoning-dilution.md)
- [Inference Regime Observability](inference-regime-observability.md)
- [Harness Engineering](harness-engineering.md)
- [Iterative Repair Loops](iterative-repair-loops.md)
- [Source: The Inference Gap](../sources/the-inference-gap.md)
