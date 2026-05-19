---
tags: [investing, data-n-ai, concept, semiconductors, ai-infra, macro]
sources: ["raw/investing/articles/SK Hynix is about $50bn away from being a trillion-dollar company.md", "raw/investing/articles/Samsung Begins HBM4 Shipments as SK Hynix Lags and a 50,000-Worker Strike in Five Days Threatens the AI Chip Supply.md", "raw/investing/articles/SK Hynix Shares Hit All-Time High as Tech Giants Offer to Co-Finance New Chip Plants.md", "raw/investing/articles/Buy TSMC stock as 'recent concerns are overdone' BofA.md"]
updated: 2026-05-19
---

# AI Semiconductor Supply Chain

The physical stack of companies, technologies, and equipment required to produce AI accelerators. As of 2026, this chain is extremely concentrated, subject to geopolitical risk, and being bid up by hyperscalers in a way that is restructuring memory and foundry markets globally.

## The Stack

```
AI Model / Inference Workload
          ↓
AI Accelerator (Nvidia GPU, Google TPU, Microsoft Maia, Amazon Trainium)
          ↓
Logic Die + HBM stack — bonded via CoWoS or similar advanced packaging
          ↓
  HBM production          Logic die (foundry)
  SK Hynix  57%           TSMC  ~90% advanced nodes
  Samsung   ~30%          Samsung Foundry  ~5%
  Micron    ~13%
          ↓
TC Bonder equipment       EUV Lithography
HANMI (#1 global)         ASML (monopoly, ~$400M/machine)
```

## Structural Dynamics (2026)

### Supply Constraints
- **HBM 2026**: Sold out at both SK Hynix and Samsung; shortages expected into 2027
- **DRAM displacement**: Each HBM wafer displaces ~3 conventional DRAM wafers — creating a parallel DRAM shortage
- **TSMC advanced packaging**: CoWoS lead time a known bottleneck for Nvidia shipment scheduling

### Hyperscaler Co-Investment
Microsoft, Google, and Amazon are offering to co-finance ASML EUV machines at SK Hynix (~$400M each) for guaranteed supply. Big Tech combined 2026 capex: ~$725B. This is unprecedented — end customers bankrolling their suppliers' capacity expansion.

### Geopolitical Risk
- US removed Samsung and SK Hynix from Verified End User (VEU) program in September 2025 → annual license required for China operations
- TSMC advanced node expansion depends on Taiwan and US stability
- Annual US export control licensing creates material uncertainty for Korean companies' China factories

## Concentration Risk

| Layer | Dominant Player(s) | Concentration |
|-------|--------------------|---------------|
| HBM production | SK Hynix, Samsung | 2 players, ~87%+ |
| Logic foundry (advanced) | TSMC | ~90%+ of leading edge |
| EUV lithography | ASML | Monopoly |
| TC bonders (HBM packaging) | HANMI Semiconductor | #1 global |

## Investment Implications

- Companies anywhere in this stack with supply constrained by AI demand are structural beneficiaries, not cyclical
- Pick-and-shovel positions: HANMI (TC bonders), ASML (EUV), TSMC (packaging + logic)
- Pure-play memory exposure: SK Hynix, Samsung, Micron
- Key risks: geopolitical disruption (Korea, Taiwan), labor action (Samsung strike risk), technology transition stumbles (HBM4E yield ramp)

## Cross-Topic Note

This supply chain is the physical infrastructure that the data-n-ai compute stack depends on. LLM inference at scale is bounded by memory bandwidth (see [HBM](hbm.md)), not just GPU compute. The investment thesis for the AI memory stack is therefore also a thesis about the limits of AI scaling.

## See Also

- [HBM](hbm.md)
- [Advanced Packaging](advanced-packaging.md)
- [TSMC](../entities/tsmc.md)
- [SK Hynix](../entities/sk-hynix.md)
- [Samsung Electronics](../entities/samsung-electronics.md)
- [HANMI Semiconductor](../entities/hanmi-semiconductor.md)
- [Nebius Group](../entities/nebius-group.md)
