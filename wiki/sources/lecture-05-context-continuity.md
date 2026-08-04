---
tags: [data-n-ai, source, agents, prompt-engineering]
sources: [raw/data-n-ai/articles/2026-08-04-lecture-05-context-continuity.md]
updated: 2026-08-04
---

# Source: Lecture 05 — Keeping Context Alive Across Sessions

Course lecture from *Learn Harness Engineering* (walkinglabs.github.io), part of a project-based curriculum on designing environments, state, verification, and control systems for Codex and Claude Code. Covers why long-running agent tasks lose continuity across session boundaries and how structured state-persistence artifacts fix it.

## Key Claims

- **Context windows are finite, permanently.** Growing window size (128K → 1M) doesn't solve the problem — complex tasks will still exhaust whatever budget exists. Agents burn tokens on codebase understanding, decision history, tool output, and conversation state, and this grows faster than window expansion.
- **Compaction preserves "what," loses "why."** Final code output survives; the intermediate reasoning that explains *why option A was chosen over option B* does not. The next session sees the code and may "optimize away" a deliberate decision it doesn't know was deliberate.
- **"Context anxiety"** (Anthropic's term): as context approaches the limit, agents exhibit rushed-finish behavior — skipping verification, taking the simple path over the optimal one. Anthropic's March 2026 research found this is severe on **Sonnet 4.5** but greatly diminished on **Opus 4.5** — meaning harness design must account for the specific target model, not a one-size-fits-all template.
- **Drift compounds across sessions.** Each new session has a slightly different understanding of project goals; without correction, each session's deviation stacks on the last.
- **Rebuild cost is the key metric**: the time a new session needs to reach an executable, oriented state. A good harness compresses this from ~15 minutes to ~3 minutes.
- **Compaction vs. reset are complementary, not competing.** Compaction keeps continuity within a session but doesn't eliminate context anxiety (the agent still "remembers" it was running low). Reset gives a clean mental state but is entirely dependent on the completeness of handoff artifacts.

## Practical Toolkit (the article's prescription)

1. **PROGRESS.md** — current state (commit, test status, lint), completed items, in-progress items, known issues, next steps.
2. **DECISIONS.md** — a decision log: what was decided, why, what alternative was rejected, when. Explicitly *not* a design doc — just enough to prevent re-litigating settled choices.
3. **Git commits as checkpoints** — free, versioned state snapshots; commit messages should carry the "why."
4. **Clock-in / clock-out routine in AGENTS.md** — explicit session-start (read PROGRESS.md/DECISIONS.md, run checks, resume from "Next Steps") and session-end (update PROGRESS.md, run checks, commit) steps.
5. **Mixed strategy** — short tasks (<30 min) complete in one session; long tasks need the full artifact set. Rule of thumb: if a task will need >60% of the context window, start preparing the handoff before you're forced to.

## Cited Quantitative Example

Illustrative case (not the article's own experiment — a worked example): a 12-feature-point blog+auth build across 5 sessions.

| | No state persistence | With state persistence |
|---|---|---|
| Session 2 rebuild time | ~15 min | ~3 min |
| Features completed (of 12) | 7 (58%) | 12 (100%) |
| Hidden defect rate | 43% | 8% |

## Notable Quote

> "Treat the agent like an engineer whose short-term memory gets wiped at every session. Before it 'clocks out,' it must write down critical information so the next 'shift' agent can pick up quickly."

## Sources Cited by the Article

- Anthropic: [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Anthropic: [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- OpenAI: [Harness Engineering](https://openai.com/index/harness-engineering/)
- [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172)

## Metadata

- Source: [Lecture 05, Learn Harness Engineering](https://walkinglabs.github.io/learn-harness-engineering/en/lectures/lecture-05-why-long-running-tasks-lose-continuity/)
- Type: course lecture (teaching material, not primary research — synthesizes Anthropic/OpenAI harness-engineering posts)
- Ingested: 2026-08-04

## Related Pages

- [Session Continuity](../concepts/session-continuity.md)
- [Context Engineering](../concepts/context-engineering.md)
- [AGENTS.md](../concepts/agents-md.md)
- [Ralph Loop](../concepts/ralph-loop.md)
