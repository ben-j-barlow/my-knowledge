---
tags: [investing, data-n-ai, concept, semiconductors, memory, hbm, ai-infra]
sources: ["raw/investing/articles/SK Hynix is about $50bn away from being a trillion-dollar company.md", "raw/investing/articles/Samsung Begins HBM4 Shipments as SK Hynix Lags and a 50,000-Worker Strike in Five Days Threatens the AI Chip Supply.md", "raw/investing/articles/SK Hynix Shares Hit All-Time High as Tech Giants Offer to Co-Finance New Chip Plants.md"]
updated: 2026-05-19
---

# High Bandwidth Memory (HBM)

Stacked DRAM architecture that sits physically adjacent to the GPU die on AI accelerators. HBM stacks multiple DRAM dies vertically using through-silicon vias (TSVs) and connects them directly to the processor via an interposer. The result: dramatically higher memory bandwidth at lower power than conventional DRAM modules placed on a PCB.

## Why HBM Matters for AI

For LLM inference, memory bandwidth — not raw compute — is increasingly the binding constraint. Moving model weights from memory to GPU arithmetic units is the bottleneck; HBM reduces it by placing far more bandwidth directly adjacent to the chip.

> "At $948bn, SK Hynix is no longer a memory company that benefits from AI. It is being valued as the structural counterparty to it." — The Next Web, May 2026

## Generations

| Generation | Key Platform | Notes |
|-----------|-------------|-------|
| HBM3E | Nvidia Hopper/Blackwell, Microsoft Maia 200 | Current production; SK Hynix dominant |
| HBM4 | Nvidia Vera Rubin | Samsung: first to ship (Feb 2026), 11.7 Gbps (46% above JEDEC 8 Gbps); SK Hynix: ramping |
| HBM4E | Nvidia next-gen | SK Hynix: samples H2 2026, mass production 2027; Samsung: samples Q2 2026 |

## Market Structure

Three producers, sharply unequal share:
1. **SK Hynix** — ~57% market share; ~70% of Nvidia's HBM orders
2. **Samsung** — ~30%+; first to mass-produce HBM4
3. **Micron** — third; smaller share

No credible fourth HBM producer.

## Supply and Capacity Dynamics

Each HBM wafer produced displaces ~3 conventional DRAM wafers from fab capacity. This reallocation is causing:
- Q1 2026 DRAM contract prices: +90–95% vs Q4 2025
- Goldman Sachs 2026 supply-demand gap forecast: 4.9% (worst in 15 years)
- Gartner: DRAM prices +47% in 2026; DRAM+SSD combined +130% by end 2026
- PC unit shipments: ~10.4% decline projected as component costs rise
- Consumer price relief not expected before late 2027 or 2028

## Hyperscaler Demand

2026 HBM supply from both SK Hynix and Samsung is sold out. Microsoft, Google, and Amazon have offered to co-finance ASML EUV lithography machines (~$400M each) at SK Hynix for guaranteed supply access. Hyperscalers are locking multi-year contracts; mid-market buyers compete for residual spot supply.

## Key Production Equipment

TC bonders are the critical tool for HBM die stacking. [HANMI Semiconductor](../entities/hanmi-semiconductor.md) holds #1 global TC bonder market share.

## See Also

- [Advanced Packaging](advanced-packaging.md)
- [AI Semiconductor Supply Chain](ai-semiconductor-supply-chain.md)
- [SK Hynix](../entities/sk-hynix.md)
- [Samsung Electronics](../entities/samsung-electronics.md)
- [HANMI Semiconductor](../entities/hanmi-semiconductor.md)
- [TSMC](../entities/tsmc.md)
