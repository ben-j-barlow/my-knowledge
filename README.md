# my-knowledge

A personal knowledge base covering **Investing**, **AI Coding**, and **Data Engineering** — built on the LLM wiki pattern.

Raw sources are immutable. The LLM writes and maintains the wiki. You read; the LLM bookkeeps.

## Quick start

```bash
# Ingest a web article
python scripts/ingest_url.py <url> investing

# Get the prompt to compile it into the wiki
./scripts/compile.sh investing 2026-05-14-article-slug.md

# Ask a question
./scripts/qa.sh "What valuation frameworks are in the wiki?" investing

# Health check
./scripts/health_check.sh
```

## Structure

```
raw/        # Source documents — immutable, organized by topic
wiki/       # LLM-maintained wiki — concepts, entities, sources, synthesis
outputs/    # Generated Q&A answers, slides, charts
scripts/    # Helper scripts for ingestion and prompting
CLAUDE.md   # Operating manual for the LLM
```

Open this directory as an Obsidian vault. See `.obsidian/plugins/README.md` for recommended plugins.

See `CLAUDE.md` for the full schema and workflow documentation.
