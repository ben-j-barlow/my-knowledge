---
tags: [data-n-ai, concept, agents, prompt-engineering, harness-engineering]
sources: ["raw/data-n-ai/articles/2026-08-27-audit-your-agent-files.md"]
updated: 2026-10-09
---

# Agent Configuration Audit

An agent configuration audit is the periodic practice of asking every piece of a coding agent's setup — context files, skills, plugins, MCP servers, hooks, memory, commands — to **earn its place again**. It is the maintenance half of [Context Engineering](context-engineering.md): the other pages in this wiki cover what to put in front of the model; this one covers when to take it away.

The premise, from [Addy Osmani](../entities/addy-osmani.md): **agent configuration has a half-life.** Each instruction was written against a specific model, harness, and codebase. All three move; the instruction stays. A rule that compensated for a real weakness last quarter may now be dead weight — or actively steering a better model wrong.

---

## Configuration rot: the ratchet

Nobody sets out to write a thousand-line instruction file. It ratchets:

1. The agent gets something wrong, once, in a way that stung.
2. You add a rule — reasonable in isolation.
3. The file grows and dilutes what matters.
4. Adherence drops, so quality gets worse.
5. Go to 1.

Additions are triggered by a visible failure; removals have no trigger at all. The same asymmetry applies to skills (installed to try, never uninstalled), MCP servers (connected once, rarely called), and auto-memory (a preference mentioned once becomes permanent). This is the mechanism behind the **bloat** failure mode on the [AGENTS.md](agents-md.md) page.

How common it is: a study of 100 popular repositories (arXiv:2606.15828) found lint-related leakage in **62%** of agent files, context bloat in **42%**, and skill leakage in **35%**, with the smells frequently co-occurring.

## Why removal is usually safer than it feels

- **Instruction value expires.** Anthropic reports removing more than 80% of Claude Code's system prompt for its Claude 5 generation models with no measurable loss on internal coding evals. (Not a target — private evals, one harness — but evidence that scaffolding written for older models stops paying.)
- **Context files don't clearly improve correctness.** Across 288 runs on 17 real tasks (arXiv:2607.27250), context files changed *how* agents worked — e.g. running targeted tests after being told the full suite is slow — but not how often they succeeded.
- **Prose is a weak carrier.** Prose summaries of code answered 4 of 45 behavioural questions where the source itself answered 27 (arXiv:2607.09691). On long policy handbooks, the best of 30 model configurations reached a 36.2% strict pass rate, sometimes finding the relevant rule and acting against it.
- **Personal isn't better than generic.** A skill distilled from one developer's history performed about as well as one borrowed from another developer; a pooled generic skill beat both (arXiv:2608.10319, simulator-based).

"We keep things because removing them feels unsafe" — which is usually an unexamined bet that the model and harness have not improved since the rule was written.

---

## The audit loop

Cadence: every couple of weeks to monthly.

| Step | What | Why |
|---|---|---|
| 1. Archive | Snapshot the whole setup | Makes every later step cheap to undo — the answer to "what if quality drops?" |
| 2. Detect | Run `/doctor` in a Claude Code session, then `/memory` | Surfaces unused skills/plugins/MCP servers relative to context cost, slow hooks, duplicated `CLAUDE.md` guidance, always-loaded content the agent could just read |
| 3. Remove | What was flagged, plus anything you don't remember installing | You can't reason about a setup you've forgotten |
| 4. Test removal | Run a real task with no local skills — raw model and harness | The actual experiment |
| 5. Decide | Keep the deletion or restore | |

Notes on running it:

- **Step 4 is a smoke test, not a proof.** Agent outcomes vary even at low temperature (~9% of byte-identical reruns changed outcome in one study), so repeat the run when the decision matters. A failure in exactly the way a skill was written to prevent is positive evidence for keeping it.
- **`/doctor` is triage, not judgment.** It can tell that something is unused or duplicated; it cannot tell whether "never change this protocol field" protects a live integration or documents a deleted system. The human still owns the keep/kill call.
- **`/doctor` ≠ `claude doctor`.** The slash command inside a session audits configuration; the shell command only prints installation diagnostics.
- **Memory is a separate surface.** Auto-memory holds stale preferences even after the repo files are tidy.

## What survives an audit

Keep in context files only what the model cannot infer from the code (the same rule as [AGENTS.md](agents-md.md), now with a second source):

- how to run the right checks
- which operations are expensive
- what must remain untouched, and which files are generated
- where the unusual conventions live

Cut generic clean-code advice, summaries of code that exists, and anything the README says. **Point the agent at real code, not descriptions of it.**

For skills, prefer a strong generic/community skill and add personal rules gradually, only when a preference has recurred across similar tasks. Skills earn their keep with concrete, task-specific examples — not formatting preferences.

## Hard constraints belong below the prose

If a rule must *always* hold, a markdown sentence is the wrong place for it: encode it as a **test, hook, or permission**. Of everything in the agent environment, permissions and settings are "the only rules that actually bind the agent." This is the single-developer version of [Agent Security: Defense-in-Depth](agent-security-defense-in-depth.md)'s "enforcement below the agent," and of the [Harness Engineering](harness-engineering.md) claim that a deterministic layer, not an instruction, is what makes behaviour reliable.

## What an unused skill actually costs

Not thousands of tokens per prompt. Only skill **names and descriptions** are always loaded, inside a listing budget (default 1% of the context window; descriptions are shortened first when over budget). The **body** loads when the skill is invoked and then stays for that session. So the case for pruning [skills](claude-skills.md) is:

- **Discoverability** — the model picks from a list; longer lists pick worse.
- **Accidental triggering** — overlapping skills with unclear precedence (Osmani found a pile of forgotten anti-slop writing skills).
- **Maintenance** — everything installed is something you now own.
- **Your own clarity.**

---

## Relationship to other patterns

- [Harness Evolution](harness-evolution.md) — RRSI prunes harness components that stop earning a measured gain (its L1-style regularizer). An audit is the same rule applied by hand, with the removal test as a crude ablation.
- [Claude Skills](claude-skills.md) — Anthropic's analytics team lists "prune scaffolding as models improve" as a maintenance practice and fixed *drift* with a CI hook; an audit addresses the complementary problem of *accumulation*.
- [Session Continuity](session-continuity.md) — another case where a workaround was model-dependent (context anxiety severe on one model generation, diminished on the next).

## Open questions

- No public benchmark yet measures the effect of *removing* configuration; the evidence is one vendor's private evals plus studies of adding it.
- The context-file studies conflict on correctness (see [AGENTS.md](agents-md.md#does-it-actually-help-the-evidence-conflicts)).

## Related Pages

- [AGENTS.md](agents-md.md)
- [Context Engineering](context-engineering.md)
- [Claude Skills](claude-skills.md)
- [Harness Evolution](harness-evolution.md)
- [Harness Engineering](harness-engineering.md)
- [Agent Security: Defense-in-Depth](agent-security-defense-in-depth.md)
- [Session Continuity](session-continuity.md)
- [Addy Osmani](../entities/addy-osmani.md)
- [Anthropic](../entities/anthropic.md)
- [Source: Audit Your Agent Files](../sources/2026-08-27-audit-your-agent-files.md)
