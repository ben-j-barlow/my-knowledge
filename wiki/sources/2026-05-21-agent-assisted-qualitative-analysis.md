---
tags: [data-n-ai, source, agents, prompt-engineering]
sources: ["raw/data-n-ai/articles/Exploring Agent-Assisted Qualitative Analysis.md"]
updated: 2026-05-28
---

# Source: Exploring Agent-Assisted Qualitative Analysis

**Author:** sh-reya.com (academic researcher, recently accepted faculty offer)
**Published:** 2026-05-21
**URL:** https://www.sh-reya.com/blog/ai-qual-analysis/

Six-experiment study applying Claude Sonnet (via Agent SDK) to grounded theory qualitative analysis of 451 tweets asking "when do you switch away from Claude?" The author varies agent setup and human involvement to find where naive agentic approaches break down.

## Setup

**Data:** 451 public tweets responding to Sholto Douglas's question: *"When do you reach for other models instead of Claude? What can we do better?"*

**Six conditions:**

| ID | Grounded theory in prompt? | Human involvement | Multi-agent? |
|----|---------------------------|-------------------|--------------|
| exp0 | No — just "organize and group complaints" | None | No |
| exp1 | Yes | None | No |
| exp2-codes | Yes | Review/edit proposed codes per batch in a browser UI | No |
| exp2-memo | Yes | Read agent memo, leave written direction feedback per batch | No |
| exp3-hierarchical | Yes | None | Yes — supervisor + parallel workers |
| exp3-independent | Yes | One round of feedback after two coders finish | Yes — two coders + reconciliation |

## Key Findings

### Without HITL, agents converge prematurely
exp0 and exp1 produce organized, readable reports that nonetheless miss depth. The agent settles on a stable framing early and mines the data for confirmatory evidence rather than letting the theory emerge. The exp0 report (no methodology) is a list of 29 complaint buckets; exp1 (grounded theory prompt) produces "The Reliability Crisis" — a coherent central thesis — but reaches it too fast and holds it too rigidly.

### Memo feedback outperforms code editing
exp2-memo (tell the agent where to go) produces structurally different analyses than exp2-codes (edit individual tweet codes). Code-editing mode keeps the human in a reactive, artifact-correcting role; memo mode keeps them in a proactive, direction-setting role. The latter is more efficient (less work per batch) and produces more substantive divergence from the no-HITL baseline.

### Independent coders + one round of feedback is the strongest setup
exp3-independent (two agents code the full corpus separately, reconcile disagreements, then one round of human feedback) produces the most distinct analysis. The disagreement surface from independent coders exposes genuine ambiguity in the data — the human's feedback can then resolve it with judgment rather than just reviewing pre-agreed-upon codes.

### The core problem: evaluation criteria evolve
Qualitative analysis is fundamentally hard for current agentic systems because the "right" analysis depends on context outside the corpus and the evaluation criteria themselves change as the researcher interacts with data. Agents assume stable objectives and converge prematurely on fixed framings. This is not a fixable prompt engineering issue — it reflects a structural mismatch between the task shape and current agent architecture.

## Notable Quotes

> "Doing this well requires a kind of taste and judgment that is difficult to specify explicitly, which makes it a much harder AI-assistance problem than most tasks out there."

> "The evaluation criteria themselves evolve throughout the workflow. Researchers often discover what matters by interacting with the data over many rounds of interpretation."

## What the Different Reports Found

The same 451 tweets produced fundamentally different theories:
- **exp0**: 29 discrete complaint categories (organized but flat)
- **exp1**: "Reliability Crisis" — high ceiling, unreliable floor
- **exp2-codes**: "Trust Spiral" — trust degrades across 5 simultaneous dimensions, becomes self-reinforcing
- **exp2-memo**: Multi-model orchestration as the dominant pattern; "switching" is a misnomer — users build hybrid workflows
- **exp3-hierarchical**: Similar to exp1, supervisor framing locked in early
- **exp3-independent**: Most structurally distinct; integrated reliability + relationship framing

## Related Pages

- [Grounded Theory](../concepts/grounded-theory.md)
- [Human-in-the-Loop](../concepts/human-in-the-loop.md)
- [Iterative Repair Loops](../concepts/iterative-repair-loops.md)
- [LLM Limitations](../concepts/llm-limitations.md)
