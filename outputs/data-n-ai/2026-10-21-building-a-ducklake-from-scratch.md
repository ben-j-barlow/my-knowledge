---
tags: [data-n-ai, synthesis, agents, pipelines, etl, lakehouse, analytics]
sources: [wiki/concepts/ducklake.md, wiki/sources/2025-10-10-ducklake-tech-review.md, wiki/sources/2026-10-06-ducklake-maintenance-strategy.md, wiki/concepts/write-audit-publish.md, wiki/concepts/data-contracts.md, wiki/concepts/data-quality-traffic-lights.md, wiki/concepts/cli-tools-for-agents.md, wiki/concepts/agent-security-defense-in-depth.md, "https://ducklake.select/docs/stable/duckdb/usage/connecting", "https://ducklake.select/docs/stable/duckdb/usage/choosing_a_catalog_database", "https://ducklake.select/docs/stable/duckdb/usage/configuration", "https://ducklake.select/docs/stable/duckdb/usage/time_travel", "https://ducklake.select/docs/stable/duckdb/maintenance/recommended_maintenance"]
updated: 2026-10-21
---

# Guide: Building a DuckLake from Scratch (for an Agent) and Reading It from Dashboards

**Question:** What does an agent need to know to build a DuckLake for a new data store from scratch, and how is it read for dashboards?

**Audience:** a coding agent (or human) starting with an empty repo and a new data source. Written as an operating brief: decisions first, then ordered steps with copy-paste SQL, then verification, maintenance, and the dashboard read path.

> **Evidence note.** Three kinds of claim are mixed here, and each is labelled:
> - **[wiki]** from Hoyt Emerson's tutorials already ingested (practitioner, one author, no benchmarks).
> - **[docs]** from the official DuckLake docs (`ducklake.select/docs/stable`), fetched 2026-10-21.
> - **[synthesis]** my recommendation, built from wiki pages on write-audit-publish, data contracts, and agent security. Treat as hypotheses.
>
> DuckDB was **not installed** in this session, so no SQL below was executed. Run the smoke test (section 7) before trusting any of it. Exact DuckDB/DuckLake version requirements were not stated in the pages fetched. Pin versions yourself (section 2).

---

## 0. The mental model (read this first)

A DuckLake is **two things that must both survive**:

| Piece | What it holds | Where it lives |
|---|---|---|
| **Catalog** | All metadata: schemas, tables, snapshots, file lists, delete markers, *inlined small inserts* | A SQL database: DuckDB file, SQLite, **PostgreSQL**, (MySQL, not recommended) |
| **Data files** | Parquet files | Local folder or object storage (S3 etc.) |

There is no server. Every client (agent, pipeline, dashboard) runs its own DuckDB, loads the `ducklake` extension, and `ATTACH`es the pair. Compute is wherever DuckDB runs. [wiki][docs]

Consequences an agent must internalise:

1. **Losing the catalog = losing the lake**, even if the Parquet files are intact. Back up the catalog database like any production database.
2. **Every write creates a snapshot.** Snapshots are cheap; old *data files* are not deleted until you expire snapshots and clean up (section 8). DuckLake never deletes data files on its own. [docs]
3. **Concurrency is decided by the catalog choice**, not by DuckLake itself (section 1).
4. **Small inserts may live in the catalog**, not in Parquet (data inlining). Don't be surprised when `glob()` on the data folder doesn't show recent rows. [wiki]

---

## 1. Decisions to make before writing any code

Make these decisions explicitly and write them into the repo's `AGENTS.md` / README. An agent that guesses here will rebuild later.

### 1.1 Catalog database

| Situation | Catalog | Why [docs] |
|---|---|---|
| One person/agent, local prototype | **DuckDB file** | Simplest; "limited to a single client" |
| Several local processes (agent + dashboard on a laptop) | **SQLite** | Local multi-process, retries on write lock; no concurrent read+write |
| Multi-user, remote clients, anything shared | **PostgreSQL ≥ 12** | The only option presented as multi-user; managed Postgres (e.g. Supabase) works [wiki] |
| (avoid) | MySQL ≥ 8 | Docs explicitly do not recommend it (connector issues) |

**Default recommendation [synthesis]:** prototype on a DuckDB-file catalog, but if dashboards or more than one writer/reader will ever touch it, start on Postgres. Migrating catalogs later is the expensive path.

### 1.2 Data storage

- Prototype: local folder (default `<catalog>.files/` for a DuckDB-file catalog).
- Shared/production: object storage (`s3://bucket/prefix/`). `DATA_PATH` is **required** for non-DuckDB catalogs. [docs]
- One bucket/prefix per lake. Never share a prefix between two DuckLakes (orphan cleanup, section 8, deletes files the catalog doesn't know).

### 1.3 Write pattern (drives maintenance)

| Pattern | Effect | Maintenance consequence [wiki] |
|---|---|---|
| Tiny/streaming inserts (<10 rows each, default inlining limit) | Rows pile up *in the catalog* | Must `flush_inlined_data` or Postgres degrades |
| Batch appends (>10 rows) | Many Parquet files accumulate | `merge_adjacent_files` |
| Daily drop-and-recreate (Emerson's case) | One live file, many dead ones | `expire_snapshots` + `cleanup_old_files` is the whole job |
| Row-level UPDATE/DELETE | Delete files accumulate | `rewrite_data_files` |

### 1.4 Time-travel policy

Decide **how many days of history users get** (Emerson uses a 7-day rolling window [wiki]). This one number becomes the `older_than` interval in maintenance. Time travel only works while the old data files still exist: expire a snapshot and its files, and that version is gone.

### 1.5 Who reads, and how

Decide now: agents only? Analysts in DuckDB CLI/UI? A BI dashboard? This determines credentials and roles (section 9) and the dashboard pattern (section 10).

---

## 2. Prerequisites and repo layout

**Install:** DuckDB (CLI and/or Python package). The `ducklake` extension is installed from within DuckDB (`INSTALL ducklake;`). The `postgres` and `httpfs` extensions are needed for a Postgres catalog and S3 respectively; DuckDB normally autoloads them. [wiki][docs]

**Pin versions** in the repo (`requirements.txt` / `uv.lock` / a `.duckdb-version` file). The catalog schema is versioned, and `AUTOMATIC_MIGRATION` defaults to `false` [docs], so an upgraded client can refuse to open an older catalog. Upgrade deliberately, not incidentally.

Suggested layout (adapt to the repo; this mirrors the medallion layout in [the longer-running-agents guide](2026-10-09-enabling-longer-running-agentic-development-data-ingestion.md)):

```
lake/
  README.md              # the 1.x decisions above, catalog/data locations (NOT secrets)
  sql/
    00_secrets.sql.tmpl  # templates only; real secrets are never committed
    01_attach.sql
    02_options.sql
    10_schemas.sql
    20_bronze_*.sql
    30_silver_*.sql
    40_gold_*.sql
    90_maintenance.sql
  pipelines/             # python/dbt/etc. that run the sql
  contracts/             # data contracts + audit assertions (section 6)
  tests/
    smoke_test.py        # section 7
```

---

## 3. Credentials: agent passes SQL, never sees secrets

Use **DuckDB secrets** so the agent attaches the lake without handling credentials. A persistent secret survives sessions. [wiki: CLI Tools for Agents][docs]

```sql
-- Postgres catalog credentials
CREATE OR REPLACE PERSISTENT SECRET pg_catalog_secret (
    TYPE postgres,
    HOST '<host>', PORT 5432, DATABASE '<db>',
    USER '<user>', PASSWORD '<password>'
);

-- S3 data credentials (use the credential chain where possible)
CREATE OR REPLACE PERSISTENT SECRET s3_lake_secret (
    TYPE s3, PROVIDER credential_chain, REGION '<region>'
);

-- A DuckLake secret bundling catalog + data path  [docs]
CREATE OR REPLACE PERSISTENT SECRET my_lake (
    TYPE ducklake,
    METADATA_PATH '',
    DATA_PATH 's3://<bucket>/<prefix>/',
    METADATA_PARAMETERS MAP {'TYPE': 'postgres', 'SECRET': 'pg_catalog_secret'}
);
```

Rules for the agent [synthesis, from [Agent Security](../../wiki/concepts/agent-security-defense-in-depth.md)]:

- Real values come from the human or a secrets manager. **The agent writes templates, never real passwords, and never commits `~/.duckdb/stored_secrets`.**
- Create **separate catalog roles for writer and reader** (section 9) and one secret per role.
- If you cannot create secrets, stop and ask. Don't inline credentials in SQL files.

---

## 4. Bootstrap: create the lake

### 4.1 Local prototype (DuckDB-file catalog)

```sql
INSTALL ducklake;
ATTACH 'ducklake:my_lake.ducklake' AS lake;   -- creates catalog + my_lake.ducklake.files/
USE lake;
```
[wiki][docs] `CREATE_IF_NOT_EXISTS` defaults to `true`, so **a typo in the path silently creates a brand-new empty lake**. Always confirm what you attached (section 7, check 1).

### 4.2 Shared lake (Postgres catalog + S3 data)

```sql
INSTALL ducklake;

-- via the secret from section 3
ATTACH 'ducklake:my_lake' AS lake;

-- or explicitly (data path required for Postgres catalogs)
ATTACH 'ducklake:postgres:dbname=<db> host=<host> user=<user>'
    AS lake (DATA_PATH 's3://<bucket>/<prefix>/');
```
[docs]

For **first-time creation only**, the writer role must have rights to create the DuckLake metadata tables in the catalog database. Afterwards, day-to-day pipelines don't need DDL on Postgres itself. [synthesis]

### 4.3 Set options once, then record them

```sql
CALL lake.set_option('parquet_compression', 'zstd');     -- default snappy
CALL lake.set_option('expire_older_than', '7 days');     -- see caveat below
CALL lake.set_option('require_commit_message', true);    -- agents must explain writes
FROM lake.options();                                      -- read them back
```
[docs] Options can be scoped global → schema (`schema => 'gold'`) → table (`table_name => '...'`); the most specific wins. Notable options and defaults: `data_inlining_row_limit` 10, `target_file_size` 512MB, `parquet_row_group_size` 122880, `rewrite_delete_threshold` 0.95, `auto_compact` true.

Caveats [synthesis, unverified]:
- The docs describe `expire_older_than` as "minimum age of snapshots before they are expired by default". Confirm on your version that the maintenance calls honour it. Safer: always pass `older_than` explicitly (section 8).
- `require_commit_message => true` is worth enabling for agent-written lakes, since the audit trail is the point (section 5.3). Check that your pipeline code always sets one, or writes will fail.
- The `ATTACH` options table lists `DATA_INLINING_ROW_LIMIT` default `0`, while the options table lists `data_inlining_row_limit` default `10`, and Emerson reports <10 rows are inlined. Don't rely on either: **set it explicitly** (`0` disables inlining if you'd rather have no catalog-resident rows).

### 4.4 Schemas = layers

```sql
CREATE SCHEMA IF NOT EXISTS lake.bronze;   -- raw, as landed
CREATE SCHEMA IF NOT EXISTS lake.silver;   -- cleaned, typed, deduped
CREATE SCHEMA IF NOT EXISTS lake.gold;     -- dashboard-facing, contract-bound
CREATE SCHEMA IF NOT EXISTS lake.staging;  -- write-audit-publish landing zone (section 6)
```
Dashboards read **gold only**. Agents exploring read silver/gold.

---

## 5. Loading data

### 5.1 First load

```sql
CREATE TABLE lake.bronze.orders AS
FROM read_csv('path/or/s3://.../orders*.csv');      -- format auto-detected [wiki]
```
For other sources DuckDB can read Parquet, JSON, Postgres (`postgres_scanner`/`ATTACH ... TYPE postgres`), and S3 through one interface.

### 5.2 Ongoing loads: pick one and document it

| Pattern | SQL shape | Notes |
|---|---|---|
| **Recreate** (small data, simplest) | `DROP`+`CREATE TABLE AS` in one transaction | Emerson's daily gold rebuild. Fine until rebuild time hurts. Leaves old files until cleanup |
| **Append** | `INSERT INTO ... SELECT` | Needs an idempotency key (`WHERE NOT EXISTS`, or load-ledger table). Many files → merge |
| **Replace partition/slice** | `DELETE ... WHERE batch_date = X; INSERT ...` in one transaction | Atomic, idempotent re-runs |

Wrap multi-statement changes in `BEGIN; ... COMMIT;` so readers never see half a load. Re-running a job must be safe (idempotent); agents retry.

### 5.3 Always set a commit message

```sql
BEGIN;
INSERT INTO lake.silver.orders SELECT ... FROM lake.bronze.orders WHERE ...;
CALL lake.set_commit_message('etl-agent', 'Load orders batch 2026-10-21',
                             extra_info => '{"run_id": "abc123", "source": "orders_v2"}');
COMMIT;
```
[wiki] Without it, `ducklake_snapshots()` only shows a terse `changes` column. Putting a `run_id` in `extra_info` ties each snapshot to a pipeline run, which is exactly what you want for audit and rollback.

### 5.4 Schema changes and partitioning

```sql
ALTER TABLE lake.silver.orders ADD COLUMN channel VARCHAR DEFAULT 'unknown';  -- no Parquet rewrite
ALTER TABLE lake.silver.orders DROP COLUMN channel;
ALTER TABLE lake.silver.events SET PARTITIONED BY (year(created_at), month(created_at));
```
[wiki] Partitioning applies **only to data written after** the change, and is usually unnecessary at small scale (small-file risk). Don't partition by default.

---

## 6. Trust: write-audit-publish and contracts

Agent-written pipelines must not publish unaudited data to gold. Apply [Write-Audit-Publish](../../wiki/concepts/write-audit-publish.md) and [Data Contracts](../../wiki/concepts/data-contracts.md) [synthesis]:

1. **Write** the candidate table into `lake.staging.<name>`.
2. **Audit** with assertions from `contracts/` (row count > 0 and within ±X% of previous snapshot, no NULL keys, unique grain, referential checks, value ranges, freshness).
3. **Publish** only if every assertion passes: in one transaction, replace `lake.gold.<name>` from staging and set a commit message with the audit result.

```sql
-- audit example: grain must be unique
SELECT count(*) AS dupes FROM (
  SELECT order_id FROM lake.staging.orders_gold GROUP BY order_id HAVING count(*) > 1
);   -- must return 0 or the publish step does not run
```

Because every publish is a snapshot, a bad publish is recoverable: query `AT (VERSION => n-1)`, compare, and restore, **provided the old files haven't been cleaned up**. This is a reason to keep the retention window longer than your slowest detection time.

---

## 7. Verify the build (do not declare done without this)

An agent that stops at "the SQL ran" has not finished ([Premature Completion Declaration](../../wiki/concepts/premature-completion-declaration.md)). Run and show the output of each check:

| # | Check | How | Pass condition |
|---|---|---|---|
| 1 | Attached the right lake | `FROM lake.options();` and `SELECT * FROM duckdb_databases();` | `data_path` and catalog are the intended ones, not a stray new file |
| 2 | Tables exist with right schema | `DESCRIBE lake.gold.<t>;` | Matches contract |
| 3 | Data readable | `SELECT count(*) FROM lake.gold.<t>;` | Non-zero, matches source |
| 4 | Snapshots recorded | `FROM ducklake_snapshots('lake');` | One per write; commit messages present |
| 5 | Time travel works | `SELECT ... FROM t AT (VERSION => 1)` vs current | Differs where expected |
| 6 | Files are where expected | `FROM ducklake_list_files('lake', '<table>');` (or `FROM glob('<data_path>/**/*')`) | Parquet in the expected location. Absence for tiny tables may just be inlining |
| 7 | **Second client can read** | New process, reader credentials, `ATTACH ... (READ_ONLY)`, `SELECT` | Works. This is what the dashboard will do |
| 8 | **Reader cannot write** | Same session: `INSERT`/`CREATE TABLE` | Fails (permission denied) |
| 9 | Maintenance dry-runs clean | section 8 with `dry_run => true` | Plausible lists, nothing unexpected |

Put checks 1–8 in `tests/smoke_test.py` so the loop has a binding gate, not a prose reminder (see [Harness Engineering](../../wiki/concepts/harness-engineering.md)).

---

## 8. Maintenance (schedule it from day one)

Open-source lakehouses leave this to you. [wiki] Order matters: expire → clean up.

```sql
-- 0. dry-run everything first
CALL ducklake_expire_snapshots('lake', dry_run => true, older_than => now() - INTERVAL '7 days');

-- 1. flush inlined rows to Parquet (only if you stream/tiny-insert)
CALL ducklake_flush_inlined_data('lake');

-- 2. compact small files (batch-append lakes)
CALL ducklake_merge_adjacent_files('lake');

-- 3. retire snapshots outside the time-travel window
CALL ducklake_expire_snapshots('lake', older_than => now() - INTERVAL '7 days');

-- 4. delete files no remaining snapshot references (grace window protects in-flight queries)
CALL ducklake_cleanup_old_files('lake', dry_run => true,  older_than => now() - INTERVAL '1 hour');
CALL ducklake_cleanup_old_files('lake', dry_run => false, older_than => now() - INTERVAL '1 hour');

-- 5. rewrite files dominated by deletes (UPDATE/DELETE-heavy tables)
CALL ducklake_rewrite_data_files('lake');

-- 6. files in storage the catalog doesn't know about
CALL ducklake_delete_orphaned_files('lake', dry_run => true);
CALL ducklake_delete_orphaned_files('lake', dry_run => false);
```
Syntax for steps 3–4 and 6 is from Emerson's tutorial [wiki]; the others use the same call shape per the docs' function list [docs]. The single `CHECKPOINT;` statement runs the set together. The docs recommend it for periodic runs. For the catalog itself, on PostgreSQL an occasional `VACUUM` is "likely sufficient". [docs]

**Rules for the agent:**
- **Always dry-run first and read the list**, especially `delete_orphaned_files`: it deletes anything under the data path the catalog doesn't track (the reason for one prefix per lake, section 1.2).
- Keep the cleanup grace window (`older_than` ≥ 1 hour here) so running queries, including a dashboard mid-refresh, don't lose files.
- Schedule maintenance **after** the daily load, as one job. Emerson ran it as a Python script on a scheduler (MotherDuck Flights, sponsor of that article). Any scheduler works.
- Don't shorten retention without telling the human: it permanently removes the ability to roll back.

---

## 9. Access control: writer vs. reader

This is **[synthesis]**. I couldn't retrieve a DuckLake access-control page, so verify against your catalog and bucket.

| Principal | Catalog (Postgres) | Object storage | Used by |
|---|---|---|---|
| **Writer / maintainer** | Read-write on the DuckLake metadata tables | Read, write, **delete** on the prefix | Pipelines, maintenance job |
| **Reader** | **SELECT only** on the metadata tables | **Read-only** (`GetObject`, `ListBucket`) on the prefix | Dashboards, analysts, exploring agents |

- Enforcement belongs in Postgres grants and IAM, **not** in `ATTACH (READ_ONLY)` alone. `READ_ONLY` is a client-side flag, and a reader holding writer credentials can simply omit it. Use both: grants as the lock, the flag as a seatbelt. [docs for the flag; rest synthesis]
- Exploring agents get the **reader** secret only. This follows [Agent Security: Defense-in-Depth](../../wiki/concepts/agent-security-defense-in-depth.md): enforcement below the agent.
- If you use a DuckDB-file or SQLite catalog, there is no such separation. Everyone with the file is a writer.

---

## 10. Reading the DuckLake for dashboards

### 10.1 What a "dashboard read" really is

There is no DuckLake server to point a BI tool at. A dashboard is **another DuckDB client**: some process running DuckDB attaches the lake read-only, runs SQL against gold tables, and returns rows. The only question is *where that DuckDB process lives*. [docs: catalog is the sync point]

```sql
-- what every dashboard backend does at startup
INSTALL ducklake; LOAD ducklake;
-- reader credentials (pg reader role + S3 read-only) via secret
ATTACH 'ducklake:my_lake_reader' AS lake (READ_ONLY);
SELECT ... FROM lake.gold.sales_daily WHERE ...;
```

Multiple dashboards/users reading concurrently requires a **Postgres catalog** (section 1.1). Do not point many dashboard workers at a DuckDB-file catalog.

### 10.2 Four patterns

| # | Pattern | Shape | Best for | Watch out |
|---|---|---|---|---|
| A | **Embedded DuckDB in the app** | Streamlit/Dash/FastAPI/Evidence/notebook process attaches the lake read-only and queries gold | Internal tools, small user counts, fastest to build | Every worker holds its own connection and S3 reads; cold-start `ATTACH` cost; credentials live in the app host |
| B | **BI tool via a DuckDB connection** | Metabase, Superset, Grafana, etc. using a DuckDB driver with an init step that runs the `ATTACH` | Existing BI stack, self-serve for analysts | **Unverified.** My web search found only video titles about connecting Metabase and Superset to DuckLake on S3, no docs. Test that the driver (a) loads extensions, (b) runs init SQL, (c) supports concurrent sessions, before committing |
| C | **Thin query API** | A small service owns the DuckLake connection and exposes parameterised endpoints; the dashboard calls the API | Many viewers, many tools, tight control; caching and auth in one place | One more service to run. Worth it past a handful of users |
| D | **Export / materialise** | A job after the daily load writes gold aggregates to Parquet/CSV (or a small DuckDB file) that the dashboard reads | Static or build-time dashboards (e.g. Evidence builds), very high fan-out, reader should never touch the lake | Staleness equals export cadence; one more artefact to keep consistent |

**Default recommendation [synthesis]:** start with **A** for an internal dashboard; move to **C** when more than one dashboard tool or many viewers appear; use **D** when the dashboard is public or build-time.

### 10.3 Dashboard-specific techniques

1. **Read gold, never bronze.** Gold tables are the contract-bound, audited layer (section 6). Build dashboard-shaped (pre-aggregated, denormalised) gold tables; dashboards shouldn't join five silver tables on every refresh.
2. **Pin a consistent snapshot per page load.** Tiles queried at different moments can disagree if a load lands between them. Either attach at a snapshot (`ATTACH 'ducklake:...' (SNAPSHOT_VERSION n)` or `(SNAPSHOT_TIME '...')` [docs]) or capture `max(snapshot_id)` once and use `AT (VERSION => n)` on every query. Cheap insurance for multi-tile pages.
3. **Show data freshness.** Surface `max(snapshot_time)` from `ducklake_snapshots('lake')` (or the latest commit message / `run_id`) as a "Last updated" badge. This feeds [Data Quality Traffic Lights](../../wiki/concepts/data-quality-traffic-lights.md): red if the latest snapshot is older than the SLA.
4. **Use snapshots as a feature.** Emerson's suggestion: put snapshots in a dashboard filter ("compare to yesterday's version"), or display commit messages as a change log. This is only possible inside your retention window. The 7-day policy is literally the dashboard's history depth. [wiki]
5. **Choose the right query path for performance.** Parquet is columnar, so select only needed columns. Pre-aggregate heavy metrics in gold. Keep files large via `merge_adjacent_files` (fewer files = faster scans, [wiki]). Put a result cache (app-level or API-level, keyed on snapshot id) in front of expensive tiles: **the snapshot id is a perfect cache key**, since results for a given id never change.
6. **Keep dashboards read-only and bounded.** Reader role (section 9), query timeout, row limit in the API/driver.
7. **Plan around maintenance.** `cleanup_old_files` after a grace window can delete files an open dashboard query still needs. Schedule maintenance outside peak hours and keep the 1-hour (or longer) grace window. A pinned snapshot older than the retention window will start failing.
8. **Network cost.** Readers pull Parquet from S3. A dashboard in a different region from the bucket pays latency and egress. Co-locate, or use pattern D.

### 10.4 Agents as dashboard authors

An agent building a dashboard should [synthesis]:
- Use the **reader** secret only, and confirm with smoke check 8 that writes fail.
- Query through a thin CLI/wrapper (see [Optimising Agents for Data Exploration with DuckDB CLIs](2026-10-20-duckdb-clis-for-agent-data-exploration.md)) with row caps.
- Read business definitions from the semantic layer / gold column docs rather than inventing metric logic ([Semantic Layer](../../wiki/concepts/semantic-layer.md)). Define each dashboard metric once, in a gold table or view.
- Verify every tile's number against an independent query before declaring the dashboard done.

---

## 11. Common failure modes

| Failure | Cause | Prevention |
|---|---|---|
| "Lake is empty" after a restart | `CREATE_IF_NOT_EXISTS=true` created a new lake at a mistyped/relative path | Absolute paths or secrets; smoke check 1 |
| Reads fail after upgrading DuckDB | Catalog schema version mismatch (`AUTOMATIC_MIGRATION` default false) | Pin versions; migrate deliberately |
| Recent rows missing from `glob()` | Inlined in the catalog | Query through the table, or `flush_inlined_data` |
| Postgres catalog slows down | Streaming tiny inserts → large inlined tables | Flush on a schedule, or set `data_inlining_row_limit` to 0 |
| Storage bill keeps growing | Never expired snapshots / cleaned files | Daily maintenance job |
| Time travel returns "not found" | Version expired; files cleaned | Retention ≥ detection time; check `ducklake_snapshots` |
| Dashboard query errors mid-refresh | Files cleaned during a long query | Grace window; run maintenance off-peak |
| Reader modified data | Reader had writer credentials | Separate roles and IAM (section 9) |
| Concurrent writers collide | DuckDB-file or SQLite catalog | Postgres catalog; serialize writers |
| Orphan cleanup deleted unrelated files | Shared bucket prefix | One prefix per lake; always dry-run |
| Bad gold publish | No audit gate | Write-audit-publish (section 6) |

---

## 12. Agent task checklist (copy into the feature list)

1. Record decisions 1.1–1.5 in `lake/README.md`. **Ask the human** if catalog choice, retention window, or reader population is unknown.
2. Pin versions; write secret templates; get the human to supply real credentials.
3. Create the lake, set and record options, create schemas.
4. Load one source end to end with idempotent, committed-with-message transactions.
5. Add contracts and the staging → audit → gold publish step.
6. Run the smoke test (section 7); paste the output.
7. Write and dry-run the maintenance job; schedule it after the load.
8. Create reader role/secret; verify reader can't write.
9. Build the dashboard read path (section 10) with snapshot pinning and a freshness badge.
10. Report what was verified and what was not.

---

## Open questions and gaps

- **Untested here.** No DuckDB was available, so every statement is from docs/tutorials, not execution.
- **Dashboard tool drivers** (Metabase, Superset, Grafana, Evidence) with DuckLake are unverified. Only titles of tutorials were found.
- **Postgres role grants** and the exact S3 policy for a read-only DuckLake client were not found in the docs fetched. Section 9 is a design recommendation.
- **Upsert/MERGE** support and **multiple concurrent writers** to one table: not covered by fetched pages. Check the docs before designing for them.
- **Version requirements** and format-stability guarantees: not stated in fetched pages. See also the date discrepancy noted on the [DuckLake](../../wiki/concepts/ducklake.md) page.

## Sources

- [DuckLake docs: Connecting](https://ducklake.select/docs/stable/duckdb/usage/connecting)
- [DuckLake docs: Choosing a Catalog Database](https://ducklake.select/docs/stable/duckdb/usage/choosing_a_catalog_database)
- [DuckLake docs: Configuration](https://ducklake.select/docs/stable/duckdb/usage/configuration)
- [DuckLake docs: Time Travel](https://ducklake.select/docs/stable/duckdb/usage/time_travel)
- [DuckLake docs: Recommended Maintenance](https://ducklake.select/docs/stable/duckdb/maintenance/recommended_maintenance)
- Wiki: [DuckLake](../../wiki/concepts/ducklake.md), [Tech Review](../../wiki/sources/2025-10-10-ducklake-tech-review.md), [Maintenance Strategy](../../wiki/sources/2026-10-06-ducklake-maintenance-strategy.md), [Write-Audit-Publish](../../wiki/concepts/write-audit-publish.md), [Data Contracts](../../wiki/concepts/data-contracts.md)
