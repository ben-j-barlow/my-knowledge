---
tags: [data-n-ai, source, agents, prompt-engineering, harness-engineering]
sources: ["raw/data-n-ai/papers/2026-09-25-rrsi-regularized-recursive-self-improvement-of-agent-harnesses.pdf"]
updated: 2026-10-02
---

# Source: RRSI — Regularized Recursive Self-Improvement of Agent Harnesses

Peng Xia, Rujun Han, Zifeng Wang, Yanfei Chen, Yufan Zhuang, Yoonho Lee, Chengsong Huang, Han Yu, Zhongying CuiZhu, Yifei Ming, Huaxiu Yao, Burak Gokturk, Tomas Pfister, Chen-Yu Lee. Google Cloud AI Research / UNC-Chapel Hill / Stanford / WashU. arXiv:2609.24972v2, 2026-09-25. Code: github.com/google-research/rrsi.

## Core Problem

An LLM agent's capability is "largely magnified by its harness" — the prompts, control flow, tool interfaces, memory, and context management wrapped around a frozen backbone model. Recent methods automate harness design by having an LLM iteratively propose and select edits to the harness based on feedback from a fixed **evolve set** of tasks — a practical form of **recursive self-improvement (RSI) at the agent-system level**, distinct from RSI on model weights.

The paper's central finding: this recursive evolution **overfits**. Gains on the evolve set can be large while gains on out-of-distribution (OOD) benchmarks shrink or vanish entirely — some prior methods (AHE, TTHE) finish *below* the unevolved starting harness on held-out tasks despite solid evolve-set gains (Figure 1a in the paper: a scatter of evolve-set gain vs. OOD gain where most prior methods sit near or below the 1:1 transfer line).

## Why It Overfits

Three coupled failure modes drive the evolve-to-transfer gap:
- **Benchmark-specific fitting** — edits encode patterns specific to the evolve set's tasks.
- **Noise chasing** — candidates are favored by evaluation noise rather than real mechanism improvements.
- **Complexity accumulation** — the harness accrues machinery that raises the evolve-set score without improving the underlying agent mechanism.

## RRSI: Regularizing the Evolution Loop

RRSI keeps the harness edit space fully open (any component — prompts, control flow, config, tools, skills, memory, subagents — can still be modified, added, or removed) but regularizes the *search trajectory* through that space, on both the proposal and selection sides. The paper explicitly frames each regularizer as a *qualitative* analogy to a classical ML regularization technique, not an actual norm-penalized objective (harness components aren't a continuous parameter vector).

### Proposal-Side Regularization (controls how search capacity is used)
- **Annealed update sparsity (L0-style)** — caps how many independently-attributable edits one candidate may bundle, via a budget that decreases over rounds (`b_t`, Eq. 4): early rounds allow broader multi-edit candidates to discover new mechanisms, later rounds force small, attributable, single-mechanism changes.
- **Evidence-aware credit assignment** — every evaluated candidate's component, hypothesis, score/cost delta, and accept/reject outcome are recorded; the proposer conditions on this full history so it doesn't keep re-testing hypotheses already falsified.
- **Structured exploration** — when progress stalls (no improvement beyond the noise band over a window of rounds), a portion of the proposal budget is redirected to components not yet exercised, rather than continuing to rewrite the same handful of prompts.

### Selection-Side Regularization (controls which gains become permanent state)
- **Leakage screening** — a critic rejects candidates that hardcode task names, entity names, task-specific values/answers, or otherwise encode benchmark-specific logic, *before* evaluation (so a leaking candidate never gets the inflated score that would make it attractive later).
- **Noise-adjusted performance floor (stability-aware acceptance)** — a candidate must beat a noise band `δ` (calibrated by repeatedly re-evaluating the unchanged base harness) over the best score seen so far, preventing the search from "walking downhill" through a sequence of individually-noise-sized regressions.
- **Complexity-aware acceptance (Ridge/L2-style)** — for gains that clear the noise band, additional inference cost (policy tokens) must be justified by the size of the measured gain (`ΔC ≤ β0 + β1·ΔS`); gains within the noise band use a separate shaped admissibility rule combining score, cost, and structural novelty.
- **Structural pruning (Lasso/L1-style)** — components that have been exercised but produced no strictly positive measured gain within a recent pruning window are reported to the proposer as deletion targets; mechanisms must keep earning their place rather than persisting by default.

## Experimental Setup

Evaluated across 8 benchmarks in 3 domains, each with an evolve set and held-out/OOD splits: **Coding** (Terminal-Bench 2.1 evolve → SWE-bench Verified OOD), **Agentic workspace** (Harvey LAB evolve + in-distribution held-out → JobBench, GDPval, APEX-Agents OOD), **Engineering design** (EngDesign evolve → Frontier-Eng OOD, graded by frozen simulators/testbenches rather than an LLM judge — ruling out "gaming the judge" as an explanation for transfer). Policy frozen at Claude Opus 4.8 for the main results; Gemini 3.5 Flash used to test policy-independence. Baselines: Meta-Harness, AHE, TTHE, HarnessX — four recent unregularized harness-evolution methods, all started from the same base harness `H0` under the same candidate budget.

## Key Results

- RRSI gains up to **14.1 points** on the split it evolves against and up to **4.7 points on out-of-distribution benchmarks**, while unregularized evolution and prior methods either transfer little of their evolve-set gain or regress below `H0` on OOD splits.
- No held-out split regresses anywhere under RRSI — the specific failure mode a memorizing harness produces.
- **Deterministic-grading check**: because Harvey LAB/JobBench/GDPval use an LLM judge, a harness could in principle improve its score by gaming the judge rather than doing better work. EngDesign/Frontier-Eng use frozen simulators/testbenches instead (deterministic, pass/fail against physical constraints), and the OOD gains survive unchanged there — evidence the transfer is real, not judge-exploitation.
- **Ablation**: removing acceptance-side regularizers alone raises evolve-set score (90.5→91.5) but drops OOD average (43.6→41.0) and raises token cost by ~50%. Removing both regularizer groups gives the *highest* evolve-set score of any arm (92.8) but OOD average falls to 40.3 — within a point of the unevolved harness — at 3.80M tokens/trial vs. RRSI's 2.42M.
- **Policy-independence**: run independently with Claude Opus 4.8 and Gemini 3.5 Flash, RRSI improves both the evolve set and SWE-bench Verified OOD under each, so the benefit isn't an artifact of one backbone.
- **Cross-model transfer**: a harness evolved under Gemini 3.5 Flash, evaluated unchanged under a smaller, never-searched-with model (Gemini 3.1 Flash Lite), still raises Terminal-Bench 2.1 accuracy 11.2→14.6 (+30.4% relative) — the harness is a program, not a set of weights, and its improvements aren't tied to the policy that searched for them.
- **Efficiency**: RRSI produces the lightest harness of any evolved arm — fewer policy tokens/trial and fewer steps/trial than all four baselines, while sitting strictly in the region that dominates on cost *and* OOD transfer (Figure 4a).

## Qualitative Case Study (Appendix E)

Concrete accept/reject examples: a bounded pre-completion verification check was accepted (+3.93 evolve-set points, cleared the noise band); a similar-looking candidate with a smaller measured gain and higher inference cost was rejected by the cost rule despite a positive score change (+1.69 points, +26.1% cost); a candidate that *reduced* cost was still rejected because its score fell below the noise-adjusted floor (−2.81 points, despite −13.6% cost) — lower cost alone cannot compensate for a regression. The takeaway: specificity, evaluation stability, and cost jointly gate whether a change is retained — not score alone.

## Limitations (per paper)

Frozen-backbone setting only (no joint weight+harness evolution studied); still relies on a finite evolve set and several regularization hyperparameters, so effectiveness may depend on feedback-signal quality and search budget; broader validation needed across substantially different agent architectures, tool ecosystems, and longer-running self-improvement processes.

## How This Extends the Existing Wiki

This is the most rigorous empirical confirmation yet of a pattern already recurring across several unrelated sources in this wiki: **letting a system auto-generate or auto-evolve its own scaffolding, without some form of curation/regularization, looks good in-sample and degrades out-of-sample.** See the new cross-topic connection logged in [Overview](../overview.md) and the [Harness Engineering](../concepts/harness-engineering.md) concept this paper extends with a concrete, measured account of what happens when a Harness is allowed to *evolve itself* rather than being hand-designed.

## Source

[raw/data-n-ai/papers/2026-09-25-rrsi-regularized-recursive-self-improvement-of-agent-harnesses.pdf](../../raw/data-n-ai/papers/2026-09-25-rrsi-regularized-recursive-self-improvement-of-agent-harnesses.pdf)
