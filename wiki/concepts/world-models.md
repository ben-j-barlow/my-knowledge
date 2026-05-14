---
tags: [data-n-ai, concept, world-models, robotics]
sources: [raw/data-n-ai/articles/AI for the Real World A conversation with Yann LeCun.md]
updated: 2026-05-14
---

# World Models

A system that learns how the world evolves and can predict the consequences of actions — the proposed alternative to LLM-based AI for physical and agentic tasks.

## Core Idea

Reasoning is search. To plan, a system needs an internal model to search through: simulate a candidate action, evaluate the predicted state, revise. LLMs have no such model — they sample tokens directly, which is why chain-of-thought is a workaround rather than genuine reasoning.

## JEPA

LeCun's proposed architecture (Joint Embedding Predictive Architecture). Predicts in **abstract latent space** rather than at the pixel level. Details that aren't predictable (noise, exact pixel values) are discarded in the representation; causally relevant structure is preserved. Result: reliable predictions without being penalised for failing to model randomness.

## Key Advantage Over LLMs

World models can learn from unlabelled video — the largest available data corpus — because they target state prediction, not action labels. Abstract state is also body-agnostic, enabling embodiment transfer without retraining.

## Landscape (mid-2026)

| Company | Approach |
|---------|----------|
| AMI Labs (LeCun) | JEPA abstract state; industrial/physical AI |
| World Labs (Fei-Fei Li) | 3D world generation from text/image/video |
| Google DeepMind Genie 3 | Interactive world generation |
| 1X / Generalist AI | Video-pretrained models for humanoid robotics |
| NVIDIA Cosmos | Platform for physical AI world models |
| Tesla | Unified model for vehicles and humanoid robots |

Key fork: predict pixels/geometry vs. predict abstract state.

## See Also

- [LLM Limitations](llm-limitations.md)
- [Robotics](robotics.md)
- [Yann LeCun](../entities/yann-lecun.md)
- [AMI Labs](../entities/ami-labs.md)
