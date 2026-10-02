---
title: Harness Engineering for Agentic Data Engineering
type: source-summary
source_url: hackernoon.com/rebuilding-data-engineering-with-harness-engineering-a-new-paradigm-for-the-agent-era
source_title: "Rebuilding Data Engineering with Harness Engineering: A New Paradigm for the Agent Era"
source_author: Nie Lifeng
source_publisher: HackerNoon
source_date: 2026-09-27
source_type: opinion / thought leadership (AI-assisted per HackerNoon label)
ingested: 2026-10-01
tags: [harness-engineering, agentic-data-engineering, agentic-data-stack, ai-agents, data-governance, skills, modern-data-stack]
note: Paraphrased summary plus clearly labelled extensions. Not a reproduction of the article. Diagrams in the original were not visible when summarised.
---

# Harness Engineering for Agentic Data Engineering

## 1. Thesis
- The Modern Data Stack (MDS) was designed for humans, not agents. Humans silently fill in missing context (business terms, ambiguity, risk, accountability). Agents do not.
- Generative AI pushes the cost of producing SQL, code, DAGs and config toward zero. These become commodities.
- The scarce resources become: context, verification, governance, controlled execution, accountability.
- The real problem is not generating artifacts but safely delivering them to production.
- Most dangerous failure mode: not an agent that fails, but an agent that produces a wrong result and successfully executes it in production (Wrong Data -> Wrong Decision -> Wrong Action).
- Core claim: agents do not primarily lack intelligence; they lack the engineering system that turns intelligence into reliable outcomes. Between generation capability and production capability sits an engineering system, the Harness.

## 2. Context: Platform Evolution
- Platforms (Snowflake, Databricks) are converging on four capabilities: Context, Capability, Governance, Execution.
- Snowflake path (per article): Data Warehouse -> Data Cloud -> AI work interface -> enterprise agent platform.
- Databricks path (per article): Data Lake -> Lakehouse -> Data + AI engineering -> agent-ready execution platform.
- "Agent-ready" means: data discoverable, schemas understandable, metrics have clear business definitions, workflows executable, actions auditable.
- Users shift from humans (data engineers, analysts, BI users, platform engineers) to agents (coding, data, business, operations agents).
- Humans need UIs, docs, guided workflows. Agents need APIs, Skills, context, policies, structured feedback.
- Era sequence: Database Era -> Big Data Platform Era -> Modern Data Stack Era -> Agentic Data Stack Era (Context, Skills, Control, Harness as first-class concerns).
- Workflow shift:
  - Old: Write SQL -> Build Pipeline -> Configure DAG -> Monitor -> Fix
  - New: Understand Intent -> Plan -> Invoke Capabilities -> Execute -> Validate -> Learn

## 3. What the Modern Data Stack Got Right and Where It Stops
- Got right: modularity, cloud resources, standardised tools, composability.
- Toolchain layers: Source, Ingestion, Storage, Transformation, Orchestration, Governance, BI.
- Limit: much "automation" still depends on humans filling gaps.
- Three concerns with agents: Complexity (more hidden dependencies and one-off scripts), Accountability (who verifies, approves, owns), Production risk (incorrect SQL that runs successfully).
- Six engineering requirements: Validation, Ownership, Lineage, Security, Rollback, Audit.
- Data engineering has no "close enough": errors flow into financial reports, operations, customer decisions.

## 4. The Harness
A controlled engineering layer between agents and underlying tools. Provides controls, context, verification and recovery so AI output is trusted, verifiable, controlled, recoverable, accountable.

### 4.1 Three types of evidence required
| Evidence | Question it answers |
|---|---|
| Outcome | Does it genuinely speed delivery, catch errors earlier, reduce rework, rather than just shifting work to review? |
| Process | Is every step explainable, traceable, recoverable? Can failures be attributed to Context, Skill, Runtime or Policy? Can it retry, roll back, hand back to a human? |
| Governance | Are high-risk actions explicitly constrained by Policy? Which run automatically vs need approval? Does the audit trail show who did what, when, why, and the result? |

### 4.2 Seven sign-off gates (production-readiness checkpoints)
Purpose: answer "when is it safe to delegate?" Not product features.
1. Intent can be verified: goals, boundaries, acceptance criteria as structured input.
2. Context is complete: business, data, permission, execution context available; no guessing.
3. Plan can be reviewed: SQL, DAGs, task steps human-readable, system-verifiable, risk-reviewable.
4. Execution is controlled: permissions, target environments, execution paths, Skill selection within Policy.
5. Results can be validated: data quality, business-definition checks, reconciliation, lineage validation; success of execution is not proof of correctness.
6. Failures can be recovered: system knows whether to retry, roll back or escalate.
7. Actions are auditable: plans, approvals, executions, results, version changes recorded across the lifecycle.

Worked example used in discussion: "daily dataset of revenue from high-value customers, approved revenue definition, no production overwrite, human approval if result moves >5%."
- Gate 1: high-value = defined cohort; revenue = recognised revenue; constraints stated.
- Gate 3: reviewer spots a join that duplicates rows for customers with multiple accounts.
- Gate 4: agent may write to dev schema only, using approved Skills.
- Gate 5: total reconciles to finance ledger; no null customer IDs.
- Gate 6: source API timeout -> retry twice -> escalate rather than leave a half-loaded table.
- Gate 7: months later, can answer who approved the metric change and what ran.
- Observation: gates 5 and 7 are the ones most pipelines skip.

### 4.3 Three foundations
**Correctness** has four levels: Syntactic -> Execution -> Data -> Business. Valid SQL can still be business-wrong (e.g. "Revenue" = order amount vs paid vs recognised vs net). Common failures: wrong source, wrong metric definition, wrong time window, join duplicates, ignored business rules.

**Capability**: without reusable Capabilities, agents just produce more temporary scripts (one-off, hard to standardise, audit, roll back, poor feedback). A Capability is a reusable structured Skill with defined inputs, outputs, policies, validation and recovery.

**Context**: four types: Business, Data, Execution, Organisational. Without context the agent guesses.

### 4.4 Skill-first software
- Traditional software is UI-first. Agent-native software must be Skill-first: Skills discoverable, context injectable, policies constraining actions, feedback machine-consumable, results verifiable.

## 5. Five-Layer Agentic Data Stack
Rule: agents never call underlying tools directly; they go through the Harness, with L3 context and L4 controls defining what is permitted.

| Layer | Name | Role | Example (running revenue case) |
|---|---|---|---|
| L5 | Business Intent | People define outcomes, not steps. Eight dimensions: goal, data scope, time window, quality requirements, cost constraints, risk boundaries, approval conditions, acceptance criteria | "Daily high-value-customer revenue dataset, approved definition, no prod overwrite, approval if >5% change" |
| L4 | Agentic Orchestration Control Plane | Human defines goal -> agent plans -> control plane enforces boundaries -> human intervenes when necessary. Checkpoints: goal description, skill check, policy check, human gate, audit, multi-task configuration | Plan includes a production write -> paused for human approval |
| L3 | Semantic & Knowledge | Context agents must consult before acting: business rules, metadata, lineage, metrics, glossary, ontology, data contracts, execution memory | Says "revenue" = recognised revenue, which table is authoritative, which fields are sensitive |
| L2 | Data Engineering Harness | Controlled gateway: Skill definition -> permission check -> context injection -> validation -> observability -> rollback | Checks agent may write to dev only, injects definition, validates output, can roll back |
| L1 | Deterministic Execution (Runtime) | Executes SQL, sync, batch and CDC, scheduling; produces logs and status. Components named: databases/warehouses, lakehouses/Iceberg, Spark, Flink, SeaTunnel, DolphinScheduler, SQL engines, data-quality engines | Spark runs the transform, SeaTunnel syncs, DolphinScheduler schedules |

- Traditional stack organisation: Storage -> Compute -> Orchestration -> Governance -> BI.
- Agentic stack organisation: Intent -> Control -> Semantic -> Harness -> Runtime.
- Four questions the layers answer: where does the agent get its goals; how does it understand enterprise capabilities and meaning; which capabilities can it invoke; who controls execution, validation and rollback.

## 6. Minimum Viable Loop
Intent -> Context -> Plan -> Skill -> Execute -> Validate -> Review -> Feedback
- Continuous loop, not one-shot generation.
- Feedback loop variant: Plan -> Execute -> Observe -> Diagnose -> Repair -> Validate -> Continue / Rollback / Escalate.
- Supported by Execution Memory (context, execution history, operational experience).
- Feedback sources: execution state, logs, metrics, data quality, lineage impact, human feedback.
- Agent responses: auto-repair when root cause is clear; adjust plan; stop or escalate when unsafe.

## 7. Design Principles
**A Skill is not a Prompt.** A Prompt shapes how an agent responds; a Skill determines whether it can execute safely. Skill components: Input, Context, Policy, Execution, Validation, Rollback, Output. Distinct from a Tool API, which exposes a low-level operation and leaves failure handling to the caller.

**CLI for agents, GUI for humans.**
- CLI/API: structured I/O, programmatic invocation, testability, version control, Skills, MCP, SDKs, declarative config.
- GUI: inspect plans and artifacts, review SQL/DAGs/logs/results, monitor permissions and risk, take control on exceptions.
- Flow: human sets goal in GUI -> agent calls Skills via CLI/API -> Runtime executes -> GUI shows DAGs, SQL, logs, risk -> human approves or takes over.

**Human-in-the-loop protects risk boundaries, not every step.**
| Risk | Handling | Examples |
|---|---|---|
| Low | Auto-execute | read metadata, query dev, generate docs |
| Medium | Execute and notify | create dev tasks, low-cost validation |
| High | Human approval | write to production, schema changes, modify critical metrics |
| Critical | Block or dual approval | delete core tables, bulk overwrites, sensitive-data operations |
Principles: intervene by risk; approve critical decisions not mechanical actions; humans define Policy, agents operate within it.

**Clear ownership.**
- Business sign-off: owners define goals, constraints, acceptance criteria.
- Platform governance: policies, permissions, approvals, rollback, environment boundaries.
- Automated execution: agents and Harness supply context, plan, invoke Skills, return logs and validation.
- Audit: reviewers step in for high-risk, uncertain, or acceptance-conflicting decisions.
- Human intervention reserved for: high-risk actions on critical data, unrecoverable exceptions with unclear retry/rollback boundary, results conflicting with acceptance criteria.

## 8. Case Studies (Open Source Implementations)
**Apache SeaTunnel CLI: data integration as a Skill (L1 + L2).**
- Capabilities: source/schema/table/field discovery; automatic job generation; batch and CDC; structured feedback (status, logs, row counts, errors); error-driven repair and retry.
- Skill set: DiscoverSource(), InspectSchema(), CreateBatchSync(), CreateCDC(), ValidateMapping(), RunSyncJob().
- Loop: Execute -> Logs -> Repair -> Retry.
- Future direction: context-aware mapping, broader Data Flow Skill, self-healing integration, AI-ready pipelines.

**Apache DolphinScheduler: orchestration and engineering order.**
- Capabilities: generate workflow DAGs; auto-establish dependencies; create real assets (Definitions, Instances, Versions); execute and monitor; repair failed workflows and rerun nodes; GUI for human review.
- Agentic workflow: human goal -> agent plan -> policy check -> DolphinScheduler executes -> agent repairs / human reviews.
- Future direction: policy-aware orchestration, human review gates, self-healing workflows, multi-agent coordination.

**End-to-end demo test:** Discover data -> create integration task -> run sync -> generate SQL transforms -> build DAG -> execute -> read logs and diagnose -> repair and retry -> present for human review. The point is orchestrating multiple deterministic systems through a Harness, not generating SQL.

## 9. Role of the Data Engineer
- Progression: SQL Writer -> Pipeline Builder -> Workflow Operator -> Platform Engineer -> Agent Capability Designer.
- Emerging design roles: Context Designer, Skill Designer, Policy Designer, Evaluation Designer, Agent Engineering Commander.
- Enduring core skills: data modelling, business abstraction, architecture design, data governance, risk judgement, accountability.

## 10. Adoption Path
- Start with high-frequency, low-risk, verifiable tasks: discovery/metadata/schema understanding; SQL drafting, rule validation, DAG assembly; integration task creation, parameter orchestration, environment checks; log diagnosis, repair suggestions, retry orchestration.
- Avoid full autonomy for: deleting/overwriting/bulk-modifying production data; changing critical metric definitions or cross-domain master data; schema changes or high-cost writes without approval and rollback; cross-team workflows with unclear ownership or unverifiable results.
- Three stages: Collaborative Assistance -> Controlled Execution -> Governed Autonomy.
- Principle: start small, prove reliability, expand the boundary of autonomy.

## 11. Conclusion Formulas (article)
- Humans define the goal; agents execute; the Harness governs delivery.
- Business Intent + Agent Intelligence + Enterprise Context + Engineering Skills + Policy & Control + Human Review = Trusted Agentic Data Engineering.
- The agent generates; the Runtime executes; the Harness makes the outcome trustworthy.

## 12. Discussion Notes (extensions, NOT from the article)
**Where stochasticity lives vs where determinism is enforced.**
- The agent is stochastic only in choosing which Skill to call and with what parameters. Skill implementations and Runtime engines are ordinary deterministic code.
- Article-aligned controls: narrow typed Skill interfaces (no free-form production SQL); pre-execution permission, policy and context checks; deterministic engines do the work; post-execution validation catches technically successful but wrong results.
- Added extensions: idempotent, version-pinned Skills so retries and replays give identical outcomes; golden-set tests for Skills (fixed inputs, asserted outputs).
- Caveat: this makes execution deterministic, not the agent's decisions. Two runs of the same intent may yield different plans. Controls (risk-tiered approval, validation gates, rollback) bound the damage rather than eliminate variance.

## 13. Concept Index
Agent-ready platform; Agentic Data Stack; Agentic Orchestration Control Plane; Audit; Business Intent; Capability; Context (business/data/execution/organisational); Correctness levels; CLI vs GUI; Deterministic Execution; Execution Memory; Feedback Loop; Governance; Governed Autonomy; Harness; Human-in-the-loop (risk tiers); Minimum Viable Loop; Modern Data Stack; Outcome/Process/Governance evidence; Policy; Rollback; Semantic Layer; Seven sign-off gates; Skill vs Prompt vs Tool API; Skill-first software; SeaTunnel; DolphinScheduler.

## 14. Source
hackernoon.com/rebuilding-data-engineering-with-harness-engineering-a-new-paradigm-for-the-agent-era
