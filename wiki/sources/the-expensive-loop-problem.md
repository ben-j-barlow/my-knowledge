---
tags: [data-n-ai, source, llm, agents, benchmarks, harness-engineering]
sources: ["raw/data-n-ai/articles/2026-10-13-the-expensive-loop-problem.md"]
updated: 2026-11-09
---

# Source: The Expensive-Loop Problem (frmsaul)

**Origin:** LessWrong post by [frmsaul](../entities/frmsaul.md)
**URL:** https://www.lesswrong.com/posts/2mStxuNDMdaWdyHu6/the-expensive-loop-problem
**Published:** 2026-10-13 · **Clipped:** 2026-11-09
**Raw:** `raw/data-n-ai/articles/2026-10-13-the-expensive-loop-problem.md`

## Summary

An essay arguing that LLMs are excellent where feedback is **quick, deterministic and cheap** ("cheap-loop" domains: anything computer-checkable) and weak where feedback is **slow, costly or scarce** ("expensive-loop" domains: science, business, policy, medicine, AI R&D itself). The likely cause is training: labs can cheaply assign reward in cheap-loop domains, so models never learn the skills expensive loops demand. See [The Expensive-Loop Problem](../concepts/expensive-loop-problem.md) for the concept and its application to this wiki.

## Key Claims

1. **Proxy selection.** Expensive loops are navigated with ladders of cheaper proxies (cells → mice → human trials; small → large training runs; script read → animatic → test screening). Models either skip proxies and burn expensive experiments, or pick easily Goodharted ones — and, when given a proxy, overfit it, sometimes cheating. Proxies also fail when optimised (Goodhart) and capture only the measurable (McNamara fallacy).
2. **Theory building.** A theory is a causal model that lets you generalise across experiments and price the *information value* of the next one (Maxwell, germ theory, Moneyball, scaling laws). Cheap-loop tasks hand you the theory in the task description. Models read noise as signal, confirm rather than falsify, and respond to falsification unpredictably — either discarding too much of the theory or growing it without Occam pressure — then double down on whichever failure mode they started in.
3. **Resource awareness.** Models are either too conservative (often compute) or too wasteful (often time):
   - PostTrainBench: one run spent **61% of its budget on evaluation, 3.6% on RL training**; another spent ~72% of wall-clock diagnosing throughput, leaving ~83 minutes to train.
   - The `tail -5` → `tail -30` → `grep` pattern: re-running a 5-minute command instead of saving output to a file once.
   - An Amazon study of production ML systems: the agent "treats a 15-hour multi-GPU run as no more consequential than a 30-minute ablation"; it has "no model of information gain relative to compute expenditure".
   - Context is the one resource models do conserve — probably because it is scarce even in cheap-loop training (footnote 3).
4. **Error correction.** Failures sit on a three-rung ladder: *parameter* → *strategy* → *premise*. Cheap-loop training only exercises the bottom rung. PostTrainBench agents "lock into a default strategy before any experimental evidence arrives"; extra tokens buy "denser refinement within the committed strategy but not a better one"; **a single mid-run instruction to change strategy beat the agent's own continuation by up to 17.44%**. Ege Erdil (Mechanize) and the Mechanize GBA-emulator eval: models write their own shallow tests, and when asked to verify by playing games, most never play — they see the title screen and call it done.
5. **Humans are not immune.** Ancestral environments were expensive-loop; modern schooling and work train cheap-loop habits. Reward hacking, confirmation bias, the McNamara and ludic fallacies are old human failures; the Great Leap Forward, the subprime crisis and the Maginot Line are cited as cheap-loop thinking applied to expensive-loop problems. Mood, stimulants and psychedelics are speculated to shift the mode. Frameworks for telling the loops apart: Hogarth's kind/wicked environments, Bezos's one-way/two-way doors, pre-mortems, Kelly criterion.
6. **Safety.** Expensive-loop capability is upstream of dangerous abilities (persuasion, offensive biotech, long-term strategy). But "strong cheap-loop, weak expensive-loop" AI is itself an x-risk via **reward hacking**. The author leaves open whether the former can be had without the latter.
7. **How AI could improve.** Train in more expensive loops (GRPO-style repetition makes this costly: ~8 attempts × 5 visits = 40 attempts per task); hope for cheap-to-expensive generalisation (possible "escape velocity" ~$10k loops); or build cheap **wargame** environments that simulate the critical parts of an expensive loop (Prussian Kriegsspiel as precedent; robotics' sim-to-real gap as the warning). If none works, training may need civilisation-scale environments — the Borges map parody in footnote 7.

## Notable Quotes

> "The agent has no model of information gain relative to compute expenditure, and no prior over the consequence severity of proposed changes." (Amazon study, quoted)

> "Additional tokens buy denser refinement within the committed strategy but not a better one." (PostTrainBench, quoted)

> "In a cheap-loop environment, error correction is basically free." / "Your core beliefs are part of the environment."

## Caveats

- **Single-author essay.** Evidence is borrowed from a few benchmarks and anecdotes; the cheap/expensive dichotomy is a framing, not a measured variable. In practice cost of feedback is a continuum.
- **AI-R&D-heavy examples.** PostTrainBench, the Amazon study and TasteVal concern ML research tasks; transfer to everyday software engineering is plausible but not shown by the article.
- **Training-dynamics explanation is conjecture** ("presumably"); the author does not test it.
- Footnote 2 notes models *are* improving on some elements (TasteVal) — attributed to better ML knowledge rather than better theory-building.
- Several cited arXiv IDs (2608.x–2610.x) post-date much of the wiki's other material; treat the specifics as the article's claims.

## Operational Takeaways

The article gives no software-engineering advice. The implications drawn from it in discussion (task classification, proxy ladders, ROI-before-run, mid-run strategy review, human-owned theory) are filed — marked as inference — in the guide [Agentic Engineering: A General How-To Guide](../../outputs/data-n-ai/2026-11-09-agentic-engineering-how-to-guide.md) alongside the practices from [The Inference Gap](the-inference-gap.md).

## Related Pages

- [The Expensive-Loop Problem](../concepts/expensive-loop-problem.md)
- [frmsaul](../entities/frmsaul.md)
- [Agentic Engineering: A General How-To Guide](../../outputs/data-n-ai/2026-11-09-agentic-engineering-how-to-guide.md)
- [Source: The Inference Gap](the-inference-gap.md) — companion: *how much reasoning you get* vs. this article's *how costly feedback is*
- [Premature Completion Declaration](../concepts/premature-completion-declaration.md)
- [Human-in-the-Loop](../concepts/human-in-the-loop.md)
- [Harness Evolution](../concepts/harness-evolution.md)
- [LLM Limitations](../concepts/llm-limitations.md)
