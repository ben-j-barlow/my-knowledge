# Operations Log

Append-only chronological record of all ingests, queries, and lint passes.

Each entry format: `## [YYYY-MM-DD] <operation> | <topic(s)> | <title>`

Useful greps:
```bash
grep "^## \[" wiki/log.md | tail -10           # last 10 operations
grep "^## \[" wiki/log.md | grep "investing"    # all investing operations
grep "^## \[" wiki/log.md | grep "ingest"       # all ingests
```

---

## [2026-05-14] init | all | Knowledge base initialized
## [2026-05-14] ingest | data-n-ai | AI for the Real World: A Conversation with Yann LeCun
## [2026-05-14] ingest | data-n-ai | Build Iterative Repair Loops with Codex
