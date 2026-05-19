---
title: "The Modern Data Stack is Overcomplicated: Data Ingestion"
source: "https://lukewhittaker.substack.com/p/the-modern-data-stack-is-overcomplicated-5ff?utm_source=tldrdata"
author:
  - "[[Luke Whittaker]]"
published: 2026-05-13
created: 2026-05-19
description: "Getting data from A to B shouldn't be a full-time job. Part 2 of a 10 part series exploring every layer of a modern data stack, and the trade-offs nobody talks about."
tags:
  - "clippings"
---
On paper, you’d think that data ingestion is the simplest problem in the data stack.

You have data at point A. You need to move it over to point B, you move it.

That’s it, job completed!

Yet, ingestion is where I’ve seen more data platforms quietly fall apart than anywhere else. Not in some catastrophic business ending way, more in slow grinding ways, that come back to bite you down the line. Connectors that silently drop columns, schemas that drift overnight. Then there are cases APIs change on Tuesday leaving your dashboards broken by Wednesday. A “real-time” streaming setup that costs more than the analytics it powers.

The decisions you make here look small at the time. They soon compound.

This post is about the three main approaches to ingestion you are likely to face in the early stages of building a data stack, what each one is actually like to live with, and the costs - not just the financials - that nobody seems to mention until you’re knee deep.

---

## To Self-host or Vendor Managed?

Most ingestion problems can be solved by one of three approaches. Most real platforms end up using a mix of all three, even when they don’t mean to.

### Managed Connectors

**The promise**: pre-built connectors for hundreds of sources, maintained by a third party, setup in an afternoon.

**The reality**: it depends entirely on which connector you’re using.

Integrations like Shopify, Stripe, NetSuite, and other big SaaS platforms, tend to work very well, these connectors are stress tested, properly maintained, and you can genuinely set these up in an afternoon or sooner. This is where your managed connectors fully earn their reputations.

Now the story is slightly different for less popular sources, which can often times be less reliable, less maintained, and more likely to break in some interesting ways. I’ve spent more time than I’d like debugging a connector that worked fine in development but quietly failed on edge cases in production.

The Fivetran vs Airbyte (other companies available) question often seems to come up time and time again. How I see these tools, in their own right they are great tools, but they are solving slightly different problems:

- **Fivetran** is the polished, reliable, and quite an expensive option. It is definitely a tool you setup once and fully take for granted because it “just works”, unfortunately this does come with a premium price tag.
- **Airbyte** is open-source, flexible, and significantly cheaper at volume, even considering Airbyte cloud their managed version. With this you will find some quality variable with the non-Airbyte approved connectors found on their marketplace

**Good for**: standard SaaS sources where you don’t want to maintain API integrations yourself.

**Watch out for**: less popular connectors, price changes, and false sense of security that comes with “managed”

### Event Streaming

**The promise**: real-time data, decoupled producers and consumers, infinitely scalable.

**The reality**: all of that is true, but the bar to justify it is higher than most people realise.

I’ve worked with Kafka extensively. When you need it, nothing else quite comes close. Event-driven architectures, high-volume transactional data, systems that need to react to changes in milliseconds, then Kafka is your best bet.

The problem lies in that “real-time” phrase. This sounds great in a planning meeting, and then someone proposes using Kafka for a source that updates once a day. The infrastructure cost isn’t huge, but the technical overhead on a small team is real. You now need to think about topics, partitions, consumer groups, schema registries, dead letter queues, and a dozen other things that don’t matter if you’re moving data in batches.

Managed Kafka, like Confluent, is almost always the right call for a small team. Self-hosted Kafka is a full-time job in itself, so unless you have specific requirements, you don’t want that someone to be you.

**Good for**: high-volume operational data, event-driven systems, anywhere you genuinely need sub-second latency downstream.

**Watch out for**: The operational overhead, and using it because it sounds cool rather than actually needing it. This will outlast the initial enthusiasm.

### Custom Pipelines

**The promise**: total control, fits any source, no vendor dependency.

**The reality**: you own every bug, every edge case, every retry, and every schema change. Forever.

This is the option nobody puts on their architecture diagram but everyone ends up running. The niche API that no connector supports. The legacy system that outputs data in a weird format.

Custom pipelines have a quiet honesty to them. There’s no vendor to blame when things break, it’s just code that you wrote, doing what you told it to do. That may sound bad, but this has some advantages. You know exactly how it works, when issues inevitably arise, you know exactly how to fix them.

The trap is treating custom pipelines as “free” because there’s no license fee. Trust me they are not! Cost comes in the form of your time - building, testing, monitoring, maintaining, and eventually rebuilding when the original author leaves and nobody documented it.

**Good for**: niche or legacy sources, anything where managed connectors don’t exist or don’t work properly

**Watch out for:** accumulating dozens of half-maintained scripts that nobody fully understands. Custom pipelines need the same discipline as any other production system - tests, monitoring, documentation, retry logic. Ignore these and you introduce technical debt.

---

### The Hybrid Reality

In practice, almost every data platform uses a mix of these three approaches. It’s not a failure of architecture, it’s the right answer (at least in my opinion).

A reasonable split might look like:

- **Managed connectors** for your standard SaaS sources, CRM, Finance, Marketing. These are commodity integrations, there’s no need to reinvent the wheel here
- **Event streaming** for high-volume operational data where latency genuinely matters, order events, user activity.
- **Custom pipelines** for those niche APIs and legacy sources

When I looked at our own ingestion layer, the split looks pretty much like that. Managed connectors handle the brunt of the work, we consume Kafka events for the high-volume transactional data from our core systems. We have custom built connectors in AWS-CDK (you could use Terraform) pipelines for sources where nothing else made sense.

The lesson isn’t to “pick one approach”, it’s to pick the right approach that allows you to cut the time barrier from consuming data to insight.

---

### The Hidden Costs

Most posts you read about the ingestion layer tend to stay fairly surface level and only speak about the tools, maybe show some architectural diagrams and call it a day.

Cost to a start-up/scale up company is where the ingestion decision can either drive your team forward or become that uncomfortable anchor down the road, and not just the cost of the tool, the real cost is more layered than that.

#### The Obvious Costs

These are the costs that are clear as day to see on company pricing pages or sales conversations.

- **Fivetran’s row based pricing**: on the small scale is reasonable until your volume usage becomes high. This means it’s easy to forecast in year one, but as you grow forecasting spend becomes a job in itself.
- **Confluent’s cloud pricing/throughput based pricing**: pay for what you stream. Predictable, but can add up quickly with high volumes.
- **Lambda per-invocations pricing**: Cheap for small jobs. Pricey when someone configures a pipeline to poll an API every minute and nobody notices for six months.
- **Compute at the warehouse**: where your data actually lands. This is often forgot about in ingestion conversations, but can be a significant chunk of your spend if too misconfigured.

These are the ones that are easy to model!

#### The Hidden Costs

**Engineering time**: this is the big one. “Free” open-source tools aren’t free, they’ll cost you setup time, ongoing maintenance, and engineering time you spend debugging a connector instead of prioritising higher-value work. A custom Lambda is cheap to run but expensive to build properly and maintain, with testing, monitoring, documentation, and observability all eating in to the time your team could be utilised elsewhere. If you don’t factor this time in, this can catch you out down the line.

**Connector churn**: when a self-managed connector breaks after an API change, one or more team members sprints get derailed. The fix might be simple e.g. a misconfiguration or edge case that was missed. The real cost here is the time it took to find out the root cause, and then there’s the stakeholder trust that is lost.

**Schema drift**: silent column additions, data type changes, fields randomly disappearing. Managed connectors will often handle these for you. Custom pipelines will only capture the data you planned for. The cost here is the broken models and bad data flowing downstream before anyone notices.

**Over engineering**: running an event-driven architecture for data that only updates a sales dashboard daily. Starting here from day one is only going to create bottleneck after bottleneck. This might feel like the right decision because stakeholders want “real-time analytics” but what they really mean is “When I do eventually get round to looking at the dashboard, I want the dashboard to have the most recent data”. So if they are only viewing this dashboard every morning at 9 a.m, batch is the clear winner.

#### How To Weigh Up Cost?

In my opinion cost should not come down to “what is cheapest”, of course no one wants to spend £1million+ on data tools. It's more: with the resources I have at my disposal, how can we efficiently bring data into our central data store, and free up the team to prioritise value-driving work.

So what would a one data engineer team vs a ten data engineer team be thinking?

A solo data engineer should lean more heavily into managed connectors, even if the initial cost to onboard might seem relatively high. The time saved by not building connectors, and instead focusing on modelling data to help your Analysts drive deeper insights, far outweighs the license fee - and could translate to 2-5x revenue growth.

A team of ten data engineers with strong platform engineering experience has the freedom to absorb the complexity of building custom pipelines - they're large enough to sustain the maintenance burden that a smaller team simply couldn't.

At a certain scale, even managed connectors can become financially unviable, and bringing connectors in-house is the right thing to do, but this scale is much higher than most people assume.

Mistakes I see/hear often is teams optimising for the wrong cost. Either obsessing over license fees (guilty of this myself in the past) while ignoring the engineering time they’re burning, or diving straight into building everything themselves without evaluating what that actually means.

---

### How To Decide?

So we’ve spoken about the costs, and where one path or another leads you 6+ months down the line. All of this means nothing without a way to objectively evaluate what approach is the best fit.

Here’s a framework I use to help me decide which approach will fit my use case.

#### What’s the source?

- Standard SaaS platform with a well supported connector → managed connector
- High volume data where low-latency really matters → event streaming
- Niche, legacy, or this connector will not be on the Vendors roadmap for the next 12+ months → custom pipeline

#### What latency do you actually need?

- Daily batch is fine for 95% of analytics use cases - here I’m looking for if my use case sits in the 5%
- Hourly is a reasonable middle ground to get the “real-time” feel
- Genuine sub-minute latency, streaming it is

#### How big is your team?

- solo or small team → lean more on managed connectors
- Larger team → have more of a hybrid set up

If none of these point you to a clear answer then you are likely overthinking. Always start off from the simplest option that meets your actual requirements. You can always change/extend this down the line. The cost of building wrong at the start is cheaper down the line than over-engineering and waiting for your business to reach that scale.

---

### Final Thoughts

My view on this is, **what really is the impact I bring to the business as a data engineer**? Personally I don't see that in building data connectors, though I believe this to be a fundamental skill every data engineer should know and be able to do. The real value of a data engineer lies in using data to drive impact across the business. In a start-up or scale-up environment that means staying agile and capturing quick wins - and spending two weeks building a data connector simply isn't a good use of time, personally or commercially.

As a data engineering function, we’ll be measured on the availability, accuracy, and, actionability of the data. So how we move data from Point A to B is less of a worry.

---

### What’s Next?

Now we have data flowing in. Next we need to decide where this data will live.

Part 3 will explore the warehousing layer - Snowflake, Databricks, BigQuery, Redshift, and MotherDuck - and why this decision will shape almost everything downstream. This choice will affect your transformation layer, governance model, cost profile, and even how easy it is to bring onboard AI (yes that buzzword) workloads later.

It’s also the decision people get most emotional about, this should be fun.

If you’ve enjoyed this one and decide to stick around, see you on the next one!