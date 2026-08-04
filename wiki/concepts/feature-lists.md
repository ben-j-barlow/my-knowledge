---
tags: [data-n-ai, concept, agents, prompt-engineering, testing]
sources: [wiki/sources/lecture-08-feature-lists.md]
updated: 2026-08-04
---

# Feature Lists (Harness Primitives)

A feature list is a machine-readable data structure — not a human memo — that defines agent task scope, tracks completion state, and gates when the agent is allowed to call a feature "done." It is a harness primitive: the scheduler, verifier, and handoff reporter all depend on reading and writing it, the way a database constraint is depended on by every query that touches the table.

The problem it solves: agents don't know what "done" means unless told explicitly. Asked to "add a shopping cart," an agent may consider "wrote a Cart component" sufficient, when the human meant a full browse→add→checkout path. Left to its own judgment, an agent's implicit completion standard tends toward "the code has no obvious syntax errors" — not end-to-end behavioral correctness.

---

## The Triple Structure

Every feature item carries three required fields:

| Field | Purpose | Example |
|---|---|---|
| **Behavior** | What the agent should do, stated as an observable outcome | "POST /cart/items returns 201" |
| **Verification command** | The exact executable check that counts as proof | `curl ... | jq .status == 201` |
| **State** | Where the item currently stands | `not_started` / `active` / `blocked` / `passing` |

Missing any one field makes the item unusable by the harness — a behavior with no verification command is unfalsifiable; a verification command with no behavior description is unexplainable; a state with neither is meaningless.

## State Machine

```
not_started → active → passing
                 ↓
              blocked
```

- **Pass-state gating**: the only way an item moves from `active` to `passing` is a successful run of its verification command. This transition is controlled by the harness, not the agent, and is irreversible — once `passing`, an item doesn't go back.
- **Blocked** signals a dependency issue rather than agent failure — distinct from simply not passing yet.
- **Back-pressure**: the count of not-yet-passing items is the pressure the harness exerts on the agent to keep working. Zero pressure = project complete — an objective signal, not the agent's self-report.

## Why It Has to Be a Primitive, Not a Document

Documents are advisory; primitives are enforced. The article's framing: a feature list functioning as a harness primitive plays the same role as a **database-level constraint** versus an application-layer check — the former can't be bypassed by any code path, the latter depends on every caller behaving correctly. An agent that "thinks it's done" cannot mark a feature `passing` on its own judgment; only a successful verification run can.

Four harness components consume the same feature list, giving the system a single point of coordination instead of four components each with their own notion of state:

1. **Scheduler** — picks the next `not_started` item.
2. **Verifier** — runs the verification command, authorizes (or refuses) the state transition.
3. **Handoff reporter** — generates session handoff summaries directly from feature-list state, not from the agent's account of what it did.
4. **Progress tracker** — reports state distribution as a project health metric.

## Single Source of Truth

All information about "what needs to be done" must derive from the one feature list — no contradicting scope buried in conversation history, code TODOs, or requirements mentioned mid-session and never written down. Divergence between the feature list and any other source of "what's left" is treated as a bug in the harness, not a detail to reconcile manually.

## Granularity Calibration

Each item should be scoped to "completable in one session":

- Good: *"User can add items to cart"*
- Too broad: *"Implement the shopping cart"* — won't finish in one pass, state tracking becomes meaningless
- Too narrow: *"Create the name field on the Cart model"* — management overhead exceeds the value of tracking it separately

## Measured Effect

Illustrative 10-feature e-commerce case: memo-based tracking left a new session needing ~20 minutes to infer state (and led it to re-implement completed work); a structured feature list let a new session read state in ~3 minutes and resume directly from the first non-`passing` item. Reported result: **+45% feature completion rate, zero duplicate implementations** versus free-form tracking.

---

## Relationship to Other Patterns

- [Ralph Loop](ralph-loop.md) — the same underlying principle (an external gate, not the agent, decides when work is done) expressed as a concrete data structure. The Ralph Loop is the *control flow* (`until tests_pass: re-prompt`); the feature list is the *state* that control flow reads and writes — pass-state gating is what makes each iteration's "done" claim falsifiable.
- [Session Continuity](session-continuity.md) — a feature list is the machine-readable, harness-enforced version of PROGRESS.md. Where PROGRESS.md is a human-legible handoff note an agent writes and might write badly, a feature list's handoff reporter generates the summary automatically from state that was never the agent's to freely edit — removing the failure mode where the note itself is vague ("mostly done").
- [Data Contracts](data-contracts.md) — the same shape applied to data pipelines instead of application features: an executable specification (contract assertions / verification command) that gates a transition (publish / passing) the agent cannot grant itself. Both replace "the agent's word that it's correct" with a mechanical check.
- [AGENTS.md](agents-md.md) — the natural place to declare feature-list rules ("only one feature active at a time," "don't edit state fields yourself") as the kind of non-inferable procedural constraint AGENTS.md is for.
- [Premature Completion Declaration](premature-completion-declaration.md) — pass-state gating is the concrete mechanism that prevents this failure: a feature cannot become `passing` on the agent's say-so, only on a successful verification-command run.

## Related Pages

- [Ralph Loop](ralph-loop.md)
- [Session Continuity](session-continuity.md)
- [Data Contracts](data-contracts.md)
- [AGENTS.md](agents-md.md)
- [Premature Completion Declaration](premature-completion-declaration.md)
- [Source: Lecture 08 — Use Feature Lists to Constrain What the Agent Does](../sources/lecture-08-feature-lists.md)
