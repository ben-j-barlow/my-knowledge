---
tags: [data-n-ai, source, agents, prompt-engineering, observability]
sources: [raw/data-n-ai/articles/2026-09-11-lecture-11-runtime-observability.md]
updated: 2026-09-11
---

# Source: Lecture 11 — Making the Agent's Runtime Observable

Learn Harness Engineering course, lecture 11. Argues reliability is fundamentally an **evidence problem**: without observability, agent decisions, evaluations, and retries all become guesswork. Introduces two layers — runtime observability and process observability — and walks through Anthropic's three-agent (planner/generator/evaluator) architecture experiment as the worked example.

## Key Claims

- **Four costs of missing observability**: can't distinguish "correct" from "looks correct" (code review shows what was written, runtime tracing shows what actually ran); evaluation becomes non-reproducible mysticism (different evaluators score the same output differently with no shared rubric); retries become blind guesses (wrong-direction fixes burn tokens); session handoff becomes an information cliff — Anthropic's observation: **missing observability wastes 30–50% of session time on redundant re-diagnosis**.
- **Two layers, both required**:
  - *Runtime observability* — system-level signals (logs, traces, process events, health checks, resource utilization, full error context). Answers "what did the system do."
  - *Process observability* — visibility into harness decision artifacts (plans, sprint contracts, scoring rubrics, acceptance criteria). Answers "why should this change be accepted."
- **Why agents can't self-report their way to this**: agents don't know what they don't know (they log what they *think* matters, which is usually insufficient); log formats vary session to session, blocking systematic analysis; process observability (contracts, rubrics) is a structured artifact that logging alone can't produce — it needs harness-level scaffolding.
- **Sprint contract**: a short-term agreement negotiated *before* coding starts — scope, verification standards, explicit exclusions. Front-loads alignment between generator and evaluator so the evaluator doesn't reject work for reasons that were foreseeable.
- **Evaluator rubric**: converts "is it good" into dimension-by-dimension structured scoring (e.g. code correctness / architecture compliance / test coverage, graded A–D), making evaluation reproducible across evaluators.
- **Illustrative comparison** (Claude Code, "add dark mode"): without observability — vague plan, vague rejection ("doesn't feel right"), 3–4 blind retry rounds, ~45 min, barely acceptable. With sprint contract + rubric + runtime traces — one iteration, specific evidence-backed feedback ("contrast 2.1:1, needs 4.5:1 per WCAG AA"), ~15 min. **3x efficiency**, observability the only variable changed.
- **Anthropic's three-agent DAW-building experiment** (March 2026; "build a browser-based DAW using the Web Audio API"): Planner → Generator (implements sprint-by-sprint against negotiated contracts) → Evaluator (uses Playwright MCP to interact with the running app like a real user, scores across product depth / functionality / visual design / code quality with hard per-dimension thresholds). Full run: 3h50m, $124.70, three build/QA rounds. QA feedback was specific and actionable (e.g. "clips can't be dragged, no instrument UI panel, no visual effects editor" — not "it doesn't feel right"). The evaluator's judgment itself needed iteration: early versions found real issues, then talked themselves into dismissing them — fixed by reading evaluator logs, finding divergence points from human judgment, and updating the QA prompt.
- **Design principle for the planner**: deliberately kept high-level ("be bold in scope," "focus on product context ... rather than detailed technical implementation") — premature granular specification, if wrong, cascades downstream; better to constrain deliverables and let the agent find its own implementation path.
- Recommends OpenTelemetry as the standardization layer: one trace per harness session, one span per task, sub-spans per verification step, so observability data plugs into standard tooling (Jaeger, Zipkin).

## Notable Quotes

> "Without observability, agents make decisions under uncertainty, evaluations become subjective judgments, and retries become blind wandering."

> "Runtime signals explain 'what happened,' process artifacts explain 'why it was done this way.'"

## Metadata

- **Source**: [Lecture 11 — Making the Agent's Runtime Observable](https://walkinglabs.github.io/learn-harness-engineering/en/lectures/lecture-11-why-observability-belongs-inside-the-harness/) (Learn Harness Engineering)
- **Cites**: Anthropic, "Harness design for long-running application development"; Charity Majors, *Observability Engineering*; Google, Dapper (Sigelman et al.); Google, *Site Reliability Engineering*

## Relevant Wiki Pages

- [Data Quality Observability](../concepts/data-quality-observability.md) — where the runtime/process observability distinction and sprint-contract pattern are folded in as the agent-harness analogue of pipeline observability
- [Premature Completion Declaration](../concepts/premature-completion-declaration.md) — the failure mode this lecture's evaluator rubric is designed to prevent
- [Feature Lists](../concepts/feature-lists.md)
