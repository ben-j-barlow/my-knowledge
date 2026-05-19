---
tags: [data-n-ai, source, llm, agents, ai-infra, semiconductors, hbm]
sources: [raw/data-n-ai/articles/AI economics part 2.md]
updated: 2026-05-19
---

# AI Economics Part 2: Training, Human Inference, and Agentic Inference

> Source: https://x.com/sriramkri/status/2054594308494229882
> Author: @sriramkri (Sriram Krishnan)
> Published: 2026-05-14

## Summary

A detailed breakdown of the three distinct AI workloads — training, human inference, agentic inference — and how they stress hardware differently across all four components: CPU, GPU, HBM, DRAM. The key argument: current infrastructure was built and optimized for human inference (short, spiky, low-context). Agentic inference is a fundamentally different and harder problem that simultaneously stresses all four components, and no purpose-built silicon exists yet for it. HBM is entering a second supercycle driven by agentic AI's context appetite.

## Key Claims

### Workload Profiles

| Workload | GPU Pattern | HBM | DRAM | CPU |
|---------|------------|-----|------|-----|
| Training | Flat, sustained | Constant high-speed feed | Never touched | Spectator |
| Human inference | Spiky (mirrors human hours) | Heavy lifting | Largely idle | Traffic coordinator only |
| Agentic inference | Sustained with CPU gaps | Hard constraint; overflows to DRAM | Grows with task history, tool results | Primary player (every tool call) |

### Agentic Inference Is the Hardest
- 10–50x more compute per session than human inference
- Long context windows and task history overflow HBM's limited capacity → spills into DRAM
- Every external tool call: GPU hands off to CPU → CPU parses result, formats tokens, writes to DRAM → hands back to GPU
- A 2% error rate across 50 tool calls = task failure most of the time
- No purpose-built infrastructure exists; agentic workloads currently run on hardware designed for humans

### HBM: Two Supercycles
- Training caused the **first** HBM supercycle
- Agentic AI's appetite for long context is causing the **second**
- HBM capacity is extremely hard to build — can only bond so much memory to a chip before running out of space
- SK Hynix, Samsung, Micron dominate because of this physical constraint + decades of specialized packaging investment
- **CXL 3.0** is the most promising near-term fix: allows CPU and GPU to share a unified memory pool directly, eliminating the PCIe highway — but commercial deployment at scale is 2–3 years out (i.e. ~2028–2029)

### GPU Utilization Asymmetries
- Human inference: idle 3am–9am → "using a Ferrari to wheel groceries"
- Opportunity: idle capacity could run training, higher-margin products, or cheaper older models
- Inference-specific chips optimized for short-context, high-concurrency: Groq, AWS Inferentia

### Nvidia Moat
- Not just the GPU — **NVLink** (networking between GPUs) + **CUDA** (software ecosystem)
- "No one has matched all three yet"
- The ecosystem around GPUs becomes more critical as inter-chip communication overhead grows

## Related Wiki Pages

- [HBM](../concepts/hbm.md)
- [Agentic Inference](../concepts/agentic-inference.md)
- [AI Semiconductor Supply Chain](../concepts/ai-semiconductor-supply-chain.md)
- [Iterative Repair Loops](../concepts/iterative-repair-loops.md)
