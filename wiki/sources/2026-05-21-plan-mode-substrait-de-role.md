---
tags: [data-n-ai, source, agents, etl, pipelines, prompt-engineering]
sources: ["raw/data-n-ai/articles/Plan Mode All the Time, Substrait over SQL, and the End of the DE Role ft. Chris Riccomini.md"]
updated: 2026-05-28
---

# Source: Plan Mode All the Time, Substrait over SQL, and the End of the DE Role

**Author:** MotherDuck (interview with Chris Riccomini)
**Published:** 2026-05-21
**URL:** https://motherduck.com/blog/cost-as-tokens-substrait-llm-chris-riccomini/

Second interview in MotherDuck's "How to use AI with DE" series. Chris Riccomini (Apache Samza, SlateDB, co-author DDIA 2nd ed) covers AI correctness in financial data, Substrait vs SQL for LLMs, the Ralph Loop for context management, agent security, and the future of the data engineer role.

## Part 1: Correctness in Financial Data

**Risk/fraud:** Requires model explainability (why the model made the decision) — random forest was preferred at WePay for this reason.

**Data engineering:** "More like a traditional data modeling situation." Define invariants that must always hold (ledger sums up). Traditional data verification tools still apply — AI just generates the pipelines.

**Analytics:** Legitimate fear of hallucination, but also a pre-existing problem. Chris's view has shifted: with a human in the loop, the latest LLMs may actually *improve* accuracy vs. solo human analysts because they're better at spotting bugs and inconsistencies.

## Part 2: Substrait Over SQL

**Core claim:** LLMs should communicate data transformations in Substrait rather than SQL.

**Why:** SQL is purely logical ("JOIN") — it says *what* but not *how*. Substrait can express both logical and physical operators ("merge join" or "hash join"). This gives LLMs the ability to:
1. Use fewer tokens for equivalent transformations (more efficient serialization)
2. Perform client-side query optimization — choose physical execution strategy and pass a physical plan directly to the DB
3. Reduce hallucination by constraining output to a structured grammar

**Caveat:** SQL is vastly overrepresented in LLM training data; Substrait is not. Adoption would require deliberate effort.

## Part 3: Plan Mode and the Ralph Loop

**Plan mode all the time:** Don't flip from "plan" to "implement." Iteratively probe and expand the plan through many rounds — ask for details, expand sections, challenge assumptions — until there is no possible way the implementation can go wrong.

**The Ralph Loop** (from ghuntley.com/loop/): A bash loop that repeatedly prompts an agent with the same goal until external tests pass. Forces the agent to work, fail, and fix — rather than declaring itself done. Handles the failure case that human-guided plan mode leaves open.

**Quality gates — three steps:**
1. Define what quality means for your use case (e.g., test coverage)
2. Measure it (e.g., coverage tool in CI)
3. Enforce thresholds (e.g., `CLAUDE.md` rule + git commit hook)

**Incremental loads for determinism:** Convert full batch loads to incremental daily loads to reduce non-determinism scope. A re-run of an incremental job only re-introduces non-determinism into the last day's data — acceptable for most use cases.

## Part 4: Security — "Okta for Agents"

Agents in the enterprise are a nightmare to manage: arbitrary skills loaded from marketplaces, hidden code injection via comments in repos, no auditability.

> "We absolutely need lineage, auditability, RBAC, ABAC, and so on. It's the wild west right now."

Chris had been advocating "Okta for Agents" independently of Maxime Beauchemin. MCP's initial security model was "completely lacking" — they've since added better support.

## Part 5: Future of AI and DE Role

**What agents already do well:** Inspect failed GitHub Actions, run SQL queries, write Python — all the grunt work of data engineering. Self-healing pipelines are feasible; tooling and practices haven't yet adapted (Amdahl's Law for AI tools: agents can be 50x faster but tools are designed for human speed).

**DE role convergence:** "Data engineer" as a distinct role may dissolve into a unified "data" role covering DE + ML + analytics. Chris has been pushing this thesis for years; AI accelerates it.

**Agent ergonomics / cost-as-tokens:** Language choice is shifting to what produces the smallest, fastest, cheapest LLM output — not what's most ergonomic for humans. Chris now doesn't care what language his projects are in; he cares about performance, stability, and token cost.

**On learning with AI:** Using AI to build SlateDB language bindings (Node, Java, Python, Go), Chris learned CBingen, UniFFI, FFIs from scratch. He would have learned more without AI but wouldn't have done the work at all.

## Related Pages

- [Chris Riccomini](../entities/chris-riccomini.md)
- [Substrait](../concepts/substrait.md)
- [Ralph Loop](../concepts/ralph-loop.md)
- [Query Optimization](../concepts/query-optimization.md)
- [Data Ingestion](../concepts/data-ingestion.md)
- [AI Org Operating Model](../concepts/ai-org-operating-model.md)
- [Human-in-the-Loop](../concepts/human-in-the-loop.md)
