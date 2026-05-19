# Wiki Index

Global catalog of all wiki pages. One row per page. Updated by the LLM on every ingest.

To filter by topic in Obsidian, use a Dataview query (see bottom of this file).

| Page | Summary | Tags |
|------|---------|------|
| [Overview](overview.md) | Cross-topic synthesis and relationship map | all |
| [World Models](concepts/world-models.md) | Systems that predict world state rather than tokens; the proposed alternative to LLMs for agentic tasks | data-n-ai, concept, world-models |
| [LLM Limitations](concepts/llm-limitations.md) | Structural limits of LLMs — no world model, language bias, chain-of-thought as workaround | data-n-ai, concept, llm |
| [Robotics](concepts/robotics.md) | VLA models and world-model alternatives for physical robot systems | data-n-ai, concept, robotics |
| [Yann LeCun](entities/yann-lecun.md) | Meta Chief AI Scientist; JEPA architect; founder of AMI Labs; leading critic of LLM path to AGI | data-n-ai, entity |
| [AMI Labs](entities/ami-labs.md) | LeCun's company building JEPA world models for industrial and physical-world AI | data-n-ai, entity |
| [Source: AI for the Real World](sources/yann-lecun-ai-real-world.md) | LeCun interview: LLMs as dead-end, world models as alternative, AMI Labs thesis | data-n-ai, source |
| [Iterative Repair Loops](concepts/iterative-repair-loops.md) | Closed-loop agent pattern: review → repair → validate, with structured handoffs and stop conditions | data-n-ai, concept, agents |
| [Codex](entities/codex.md) | OpenAI's agentic coding CLI; supports headless/programmatic use with structured JSON output schemas | data-n-ai, entity, agents |
| [OpenAI](entities/openai.md) | Creator of GPT models, Codex, Responses API, and Evals API | data-n-ai, entity |
| [Source: Build Iterative Repair Loops with Codex](sources/codex-iterative-repair-loops.md) | OpenAI Cookbook: 3-phase closed-loop repair agent with structured handoffs and per-iteration audit trail | data-n-ai, source, agents |
| [HBM](concepts/hbm.md) | High Bandwidth Memory: stacked DRAM for AI accelerators; supply dynamics, generations HBM3E→HBM4E, market structure | investing, data-n-ai, concept, hbm |
| [Advanced Packaging](concepts/advanced-packaging.md) | CoWoS, SoIC, TC bonders, hybrid bonding — the integration techniques placing memory next to logic in AI chips | investing, data-n-ai, concept, advanced-packaging |
| [AI Semiconductor Supply Chain](concepts/ai-semiconductor-supply-chain.md) | Physical stack powering AI compute: HBM → logic die → advanced packaging → EUV; concentration risks and hyperscaler co-investment | investing, data-n-ai, concept, ai-infra |
| [TSMC](entities/tsmc.md) | World's dominant contract foundry; leading at 3nm/N2; CoWoS >98% yield; ≥10x capacity vs. nearest competitor at advanced nodes | investing, entity, foundry |
| [SK Hynix](entities/sk-hynix.md) | World's largest HBM supplier; ~57% market share; ~$948B market cap (May 2026); 2026 supply sold out; supplies ~2/3 of Nvidia Vera Rubin HBM4 | investing, data-n-ai, entity, hbm |
| [Samsung Electronics](entities/samsung-electronics.md) | South Korean conglomerate; ~40% global DRAM share; first to ship HBM4 (Feb 2026); crossed $1T market cap May 6; 50k+ worker strike threatened May 21 | investing, data-n-ai, entity, hbm |
| [HANMI Semiconductor](entities/hanmi-semiconductor.md) | South Korean semiconductor equipment firm; #1 global TC bonder market share; establishing Hanmi USA in San Jose 2026 | investing, entity, advanced-packaging |
| [Rocket Lab](entities/rocket-lab.md) | US aerospace; Electron operational, Neutron nearing first flight; Q1 2026 revenue +63% to $200M; vertically integrating via acquisitions | investing, entity, space |
| [Tesla](entities/tesla.md) | EV/AV/robotics platform; Piper Sandler SOTP: ~$400/share ex-Optimus; Musk: "80% of Tesla's value will be Optimus" | investing, data-n-ai, entity, ev, robotics |
| [Eos Energy](entities/eos-energy.md) | Zinc-based BESS company; Q1 2026 revenue +445%; Cerberus Capital $100M partnership → bankability milestone | investing, entity, energy-storage |
| [IonQ](entities/ionq.md) | Trapped-ion quantum computing; 2026 guidance $260–270M revenue, >100% organic growth; trades at ~72x sales | investing, entity, quantum-computing |
| [Nebius Group](entities/nebius-group.md) | AI cloud infrastructure; Q1 AI cloud revenue +841% YoY; 4 GW+ contracted data center power for 2026; broke ground on US gigawatt-scale AI factory | investing, data-n-ai, entity, ai-infra |
| [Source: BofA Buy TSMC May 2026](sources/tsmc-bofa-buy-may2026.md) | BofA reiterates Buy on TSMC; N2 2 quarters ahead of schedule; competitors at 1/8 TSMC capacity at 3nm | investing, source, semiconductors |
| [Source: Tesla Optimus Piper Sandler](sources/tesla-optimus-piper-sandler.md) | Piper Sandler SOTP assigns ~$400/share to 17 non-Optimus Tesla lines; Optimus treated as free optionality | investing, source, robotics |
| [Source: Hanmi USA Expansion](sources/hanmi-usa-expansion.md) | HANMI establishing San Jose subsidiary; HBM4 ramp driving TC bonder order concentration in Q2 2026 | investing, source, advanced-packaging |
| [Source: Rocket Lab Q1 2026](sources/rocket-lab-q1-2026.md) | Rocket Lab Q1 revenue $200M +63%; Q2 guidance 12% above consensus; record backlog; Neutron nearing first flight | investing, source, space |
| [Source: Samsung HBM4 + Strike](sources/samsung-hbm4-shipments-strike.md) | Samsung first to ship HBM4; 50k+ worker strike May 21–June 7; DRAM prices +90% Q1; worst shortage in 15 years | investing, data-n-ai, source, hbm |
| [Source: SK Hynix Near $1T](sources/sk-hynix-near-trillion.md) | SK Hynix ~$948B market cap, 9x in 2 years; "structural counterparty to AI"; memory bandwidth = binding constraint for inference | investing, data-n-ai, source, hbm |
| [Source: SK Hynix ATH + Co-Financing](sources/sk-hynix-cofinancing.md) | Microsoft/Google/Amazon offering to co-finance ASML EUV machines at SK Hynix; Q1 operating margin 72%; M15X timeline pulled forward | investing, data-n-ai, source, hbm |
| [Source: Eos Energy Q1 2026](sources/eos-energy-q1-2026.md) | Eos Energy Q1 revenue +445%; Cerberus Capital JV with $100M and 2 GWh supply deal — bankability milestone | investing, source, energy-storage |
| [Agentic Inference](concepts/agentic-inference.md) | Distinct workload profile: long context overflows HBM into DRAM, CPU active for every tool call, 10–50x compute vs human sessions; no purpose-built hardware yet | data-n-ai, concept, agents, ai-infra |
| [Event-Driven Architecture](concepts/event-driven-architecture.md) | Decoupled producers/consumers via durable event logs; topics, partitions, consumer groups, schema registry, DLQ; when to use (and when not to) | data-n-ai, concept, streaming, etl |
| [Data Ingestion](concepts/data-ingestion.md) | Three approaches: managed connectors, event streaming, custom pipelines; tradeoffs, hidden costs, decision framework | data-n-ai, concept, etl, pipelines |
| [Kafka](entities/kafka.md) | Apache Kafka: dominant open-source event streaming platform; durable partitioned log; self-hosted is a full-time job — Confluent is almost always the right call | data-n-ai, entity, streaming |
| [Confluent](entities/confluent.md) | Managed Kafka (Confluent Cloud) plus Schema Registry; throughput-based pricing; founded by Kafka's original creators | data-n-ai, entity, streaming |
| [Apache Arrow](entities/apache-arrow.md) | Zero-copy in-memory columnar interchange layer; embedded in DuckDB, Polars, Spark, Snowflake; Arrow IPC, Flight, ADBC | data-n-ai, entity, etl |
| [Fivetran](entities/fivetran.md) | Polished managed connector service; row-based pricing; "set it and forget it" for standard SaaS sources | data-n-ai, entity, etl |
| [Airbyte](entities/airbyte.md) | Open-source managed connectors; self-hosted or Airbyte Cloud; cheaper than Fivetran, variable quality on marketplace connectors | data-n-ai, entity, etl |
| [Source: AI Economics Part 2](sources/ai-economics-part2.md) | Training vs human inference vs agentic inference hardware profiles; second HBM supercycle; CXL 3.0; Nvidia moat (GPU + NVLink + CUDA) | data-n-ai, source, agents, hbm |
| [Source: Apache Arrow as Data Interchange](sources/apache-arrow-data-interchange.md) | Arrow as zero-copy interchange layer beneath DuckDB, Polars, Spark; eliminates serialization cost at every pipeline hop | data-n-ai, source, etl |
| [Source: Modern Data Stack — Data Ingestion](sources/modern-data-stack-ingestion.md) | Three ingestion approaches; Fivetran vs Airbyte; when to use Kafka; hidden costs; decision framework | data-n-ai, source, etl, streaming |

---

## Dataview Queries

Filter by topic (requires Obsidian Dataview plugin):

**Investing pages**
```dataview
TABLE summary, tags
FROM "wiki"
WHERE contains(tags, "investing")
SORT file.name ASC
```

**Data & AI pages**
```dataview
TABLE summary, tags
FROM "wiki"
WHERE contains(tags, "data-n-ai")
SORT file.name ASC
```

**Cross-topic pages (tagged with both topics)**
```dataview
TABLE summary, tags
FROM "wiki"
WHERE contains(tags, "investing") AND contains(tags, "data-n-ai")
SORT file.name ASC
```
