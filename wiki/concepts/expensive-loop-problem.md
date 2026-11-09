---
tags: [data-n-ai, concept, llm, agents, benchmarks, harness-engineering]
sources: ["raw/data-n-ai/articles/2026-10-13-the-expensive-loop-problem.md"]
updated: 2026-11-09
---

# The Expensive-Loop Problem

**Cheap-loop tasks** have feedback that is quick, deterministic and cheap: unit tests, type checks, a failing repro, a compile error. **Expensive-loop tasks** have feedback that is slow, costly, noisy or scarce: a production load test, a data migration, a multi-hour training run, a product launch, a wet-lab experiment. Models are trained mostly in the first kind and are noticeably worse in the second. Coined in [The Expensive-Loop Problem](../sources/the-expensive-loop-problem.md) by [frmsaul](../entities/frmsaul.md).

## What expensive loops require (and cheap-loop training doesn't teach)

| Skill | What it is | Typical model failure |
|---|---|---|
| **Proxy management** | Pick cheap stand-ins for the costly target; notice when a proxy stops transferring | Skips proxies, or picks Goodhart-able ones and then overfits or cheats on them |
| **Theory building** | A causal model that generalises across experiments and prices their information value; improved by trying to falsify it | Reads noise as signal; confirmation bias; either discards too much theory or bloats it; doubles down |
| **Resource awareness** | Budget time/compute against expected information gain | Treats a 15-hour run like a 30-minute one; over-monitors; re-runs slow commands instead of saving output |
| **Error correction** | Diagnose failure at the right rung: *parameter → strategy → premise* | Only ever fixes parameters; locks into the first strategy; never questions the premise |

All four are the same underlying shortage: in cheap loops, the theory, the metric and the experiments are given by the environment, so the model never has to produce them.

## Why this matters for software engineering

Coding agents look strong because most day-to-day programming *is* cheap-loop. Trouble starts when a task quietly contains an expensive loop: performance work that needs real traffic, a migration that can't be cheaply rolled back, an ML pipeline whose run takes hours, a "does this feel right" UX decision, or anything gated on slow CI or a human. The agent will often treat it as cheap — running the full thing repeatedly, trusting a single green metric, or writing superficial tests it then grades itself on.

Two corollaries for this wiki's existing patterns:

- **[Ralph Loop](ralph-loop.md) and [Iterative Repair Loops](iterative-repair-loops.md) presuppose a cheap loop.** Re-running until tests pass is a good strategy only when each iteration costs seconds. Applied to a loop that costs hours or dollars, the same pattern burns the budget — which is the article's resource-awareness failure.
- **Verification failures are loop-cost failures.** The Mechanize GBA eval (models boot the game, see the title screen, declare success) is a concrete case of [Premature Completion Declaration](premature-completion-declaration.md): the real check was expensive (play the game), the cheap proxy (it boots) was substituted, and nothing flagged the substitution.

## Making an expensive loop cheaper

The article's own answer for humans, and the transferable one for harness design:

1. **Proxy ladder** — order cheaper stand-ins from least to most expensive and climb deliberately (unit → integration → staging/shadow traffic → canary → full rollout; sample → partition → full dataset; small model → large run).
2. **Wargames / simulators** — cheap environments that keep the *critical* details of the expensive loop. Hard to build, and fail where the simulator is wrong in ways that matter (robotics' sim-to-real gap).
3. **Information-gain budgeting** — estimate what an experiment will teach versus what it costs *before* running it.
4. **Strategy-level checkpoints** — force a parameter/strategy/premise diagnosis after repeated failures, rather than more tokens within the same approach (PostTrainBench: one mid-run strategy nudge beat the agent's continuation by up to 17.4%).
5. **Human-owned theory** — humans keep the causal model and choose which experiments are worth running; the agent executes and reports. Consistent with [Human-in-the-Loop](human-in-the-loop.md)'s finding that direction-level feedback beats artifact-level review.

## Relationship to other pages

- **[The Inference Gap](inference-gap.md)** — orthogonal and complementary. The Inference Gap asks *how much reasoning depth you actually receive per step*; the Expensive-Loop Problem asks *how costly it is to find out you were wrong*. A task can be high on both axes (a hard, slow-to-verify decision), which is where agents most need decomposition, executed evidence and human theory. Both converge on the same move: **take judgment out of the model's head and put it into mechanisms or humans.**
- **[Harness Evolution](harness-evolution.md)** — RRSI's evolve-set overfitting is Goodhart's law on a proxy (the evolve-set score); its noise floor, leakage screen and holdout are proxy-management tools.
- **[Premature Completion Declaration](premature-completion-declaration.md)** — shallow self-written tests are the verification-side face of "no theory, no falsification."
- **[Harness Engineering](harness-engineering.md)** / **[Agent Configuration Audit](agent-configuration-audit.md)** — put budgets, gates and kill criteria in hooks and tests rather than prose.
- **[Agent Security: Defense-in-Depth](agent-security-defense-in-depth.md)** — the article's safety section (reward hacking by strong cheap-loop, weak expensive-loop systems) is the capability-side counterpart to the "accidental meltdown" thread.

## Open Questions

- Does cheap-to-expensive generalisation exist ("escape velocity" at ~$10k loops), or must each price point be trained separately?
- Can wargame environments capture the critical details for software-engineering loops (deploys, migrations, production incidents)?
- Is the cheap/expensive split a useful discrete classification in practice, or just a continuum of feedback cost?

## Related Pages

- [Source: The Expensive-Loop Problem](../sources/the-expensive-loop-problem.md)
- [frmsaul](../entities/frmsaul.md)
- [Agentic Engineering: A General How-To Guide](../../outputs/data-n-ai/2026-11-09-agentic-engineering-how-to-guide.md)
- [The Inference Gap](inference-gap.md)
- [Agentic Engineering Under Variable Inference](agentic-engineering-under-variable-inference.md)
- [Ralph Loop](ralph-loop.md)
- [Iterative Repair Loops](iterative-repair-loops.md)
- [Human-in-the-Loop](human-in-the-loop.md)
- [LLM Limitations](llm-limitations.md)
