---
tags: [data-n-ai, source, llm, agents, benchmarks, harness-engineering]
sources: ["raw/data-n-ai/articles/2026-09-19-the-inference-gap.md"]
updated: 2026-11-09
---

# Source: The Inference Gap (@Lon)

**Origin:** X article by [@Lon](../entities/lon.md)
**URL:** https://x.com/Lon/status/2101034933284417614
**Published:** 2026-09-19 · **Clipped:** 2026-11-09
**Raw:** `raw/data-n-ai/articles/2026-09-19-the-inference-gap.md`

## Summary

A forensic, single-user study of what [Anthropic](../entities/anthropic.md)'s Fable 5 actually *did* behind the "xhigh" and "max" effort settings in Claude Code. After perceiving a sharp quality drop following Fable 5's permanent subscription availability (July 20, 2026), the author built a semantically aware proxy to capture wire logs and analysed ~43K model invocations across 65 days. They expected to find a nerfed or rerouted model. Instead: **the model identity was unchanged, but the inference regime delivered behind it was small, fragmented and drifting downward.** The gap between that and the regimes behind headline benchmarks is **the Inference Gap**. See [The Inference Gap](../concepts/inference-gap.md) for the concept.

## Dataset

Fable 5 at xhigh/max effort; Jul 1 – Sep 7, 2026; 65 usage days, 3 machines, 2 subscription accounts, 25 project groups, 213 sessions, 48 Claude Code versions (2.1.197–2.1.263); 43,261 invocations (43,007 with quantified thinking) and 7,853 complete turns. Definitions: a **turn** is one user request ending in a terminal response; an **invocation** is one API call within it; a turn's thinking is the sum over its invocations. Invocation thinking = an *uninterrupted* reasoning sequence; turn thinking = a possibly fragmented total, and the two are not interchangeable.

## Key Claims and Numbers

1. **Higher effort regularly produces little thinking.** Median invocation: **123** thinking tokens; **39.2%** of invocations had *none*. Median turn: ~2,028; 6% of turns had none. Anthropic's docs say xhigh "always thinks deeply" and max "always thinks". 96.3% of invocations stayed under 4,096 thinking tokens.
2. **Thinking fragments as turns grow** ([Thinking Fragmentation](../concepts/reasoning-dilution.md#thinking-fragmentation)). At 131K turn-level thinking tokens the longest single invocation holds only ~12%; the rest is spread over hundreds of invocations. A "32K thinking" turn is rarely a 32K serial chain.
3. **Reasoning dilution** ([Reasoning Dilution](../concepts/reasoning-dilution.md)). 32× more incoming text (4K→131K) gives only ~3.5× more median thinking; below one thinking token per input token from ~4.5K input. The author links this anecdotally to more inconsistent designs, unfaithful long-horizon completion, and *lower* guideline adherence as instruction files grow.
4. **The regime is non-stationary and declining.** August median thinking was 22–51% below July depending on weighting (turn 21.9%, day 23.1%, session 35.1%, project 46.2%, invocation 50.6%). Around Aug 22–23, median invocation thinking hit zero for ~a week. Partial recovery near Sep 1, then another decline. A held-out-project ensemble test found a **shared temporal component** consistent with an external process — mechanism (capacity, routing, policy, adaptive effort) unidentified.
5. **The benchmark gap.** Back-solved benchmark thinking for ARC-AGI-2 / HLE runs: ~20–50K tokens per invocation (blended ~24.4K at xhigh, ~32.1K at max). Median delivered thinking is **~230× (≈8 doublings) lower**; P75 ~38× short, P90 ~13× short. Benchmark score is roughly **log-linear in thinking compute**; extrapolating the low–med slope implies ARC-AGI-2 ≈1.5% at P50 delivery vs ~88–89% at benchmark settings (HLE 38% vs ~57–58%). These are extrapolations, not re-runs.
6. **Fanout is not serial depth.** A 48-invocation benchmark agent run had 179K reasoning tokens with its five biggest invocations at 18–31K and *no* zero-thinking calls; the corpus's largest turn (145K, 344 invocations) had none comparable, and every one of 105 turns with ≥48 invocations contained zero-thinking calls. Best-of-N, subagent fleets and longer runs add breadth, not missing sequential depth, and can cost more.
7. **Two frontiers.** The *model frontier* (achievable under a favourable regime) versus the *accessible frontier* (what a user can reliably elicit). Cheaper tokens and stronger models can coexist with a rising cost of approaching the demonstrated frontier.

## Thinking-in-Claude-Code Timeline (author's source analysis, 500 versions)

Fixed budgets of 4K/10K/31,999 (Mar 2025) → 4K/10K tiers removed (Sep 2025, v2.0.0) → adaptive thinking for Opus 4.6 (Feb 2026) → `ultrathink` numeric effect removed then returned as prompt steering only (Feb–Mar 2026) → undocumented 127,999 fixed path (Mar 2026) → Opus 4.7 introduces xhigh and goes adaptive-only, no fixed-budget path (Apr 2026). The trend: **users lost direct control of the thinking budget**.

## Recommendations (the author's)

Aimed at providers/regulators, not users: report realized reasoning tokens per invocation and per turn, maximum uninterrupted span, zero-thinking share, distributions by effort level, configured ceilings vs realized consumption, and changes over time; cost-recovery mechanisms for avoidable failures; frame under-deliberation as a safety and liability matter. Reframe "was it nerfed?" as "under what inference regime was it delivered?"

## Notable Quotes

> "The same advertised effort setting did not correspond to a stable amount of delivered thinking over time."

> "Ten million task-level tokens are not ten million uninterrupted reasoning tokens. Parallel sampling is not serial depth. A configured ceiling is not realized consumption."

> "The model is now only half the system. The inference regime determines how much of the frontier you get to see."

## Caveats

- **n=1**: one author, two accounts, Claude Code on Fable 5 only; not shown to generalize across users or harnesses.
- **Mechanism unproven.** Adaptive effort logic may legitimately give tool-call steps little thinking; the problem may be concentrated in a minority of hard turns. The article cannot separate this from capacity throttling.
- **Benchmark thinking counts are reconstructed** from cost/usage data (providers rarely disclose them); score impacts at delivered levels are log-slope extrapolations.
- **Advocacy framing.** The author is arguing for disclosure and regulation; data and interpretation should be weighed separately.
- Collection code unreleased. The article's scenario (Fable 5, Fable 5.1, Opus 5) post-dates much of the other material in this wiki; treat model details as the article's claims.

## Operational Takeaways

The article gives almost no user-level advice. The operational implications drawn from it in discussion are filed separately, clearly marked as inference: [Agentic Engineering Under Variable Inference](../concepts/agentic-engineering-under-variable-inference.md).

## Related Pages

- [The Inference Gap](../concepts/inference-gap.md)
- [Reasoning Dilution](../concepts/reasoning-dilution.md)
- [Inference Regime Observability](../concepts/inference-regime-observability.md)
- [Agentic Engineering Under Variable Inference](../concepts/agentic-engineering-under-variable-inference.md)
- [Agentic Engineering: A General How-To Guide](../../outputs/data-n-ai/2026-11-09-agentic-engineering-how-to-guide.md)
- [Source: The Expensive-Loop Problem](the-expensive-loop-problem.md) — companion article on loop cost
- [Anthropic](../entities/anthropic.md)
- [Context Engineering](../concepts/context-engineering.md)
- [Agent Configuration Audit](../concepts/agent-configuration-audit.md)
- [Lon (@Lon)](../entities/lon.md)
