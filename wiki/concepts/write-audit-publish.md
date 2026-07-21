---
tags: [data-n-ai, concept, pipelines, testing, etl]
sources: [wiki/sources/motherduck-trustworthy-ai-pipelines.md]
updated: 2026-07-21
---

# Write-Audit-Publish (WAP)

A three-phase pattern for safe data pipeline deployment: build the result (write) → validate against a spec (audit) → only then publish. The audit gate is the only permission for data to leave the pipeline; if validation fails, the pipeline fails loudly rather than loading wrong numbers.

## Three Phases

### 1. Write
Generate the output in a staging layer. For idempotent pipelines: clear the window (e.g., delete this year), then insert fresh results. No touching the published table yet.

### 2. Audit
Run assertions against the [[data-contracts]]. Check:
- Row counts and nullability
- Column value ranges
- Uniqueness constraints
- Grain and deduplication rules
- Any fuzzy business rule that's hard to encode in SQL

If audit passes, proceed to publish. If audit fails, the pipeline errors loudly — no silent data corruption.

### 3. Publish
Only if audit passed: move or swap the staging output to the published table. This is typically a single atomic operation (INSERT, or table swap for efficiency).

## Example: NOAA GHCN Pipeline

```python
# 1. WRITE: Clear the year, then insert fresh results
con.execute(f"DELETE FROM {TABLE} WHERE year = {int(year)}")
con.execute(f"INSERT INTO {TABLE} BY NAME SELECT * FROM staging")

# 2. AUDIT: Assert the contract
MIN_C, MAX_C = -90.0, 60.0
n, bad_range, nulls = con.execute(f"""
    SELECT COUNT(*),
           COUNT(*) FILTER (WHERE value_c < {MIN_C} OR value_c > {MAX_C}),
           COUNT(*) FILTER (WHERE station IS NULL OR obs_date IS NULL OR value_c IS NULL)
    FROM {table}""").fetchone()

assert n > 0, "audit: staging is empty"
assert bad_range == 0, f"audit: {bad_range} readings outside {MIN_C}..{MAX_C} C (units bug?)"
assert nulls == 0, f"audit: {nulls} rows with null station/date/value"

# 3. PUBLISH: If audit passed, data is already in the table
# (INSERT was within the audit check, so we're good to go)
```

## Why WAP for AI-Generated Pipelines

AI is non-deterministic and can't see data. It can produce code that runs (no errors) but returns wrong numbers. The [[data-contracts]]-based audit is the guardrail:

- **Catches silent bugs:** Unit conversion bugs (forgot `/10`), duplicates, quality-flag leakage, grain changes — all caught by range/uniqueness/count assertions
- **Fail loudly:** A pipeline that errors is far better than one that loads silently wrong data. The agent reads the error, fixes the transform, and retries
- **Deterministic gate:** Unlike testing code (which is open-ended), the audit gate is a deterministic check of output against a formal spec — the same assertion runs the same way every time

## Common Audit Assertions

```python
# Range check (catches unit bugs)
assert all(MIN <= col <= MAX)

# Deduplication  
assert count_distinct(key_cols) == count(rows)  # exactly one row per key

# Null checks
assert not any(key_cols.isnull())

# Row count sanity
assert count(rows) > 0  # not empty
assert count(rows) < MAX_EXPECTED  # not runaway growth

# Foreign key checks (if downstream dependencies exist)
assert all(foreign_key in upstream_table)
```

## Related Concepts

- [[data-contracts]] — the specification being audited
- [[agents-in-data-engineering]] — WAP is the canonical safe deployment for agent-written pipelines
- [[self-healing-pipelines]] — cascading recovery; WAP is the first gate
