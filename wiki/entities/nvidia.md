---
tags: [investing, data-n-ai, entity, semiconductors, ai-infra]
sources: [raw/investing/articles/2026-05-17-treasury-yields-testing-ai-equity-rally.md]
updated: 2026-05-20
---

# Nvidia

Dominant AI accelerator company. Designs the GPUs that power virtually all large-scale AI training and most inference workloads. Competitive moat rests on three interlocking components: GPU hardware, NVLink high-speed interconnect, and the CUDA software ecosystem that the vast majority of AI research and production code is written against.

## Role in the AI Supply Chain

Nvidia sits at the top of the [AI semiconductor supply chain](../concepts/ai-semiconductor-supply-chain.md): it designs the accelerators that consume HBM (from SK Hynix, Samsung, Micron) and are fabricated and packaged by TSMC. The GPU die is the logic component bonded to HBM stacks via CoWoS advanced packaging.

- **SK Hynix** supplies ~2/3 of Nvidia's HBM4 for Vera Rubin generation
- **TSMC** is the exclusive advanced-node foundry for Nvidia GPUs
- Nvidia therefore concentrates supply-chain risk at both memory and logic layers

## Key Products

| Generation | Notes |
|---|---|
| H100 / H200 | Hopper architecture; primary training workhorse 2023–2024 |
| Blackwell (B100/B200) | Current generation; multi-die NVLink configuration |
| Vera Rubin | Next generation; HBM4 |

## Investment Characteristics

Nvidia is the archetype **long-duration growth stock**. A substantial portion of its valuation is tied to projected future cash flows from AI infrastructure buildout, rather than current earnings. This creates high sensitivity to changes in the discount rate (see [equity duration](../concepts/equity-duration.md)).

Even with strong earnings, Nvidia's stock is vulnerable when long-term Treasury yields rise — not because the business is deteriorating, but because the present value of its future cash flows shrinks mechanically as the discount rate increases.

As of May 2026, with the 30-year Treasury above 5%, this dynamic is live: Nvidia continues to post excellent results but faces multiple compression pressure.

## See Also

- [AI Semiconductor Supply Chain](../concepts/ai-semiconductor-supply-chain.md)
- [HBM](../concepts/hbm.md)
- [TSMC](tsmc.md)
- [SK Hynix](sk-hynix.md)
- [Equity Duration](../concepts/equity-duration.md)
- [Agentic Inference](../concepts/agentic-inference.md)
- [Source: Treasury Yields Are Testing The AI Equity Rally](../sources/treasury-yields-testing-ai-equity-rally.md)
