---
tags: [data-n-ai, synthesis, agents, analytics, prompt-engineering, harness-engineering]
sources: [wiki/concepts/cli-tools-for-agents.md, wiki/concepts/duckdb-for-agents.md, wiki/concepts/correctness-layer.md, wiki/concepts/agentic-analytics.md, wiki/concepts/context-engineering.md, wiki/concepts/agent-security-defense-in-depth.md, wiki/sources/duckdb-ai-workflow.md]
updated: 2026-10-20
---

# Optimising Agents for Data Exploration with Purpose-Built DuckDB CLIs

**Question:** How can agents be optimised to explore data by building DuckDB CLIs for the agent to call as tools?

**Short answer:** Don't hand the agent a database and a blank editor. Wrap DuckDB in a small CLI whose verbs match the exploration loop (orient → profile → drill → verify), whose output is bounded and structured, whose errors tell the agent what to do next, and whose permissions are enforced by the tool rather than requested in a prompt. The agent then spends its tokens on *deciding what to look at*, not on writing, debugging, and re-reading code.

> **Evidence note.** The *why CLIs work* material comes from one practitioner source (Hoyt Emerson, no benchmarks). The *how to design the CLI* section is my synthesis from the wiki's context-engineering, correctness-layer, and security pages. Treat the design rules as hypotheses to measure (see [Measure it](#7-measure-it)), not established results.

---

## 1. Why a CLI, and why DuckDB

Emerson's framing: CLI tools are "essentially localized MCP servers — tool calls on your computer without the need for direct MCP calls." The reasons it works for exploration ([CLI Tools for Agents](../../wiki/concepts/cli-tools-for-agents.md)):

| Property | Effect on the agent |
|---|---|
| Functions are baked in | Agent picks among operations instead of inventing code, so it stays focused |
| Small command → result → next command | Fast loop; errors are read and retried in-loop instead of debugging a whole script |
| No generated Python for ad hoc work | Fewer hallucinations ("Python files are where hallucinations are more prone") |
| Models already know DuckDB's CLI and SQL | Works even with a cheap, older model (Haiku) |
| No MCP server | Less overhead; MCP is better reserved for SaaS platforms |
| Local secrets manager | Agent passes SQL, never sees credentials |
| Stateless processes | Trivially parallel: one agent, one CLI session |

DuckDB specifically fits because it is in-process (~3 ms median latency, no network hop), reads Parquet/CSV/JSON/Postgres/S3 through one interface, and installs as a single binary ([DuckDB for Agents](../../wiki/concepts/duckdb-for-agents.md)). Low latency matters more than throughput here: exploration is hundreds of small, throwaway queries.

## 2. Raw `duckdb` CLI vs. a purpose-built wrapper

The stock DuckDB CLI is already a good agent tool. Building your own CLI on top buys four things the stock one can't:

1. **A narrower action space.** `explore profile orders.parquet` has one obvious way to be called. Raw SQL has infinite ways, and each one costs tokens to write and a chance to be wrong.
2. **Bounded, shaped output.** The stock CLI will happily print 2 million rows into the context window. A wrapper can cap rows, truncate wide cells, and lead with a summary.
3. **Enforced guardrails.** Read-only, row limits, statement allow-lists, and a query timeout live in the tool, which is the right place ([Agent Security: Defense-in-Depth](../../wiki/concepts/agent-security-defense-in-depth.md): enforcement below the agent, not in the prompt).
4. **Encoded team knowledge.** "Revenue is `net_amount` from `fct_orders`" can be a verb or a default, rather than something the agent re-derives each session.

Use the **raw CLI** when the data is clean and you're one person exploring (Emerson's case). Build a **wrapper** when several people or agents share it, the data is large or sensitive, or you've watched agents waste steps on the same things repeatedly.

## 3. Design the verbs around the exploration loop

Map verbs to what a good analyst actually does. Each verb should be one call, one answer.

| Stage | Verb | Backed by (DuckDB built-ins) | Agent learns |
|---|---|---|---|
| **Orient** | `sources` | `duckdb_tables()`, `glob()` | What exists |
| | `schema <src>` | `DESCRIBE` | Columns, types |
| | `sample <src> [-n]` | `USING SAMPLE`, `LIMIT` | What rows look like |
| **Profile** | `profile <src>` | `SUMMARIZE` | Nulls, min/max, approx distinct, quantiles per column |
| | `values <src> <col>` | `GROUP BY ... ORDER BY count DESC LIMIT` | Top categorical values, cardinality |
| | `dupes <src> <key...>` | `GROUP BY ... HAVING count(*) > 1` | Is this really the grain? |
| **Drill** | `query "<select>"` | Read-only SQL, capped | Anything the verbs don't cover |
| **Verify** | `join-check <a> <b> <key>` | anti-joins, match rates | Fan-out, orphan keys, join cardinality |
| | `compare <q1> <q2>` | `EXCEPT` both ways | Do two queries agree? |
| | `reconcile <q> --against <src>` | Aggregates vs. a known total | Does it tie to a trusted number? |

Why this shape:

- **`profile` first** collapses what would be dozens of exploratory queries (nulls per column, ranges, distinct counts) into one call. This is the biggest single token and step saver.
- **`query` is the escape hatch**, not the main door. If agents are mostly using `query`, your verbs are wrong; read the transcripts and promote the repeated patterns into verbs.
- **Verify verbs** are where this overlaps with the [Correctness Layer](../../wiki/concepts/correctness-layer.md): the agent doesn't *decide* the join is safe, it calls a function that *proves* match rates and fan-out. The SQL failure mode that matters for exploration is "runs green, answer wrong" ([Agentic Analytics](../../wiki/concepts/agentic-analytics.md)), and `join-check` and `reconcile` are cheap, deterministic checks against it. This is also where Emerson says AI is weakest ("sketchy on complex joins"), so it's the highest-value place to add structure.

## 4. Design the output for a reader with a token budget

The agent's context is the scarcest resource ([Context Engineering](../../wiki/concepts/context-engineering.md): context rot, instruction value expires). Shape every response accordingly.

- **Summary before detail.** First line: `rows=1,204,331 cols=18 truncated=false`. Then the table.
- **Hard caps with a visible truncation marker.** Default 50 rows, cell width ~80 chars, and print `... 1,204,281 more rows; narrow with WHERE or use values/profile`. A silent cap is dangerous: the agent will treat a truncated sample as the whole.
- **Stable, compact format.** Markdown tables or line-delimited JSON; same column order every time. Emerson saves results as markdown so they become reusable context for follow-up prompts, so make that the default output.
- **Provenance footer.** Source, row count, and freshness (file mtime or snapshot ID). This is the [provenance footer](../../wiki/concepts/agentic-analytics.md#the-provenance-footer) idea applied at tool level: the agent can then report how trustworthy its answer is.
- **Spill big results to disk.** If the user needs the full set, write Parquet to a scratch path and return the path plus a profile, never the rows.

## 5. Make errors do the agent's thinking

The in-loop retry is the core advantage, so give it good raw material. A bare DuckDB error costs a round trip to interpret; an informative one often costs none.

```
ERROR column "order_dt" not found in orders
  did you mean: order_date, ordered_at
  columns: order_id, customer_id, order_date, ordered_at, net_amount, ...
  next: explore schema orders
```

Rules of thumb: include nearest-match suggestions, the valid column list (or a pointer to `schema`), and the next command to try. Return **non-zero exit codes** so loops and harnesses can branch. Keep errors short; don't dump stack traces.

## 6. Put the guardrails in the tool, not the prompt

From [Agent Security](../../wiki/concepts/agent-security-defense-in-depth.md) and [Harness Engineering](../../wiki/concepts/harness-engineering.md): the harness is a controlled gateway; rules the agent can ignore aren't controls.

- **Read-only by default.** Open files and attach databases read-only; allow `SELECT`/`DESCRIBE`/`SUMMARIZE` only. Writes are a separate, explicitly named verb (or a separate CLI), and for anything production-bound route through [Write-Audit-Publish](../../wiki/concepts/write-audit-publish.md).
- **Resource limits.** Query timeout, memory limit, max rows returned. A runaway cross join shouldn't be survivable.
- **Credentials stay out of the agent.** Use DuckDB's persistent secrets manager so `ATTACH` just works and the agent only ever passes SQL. Emerson's pattern: production DuckLake = Postgres catalog + S3, with a stored secret. Note the wiki's caveat: this is convenience, not enforcement; scope the underlying credentials to read-only too.
- **Parallel-safe.** A DuckDB file allows one read-write connection. For parallel agents use read-only attaches, Parquet/CSV, or a DuckLake with a Postgres catalog. Make the CLI stateless so each agent invocation is independent.

## 7. Wire it in, then measure it

**Make it discoverable with almost no context.** A CLAUDE.md/AGENTS.md of a few lines is enough; Emerson's was essentially "use the DuckDB CLI only, here's the `ATTACH` statement, secrets are already stored." Follow the [AGENTS.md](../../wiki/concepts/agents-md.md) rule of writing only what the agent can't infer, and make the CLI self-describing (`explore --help` lists verbs with one-line examples) so the instructions don't have to. Skills and semantic layers added little for Emerson on clean gold data, but were decisive at enterprise scale ([Agentic Analytics](../../wiki/concepts/agentic-analytics.md): skills took accuracy 21% → 95%). If your data is messy or ambiguous, add a [Semantic Layer](../../wiki/concepts/semantic-layer.md) behind a verb like `metric <name>`, and require the agent to try it first.

**Measure it**, because the design rules above are untested hypotheses:

| Metric | How |
|---|---|
| Steps to correct answer | Count tool calls on a fixed question set |
| Tokens per task | Cost-per-task, not cost-per-token ([Correctness Layer](../../wiki/concepts/correctness-layer.md)) |
| Accuracy | Q/A pairs with known answers, pinned to a data snapshot |
| `query` share of calls | Falling share = verbs are covering real needs |
| Silent-wrong rate | Cases where the answer ran but was wrong; did `join-check`/`reconcile` catch them? |

Change one thing at a time and re-run the same set (the ablation discipline from Anthropic's analytics work). Also test with a cheap model: if a small model solves the set with your CLI but not with raw SQL access, the CLI is carrying real weight.

## 8. A minimal sketch

Illustrative only. The agent never writes or edits this; you do, once.

```python
#!/usr/bin/env python3
"""explore: agent-facing DuckDB CLI. Read-only, bounded, self-describing."""
import argparse, sys, duckdb

MAX_ROWS, MAX_CELL = 50, 80

def con():
    c = duckdb.connect(":memory:")          # stateless; attach read-only sources here
    c.execute("SET memory_limit='4GB'")
    return c

def show(rel, n=MAX_ROWS, src=""):
    cols = rel.columns
    rows = rel.fetchmany(n + 1)
    trunc = len(rows) > n
    print(f"source={src} cols={len(cols)} shown={min(len(rows), n)} truncated={str(trunc).lower()}")
    print("| " + " | ".join(cols) + " |")
    print("|" + "---|" * len(cols))
    for r in rows[:n]:
        print("| " + " | ".join(str(v)[:MAX_CELL] for v in r) + " |")
    if trunc:
        print("... more rows; narrow with WHERE, or use `values`/`profile`")

def fail(msg, hint):
    print(f"ERROR {msg}\n  next: {hint}", file=sys.stderr); sys.exit(1)

def main():
    p = argparse.ArgumentParser(prog="explore")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("schema", "profile", "sample"):
        sub.add_parser(name).add_argument("src")
    v = sub.add_parser("values"); v.add_argument("src"); v.add_argument("col")
    q = sub.add_parser("query"); q.add_argument("sql")
    a = p.parse_args()
    c = con()
    try:
        if a.cmd == "schema":  show(c.sql(f"DESCRIBE SELECT * FROM '{a.src}'"), src=a.src)
        if a.cmd == "profile": show(c.sql(f"SUMMARIZE SELECT * FROM '{a.src}'"), src=a.src)
        if a.cmd == "sample":  show(c.sql(f"SELECT * FROM '{a.src}' USING SAMPLE 20 ROWS"), src=a.src)
        if a.cmd == "values":
            show(c.sql(f'SELECT "{a.col}", count(*) AS n FROM \'{a.src}\' GROUP BY 1 ORDER BY n DESC'), src=a.src)
        if a.cmd == "query":
            stmts = duckdb.extract_statements(a.sql)
            if len(stmts) != 1 or stmts[0].type != duckdb.StatementType.SELECT:
                fail("only a single SELECT is allowed", "use `explore schema|profile|sample|values`")
            show(c.sql(a.sql))
    except duckdb.Error as e:
        fail(str(e).splitlines()[0], f"explore schema {getattr(a, 'src', '<src>')}")

main()
```

Smoke-tested on a small Parquet file (`schema`, `profile`, `values`, and the non-SELECT rejection and error hint all behave as shown). Known gap: a SELECT-only check does not stop `SELECT * FROM read_csv('/etc/passwd')`. For real use, restrict file access with `SET allowed_directories=[...]` followed by `SET enable_external_access=false` (or run the CLI in a sandbox with only the data mounted); the statement-type check alone is a speed bump, not a boundary.

Extensions worth adding, in order: `join-check`, `dupes`, a provenance footer, `--format json`, a query timeout, and read-only `ATTACH` for your lake or DuckLake.

## 9. Where this does not apply

- **Production pipelines.** Exploration CLIs are for understanding data. Anything that writes needs [Data Contracts](../../wiki/concepts/data-contracts.md) and [Write-Audit-Publish](../../wiki/concepts/write-audit-publish.md).
- **Data bigger than one node.** DuckDB is single-node; for petabyte scans route to Spark/Iceberg ([DuckDB for Agents](../../wiki/concepts/duckdb-for-agents.md)). A thin CLI can hide that routing from the agent.
- **Ambiguity, not mechanics, is the bottleneck.** If the problem is "which of 40 revenue columns?", better verbs won't fix it. That is a structure problem (canonical datasets, semantic layer), not an access problem ([Agentic Analytics](../../wiki/concepts/agentic-analytics.md)).
- **SaaS sources.** Emerson's own line: MCPs are for SaaS platforms; CLIs are for local and lake data.

## Takeaways

1. A CLI works because it shrinks the agent's action space and tightens its feedback loop; DuckDB makes that cheap and fast.
2. Wrap it when you need bounded output, enforced safety, or shared team knowledge. Otherwise the stock CLI is fine.
3. Verbs mirror the loop: orient, profile, drill, verify. `profile` and the verify verbs give the most leverage.
4. Output is context budget: summarise first, cap visibly, add provenance.
5. Errors should say what to try next; guardrails belong in the tool.
6. Measure steps, tokens, and accuracy against a fixed question set, with a cheap model as the stress test.
