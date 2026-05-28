---
tags: [data-n-ai, concept, agents, prompt-engineering]
sources: ["raw/data-n-ai/articles/Build iterative repair loops with Codex.md"]
updated: 2026-05-14
---

# Iterative Repair Loops

A closed-loop agent workflow pattern where an agent produces output, validates it against a rubric, and uses the feedback to improve the next pass — repeating until the output satisfies its acceptance criteria or a stop condition is reached.

## Structure

Three phases with structured handoffs:

| Phase | Role | Key constraint |
|-------|------|----------------|
| **Review** | Inspect artifact, return structured findings | No edits — identification only |
| **Repair** | Apply focused edits to a copy | Smallest useful change; don't assume it worked |
| **Validate** | Execute + judge against rubric | Failures become input to the next repair |

The loop gets more specific as it runs: early passes work from review findings; later passes work from observed validation failures.

## Why Structure the Handoffs

Returning JSON schemas (not prose) at each phase boundary makes the loop composable and debuggable. A repair prompt that receives `remaining_delta: ["execution failed: missing import"]` is far more precise than one receiving a previous model response as free text.

## Stop Conditions

Equally important as the repair prompt itself. A loop should stop when:
- Validation passes
- Maximum iterations reached
- `remaining_delta` stops changing between passes (the loop has stalled)
- The remaining issue requires human judgment

## Audit Trail

Each iteration should produce a record capturing: review findings, what changed, whether execution passed, and remaining delta. This answers the question "why did the loop continue / stop?" and produces a clear handoff for human review — the difference between an impressive-looking edit and a maintainable workflow.

## Applicable Domains

The pattern applies wherever agent output can be measured with trustworthy feedback:
- Code modernization (run tests; failures become next delta)
- Regulatory/compliance content (check required language, citations, jurisdiction terms)
- Documentation freshness (execute notebooks; errors become repair input)
- Support knowledge (test against current product behaviour)
- Protocol optimization (validate against domain rules)

## Limits: When Structured Loops Aren't Enough

Iterative repair loops assume the acceptance criteria are **stable and verifiable** — run the tests, check the schema, compare against a rubric. This assumption breaks for open-ended tasks where the criteria themselves evolve as the work progresses (qualitative analysis, creative direction, exploratory research).

In those cases, the loop produces technically correct but directionally wrong output — the agent converges on a plausible framing early and iterates within it. Human steering at the *direction* level (not the artefact level) is needed before the loop locks in. See [Human-in-the-Loop](human-in-the-loop.md).

For tasks where the criteria are stable but the agent stops too early, the [Ralph Loop](ralph-loop.md) addresses this by making external tests the only valid stop condition.

## Related Pages

- [Source: Build Iterative Repair Loops with Codex](../sources/codex-iterative-repair-loops.md)
- [Human-in-the-Loop](human-in-the-loop.md)
- [Ralph Loop](ralph-loop.md)
- [Codex](../entities/codex.md)
