---
tags: [data-n-ai, concept, agents, prompt-engineering]
sources: ["raw/data-n-ai/articles/Exploring Agent-Assisted Qualitative Analysis.md"]
updated: 2026-05-28
---

# Human-in-the-Loop (HITL)

The practice of injecting human judgment at defined points in an otherwise automated agentic workflow. Not a single thing — the *level of abstraction* at which a human intervenes determines both the effort required and the quality of the outcome.

## Why It Matters

Current agents assume stable objectives and converge prematurely on fixed framings for open-ended tasks. Structured agent loops (see [Iterative Repair Loops](iterative-repair-loops.md)) work well when the acceptance criteria are fixed and verifiable. When criteria evolve as the work progresses — qualitative analysis, creative direction, strategy — human steering is necessary to prevent premature lock-in.

HITL is not a fallback for agent failure. It is a design choice about where human judgment creates the most leverage.

## Two Modes of Intervention

Identified empirically through the qualitative analysis experiments:

### 1. Artifact Review (Code Editing)
The human directly edits, approves, or rejects individual output artefacts — codes, classifications, decisions — after each batch.

**Effort:** High. Requires reading every artefact produced.
**Effect:** Keeps individual outputs accurate but does not change the agent's framing or direction.
**Failure mode:** The human is reactive, not proactive. The agent continues on the same trajectory — just with better-labelled steps.

### 2. Direction Setting (Memo Feedback)
The human reads the agent's analytical memo and writes high-level steering: "focus more on X," "you're missing the institutional trust dimension," "these two categories should be merged."

**Effort:** Lower. One memo read + one direction note per batch.
**Effect:** Changes the trajectory of the analysis. Produces structurally different outputs from the no-HITL baseline.
**Key insight:** Feedback at a higher level of abstraction is both cheaper and more valuable.

## Timing

HITL at the wrong time (after the agent has converged) is expensive because the human must undo work before doing new work. HITL at the right time (before the agent locks in a framing) is cheap.

Early-stage direction feedback during open coding is more leveraged than late-stage review after selective coding.

## Multi-Agent HITL

One productive pattern: two independent agents process the same corpus separately, then a reconciliation step compares where they disagree. Human feedback is applied once to the disagreement surface. This produces:
- More framing diversity than a single agent
- Lower human effort than reviewing every step of two independent runs
- A principled disagreement surface that focuses human judgment where it's most needed

## Relationship to Other Patterns

- **Iterative repair loops:** Closed-loop pattern for tasks with *stable* acceptance criteria (run tests, check output format). HITL is implicit in the stop condition ("remaining issue requires human judgment") but the loop itself runs without humans. For tasks with *evolving* criteria, HITL needs to be built into the loop at the direction level.
- **Ralph Loop:** Autonomous iteration via external test gates. Addresses a different failure mode (agents declaring themselves done prematurely) rather than premature convergence on a wrong framing.

## Related Pages

- [Grounded Theory](grounded-theory.md)
- [Iterative Repair Loops](iterative-repair-loops.md)
- [Ralph Loop](ralph-loop.md)
- [LLM Limitations](llm-limitations.md)
- [Source: Agent-Assisted Qualitative Analysis](../sources/2026-05-21-agent-assisted-qualitative-analysis.md)
