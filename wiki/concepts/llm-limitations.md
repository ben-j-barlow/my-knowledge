---
tags: [data-n-ai, concept, llm]
sources: [raw/data-n-ai/articles/AI for the Real World A conversation with Yann LeCun.md]
updated: 2026-05-14
---

# LLM Limitations

Structural limits of large language models — what they cannot do regardless of scale, and why.

## No World Model

LLMs predict the next token. They have no internal model of how the world evolves and cannot predict the consequences of actions. This makes them fundamentally unsuited to reliable agentic use: an agent that cannot simulate outcomes before acting cannot plan.

## Intelligence Is Not Mostly Language

LeCun's estimate: a 4-year-old receives ~10^14 bytes of visual data in their first four years of life — the same order of magnitude as an LLM's entire training corpus. The child also receives tactile, auditory, and proprioceptive data on top of this. Intelligence is built primarily from embodied, sensorimotor experience, not from language. Training exclusively on text cannot close this gap.

> "We're never going to get to human-level AI by just training on text. It's just not going to happen." — Yann LeCun

## Declarative Knowledge vs. Understanding

LLMs accumulate and retrieve declarative knowledge well. They become more familiar with the kinds of questions people ask over time. But this is distinct from building a deeper model of reality — they look smarter without understanding more.

## Where LLMs Do Work

LeCun's own concession: LLMs are well-suited to **coding and math**. In these domains, symbol manipulation *is* the substrate of reasoning — the work is in manipulating discrete, compressible tokens. Outside these domains, the architecture hits a ceiling.

## Chain-of-Thought Is a Workaround

Chain-of-thought prompting is described as "a very, very inefficient way of coercing autoregressive prediction systems to approach reasoning." Real reasoning is internal simulation: running mental models, testing counterfactuals, planning hierarchically. CoT approximates this by externalising intermediate steps as tokens, but the underlying system still has no model to search through.

## The Language Bias

Humans attribute intelligence to things that express themselves fluently in language. LLMs exploit this bias. Fluency is not understanding.

## See Also

- [World Models](world-models.md)
- [Yann LeCun](../entities/yann-lecun.md)
