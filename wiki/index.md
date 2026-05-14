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
