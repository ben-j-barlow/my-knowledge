---
tags: [investing, data-n-ai, synthesis]
updated: 2026-05-14
---

# Overview

Cross-topic synthesis and relationship map. Updated by the LLM as the wiki grows.

---

## Topics

### Investing

Current coverage is concentrated in the AI infrastructure trade and adjacent sectors.

**AI memory supply chain:** The dominant theme. SK Hynix and Samsung hold the only meaningful HBM supply — the stacked DRAM that powers Nvidia, Google, and AMD AI accelerators. 2026 HBM supply is sold out at both companies. Hyperscalers (Microsoft, Google, Amazon) are now offering to co-finance supplier capacity expansion, a structural signal of how constrained the market is. The HBM capacity reallocation is simultaneously causing the worst DRAM shortage in 15 years. SK Hynix sits at ~$948B market cap (9x in 2 years); Samsung crossed $1T on May 6.

**Pick-and-shovel semiconductor exposure:** TSMC (foundry moat — N2 two quarters ahead; CoWoS >98% yield) and HANMI Semiconductor (TC bonders, #1 global share, US expansion underway) provide indirect AI infrastructure exposure with differentiated competitive moats.

**Space:** Rocket Lab is scaling from small-lift (Electron) to medium-lift (Neutron) while vertically integrating into satellite subsystems. Q1 2026: $200M revenue (+63%), record backlog, Neutron nearing first flight.

**Robotics/EV:** Tesla thesis has shifted away from EVs — the Piper Sandler SOTP assigns ~$400/share to 17 non-Optimus lines, treating Optimus as free optionality. Musk projects 80% of Tesla's value will eventually be Optimus.

**Energy storage:** Eos Energy (zinc BESS) passed a key bankability test: Cerberus Capital committed $100M and a 2 GWh supply deal via Frontier Power USA. Q1 revenue +445%. Technology differentiator: zinc chemistry vs. lithium-ion for long-duration storage.

Subtopics tracked: `semiconductors`, `hbm`, `foundry`, `advanced-packaging`, `equities`, `ev`, `robotics`, `space`, `energy-storage`, `quantum-computing`, `ai-infra`

### Data & AI

Current coverage spans two threads:

**LLM limitations and world models:** LLMs are commercially valuable but architecturally incapable of predicting action consequences — which Yann LeCun argues disqualifies them for general intelligence. World models (JEPA) are the proposed alternative, learning abstract state representations enabling planning and embodiment.

**Agentic patterns:** Iterative repair loops are an emerging practical pattern for agentic maintenance tasks — closed-loop workflows where an agent reviews an artifact, repairs it, validates the result, and feeds failures back as input to the next pass. The key insight is that separating review / repair / validate with structured JSON handoffs makes agent output auditable and trustworthy, not just impressive.

Subtopics being tracked: `llm`, `world-models`, `robotics`, `agents`, `prompt-engineering`

---

## Cross-Topic Connections

*Populated by the LLM as connections emerge.*

| Connection | Topics | Notes |
|-----------|--------|-------|
| HBM supply constraint = AI inference bottleneck | investing + data-n-ai | Memory bandwidth is the binding constraint for LLM inference at scale. The investment case for SK Hynix/Samsung is the same phenomenon LeCun's world-model critique points at from the other side: LLM-style compute scaling hits physical limits. |
| Hyperscaler capex → semiconductor supply chain | investing + data-n-ai | Big Tech's $725B 2026 capex must exit through HBM, CoWoS, and EUV. The AI infrastructure buildout (data-n-ai) is the demand signal for the semiconductor supply chain investment thesis (investing). |
| Nebius Group as AI cloud infrastructure play | investing + data-n-ai | GPU cluster operators like Nebius are the customers of the HBM/TSMC stack and the infrastructure layer below LLM APIs. |
| Tesla Optimus + inference-as-a-service | investing + data-n-ai | Piper Sandler labels Optimus and "inference-as-a-service" as thesis-defining for Tesla — connecting robotics/embodied AI (data-n-ai) to equity valuation (investing). |

---

## Open Questions

*Questions surfaced during ingestion or Q&A that warrant further investigation.*

- (none yet)
