---
title: "7 Crucial Barriers between Data Teams and Self-Healing Data Architecture"
source: "https://dataopsleadership.substack.com/p/7-crucial-barriers-between-data-teams?utm_source=tldrdata"
author:
  - "[[Hugo Lu]]"
published: 2026-06-18
created: 2026-07-23
description: "What Data Teams need to build with AI to make Self-Healing Data Architecture a practical reality"
tags:
  - "clippings"
---
![](https://substackcdn.com/image/fetch/$s_!bXPZ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa78a1738-2f8f-4e39-8cba-cb0d6104d7b7_1920x1280.jpeg)

AI rendering of Self-Healing Data Architecture (?) Photo by SoloTravelGoals on Unsplash

It’s no surprise that the largest companies in the world are building agents to create autonomous architecture. [Genie Zero Ops](https://www.databricks.com/blog/introducing-genie-zeroops) was the worst-kept secret in Databricks Land, but it’s a really exciting development.

Genie Ops has context of everything in Unity Catalog. It is, weirdly, always running. It has access to sandboxes, and tests data and can hotfix it, even waiting for a human in the loop to interact with the results (github, Jira ticket etc.) to allow the loop to be closed.

It’s a very cool piece of kit, but wanting in many ways.

1. Credential Management is not clearly defined
2. It is always on, and therefore control is limited
3. Not obvious how the Skills are defined
4. lacks context of anything outside of Unity - tying you to Unity Catalog “Everything is fine if you have the context” “It’s easy when the data is clean reliable and fresh”
5. Lacks a proper orchestrator / event-based orchestration

Concretely, there are a few barriers to achieving the nirvana of self-healing data architecture and I don’t think we are quite there yet. I wrote these up below. The Databricks announcements corroborate this article quite nicely.

### Introduction

For many data engineers, AI examples of Data Engineering revolve around one thing: fixing pipeline. An engineer opens up claude code, pastes some logs, and a pull request is made.

Semantics are fundamental here. Because when people say “Self-Healing” what they mean is “Self-managing”. The key to success in AI is not defined by manual intervention and interaction — but the absence of it.

The dream for Data Teams is a system whereby Data Pipelines and workflows generally succeed without any human intervention at all. However, there are barriers that lie in between us and this golden future.

Agents require context — fixing a pipeline may be due to a transient error, upstream schema change, or something uncontrollable entirely like a human dropping a table. Experience provides engineering teams with the know-how of how to fix these; context agents are missing.

A shift in mindset will also be apparent. The old pattern of “New branch, merge, re-run” is distinctly *slow* and not *agenty*. Unless we are to change our patterns and allow agents to *merge* PRs as well, this seems like a large mindset shift is required.

Finally, data does not “branch” well. Projects like Lake FS promised to make “Git for data” mainstream, but it is not. I have been writing about [zero-copy cloning](https://medium.com/snowflake/why-snowflakes-clone-command-changes-the-game-for-ci-cd-in-data-ccb6fb9955ba) for years, but it is still not widely used. The distinctions between *code* and *data* are not obvious.

In this article, we’ll cover 7 barriers in between the typical Data Stacks of today and the nirvana of self-healing data pipelines / autonomous data pipelines.

Let’s dive in!

### Barrier 1 | Context and failure recall

Pipelines can fail for a plethora of reasons, and being able to fix pipelines *period* is a requirement for an AI system. We can categorise failures into a few broad types:

- Infrastructure issues
- Code issues
- Data Issues
- Transient or Third Party issues

Generally, the manner of fixing data requires knowledge of the system. For example, Acme’s Kubernetes Cluster may only be accessible by Mr. Bob, who is the only person who has access to Bob’s special access key hidden in AWS Secrets Manager with a non-standard header. AI doesn’t know about Bob’s key, so won’t be able to fix the cluster.

Similarly, Analyst Sophie may know that the right thing to do in Widgets Incorporated is to simply gloss over the fact that sales are reported in multiple currencies, and to manipulate the numbers to be 10% higher than the ones yesterday. AI doesn’t know how to treat the numbers.

AI may also not know that to failure handle the internal API, you simply need to try it again between 2.47am and 3.12am.

These are ridiculous examples, but they illustrate the point that the knowledge to fix these different types of errors often exists within individuals’ heads. It is not enough to speak about “Metadata context”. While gathering lineage, logs, code, documentation, and other *written-down* context is undoubtedly imperative, AI is actually pretty good at *just working it out*.

As Data Folks, we’ve all been in a situation where we (Or perhaps someone we’ve spoken to) has thought:

> “How on earth could I have known that?”

At the end of the day, only humans know where the bodies are buried.

![](https://substackcdn.com/image/fetch/$s_!OmYS!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F05d80865-f1dc-4261-94d4-2a930d3c58b5_600x361.jpeg)

This entire structure is tech debt and could be broken down with AI. Source

### Barrier 2 | Elastic infrastructure

Considering issues of the infrastructure type specifically, I am coining a term “Elastic” infrastructure. “Elastic Infrastructure” does not just scale, but also has an API to manage it.

An EC2 instance would not be elastic, as it does not scale beyond a certain point.

A Kubernetes cluster on a locked-down machine would not be elastic w.r.t cloud as there would be no API to be managed.

The reason is that AI will require access to Infrastructure in order to recover failures from it.

SaaS providers should relish this opportunity. SAAS providers necessarily take the management burden of infrastructure from Data Teams away, for a fee. This is a very AI-friendly approach, but falls down in respect of Barrier 6, which we will get to.

### Barrier 3 | Operational Agents and Quality Data

Pete in Finance has overwritten the Supply and Operations Planning Google Sheet for the US again. The international forecasts are broken, and your pipeline is failing. There are 0 rows in `us_forecast_dec_v1` and `forecasts_agg` is stale.

AI is telling you the connectors are fine but there was no data. It can’t do anything.

What is the solution here? Let’s play a quiz. I’ll give you some ideas, and you pick the right answer.

- **Option 1:** let AI hallucinate the forecasts
- **Option 2:** let AI hallucinate the forecasts in your data warehouse, and re-run the Google Sheet Pipeline Later
- **Option 3**: AI Tells Pete to upload the damn forecasts!
- **Option 4**: there is a warm pool of [rented humans](https://rentahuman.ai/). When this type of pipeline fails, the AI instructs the warm pool to bother Pete *in person* until he fixes the pipeline himself, by hand

Of course, there is no right answer! All options are not great, ranging from bad to ludicrous. In fact, Option 4 doesn’t really require AI at all, but something called Teamwork.

Quality Data is as ever, the most important thing for a data engineer. Data Teams should ask this question when they interview more “How good is your data?”. It is such a determinant of Quality of Life, it is surprising not to get more of a mention.

That is not to say that Operational Agents have no place — for example, genuine fat finger errors could easily be corrected by an operational agent. For example, let’s say there is a new deal for $10m — perhaps the correct number is $1m. An agent with a Salesforce API Key could easily amend the data, and restart a pipeline.

### Barrier 4 | Git for Data

The previous example raises an important question, which is “Should AI Agents edit production?”

If you’ve experienced multiple Saleforce environments in your career — I hear your pain. But the feature is designed to avoid the situation above. You see, perhaps the account executive **has** landed a whale deal and it **is** worth $10m. In that case, surely much better for the agent to edit the staging Salesforce instance rather than the Production one?

![](https://substackcdn.com/image/fetch/$s_!4yfN!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3f467760-5c2f-4378-98f2-ef3337e9a78c_1920x1366.png)

Complex Version of how AI can take branching data in git and then you can automatically recover a pipeline

The above is a high-level rendering of what the process using a git-for-data like approach would work. There is a simple version below.

![](https://substackcdn.com/image/fetch/$s_!syaW!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F153f63d2-dce0-4338-bd4d-47fd72c90953_600x305.png)

Simple version of an AI Workflow

In both cases, AI needs a new branch to do its work. That branch needs zero copy clones of the data, it needs a git for data approach, and you need to be able to efficiently “switch in” the data at the end.

![](https://substackcdn.com/image/fetch/$s_!g985!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88e1f469-cbe4-4f97-b3b7-9a3959e348fb_600x218.png)

Simple git for data workflow

Without this structure in place, I struggle to see how AI will be trusted to reliably fix things, without creating a governance nightmare whereby it has write access to production data.

In respect of this, companies like Snowflake are well-positioned as they have supported features like zero-copy cloning for a long time. Motherduck also supports this feature. The clearest winner, though — is iceberg.

Iceberg supports **time travel, rollback, and git for data**. Companies like [Bauplan](https://docs.bauplanlabs.com/concepts/git-for-data) have built compute engines around iceberg, which make for a nice, AI-friendly experience. AI should be a huge catalyst for iceberg.

### Barrier 5 | Pervasion through the industry

Self-Healing Architecture hits a problem when we talk about interoperability.

[Fivetran](https://www.fivetran.com/blog/what-is-open-data-infrastructure) and [dbt](https://www.getdbt.com/blog/what-is-open-data-infrastructure) made a big fuss about open data infrastructure in 2025 — it is not the same thing as *open source data infrastructure*, but rather refers to an approach I think is better called the [Modular Data Architecture](https://towardsdatascience.com/microservices-vs-monolithic-approaches-in-data-8d9d9a064d06/), whereby different functions get different tools.

![](https://substackcdn.com/image/fetch/$s_!8-8V!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff751d4ca-52ac-4266-8e9a-df125ff21f54_600x350.png)

[Another example](https://medium.com/@hugolu87/enterprise-data-architecture-101-aws-snowflake-blueprints-16bb061526c4) below.

![](https://substackcdn.com/image/fetch/$s_!Xya4!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F836d9d24-e7dc-4e09-84b6-bb079ba70033_600x380.png)

Modular Data Architecture. Source

There is no point having a self-healing architecture if the underlying components do not support it. Underlying service providers most provide relevant APIs that support all the tenets of this paper, as well as self-healing functionality themselves for patterns to work.

For example, suppose there is a silent failure in an ELT Provider, whereby the sub-schema changes; the columns and types remain the same, but the values change. Perhaps now there are currencies reported in Yen, as well as in USD, but the two columns `currency` and `local_value` remain.

The right thing to do may be to amend the ELT Job in its staging environment, verify the rest of the pipeline from that staging data, switch out the data that is now correct, and then finally switch over the erroneously succeeding ELT job.

Many ELT tools simply do not provide the APIs to get this functionality. However if you were doing this with a python script you controlled yourself — no problem. This will create massive pressure on the ETL players of today to change their structures or die.

This is a massive barrier in between the modular systems of today and true self-healing autonomous architecture. The only other examples would be for the systems themselves to all become independently self-healing, as you would hope that if all parts of a system are self-healing, then so too is the whole.

### Barrier 6 | Agent Sandboxes and New Orchestrators

The logical place to run Agents that fix things is within an Orchestration Tool.

This is because the Orchestration Tool has a few things the agent needs.

1. The ability to run any code, and to replay any DAG with any sets of arbitrary parameters
2. The connections to the different parts of the system the agent may need (remember, an orchestrator orchestrates, so it has access to things)
3. Alerting built-in, with monitoring, recovery, and scalable infrastructure

However there is one huge enormous problem — and that is security.

Companies like [Cloudflare have built agent sandboxes](https://blog.cloudflare.com/sandbox-ga/). This is because models like Fable ([which was recently banned](https://www.reddit.com/r/ClaudeAI/comments/1u4dij4/megathread_for_us_government_suspension_of_fable/)) need sandboxes, as they can [break out](https://www.anthropic.com/engineering/how-we-contain-claude). This is especially the case when under attack from [prompt injection](https://www.ibm.com/think/topics/prompt-injection).

![](https://substackcdn.com/image/fetch/$s_!j0Ho!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6c3beca-351f-439e-a24a-1a9108b0098b_900x692.png)

The dangers of prompt injection when running AI Agents in the same infrastructure as your legacy Orchestrator

Legacy Orchestration Tools are simply not made to handle agents in this way. The security risks are immense. Not to mention AI workloads could tread on the toes of data ones!

It is quite clear agents will require access to orchestration frameworks. Whether that is Open AI and Anthropic providing an orchestrator, new age orchestrators with agent sandboxes, or some form of interoperability between the two — something has to give here. Because security.

### Barrier 7 | Standards for Proxy Servers and Agent Definition

One approach to security is to set-up a Proxy Sservice for Agents. Rather than install the secrets in the sandbox, the Agent has access to a given number of tools / MCPs.

The Proxy Service is then the only thing that has access to external systems. This means that even if the Agent becomes a victim of a prompt injection attack, all it could do is limited by the endpoints in the MCPs it has access to.

![](https://substackcdn.com/image/fetch/$s_!K9es!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb433975-071b-4917-8438-1a2fca106336_900x521.png)

An illustration of a basic proxy service with an auth server and a credentials DB

What this proxy service needs to look like is not obvious. [MCP is big](https://www.reddit.com/r/mcp/comments/1tle6gl/reducing_context_window_efficiently_in_mcp_heres/). Cloudflare [released Code Mode](https://blog.cloudflare.com/code-mode/). If you need to access multiple different endpoints, how the MCP Servers ought to be configured is not straightforward or obvious.

Open Standards should prevail — any agent looking to interact securely with multiple systems would benefit, from a security perspective, from interactive with a proxy service. These exist today, but in private SaaS tools like [Foundry](https://www.palantir.com/docs/foundry/data-connection/agent-proxy).

Frameworks for designing agents would also need to emerge. In the example above, a single agent requiring integration to hundreds of systems may not be feasible, as the context required to access hundreds of MCPs may be too large.

### Putting all together | Single Pane of Glass for AI

Collectively, achieving the above would allow data teams to build out a single pane of glass for AI.

- **Context**: provides the agents with the information to solve any problem
- **Elastic infrastructure**: provides the foundation for fixing pipelines
- **Quality Data**: eradicates the human side of the data inputs
- **Git for Data**: creates reliability and trust in AI
- **Mass Adoption**: prevents industry collapse
- **Agent Sandboxes and New Orchestrators**: remove legacy architecture
- **Proxy Servers**: do their best to guaranteee security

This single pane of glass would allow AI Agents to operate in a secure way. They would execute when they needed to, and would have the context to achieve what they needed to as well.

Core data primitives like git for data, elastic infrastructure, and support throughout the ecosystem would turn this from a theoretical idea into a practical reality.

Data Teams looking to implement Autonomous architecture will impose significant pressure on existing vendors to support interoperability.

This will exacerbate consolidation, as traditional walled-gardens like Salesforce, SAP, and ServiceNow roll-out their own agentic products and data studios, capable of controlling the end-to-end without providing interoperability.

*It is probably about time you tried [Orchestra](https://app.getorchestra.io/signup).*