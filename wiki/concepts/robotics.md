---
tags: [data-n-ai, concept, robotics, world-models]
sources: [raw/data-n-ai/articles/AI for the Real World A conversation with Yann LeCun.md]
updated: 2026-05-14
---

# Robotics

AI applied to physical robot systems. Currently dominated by VLA models; world models are the proposed next step.

## Current Dominant Approach: VLAs

Vision-language-action (VLA) models map observations directly to motor commands. Useful but hit two structural ceilings:

1. **Data scarcity** — teleoperated robot data is high quality but doesn't scale; bounded by robot count and operator hours
2. **Embodiment lock-in** — policies trained on one robot body transfer poorly to another; knowledge is captured at the level of "how this robot moves" rather than "what should happen in the world"

Workarounds exist (UMI grippers, wearable rigs, cross-embodiment datasets, sim pipelines) but each has an embodiment gap to bridge.

## World Models as the Alternative

State prediction rather than action prediction:

- Learned from unlabelled human video (no action labels needed)
- Abstract state is body-agnostic — physics is the same regardless of embodiment
- Enables calibration to a new body rather than full retraining

## Key Players

- **1X** — video-pretrained world model; uses a second model to convert state predictions into motor commands
- **Generalist AI** — trains on ~500K hours of wearable-captured human interaction data
- **AMI Labs** — JEPA-based; targeting industrial robotics and process control
- **Tesla** — unified model for vehicles and humanoid robots

## See Also

- [World Models](world-models.md)
- [AMI Labs](../entities/ami-labs.md)
