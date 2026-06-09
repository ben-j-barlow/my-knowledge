---
tags: [investing, data-n-ai, synthesis]
updated: 2026-06-05
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

**Macro / rates risk to AI equities:** The 30-year Treasury crossed 5% and the 10-year is at ~4.6% as of May 2026, compressing the equity risk premium for the S&P 500 to near zero and into negative territory for the Nasdaq 100 and Mag 7. AI and semiconductor stocks are disproportionately exposed because they are the longest-duration equities in the market — most of their value is in projected future cash flows, making them mechanically sensitive to discount rate increases even when fundamentals remain strong. The SOX is at 25x projected earnings vs. a 10-year average of ~19x. The Trump-Xi summit (May 2026) failed to resolve any structural issue (Taiwan, rare earths, semiconductor export controls, Hormuz/Iran) — geopolitical risk premium persists.

Subtopics tracked: `semiconductors`, `hbm`, `foundry`, `advanced-packaging`, `equities`, `ev`, `robotics`, `space`, `energy-storage`, `quantum-computing`, `ai-infra`, `macro`, `geopolitics`, `valuation`

### Data & AI

Current coverage spans two threads:

**LLM limitations and world models:** LLMs are commercially valuable but architecturally incapable of predicting action consequences — which Yann LeCun argues disqualifies them for general intelligence. World models (JEPA) are the proposed alternative, learning abstract state representations enabling planning and embodiment.

**Agentic patterns:** Iterative repair loops work well when acceptance criteria are stable and verifiable. Two newer patterns address the cases they don't cover: the **Ralph Loop** (bash loop that gates on external tests — the agent cannot self-declare done) handles premature task abandonment; **human-in-the-loop at the direction level** handles tasks where the evaluation criteria evolve (qualitative analysis, exploratory research, strategy). The key finding from the qualitative analysis experiments: memo/direction feedback (tell the agent where to steer) outperforms artifact-level code review both in efficiency and in the quality of the resulting analysis. Independent multi-agent coding followed by one round of human reconciliation feedback is the strongest setup found so far.

**Agentic inference as a distinct workload:** Agentic AI stresses all four hardware components simultaneously (CPU, GPU, HBM, DRAM) in ways neither training nor human inference do. Long context overflows HBM into DRAM; every tool call creates a CPU-GPU-DRAM handoff cycle; sessions run 10–50x longer than human inference. No purpose-built hardware exists yet — this is driving the second HBM supercycle.

**Data pipelines and ingestion:** Three ingestion approaches covered — managed connectors (Fivetran, Airbyte), event streaming (Kafka, Confluent), and custom pipelines. Core tension: operational simplicity vs. latency requirements vs. team size. Most teams over-engineer for latency they don't need. Apache Arrow is the emerging zero-copy interchange standard adopted beneath DuckDB, Polars, Spark, and Snowflake.

**Query engines and lakehouse statistics:** DuckDB is the dominant single-node analytical engine — in-process, no server, 33-pass optimizer, zone maps. Apache Spark remains the distributed standard; Databricks Photon is consistently 2–20x faster than vanilla Spark for join-heavy workloads. The structural problem in lakehouses: statistical metadata is optional in both Iceberg and Delta Lake and frequently absent — query planners fall back to guesses, producing wrong join orders, memory spilling, and queries that never complete. FloeDB (Floecat) is attempting to fix this at the open-source layer.

**Data layout — clustering replacing partitioning:** The physical organisation of files is the biggest lever on scan cost, because pruning on Delta/Iceberg is always file-level against transaction-log min/max stats (there is no directory-pruning shortcut, even with partitioning). Hive-style partitioning, the 15-year standard, forces an irreversible table-creation-time choice and over-partitions/creates small files in >75% of cases. Databricks Liquid Clustering reframes layout as a hint the engine uses (keys changeable anytime, or auto-selected from query patterns), claiming no small-file problem, multi-dimensional clustering, row-level concurrency, and benefit to any reader since it's a write-side optimisation writing standard Parquet+stats. Reported migrations: 5.9–7.7x query speedups and ~27% storage reduction. The theme connects to lakehouse statistics (layout quality = clustering quality = narrow per-file ranges) and to the agentic-data theme: layout should become an automated implementation detail because agents generate query patterns faster than humans can re-partition.

**Self-healing pipelines:** Six-layer pattern (Halodoc case study) for autonomous recovery without manual intervention: CDC auto-recovery, source-vs-lake consistency, mini-batch processing, smart memory scaling, warehouse lock management, cascading dependency recovery. Design principle: alert first, act second; fix foundation before downstream.

**AI org operating model:** Eric Weber's two-stack model — technical stack (well-funded, gets budget) × operating stack (drifts, nobody funds it). They multiply, not add. Three emerging IC job shapes: AI output curators, algorithm/primitive writers, end-to-end orchestrators. Manager-as-router model dissolving; manager-as-coach replacing it. Chris Riccomini's complementary thesis: "data engineer" as a distinct title will dissolve into a unified data role covering DE + ML + analytics.

**AI and data engineering workflows:** Chris Riccomini's practitioner framework: (1) plan mode all the time — never flip to implementation without iteratively probing the plan to exhaustion; (2) Ralph Loop for autonomous execution — external test gates, not the agent, decide when work is done; (3) quality gates — define, measure, enforce; (4) Substrait over SQL for LLM-generated queries — physical + logical operators, fewer tokens, client-side optimization; (5) incremental loads over full batch loads to scope non-determinism risk. Language choice is shifting to agent ergonomics: smallest, cheapest LLM output wins over human ergonomic preferences.

**Context engineering and AGENTS.md:** The discipline of deciding what enters an agent's context window. Two converging empirical studies (Augment Code's AuggieBench; ETH Zurich, arXiv:2602.11988): a good `AGENTS.md` can equal a model upgrade (Haiku→Opus), but a bad one is worse than none — and **auto-generated context files reduce success rates while raising cost ~20%**, because they duplicate docs the agent already reads. Human-curated files help ~4 points. The governing rule is *write only the non-inferable* (custom commands, specific tooling, counterintuitive patterns) and keep files ~100–150 lines via progressive disclosure. Failure modes are all forms of context rot: overexploration (too much architecture / too many bare "don'ts"), bloat, and silent drift. `AGENTS.md` matters because it's the only doc location with reliable discovery (100% vs <10% for orphan `_docs/`). Prompt caching is the primary cost mitigation. This is the applied edge of the same theme as the Ralph Loop and human-in-the-loop work: encode direction and constraints up front, don't bury the agent in reference material.

**Agentic analytics — context over codegen:** Anthropic's own DS/DE team automates 95% of business analytics queries at ~95% accuracy with Claude, and the write-up is the most concrete production account in the wiki. The thesis ties directly into the context-engineering thread: **analytics accuracy is a context and verification problem, not a code-generation one** — unlike coding (open-ended, tests as guardrails), analytics has one correct answer with no deterministic proof, so the whole game is mapping a question to the right entity. Three failure modes (concept↔entity ambiguity, staleness, retrieval failure) are attacked by a four-layer stack: canonical **data foundations** → a governed **semantic layer**/sources of truth → **Claude Skills** (on-demand procedural markdown) → **validation** (offline evals + ablation + online adversarial review). Two findings generalize beyond analytics: (1) a **null-result ablation** — grep access to thousands of prior SQL files moved accuracy <1 point even though the answer was present 80% of the time — proves the bottleneck is *structure, not access*, reproducing the ETH Zurich AGENTS.md result on a new surface; (2) **auto-generating the semantic layer was net-negative**, so they generate *docs* with the LLM but humans own the *definitions*. Skills were the single biggest lever (21%→95%), and the doc-drift problem that AGENTS.md leaves "unsolved" they partly solved with repo colocation + a CI hook that fails any model PR not touching its skill. The provenance footer (source tier / freshness / owner) is their main defense against the silent-failure mode.

**Agents as parallel research machines:** A recurring 2026 orchestration shape — decompose a task into independent sub-questions and run them as parallel sub-agents, then reconcile. Seen in Augment's Intent (coordinator → parallel implementors → verifier), the qualitative-analysis multi-coder setup, and the Kimi 2.6 Agent Swarm (claimed 300 sub-agents / 1,500 tool calls / 4.5× faster) applied to Polymarket weather-market trading. The trading case is also a clean cross-topic example: the edge is reacting to public-data revisions before the market reprices, where reading the *resolution rules* (observed Wunderground station data, whole degrees, no post-finalization revisions) matters more than forecasting.

Subtopics being tracked: `llm`, `world-models`, `robotics`, `agents`, `ai-infra`, `etl`, `pipelines`, `streaming`, `query-optimization`, `lakehouse`, `prompt-engineering`, `prediction-markets`

---

## Cross-Topic Connections

*Populated by the LLM as connections emerge.*

| Connection | Topics | Notes |
|-----------|--------|-------|
| HBM supply constraint = AI inference bottleneck | investing + data-n-ai | Memory bandwidth is the binding constraint for LLM inference at scale. The investment case for SK Hynix/Samsung is the same phenomenon LeCun's world-model critique points at from the other side: LLM-style compute scaling hits physical limits. |
| Hyperscaler capex → semiconductor supply chain | investing + data-n-ai | Big Tech's $725B 2026 capex must exit through HBM, CoWoS, and EUV. The AI infrastructure buildout (data-n-ai) is the demand signal for the semiconductor supply chain investment thesis (investing). |
| Nebius Group as AI cloud infrastructure play | investing + data-n-ai | GPU cluster operators like Nebius are the customers of the HBM/TSMC stack and the infrastructure layer below LLM APIs. |
| Tesla Optimus + inference-as-a-service | investing + data-n-ai | Piper Sandler labels Optimus and "inference-as-a-service" as thesis-defining for Tesla — connecting robotics/embodied AI (data-n-ai) to equity valuation (investing). |
| Agentic inference → second HBM supercycle | investing + data-n-ai | The agentic inference workload profile (long context, HBM overflow, sustained compute) is driving a second HBM demand wave independent of training scaling. The HBM shortage thesis (investing: SK Hynix, Samsung) is partly grounded in the same workload shift that drives agentic AI infrastructure investment. |
| Kafka / EDA in data pipelines → AI inference infrastructure | data-n-ai | Event-driven architectures feed operational data into the warehouses and vector stores that LLM applications query at inference time. The data ingestion layer (Kafka, Fivetran) is the upstream supply chain for the AI feature store and RAG pipeline. |
| AI infrastructure enthusiasm → equity duration risk | investing + data-n-ai | The AI infrastructure buildout (data-n-ai) is the demand signal for semiconductor capex (investing), but the same enthusiasm has pushed AI equities into long-duration territory — most of their value is in future AI-driven cash flows. Rising Treasury yields compress these valuations mechanically, independent of whether AI execution delivers. The better the AI story, the longer the duration, and the more exposed to rate moves. |
| Agent swarms → prediction-market trading edge | investing + data-n-ai | Parallel agent orchestration (data-n-ai) turns free public data into a trading edge (investing): in Polymarket weather markets the inefficiency is the lag between a forecast revision and the market repricing. The moat is execution speed/workflow, not data access — the same "agents as parallel research machines" pattern, applied to a market instead of a codebase. |

---

## Open Questions

*Questions surfaced during ingestion or Q&A that warrant further investigation.*

- (none yet)
