---
tags: [data-n-ai, source, agents, prompt-engineering, llm]
sources: [raw/data-n-ai/articles/2026-09-11-wikiskill-agent-skill-evolution.md]
updated: 2026-09-11
---

# Source: WikiSkill — Compiling Agent Experience into Persistent Knowledge for Skill Evolution

arXiv paper (Google Research: Tang, Rashtchian, Ferng, Tomkins, Juan, Vu; 2026, https://arxiv.org/html/2608.27454). Proposes a framework that automatically evolves [Claude-Skills](../concepts/claude-skills.md)-style agent skills, with the key move being a **persistent wiki layer inserted between raw execution traces and the evolving skills** — structurally the same three-layer shape (raw / wiki / skill) this knowledge base itself uses (raw / wiki / schema). Worth reading as validation that the pattern generalizes beyond human-agent collaboration to fully automated skill discovery.

## Key Claims

- **The gap in prior skill-evolution methods**: EvoSkill keeps a cumulative history of proposals+outcomes, Trace2Skill extracts lessons per-trajectory, SkillOpt uses rejected-edit feedback — none of them maintain what's been *learned* as a separate, structured, persistent knowledge representation. Insights stay scattered across optimization histories instead of compounding.
- **Three-layer architecture**: **Raw Layer** (`raw/`) — immutable step-by-step execution traces (reasoning, tool calls, outputs). **Wiki Layer** (`wiki/`) — structured, compounding knowledge: a `patterns/` directory of markdown pages documenting specific failure modes or successful strategies with actionable workarounds, an `index.md` catalog, an append-only evolution log (`logs.md`), and a programmatically-updated `skill-impact.md` audit trail (proposal diffs + validation scores + accept/reject outcomes). **Skills Layer** (`skills/`) — the active procedural skill set actually injected into the agent's prompt at inference; each skill pairs a `SKILL.md` with a `PURPOSE.md` that traces it back to the wiki pattern(s) that motivated it.
- **The loop, four components per iteration**: an *Inference Agent* rolls out training tasks using the current skills (explicitly **denied** wiki access during training — see ablation below); a *Wiki Maintainer* reads the traces plus the existing wiki and does root-cause analysis on failures / extracts successful strategies, patch-editing pattern pages incrementally; a *Skill Proposer* (ReAct-style, tool-using, reads the wiki index + skill-impact history + task outcome summary, then actively pulls specific pattern pages and raw traces on demand) proposes one atomic skill creation or edit per iteration; a *Gating and Rollback* mechanism applies the proposal, evaluates on a held-out validation split, and keeps it only if validation score improves — otherwise reverts the skill set. **Critically, the wiki is never rolled back** — rejected proposals and their outcomes stay in the audit trail even when the skill change itself is discarded, so the Proposer doesn't re-propose known failures.
- **Headline result**: across 5 models (Qwen 4B/9B/27B, Gemma-31B, Gemini-3.5-Flash) and 5 benchmarks (math reasoning, web search, spreadsheet manipulation, long-context QA, embodied tasks), WikiSkill beat the strongest competing skill-evolution method by 3.3–12.0 average points per model, and improved over no-skill baselines in most model-benchmark pairs. Competing methods were inconsistent — e.g. EvoSkill improved Qwen-9B on math (28.2%→58.1%) but *degraded* Gemma-31B on the same benchmark (33.9%→29.8%).
- **Skill evolution complements model scale, doesn't substitute for it, but can compensate**: within the Qwen family, WikiSkill's average improvement grew with model size (+12.3 pts at 4B, +17.5 at 9B, +23.9 at 27B) — bigger models extract more value from the same procedural knowledge. Yet a 9B model with WikiSkill (47.4% avg) beat a 27B model with no skills at all (39.4% avg) — evolved procedural knowledge and raw model capability are complementary, separately-purchasable sources of performance.
- **Skills transfer across models, and transferred skills sometimes beat self-evolved ones**: Qwen-27B-evolved skills lifted Qwen-9B to 50.5% on the spreadsheet benchmark vs. 33.6% with its own self-evolved skills (and 24.3% with none). Even small→large transfer worked: Qwen-4B skills lifted Gemma-31B from 33.9% to 73.1% on math. But transfer isn't guaranteed positive — Qwen-4B's skills for the spreadsheet task encoded low-level workarounds (single-line Python commands, string-conversion rules) that *helped* the small model avoid execution failures but *constrained* Gemini-3.5-Flash away from cleaner end-to-end scripts it was otherwise capable of, cutting its score from 50.5% to 18.1%. The paper's framing: skill *discovery* and skill *execution* are distinct capabilities that self-evolution normally conflates.
- **Ablation proves the wiki layer is load-bearing, not decorative**: on Gemini-3.5-Flash, giving the Skill Proposer wiki access (vs. none, with no Wiki Maintainer at all) raised average score from 48.7% to 63.7% (+15.0 points) — without persistent cross-iteration knowledge, the Proposer couldn't resolve intricate recurring failure modes. Conversely, giving the *Inference Agent* wiki access during training **hurt** final skill quality (63.7%→60.9%): the hypothesis is that the agent partially solved tasks by reading the wiki directly instead of using skills, making its rollout traces less informative for skill development. Net design rule: the raw/inference layer should stay wiki-blind; only the maintenance/proposal layer should read it — directly mirroring "LLM reads from raw/, never writes" plus "the wiki is LLM-owned, not agent-execution-owned" as a *training-time* constraint, not just a human-workflow convention.
- **Skill refinement is genuinely iterative, not front-loaded**: only 39–58% of accepted skill updates happened in the earliest iterations; substantial refinement continued into middle and late iterations, especially on harder benchmarks (33% of SealQA's accepted updates came in the middle stage alone). A worked case study on ALFWorld shows a rejected proposal at iteration 0 (`goal-directed-action`, failed validation) informing an accepted, more specific proposal at iteration 1 (`break-repetition-loop`, with the concrete rule "never return an item to its origin location"), later refined again at iteration 4 as new loop-variant evidence accumulated in the wiki — each refinement citing the wiki pattern that motivated it.

## Notable Quotes

> "We ask: Can agent experience be similarly compiled into persistent knowledge to support long-term skill evolution?"

> "Skill discovery and skill execution are distinct capabilities."

## Caveats / Limitations (author-stated)

- Skills are injected directly into the prompt (no retrieval/triggering evaluated) — doesn't test what happens as a skill *library* grows large enough to need selection, which is exactly the retrieval-failure problem [Claude Skills](../concepts/claude-skills.md) solves with router skills.
- Validation gating requires strict improvement to accept a proposal, which excludes neutral changes that might enable later gains — a stricter bar than this repo's own wiki-update discipline.
- No automated wiki-pruning mechanism yet; pattern pages, logs, and diffs accumulate indefinitely. The paper flags this as unsolved — same open problem as `AGENTS.md`'s drift.

## Metadata

- **Source**: [WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution](https://arxiv.org/html/2608.27454) (Tang, Rashtchian, Ferng, Tomkins, Juan, Vu — Google Research / Virginia Tech, 2026)

## Relevant Wiki Pages

- [Claude Skills](../concepts/claude-skills.md) — updated with a section comparing Anthropic's human-maintained skill pairing to WikiSkill's fully automated evolution loop
- [Session Continuity](../concepts/session-continuity.md) — the wiki-as-persistent-cross-iteration-memory pattern, applied to *skill development* rather than task handoff
- [Feature Lists](../concepts/feature-lists.md) — gating-and-rollback here is the same "external, enforced pass/fail gate, not agent self-report" primitive
- [AGENTS.md](../concepts/agents-md.md) — the unsolved-drift problem this paper's `skill-impact.md` audit trail partially addresses
