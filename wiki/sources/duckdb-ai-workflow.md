---
tags: [data-n-ai, source, agents, analytics, prompt-engineering]
sources: ["raw/data-n-ai/articles/2026-09-13-my-duckdb-ai-workflow.md"]
updated: 2026-10-16
---

# Source: My DuckDB + AI Workflow

**Author**: Hoyt Emerson (The Full Data Stack; founder of Early Signal)
**Published**: 2026-09-13 · **URL**: https://thefulldatastack.substack.com/p/my-duckdb-ai-workflow
**Type**: Practitioner opinion / tips piece (single-author experience, no benchmarks)

## Core Claim

For analytics and research, the best agent setup is the terminal: a coding agent (Claude Code) driving the **DuckDB CLI** over local files, with no IDE, no Python scripts, and no MCP server. [CLI tools are, in the author's words, "essentially localized MCP servers"](../concepts/cli-tools-for-agents.md). The headline result is "the almost complete absence of hallucinations" — even with a two-year-old Haiku model.

## Key Claims

1. **Hallucinations are more prone in Python files.** Having the agent write Python artifacts for ad hoc / exploratory analysis is unnecessary and is "where hallucinations are more prone to happen." Driving the DuckDB CLI instead keeps the agent in SQL against a real engine. See [LLM Limitations](../concepts/llm-limitations.md).
2. **Why CLI tools suit agents** (collected in [CLI Tools for Agents](../concepts/cli-tools-for-agents.md)): baked-in functions keep the agent focused; fast iteration loop instead of one big script to debug; errors handled behind the scenes while you wait; no Python-script artifacts; local credential handling; trivially parallelizable; agents already know DuckDB and its CLI; works with cheap models; no MCP needed; the terminal is the whole environment.
3. **Cheap models are enough** for data analysis and research (author uses a two-year-old Haiku).
4. **MCPs are for SaaS platforms**; for analytics on local/lake data, use the CLI.
5. **Skill files are not very useful for analytics**, and **semantic layers add only marginal gains** when the gold layer is clean. A short `CLAUDE.md` (use DuckDB CLI only, the `ATTACH` statement, "secrets already stored") is enough. Contrast with [Agentic Analytics](../concepts/agentic-analytics.md), where skills and a semantic layer were decisive at enterprise scale.
6. **AI is "flawless" at data cleaning** (type fixes, trimming, NULL handling, concatenation, reshaping) but "sketchy" on complex joins that need subject-matter expertise.

## The Four Tips

| Tip | Gist |
|-----|------|
| Stay in the terminal | Claude Code + DuckDB CLI in a modern terminal (Ghostty) with split panes: file system / DuckDB / agent. Save results as markdown so they become context for later prompts. |
| Let AI do the annoying things | Penguins example: assess dataset → find bad types → assess NULLs → fix types → write cleaned file, in <10 seconds. Sanity-check immediately in DuckDB. |
| Authorize credentials locally | DuckDB's persistent secrets manager means the agent passes SQL (`ATTACH 'ducklake:ducklake_prod'`) and never reads credentials. Production DuckLake = Postgres catalog + S3 data, with a third secret referencing both. |
| Parallel agents | One agent proposes four analyses; four agents run them concurrently. Each spins up its own in-memory DuckDB, so use Parquet/CSV or a DuckLake with a Postgres catalog — a single DuckDB file allows one connection. Outputs: markdown or interactive HTML. |

## Notable Quotes

> "Python files are also where hallucinations are more prone to happen."

> "Coming back to when I created the CLI tools helped me understand that where AI agents thrive is working with those terminal tools. That's because there is already a set of functions baked into them that keeps an agent focused."

> "When I was trying to use Cursor or another IDE for analytics, I was bringing a bazooka to a knife fight."

## Caveats

- Anecdotal, single practitioner; the hallucination claim for Python is asserted, not measured.
- Scope is exploratory analytics on clean gold-layer data, not production pipelines (compare [Write-Audit-Publish](../concepts/write-audit-publish.md) and [Data Contracts](../concepts/data-contracts.md)).
- Opening thesis: copying someone else's AI workflow doesn't transfer — tips travel better than workflows.

## See Also

- [CLI Tools for Agents](../concepts/cli-tools-for-agents.md)
- [DuckLake](../concepts/ducklake.md) · [Source: DuckLake Maintenance Strategy](ducklake-maintenance-strategy.md)
- [DuckDB](../entities/duckdb.md) · [DuckDB for Agents](../concepts/duckdb-for-agents.md)
- [LLM Limitations](../concepts/llm-limitations.md)
- [Semantic Layer](../concepts/semantic-layer.md) · [Claude Skills](../concepts/claude-skills.md)
