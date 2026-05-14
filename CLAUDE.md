# Knowledge Base Schema

This is the operating manual for this repository. Read it at the start of every session. Update it whenever a new convention is established so future sessions can pick up without re-explanation.

---

## Purpose

A personal knowledge base covering three research topics:

- **Investing** — valuation frameworks, macro, equity research, notable investors, books, datasets
- **Data & AI** — LLM APIs, coding agents, prompt engineering, benchmarks, data pipelines, orchestration, storage, streaming, transformation, MLOps

These topics overlap deliberately. A page on quant strategies using ML belongs to both `investing` and `data-n-ai`. Cross-topic synthesis is a feature, not a problem.

---

## Architecture

Three layers:

1. **Raw sources** (`raw/`) — immutable source documents. LLM reads from here, never writes. Organized by topic subdirectory.
2. **Wiki** (`wiki/`) — LLM-owned markdown. All topics coexist here, filtered via YAML frontmatter tags. You (the human) read this; the LLM writes and maintains it.
3. **Schema** (this file) — the operating manual. Co-evolved over time. Update it when conventions change.

---

## Directory Layout

```
raw/
  investing/articles/     # Web clips, blog posts  (YYYY-MM-DD-slug.md)
  investing/papers/       # Research papers, notes
  investing/assets/       # Downloaded images referenced by raw docs
  data-n-ai/...

wiki/
  index.md                # Global catalog — one row per page, with tags
  log.md                  # Append-only operations log
  overview.md             # Cross-topic synthesis and relationship map
  concepts/               # Ideas, techniques, frameworks
  entities/               # People, companies, tools, funds, models
  sources/                # One summary page per raw source

outputs/
  investing/              # Q&A answers, slides, charts
  data-n-ai/
```

---

## Tag Conventions

Every wiki page has YAML frontmatter. Tags fall into three categories.

### Topic tags (≥1 required)
- `investing`
- `data-n-ai`

Assign all that apply. Cross-topic pages are encouraged.

### Type tags (exactly 1 required)
- `concept` — an idea, technique, or framework
- `entity` — a person, company, tool, fund, or model
- `source` — summary of a raw source document
- `synthesis` — a filed query answer or analysis

### Subtopic tags (optional, grow organically)
Add freely as the wiki grows. Examples: `valuation`, `llm`, `rag`, `agents`, `etl`, `pipelines`, `streaming`, `macro`, `equities`, `benchmarks`, `prompt-engineering`

### Example frontmatter
```yaml
---
tags: [data-n-ai, concept, rag, vector-databases]
sources: [raw/data-n-ai/articles/2026-05-01-rag-overview.md]
updated: 2026-05-14
---
```

---

## Raw Source Conventions

- Place files in `raw/<topic>/<articles|papers|assets>/`
- **Naming**: `YYYY-MM-DD-slug.md` for dated content (articles, reports); `slug.md` for timeless reference (books, tool docs)
- **Immutable**: never edit a raw file after creation. It is the ground truth.
- **Images**: downloaded to `raw/<topic>/assets/`. Reference them in the raw doc with a relative path (`../assets/image.png`). The LLM reads images by viewing them separately after reading the text.

---

## Wiki Conventions

- Every page must have YAML frontmatter with topic tag(s), exactly one type tag, and a `sources` list
- Use **relative markdown links** for internal links — not Obsidian wikilinks — for git compatibility: `[DCF Analysis](../concepts/dcf-analysis.md)`
- Before creating a new page, check `wiki/index.md` to avoid duplicates
- When updating an existing cross-topic page with a new source from a different topic, add that topic tag to its frontmatter
- The `updated` field in frontmatter should reflect the date of the last substantive change

---

## Ingest Workflow

Run when a new source is added to `raw/`. Work through one source at a time; stay interactive.

1. **Read** the source in full
2. **Discuss** key takeaways with the user — what to emphasize, what depth to go into, what to skip
3. **Create** `wiki/sources/<slug>.md` — summary, key claims, notable quotes, metadata, correct tags
4. **Update or create** relevant `wiki/concepts/` and `wiki/entities/` pages
   - Check `wiki/index.md` first — never create a duplicate page
   - When updating an existing page, add the new topic tag if not already present
5. **Update** `wiki/index.md` — add or update one row per touched page (page link, one-line summary, tags)
6. **Update** `wiki/overview.md` if the source shifts the big picture or surfaces a meaningful cross-topic connection
7. **Append** to `wiki/log.md`:
   ```
   ## [YYYY-MM-DD] ingest | <topic> | <Source Title>
   ```
8. One source routinely touches 10–15 wiki pages. That is expected and correct.

---

## Query Workflow

Run when asked a question against the knowledge base.

1. Read `wiki/index.md` in full; if the query is topic-scoped, filter rows by the relevant topic tag(s)
2. Read the relevant wiki pages in full
3. If more depth is needed, read the relevant raw sources
4. Synthesize an answer; write it to `outputs/<topic>/YYYY-MM-DD-<slug>.md`
5. If the answer is valuable (comparison, analysis, newly surfaced connection), **file it back into the wiki** as a `synthesis`-tagged page and add it to `wiki/index.md`
6. Append to `wiki/log.md`:
   ```
   ## [YYYY-MM-DD] query | <topic(s)> | <question>
   ```

---

## Lint Workflow

Run periodically to maintain wiki health.

Scan for:
- Pages missing topic or type tags
- Contradictions between pages (especially on cross-topic concepts)
- Stale claims superseded by newer sources
- Orphan pages (no inbound links from other wiki pages)
- Concepts mentioned on ≥2 pages that lack their own concept page
- Missing cross-references between obviously related pages
- Data gaps that a web search could fill

Write findings to `outputs/<most-relevant-topic>/YYYY-MM-DD-health-check.md`.

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] lint | all | health-check
```

---

## Output Formats

| Format | How |
|--------|-----|
| Markdown report | Default. Write to `outputs/<topic>/YYYY-MM-DD-<slug>.md` |
| Slide deck | Marp format — add `marp: true` to the YAML frontmatter |
| Chart | Write a self-contained matplotlib Python script to `outputs/<topic>/`; user runs it |
| Dataview table | Write a fenced `dataview` code block in a markdown file; renders in Obsidian |

Valuable outputs (analyses, comparisons, synthesized connections) should be filed back into `wiki/` as `synthesis`-tagged pages.

---

## Log Format

Each entry in `wiki/log.md` starts with a consistent prefix for easy grepping:

```
## [YYYY-MM-DD] ingest | investing | Buffett 2024 Annual Letter
## [YYYY-MM-DD] query | data-n-ai | How do RAG pipelines work at scale?
## [YYYY-MM-DD] lint | all | health-check
```

Useful greps:
```bash
grep "^## \[" wiki/log.md | tail -10          # last 10 operations
grep "^## \[" wiki/log.md | grep "investing"   # all investing operations
grep "^## \[" wiki/log.md | grep "ingest"      # all ingests
```

---

## Schema Evolution

This file is a living document. Update it when:
- A new tag convention is established
- A workflow step is added, removed, or reordered
- A new output format is adopted
- A naming convention changes

The goal: any future Claude Code session opens this file and operates correctly with no additional explanation from the user.
