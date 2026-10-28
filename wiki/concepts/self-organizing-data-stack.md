---
tags: [data-n-ai, concept, agents, pipelines, orchestration, data-modeling]
sources: ["raw/data-n-ai/articles/2026-10-14-the-self-organizing-data-stack.md"]
updated: 2026-10-28
---

# Self-Organizing Data Stack

A proposed architecture (Ananth Packkildurai, 2026-10) in which an **orchestration engine maintains the dependency graph and physical tables**, while humans own only **meaning** — definitions, policies, judgments. The DAG flips from a hand-drawn input to a runtime output. See [source summary](../sources/2026-10-14-the-self-organizing-data-stack.md).

## Why it is proposed

Manual DAGs plus cheap agent code generation produce table sprawl: refactoring is risky, copying is cheap. Agents as *consumers* remove the need for human-legible star schemas, so the model can be reshaped continuously.

## Core Design

- **Asset = contract**: stable identity + semantic meaning + grain + per-consumer commitments; implementation is swappable underneath.
- **Five loops**: Synthesize → Consolidate → Verify & Repair → Coordinate → Escalate.
- **Semantic layer is load-bearing**: missing meaning triggers escalation, never a SQL guess.
- **Decision log**: requirements link to authorising decisions/policies (W3C PROV, OpenLineage).
- **Operator controls**: freeze domain, pin version, replay proposal on history. Debug from unmet commitments.
- **Metabolism**: retire/demote assets when commitments expire.

## Where It Sits Relative to Existing Pages

| Existing idea | Relationship |
|---|---|
| [Semantic Layer](semantic-layer.md) | Prerequisite; the engine can only reorganise what it can prove equivalent from formal definitions |
| [Data Contracts](data-contracts.md) | Generalised: contracts become consumer *commitments* the engine enforces on every graph change |
| [Correctness Layer](correctness-layer.md) | "Adversarial verification; never let an agent grade its own work" is the same deterministic-core principle |
| [Self-Healing Architecture Requirements](self-healing-architecture-requirements.md) | Repair loop + versioned atomic activation echo context capture and git-for-data pillars |
| [Data Versioning and Branching](data-versioning-and-branching.md) | Atomic activation, pinning and replay-against-history need snapshot/branch primitives |
| [Harness Engineering](harness-engineering.md) | Same split: agent proposes, deterministic control plane gates; here applied to the runtime, not just the IDE |
| [Write-Audit-Publish](write-audit-publish.md) | The Verify → Coordinate steps are a graph-level WAP |

## Stopgap: Context Pipeline (ECL)

Extract, Contextualize, Link: extract, version and link entity definitions and domain decisions into an authoritative layer alongside current pipelines, so coding agents can see business rules not buried in 400-line SQL.

## Open Questions

- Can equivalence of two compiled specs be proven in practice (needed for safe Consolidate)?
- Who is the engine? No implementation is named in the source.
- How to bound autonomous reorganisation cost and blast radius beyond freeze/pin controls.
