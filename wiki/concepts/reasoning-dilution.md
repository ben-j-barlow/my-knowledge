---
tags: [data-n-ai, concept, llm, agents, context-engineering]
sources: ["raw/data-n-ai/articles/2026-09-19-the-inference-gap.md"]
updated: 2026-11-09
---

# Reasoning Dilution and Thinking Fragmentation

Two measured ways delivered reasoning fails to keep pace with task size in agentic coding, both from [The Inference Gap](../sources/the-inference-gap.md) (one user, Fable 5 in Claude Code — treat as a hypothesis-grade finding).

## Reasoning dilution

As incoming text per turn (user input, tool results, attachments — *not* the carried-forward history) grows, thinking grows far more slowly:

| Input tokens per turn | Median thinking | Thinking per 1K input |
|---|---|---|
| 1,024 | 2,639 | 2,577 |
| 4,096 | 4,336 | 1,059 |
| 16,384 | 7,122 | 435 |
| 65,536 | 11,806 | 180 |
| 131,072 | 15,179 | 116 |

A 32× rise in input gives ~3.5× more thinking; there is progressively *less thinking per unit of material received*. The author's anecdotal correlates: more logical inconsistency when given bigger specs or codebase reads; less faithful completion on long-horizon tasks (incomplete work, mismatch with agreed design, claims about results that do not exist); and **longer corrective guideline additions leading to lower adherence**. At comparable input, August thinking was 18–32% below July.

Relation to existing wiki findings: this offers a *mechanism candidate* for [context rot](context-engineering.md#context-rot) and for the ETH Zurich result that bloated context files hurt — more material competes for a roughly fixed reasoning allotment. It is consistent with, not proof of, those results.

## Thinking fragmentation

An invocation's thinking is an *uninterrupted serial sequence*; a turn's thinking is a sum over invocations that may be interleaved with reads, edits and tool calls. As turn thinking grows, the longest single sequence accounts for a shrinking share:

| Turn thinking | Largest invocation's share | Median invocations/turn |
|---|---|---|
| 4,096 | 81% | 4 |
| 16,384 | 37% | 20 |
| 65,536 | 18% | 83 |
| 131,072 | 12% | 350 |

A "32K thinking" turn typically looks like `1K think → read → 1K think → bash → 1K think → edit …`. Tool observations make this *useful*, but it is not equivalent to 32K of uninterrupted deliberation. Of 105 turns reaching ≥48 invocations, all contained zero-thinking calls.

## Why it matters

- Accumulated thinking totals **overstate** sequential reasoning depth.
- Recovery tactics (subagents, best-of-N, longer runs) add breadth, not serial depth — see [The Inference Gap](inference-gap.md).
- Hard design and architecture decisions are where shallow serial reasoning does the most damage; this motivates isolating them into short, focused, low-context steps ([Agentic Engineering Under Variable Inference](agentic-engineering-under-variable-inference.md)).

## Related Pages

- [The Inference Gap](inference-gap.md)
- [Context Engineering](context-engineering.md)
- [Agent Configuration Audit](agent-configuration-audit.md)
- [Session Continuity](session-continuity.md)
- [Premature Completion Declaration](premature-completion-declaration.md) — unfaithful long-horizon completion is the symptom both pages describe
- [Source: The Inference Gap](../sources/the-inference-gap.md)
