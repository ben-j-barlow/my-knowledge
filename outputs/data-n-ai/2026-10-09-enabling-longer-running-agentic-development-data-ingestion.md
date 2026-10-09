---
tags: [data-n-ai, synthesis, agents, harness-engineering, pipelines, testing, etl]
sources:
  - wiki/concepts/feature-lists.md
  - wiki/concepts/premature-completion-declaration.md
  - wiki/concepts/session-continuity.md
  - wiki/concepts/ralph-loop.md
  - wiki/concepts/iterative-repair-loops.md
  - wiki/concepts/harness-engineering.md
  - wiki/concepts/data-contracts.md
  - wiki/concepts/write-audit-publish.md
  - wiki/concepts/correctness-layer.md
  - wiki/concepts/human-in-the-loop.md
  - wiki/concepts/agent-security-defense-in-depth.md
  - wiki/concepts/data-quality-observability.md
  - wiki/concepts/agent-configuration-audit.md
  - wiki/concepts/agents-in-data-engineering.md
  - wiki/concepts/local-vs-cloud-data.md
  - wiki/concepts/harness-evolution.md
  - wiki/concepts/semantic-layer.md
  - wiki/concepts/agentic-analytics.md
  - wiki/concepts/agents-md.md
  - wiki/concepts/context-engineering.md
  - wiki/concepts/claude-skills.md
  - wiki/concepts/duckdb-for-agents.md
  - wiki/entities/anthropic.md
updated: 2026-10-09
---

# Enabling Longer Running Agentic Development for Data Ingestion

## 1. Summary

A coding agent can be trusted with a multi-hour ingestion task when three
questions are answered by something other than the agent:

- **Is it allowed?** Answered by permissions the agent cannot change.
- **Is it done?** Answered by a verification command, not by the agent's report.
- **Is it right?** Answered by executable data contracts and a diff against
  production data.

Most repositories answer all three in prose: a rules file, a definition of
done, a list of data gotchas. Prose is useful context, but it does not hold
under a long unattended run. This document describes five components that
replace prose with checks, and shows each one applied to a toy repository.

| # | Component | Replaces |
|---|---|---|
| 1 | Permissions that bind | "Never do X" sentences in a rules file |
| 2 | One verification command, ending in a real-data dry run | "Run the tests before you finish" |
| 3 | Executable data contracts | Prose gotchas in a data catalog |
| 4 | Task contract, expected diff, and feature list | A task described in chat |
| 5 | A loop with stop conditions, saved state, and an independent evaluator | The agent deciding when to stop and grading its own work |

With these in place the human moves from supervising steps to two
checkpoints: approving the task contract before work starts, and approving
the merge at the end. The overall framing is [Harness Engineering](../../wiki/concepts/harness-engineering.md); each section below links to its supporting pages.

## 2. Why long runs fail

Four failure modes grow with run length.

**The agent says it is done when it is not** ([Premature Completion Declaration](../../wiki/concepts/premature-completion-declaration.md)). Models are systematically
overconfident about their own work, and asking for more objectivity does not
fix it. In one cited experiment, the same model with the same prompt produced
a non-working result in 20 minutes for $9 when run bare, and a working one in
6 hours for $200 when run as planner, generator, and separate evaluator. The
only variable was the structure around the model.

**Code that runs is not code that is correct** ([Agents in Data Engineering](../../wiki/concepts/agents-in-data-engineering.md), [Correctness Layer](../../wiki/concepts/correctness-layer.md)). An ingestion transform can
parse, execute, and load plausible rows while being wrong: a missed unit
conversion, a duplicated key, a join that changes the grain. Nothing errors.
The wrong numbers are discovered downstream, later.

**The agent routes around friction** ([Agent Security: Defense-in-Depth](../../wiki/concepts/agent-security-defense-in-depth.md)). A long run will hit a locked file, a
missing path, or an expired credential. An agent pursuing a legitimate goal
looks for a workaround, and the workaround may cross a boundary no human
operator would cross. No malicious prompt is needed.

**State is lost between sessions** ([Session Continuity](../../wiki/concepts/session-continuity.md)). Any task longer than one context window
crosses a boundary where reasoning is summarised or dropped. A fresh session
may redo finished work, or "correct" a deliberate decision it cannot know was
deliberate.

A fifth finding explains why the answer is not more instructions ([Agent Configuration Audit](../../wiki/concepts/agent-configuration-audit.md), [AGENTS.md](../../wiki/concepts/agents-md.md)). Across 288
runs on real tasks, context files changed how agents worked but not how often
they succeeded. On long policy handbooks, the best of 30 model configurations
followed the rules strictly 36.2% of the time. Instructions carry context;
they do not carry guarantees.

## 3. The toy repository

The examples use an invented repository, `parcel-lake`, which ingests carrier
rate cards and shipment files into a local lake.

```
parcel-lake/
  libs/            tested libraries
  apps/            thin command-line runners, one per pipeline
  legacy/          older scripts being migrated, kept as-is
  docs/catalog/    one page per table, with a "Gotchas" section
  locations.json   the single source of deployment paths
  AGENTS.md        rules and conventions for the agent
```

Its conventions:

- **Medallion lake on local disk.** Bronze holds raw vendor files, silver
  holds cleaned tables, gold holds business tables. Gold transforms read
  silver from files.
- **No development environment.** A new transform runs against production
  paths the first time it is trusted.
- **Scheduled jobs run from a second checkout** on the same machine. A sync
  job resets that checkout to the main branch. The pipelines themselves do
  not call git.
- **An incremental ledger** records how far each gold table has been advanced.
- **A reference table**, `carrier_registry`, is maintained by hand and must
  not be edited by tooling.
- **Rules in `AGENTS.md`:** do not edit the registry, do not delete shared
  output, do not add dependencies without asking, do not copy patterns from
  `legacy/`.

One consequence matters for everything below: because the scheduler checkout
tracks main, **merging to main is the production deploy.** That makes the
merge the natural single human gate. Everything before it can be autonomous,
provided the agent cannot write to the lake or to main.

## 4. Component 1: Permissions that bind

### Advisory and binding rules

An **advisory** rule is a sentence the agent is asked to follow: "never edit
the carrier registry". The agent usually complies. It can also misread the
rule, lose it after a context reset, or decide a workaround is justified.

A **binding** rule makes the action fail whatever the agent decides. If the
agent's process has no write access to the registry file, an edit errors out.
The principle from the [agent-security literature](../../wiki/concepts/agent-security-defense-in-depth.md): a safeguard the agent can
decline to invoke, or reconfigure, is not a safeguard.

Every rule in the toy repository's `AGENTS.md` is advisory.

### Tier actions by blast radius

Human approval should protect risk boundaries, not every step ([Harness Engineering](../../wiki/concepts/harness-engineering.md), [Human-in-the-Loop](../../wiki/concepts/human-in-the-loop.md)).

| Tier | Handling | `parcel-lake` actions |
|---|---|---|
| Low | Automatic | Read the repository; query the lake read-only; edit code on a task branch; commit to that branch; run tests, linters, and dry runs; write inside the task's overlay directory |
| Medium | Do, then notify | Open a pull request; update catalog pages and docs |
| High | Human approval | Merge to main; first real write of a new or changed transform; advance the ledger; add or change a scheduled job; add a dependency; edit `locations.json` |
| Critical | Blocked | Edit `carrier_registry`; delete shared output; touch secrets; touch the scheduler checkout or the schedule |

### Three independent layers

Each layer should fail for a different reason, so one mistake does not expose
the lake.

1. **Filesystem.** Run long tasks as an operating-system user with read-only
   access to the lake and write access only to an overlay directory. This is
   the strongest layer, because the agent cannot reconfigure it from inside
   its session, and it works with any agent tool.
2. **Agent tool.** Deny rules and pre-execution hooks that block pushes to
   main, dependency changes, and writes outside the working tree. The tool's
   own settings file must be protected too, or the agent can edit the rule
   away.
3. **Version control.** Branch protection so main accepts only a reviewed
   pull request.

Run long tasks from a **third checkout**, the same pattern the scheduler
uses, so a multi-hour run never collides with the tree a person is editing.

### Signals only reduce authority

If a monitor or check detects something odd, the response is to pause or
narrow what the agent can do. No signal should ever grant more access
(design rule 3 in [Agent Security: Defense-in-Depth](../../wiki/concepts/agent-security-defense-in-depth.md)).

## 5. Component 2: One verification command

A single entry point that the agent, the loop, and a person all run. Each
layer runs only if the one before passes.

| Layer | Check | Catches |
|---|---|---|
| 1. Static | Formatter, linter, type checker | Syntax and style |
| 2. Unit | Tests for the touched libraries and runners, on small fixtures | Logic errors and edge cases |
| 3. Runtime | The real runner in dry-run mode, reading production inputs | Path binding, real schemas, real volumes: what fixtures hide |
| 4. Data | Contract assertions on the dry-run output, plus a diff against the live table | Wrong numbers from code that ran without error |

Unit tests alone are not enough because their isolation is what blinds them
(see the three-layer termination check in [Premature Completion Declaration](../../wiki/concepts/premature-completion-declaration.md)):
a fixture never has the column that turned out to be a string, or the ten
million rows that expose a bad join.

Failure messages should say what to check next, not only what failed ([actionable error feedback](../../wiki/concepts/premature-completion-declaration.md)). "Layer
4: 312 duplicate keys on (carrier_id, lane_id, valid_from); the silver table
has two files for 2026-09-30" lets the agent repair without a human.

### The fast inner loop and the real-data outer gate

The recommended agent workflow for data pipelines ([Local vs. Cloud Data](../../wiki/concepts/local-vs-cloud-data.md), [Agents in Data Engineering](../../wiki/concepts/agents-in-data-engineering.md)) has four steps:

1. **Inspect** production data before writing any transform: schema, sample
   rows, null rates, duplicates. A read-only query server gives the agent
   this.
2. **Unit test locally** on a handful of fixture rows, in sub-second time.
3. **Check against the data contract.**
4. **Deploy.**

The principle that carries over to an all-local lake: keep the agent's inner
loop on small, fast data (layers 1 and 2), and gate on real data once the
inner loop is green (layers 3 and 4).

## 6. Dry runs

### What a dry run does

A dry run executes a real pipeline against real production inputs and cannot
change anything.

1. **Reads production for real**, with actual schemas and volumes.
2. **Runs the whole transform and the audit.** Contract assertions execute,
   so a unit bug fails here.
3. **Writes nowhere, or only to an overlay.**
4. **Suppresses every side effect:** advancing the ledger, sending
   notifications, moving or renaming input files, and anything another job
   would read as "this already ran".
5. **Emits a report and a meaningful exit code.**

A report for the toy repository might read:

```
dry-run: build-gold-lane-rates   task: fix-fuel-surcharge
reads:   silver.rate_cards (overlay), silver.lanes (production)
writes:  overlay/fix-fuel-surcharge/gold/lane_rates   (4,812,330 rows)
contract: 6/6 assertions passed
diff vs production gold.lane_rates:
  rows added 0, removed 0, changed 18,204
  changed columns: total_rate
  changed keys:    carrier_id = 'NRX', valid_from >= 2026-07-01
expected diff: MATCH
exit 0
```

### Two modes

- **Plan-only** computes and reports without persisting. Cheap; good for a
  single transform.
- **Overlay** writes the would-be output under a separate root, one directory
  per task. This allows full-table diffs and lets a downstream step read the
  result.

### Building it so the flag cannot lie

Scattering `if not dry_run:` through a runner is fragile: one missed branch
is a real write. The safer design is for runners to receive their output
location as an argument. A dry run then passes an overlay root and a no-op
ledger, so writes go somewhere else by construction.

| | Fragile | Robust |
|---|---|---|
| Mechanism | A boolean checked before each write | The output root and ledger are injected by the entry point |
| Failure mode | A forgotten check writes to production | None inside the runner; it has no production path to write to |
| Test | Hard to prove | Run in dry-run mode and assert nothing outside the overlay changed |

Under a read-only lake user, the filesystem enforces this as well.

### Dry runs across a medallion chain

Plan-only cannot chain. If a task changes a silver transform, gold must read
the new silver to say anything useful. Without a persisted overlay, gold
silently reads the old production silver and reports a result that does not
reflect the change.

The rule is **overlay-first read, production fall-through:**

- Writes always go to the task's overlay.
- Each read resolves to the overlay copy if one exists, otherwise production.

```python
def resolve_read(table: str, prod_root: Path, overlay_root: Path | None) -> Path:
    if overlay_root and (overlay_root / table).exists():
        return overlay_root / table
    return prod_root / table
```

| Task changes | Run | Gold reads |
|---|---|---|
| Gold only | Gold to overlay | Production silver |
| Silver | Silver, then gold, each to overlay | Overlay silver |
| Bronze parsing | Bronze, silver, gold in order | Overlay at each hop |

Each layer gets its own contract check and its own diff, so a bad silver
change is caught at silver and not discovered as an unexplained gold
difference.

Points that need care:

- **Resolve per table, not per partition.** If the overlay holds only the
  rewritten dates and the rest falls through, the result is a silent mix of
  old and new logic. Either overlay the complete table, or give the runner an
  explicit window and compare only inside it.
- **Copy the ledger.** A dry run reads a copy of the incremental ledger and
  writes its advance to that copy. Otherwise it either advances the real
  ledger or reads a watermark that does not match the overlay data.
- **Limit volume.** Declare a date or key filter in the task contract instead
  of overlaying full tables on every iteration.
- **Put the resolver in the shared path layer**, in front of the path
  constants, so no runner can read or write production by accident.

### Sandbox root or development environment

A full development lake has real costs: a copy to store, and drift from
production. Dry runs with overlays avoid both, because reads stay live.

A development copy (trade-offs in [Local vs. Cloud Data](../../wiki/concepts/local-vs-cloud-data.md)) adds value only for what a dry run cannot exercise: the
real write path (atomic swap, partition layout, ledger advance), a downstream
consumer reading the new output, and concurrency with a scheduled job.

The middle option is a **sandbox root** (a cousin of the branching and shared-context ideas in [DuckDB for Agents](../../wiki/concepts/duckdb-for-agents.md)): reads fall through to production,
writes go to a per-task root, and the agent may write real tables there, run
downstream jobs against them, and discard the lot. It is the overlay
mechanism with write-and-read-back allowed. The sandbox must be selected by
whoever launches the run, not by the agent, or the agent can point itself
back at production.

## 7. Component 3: Executable data contracts

### What a contract is

An executable specification of a table ([Data Contracts](../../wiki/concepts/data-contracts.md)): what one row means, the rule for each
column, and the invariants that must hold. It replaces "be careful with this
table" with assertions that pass or fail.

### Golden tests and contract assertions

These are different checks and both are needed.

| | Golden test | Contract assertion |
|---|---|---|
| Input | A small fixture written by hand | Any real output |
| Question | Does the code produce the expected rows? | Does the data satisfy the invariants? |
| Runs at | Layer 2, locally | Layer 4, and as the audit before publish |
| Catches | Logic bugs, edge cases | Unit errors, duplicates, drift, bad vendor files |

They connect through the contract: each rule gets a fixture row that would
violate it. A rule about deduplication gets a duplicated row; a rule about
quality flags gets a flagged row; the expected output omits both.

### A minimal shape

Keep the contract as code next to the table's catalog page. One file per
table, each assertion a query that returns the violating rows, so an empty
result means pass.

```python
# docs/catalog/gold/lane_rates.contract.py
CONTRACT = {
    "grain": "one row per (carrier_id, lane_id, valid_from)",
    "assertions": {
        "key_unique":
            "SELECT carrier_id, lane_id, valid_from FROM t "
            "GROUP BY ALL HAVING count(*) > 1",
        "no_null_keys":
            "SELECT * FROM t WHERE carrier_id IS NULL "
            "OR lane_id IS NULL OR valid_from IS NULL",
        "rate_in_range":
            "SELECT * FROM t WHERE total_rate <= 0 OR total_rate > 50000",
        "known_carrier":
            "SELECT DISTINCT carrier_id FROM t "
            "WHERE carrier_id NOT IN (SELECT carrier_id FROM carrier_registry)",
        "not_empty":
            "SELECT 1 WHERE (SELECT count(*) FROM t) = 0",
    },
}
```

The range check is the kind that catches a missed unit conversion: a rate
stored in cents and read as currency puts every row far outside the range.

### Bootstrapping when nothing is formalised

Three sources already hold most of the knowledge.

1. **Catalog gotchas.** Each prose warning is a contract rule waiting to be
   written as a query.
2. **The lake itself.** Have the agent profile a table and propose candidate
   invariants: grain, key uniqueness, null rates, ranges, row counts per
   period, links to reference tables. A person accepts or rejects each one.
3. **Past incidents.** Every earlier fix implies an assertion and a fixture
   row. These are the most valuable because they happened.

Two cautions. Profiled invariants describe the data as it is, including its
existing bugs: a profile showing 0.3% null rates proposes "nulls allowed"
unless someone knows the answer should be zero. And business definitions stay
human-owned ([Semantic Layer](../../wiki/concepts/semantic-layer.md), [Agentic Analytics](../../wiki/concepts/agentic-analytics.md)): the agent drafts, a person decides.

An assertion that has never failed is unverified. For each one, add a
deliberately violating fixture row and confirm it fails.

### Audit before publish, inside the run

The same contract gates production writes ([Write-Audit-Publish](../../wiki/concepts/write-audit-publish.md)): write to a temporary sibling,
assert the contract, swap atomically, and fail loudly otherwise. This is a
gate inside the pipeline, not a second environment. It also protects
scheduled jobs from bad vendor files, with or without agents.

### What contracts do not cover

Correctness has four levels ([Correctness Layer](../../wiki/concepts/correctness-layer.md), [Harness Engineering](../../wiki/concepts/harness-engineering.md)): syntactic, execution, data, and business.
Contracts guard the data level. A table can satisfy every assertion and still
use the wrong definition of "effective date". That level is only as strong as
the invariants a person wrote down.

## 8. Component 4: Task contract, expected diff, feature list

### The task contract

Before a long task starts, the agent drafts a short contract and a person
approves it. This is the cheapest and most valuable review point: feedback on
direction before the agent converges beats reading diffs afterwards ([Human-in-the-Loop](../../wiki/concepts/human-in-the-loop.md)).

```yaml
task: fix-fuel-surcharge
goal: Apply the NRX fuel surcharge from valid_from, not from file date.
scope:
  code: [libs/rates, apps/build_gold_lane_rates]
  exclusions: [legacy/, carrier_registry, scheduled jobs]
paths:
  reads:  [silver.rate_cards, silver.lanes, reference.carrier_registry]
  writes: [gold.lane_rates]
expected_diff:
  gold.lane_rates:
    schema: unchanged
    rows_added: 0
    rows_removed: 0
    changed_keys: "carrier_id = 'NRX' AND valid_from >= '2026-07-01'"
    changed_columns: [total_rate]
    everything_else: identical
approvals_needed: [merge to main, first production write]
```

### The expected diff

A prediction, written before any code changes, of how the output should
differ from what is live. The dry run produces the actual diff and the two
are compared mechanically. Anything outside the declared scope fails.

Contract assertions say the output is valid. The expected diff says the
change is the intended one. A fix for one carrier that also shifts rates for
another passes every assertion and fails the diff.

| Task type | Expected diff |
|---|---|
| Refactor or migration of a legacy script | Empty: output identical to production |
| Bug fix | Named keys and columns change; no rows added or removed |
| New column | One column added; all existing columns identical |
| Backfill | Rows added for the listed keys and dates; none modified |

The empty diff is the strongest oracle available, which makes migrations of
legacy scripts the best first use of long autonomous runs.

Rules: the agent drafts the diff, a person approves it before coding, and it
is then frozen. Amending it mid-run needs approval; otherwise the loop can
rewrite the expectation until it matches. Where the diff cannot be predicted
exactly, declare bounds and accept a looser check. The comparison needs the
table's grain to line rows up, which is one more reason to write the contract
first.

### The feature list

A machine-readable list of the task's items ([Feature Lists](../../wiki/concepts/feature-lists.md)). Each has three fields: an
observable behaviour, the exact command that proves it, and a state.

```json
[
  {"id": 1, "behaviour": "Surcharge keyed on valid_from in libs/rates",
   "verify": "verify --layer unit libs/rates", "state": "passing"},
  {"id": 2, "behaviour": "Gold runner supports dry run to overlay",
   "verify": "verify --layer runtime apps/build_gold_lane_rates", "state": "active"},
  {"id": 3, "behaviour": "Dry-run diff matches expected_diff",
   "verify": "verify --layer data --task fix-fuel-surcharge", "state": "not_started"}
]
```

Rules:

- **Only the loop sets `passing`,** after a successful run of the item's
  command. The agent cannot mark its own work done.
- **One item active at a time** ([WIP=1](../../wiki/concepts/feature-lists.md)). In a controlled case this gave 87.5%
  completion against 37.5% unconstrained, with less code written.
- **No refactoring until the item passes** ([Premature Completion Declaration](../../wiki/concepts/premature-completion-declaration.md)). Refactoring first moves the line
  between verified and unverified code.
- **Items are sized to one session.**
- **The handoff report is generated from the list,** not written by the agent.

## 9. Component 5: The loop

**Control flow** ([Ralph Loop](../../wiki/concepts/ralph-loop.md)). Re-prompt the agent against the feature list until every
item passes. The agent cannot end the loop by declaring success.

**Stop conditions** ([Iterative Repair Loops](../../wiki/concepts/iterative-repair-loops.md)). As important as the prompt:

- every item passing
- an iteration cap reached
- the failure output unchanged between passes (the loop has stalled)
- a step that needs a High-tier approval
- an item marked blocked

**Saved state** ([Session Continuity](../../wiki/concepts/session-continuity.md)). In the task directory on the branch: the feature list, a
decisions log (decision, reason, rejected alternative), and one commit per
passing item. The target is a fresh session oriented in about 3 minutes
instead of 15.

**Independent evaluator** ([Premature Completion Declaration](../../wiki/concepts/premature-completion-declaration.md)). Before the pull request opens, a reviewer with
fresh context and a fixed rubric reruns the verification command and attacks
the change against the task contract. Blocking findings go back into the
loop. Self-review is structurally generous, so the reviewer must be separate.
Do not economise on it: [Anthropic's analytics team](../../wiki/entities/anthropic.md) measured +6% accuracy for +32% tokens from
adversarial review, and lost most of the gain with a cheaper reviewer model.

**Audit trail** ([Data Quality Observability](../../wiki/concepts/data-quality-observability.md), runtime versus process observability). Per iteration: what changed, which layer failed, what
remains. The pull request carries the final verification output and the diff
report, so the human reviewer reads evidence.

**Notification.** "Stopped, needs a person" should reach someone through the
same channel that scheduled-job failures use.

## 10. The toy repository, before and after

| Area | Before | After |
|---|---|---|
| Boundaries | Sentences in `AGENTS.md` | Read-only lake user, tool deny rules, protected main |
| Where the agent works | The tree a person edits | A third checkout |
| Definition of done | "Run the tests" | One verification command with four gated layers |
| Dry runs | Optional, per runner, flag-checked | Standard in the runner pattern; output root and ledger injected |
| Reads in a chain | Always production | Overlay first, production fall-through, resolved in the shared path layer |
| Table knowledge | Gotchas in catalog prose | A contract file beside each catalog page |
| Publishing | Runner writes straight to gold | Write, audit against contract, atomic swap |
| Task definition | A chat message | An approved task contract with an expected diff |
| Progress | The agent's summary | A feature list whose states only the loop can set |
| Review | The agent checks itself | A fresh-context evaluator, then a person at merge |
| Legacy migrations | Compared by hand | Empty expected diff, compared mechanically |
| Scheduler | Tracks main; sync can fail silently | Each job logs the commit it ran |

## 11. Rollout

| Step | Build | Done when |
|---|---|---|
| 1 | Permission tiers, read-only lake user, third checkout, protected main | A deliberate attempt to write the lake or push to main from the agent checkout fails |
| 2 | Verification command, layers 1 and 2; then the dry-run standard and the read resolver | One command gives pass or fail for any touched module |
| 3 | Pilot on one legacy migration with an empty expected diff | A migration reaches a pull request unattended with a clean comparison |
| 4 | Contracts and audit-before-publish for the two or three most-read gold tables | A seeded unit bug and a seeded duplicate are both caught |
| 5 | Task contract, feature list, loop, evaluator | A multi-session task resumes from saved state without rediscovery |
| 6 | Extend to new pipelines; review metrics monthly | See below |

**Metrics**

- Verified completion rate: verified items divided by activated items.
- Human interventions per task.
- Rebuild time for a fresh session.
- Defects found after merge. If these do not fall, the gates are weak and
  more freedom has not been earned.

## 12. Guarantees and limits

| Guaranteed by construction | Not guaranteed |
|---|---|
| An unattended run cannot write the lake, main, reference tables, or the scheduler checkout | Business-level correctness beyond the invariants written into contracts |
| Nothing is called done without a passing verification run on real data | Correctness of tables that have no contract yet |
| Every production change passes one human gate with evidence attached | That the scheduler is running the merged commit, unless each job logs it |
| A stopped run can resume from recorded state | Identical results on rerun: in one study about 9% of identical reruns changed outcome, so repeat a check when the decision matters |

If the read-only operating-system user is not practical, the lake is
protected only by tool-level rules, which is a materially weaker guarantee.

## 13. Maintenance

- **Delete rules the gates now enforce** ([Agent Configuration Audit](../../wiki/concepts/agent-configuration-audit.md)). Agent configuration accumulates
  because additions follow a visible failure and removals have no trigger.
  Once a boundary is a permission, its sentence in the rules file is dead
  weight. Keep only what the model cannot infer from the code ([AGENTS.md](../../wiki/concepts/agents-md.md), [Claude Skills](../../wiki/concepts/claude-skills.md)): how to run the
  checks, what is expensive, what must not be touched, where the unusual
  conventions live.
- **Do not let the agent rewrite its own instructions unreviewed** ([Harness Evolution](../../wiki/concepts/harness-evolution.md), [Context Engineering](../../wiki/concepts/context-engineering.md)).
  Auto-generated or self-evolved scaffolding tends to improve on the cases it
  was tuned on and degrade elsewhere.
- **Revisit the harness when the model changes** ([Session Continuity](../../wiki/concepts/session-continuity.md), on context anxiety). Workarounds written for one
  model generation can be unnecessary, or harmful, on the next.

## 14. Sources

Synthesised from these wiki pages:

- [Feature Lists](../../wiki/concepts/feature-lists.md)
- [Premature Completion Declaration](../../wiki/concepts/premature-completion-declaration.md)
- [Session Continuity](../../wiki/concepts/session-continuity.md)
- [Ralph Loop](../../wiki/concepts/ralph-loop.md)
- [Iterative Repair Loops](../../wiki/concepts/iterative-repair-loops.md)
- [Harness Engineering](../../wiki/concepts/harness-engineering.md)
- [Data Contracts](../../wiki/concepts/data-contracts.md)
- [Write-Audit-Publish](../../wiki/concepts/write-audit-publish.md)
- [Correctness Layer](../../wiki/concepts/correctness-layer.md)
- [Human-in-the-Loop](../../wiki/concepts/human-in-the-loop.md)
- [Agent Security: Defense-in-Depth](../../wiki/concepts/agent-security-defense-in-depth.md)
- [Data Quality Observability](../../wiki/concepts/data-quality-observability.md)
- [Agent Configuration Audit](../../wiki/concepts/agent-configuration-audit.md)
- [Agents in Data Engineering](../../wiki/concepts/agents-in-data-engineering.md)
- [Local vs. Cloud Data](../../wiki/concepts/local-vs-cloud-data.md)
- [Harness Evolution](../../wiki/concepts/harness-evolution.md)
- [Semantic Layer](../../wiki/concepts/semantic-layer.md)
- [Agentic Analytics](../../wiki/concepts/agentic-analytics.md)
- [AGENTS.md](../../wiki/concepts/agents-md.md)
- [Context Engineering](../../wiki/concepts/context-engineering.md)
- [Claude Skills](../../wiki/concepts/claude-skills.md)
- [DuckDB for Agents](../../wiki/concepts/duckdb-for-agents.md)
- [Anthropic](../../wiki/entities/anthropic.md)

The dry-run design, the overlay-first read rule, the expected diff, and the
contract file shape are this document's own design, built on those sources.
The wiki does not prescribe them.
