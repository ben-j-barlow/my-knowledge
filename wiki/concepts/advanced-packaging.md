---
tags: [investing, data-n-ai, concept, semiconductors, advanced-packaging, ai-infra]
sources: ["raw/investing/articles/Buy TSMC stock as 'recent concerns are overdone' BofA.md", "raw/investing/articles/HANMI Semiconductor Accelerates U.S. Expansion, Establishes Hanmi USA.md"]
updated: 2026-05-19
---

# Advanced Semiconductor Packaging

Methods for integrating multiple chips or dies into a single package with far shorter interconnects than traditional PCB-level assembly. Enables AI accelerators to connect logic dies (GPUs, TPUs) with HBM at very high bandwidth and low latency. As process node scaling slows, packaging has become a key source of system-level performance gains.

## Key Technologies

### CoWoS (Chip on Wafer on Substrate) — TSMC
Mounts the logic die and HBM dies on a silicon interposer, then on a substrate. The dominant method for packaging current AI accelerators (Nvidia H100/H200/Blackwell).

- TSMC CoWoS yield: **>98%** (May 2026)
- Capacity CAGR: **80%** through 2027

### SoIC (System on Integrated Chips) — TSMC
True 3D die-to-die stacking with fine-pitch bonding. Denser integration than CoWoS.

- Capacity CAGR: **90%** through 2027

### EMIB-T (Embedded Multi-die Interconnect Bridge – Tile) — Intel
Intel's competing approach to CoWoS.

- Pilot yield: **80–85%** (May 2026)
- Must reach 95% for mass production by mid-2027 — execution risk flagged by BofA

### TC Bonder (Thermocompression Bonder)
Equipment that bonds HBM dies together and to logic dies under heat and pressure. Critical for every HBM chip shipped.

- **[HANMI Semiconductor](../entities/hanmi-semiconductor.md)**: #1 global TC bonder market share
- Key products: 2.5D TC Bonder 40 and 2.5D TC Bonder 120

### Hybrid Bonding
Next-generation bonding with finer pitch and better power efficiency than thermocompression. Enables denser stacking.

- HANMI: second-generation hybrid bonder prototype expected H2 2026

### BOC COB Bonder (Chip on Board)
Memory chip-on-board packaging; HANMI began shipping to global memory companies in 2026.

## Why Packaging Matters Now

At the 3nm and N2 nodes, each die shrink is harder and more expensive to achieve. Packaging allows chipmakers to deliver system-level performance improvements by stacking or tiling multiple dies — a path that scales faster than lithography alone. The yield and throughput with which a company can execute advanced packaging has become a competitive moat comparable to its node leadership.

## See Also

- [HBM](hbm.md)
- [AI Semiconductor Supply Chain](ai-semiconductor-supply-chain.md)
- [TSMC](../entities/tsmc.md)
- [HANMI Semiconductor](../entities/hanmi-semiconductor.md)
