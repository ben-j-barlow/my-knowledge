---
tags: [data-n-ai, concept, agents, etl, pipelines, harness-engineering]
sources: ["wiki/sources/harness-engineering-agentic-data-engineering.md", "wiki/sources/rrsi-regularized-recursive-self-improvement.md"]
updated: 2026-10-02
---

# Harness Engineering (for Data Engineering)

A **Harness** is the controlled engineering layer sitting between an AI agent and the underlying deterministic tools (databases, orchestrators, sync engines). It is what turns raw model intelligence into something safe to delegate production work to: agents do not primarily lack capability, they lack the engineering system — context injection, permission checks, validation, rollback — that makes their output trustworthy, controlled, and recoverable.

Rule of thumb: **the agent never calls underlying tools directly.** Every action routes through the Harness, which consults governing context before executing and validates results after.

This is the data-engineering-specific vocabulary for a pattern this wiki already tracks generically — see [Correctness Layer](correctness-layer.md) (probabilistic agent / deterministic core split) and [Feature Lists](feature-lists.md) (external gate decides "done," not the agent).

---

## The Seven Sign-Off Gates

A checklist for "when is it safe to delegate this to an agent" — not a product feature list.

1. **Intent can be verified** — goal, boundaries, acceptance criteria given as structured input, not inferred.
2. **Context is complete** — business, data, permission, execution context available; the agent isn't guessing.
3. **Plan can be reviewed** — the generated SQL/DAG/steps are human-readable, system-verifiable, risk-reviewable *before* execution.
4. **Execution is controlled** — permissions, target environment, and Skill selection are constrained by Policy.
5. **Results can be validated** — data quality, business-definition checks, reconciliation, lineage; a successful run is not proof of a correct run.
6. **Failures can be recovered** — the system knows whether to retry, roll back, or escalate to a human.
7. **Actions are auditable** — plans, approvals, executions, results, and version changes are recorded across the lifecycle.

Gates 5 and 7 (validate, audit) are the ones most hand-built pipelines skip — they require infrastructure (reconciliation checks, an audit trail) that's easy to omit when "the query ran" is mistaken for "the query is right." See [Write-Audit-Publish](write-audit-publish.md) (gate 5) and [Data Contracts](data-contracts.md) (gates 2 and 5 together).

## Three Foundations

- **Correctness** has four levels: Syntactic → Execution → Data → Business. Valid, running SQL can still be *business*-wrong (which "Revenue" definition did it use?). This is a finer-grained version of [Correctness Layer](correctness-layer.md)'s probabilistic/deterministic split — it names where in the stack a wrong-but-plausible answer can hide.
- **Capability** — without reusable Skills, an agent just produces more one-off scripts: hard to standardize, audit, roll back, or get structured feedback from.
- **Context** — Business, Data, Execution, Organisational. Without it, the agent guesses; see [Semantic Layer](semantic-layer.md) as the canonical Business/Data context source.

## Five-Layer Agentic Data Stack

| Layer | Name | Role |
|---|---|---|
| L5 | Business Intent | People define outcomes (goal, scope, time window, quality/cost/risk bounds, approval conditions, acceptance criteria), not implementation steps |
| L4 | Agentic Orchestration Control Plane | Agent plans against a goal; control plane enforces policy boundaries; routes to a human gate when a plan crosses one |
| L3 | Semantic & Knowledge | Business rules, metadata, lineage, metrics, glossary, data contracts, execution memory — what the agent must consult before acting |
| L2 | Data Engineering Harness | The controlled gateway itself: Skill definition → permission check → context injection → validation → observability → rollback |
| L1 | Deterministic Execution (Runtime) | Ordinary deterministic code executes: SQL engines, lakehouses, Spark/Flink, sync tools (SeaTunnel), schedulers (DolphinScheduler) |

Traditional stack organization is Storage → Compute → Orchestration → Governance → BI. The agentic reorganization is Intent → Control → Semantic → Harness → Runtime — governance and context move from being bolted on at the edges to being load-bearing layers the agent must pass through.

## Minimum Viable Loop

`Intent → Context → Plan → Skill → Execute → Validate → Review → Feedback`, continuously, not one-shot generation. On failure: `Plan → Execute → Observe → Diagnose → Repair → Validate → Continue / Rollback / Escalate`, backed by an **Execution Memory** of context, history, and operational experience.

## Design Principles

**A Skill is not a Prompt, and not a Tool API.**
- A *Prompt* shapes how an agent responds.
- A *Tool API* exposes a low-level operation and leaves failure handling to the caller.
- A *Skill* is the structured unit that determines whether an action can execute *safely*: Input, Context, Policy, Execution, Validation, Rollback, Output.

This sharpens [Claude Skills](claude-skills.md)'s existing Skill-vs-AGENTS.md distinction with a second axis: Anthropic's skill pairs (router + process) are Harness-sense Skills precisely because they carry context-injection and validation behavior, not just instructions.

**CLI/API for agents, GUI for humans.** Agents need structured, testable, version-controllable I/O (Skills, MCP, SDKs); humans need to inspect plans, review SQL/DAGs/logs, and take control on exceptions. Flow: human sets a goal in a GUI → agent calls Skills via CLI/API → Runtime executes → GUI surfaces the plan and risk → human approves or intervenes.

**Human-in-the-loop protects risk boundaries, not every step.**

| Risk | Handling | Examples |
|---|---|---|
| Low | Auto-execute | read metadata, query dev, generate docs |
| Medium | Execute and notify | create dev tasks, low-cost validation |
| High | Human approval | write to production, schema changes, modify critical metrics |
| Critical | Block or dual approval | delete core tables, bulk overwrites, sensitive-data operations |

This generalizes [Human-in-the-Loop](human-in-the-loop.md)'s finding (direction-level feedback beats artifact-level review) with a complementary axis: *which* actions get a human in the loop at all should be set by blast radius, not by habit.

## Open-Source Case Studies

- [Apache SeaTunnel](../entities/apache-seatunnel.md) — data integration exposed as a Skill set (discover → generate job → run → structured feedback → error-driven repair).
- [Apache DolphinScheduler](../entities/apache-dolphinscheduler.md) — orchestration as a Skill: generate DAGs, create real versioned assets, repair failed workflows, surface a GUI for human review.

Both are concrete L1+L2 implementations: deterministic engines underneath, a Skill-shaped interface on top, so the agent is stochastic only in *which Skill to call with what parameters*, never in how the engine itself executes.

## Evolving the Harness Itself

Everything above describes a hand-designed Harness. [Harness Evolution](harness-evolution.md) covers what happens when the Harness is instead improved automatically by an LLM proposer iterating against feedback — a practical form of recursive self-improvement at the agent-system level — and why that process reliably overfits to its evolve set unless the search itself is regularized (leakage screening, a noise-adjusted acceptance floor, cost-aware acceptance, structural pruning). It's the dynamic, time-dimension counterpart to the static sign-off gates above: the gates ask whether a given harness is safe to run, while harness evolution asks whether the *process that produced* the harness can be trusted to generalize.

## Adoption Path

Three stages: **Collaborative Assistance → Controlled Execution → Governed Autonomy.** Start with high-frequency, low-risk, verifiable tasks (discovery, SQL drafting, DAG assembly, log diagnosis); keep full autonomy away from production deletes/overwrites, critical metric definition changes, and unapproved schema changes. This parallels [Agents in Data Engineering](agents-in-data-engineering.md)'s three maturity levels (Chat-Phase → Autonomous → Dedicated Tooling), viewed from the governance side rather than the tooling side.

## Related Concepts

- [Correctness Layer](correctness-layer.md) — the deterministic-core architecture one layer of the Harness is built from
- [Agents in Data Engineering](agents-in-data-engineering.md) — maturity-level framing of the same progression
- [Data Contracts](data-contracts.md) / [Write-Audit-Publish](write-audit-publish.md) — concrete implementations of gates 2 and 5
- [Claude Skills](claude-skills.md) — a real-world example of Skill-not-Prompt
- [Semantic Layer](semantic-layer.md) — the canonical L3 context source
- [Human-in-the-Loop](human-in-the-loop.md) — complementary finding on *how* humans intervene, once this concept establishes *when*
- [Harness Evolution](harness-evolution.md) — regularizing automated, recursive improvement of the Harness itself
- [Agent Security: Defense-in-Depth](agent-security-defense-in-depth.md) — the same "deterministic layer below the agent" structure, applied to containing unauthorized actions rather than guaranteeing correct output
- [Source: Rebuilding Data Engineering with Harness Engineering](../sources/harness-engineering-agentic-data-engineering.md)
- [Source: RRSI — Regularized Recursive Self-Improvement of Agent Harnesses](../sources/rrsi-regularized-recursive-self-improvement.md)
