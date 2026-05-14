---
tags: [data-n-ai, source, agents, prompt-engineering]
sources: ["raw/data-n-ai/articles/Build iterative repair loops with Codex.md"]
updated: 2026-05-14
---

# Source: Build Iterative Repair Loops with Codex

**Origin:** OpenAI Cookbook  
**URL:** https://developers.openai.com/cookbook/examples/codex/build_iterative_repair_loops_with_codex  
**Created:** 2026-05-14

## Summary

A practical cookbook demonstrating closed-loop agent workflows: an agent produces output, validates it, and uses feedback to improve the next pass. The worked example is a documentation reliability workflow that detects and repairs stale API/SDK notebooks, but the pattern is explicitly general.

## Core Pattern

Three phases, each with structured JSON outputs so handoffs are machine-readable rather than prose:

1. **Review** — inspects the artifact and returns structured findings. Does not edit files. Keeps the first step focused on identification before any changes.
2. **Repair** — applies the smallest useful edits to a *copy* of the artifact, informed by review findings and any validation delta from the previous pass. The loop does not assume the edit worked.
3. **Validate** — executes the artifact and asks a judge to score it against a rubric. Failures become the `remaining_delta` for the next repair pass.

Validation closes the loop. The repaired artifact must satisfy the checks that matter, and remaining issues become the next repair input.

## Key Claims

- Separating review from repair from validation keeps each phase focused and auditable.
- Structured outputs at every handoff make the loop easier to debug, rerun, and adapt to other artifact types.
- A per-iteration `record.json` audit trail (what was found, what changed, did it execute, what remains) is what makes agentic maintenance *trustworthy* rather than just impressive.
- **Stop conditions matter as much as the repair prompt.** A good loop stops when: validation passes; max iterations reached; remaining delta stops changing; or the next decision needs human review.
- The pattern applies wherever agent output can be measured with trustworthy feedback: code modernization, regulatory content, support articles, clinical protocols, and more.

## Notable Quote

> "The important signal is not that Codex made edits. The important signal is that the remaining validation delta gets smaller as the loop runs."

## Implementation Notes

- Uses [Codex](../entities/codex.md) CLI in headless mode (`codex exec`) with `--output-schema` to enforce structured JSON responses.
- Business rules (what "good" means for the domain) are passed explicitly so the model doesn't infer them from scratch each pass.
- Cases run concurrently; each case is independent.
- The three sample fixtures are staged to clear at iterations 1, 2, and 3 respectively, demonstrating convergence.

## Related Pages

- [Codex](../entities/codex.md)
- [OpenAI](../entities/openai.md)
- [Iterative Repair Loops](../concepts/iterative-repair-loops.md)
