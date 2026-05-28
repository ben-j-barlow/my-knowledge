---
tags: [data-n-ai, entity]
sources: ["raw/data-n-ai/articles/Plan Mode All the Time, Substrait over SQL, and the End of the DE Role ft. Chris Riccomini.md"]
updated: 2026-05-28
---

# Chris Riccomini

Software engineer, author, investor, and advisor. One of the most experienced practitioners in the data engineering space, spanning distributed systems, stream processing, and the AI transition.

## Background

Previously at WePay (data engineering and financial data), LinkedIn, and PayPal. Built financial data systems where correctness and invariant-checking were non-negotiable.

## Notable Work

- **Apache Samza**: Distributed stream processing framework (Apache project)
- **SlateDB**: Embedded key-value store built on object storage (current primary project)
- **Apache Airflow PMC** member
- Co-author of the 2nd edition of *Designing Data-Intensive Applications* (with Martin Kleppmann)
- Author of *The Missing README: A Guide for the New Software Engineer*

## Current Activity

- **Investment:** Materializedview.capital
- **Newsletters:** [rng.md](https://rng.md/) (current — engineering, VC, AI) and [Materialized View](https://materializedview.io/) (older, still rich archive)
- Advocates "merge analytics and data engineers" — the over-specialization of the data role is now a liability

## Key Views

- LLMs should speak **Substrait**, not SQL, for data transformations
- **Plan mode all the time** — never flip to implementation without exhaustive iterative refinement of the plan
- **Agent ergonomics** over human ergonomics in language selection: performance, stability, and token cost win
- **Data engineer as distinct role** will likely dissolve into a unified data role (DE + ML + analytics)
- **"Okta for Agents"** is necessary — enterprise agents need RBAC, ABAC, lineage, auditability
- MCP's initial security model was "completely lacking"

## Related Pages

- [Source: Plan Mode All the Time](../sources/2026-05-21-plan-mode-substrait-de-role.md)
- [Substrait](../concepts/substrait.md)
- [Ralph Loop](../concepts/ralph-loop.md)
- [AI Org Operating Model](../concepts/ai-org-operating-model.md)
