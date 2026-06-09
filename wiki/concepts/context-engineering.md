---
tags: [data-n-ai, concept, agents, prompt-engineering, llm]
sources: ["raw/data-n-ai/articles/How to Build Your AGENTS.md (2026) The Context File That Makes AI Coding Agents Actually Work.md", "raw/data-n-ai/articles/A good AGENTS.md is a model upgrade. A bad one is worse than no docs at all..md"]
updated: 2026-06-05
---

# Context Engineering

Context engineering is the discipline of deciding **what goes into an agent's context window, and what stays out** — managing the finite, expensive, and quality-degrading resource that is the token budget. It is the layer above prompt engineering: not just *how* you phrase an instruction, but *which* instructions, docs, examples, and tool outputs are present when the model reasons.

The central tension: more context is not better. Every token added has a cost (inference dollars + reasoning steps) and a risk (context rot — the model degrading as the window fills with marginally-relevant material). Good context engineering maximizes signal per token.

---

## Context rot

As the context window fills, model performance degrades — even on content that is technically present. Symptoms:

- **"Lost in the middle":** instructions placed mid-context get silently dropped in long sessions. Mitigation: keep documents short, place critical rules early, start fresh sessions for new tasks.
- **Overexploration:** vague architecture descriptions or long lists of warnings push the agent into reading dozens of files to "understand" before acting — loading tens to hundreds of thousands of tokens of irrelevant context and producing *worse* output. (See the [AGENTS.md](agents-md.md) overexploration trap.)
- **Graceful degradation under pressure:** Anthropic's guidance notes that as context grows, well-behaved agents preserve architectural decisions while discarding redundant tool outputs.

---

## The ETH Zurich finding: context files have a measurable cost

The key empirical anchor (ETH Zurich, arXiv:2602.11988) evaluated multiple coding agents across SWE-bench Lite and AGENTbench, comparing LLM-generated vs developer-written context files against a no-context baseline:

| Context file type | Inference cost | Task success change |
|---|---|---|
| **LLM-generated (auto-init)** | +20–23% | −0.5% (SWE-bench Lite) to −2% (AGENTbench) |
| **Developer-written (human-curated)** | up to +19% | ~+4 points (AGENTbench) |
| **No context file** | baseline | baseline |

Two conclusions that challenge common practice:

1. **Auto-generated context files hurt.** In 5 of 8 settings they reduced success rates, added 2.45–3.92 steps per task, and raised cost 20–23%. They are *redundant with documentation the agent already reads independently* — duplicating it adds cost without signal. (A follow-up that first stripped all other repo docs found LLM-generated files then helped by +2.7%, confirming the redundancy mechanism.)
2. **Human-written files help, but modestly** (~4 points) — and still incur the token overhead. Worth it because the overhead is the same either way; only human curation buys the upside.

### Independent confirmation: Anthropic's analytics null result

Anthropic's internal [agentic analytics](agentic-analytics.md) team reproduced the same mechanism on a different surface. They gave their agent grep access to **thousands** of prior SQL files and verified in transcripts it read them before every answer — accuracy moved **<1 point.** The answer was present in the corpus ~80% of the time on questions it got wrong, but "answer present" did not predict "now correct." Conclusion: the bottleneck is **structure** (mapping a question to the right entity), **not access** to prior work — the warehouse analogue of "auto-generated context files are redundant." A corollary they hit independently: **auto-generating the [semantic layer](semantic-layer.md) was net-negative** (it encoded the ambiguities it was meant to remove), so they **generate documentation with the LLM but let a human own the definition** — the same generate-docs-not-definitions split AGENTS.md reaches for hand-authored files.

### The cost in dollars

At Claude Sonnet 4.6 pricing (~50K input / 5K output baseline task), the ~20% overhead works out to roughly **$45 / 1K tasks, $450 / 10K, $4,500 / 100K per month.** **Prompt caching is the primary mitigation** — cache reads are ~90% cheaper than standard input pricing, which is why caching is non-negotiable for any production agent loop.

---

## Operating principles

- **Write only the non-inferable.** The single highest-leverage rule (detailed under [AGENTS.md](agents-md.md)). Anything the agent can discover by reading code or existing docs is pure overhead.
- **Progressive disclosure.** Surface common cases; push detail into reference files loaded on demand. Outline *what* is in each reference, go no deeper.
- **Manage discovery, not just authorship.** Agents reliably read `AGENTS.md` (100%) and its references (>90%); orphan `_docs/` are read <10% of the time. Placement determines whether content is ever seen.
- **Respond to observed failure, not speculation.** Rules added speculatively bloat the window; rules added in response to a real failure carry signal.
- **Caching changes the calculus.** Stable context (system prompts, AGENTS.md) should be cache-friendly so the 20% overhead is paid once, not per call.
- **Drift is the maintenance frontier.** Static context goes stale silently. Emerging answers: semantic code indexes (Augment's Context Engine), and "living specs" that agents update as they work ([Augment Code](../entities/augment-code.md)'s Intent).

---

## Relationship to other patterns

Context engineering is the connective tissue under several patterns already in this wiki:

- [AGENTS.md](agents-md.md) — the most-studied context-engineering surface.
- [Substrait](substrait.md) — Chris Riccomini's "cost-as-tokens" argument is context engineering applied to query interfaces: choose the representation that produces the smallest, cheapest LLM output.
- [Ralph Loop](ralph-loop.md) — re-prompting with a clean context each iteration is itself a context-management strategy (avoids accumulating rot across attempts).
- [Human-in-the-Loop](human-in-the-loop.md) — direction-level feedback is high-signal-per-token compared to artifact-level review.
- [Agentic Inference](agentic-inference.md) — long agent contexts overflow HBM into DRAM; context length is a hardware cost, not just a quality one.
- [Agentic Analytics](agentic-analytics.md) / [Claude Skills](claude-skills.md) — the warehouse version: metadata-as-product makes a warehouse "legible" the way code is; the structure-not-access null result reproduces the ETH Zurich finding; skills solve drift with a CI hook rather than leaving it unsolved.

## Related Pages

- [AGENTS.md](agents-md.md)
- [Agentic Analytics](agentic-analytics.md)
- [Claude Skills](claude-skills.md)
- [Semantic Layer](semantic-layer.md)
- [Substrait](substrait.md)
- [Ralph Loop](ralph-loop.md)
- [Human-in-the-Loop](human-in-the-loop.md)
- [Agentic Inference](agentic-inference.md)
- [Augment Code](../entities/augment-code.md)
- [Source: How to Build Your AGENTS.md (2026)](../sources/2026-04-01-how-to-build-agents-md.md)
