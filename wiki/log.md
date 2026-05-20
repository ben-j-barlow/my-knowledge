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
## [2026-05-19] ingest | investing | Buy TSMC stock as 'recent concerns are overdone' — BofA
## [2026-05-19] ingest | investing | Elon Musk Sees $15 Trillion Optimus Upside — Tesla Investors Could Get A Piece For 'Free'
## [2026-05-19] ingest | investing | HANMI Semiconductor Accelerates U.S. Expansion, Establishes Hanmi USA
## [2026-05-19] ingest | investing | Rocket Lab's Q1 Surge: Revenue Jumps 63% as Neutron Nears First Flight
## [2026-05-19] ingest | investing | Samsung Begins HBM4 Shipments as SK Hynix Lags and Strike Threatens AI Chip Supply
## [2026-05-19] ingest | investing | SK Hynix is about $50bn away from being a trillion-dollar company
## [2026-05-19] ingest | investing | SK Hynix Shares Hit All-Time High as Tech Giants Offer to Co-Finance New Chip Plants
## [2026-05-19] ingest | investing | Why Eos Energy Stock Jumped Over 20% Today (+ IonQ, Nebius bundled)
## [2026-05-19] ingest | data-n-ai | AI Economics Part 2 (@sriramkri) — training vs inference vs agentic inference hardware profiles
## [2026-05-19] ingest | data-n-ai | Apache Arrow as Data Interchange
## [2026-05-19] ingest | data-n-ai | The Modern Data Stack is Overcomplicated: Data Ingestion
## [2026-05-20] ingest | data-n-ai | Halodoc Self-Healing Data Pipelines
## [2026-05-20] ingest | data-n-ai | DuckDB Internals: Why is DuckDB Fast? (Part 1)
## [2026-05-20] ingest | data-n-ai | Lakehouse Statistics and Why Query Engines Get Lost
## [2026-05-20] ingest | data-n-ai | We're Missing Data: The Other Half of AI Transformation (Eric Weber)
## [2026-05-20] ingest | data-n-ai | Why Spark Joins Are Expensive — and What to Do About It
## [2026-05-20] ingest | investing | Treasury Yields Are Testing The AI Equity Rally (Agar Capital)
