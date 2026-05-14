# Wiki Index

Global catalog of all wiki pages. One row per page. Updated by the LLM on every ingest.

To filter by topic in Obsidian, use a Dataview query (see bottom of this file).

| Page | Summary | Tags |
|------|---------|------|
| [Overview](overview.md) | Cross-topic synthesis and relationship map | all |

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

**AI Coding pages**
```dataview
TABLE summary, tags
FROM "wiki"
WHERE contains(tags, "ai-coding")
SORT file.name ASC
```

**Data Engineering pages**
```dataview
TABLE summary, tags
FROM "wiki"
WHERE contains(tags, "data-engineering")
SORT file.name ASC
```

**Cross-topic pages (tagged with 2+ topics)**
```dataview
TABLE summary, tags
FROM "wiki"
WHERE length(filter(tags, (t) => contains(["investing","ai-coding","data-engineering"], t))) > 1
SORT file.name ASC
```
