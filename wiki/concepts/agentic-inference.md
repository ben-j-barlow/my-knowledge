---
tags: [data-n-ai, concept, agents, ai-infra, llm]
sources: [raw/data-n-ai/articles/AI economics part 2.md]
updated: 2026-05-19
---

# Agentic Inference

A distinct AI workload profile that differs fundamentally from both training and human inference. Characterized by long multi-step tasks, continuous 24/7 operation, heavy memory requirements, and active CPU involvement for external tool calls. No purpose-built hardware exists for it yet — current agentic workloads run on infrastructure designed for human inference.

## The Three Workload Profiles

| Workload | Duration | GPU pattern | HBM role | DRAM role | CPU role |
|---------|---------|------------|---------|---------|---------|
| **Training** | Weeks | Flat, sustained | Constant feed to GPU | Never touched | Spectator |
| **Human inference** | Seconds | Spiky (follows human hours) | Heavy lifting for fast first token | Largely idle | Traffic coordinator |
| **Agentic inference** | Hours | Sustained with CPU-gap interruptions | Hard constraint; overflows to DRAM | Growing store of task history and tool results | Primary player |

## Why Agentic Inference Is the Hardest Workload

It stresses all four hardware components simultaneously in ways training and human inference do not:

- **HBM overflow**: Long context windows and accumulated task history exceed HBM's limited on-chip capacity → spills into off-chip DRAM, which is much slower to access
- **CPU-GPU handoff loop**: Every external tool call (API, internet, file) requires: GPU pauses → CPU parses result, formats back to tokens, writes context to DRAM → CPU hands back to GPU to resume generation. This constant back-and-forth is absent in training and minimal in human inference
- **Scale**: 10–50x more compute per session than human inference
- **Error compounding**: a 2% error rate across 50 tool calls = the task fails most of the time; reliability matters more than speed

## Human vs. Agentic Demand Characteristics

| Dimension | Human | Agentic |
|-----------|-------|---------|
| Timing | Bursty, follows human hours | 24/7, programmable |
| Sessions | Short, one at a time | Long, concurrent |
| Memory span | Minutes | Hours or days |
| Mid-task clarification | Possible | Impossible |
| Error tolerance | High | Near-zero |
| Bottleneck | First-token latency | Reliability, memory, precision |

## Infrastructure Gap

Current GPU clusters were optimized for low-latency, short-context, bursty human prompts. The agentic workload profile — long context, heavy CPU-GPU handoff, HBM spillover to DRAM, sustained compute — is fundamentally different and requires:

- Larger effective memory bandwidth (hence the second HBM supercycle)
- Better CPU-GPU memory coherence (CXL 3.0 is the most promising fix; ~2028–2029 at scale)
- Different chip architectures than inference-optimized chips like Groq or AWS Inferentia (which are optimized for short-context high-concurrency, not long-running sessions)

## GPU Utilization Pattern

Training: flat `────────`  
Human inference: spiky `───╭──╮───` (peaks 9am, dips 3am)  
Agentic inference: sustained but interrupted `──╌──╌──╌──` (gaps = CPU tool-call time)

The human inference pattern creates significant idle GPU capacity (off-peak hours), which cloud providers are trying to fill with spot pricing and reallocation.

## Connection to HBM Supercycles

Training caused the **first HBM supercycle** in 2023–2024. Agentic inference, with its appetite for long context that overflows HBM into DRAM, is driving the **second** — independent of training scaling.

## See Also

- [HBM](hbm.md)
- [AI Semiconductor Supply Chain](ai-semiconductor-supply-chain.md)
- [Iterative Repair Loops](iterative-repair-loops.md)
- [Source: AI Economics Part 2](../sources/ai-economics-part2.md)
