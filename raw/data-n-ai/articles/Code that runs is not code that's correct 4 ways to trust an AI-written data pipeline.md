---
title: "Code that runs is not code that's correct: 4 ways to trust an AI-written data pipeline"
source: "https://motherduck.com/blog/robust-data-pipelines-with-ai/?utm_source=tldrdata"
author:
  - "[[MotherDuck]]"
published: 2026-07-15
created: 2026-07-21
description: "AI pipelines run green and still return wrong numbers. Four habits to turn a one-shot prompt into a data pipeline you can actually trust."
tags:
  - "clippings"
---
Writing a data pipeline with AI has never been easier. You type a prompt, wait a minute, and something that runs shows up. The pipeline is green. The number it returns is... wrong.

Indeed, a pipeline that runs and a pipeline that is correct are two different things, and AI is very good at the first one. Two things work against you.

First, **AI is non-deterministic**. Ask three times, get two different implementations, and the green checkmark won't tell you which one is correct.

Second, often, **AI can't see your data and metadata**. So it guesses: your schema, what counts as a duplicate, what the units are. Those guesses are silent bugs. Again, no error will be seen in the pipeline, just plausible wrong numbers.

In this blog, I'll go over four things I systematically do to turn a lucky one-shot prompt into a pipeline I can actually trust.

Everything here is tool agnostic. I'll be using Claude Code and MotherDuck in the examples, but map it to your stack.

## 1\. Foundations still matter

The old data engineering discipline did not disappear. It matters more now that AI generates so much code that you are not sure is correct.

Here is a one-shot prompt, no MCP connected:

The one-shot prompt

Load NOAA GHCN daily max temperatures for US stations from the public S3 parquet into MotherDuck and tell me the average and hottest max temp.

Nothing in that prompt is wrong. It just trusts the model to know things it cannot see. Here is what comes back:

```python
Copy codecon.execute("""
    CREATE OR REPLACE TABLE daily_tmax_naive AS
    SELECT ID AS station, DATE AS obs_date, DATA_VALUE AS tmax
    FROM read_parquet(
        's3://noaa-ghcn-pds/parquet/by_year/YEAR=2024/ELEMENT=TMAX/*.parquet',
        hive_partitioning = true
    )
    WHERE ID LIKE 'US%'
""")

avg, hottest = con.execute(
    "SELECT ROUND(AVG(tmax), 1), MAX(tmax) FROM daily_tmax_naive"
).fetchone()
print(f"average max temperature: {avg}")     # 179.6
print(f"hottest reading:         {hottest}")  # 8078
```

It runs. It is also one query with everything hardcoded, and it has **3 problems** you would never catch from the green checkmark:

- The data is partitioned per year, but `YEAR=2024` is hardcoded. You can't load another year or reload one, so a trend is impossible. And `CREATE OR REPLACE` wipes the whole table every run. This can be really expensive in compute for larger dataset.
- It reads `DATA_VALUE` as-is. GHCN stores temperature in tenths of a degree, as a plain integer: `151` means 15.1 C, not 151. There is no decimal point to warn you, so the average comes back at 179.6. Roughly the temperature of hell...
- The source ships a quality flag (`Q_FLAG`) on each reading. The naive pipeline keeps the flagged-bad rows, so the "hottest reading" is `8078`, which is 807.8 C, and will pollute any calculation you make.

None of this throws an error.

So what fundamentals go into the prompt? To name a few:

- Parameters, so you can load or reload a specific year.
- Incremental load instead of a full snapshot every run.
- Inspect the data first so you can spot the gotchas like the tenths-of-a-degree trap.

That last one is a good segue to the tip number 2.

## 2\. Give your AI eyes on your data & metadata

Inspecting the data by hand works, but you can hand that job to the agent. Use an MCP for your database. They are common now. I use the [MotherDuck MCP](https://motherduck.com/docs/sql-reference/mcp/) to read the S3 data and inspect it.

I just prompt it to inspect, it runs a few queries, and it figures out what I would have had to find myself: the values are in tenths of a degree, the data is partitioned by year and by element, and there is that `Q_FLAG`.

Now the agent has seen the real data, and the prompt carries the fundamentals. The transform comes out very different:

```
Copy codedef curate_sql(src: str) -> str:
    """Raw GHCN rows -> clean daily_tmax rows. Encodes the contract:
    tenths-of-a-degree -> C, QA filter, parsed date, one row per station/day."""
    return f"""
        SELECT DISTINCT
            ID                              AS station,
            strptime(DATE, '%Y%m%d')::DATE  AS obs_date,
            DATA_VALUE / 10.0               AS value_c,   -- tenths of a degree C
            CAST(YEAR AS INTEGER)           AS year
        FROM {src}
        WHERE Q_FLAG IS NULL                              -- drop QC-failed readings
    """
```

The year is a parameter now, not a constant. Everything that changes between runs is injected from the environment `YEARS`, so backfilling is just a different list:

```
Copy code# everything that changes between runs is injected (tip 1)
YEARS = [y.strip() for y in os.environ.get("YEARS", "2024").split(",") if y.strip()]
```

And the publish is idempotent: clear the year, then insert. Run it twice, the count doesn't move.

```
Copy code# idempotent by year: clear just this year, then insert. re-run -> same state.
con.execute(f"DELETE FROM {TABLE} WHERE year = {int(year)}")
con.execute(f"INSERT INTO {TABLE} BY NAME SELECT * FROM staging")
```

Now that AI can see the data, creating robust unit tests is easy. Because the agent inspected the data, it mocks look-alike rows and tests the real risks. It's important to keep this kind of data local, not leaning on the cloud, so the agent loop stays fast. We already have DuckDB running in process, so the test will be really fast and cheap to run. Here some sample of fixture used for the tests: a tenths-of-a-degree value, a QC-failed reading, and an exact duplicate.

```
Copy code# (station, date, data_value, q_flag, m_flag, s_flag, year)
RAW_ROWS = [
    ("USW0001", "20240101", 151, None, None, "S", 2024),  # good: 151 tenths = 15.1 C
    ("USW0001", "20240101", 151, None, None, "S", 2024),  # exact duplicate -> dedupe
    ("USW0002", "20240101", 560, "X",  None, "S", 2024),  # QC-failed -> dropped
]

def test_tenths_to_celsius():
    con = _staging(duckdb.connect())
    v = con.execute("SELECT value_c FROM staging WHERE station='USW0001'").fetchone()[0]
    assert v == 15.1, f"expected 15.1 C, got {v}"
```

It runs the same SQL the Flight runs, on local DuckDB, no network and ran under a second:

```bash
Copy codeuv run --with duckdb python test_pipeline.py
```

## 3\. Make the goal a contract, not a prompt

This is the hardest one and one of the most important. You are not judging the code. **You are judging the output against a goal you set up front**.

I write the contract first, as a docstring at the top of the flight. It states the end goal, not the steps: what table exists when this is done, what one row means, and every fuzzy term defined exactly.

```
Copy code"""
Table climate_demo.daily_tmax holds QA-passed daily MAXIMUM temperature, in
degrees Celsius, for US weather stations.

  - value_c = DATA_VALUE / 10.0   (GHCN stores tenths of a degree: 151 = 15.1 C)
  - a valid reading has Q_FLAG IS NULL (it passed NOAA's quality checks)
  - obs_date is parsed from the YYYYMMDD string
  - exactly one row per (station, obs_date)
  - idempotent by year: re-running a year replaces just that year

KPI: same-station mean TMAX per year. To measure a trend you MUST hold the
station set fixed. The all-station average is biased by changing coverage over
time (stations get added in colder/higher places), which makes real warming
look like cooling.
"""
```

That last line is the real check. If you want to measure a warming trend across the US, you have to compare the same stations over time. Stations get added over the years, some in cold places, and if you average across all of them you bias the trend.

This sounds exhaustive as a goal, but you can draft this contract with AI and iterate it against the data.

Finally the contract becomes an assertion. This is [Write-Audit-Publish old strategy](https://lakefs.io/blog/data-engineering-patterns-write-audit-publish/): build the result, check it against the contract, publish only if it passes. The range check catches the tenths-of-a-degree bug for free, because a forgotten `/10` puts every reading far outside any real air temperature.

```
Copy codeMIN_C, MAX_C = -90.0, 60.0  # world records are about -89 and +57

def audit(con, table="staging"):
    n, bad_range, nulls = con.execute(f"""
        SELECT COUNT(*),
               COUNT(*) FILTER (WHERE value_c < {MIN_C} OR value_c > {MAX_C}),
               COUNT(*) FILTER (WHERE station IS NULL OR obs_date IS NULL OR value_c IS NULL)
        FROM {table}""").fetchone()
    assert n > 0, "audit: staging is empty"
    assert bad_range == 0, f"audit: {bad_range} readings outside {MIN_C}..{MAX_C} C (units bug?)"
    assert nulls == 0, f"audit: {nulls} rows with null station/date/value"
```

A flight that errors is far better than one that silently loads with wrong numbers. Always fail loudly.

I deploy the same file as a MotherDuck Flight, and the agent runs it, reads `get_flight_logs`, fixes, and retries until the contract passes.

```sql
Copy codeCALL md_run_flight(id := '...', config := MAP {'YEARS': '1984'});
```

Bonus: I asked it to build a [Dive](https://app.motherduck.com/dives/is-the-us-getting-warmer-it-depends-which-294b9a1a-1609-4fdc-be94-2b88af1de610) (a dashboard in pure JavaScript) and deploy it. Even when your job is just to ingest clean data, a chart catches weird things faster than rows do.

As we can see, the average across all US stations drifts down from 18.23 C in 1974 to 17.92 C in 2024 and looks like cooling, because the network grew from about 6,160 to 8,726 sites in colder, higher places. Hold the station set fixed (the 2,652 stations reporting in every year) and the signal flips: 18.16 up to 19.27, about +1.1 C. Same data, opposite conclusions.

## 4\. Package it so it happens every time

All those instructions (parameters, idempotency, eyes on the data first, the contract, local tests) belong in one place. Put them in a markdown skill file: a name, a description, and the rules.

```markdown
Copy code---

name: robust-flight
description: Build a robust MotherDuck Flight - idempotent, backfillable,
tested on real data, gated by a data contract.

---

- Get eyes on the data before writing any transform (MCP: query, list_columns).
- Write the contract first, as a docstring: what table exists, what one row
  means, every fuzzy term defined, the KPI it must compute.
- Foundations: parameterized window, idempotent (delete-window-then-insert),
  incremental by default.
- Make the gnarly logic a pure function and golden-test it locally on DuckDB.
- Write-Audit-Publish: assert the output against the contract, publish only if it passes.
```

Now every new pipeline inherits the same discipline. If you want inspiration, look at the MotherDuck [agent skills repo](https://github.com/motherduckdb/agent-skills). There are a bunch of skills for data work around DuckDB and MotherDuck, and the patterns reuse fine on other stacks.

## Going further

We've covered 4 steps to make your prompt better for data pipelines:

1. Foundations still apply: parameters, incremental load, inspect first.
2. Give the AI eyes on your real data.
3. Make the goal a contract, not a prompt.
4. Package it so it happens every time you write a pipeline.

The final prompt looks like this:

The robust prompt

Build a MotherDuck Flight that curates NOAA GHCN daily max temperatures for US stations into md:climate\_demo.daily\_tmax. ==Before writing any transform, use the MotherDuck MCP to inspect the source on S3: schema, units, null rates, and duplicate keys.== ==Judge the output against a contract, not the code: one row per station and day, value in Celsius (DATA\_VALUE is tenths of a degree), keep only readings that passed QC where Q\_FLAG is null, and the KPI is same-station mean TMAX per year, holding the station set fixed so changing coverage does not bias the trend.== ==Take the year(s) as a parameter so I can backfill any year, make it idempotent by deleting the year then inserting so a re-run is a no-op, and read straight from the public S3 parquet with no download.== ==Factor the transform into a pure SQL function and write golden tests that run on local DuckDB (a tenths-of-a-degree value, a QC-failed row, a duplicate), add a Write-Audit-Publish step that refuses to publish if any reading is outside -90 to 60 C or a key is null, then deploy it, run it, read the logs, and iterate until the audit passes.==

To go further than this, you would create a full "data pipeline agent" that reuses most of the same logic but probably be on server-side and be used through an MCP for easy distribution across your team. This requires much more work, but starting with the tips above is really easy.

In the meantime, I hope it is not too warm on your side of the world during this summer. Stay cool, and keep your `SKILL.md` up to date!