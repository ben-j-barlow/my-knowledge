---
tags: [data-n-ai, source, llm, world-models, robotics]
sources: [raw/data-n-ai/articles/AI for the Real World A conversation with Yann LeCun.md]
updated: 2026-05-14
---

# AI for the Real World: A Conversation with Yann LeCun

> Source: https://x.com/AnneliesGamble/status/2054219457451733382
> Author: Annelies Gamble (interview)
> Published: 2026-05-12

## Summary

LeCun argues LLMs are commercially useful but architecturally incapable of reaching human-level intelligence. The core problem: they predict tokens, not world states. His alternative — world models using JEPA — learns abstract representations of how the world evolves, enabling planning and action prediction. He recently founded AMI Labs to build this for industrial and physical-world applications.

## Key Claims

- LLMs cannot predict the consequences of actions — a prerequisite for any reliably agentic system
- A 4-year-old receives ~10^14 bytes of visual data, the same order of magnitude as an LLM's entire training corpus — text alone is insufficient for human-level intelligence
- LLMs excel in coding and math because symbol manipulation *is* the substrate of reasoning in those domains; elsewhere, they hit a ceiling
- Chain-of-thought is "a very inefficient way of coercing autoregressive systems to approach reasoning" — not real reasoning
- JEPA predicts in abstract latent space rather than at the pixel level, removing noise and preserving causal structure
- World models unlock learning from unlabelled video — the largest available corpus — by targeting state prediction rather than action labels
- The relevant frame is not AGI but "Superhuman Adaptable Intelligence" (SAI): solving problems you weren't trained on

## Notable Quotes

> "Will these models take us to human-level intelligence or something similar to it? Absolutely no."

> "If you want a system to act intelligently, it has to be able to predict the consequences of its actions. And LLMs are completely incapable of doing this."

> "Language will serve as an interface to a system that thinks."

## Related Wiki Pages

- [World Models](../concepts/world-models.md)
- [LLM Limitations](../concepts/llm-limitations.md)
- [Yann LeCun](../entities/yann-lecun.md)
- [AMI Labs](../entities/ami-labs.md)
