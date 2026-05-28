---
tags: [data-n-ai, concept, agents]
sources: ["raw/data-n-ai/articles/We're Missing Data The Other Half of AI Transformation.md"]
updated: 2026-05-20
---

# AI Org Operating Model

Framework for thinking about what has to change in a data or engineering organisation when AI tools are adopted at scale. Proposed by Eric Weber. The core claim: AI transformation has two stacks that must be funded together. They multiply — not add.

## The Two-Stack Model

**Technical stack** (well-funded): model providers, eval infrastructure, agent frameworks, applications, throughput metrics. This is what gets the budget and executive attention. "Comparatively easy to know what to do about."

**Operating stack** (typically left to drift): manager redesign, career architecture, team composition, data-product partnership, stakeholder trust, communication norms. "Almost nobody is funding deliberately."

### Why Multiplicative, Not Additive

- Technical investment × stuck operating model → productivity bump, then **plateau**
- Modest technical investment × updated operating model → lower initial throughput, but **compounding capability** over time

A multi-million-dollar AI tooling budget with no equivalent investment in operating transformation funds one half and hopes the other happens for free.

## Operating Transformation Components

### Manager Redesign
The **manager-as-router** model (assign tickets, unblock, run standups) is dissolving. The replacement: **manager-as-coach** — develop judgment, set quality bars, calibrate review of AI output.

People who were excellent managers under the old model often struggle under the new one, and most companies are not helping them make the transition.

### Career Architecture
The IC ladder (associate → senior → staff, with "data scientist" or "ML engineer" titles) no longer maps to the actual work. Three distinct job shapes exist now:
1. AI output curators — reviewing, calibrating, and improving AI-generated work
2. Algorithm and primitive writers — building the systems AI builds on top of
3. End-to-end orchestrators — owning complete product surfaces

Promotions and skips calibrated on the old model are increasingly misaligned with actual impact.

### Team Composition
Most teams are still sized as if every engineer produces work the same way. The rebalance that high-performing teams have made:
- **More**: people on data, evaluation, and trust functions
- **Fewer**: people on pure feature execution

Most companies treat this as headcount drama. A few treat it as a deliberate operating choice. The deliberate ones get better outcomes.

### Data-Product Partnership
PMs can now generate first-pass analyses in ~15 minutes with Claude or ChatGPT. The data function's value has shifted:
- **Was**: source of analyses
- **Now**: defining what analyses should mean; calibrating evidence quality; building measurement infrastructure the product team uses for decisions

Both sides are "operating on a contract that is no longer current."

### Stakeholder Trust
With AI in the loop, throughput is a noisy signal — anyone can point to tokens processed, tickets closed, lines accepted. Teams that handle this well invest in:
- Shorter feedback loops
- More visible decisions
- Plain language explanations of what changed and why

Without this investment, stakeholders quietly conclude the team is less valuable, even when it has become more valuable.

### Communication Norms
"We ran an analysis" is no longer sufficient — it doesn't differentiate from anyone with a Claude window. What lands now:

> "We made this decision based on this evidence and here is what we expect to see."

The shift sounds small. It is actually a redesign of how the team relates to the rest of the company.

## Role Convergence: The End of "Data Engineer"

Chris Riccomini's complementary thesis: the over-specialisation of the data role (data engineer / data scientist / ML engineer / analytics engineer as separate titles) is a liability that AI is now dissolving. AI can handle the grunt work of each — inspecting failed pipelines, writing SQL, training models — making the distinctions less meaningful.

The predicted consolidation: a unified "data" role covering data engineering, analytics, and ML/AI. This aligns with Eric Weber's career architecture changes above — the three new job shapes (curators, primitive writers, orchestrators) cut across the old title boundaries. See [Source: Plan Mode All the Time](../sources/2026-05-21-plan-mode-substrait-de-role.md).

## See Also

- [Source: We're Missing Data — The Other Half of AI Transformation](../sources/ai-org-operating-model.md)
- [Source: Plan Mode All the Time](../sources/2026-05-21-plan-mode-substrait-de-role.md)
- [Chris Riccomini](../entities/chris-riccomini.md)
- [Iterative Repair Loops](iterative-repair-loops.md)
