---
tags: [data-n-ai, concept, llm, agents, harness-engineering, benchmarks]
sources: ["raw/data-n-ai/articles/2026-09-19-the-inference-gap.md"]
updated: 2026-11-09
---

# Inference Regime Observability

The practice of measuring *what an LLM call actually delivered* — not just which model and effort setting you requested. It is the user-side counterpart to the disclosures [The Inference Gap](../sources/the-inference-gap.md) asks providers to make. The first half (provider reporting) is the article's; the second half (user-side practice) is **inference drawn in discussion, not claimed by the source**.

## What the article asks providers to report

- realized reasoning tokens per invocation and per user-facing turn
- maximum uninterrupted reasoning span
- share of invocations with zero thinking
- thinking distributions by effort level (not only averages)
- configured ceilings versus realized consumption
- changes in those distributions over time

The author notes the trend is the opposite: providers have moved from stating fixed thinking budgets to reporting effort labels, costs or total-token budgets, so the performance-bearing resource is *less* observable.

## User-side practice (inferred)

1. **Log per call**: reasoning tokens, zero-thinking flag, invocations per turn, longest span, effort setting, harness version, timestamp. Where the API hides reasoning tokens, log usage fields and derive what you can.
2. **Track a few robust statistics over time**: median and P90 thinking per invocation, zero-thinking share, thinking per input token. Alert on shifts — the article's strongest signal was a multi-day trough where median invocation thinking hit zero.
3. **Keep a golden-task suite** (small, deterministic pass/fail) and rerun it on a schedule and when behaviour "feels worse". Distinguishes a bad regime day from a prompt regression.
4. **Evaluate through the production path**: same harness, effort, context size and load as real work, not a vendor-run demo.
5. **Measure cost per *successful* task**, not per token; hidden degradation shows up as retries and larger agent teams.
6. **Check logs before rewriting prompts** when quality drops.

## Limits

- A low thinking count is not automatically a defect: adaptive allocation may rightly spend little on trivial tool-call steps. Condition on task difficulty (e.g. golden tasks, or turn-level hardness) before inferring starvation.
- Sampling bias: the article's data are one user's; others' regimes may differ.

## Related Pages

- [The Inference Gap](inference-gap.md)
- [Reasoning Dilution](reasoning-dilution.md)
- [Agentic Engineering Under Variable Inference](agentic-engineering-under-variable-inference.md)
- [Harness Engineering](harness-engineering.md) — telemetry is a harness responsibility
- [Data Quality Observability](data-quality-observability.md) — the same "measure the delivered thing, not the configured thing" idea for data
- [Source: The Inference Gap](../sources/the-inference-gap.md)
