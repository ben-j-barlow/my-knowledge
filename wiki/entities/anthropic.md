---
tags: [data-n-ai, entity, agents, llm]
sources: ["raw/data-n-ai/articles/How Anthropic enables self-service data analytics with Claude.md"]
updated: 2026-06-09
---

# Anthropic

AI safety and research company; maker of the **Claude** family of models (Opus / Sonnet / Haiku), the **Claude Code** agentic CLI, and the **Model Context Protocol (MCP)**. Anthropic appears across this wiki as the provider whose models and tooling underpin most of the agentic and coding-agent material; this page collects what sources say about Anthropic *itself* and its own internal practices.

---

## Internal data analytics (the canonical case study)

Anthropic's Data Science & Data Engineering team published the most detailed public account of running [agentic analytics](../concepts/agentic-analytics.md) in production:

- **95% of business analytics queries automated** via Claude, at **~95% aggregate accuracy** (~99% in mature domains) — freeing the data team for causal modeling, forecasting, and ML.
- The accuracy comes from a four-layer stack — [data foundations](../concepts/agentic-analytics.md) → [semantic layer](../concepts/semantic-layer.md)/sources of truth → [Claude Skills](../concepts/claude-skills.md) → validation — built around the thesis that **analytics accuracy is a context and verification problem, not a code-generation one.**
- Headline internal numbers: **skills took accuracy from 21% → 95%+**; skill docs **drifted 95%→65% in a month** without maintenance (fixed with a CI hook + repo colocation; ~90% of data-model PRs now touch a skill); a **null-result ablation** (grep access to thousands of prior SQL files moved accuracy <1 point) proved the bottleneck is *structure, not access*; **auto-generating the semantic layer was net-negative**.
- Practices they productionized: a **provenance footer** on every answer, an **adversarial-review sub-agent** (+6% accuracy / +32% tokens / +72% latency), **per-domain eval launch gates**, and a **scheduled correction-harvesting agent** that scans stakeholder channels and opens reference-doc PRs.

See [Source: How Anthropic Enables Self-Service Data Analytics with Claude](../sources/2026-06-03-anthropic-self-service-analytics.md).

---

## Standards and ecosystem contributions

- **MCP (Model Context Protocol)** — Anthropic's open standard for serving tools/resources to agents; in the analytics stack, skills are served to hosted surfaces over MCP. In December 2025 Anthropic **donated MCP to the Agentic AI Foundation** (Linux Foundation), alongside OpenAI donating `AGENTS.md` and Block donating Goose. (See [AGENTS.md](../concepts/agents-md.md).)
- **Claude Code** — the agentic coding CLI whose **skills** mechanism (on-demand markdown folders) is the procedural backbone of the analytics system.
- **Context guidance** — Anthropic's published guidance on graceful context degradation (agents preserving architectural decisions while discarding redundant tool outputs) is cited in [Context Engineering](../concepts/context-engineering.md).

---

## Models (referenced across the wiki)

- **Claude Opus** — flagship; the "Haiku→Opus" jump is the benchmark of quality used in the AGENTS.md studies.
- **Claude Sonnet** — mid-tier; Sonnet pricing anchors the context-file cost math in [Context Engineering](../concepts/context-engineering.md).
- **Claude Haiku** — fast/cheap tier.

> For authoritative, current model IDs, pricing, and parameters, consult the Claude API skill rather than relying on figures quoted in dated sources.

---

## Related Pages

- [Agentic Analytics](../concepts/agentic-analytics.md)
- [Claude Skills](../concepts/claude-skills.md)
- [Semantic Layer](../concepts/semantic-layer.md)
- [AGENTS.md](../concepts/agents-md.md) — Anthropic donated MCP to the same foundation as AGENTS.md
- [Context Engineering](../concepts/context-engineering.md)
- [OpenAI](openai.md) — the comparison point for Codex / AGENTS.md
- [Source: How Anthropic Enables Self-Service Data Analytics with Claude](../sources/2026-06-03-anthropic-self-service-analytics.md)
