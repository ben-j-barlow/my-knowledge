---
tags: [data-n-ai, source, agents, prompt-engineering, harness-engineering]
sources: ["raw/data-n-ai/articles/Audit your Agent files.md"]
updated: 2026-10-09
---

# Source: Audit Your Agent Files (Addy Osmani)

[Addy Osmani](../entities/addy-osmani.md)'s blog, published 2026-08-27. A practitioner's guide to periodically auditing a coding agent's configuration — `CLAUDE.md`/`AGENTS.md`, skills, plugins, MCP servers, hooks, memory — anchored on a batch of mid-2026 empirical studies and on Claude Code's `/doctor` command. Osmani maintains a skills pack himself, so this is a critique from inside the skills camp rather than from a sceptic.

## Thesis

> Your coding agent's configuration has a half-life.

Models improve, harnesses add capabilities, codebases change — and the instructions written for an older version stay behind. Every item in the setup "was added for a reason. An audit is just the question of whether that reason is still true." The practical rule: **installing a useful skill and keeping it forever are separate decisions.**

Osmani explicitly softens the harder "official guidance" (delete `CLAUDE.md`, skills, and hooks every couple of months and rebuild only what matters): people don't do it because they fear a quality drop and have no cheap way to restore. His version is *archive first, then test removal*, so the experiment is cheap to undo.

## What accumulates (the "agent environment")

| Surface | How it rots |
|---|---|
| Context files (`CLAUDE.md`, `AGENTS.md`) | Grow past the 200-line guidance one rule at a time |
| Agent Skills | Installed once, kept forever (one anecdote: 250 → 25 after an audit) |
| Plugins | Bundles that quietly bring their own skills |
| MCP servers | Still connected, rarely called, always costing |
| Hooks | Latency on every session |
| Memory | Stale preferences survive a tidy repo — audited separately with `/memory` |
| Commands, subagents | Often repeat what the context files already say |
| Permissions, settings | "The only rules here that actually bind the agent" |

## Why configuration rots: the ratchet

Agent gets something wrong once → you add a rule (reasonable in isolation) → the file grows and dilutes what matters → adherence drops → quality gets worse → add another rule. "You wanted a short decision guide. You built a knowledge base." Shapes Osmani found in his own files: examples far longer than the rule they illustrate; content already in the README, manifest, or a skill; a rule added on every error and never removed; rules so specific they still miss the intended outcome.

## The research cited

| Study | Setup | Finding |
|---|---|---|
| Configuration smells in AGENTS.md ([arXiv:2606.15828](https://arxiv.org/abs/2606.15828)) | 100 popular repos | Lint-related leakage in **62%**, context bloat **42%**, skill leakage **35%**; most files had at least one smell and they co-occurred |
| Do context files help coding agents? ([arXiv:2607.27250](https://arxiv.org/abs/2607.27250)) | 288 runs, 17 real tasks, Claude Code + Codex | **No clear gain in correctness.** Files changed *how* agents worked, not how often they succeeded |
| Do personalized skills help? ([arXiv:2608.10319](https://arxiv.org/abs/2608.10319)) | 206 sessions, 13 developers (LLM-based developer simulator) | **Generic beat personal.** A skill from one developer's history did about as well as one borrowed from someone else; a pooled generic skill was more useful |
| What context does an agent need to act? ([arXiv:2607.09691](https://arxiv.org/abs/2607.09691)) | 45 behavioural questions about code | **Source answered 27/45, prose summaries 4/45**; ~9% of byte-identical reruns changed outcome |
| handbook.md | 20–124 page policy handbooks, 30 model configurations | Best strict pass rate **36.2%**; agents sometimes found the relevant rule and then acted against it |
| Anthropic, [The new rules of context engineering](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models) | Claude Code system prompt, Claude 5 generation models | Removed **>80%** of the system prompt with no measurable loss on internal coding evals |

Osmani's own caveats: the Anthropic result "is not a target" (private evals, specific models in a specific harness); the personalization study used a simulator, so "promising rather than final." The handbook.md result appears only in a slide, without a link.

## Key claims

- **Context files buy efficiency, not correctness.** In the 288-run study one guide flagged that the full test suite was slow; Claude ran targeted tests and wasted less time, but didn't implement the feature any better. Near misses came down to implementation judgment that more prose would not have fixed.
- **Keep only what the model can't infer from the code:** how to run the right checks, which operations are expensive, what must stay untouched, which files are generated, where the unusual conventions live. Cut generic clean-code advice, summaries of existing code, and anything the README already says.
- **Point the agent at real code, not descriptions of it** — summaries smooth over exactly the details that matter (4/45 vs 27/45).
- **Personalize slowly.** Start from a strong generic skill; add personal rules gradually; don't promote a preference to permanent memory because it was mentioned once. Personalization looked better when the same preference recurred across similar tasks, and concrete task-specific examples are where skills add value (formatting preferences don't).
- **Team/org skills are where enterprises see compounding value** — engineering culture, compliance rules, internal tooling quirks, review process (anecdotal, from Osmani's conversations).
- **Hard constraints don't belong in prose.** "If a rule must always hold, encode it in a test, hook, or permission rather than leaving it as prose the model might lose."
- **The cost of an unused skill is confusion, not tokens.** Correcting a common claim: an installed skill does *not* dump its body into every prompt. Names and descriptions load for discovery within a listing budget (default 1% of the context window, descriptions shortened first when over budget); the body loads on invocation and stays for the session. The real reasons to prune are discoverability (long lists pick worse), accidental triggering (six overlapping anti-slop skills — which wins?), maintenance, and the owner's own clarity.

## `/doctor` vs `claude doctor`

- **`/doctor`** (inside an interactive Claude Code session) is the configuration audit: flags skills, MCP servers, and plugins that look unused relative to their context cost, hooks adding noticeable latency, duplicated `CLAUDE.md` guidance, and always-loaded content the agent could read from the repo. It reports before changing anything; `CLAUDE.md` trimming needs Claude Code 2.1.206+.
- **`claude doctor`** (in a shell) is read-only installation diagnostics — the reason some people report doctor "only shows a status check."
- `/doctor` "is triage, not judgment": it can't know whether "never change this protocol field" protects a live customer integration or documents a system deleted last quarter.

## The audit loop

Every couple of weeks to monthly:

1. **Archive** — snapshot the setup so restoring costs a minute. This is the step that makes the rest safe.
2. **Run `/doctor`**, then **`/memory`** (memory rots on its own schedule).
3. **Remove** what it flagged and what you no longer remember installing.
4. **Test without them** — run a real task and tell the agent to use no local skills, raw model and harness only.
5. **Decide** — keep the deletion or restore in one command.

Step 4 is "a smoke test, not a proof": outcomes vary even at low temperature, so repeat if the decision matters. Failing in exactly the way a skill was written to prevent is useful evidence too — the skill earning its place again.

> We keep things because removing them feels unsafe — usually a bet that the model and harness have not improved since you wrote the rule.

> Keep the setup as lean as you can, and as specific as you need.

## How This Extends the Existing Wiki

- **Adds the time dimension to [AGENTS.md](../concepts/agents-md.md) and [Context Engineering](../concepts/context-engineering.md).** Those pages cover what to write; this covers when to delete, captured on the new [Agent Configuration Audit](../concepts/agent-configuration-audit.md) page.
- **A partial answer to "no automated staleness detector."** The AGENTS.md page called drift unsolved at the manual-file level; `/doctor` is a first-party detector for *unused and duplicated* configuration, though not for *wrong* configuration.
- **A tension with the Augment study.** [Augment's AuggieBench result](2026-04-23-good-agents-md-model-upgrade.md) says the best files are worth a Haiku→Opus jump; the 288-run study here finds no clear correctness gain. They are reconcilable — Augment's gains came from specific patterns (procedural workflows, decision tables) on its own benchmark and it also found bad files worse than none, while ETH Zurich's ~4 points sits in between — but the wiki should treat "context files improve correctness" as contested and "context files change workflow efficiency" as the safer claim.
- **A second data point on skill provenance.** [WikiSkill](wikiskill-agent-skill-evolution.md) found skills evolved by one model transfer to and sometimes beat another model's own; the personalization paper finds the same for humans — generic/borrowed skills match or beat personal ones. See [Claude Skills](../concepts/claude-skills.md).
- **Manual-scale pruning matches [Harness Evolution](../concepts/harness-evolution.md).** RRSI's L1-style regularizer prunes components that stop earning a measured gain; Osmani's "ask each instruction to earn its place again" is the same rule applied by hand.
- **Prose vs enforcement** echoes [Agent Security: Defense-in-Depth](../concepts/agent-security-defense-in-depth.md)'s "enforcement below the agent."

## Source

[raw/data-n-ai/articles/Audit your Agent files.md](../../raw/data-n-ai/articles/Audit%20your%20Agent%20files.md) — original at <https://addyosmani.com/blog/audit-your-agent-files/>
