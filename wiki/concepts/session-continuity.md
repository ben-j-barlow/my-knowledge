---
tags: [data-n-ai, concept, agents, prompt-engineering]
sources: [wiki/sources/lecture-05-context-continuity.md]
updated: 2026-08-04
---

# Session Continuity

Session continuity is the discipline of carrying an agent's state — progress, decisions, and verification results — across the boundary between sessions, so that a fresh session (after a context reset or a new invocation) can resume without re-deriving what a previous session already established. Where [Context Engineering](context-engineering.md) manages the token budget *within* a session, session continuity manages what survives *between* sessions.

The problem is structural, not a model-capability gap: context windows are finite no matter how large they grow, so any task that spans sessions will hit a boundary where information must either be summarized (compaction) or dropped (reset). Both lose something by default; state-persistence artifacts are what recover it deliberately.

---

## Why Continuity Breaks

- **"What" survives, "why" doesn't.** Compaction and final code output preserve the artifact but not the reasoning that produced it — why option A beat option B, why a library was chosen, why an optimization was deliberately skipped. A new session may "correct" a deliberate decision it has no way of knowing was deliberate.
- **Drift compounds.** Every session boundary introduces a small gap between the agent's understanding and the actual repo state. Uncorrected, each session's drift stacks on the last, and the implementation can end up far from the original intent after several sessions.
- **Duplicate or conflicting work.** Without a progress record, a new session can't tell what's already done — it may redo completed work, or worse, do it halfway and then discover a conflict with the existing implementation.
- **Verification has to restart from zero.** If prior test/lint results aren't recorded, every new session re-runs and re-diagnoses the whole system before it can make progress, burning context on rediscovery rather than work.

## Context Anxiety

Anthropic's term for a specific, measured failure mode: as an agent's context approaches its limit, it exhibits rushed-finish behavior — skipping verification steps, taking the simple solution over the correct one, ending tasks early to avoid "losing" information. It is a resource-anxiety behavior, not a deliberate tradeoff.

Anthropic's March 2026 research found this is **model-dependent**: severe on **Sonnet 4.5** (compaction alone isn't sufficient; context reset becomes load-bearing), but greatly diminished on **Opus 4.5** (compaction can manage context without relying on resets). The practical implication: harness design has to be tuned to the specific target model rather than templated once and reused.

## Compaction vs. Reset

Two complementary strategies, not competing ones:

| | Compaction | Reset |
|---|---|---|
| Mechanism | Summarize earlier turns within the same session | Close the session; a new one rebuilds from persisted artifacts |
| Preserves | The "what" (code, current state) | Nothing automatically — depends entirely on artifact completeness |
| Loses | The "why" (rejected alternatives, rationale) | Everything not written down |
| Effect on context anxiety | Doesn't eliminate it — the agent still "knows" it was running low | Eliminates it — a genuinely fresh session has no anxiety signal |
| Failure mode | Silent loss of rationale; "lost in the middle" | Wasted time / wrong direction if handoff artifacts are incomplete |

## Machine-Readable vs. Human-Legible Handoffs

PROGRESS.md is human-legible but not enforced — nothing stops a session from writing a vague note ("shopping cart mostly done") that a future session can't act on. [Feature Lists](feature-lists.md) push the same idea one level further: a feature's state is a harness primitive, set only by a successful verification-command run rather than by the agent's free-text account of its own progress. The handoff reporter then generates the human-readable summary *from* that enforced state, rather than trusting the agent to write it accurately. Where PROGRESS.md depends on the agent's discipline, a feature list's pass-state gating removes the agent's ability to misreport.

## State-Persistence Toolkit

1. **`PROGRESS.md`** — current state (latest commit, test/lint status), completed items, in-progress items with %, known issues, next steps. The minimum viable handoff artifact.
2. **`DECISIONS.md`** — a decision log, not a design doc: date, decision, reason, rejected alternative, constraint. Prevents a new session from re-litigating a choice with incomplete information and landing somewhere different.
3. **Git commits as checkpoints** — free, automatically versioned snapshots of exact repo state; commit messages should carry the "why," not just the "what."
4. **Clock-in / clock-out routine, specified in [AGENTS.md](agents-md.md)** — explicit session-start steps (read PROGRESS.md/DECISIONS.md, run the check command, resume from "Next Steps") and session-end steps (update PROGRESS.md, run checks, commit).

**Mixed strategy**: not every task needs this. Short tasks (under ~30 minutes) finish within one session with no extra ceremony. Long tasks need the full artifact set. Rule of thumb: if a task is projected to need more than ~60% of the context window, start preparing the handoff before it's forced on you.

## Metrics That Matter

- **Rebuild cost** — the time a new session needs to reach an executable, oriented state. A good harness compresses this from ~15 minutes (re-exploring, guessing at rationale) to ~3 minutes (read the artifacts, resume). This is the practical, measurable payoff of session continuity — treat it as the metric to optimize, not "did we write nice docs."
- **Drift** — the gap between agent understanding and actual repo state, accumulated across session boundaries. Uncontrolled drift is the mechanism by which multi-session tasks silently diverge from original intent.

## Relationship to Other Patterns

- [Context Engineering](context-engineering.md) — the sibling discipline for *within-session* token management (what goes in the window). Session continuity is the *across-session* analogue: what survives the boundary when the window resets. Context anxiety is the behavioral symptom that links them — an agent managing its in-session budget badly is the same agent that rushes to finish before a session ends.
- [AGENTS.md](agents-md.md) — the natural home for the clock-in/clock-out routine; a session-continuity procedure is exactly the kind of non-inferable, procedural content AGENTS.md is for.
- [Ralph Loop](ralph-loop.md) — a different axis of the same problem: Ralph Loop concerns iterating *within* a task until an external gate passes; session continuity concerns preserving state *across* the task's session boundaries. Both remove reliance on the agent's own judgment about when/how to stop.
- [Data Contracts](data-contracts.md) / [Write-Audit-Publish](write-audit-publish.md) — same underlying principle applied to data pipelines: don't trust the agent's self-report, verify against an external, persisted record.

## Related Pages

- [Context Engineering](context-engineering.md)
- [AGENTS.md](agents-md.md)
- [Ralph Loop](ralph-loop.md)
- [Feature Lists](feature-lists.md)
- [Human-in-the-Loop](human-in-the-loop.md)
- [Source: Lecture 05 — Keeping Context Alive Across Sessions](../sources/lecture-05-context-continuity.md)
