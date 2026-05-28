---
tags: [data-n-ai, concept, agents, prompt-engineering]
sources: ["raw/data-n-ai/articles/Exploring Agent-Assisted Qualitative Analysis.md"]
updated: 2026-05-28
---

# Grounded Theory

A qualitative research methodology for building theory directly from data rather than starting from a hypothesis and testing it. Widely used in social science, UX research, and increasingly as a lens for analysing agent logs, interview transcripts, and unstructured feedback corpora.

## Process

Three iterative stages:

**1. Open coding** — read through data and attach short labels (codes) to passages of interest. As new data is read, compare against existing codes: merge similar ones, split overly broad ones. The codes stay close to the language of the data.

**2. Axial coding** — group related codes into higher-level categories. Look for relationships between categories (causes, consequences, conditions). Example: codes "absent advisor," "shifting goals," and "no progress for months" cluster into *mentorship breakdown*; "social comparison" and "imposter feelings" into *identity strain*.

**3. Selective coding** — identify one or two core themes and organise the rest of the theory around them. The core category becomes the "spine" through which all other categories are explained.

**Memos** are written throughout: informal notes about emerging patterns, uncertainties, and possible interpretations. They preserve analytical reasoning across rounds.

**Theoretical saturation** is reached when new data stops producing new codes — typically around 60–80% declining new-code rate across batches.

## Why It's Hard for Agents

Grounded theory is one of the more tractable qualitative methods, but it poses two problems for current AI agents:

1. **Context outside the corpus:** The "right" analysis depends on the researcher's background, the intended audience, and the specific question being asked. Two analysts given identical data will produce legitimately different theories. Specifying this context explicitly is difficult.

2. **Evolving evaluation criteria:** Researchers discover what matters by interacting with the data over many rounds. The criteria for a "good" code or category at round 5 are different from round 1. Agents assume stable objectives — they converge on a framing early and treat the rest of the data as confirmatory. This produces coherent but premature theories.

The second problem is structural, not prompt-engineerable.

## Relationship to HITL

The most effective approach identified experimentally: human input at the *direction* level (memos), not the *artifact* level (editing individual codes). Telling the agent where to steer the analysis is more efficient and produces more substantive divergence than reviewing individual classifications. See [Human-in-the-Loop](human-in-the-loop.md).

## Related Pages

- [Human-in-the-Loop](human-in-the-loop.md)
- [LLM Limitations](llm-limitations.md)
- [Source: Agent-Assisted Qualitative Analysis](../sources/2026-05-21-agent-assisted-qualitative-analysis.md)
