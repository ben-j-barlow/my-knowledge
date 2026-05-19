---
title: "AI economics part 2"
source: "https://x.com/sriramkri/status/2054594308494229882?utm_source=tldrai"
author:
  - "[[@sriramkri]]"
published: 2026-05-14
created: 2026-05-19
description: "My AI economics and Rationed posts covered how AI labs have ongoing battles for GPU resources.This goes deeper into demand (inference) and s..."
tags:
  - "clippings"
---
![Image](https://pbs.twimg.com/media/HINil8jXwAA3p9z?format=jpg&name=large)

My [AI economics](https://open.substack.com/pub/sriramkrishnan/p/ai-economics?r=6rjl&utm_campaign=post-expanded-share&utm_medium=web) and [Rationed](https://sriramkrishnan.substack.com/p/rationed) posts covered how AI labs have ongoing battles for GPU resources.

This goes deeper into demand (inference) and supply (training, inference, hardware) and how I think infrastructure powering AI today may not be sufficient.

My last AI economics post was my most shared post. Thank you! Sorry I wasn’t able to respond to all the notes.

**AI demand**

Human usage is bursty and unpredictable - short prompts, random timing, one session at a time. Peaks at 9am Monday, dead at 3am Sunday. We forgive errors and lose patience when it's slow.

Agents are the opposite - continuous, programmable, 24/7. Long multistep tasks, concurrent sessions, memory spanning hours or days. Agents can't ask for clarification mid-task. Errors compound fast, a 2% error rate across 50 tool calls means the job fails most of the time.

Humans care about speed. Agents care about reliability, precision, and memory.

These different usage patterns among agents and humans have implications for how supply is utilized.

**AI supply - training and inference**

The workloads for training and inference are very different.

**Training:** Training is one massive, uninterrupted computation job. The entire internet’s worth of data fed into the model, billions of parameters adjusted across thousands of GPUs simultaneously, repeated millions of times until error rates are low enough to ship. Runs for weeks and doesn’t stop.

The bottleneck is communication between GPUs. Every GPU handles a slice of work and all of them must sync before the next step. The whole cluster moves at the speed of the slowest chip.

**Inference:** Inference is the process of the model generating a response to a prompt. It’s every output, whether a one word answer or a 126 step agent task, that consumes compute that costs money and competes for the same finite pool of GPUs

- Human inference is spiky. The hardware sits idle at 3am, gets slammed at 9am. You provision for the peak and this means GPU underutilization.
- Agentic inference is a different problem. Fewer concurrent requests but each one runs for hours and consumes 10-50x more compute than a human session. Doesn't care about the clock. Utilization is high and sustained and the memory requirements are far more demanding

Training is a one-time brute-force job. Human inference is shallow and spiky. Agentic inference is continuous, memory hungry and the hardest of the three.

Until now the supply stack has been built and optimized for low latency, short context, bursty human prompts and not for inference for agentic usage.

**AI supply - hardware**

How a chip handles training and inference comes down to four components: two types of processors and two types of memory.

Four components matter: CPUs, GPUs, HBM, DRAM.

- **CPUs are sequential generalists** and handle decision-making, routing, memory access, external/internet connections. Fast but does one thing at a time
- **GPUs are parallel math machines.** They take numbers in, run billions of matrix calculations simultaneously, return numbers out. No access to the outside world and they only know math
- **HBM (High Bandwidth Memory)** lives on the chip. Extremely fast but extremely limited in memory capacity. Expensive to manufacture. You can only bond so much to a GPU before you run out of physical space
- **DRAM (Dynamic Random Access Memory)** sits off chip. Massive storage but slow to access. Cheap to scale up but painful to retrieve from.

How these four interact depends on the workload:

- **Training:** One time, long, continuous event with GPUs and HBMs dominating A single, uninterrupted, brute force, weeks-long computation heavy maths job where thousands of GPUs crunch billions of parameters in parallel. The HBM must continuously feed these to the GPUs at high speed. A slow HBM means GPUs sit idle and run at half capacity. The entire cluster moves at the speed of the slowest chip - one lagging GPU stalls every other GPU waiting to sync. The CPUs are spectators because no decisions are made mid-run, no external tools are called, no routing logic is required for the CPU and because the training loop runs entirely within the GPU and HBM, the DRAM never gets touched too
- **Human inference**: High volume but shallow with HBMs doing the heavy lifting Millions of short requests are hitting the cluster simultaneously, each one generating a few hundred tokens and disappearing. HBM does the critical work of loading the model fast enough to return the first token before the user loses patience. DRAM and CPU are largely idle as sessions are too short to spill out of HBM and into the DRAM and the CPU does little more than route requests in from users to GPUs and routes the responses out like a traffic coordinator
- **Agentic inference:** The hardest of the three, stressing all components like CPUs, HBMs, DRAMs, GPUs simultaneously A different problem entirely with fewer concurrent requests but each request is a long, sustained job consuming 10-50x more compute than a human session. HBM becomes the hard constraint because longer context windows and task history overflow its low capacity forcing spillover into DRAM which holds the growing pile of tasks, tool results and intermediate outputs. Unlike training and human inference, the CPU is a primary player as every time the agent calls an external tool or API or connects to the internet, the GPU hands off to the CPU for the the CPUs to parse tool results, to format them back into tokens and to manage what gets written to DRAM before handing back to the GPU to continue generating That constant back-and-forth between GPUs/CPUs and HBM/DRAM makes agentic inference the most demanding workload across every component simultaneously

In practice the lines between agent and human inference them blur. If humans use the models to do web searches, calls to third party APIs or pull documents mid-conversation, the CPU becomes active, tool calls happen, DRAM starts filling up with context.

All three workloads have different GPU utilization rates:

- **Training:** Flat and sustained blue line
- **Human inference:** Red line that follows human behavior, peaks during work hours, drops at night and weekends
- **Agentic inference:** Green middle line, kind of continuous but interrupted every time the CPU takes over for a tool call, leaving the GPU momentarily idle

![Image](https://pbs.twimg.com/media/HINijV4WoAIriQn?format=jpg&name=large)

**Conclusion**

**Training**: Scaling GPUs doesn't scale compute linearly. Efficiency matters more than raw scale these days given finite supply

- Inter-chip communication overhead grows with every chip added impacting compute gains
- The focus is on how to train a frontier models with less compute, fewer passes, smarter data selection
- Ecosystem around GPUs becomes more critical, eg how GPUs are networked together, how software can be written to instruct GPUs etc
- NVIDIA’s moat isn’t just the GPU but the networking (NVLink) and software (CUDA). No one has matched all three yet

**Human inference**’s low GPU utilization is a huge opportunity cost

- Idle GPUs between 3am and 9am could be training new models, serving higher-margin products or running older models for cheaper
- Using an NVIDIAs for short human conversations is like using a Ferrari to wheel your groceries
- There’s an opening for inference-specific chips optimized for short context and high concurrency (eg Groq and AWS Inferentia)
- Cloud providers are experimenting with spot pricing and dynamic reallocation to fill idle capacity but it's still early

**Agentic inference** silicon is wide open

- The workload profile with long context, heavy CPU-GPU handoff, HBM spillover to DRAM, sustained compute etc is fundamentally different from what today’s chips are optimized for
- No purpose-built infrastructure yet as current agentic workloads run on hardware designed for humans

**HBMs** are the chokepoint:

- SK Hynix, Samsung, and Micron dominate because HBM capacity is very hard to build as you can only bond so much memory to a chip before you run out of space
- Training caused the first HBM supercycle. Agentic AI with its appetite for context is causing the second
- No credible new entrant exists thus far because HBM fabs require decades of investment and specialized packaging that TSMC currently dominates
- CXL 3.0 is the most promising near-term fix as it allows CPU and GPU to share a unified memory pool directly, eliminating the highway (PCIe) but commercial deployment at scale is still 2-3 years out

![Image](https://pbs.twimg.com/media/HINigtzWsAIFZXH?format=jpg&name=large)