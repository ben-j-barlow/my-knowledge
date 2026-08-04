---
tags: [data-n-ai, source, agents, prompt-engineering]
sources: [raw/data-n-ai/articles/2026-08-04-lecture-08-feature-lists.md]
updated: 2026-08-04
---

# Source: Lecture 08 — Use Feature Lists to Constrain What the Agent Does

Course lecture from *Learn Harness Engineering* (walkinglabs.github.io), the same series as [Lecture 05](lecture-05-context-continuity.md). Argues that a feature list is not a human memo but a **harness primitive** — a machine-readable data structure that the scheduler, verifier, and handoff reporter all depend on to function.

## Key Claims

- **Agents don't know what "done" means.** Told to "add a shopping cart," an agent may interpret that as "write a Cart component and an addToCart method" when the human meant full browse→add→checkout. Without an externalized spec, the agent defaults to its own implicit standard — usually "the code has no obvious syntax errors."
- **Unstructured progress notes are unusable by a new session.** A note like "did user auth, shopping cart mostly done, still need payments" can't answer: what does "mostly done" mean, which tests passed, what's blocking payments. Anthropic's engineering data (per the article) shows well-structured progress records cut session-startup diagnostic time by 60–80%.
- **The triple structure.** Every feature item must carry three fields: **behavior** (what the agent should do, e.g. "POST /cart/items returns 201"), **verification command** (the exact executable check), and **state**. Missing any one field makes the item unusable to the harness.
- **Four-state machine**: `not_started` → `active` → `passing`, with a `blocked` branch. States are controlled by the harness, not the agent — the agent can only *submit* a verification request; the harness runs it and decides the transition.
- **Pass-state gating is irreversible and one-directional.** The only path from `active` to `passing` is a successful verification command. This is the harness-primitive analogue of a database constraint vs. an application-layer check: constraints can't be bypassed by buggy application code, and pass-state gating can't be bypassed by an agent that thinks it's done.
- **Single source of truth.** All "what to do" information must derive from the feature list — no contradictions between it and conversation history, TODOs in code, or implicit requirements mentioned mid-session.
- **Back-pressure.** The count of not-yet-passing features is the pressure the harness exerts on the agent; zero pressure means the project is complete. This gives the harness (not the agent) an objective completion signal.

## Four Consumers of the Feature List

1. **Scheduler** — reads states, picks the next `not_started` item.
2. **Verifier** — executes the verification command, decides whether to allow the state transition.
3. **Handoff reporter** — auto-generates session handoff summaries from feature-list state (rather than relying on the agent's self-report).
4. **Progress tracker** — tallies state distribution as a project health metric.

## Granularity Calibration

Each feature should be scoped to "completable in one session." Examples from the article:
- Good: "User can add items to cart"
- Too broad: "Implement the shopping cart"
- Too narrow: "Create the name field on the Cart model"

## Cited Quantitative Example

Illustrative case: a 10-feature e-commerce platform, memo-based tracking vs. structured feature lists.

| | Memo mode | Structured mode |
|---|---|---|
| New-session state-inference time | ~20 min | ~3 min |
| Outcome | Re-implements already-completed features | Reads state, resumes directly from the first non-passing item, zero rework |
| Completion rate (relative) | baseline | **+45%** feature completion, zero duplicate implementations |

## Minimal Format Example

```json
{
  "id": "F03",
  "behavior": "POST /cart/items with {product_id, quantity} returns 201",
  "verification": "curl -X POST http://localhost:3000/api/cart/items -H 'Content-Type: application/json' -d '{\"product_id\":1,\"quantity\":2}' | jq .status == 201",
  "state": "passing",
  "evidence": "commit abc123, test output log"
}
```

Rule written into `CLAUDE.md`/`AGENTS.md`: only one feature active at a time; the agent never edits state fields directly — only the verification script does.

## Notable Framing

> "Documents are for humans to read; primitives are for systems to execute. Documents can be ignored; primitives can't be bypassed."

Frames feature lists as the harness-level equivalent of Design by Contract (Bertrand Meyer) applied to agent task scope, and cites Anthropic's "Building Effective Agents" as identifying the feature list as the "core data structure" for controlling agent scope.

## Sources Cited by the Article

- Anthropic: [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- OpenAI: [Harness Engineering](https://openai.com/index/harness-engineering/)
- Bertrand Meyer: *Design by Contract* (Object-Oriented Software Construction)
- *How Google Tests Software*

## Metadata

- Source: [Lecture 08, Learn Harness Engineering](https://walkinglabs.github.io/learn-harness-engineering/en/lectures/lecture-08-why-feature-lists-are-harness-primitives/)
- Type: course lecture (teaching material, synthesizes Anthropic/OpenAI harness-engineering posts + software-engineering theory)
- Ingested: 2026-08-04

## Related Pages

- [Feature Lists](../concepts/feature-lists.md)
- [Session Continuity](../concepts/session-continuity.md)
- [Ralph Loop](../concepts/ralph-loop.md)
- [Data Contracts](../concepts/data-contracts.md)
