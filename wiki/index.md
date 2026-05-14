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
