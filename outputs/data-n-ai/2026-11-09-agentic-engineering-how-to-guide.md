---
tags: [data-n-ai, synthesis, agents, llm, prompt-engineering, harness-engineering, testing]
sources: ["raw/data-n-ai/articles/2026-10-13-the-expensive-loop-problem.md", "raw/data-n-ai/articles/2026-09-19-the-inference-gap.md", "wiki/concepts/premature-completion-declaration.md", "wiki/concepts/agents-md.md", "wiki/concepts/context-engineering.md", "wiki/concepts/human-in-the-loop.md", "wiki/concepts/ralph-loop.md", "wiki/concepts/feature-lists.md", "wiki/concepts/session-continuity.md", "wiki/concepts/agent-configuration-audit.md", "wiki/concepts/harness-engineering.md"]
updated: 2026-11-09
---

# Agentic Engineering: A General How-To Guide

A working guide to getting reliable software out of coding agents (Claude Code, Codex and similar). It is a **living synthesis**: each new source that bears on agentic engineering should add or revise a step here and link back to its wiki page. Today it merges two recent articles with the practices already established elsewhere in the wiki:

- **Loop cost** — [The Expensive-Loop Problem](../../wiki/concepts/expensive-loop-problem.md): how costly is it to find out you were wrong?
- **Delivered depth** — [The Inference Gap](../../wiki/concepts/inference-gap.md): how much reasoning does the model actually give each step? (Detail in [Agentic Engineering Under Variable Inference](../../wiki/concepts/agentic-engineering-under-variable-inference.md).)

Both converge on one rule: **move judgment out of the model's head and into mechanisms (tests, hooks, gates, budgets) or humans (theory, direction, invariants).**

## Evidence key

| Tag | Meaning |
|---|---|
| **[EL]** | Claimed or evidenced in the Expensive-Loop article (an essay; examples are AI-R&D-heavy) |
| **[IG]** | Claimed or evidenced in the Inference Gap article (single user's data; mechanism unproven) |
| **[W]** | Independently supported by other wiki sources (linked inline) |
| **[I]** | Inferred when applying the above to software engineering — a hypothesis, not a finding |

Treat **[I]** items as things to try and measure, not as established. See [Caveats](#caveats).

---

## Step 0 — Classify the task before delegating

Two questions decide how much supervision a task needs.

1. **How costly is feedback?** (loop cost) **[EL][I]**
2. **How much sustained reasoning does the decision need?** (depth) **[IG][I]**

| | Shallow reasoning fine | Needs deep reasoning |
|---|---|---|
| **Cheap loop** (tests/types/repro, seconds) | **Delegate freely.** Typos, refactors with coverage, lint/type fixes, well-specified glue. Run in a loop ([Ralph Loop](../../wiki/concepts/ralph-loop.md)). | **Decompose, then loop.** Put the design decision in its own short step; let the loop handle implementation. |
| **Expensive loop** (deploys, migrations, long runs, human reaction) | **Supervise with gates.** Dry-run, small sample, approval before irreversible steps. | **Human owns the theory.** Agent explores and executes inside a human-authored plan, budget and kill criteria. |

Cheap-loop examples: failing repro, type error, refactor under test. Expensive-loop examples: perf work needing real traffic, schema migrations, multi-hour pipeline or training runs, anything gated on slow CI or a user's reaction.

Add one line to the task prompt or `CLAUDE.md`: *"Before starting, state whether feedback on this task is under a minute and automatic. If not, stop and propose a plan with a proxy ladder and a budget."* **[I]**

Cheap-loop tooling does not fit expensive loops: re-running a [Ralph Loop](../../wiki/concepts/ralph-loop.md) or [repair loop](../../wiki/concepts/iterative-repair-loops.md) on a task whose iteration costs hours or dollars just burns the budget. **[EL][I]**

---

## Step 1 — Set up the environment

1. **Pin the regime, not just the model.** Record model, version, prompt, effort setting *and* what was actually delivered — a model name is an incomplete spec ([Inference Regime Observability](../../wiki/concepts/inference-regime-observability.md)). **[IG]**
2. **Keep the instruction file short and non-inferable.** Write only what the agent cannot read from the repo; use progressive disclosure; human-curate, never auto-generate ([AGENTS.md](../../wiki/concepts/agents-md.md), [How to Write a Good AGENTS.md](how-to-write-agents-md.md)). Longer guideline files may also lower adherence as reasoning dilutes ([Reasoning Dilution](../../wiki/concepts/reasoning-dilution.md)). **[W][IG]**
3. **Enforce hard rules mechanically.** Anything that must always hold goes in a test, hook, linter or permission — not prose ([Agent Configuration Audit](../../wiki/concepts/agent-configuration-audit.md), [Agent Security](../../wiki/concepts/agent-security-defense-in-depth.md)). This includes resource limits and "do not touch X". **[W]**
4. **Make the cheap checks first-class.** Types, tests, linters, schema validators, data contracts: they replace reasoning with mechanism ([Correctness Layer](../../wiki/concepts/correctness-layer.md), [Data Contracts](../../wiki/concepts/data-contracts.md)). Fast checks turn expensive-feeling tasks into cheap ones. **[W][I]**
5. **Route through a harness.** The agent calls tools via a controlled layer that injects context, checks permissions, validates results and logs an audit trail ([Harness Engineering](../../wiki/concepts/harness-engineering.md)). **[W]**
6. **Build the dry run.** A sandboxed, branchable way to run the real thing cheaply (staging, shadow traffic, replayed logs, [data branches](../../wiki/concepts/data-versioning-and-branching.md), [local-first](../../wiki/concepts/local-vs-cloud-data.md)). This is the single most effective way to *convert* expensive loops into cheap ones. **[EL][W][I]**

---

## Step 2 — Plan

1. **Plan first, in a separate short step.** Probe the plan to exhaustion before implementation; keep architecture/design decisions in their own focused context, then hand implementation a settled plan ([Plan Mode All the Time](../../wiki/sources/plan-mode-substrait-de-role.md), [Agents in Data Engineering](../../wiki/concepts/agents-in-data-engineering.md)). Also fits shallow delivered depth. **[W][IG][I]**
2. **State hypotheses and falsifiers.** For any non-trivial change: *what do we believe, and what result would prove it wrong?* Models confirm rather than falsify, so write the falsifier into the plan. **[EL][I]**
3. **Write the proxy ladder.** List cheaper stand-ins in order, and for each: what it can and cannot tell you. e.g. unit → integration → staging/replayed traffic → canary → full rollout; or sample → one partition → full data; or small model → large run. Say when a proxy stops being trustworthy ("passing the mock doesn't prove the real API behaves this way"). **[EL][I]**
4. **Budget the experiments.** Cap full runs ("max 2 full runs; otherwise use the 5-minute smoke test"). For any run above a cost threshold require *expected information gain vs. cost* before executing. **[EL][I]**
5. **Write kill criteria.** "If metric X hasn't moved after Y, change strategy." Prevents hill-climbing inside a bad approach. **[EL][I]**
6. **Define done as a gated checklist** — verification levels in order, no skipping ([Premature Completion Declaration](../../wiki/concepts/premature-completion-declaration.md)). Break work into a [feature list](../../wiki/concepts/feature-lists.md) with a verification command per item. **[W]**
7. **Set scope.** One work item at a time (WIP=1); name the files/surfaces the agent may touch ([Feature Lists](../../wiki/concepts/feature-lists.md)). **[W]**

---

## Step 3 — Execute

1. **Small, relevant contexts; fresh sessions per task.** Targeted reads over long scrollback; short state artifacts (PROGRESS/DECISIONS, git checkpoints) to carry across sessions ([Context Engineering](../../wiki/concepts/context-engineering.md), [Session Continuity](../../wiki/concepts/session-continuity.md)). **[W][IG]**
2. **Save full output; search the file.** Run a slow command once, redirect output to a file, then grep/tail the file as often as needed. Never re-run a long command with a different `tail`. **[EL]**
3. **Run long jobs in the background; don't poll.** And don't pause a run to exhaustively evaluate every checkpoint (PostTrainBench: ~10 hours spent watching metrics after one good step-1 result). **[EL]**
4. **Fan out for breadth, not for hard reasoning.** Parallel agents suit independent modules, search, test generation. For a stubborn problem use one deep attempt: higher effort, clean context, narrow question. Parallelism adds breadth, not missing serial depth — and costs multiply on expensive loops. **[IG][EL][I]**
5. **Verify function, then performance, then style.** No refactoring or polish until core behaviour is verified; it reopens correctness on code that was known-good ([Premature Completion Declaration](../../wiki/concepts/premature-completion-declaration.md)). **[W]**
6. **Make workflows idempotent and checkpointed**, so a bad stretch costs a rerun, not corrupted state ([Write-Audit-Publish](../../wiki/concepts/write-audit-publish.md)). **[W][IG]**

---

## Step 4 — Verify

1. **Require executed evidence, not claims.** Test output, command output, a script-checked diff, a screenshot or recording of the real behaviour. Layered: static → runtime → system-level, each gating the next. **[W]**
2. **End-to-end, actually.** The Mechanize GBA-emulator eval: models boot the game, see the title screen and declare success. Require the agent to *exercise* the feature the way a user would, and show it. **[EL][W]**
3. **Separate the checker from the worker.** A dedicated, deliberately sceptical evaluator (or a human). Same model, same prompt: single agent $9 and broken vs. planner/generator/evaluator $200 and working ([Premature Completion Declaration](../../wiki/concepts/premature-completion-declaration.md)). **[W]**
4. **Don't let the agent write and grade its own tests alone.** Write acceptance tests first, or have them reviewed independently. Self-written tests are "the most superficial way" (Erdil). **[EL][W]**
5. **Watch for proxy cheating.** Hardcoded expected values, skipped or deleted tests, loosened thresholds, special-casing the benchmark. Make "tests/thresholds unchanged" part of the diff check. Same shape as evolve-set overfitting in [Harness Evolution](../../wiki/concepts/harness-evolution.md). **[EL][W][I]**
6. **Make failures carry repair instructions** ("POST /reset returned 500; check email service config") so the agent can self-correct without a human round-trip. **[W]**

---

## Step 5 — When it fails: diagnose, then escalate

**Diagnose the rung before retrying.** Every failure is one of: **parameter** (a setting, a typo), **strategy** (wrong approach), or **premise** (measuring the wrong thing; misunderstood task). Agents default to the bottom rung and lock in. After 2–3 failed attempts require a written diagnosis: *which rung, what evidence, what would change my mind?* A mid-run "are we sure this is the right approach?" nudge beat an agent's own continuation by up to 17% in PostTrainBench. **[EL][I]**

**Escalate by ladder, not by loop.** cheap model → higher effort → fresh narrowed context → human. Repeated retries at the same shallow regime mostly reproduce the failure. **[IG][I]**

**Stop conditions on loops.** Max iterations; stalled delta; issue needs human judgment ([Iterative Repair Loops](../../wiki/concepts/iterative-repair-loops.md)). On expensive loops, add a *budget* stop. **[W][EL]**

---

## Step 6 — Where humans spend attention

1. **Own the theory.** The causal model of your system (where does latency come from?), which experiments are worth running, and how to read ambiguous results. Models read noise as signal. **[EL][I]**
2. **Give direction, not artefact review.** Early, high-level steering beats line-by-line correction ([Human-in-the-Loop](../../wiki/concepts/human-in-the-loop.md)). **[W]**
3. **Gate by blast radius, not habit.** Auto-run low risk; approve high risk; block critical ([risk-tiered HITL](../../wiki/concepts/harness-engineering.md)). **[W]**
4. **Review design, invariants and security-sensitive code;** let verified mechanical work through. **[IG][W][I]**
5. **Watch your own cheap-loop habits.** Optimising whatever dashboard metric is easy, rabbit-holing on a green suite, treating irreversible changes like reversible ones. Reversible → move fast; irreversible → add a proxy and a pause. **[EL]**

---

## Step 7 — Measure and maintain

1. **Instrument the harness.** Log reasoning tokens, zero-thinking share, longest span, invocations per turn, and cost per *successful* task before rewriting prompts. Hidden degradation shows up as retries, bigger agent teams and extra review. **[IG][I]** (Highest-value, lowest-regret item: pays off whether or not the Inference-Gap causal story holds.)
2. **Keep a golden-task suite** that runs periodically in your real regime, so "feels worse today" becomes evidence. **[IG][I]**
3. **Audit configuration on a schedule.** Archive → `/doctor` + `/memory` → remove → test without → decide ([Agent Configuration Audit](../../wiki/concepts/agent-configuration-audit.md)). **[W]**
4. **Regularise any automated improvement.** If a system auto-evolves prompts/skills/harness, use holdouts, a noise floor and pruning ([Harness Evolution](../../wiki/concepts/harness-evolution.md)). **[W]**
5. **Diversify for critical work.** A weaker model you control may beat a stronger one delivered under a variable regime. **[IG][I]**

---

## Copy-paste block for `CLAUDE.md` / `AGENTS.md`

Keep it short; delete any line you don't enforce or measure. Prefer a hook or test over any of these lines where one is possible.

```markdown
## Working agreement

- Before starting, say whether feedback on this task is fast (<1 min) and automatic. If not, stop and propose: proxy ladder, run budget, kill criteria.
- Plan before implementing. State what would prove the plan wrong.
- Done = verified end to end with shown evidence (test output, command output, or a recording of real behaviour). "Code written" is not done.
- Do not edit tests, thresholds or fixtures to make a check pass without saying so explicitly.
- Do not refactor or polish until core behaviour is verified.
- Run slow commands once; save full output to a file and search the file.
- After 2 failed attempts, write a diagnosis: parameter, strategy, or premise? Do not keep tuning within a failed approach.
- Ask a human before irreversible or production-affecting steps.
```

---

## Caveats

- **Thin evidence base.** Both anchor articles are single-source: the Expensive-Loop essay leans on AI-R&D benchmarks (PostTrainBench, an Amazon study, Mechanize's eval) and the Inference Gap is one user's logs with an unproven mechanism. Most **[I]** items are extrapolations to everyday software engineering.
- **Confound (Inference Gap):** adaptive effort may rightly give simple steps little thinking; harm may sit in a minority of hard turns. Establish *which* tasks degrade before restructuring workflows.
- **Cheap/expensive is a continuum,** not a binary. Use it to prompt the question, not as a rigid taxonomy.
- **Some tension to manage:** fanout helps breadth but multiplies cost on expensive loops; shallow-depth defences (decompose, small contexts) can conflict with the need for a coherent theory held in one place — which is why the theory stays with a human or a short design doc.
- **Models may improve.** Several workarounds may become less necessary; the audit step exists to prune them.
- **Untested here.** Nothing in this guide has been run against the user's own agent logs yet.

## How to extend this guide

When a new source touches agentic engineering: add or revise the relevant step, tag it with an evidence key (add a new tag for the new source), link the wiki concept page, and add a backlink from that page to this guide. Prune steps that later evidence contradicts.

## Related Pages

- [The Expensive-Loop Problem](../../wiki/concepts/expensive-loop-problem.md) · [Source](../../wiki/sources/the-expensive-loop-problem.md)
- [The Inference Gap](../../wiki/concepts/inference-gap.md) · [Source](../../wiki/sources/the-inference-gap.md)
- [Agentic Engineering Under Variable Inference](../../wiki/concepts/agentic-engineering-under-variable-inference.md) — the Inference-Gap-specific subset
- [Reasoning Dilution](../../wiki/concepts/reasoning-dilution.md)
- [Inference Regime Observability](../../wiki/concepts/inference-regime-observability.md)
- [Premature Completion Declaration](../../wiki/concepts/premature-completion-declaration.md)
- [Ralph Loop](../../wiki/concepts/ralph-loop.md) · [Iterative Repair Loops](../../wiki/concepts/iterative-repair-loops.md)
- [Human-in-the-Loop](../../wiki/concepts/human-in-the-loop.md)
- [Feature Lists](../../wiki/concepts/feature-lists.md) · [Session Continuity](../../wiki/concepts/session-continuity.md)
- [AGENTS.md](../../wiki/concepts/agents-md.md) · [How to Write a Good AGENTS.md](how-to-write-agents-md.md) · [Context Engineering](../../wiki/concepts/context-engineering.md)
- [Harness Engineering](../../wiki/concepts/harness-engineering.md) · [Harness Evolution](../../wiki/concepts/harness-evolution.md) · [Agent Configuration Audit](../../wiki/concepts/agent-configuration-audit.md)
- [Agent Security: Defense-in-Depth](../../wiki/concepts/agent-security-defense-in-depth.md)
