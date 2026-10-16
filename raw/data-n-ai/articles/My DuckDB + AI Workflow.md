---
title: "My DuckDB + AI Workflow"
source: "https://thefulldatastack.substack.com/p/my-duckdb-ai-workflow"
author:
  - "[[Hoyt Emerson]]"
published: 2026-09-13
created: 2026-10-16
description: "Tips and tricks I’ve learned over the last year"
tags:
  - "clippings"
---
![](https://substackcdn.com/image/fetch/$s_!JiwL!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F76c12552-ad89-4c19-ab57-563b3bb4ee09_3089x2048.png)

### But First…Some Ranting

I personally don’t read any articles about people’s AI workflows. I admit it’s a known growth strategy to write about it, and I’m not hating on people for going that route. But I’ve been using AI in all kinds of work, from coding to content, for the last year, and I think it’s generally useless to copy someone else’s workflow. Why do I think this? Because I don’t think it will work for you. Meaning, I don’t think replicating someone else’s AI workflow will give you the results you want. It won’t “be you”.

AI is not code. It’s not as simple as “copy my prompt to become a data engineer”. The act of building things with AI is an artistic process. It is cerebral, not programmatic, regardless of the amount of deterministic code creating the harness around it. No matter how much someone shows you EXACTLY how they use AI, it does not mean it will work for you.

This is similar to how music production works. There are a ton of tools to use in electronic music production, for example. You can get on YouTube and watch a famous music producer show you EXACTLY how they wrote, edited, and mixed one of their songs. They can show you the exact settings of their compressors, the exact reasoning behind the chord progression, and the exact way they mixed the bass in. It’s all right there for you to see.

I mean…you can [watch Disclosure take you step by step](https://youtu.be/u-0Q41XB7U4?si=bF63xKvnBkMzmk0_) through how they wrote and produced the song Latch.

![](https://substackcdn.com/image/fetch/$s_!1MO1!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a31baf6-8c5c-47d4-bed3-0b029ab68ae9_800x451.gif)

But if you sat down and tried to recreate that song, you’d fall flat on your face. That’s because it’s less about the tools or the workflow and more about your own ability to get an idea from zero to one. If you don’t understand what you want, if you don’t have a clear vision, then it doesn’t matter what your workflow is.

Now, where I do find value is in learning tips and tricks that people have learned. These are small morsels of knowledge that can be more easily adopted into your creative process. And make no mistake: using AI is a creative process. Data, whether you realized it or not, was always a creative process.

---

### How I am Currently Using AI

Getting back to the crux of this article, I want to share what I’ve learned over the last year as I’ve tried to incorporate AI into my workflows. I have, essentially, two different workflows: one for web/software development and the other for analytics and research.

For web/software development, I’m in Cursor with a Pro subscription. I’m still using the traditional IDE UI at the moment. I use this to update my [company website](https://www.earlysignal.tech/), build out data tech tools like [parkbench](https://github.com/early-signal-tech/parkbench) and [fletch](https://github.com/early-signal-tech/fletch), and work on examples [I put together for my technical content](https://github.com/early-signal-tech/postgres-ducklake-sync).

For analytics, I was originally in Cursor all the time but eventually pulled the trigger on a Claude Pro subscription so I could try Claude Code. Over the last six months, since getting Claude Code, I’ve completely overhauled how I do things.

At a high level, here is a list of my most important findings:

1. Smaller “cheap” models work just fine for data analysis and research
2. MCPs are for when you need to interact directly with a SaaS platform
3. CLI tools are essentially localized MCP servers: tool calls on your computer without the need for direct MCP calls.
4. For analytics, I don’t find skill files to be all that useful
5. Almost everything you do can be done in a terminal
6. Command-line text editors like ‘nano’ are incredibly powerful
7. Upgrading from your default system terminal to something like Ghostty is a necessity
8. Semantic layers add marginal gains when using clean gold layer tables.

This is where you’d see a video of me going over my top DuckDB + AI tips if you were a subscriber! Come join and enjoy the video with the article.

---

### Why DuckDB and AI Specifically

My goodness, the conversations being had right now about semantic and context layers. Usually, these conversations are working with some enterprise-type use case where you apparently have hundreds of Postgres tables, PDF files, and CSVs all sitting in random places.

While I can obviously see this exact scenario happening at a number of large companies, it’s not what 99% of the use cases actually involve.

One thing that has improved over the last decade of the “modern data stack” has been the understanding from data professionals that getting better data models upstream means way less headaches downstream. So while some people are stuck having to figure out how to create a semantic model that incorporates the CEO’s voicemail transcriptions, the majority of us have clean gold layer data to work with.

And that gold layer is what unlocks AI’s potential. Without pulling out the silly buzzword “loop engineering,” the reality is that what you want to offer an agent is access to the tools it needs to get its job done as quickly as possible. This is what the MCP architecture was meant to solve initially. It gave your agent a set of tools to answer questions from the local UI.

Here’s the funny thing about DuckDB. It is, by its nature, an analytical environment filled with all the tools you need to quickly run analytics on data. And the absolute easiest access point is the DuckDB CLI. This is where commands can be run on data to get all kinds of information quickly. Agents understand DuckDB very well, and they understand DuckDB’s CLI commands. Without the need of any behemoth, overpriced red or blue colored data platform, you can call analytical tools quickly on your local computer to read from a file, Postgres table or cloud storage bucket at breakneck speed. DuckDB is already set up to easily read from all these sources and pass the result along to your agent.

![](https://substackcdn.com/image/fetch/$s_!Uo_H!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2ea684ca-ee95-42ae-bc20-efd4da62c5ef_625x417.jpeg)

The biggest win I have seen with AI leveraging DuckDB CLI commands is the almost complete absence of hallucinations. Yes, hallucinations have come down a lot with new models. But I don’t like to use new models because I’m cheap and practical. I like my two-year-old Haiku model that is quick and solid.

Even still, Haiku understands what to do with DuckDB and how best to analyze datasets with it. This isn’t a situation where AI is writing Python files. I find creating those types of artifacts unnecessary, especially when doing exploratory data analysis. Python files are also where hallucinations are more prone to happen.

---

### And Now, It’s Time for the Tips

When I think about offering advice on how to work with AI, I try to encapsulate certain things that I feel haven’t changed and won’t change soon. That is, until the model is literally doing all the work and running our computers for us. It’s hard to imagine a world where that’s happening, but it could literally be around the corner.

With that, I’d like to go over my four tips for using DuckDB + AI.

### 1\. Stay in the Terminal

When I first started using Claude Code, I was using it in Cursor to write scripts. I eventually broke out of Cursor and started opening Claude Code in my default system terminal. I liked being able to have an instance of Claude up on my desktop regardless of whether I had an IDE open or not.

For analytics, I haven’t used any sort of analytical IDE in over a year. I don’t see much need to. When I wanted to query data, I did it in the default system terminal within a DuckDB session. I’ve written [multiple articles](https://thefulldatastack.substack.com/p/duckdb-basics-using-sql-in-the-cli) about how to do all sorts of things within DuckDB’s CLI, and it’s my preferred method to work with DuckDB.

Data people aren’t exposed to a lot of tooling that is more popular with software engineers. You won’t see data analysts having an argument online about Vim vs. Neovim. For most of my career, I never used a terminal beyond running scripts or git commands in an IDE.

In the new world of AI, almost everyone is creating a CLI tool now. Agents love working with them. I have even designed two myself in [parkbench](https://github.com/early-signal-tech/parkbench) and [fletch](https://github.com/early-signal-tech/fletch). Through the process of creating technical content, I have been required to touch the terminal regularly to run scripts and test other tools.

This all led me to realize that I probably should upgrade from my default system terminal. It was time to join the ranks of opinionated X accounts and try out a proper, modern terminal. After getting some opinions from people I respected, I landed on Ghostty.

What Ghostty offered me (that maybe my default terminal could too, but I never tried it) was multiple windows in one terminal session. I first tried this out when DuckDB’s Quack server was announced. I wanted to do a screenshot of me connecting two DuckDB instances to a Quack server all in the same window. What Ghostty offered was the perfect solution.

![](https://substackcdn.com/image/fetch/$s_!E5aJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb189f666-bfc1-4f35-ad32-928734984cf9_3412x2144.png)

Four DuckDB’s running in one terminal

I was getting used to having multiple windows open in a terminal. Ideas started sparking when I opened a window just for the file system and a DuckDB window below it. This allowed me to do something in DuckDB, like export a new file, then quickly check it in the top window.

This essentially mimics what’s going on in an IDE, but I have exactly the two windows I need. The workflow was just faster.

![](https://substackcdn.com/image/fetch/$s_!vDHB!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F50a65701-0ff0-4f9b-a66f-1d64b0e54dea_3396x2002.png)

Doing the manual analytics with the DuckDB interface was great, but there were also times when I wanted to move faster and do something more complicated. Specifically, I had a CSV file with a bunch of X post analytics. This included a column with all the text of my posts. I wanted to do some reporting around how different topics were performing in my posts. This is a historically difficult analysis to do because of the variance in text.

![](https://substackcdn.com/image/fetch/$s_!t-9s!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1777b09a-7c11-492b-820c-8845c72653d2_3418x1996.png)

This is where I started to try out some new things with Claude. I’d been using Claude for code writing, text generation, and research. I still wasn’t sold on the AI + Analytics workflow. For whatever reason, we’re all supposed to feel good about having AI write SQL from the start every time, or worse, write Python code each time you use it to do some basic ad hoc stuff. This was silly, and I didn’t do it.

Coming back to when I created the CLI tools helped me understand that where AI agents thrive is working with those terminal tools. That’s because there is already a set of functions baked into them that keeps an agent focused. It ends up writing SQL, yes, but it iterates using the tool much faster than trying to write an entire script all at once that needs to be debugged. Instead, the agent will loop through the terminal process using a CLI tool much faster and be able to handle the error output quickly behind the scenes while you wait. That realization is what got me to try it out with DuckDB CLI. And these X posts were the perfect experiment.

All I did was open another window in my terminal session, start a Claude instance, and give it a reasonable prompt to work with.

![](https://substackcdn.com/image/fetch/$s_!IloY!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e8c80d1-c4f1-4fe5-80db-557fa3ca72eb_3408x2078.png)

The response comes right there in the Claude terminal, and I normally sanity-check it first. I might even hop back into DuckDB to look at some of the data based on Claude’s insights. If I like it, I’ll ask Claude to save it in the current folder as a markdown file. From there, it becomes context again that I can point it to for more work.

For example, I can have it look at two different analytical readouts it generated and compare them to look for any deeper connections between them. This is something that would easily eat up an hour or two of an analyst’s time, but can be done so quickly with AI and all within the terminal.

It was from that moment I realized how much we’ve over-engineered this experience. When I was trying to use Cursor or another IDE for analytics, I was bringing a bazooka to a knife fight. I now understood that staying in the terminal with DuckDB, Claude, and the local data files was all I needed to get my work done.

---

### 2\. Let AI Do the Annoying Things

When I first started out in analytics, all I learned about was cleaning data. Thinking back on that now, it’s a shame. Cleaning data took up so much time in my day-to-day that it kept me from spending more time understanding the data or getting into the technical nuance of the libraries and code I was writing. I felt like I was “doing something” when I was cleaning data. As it turns out, I was just getting really good at mopping up a mess.

Some of the most annoying things were:

1. Updating data types to reflect column values more appropriately
2. Parsing or trimming string values
3. Dealing with Nulls (either as strings or as NULL values)
4. Concatenating columns into more useful column values
5. All the silly stuff I had to do to a CSV just to get it shaped in a way that could be worked on.

With Claude, this is now simple. And in fact, it’s a tragedy I ever had to worry about this stuff in the past. While I think that AI can be sketchy when writing complicated queries that involve joins and need subject matter expertise, it is absolutely flawless when it comes to cleaning up messy datasets.

You can test this easily by leveraging the workflow I outlined in tip #1.

First, you can copy the classic Penguins dataset from a URL and save it locally as a Parquet using the DuckDB section of your terminal workflow.

```markup
## Note it's not required to specify the (FORMAT PARQUET) at the end
COPY (SELECT * FROM read_csv('https://blobs.duckdb.org/data/penguins.csv')) 
TO '~/Documents/result.parquet' (FORMAT PARQUET);
```

![](https://substackcdn.com/image/fetch/$s_!_rS9!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe774b4c1-c93c-404f-b72d-6387324c3d05_3398x2142.png)

A top-level view of the data shows that there are data types we need to change. The columns that have millimeter measurements shouldn’t be variable characters, for example. Given that we have identified at least a few columns we need to clean up, we can pass a fairly general prompt to Claude to clean this data up and create a new file in our local folder.

![](https://substackcdn.com/image/fetch/$s_!SsKI!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5618f433-a87f-4b35-a47b-90368df48113_3410x2064.png)

And quickly after you have an updated, cleaned dataset you can validate exists in the folder and sanity check immediately with DuckDB.

![](https://substackcdn.com/image/fetch/$s_!B_Ru!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F57493011-f4a6-4519-a4ae-b5c4c9261449_3402x2030.png)

NOTE: We are using Claude here because that’s my preferred agent but any other CLI based harness/agent can be open here in the terminal. Other options include Gemini, Pi, OpenCode, Cursor CLI or Codex CLI.

A slew of annoying things are being handled by AI here that I think will save you time and keep you in your workflow.

1. An initial assessment of the dataset
2. Identifying columns with improper data types
3. Assessing NULL values in the dataset
4. Updating data types for all identified columns
5. Writing the cleaned data to a new file in the local folder

All of that was done in under 10 seconds and allows me to check quickly and keep moving. From there, I could start querying the data myself or asking more questions using Claude about the data.

---

### #3 Authorize Credentials Locally

A special characteristic of using AI with CLI tools locally is that you have the added bonus of being able to authorize using local credentials. DuckDB, specifically, makes this incredibly easy with its built-in secrets manager. I go through DuckDB’s secrets manager in [multiple articles](https://thefulldatastack.substack.com/p/duckdb-basics-importing-data), so click through to get a deeper explainer on this.

The cool part about using the DuckDB CLI is that if you ask AI to use it to perform an action that requires credentials, then DuckDB will automatically look at its own secrets manager first and authorize before moving forward. Doing this removes having AI read your credentials directly. Instead, it just passes the SQL it needs to connect to an S3 bucket or a database. DuckDB handles the rest with local credentials.

This is on display magnificently with a [production-grade DuckLake](https://thefulldatastack.substack.com/p/ducklake-in-production-catalog-storage). In this setup, we have a lakehouse catalog being stored in a managed Postgres service and the data files in S3. Credentials for both are stored locally in the DuckDB secrets manager, and then a third credential is set up to reference both in one. When you ATTACH a DuckLake to your DuckDB session, you will pass the third secret name. This instructs DuckDB to use the secret’s credentials to connect to your S3 and Postgres databases.

This is a good moment to bring up the usefulness of a context file that has important commands for your AI to reference. Since I’m primarily using Claude, I will keep a [CLAUDE.md](http://claude.md/) file in the folder I’m working with for DuckDB and AI. I normally add something about only using DuckDB CLI for analytical tasks (skip trying to use MCPs), as well as important URIs and the ATTACH statement for my production DuckLake that references my local secret to pass to it.

```markup
DuckDB and DuckLake

Authentication secrets are saved locally in DuckDB secrets manager so no need to ask for them.

Use the DuckDB CLI for all analytical and data engineering tasks while in this folder.
This includes anything that DuckDB CLI can do or any task with DuckLake.

Use this to attach my production DuckLake

ATTACH 'ducklake:ducklake_prod' AS my_ducklake;
USE my_ducklake;
```

##### SUB TIP - USE NANO

A sub tip here is that I am using the *[nano](https://www.nano-editor.org/dist/latest/cheatsheet.html)* file editor right in terminal to make simple updates to files like CLAUDE.md. You can update, save and get back to your file system interface without leaving the terminal or opening up a new application.

```markup
## type right into your file system window
nano CLUADE.md
```

![](https://substackcdn.com/image/fetch/$s_!aqVP!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F14ecb772-d7d4-4b56-b927-39ada09b7f89_3414x2064.png)

Update the Claude file right in terminal then save and move on

I will then prompt the AI to read the [CLAUDE.md](http://claude.md/) to get ready to work.

With that small bit of context, we can immediately ask Claude to look at our DuckLake and give us a breakdown of what is in it. You can then have it save it as a markdown file in the local folder as context for other questions. Or you can add it to your [CLAUDE.md](http://claude.md/) file and have it read that again to add it to its memory.

With the information it provides, it lets you do some of your own queries in the DuckDB session above, using Claude.

![](https://substackcdn.com/image/fetch/$s_!KQF2!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F754f6325-38f7-4fd3-ad45-5c5722f10a06_3402x2040.png)

The same thing can be done with all other types of connections that require credentials. The best part about DuckDB’s PERSISTENT SECRETS feature is that it’s a set-it-and-forget-it scenario. You don’t have to worry about setting environment variables each time you start up a terminal session.

---

### #4 Use Multiple Agents for Parallel Jobs

This tip has nothing to do with loop engineering or running 20 agents at once to run a business. I think most of that is wishful thinking and way too expensive to be practical.

What I’m talking about is using more than one agent instance in your terminal so you can ask them all to run different analytical tasks at once. You’d be surprised how much productivity this can offer while still being pretty efficient from a token perspective.

NOTE: DuckDB is limited to being a single process database. Meaning, a single DuckDB database can only allow one connection at a time. A “sub tip” here is that you should work with Parquet or CSV files locally so that you can have multiple DuckDB instances work with the data. When you use multiple agents it will spin up their own DuckDB in memory instance so the data source needs to allow concurrent read and writes.

What I initially like to do is use an instance of Claude to first look at the table I want to analyze and come up with four different analyses that could be done on the data. This gives me a good prompt for each of my other Claudes. Here, I’m having Claude look at a table in my production DuckLake and build out four different analyses.

![](https://substackcdn.com/image/fetch/$s_!fwQi!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa9b4ef8-3222-4a1c-9885-2bbc0447f6ce_3394x1946.png)

You then throw each of those analysis breakdowns into your multiple agents and let them cook in parallel. If you have a set of analysis types you like then it’s worth keeping these in yet another markdown file to reference in the future.

![](https://substackcdn.com/image/fetch/$s_!65dd!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d42c3ac-787b-4a80-b0c8-b05a092a774f_800x419.gif)

The agents are using the DuckDB CLI to read and assess the DuckLake table. Since the catalog for my production DuckLake is in Postgres, it allows for concurrent reads and writes. When you give this analysis to the agents, you have a few options. I like to have them save the analysis in Markdown, but they can also create interactive HTML files that you can open locally to view or publish somewhere else.

![](https://substackcdn.com/image/fetch/$s_!_rxn!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F515382a3-7e88-41e5-9989-fb010c07ab69_2932x1834.png)

UGLY but useful

---

## This was Really Cool, So What’s Next?

I will keep writing about AI where it’s useful. I just recently went in depth in how I used [AI to build out data pipelines for a production DuckLake](https://thefulldatastack.substack.com/p/ducklake-in-production-pipelines). This isn’t a Substack that centers on AI but instead centers on tools and AI is just another tool. For now…

---

![](https://substackcdn.com/image/fetch/$s_!ZzA1!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15ea4386-27a1-449e-b66a-4a6c8f766693_1456x364.webp)

Hi, my name is Hoyt. I’ve spent different lives in Marketing, Data Science and Data Product Management. Other than this Substack, I am the founder of [Early Signal](https://www.earlysignal.tech/). I help data tech startups build authentic connections with technical audiences through bespoke technical content and intentional distribution. Are you an early stage start up or solopreneur wanting to get creative with your technical content and distribution strategy? [Let’s talk](https://www.earlysignal.tech/contact)!