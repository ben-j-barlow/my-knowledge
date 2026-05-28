---
tags: [data-n-ai, concept, agents, prompt-engineering]
sources: ["raw/data-n-ai/articles/Plan Mode All the Time, Substrait over SQL, and the End of the DE Role ft. Chris Riccomini.md"]
updated: 2026-05-28
---

# Ralph Loop

An autonomous agentic development technique where a shell loop (or plugin) repeatedly submits the same goal to an agent until external tests pass. The agent cannot declare itself done — only the external test gate can end the loop.

Origin: [ghuntley.com/loop/](https://ghuntley.com/loop/). Chris Riccomini references it as the "Ralph Loop" / "Wiggum Loop."

## Mechanism

```bash
until tests_pass; do
  prompt_agent_with_goal
done
```

The agent works, produces output, the external test suite runs, and if tests fail the agent is re-prompted with the same goal (plus the failure output as context). This repeats until tests pass or a maximum iteration count is hit.

## Why It Exists

The standard failure mode of agentic coding: the agent decides the task is "good enough" and stops, often leaving stubs, unhandled edge cases, or implementations that satisfy the letter but not the spirit of the requirement.

The Ralph Loop removes the agent's ability to make that call. An external verifier (tests, linter, validator) is the only authority that can end the loop. This forces the agent to iterate through actual failures rather than stopping at perceived completion.

## Contrast With Iterative Repair Loops

Both are closed-loop patterns, but they address different failure modes:

| | [Iterative Repair Loop](iterative-repair-loops.md) | Ralph Loop |
|---|---|---|
| **Trigger** | Structured review findings | External test failures |
| **Stops when** | Rubric satisfied or max iterations | External tests pass |
| **Human involvement** | Optional; built into stop condition | None in the inner loop |
| **Best for** | Auditable, multi-phase repair with structured handoffs | Fast autonomous iteration until a binary criterion is met |

## Relationship to Plan Mode

Chris Riccomini pairs the Ralph Loop with exhaustive plan-mode iteration: first, make the plan so detailed there's no possible misimplementation; then, use the Ralph Loop to iterate through execution until external quality gates confirm success. Plan mode addresses ambiguity; the Ralph Loop addresses incomplete execution.

## Quality Gates

The loop is only as good as its exit criterion. Three steps:
1. **Define** what quality means (test coverage, lint score, output format)
2. **Measure** it (tooling: coverage reports, schema validators)
3. **Enforce** thresholds (CLAUDE.md rules + git hooks — the harness runs these, not the model)

## Related Pages

- [Iterative Repair Loops](iterative-repair-loops.md)
- [Human-in-the-Loop](human-in-the-loop.md)
- [Chris Riccomini](../entities/chris-riccomini.md)
- [Source: Plan Mode All the Time](../sources/2026-05-21-plan-mode-substrait-de-role.md)
