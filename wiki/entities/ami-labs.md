---
tags: [data-n-ai, entity, world-models, robotics]
sources: [raw/data-n-ai/articles/AI for the Real World A conversation with Yann LeCun.md]
updated: 2026-05-14
---

# AMI Labs

**Advanced Machine Intelligence** (pronounced "ah-mee," the French word for friend). Founded by Yann LeCun; backed by Zetta Ventures.

## Mission

Build JEPA-based world models for physical-world AI. Targets environments where current LLM-based AI falls short: industrial process control, automation, wearable devices, robotics, healthcare.

## Thesis

A large portion of the economy runs on physical systems — factories, supply chains, power grids, biological systems, transportation. Text is the *interface* around this work, not the work itself. The systems capable of operating in these environments need a base-level understanding of the world and the ability to predict consequences of actions. AMI is building generic foundation models applicable to any situation requiring an intelligent system to run something physical.

## Architectural Bet

JEPA-style abstract representation over pixel-level generation. Abstract state prediction is cheaper to deploy, more robust to noise, and body-agnostic — the same model of physics applies across robot embodiments and industrial contexts.

## See Also

- [Yann LeCun](yann-lecun.md)
- [World Models](../concepts/world-models.md)
