---
title: "DuckDB's agent moment (Jordan Tigani)"
source: "https://roundup.getdbt.com/p/duckdbs-agent-moment-jordan-tigani?utm_source=tldrdata"
author:
  - "[[Dan Poppy]]"
published: 2026-06-18
created: 2026-07-23
description: "The database built for your laptop turns out to be one built for your agents. MotherDuck Founder and CEO Jordan Tigani explains why."
tags:
  - "clippings"
---
### The database built for your laptop turns out to be one built for your agents. MotherDuck Founder and CEO Jordan Tigani explains why.

***Season 9 of The Analytics Engineering Podcast is here.** The theme this season is Analytics × Agents. We want to explore what changes when agents become the ones querying, building, and maintaining data systems. Motherduck Founder and CEO Jordan Tigani is a great guest to kick it off.*

Jordan spent 11 years at Google building [BigQuery](https://cloud.google.com/bigquery), one of the largest distributed data warehouses on the planet. Then he left to bet on the opposite idea: that most data isn’t big, and most workloads don’t need a distributed system at all. Or as he wrote in 2023: [Big Data is Dead](https://motherduck.com/blog/big-data-is-dead/).

[DuckDB](https://duckdb.org/) runs locally, starts instantly, and installs itself. The same properties that make it great for a cell in a Jupyter notebook make it great for a swarm of agents branching, querying, and throwing away work hundreds of times a second. Jordan’s company [MotherDuck](https://motherduck.com/) is the cloud data warehouse built on top of it. He talks with Tristan about why this architecture suddenly fits the moment.

This is Jordan’s second time on the show. The last time he was just getting MotherDuck off the ground and, in his words, still trying to figure out what the hell they were doing. This time around he gets into the unusually high-trust relationship between MotherDuck and [DuckDB](https://duckdb.org/), why MotherDuck is faster and cheaper than the incumbents, how data lakes and [Iceberg](https://iceberg.apache.org/) pull DuckDB into more and more architectures, and the big one for Season 9: what agents want from an analytical database.

*Please reach out at podcast@dbtlabs.com for questions, comments, and guest suggestions.*

---

**The agenda for dbt Summit 2026 is live.** Dozens of sessions across analytics engineering, AI-ready data, agentic workflows, and enterprise scale, September 15-18 at The Cosmopolitan in Las Vegas. dbt Summit is the world's largest gathering of dbt users. Level up and start building your schedule: [Explore the sessions](https://www.getdbt.com/dbt-summit/sessions/?utm_medium=social&utm_source=substack&utm_campaign=q2-2027_dbt-summit-2026_aw&utm_content=dbt-summit____&utm_term=all_all__).

---

**Listen now:** [Spotify](https://open.spotify.com/show/4BKMMeVXk4jJnAQSqGSJvE) · [Apple Podcasts](https://podcasts.apple.com/us/podcast/the-analytics-engineering-podcast/id1574755368) · [YouTube](https://www.youtube.com/playlist?list=PL0QYlrC86xQm83Q9deiy4euEnbw8ceu3I) · [Amazon Music](https://music.amazon.com/podcasts/333fe811-1b14-499c-b609-9bfb8f06d1ae/the-analytics-engineering-podcast) · [RSS](https://analyticsengineeringroundup.libsyn.com/rss)

![](https://www.youtube.com/watch?v=p45UPCTBW_c)

---

## Three ideas from the episode

1. **Why “small data” aged well.** Data size and compute size are two different axes. Most workloads are small-data, small-compute or big-data, small-compute, and that’s where DuckDB wins.
2. **Why local-first is an agent feature.** Agents want their own environment and software they can install. A database that lives locally and graduates to the cloud by changing one string is built for that world.
3. **What an “agent swarm” for data management is.** Always-on agents handling the long list of small jobs: profiling columns, running evals, curating context, flagging the weird number before a human ever sees it.

## Key takeaways

*Lightly edited for clarity.*

### Tristan Handy: You reached out to DuckLabs to build a SaaS service. They said no, but partner with us. How does that work?

**Jordan Tigani:** When we started, it was the recognition that DuckDB is amazing. It’s really well done, these people know what they’re doing, and it’s going places. I reached out to Hannes and Mark, the co-founders of DuckLabs, to see if they’d hire me to build a SaaS service out of it. They said no, we want to just focus on the database, but we’d partner with you.

So rather than saying thanks for building an awesome open source project, now we’re going to go make a bunch of money on it, we wanted to be good partners and good stewards of open source. We gave them a co-founder share of the company, so they were economically incentivized for us to be successful. We funded a lot of development in DuckDB, and they built a lot of custom features just for MotherDuck.

We could have hashed out a highly litigated, legalese development agreement. Or we could just say, look, none of this is going to work unless we trust each other. So we chose to trust each other. I like hanging out with Mark and Hannes. I think they’re good guys.

### Where’s the line between what goes into DuckDB and what you build?

There isn’t one that’s clearly written down. The obvious one is that we’re building a hosted service and they’re not. From an open-source business model, SaaS is the cleanest one to me: you pay us to run this in the cloud. You could do it yourself, but it’d be a lot more work.

DuckDB right now doesn’t have any concept of users. There’s no real grant statement. So if you’re going to run a data warehouse in a meaningfully sized organization, it’s not quite suitable yet. That’s the stuff we’re adding: SSO, authorization, all the things you’d need to build a real data warehouse.

They just launched something they call [Quack](https://motherduck.com/blog/duckdb-client-server/), a service you can stand up on EC2 and connect to from anywhere over HTTP. I think it’s actually great for us, because a bunch of people are going to try that and then realize, hey, I need users, I need auth, I need backups, and then we can step in. They gave us a big head start, and if we can’t win with a head start that big, then we’ve done something meaningfully wrong.

### You’re making big claims about speed and cost. Where do the savings actually come from?

In BigQuery, every query has to go through a lot of hops to get to the thing actually running it. And if your query does anything non-trivial, it goes through more hops, data gets shuffled around the network, and all of that adds latency. The mechanism to build distributed databases adds latency, because they’re designed for throughput.

I remember working on BigQuery and my manager said, “I don’t care if you add a second to every query, because we’re handling giant queries. But if you’re running a dashboard, adding a second means every user sits and waits a second.” That’s really annoying.

What we’ve designed for is latency rather than throughput. The energy in DuckDB has gone into making a great single-node engine instead of a distributed system where all these things can go wrong, so they’ve been able to build a super fast engine.

Our median query time is about three milliseconds. If you look at [ClickBench](https://benchmark.clickhouse.com/), our standard instance at $2.40 an hour is something like five times faster than the Snowflake 2XL, which is $64 an hour. And that’s not our benchmark, it’s ClickHouse’s.

### “Big Data is Dead“ came out three years ago. Does it still hold up?

There are two independent axes of scale. There’s the size of data you have, and clearly some people have petabytes, so to say large data doesn’t exist is just telling people the opposite of what they know. But the other axis is compute size, and just because you have large data doesn’t mean you need large compute.

If you’re looking at the last hour of logs, you might have a petabyte over ten years, but you’re only scanning the most recent stuff, so you don’t need the big compute mechanisms.

The flip side is big compute, small data: your BI tool, where you might have 500 users all slicing the same dashboards. The data is small but you need a lot of compute for all those users. Small data and small compute, big data and small compute, small data and big compute, those are probably 97% of cases, and we handle them well.

For the genuine big data, big compute case, [DuckLake](https://ducklake.select/) is our big bet, or [Iceberg](https://iceberg.apache.org/). If your MotherDuck data is a managed DuckLake table, we can give you access to the same files sitting on S3, so you could run it on Spark.

### Are people using DuckDB as one engine on a data lake yet?

We’re seeing more and more of it. For their gold tier, people do want something more compact and managed, so we’ll see them ingesting from Iceberg. But people haven’t quite wrapped their heads around the fact that if you use Iceberg, you give up some things. We had a customer doing millions of single-row updates a day, and that generates all this mess and makes it super slow.

For a lot of smaller customers, the reason they use Iceberg is that there’s excitement and hype around it and they want to give it a try. And one thing they find is the tooling is behind the hype in terms of maturity.

### You wrote that “ETL is highly vibe codable.” Make the case.

We launched our [MCP server](https://github.com/motherduckdb/mcp-server-motherduck) in December, and all of a sudden you could just ask questions in Claude and get answers. The other thing we noticed was that Claude is really good at building data visualizations. The problem was the data it came up with wasn’t updated, hosted, or shareable. So we said, what if we replace the data Claude dumped into a TypeScript file with a SQL query, host it on MotherDuck, and now you basically have a dashboard. That was the root of [Dives](https://motherduck.com/product/dives/).

We started out saying this is not BI, it’s a narrower use case, and then it got harder to draw the line, and we realized we’d stopped using our internal BI tool. We were just using this for everything.

I also talked to someone who’d built a vibe-coded data ingestion solution, and what shocked me was it was running in Claude. They had no front end, no UI. Their whole company was an MCP server. But there’s more to data engineering than building a pipeline, and that’s where it starts to get interesting.

### What do agents want out of an analytical database?

This is exactly what my board asked me at the last meeting: How do you make it so agents use your database versus others? I wish I had a great answer. People have seen the success of [Neon](https://neon.tech/) and [Supabase](https://supabase.com/), and I just spun up a Neon database the other day to interact with agents, because agents need to store data somewhere and Postgres is a great way to do that. Why would you need an analytical database?

That’s a bit more hand-wavy to me, but there will be cases where the agent needs to interact with larger amounts of data, do aggregations, answer harder questions. We have a lot of users building agent platforms on top of MotherDuck. [Airbyte](https://airbyte.com/) just announced their agent platform and it uses us under the covers.

Our architecture is amazing for agents, because if you have a hundred agents that are branching, our tenancy model works really nicely with that. If your agents are hammering Snowflake, that sounds like an incredibly expensive thing to have them do.

### Why is local-first such an advantage in an agent world?

The way we architect working with DuckDB is that our client is DuckDB. If an agent installs DuckDB and does a bunch of stuff locally, you find out quickly that it’s very easy to use all the compute and all the memory on your machine.

Our architecture means the step from local DuckDB to cloud MotherDuck is just changing the name of your database. If the name starts with `md:`, it runs in the cloud. If it doesn’t, it runs locally. You don’t have to install anything differently. If there are agents doing stuff locally with DuckDB, there’s a great graduation case: this is too slow, it’s pulling everything down locally, let’s just push it off into MotherDuck.

### What does an “agent swarm for data management” look like?

I wrote [Water-Town](https://motherduck.com/blog/water-town-agent-swarm-data-stack/) as a takeoff on Steve Yegge’s Gastown. The idea is that as your data comes in, there are agents that do quality control and run evals that detect when something is goofy.

I was talking to someone at OpenAI about how they deal with context, and for core concepts they turn their context into evals. When I say revenue, here’s the calculation. These two tables should be joinable one to one. They have evals for all of those, so you always get the same number, and that’s operationalizable by an agent.

Then there are agents that add their own context: this field is always a capitalized U.S. state name. And agents that look at chat transcripts. When I talk to Claude I’ll say I want to know what’s happening with our paying users, and what that means is they’re in the capacity, business, or light plan. I just gave the agent information that can be captured, so the next time someone asks about paying users, it knows.

Anthropic calls this “dreaming,” taking memory and distilling it into what’s active memory, which is a cool name.

### Where does all of this leave cost?

There’s Jevons paradox, where when something gets less expensive you find more stuff to do with it. We can make analytics dramatically less expensive and move more of it locally, but people will find more ways to keep their bill similar or even higher. The good part is you’re adding value. You won’t have a human trying to debug why a dashboard is showing a weird number, because the agent will have flagged it well in advance. Or you can just ask the agent where the number came from, and it’ll look at your pipelines and show what’s going on.

## Chapters

00:00:00 — Why DuckDB is having an agent moment  
00:01:08 — Reintroducing Jordan and MotherDuck  
00:03:10 — The MotherDuck and DuckLabs relationship  
00:06:50 — Where the line gets drawn: what goes into DuckDB vs. MotherDuck  
00:09:44 — Quack, users, and the enterprise layer MotherDuck builds on top  
00:11:05 — How widely is DuckDB actually used?  
00:13:25 — Who uses MotherDuck, and what they migrate from  
00:14:41 — Hyper-tenancy and read scaling for application analytics  
00:18:05 — Why it’s faster and cheaper: latency vs. throughput  
00:21:35 — “Big Data is Dead,” revisited: the three data/compute quadrants  
00:25:45 — Iceberg, Duck Lake, and DuckDB as one engine on the lake  
00:31:19 — “ETL is highly vibe codable”: the Future Casting post  
00:32:36 — Tristan pushes back (the quote of the season)  
00:35:00 — From MCP server to Dives  
00:38:35 — What do agents actually want from an analytical database?  
00:41:37 — Two kinds of agents: the analyst and the business-process owner  
00:43:09 — The local-first advantage: brew install bigquery is not a thing  
00:46:02 — The agent swarm and “Water Town”  
00:52:06 — A thousand data analysts, Jevons paradox, and the cost of inference  
00:54:53 — Wrap-up

---

*This newsletter is sponsored by dbt Labs. Discover why more than 80,000 data teams use dbt to accelerate their data development.*