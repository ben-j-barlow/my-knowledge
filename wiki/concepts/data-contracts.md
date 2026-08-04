---
tags: [data-n-ai, concept, pipelines, testing, agents]
sources: [wiki/sources/motherduck-trustworthy-ai-pipelines.md]
updated: 2026-07-21
---

# Data Contracts

Executable specifications of the output of a data pipeline. A contract defines what table exists, what one row means, the exact transformation of each column, and the invariants that must hold. Replaces informal prompts or prose documentation with formal, testable assertions.

## Structure

A data contract typically includes:

- **Table name and schema** — what table(s) exist after the pipeline runs
- **Row semantics** — what exactly one row represents (grain, deduplication rules, uniqueness)
- **Column definitions** — transformation rules, units, null handling, valid ranges
- **KPI or aggregation semantics** — what the data is meant to compute, including critical gotchas (e.g., "same-station mean TMAX per year; *must hold station set fixed across years* to avoid bias from changing network coverage")
- **Invariants and guardrails** — ranges, nullability, uniqueness, referential integrity, row counts

## Example: NOAA GHCN Daily Max Temperatures

```
Table climate_demo.daily_tmax holds QA-passed daily MAXIMUM temperature, in
degrees Celsius, for US weather stations.

- value_c = DATA_VALUE / 10.0   (GHCN stores tenths of a degree: 151 = 15.1 C)
- a valid reading has Q_FLAG IS NULL (passed NOAA quality checks)
- obs_date parsed from YYYYMMDD string
- exactly one row per (station, obs_date)
- idempotent by year: re-running a year replaces just that year

KPI: same-station mean TMAX per year. To measure trend, MUST hold
the station set fixed. All-station average biased by changing coverage
(new stations added in colder places), making real warming look like cooling.
```

## Why Contracts Matter for AI-Generated Code

**Correctness vs. confidence:** A pipeline that runs green (no errors) is not a pipeline that is correct (returns the right numbers). AI is non-deterministic (same prompt, different outputs) and can't see data/metadata (schema, units, quality flags), so it guesses silently.

A contract is the antidote:
- **For the agent:** Clear, unambiguous specification of the goal; no room for misinterpretation
- **For testing:** Contracts become assertions; a pipeline that fails a contract assertion is far better than one that loads wrong numbers silently
- **For humans:** A contract documents the real business logic (e.g., the station-set-fixed rule) in a way that explains *why* the pipeline exists

## Contract as Assertion (Write-Audit-Publish)

The contract becomes testable code. Unit tests verify the transform against the contract locally (sample rows, mock data, range checks). In production, a [[write-audit-publish]] gate refuses to publish if any row violates the contract.

Example audit assertions:
```
MIN_C, MAX_C = -90.0, 60.0  # world records about -89 and +57
assert no readings < MIN_C or > MAX_C, f"unit bug? {count} outside range"
assert no nulls in (station, obs_date, value_c)
assert exactly one row per (station, obs_date)
```

A single forgotten `/10` on the unit conversion will put every reading far outside the valid range; the range check catches it automatically.

## Antipatterns

- **Vague prompts as contracts:** "Make the pipeline correct" or "Use the data standards" — too ambiguous for both agent and tests
- **Silent assumptions:** Contracts that don't spell out the KPI bias (like the station-set rule) hide the actual business logic
- **Untestable contracts:** Prose-only documentation that isn't wired into assertions; easily drifts from implementation

## Related Concepts

- [[write-audit-publish]] — the deployment pattern that gates on contract assertions
- [[agents-in-data-engineering]] — contracts are the specification language for agent-written pipelines
- [[correctness-layer]] — contracts are the boundary between probabilistic agent design and deterministic validation
- [Feature Lists](feature-lists.md) — the general-purpose harness version of the same idea: an executable spec (contract / verification command) gates a state transition (publish / passing) that the agent cannot grant itself
