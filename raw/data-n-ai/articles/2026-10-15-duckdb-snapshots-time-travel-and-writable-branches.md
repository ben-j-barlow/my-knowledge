---
title: "DuckDB Snapshots, Time Travel and Writable Branches"
source: "https://tobilg.com/posts/differential-storage-for-duckdb/?utm_source=tldrdata"
author:
  - "[[Tobias Müller]]"
published: 2026-10-15
created: 2026-10-28
description: "Add snapshots, time travel and writable branches to native DuckDB databases from SQL with duckdb-differential, and publish versions to S3."
tags:
  - "clippings"
---
*Snapshots, time travel and writable branches for pipelines, experiments, reproducible reports and more.*

A data import needs validation. A report needs last month’s numbers. A migration needs realistic test data. An analyst wants to compare two transformations, and an agent needs somewhere to try its own.

These workflows share a requirement: keep a known database state, then inspect it or work independently from it.

I built [duckdb-differential](https://github.com/tobilg/duckdb-differential) to make that available directly from SQL. It adds snapshots, time travel, writable branches, clones and restore to native DuckDB databases. Versions share unchanged data. Everything works locally; optional S3 publication lets other machines query a retained version or recover it into a writable database.

The extension is **experimental**, targeting **DuckDB 1.5.6 on Linux and macOS**. Let’s walk through several uses with one small database. Run the local examples in order in the same session, using an unused absolute directory for the repository:

```sql
INSTALL differential FROM community;
LOAD differential;
SET differential_repository = '/absolute/path/differential-demo';

ATTACH 'differential:retail' AS retail;
CREATE TABLE retail.orders (
    order_id INTEGER PRIMARY KEY,
    customer VARCHAR,
    amount DECIMAL(10, 2)
);
INSERT INTO retail.orders VALUES (1, 'Ada', 40.00), (2, 'Lin', 60.00);
CALL differential_create_snapshot('retail', name => 'baseline');
-- Snapshot 1: two orders, total 100.00
```

A snapshot retains the database’s checkpointed state. A branch starts a writable continuation from that state. A clone starts a separate database identity and snapshot history. Readers can keep querying the original while other work moves forward.

![A retained snapshot supports read-only reports, writable branches for imports, experiments and agents, and clones for testing. Each workspace starts from the same database state.](https://tobilg.com/images/posts/differential-storage-for-duckdb/versioned-workspaces.svg)

## Validate an import before adopting it

Suppose a daily feed contains an order whose amount was parsed with the wrong sign. Load it on a branch, where validation can catch the problem before it becomes part of the accepted dataset:

```sql
CALL differential_create_branch('retail', 'import_check', snapshot => 1);
ATTACH 'differential:retail' AS incoming (BRANCH 'import_check');
INSERT INTO incoming.orders VALUES (3, 'Jo', -25.00);

SELECT order_id FROM incoming.orders WHERE amount < 0;  -- 3
SELECT sum(amount) FROM retail.orders;                 -- Still 100.00
```

After checking the source, we correct the value to 25.00. A real pipeline could reload the affected batch after fixing its parser. Validation might check totals, missing keys, duplicate records or domain-specific rules:

```sql
UPDATE incoming.orders SET amount = 25.00 WHERE order_id = 3;
SELECT count(*) AS invalid_orders FROM incoming.orders WHERE amount < 0;
-- 0
SELECT count(*) AS orders, sum(amount) AS total FROM incoming.orders;
-- 3 orders, 125.00

CALL differential_create_snapshot(
    'incoming', name => 'validated_import', message => 'Daily feed validated'
);
-- Snapshot 2
DETACH incoming;
```

In this controlled workflow, `main` has stayed unchanged. We can adopt the candidate’s entire database state with restore:

```sql
DETACH retail;
CALL differential_restore('retail', 2, request_id => 'adopt-daily-import');
ATTACH 'differential:retail' AS retail;
SELECT sum(amount) FROM retail.orders;  -- 125.00
```

Restore requires a detached target branch, preserves its replaced state and creates a new snapshot of the selected contents: snapshot 3 here. There is **no automatic branch merge**. If another workflow has advanced `main`, reconcile those changes explicitly with SQL before adopting a candidate. Restore selects a whole database state; it does not combine diverging histories.

## Reproduce a report after the data changes

A report can record its input snapshot number and query that version again later. Attach it read-only when several queries should share the same input:

```sql
ATTACH 'differential:retail' AS report_data (SNAPSHOT_VERSION 3);

INSERT INTO retail.orders VALUES (4, 'Ada', 50.00);
CALL differential_create_snapshot('retail', name => 'later_sales');
-- Snapshot 4

SELECT sum(amount) FROM retail.orders;       -- 175.00
SELECT sum(amount) FROM report_data.orders;  -- 125.00
SELECT sum(amount) FROM retail.orders AT (VERSION => 3);  -- 125.00
DETACH report_data;
```

The live database now has another order, but the report’s input remains fixed. That is useful for monthly reporting, explaining a changed metric, and reproducing a bug against the data that triggered it. Snapshot numbers are scoped to a database: record the database identity alongside the version and report code.

A snapshot includes stored schema and data, but does not freeze external files referenced by views, credentials or session state. Materialize inputs and retain the query/code version when reproducibility matters. The same dataset alone cannot make a nondeterministic computation repeatable.

## Compare analytical scenarios

An analyst can model a pricing change on a branch without changing accepted orders. Here we deliberately start from the report’s three-order dataset:

```sql
CALL differential_create_branch('retail', 'discount', snapshot => 3);
ATTACH 'differential:retail' AS scenario (BRANCH 'discount');
UPDATE scenario.orders SET amount = amount * 0.90;

SELECT 'baseline' AS scenario, sum(amount) AS total
FROM retail.orders AT (VERSION => 3)
UNION ALL
SELECT 'discount', sum(amount) FROM scenario.orders;
-- baseline: 125.00; discount: 112.50

CALL differential_create_snapshot('scenario', name => 'discount_10pct');
DETACH scenario;
```

Additional branches can test different assumptions from the same baseline. This also works for alternative deduplication rules, segmentation logic and materialized transformations. For a calculation that is easily expressed as one read-only query, a snapshot may be sufficient; branches help when an experiment needs its own evolving tables or schema.

## Develop feature datasets on fixed inputs

A feature-engineering experiment can retain both its source data and derived tables, then label the result with its recipe:

```sql
CALL differential_create_branch('retail', 'feature_trial', snapshot => 3);
ATTACH 'differential:retail' AS features (BRANCH 'feature_trial');
CREATE TABLE features.customer_features AS
SELECT customer, count(*) AS order_count, sum(amount) AS total_spend
FROM features.orders GROUP BY customer;

SELECT count(*) FROM features.customer_features;  -- 3
CALL differential_create_snapshot(
    'features', name => 'customer_spend_v1',
    extra_info => '{"input_snapshot":3,"recipe":"customer_spend_v1"}'
);
DETACH features;
```

Another branch could build different features against snapshot 3. Retaining these datasets makes later evaluation comparisons easier to investigate. Model artifacts, random seeds and training code still need their own records; snapshot metadata can link to them. Differential supplies the database states, while your experiment tooling supplies the evaluation.

## Test a migration without changing the working database

A clone gives a test run its own database identity. It starts with snapshot 1 in its own history and shares the source’s unchanged payloads:

```sql
CALL differential_clone_database('retail', 'migration_test', snapshot => 3);
ATTACH 'differential:migration_test' AS test_db;
ALTER TABLE test_db.orders ADD COLUMN source VARCHAR DEFAULT 'import';

SELECT count(*) FROM test_db.orders WHERE source = 'import';  -- 3
SELECT count(*) FROM retail.orders;                         -- Still 4
DETACH test_db;

CALL differential_restore('migration_test', 1);
ATTACH 'differential:migration_test' AS test_db;
DESCRIBE test_db.orders;  -- Original three columns; no source column
DETACH test_db;
```

The test can exercise DuckDB’s native catalog, constraints and indexes. Restore resets its workspace between attempts while preserving the replaced state. Give concurrent test runs unique clone or branch names and a retention policy: resetting a workspace does not erase its history.

Clones live in the same repository and inherit the source’s data path. They do not create separate security boundaries or rewrite explicitly qualified catalog references in stored SQL. A fixture that explicitly refers to another database needs that dependency handled by the test harness.

## Give data agents independent attempts

An agent can use exactly the same SQL primitives as a notebook or pipeline. A controller might create a branch, expose it to one worker, inspect its candidate snapshot and decide whether to retain it:

```sql
CALL differential_create_branch(
    'retail', 'agent_attempt_42', snapshot => 3, request_id => 'attempt-42-branch'
);
ATTACH 'differential:retail' AS agent_work (BRANCH 'agent_attempt_42');

-- Example worker transformation: normalize customer labels.
UPDATE agent_work.orders SET customer = upper(customer);
SELECT count(*) AS orders, sum(amount) AS total FROM agent_work.orders;
-- 3 orders, 125.00; label correctness needs its own checks

CALL differential_create_snapshot(
    'agent_work', name => 'agent_candidate_42',
    message => 'Candidate for review', request_id => 'attempt-42-snapshot'
);
DETACH agent_work;
```

Different local processes can write different branches concurrently, with one writer process per branch. Snapshot readers remain independent. This supports several proposed transformations from a common input without requiring the workers to edit the same live database.

The controller still needs validation, resource limits and an appropriate tool interface. Branches provide data independence, **not a security sandbox**: repository access allows addressing other branches and databases. Untrusted workers need OS/container isolation as appropriate. `request_id` makes management operations retryable; it does not make arbitrary agent SQL idempotent.

## Share a validated dataset with another machine

S3 adds a distribution path to these local workflows. Create a database with an S3 `DATA_PATH`, and explicit snapshot creation exports synchronously by default. Later exports reuse previously uploaded chunks.

For this example, create a publication database from the report’s retained input. `DATA_PATH` is fixed at creation; choose S3 on the initial `ATTACH` if a database should publish its snapshots from the start.

Use an existing bucket, an unused prefix and your own region. Configure credentials through the AWS SDK chain, a named profile or scoped DuckDB `TYPE s3` secrets. The writer needs list/read/write access to the location; the reader needs list/read access. The [SQL API guide](https://github.com/tobilg/duckdb-differential/blob/main/docs/api.md) covers credentials and connection settings.

```sql
ATTACH 'differential:retail_release' AS published (
    DATA_PATH 's3://my-bucket/differential-demo/', REGION 'eu-central-1'
);
CREATE TABLE published.orders AS
SELECT * FROM retail.orders AT (VERSION => 3);

SELECT snapshot_id, export_state, export_locator
FROM differential_create_snapshot('published', name => 'report_dataset');
-- snapshot_id = 1; export_state = 'complete'; save export_locator
DETACH published;
```

This copies the selected table into a new publication database. On another machine, after configuring credentials, use a fresh session and repository:

```sql
INSTALL differential FROM community;
LOAD differential;
SET differential_repository = '/absolute/path/differential-reader';

ATTACH 'differential:s3://my-bucket/differential-demo/heads/retail_release/main'
AS published (REGION 'eu-central-1');
SELECT count(*) AS orders, sum(amount) AS total FROM published.orders;
-- 3 orders, 125.00
DETACH published;
```

The reader fetches verified file ranges on demand without downloading the whole database first. The attachment stays on the version selected at attach time. Reattach to see a newer head, or attach the saved `descriptors/<sha256>` URI to select a fixed export. A report, colleague or downstream application can therefore agree on a particular published dataset. Consumers need Differential and a compatible DuckDB reader.

![Local commits become durable in the writer's repository. A completed snapshot export enables on-demand read-only queries and full recovery into a new writable database, independently of the writer's volume.](https://tobilg.com/images/posts/differential-storage-for-duckdb/snapshot-publication.svg)

## Recover a writable database from a completed export

In the reader session, substitute the hash from the saved export locator:

```sql
CALL differential_recover_export(
    's3://my-bucket/differential-demo/descriptors/<sha256>',
    'retail_recovered', region => 'eu-central-1'
);
ATTACH 'differential:retail_recovered' AS recovered;
SELECT sum(amount) FROM recovered.orders;  -- 125.00
INSERT INTO recovered.orders VALUES (4, 'Ada', 50.00);
SELECT sum(amount) FROM recovered.orders;  -- 175.00
DETACH recovered;
```

Recovery downloads and verifies the contents, then creates a new database identity with local storage by default. It needs no original writer repository. This can support recovery after losing a local volume, moving work to another machine, or continuing independently from a shared dataset.

**A local commit and an S3 publication are separate durability boundaries.** Work is recoverable from S3 only once an export containing it has completed. Failed uploads retain local data for retry with `differential_retry_export`. Restoring a local snapshot cannot protect against losing the volume that holds every copy.

For several hosts writing one database, optional `WRITERS 'shared'` mode uses conditional S3 branch-head updates and preserves conflicting work for resolution. That has different publication settings and coordination rules; the [shared-database guide](https://github.com/tobilg/duckdb-differential/blob/main/docs/shared-databases.md) walks through them. Each host keeps its own local repository.

## How Differential stores versions

Underneath these workflows, DuckDB still handles SQL, transactions, indexes, compression and its catalog. Differential handles file operations, storing immutable chunks and their mappings in a local repository. Embedded SQLite coordinates metadata and default payload storage; no separate service is needed. A local `DATA_PATH` can place payload files in another directory.

Versions share unchanged payloads. Most chunks cover 64 KiB; the first isolates the native 12 KiB header region in a padded object. Branches and clones copy mappings, so creation has metadata costs proportional to the map size. Changes are measured in native file chunks: one updated row can affect several chunks. Local writes synchronize at native sync points using SQLite `FULL` synchronization, including `F_FULLFSYNC` on macOS. All S3 operations use the AWS SDK for C++.

The tradeoff is additional metadata, hashing and synchronization work. The [benchmark notes](https://github.com/tobilg/duckdb-differential/blob/main/docs/benchmarks.md) document measured workloads rather than a general performance guarantee. Retained versions also need maintenance: dropping a branch does not expire its snapshots, and local collection respects remaining snapshots, readers and pending operations. **Local cleanup never deletes exported S3 data or revokes an export locator.** Automatic remote garbage collection is not implemented. See the [lifecycle guide](https://github.com/tobilg/duckdb-differential/blob/main/docs/lifecycle.md) for expiry, eviction and cleanup.

## Import an existing DuckDB database

For your own existing `.duckdb` file, checkpoint and close it, then import it using an absolute path:

```sql
CALL differential_import_database('/absolute/path/existing.duckdb', 'imported');
ATTACH 'differential:imported' AS imported;
```

Import copies and verifies the source into managed storage and creates snapshot 1; it leaves the source unchanged. Files with WAL sidecars must be recovered, checkpointed and closed first.

## Compared with DuckLake and Iceberg

Differential’s focus is versioning a native database. [DuckLake snapshots](https://ducklake.select/docs/stable/duckdb/usage/snapshots) version a lakehouse catalog, and [Iceberg branches and tags](https://iceberg.apache.org/docs/latest/branching/) retain table histories. Those are useful choices when lakehouse interoperability is central. Ordinary DuckDB also supports [read-only S3 attachments](https://duckdb.org/docs/current/sql/statements/attach). Differential adds retained history, writable workspaces and incremental publication around native storage. An occasional small experiment may only need a checkpointed file copy; repeated experiments and retained versions make the extension more useful.

## Project status

The release remains experimental. Try one workflow: validate an import, preserve a report’s inputs, test a migration, or give an experiment its own branch. I’d like to hear what you tried and where it fell short. The [source](https://github.com/tobilg/duckdb-differential), [SQL reference](https://github.com/tobilg/duckdb-differential/blob/main/docs/sql-reference.md) and [issue tracker](https://github.com/tobilg/duckdb-differential/issues) are on GitHub.