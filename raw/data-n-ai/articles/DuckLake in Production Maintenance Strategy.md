---
title: "DuckLake in Production: Maintenance Strategy"
source: "https://thefulldatastack.substack.com/p/ducklake-in-production-maintenance"
author:
  - "[[Hoyt Emerson]]"
published: 2026-10-06
created: 2026-10-17
description: "Why we need it and what affects it"
tags:
  - "clippings"
---
![](https://substackcdn.com/image/fetch/$s_!WGvc!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe51945ea-d79e-4b28-8d3e-9eb0e5bdd25a_2460x1306.png)

Getting DuckLake “running” is easy, but getting DuckLake *right* requires good architecture. This is the third and final part in a mini-series on building a production-grade DuckLake. This article will get into the maintenance strategy for a well maintained DuckLake.

What affects your maintenance strategy the most and what DuckLake features do we leverage for this? We will break it all down for the use case we’ve been working with.

Let’s get into it!

---

*This article is made in partnership with [MotherDuck](https://motherduck.com/). The cloud data warehouse built for answers, in SQL or natural language. Fast, serverless analytics powered by DuckDB–from production apps to internal insights.*

![](https://substackcdn.com/image/fetch/$s_!m68x!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F42670f6e-b254-461f-b1d0-c23029e391f5_791x221.png)

---

### Why Should You Care About Maintenance

In the first and second articles of this mini-series, we got into what I’d refer to as the “fun stuff” when it comes to a DuckLake, the part everyone wants to work on. Setting up the storage and compute, building pipelines with AI, and data modeling are the things we all know and love.

But if you’re serious about building a production-grade DuckLake, maintenance needs to be on the same list as queries and pipelines.

I would wager that if I were to randomly stop a data professional in the street and ask them about their perspective on data maintenance, I’d get a long, blank stare. I imagine they might respond with something like, “Why should I care about that? I just analyze the data.”

A few years ago, that would have been true. If you were a data analyst, you’d be a consumer of upstream systems that made sure you had exactly what you needed at the right time. It was those upstream roles, like data engineer, that worried about the CAP theorem, idempotency, and schema drift. You were there to get insights, and MAINTENANCE ISN’T YOUR JOB.

Well, I think that era of clear role definitions is on its way out. And if we are being honest, I think that particular role of analyzing data is getting chewed up by the latest AI models. I have, personally, stopped doing analysis on my own. And I was a data analyst/scientist for ten years.

If you are in a small data team, especially, then this will be more acute in your day-to-day. Once your organization gets “Claude Pilled,” you’d better believe that the mess you were able to manage on your private computer to get business questions answered will not hold up against the onslaught of non-technical stakeholders asking every question under the sun about the available data. For that reason alone, we have to make an admission to ourselves as data professionals. We need better governance and maintenance of our data.

Modern data warehouses like BigQuery handle a lot of maintenance in the background for you. However, in the open-source lakehouse world, where you are standing up your own architecture to avoid that vendor lock-in, you are on the hook for these things.

---

### Maintenance Is an Important Part of a Production DuckLake

DuckLake stores its catalog metadata in a database, which creates particular maintenance needs. Specifically, you will eventually want to use “compaction” to reduce the number of Parquet files, clean up old and orphaned data files (untracked in the metadata), and flush the inlined rows to Parquet.

Other lakehouse architectures typically store both data and metadata in files on object storage. Deletes may be represented by delete files, deletion vectors, or log and metadata updates, depending on the format. As metadata and data files accumulate, maintenance may be needed, though query engines use metadata and pruning to limit what they need to inspect.

In DuckLake, the catalog database stores table metadata, including references to data and delete files. A deletion is recorded separately from the original Parquet data, and queries use the catalog’s metadata to find the relevant files and exclude deleted rows. This can simplify metadata management compared with formats that keep much of their metadata in files.

Another novel feature DuckLake leverages is “data inlining.” Small inserts, by default those affecting fewer than 10 rows, are stored directly in tables within the metadata catalog instead of being written to separate Parquet files. This helps avoid the small-file problem. The inlined data remains there until it is flushed to Parquet through a maintenance operation such as `ducklake_flush_inlined_data` or `CHECKPOINT`.

Leveraging the database to keep track of data files you shouldn’t use and to store rows from small INSERTs sets DuckLake apart from other architectures. Given that, how do we build a maintenance strategy for it?

---

### What Affects Your Maintenance Strategy

What your maintenance schedule looks like is determined by a number of things. I’ll briefly go through what I believe are the two most important ones.

#### Your Ingestion Pattern

How you ingest data into DuckLake will dictate a lot. If you stream data to your DuckLake or make very small INSERTs of fewer than 10 rows, then by default you will end up with a lot of inlined data (unless you update these settings). Postgres is incredibly performant, but eventually it will hit scaling issues when reading all the inlined data in your DuckLake. For that reason, we will want to “flush” this data to Parquet.

If you are doing batch writes that append to a DuckLake table and are more than 10 rows, then you won’t need to worry about flushing data. Instead, you will need to think about eventually using compaction to reduce the number of Parquet files in your storage bucket. Ideally, you want a small number of large Parquet files to read from. The fewer files DuckLake needs to traverse for data, the better it can generally perform.

#### Your Time Travel Policy

I’ve [demoed DuckLake’s time travel features](https://thefulldatastack.substack.com/p/tech-review-ducklake-from-parquet) in some of my first articles on DuckLake. The ability to roll back to a previous snapshot of data is incredibly powerful and has use cases beyond disaster recovery. For example, you can use snapshots in a dashboard filter to see how data changed between snapshots or to show commit change messages.

DuckLake allows us to expire snapshots and remove the data files associated with them. However, your ability to time travel is predicated on the data from the original snapshot still being there. If the data files from the initial snapshot are no longer there, then time travel is no longer an option. So, you want to consider how long you’d like to retain that ability with your data.

### How Does This Look in Practice

Let’s look at this through the lens of the use case we set up when we began this mini-series on a production DuckLake.

1. A small data team at an SMB that uses AWS
2. Data needs are simple: daily batch jobs and a relatively small user base
3. On AWS, so using S3
4. Utilizing Supabase as the managed Postgres
5. Users will be given credentials to store locally; they will use DuckDB CLI/UI as an interface and for compute resources.
6. We are re-creating a replica of a Postgres table every morning
7. We are re-creating a gold layer analytics table from the Postgres replica every morning
8. We are using MotherDuck’s Flights to schedule and run these pipelines

### How the Files Look Over Time

In our particular use case, we are recreating a gold layer table in our DuckLake every morning. So we are deleting and recreating the table. This works fine for now because we use our gold layer for analytics and do not need real-time data or all-time data. Until the time it takes to recreate the table becomes prohibitive, it works fine for us.

Let’s first look at the data files that currently represent our gold layer table:

```markup
-- attach ducklake
ATTACH 'ducklake:ducklake.prod' AS my_ducklake;

-- use gold layer schema
USE my_ducklake.gold;

-- check files 
FROM ducklake_list_files;
```

![](https://substackcdn.com/image/fetch/$s_!N1Ck!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9a9cd77-331f-48d4-a09b-30ff47333f3a_1322x482.png)

You’ll see there is just one file showing here, but why? Remember that when we run the pipeline every morning, we recreate the table. This means that we delete the table and then create a new one with the new data. Since we are not appending the data, we end up with just one file for the foreseeable future, since Parquet files can hold very large amounts of data.

We can verify that this is happening by looking at the snapshot history.

```markup
-- look at snapshots for ducklake
SELECT * FROM ducklake_snapshots('my_ducklake');
```

![](https://substackcdn.com/image/fetch/$s_!NJT9!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93019519-4884-4e61-948a-a037bda32104_3406x1004.png)

We have the Postgres replica being recreated, as well as the gold layer table being dropped and then recreated with a new INSERT. This is a good example of how the snapshots themselves explain the history of the table, even though you only see the latest data file in the prior query.

Now, if I look directly at my S3 bucket, I will see a number of Parquet files there.

![](https://substackcdn.com/image/fetch/$s_!FblY!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe7df6b55-08a8-4bc1-942c-2e30c1c5008e_1916x1066.png)

So we have a single data file representing our data, however, we have a large number of snapshots and a large number of Parquets in our S3 storage.

Now let’s go through the two items I listed above that affect the maintenance strategy here.

#### Our ingestion pattern

We have explained what our ingestion pattern is already. We recreate a Postgres replica as well as a gold layer table daily. We end up with a single file representing the data for the current version, but with a number of snapshots and other Parquet files representing the previous versions.

Also, the data we are inserting daily is well above the inlining threshold that DuckLake defaults to. That means we will not have any inlined data when we run these daily batch jobs. So we do not need to flush inlined data for this use case. For a reminder on what flushing looks like or why it would be useful, [read my article on DuckLake’s inlining feature](https://thefulldatastack.substack.com/p/understanding-ducklakes-inlining).

![](https://substackcdn.com/image/fetch/$s_!hXQu!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F30d79e22-ea83-4615-bbf7-798a5d39e521_3840x1518.png)

#### Our Time Travel Policy

The snapshots along with the other Parquet files in S3 allow us to do time travel or rollback depending on what we want from the data. We might want to incorporate a version of the table or data based on snapshot versions. These can be used in a filter of an interface, for example.

The “Policy” we create here is centered around how long we want to give a user access to older snapshots of data. We will give users a 7 day rolling window that will give them 7 days worth of snapshots and data files in case they want to use it for any specific visualizations, filters or ability to rollback data. Older snapshots will be retired and older data files will be deleted.

![](https://substackcdn.com/image/fetch/$s_!Q5nr!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7bc51792-eabe-4486-b0c1-57a86d1ab8e1_3840x1525.png)

### The Commands and Scripts

The first thing we will create is a script that will handle cleaning up snapshots and old data files beyond the time travel window we laid out. Before that, I want to list the different maintenance functions that DuckLake offers.

```markup
- \`ducklake_flush_inlined_data\`
- \`ducklake_expire_snapshots\`
- \`ducklake_merge_adjacent_files\`
- \`ducklake_rewrite_data_files\`
- \`ducklake_cleanup_old_files\`
- \`ducklake_delete_orphaned_files\`
```

A reminder that you can run all of these by using the CHECKPOINT statement. However, I would like to be more à la carte here so we can see how each works with our maintenance strategy. For example, we won’t be using `ducklake_flush_inlined_data` because we have no inlined data.

We will use the `ducklake_expire_snapshots`, `ducklake_cleanup_old_files`, and `ducklake_delete_orphaned_files` functions. These three will do everything our strategy requires based on our criteria above.

We will start by running these functions locally, but remember that we are using MotherDuck’s Flights feature to run the data pipelines. The cool part is that we can also use it to run these commands within a Python file. We won’t get into using Flights in this article because we [covered it in detail in the second article](https://thefulldatastack.substack.com/p/ducklake-in-production-pipelines) in this series.

#### Expiring Snapshots

We’ve been adding data for a number of days, which has led to snapshots being created each time. Above, we read the snapshots metadata table and could see that we had snapshots going all the way back to the previous month.

These maintenance functions have a parameter called `dry_run`, which allows you to run them without taking any permanent action. A dry run will show you what would happen if you were to run the maintenance function.

For example, before we expire any snapshots, we can first CALL a dry run to see what we have:

```markup
CALL ducklake_expire_snapshots('my_ducklake', dry_run => true, older_than => now());
```

The above will give us a full explanation of all snapshots older than now that would be expired if we were to run this.

Our time travel policy is to offer users a rolling window of seven days of snapshots and data to work with. So we will add `INTERVAL '7 days'` to the `older_than` parameter to expire only snapshots older than seven days from today.

```markup
-- expire all snapshots older than 7 days
CALL ducklake_expire_snapshots('my_ducklake', older_than => now() - INTERVAL '7 days');
```

The output of that CALL is the list of all snapshots that have been retired:

![](https://substackcdn.com/image/fetch/$s_!Hx5t!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31760a98-a1f5-4521-9257-4a7dfc0d94c0_3398x1944.png)

Running the snapshots query again shows us the updated list of snapshots:

```markup
-- look at snapshots for ducklake
SELECT snapshot_id, snapshot_time, changes FROM ducklake_snapshots('my_ducklake') ORDER BY snapshot_id;
```

![](https://substackcdn.com/image/fetch/$s_!jdMe!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F29d0364f-f6d3-47c3-a94c-96fea0443ee1_2558x936.png)

#### Cleaning Up Old Files

We can now do a dry run to see what data files would be cleaned up after these snapshots were retired.

```markup
CALL ducklake_cleanup_old_files ('my_ducklake', dry_run => true, older_than => now() - INTERVAL '1 hour');
```

This query does the following:

1. ‘my\_ducklake’ - the catalog/attached database to operate on.
2. dry\_run => true - don’t actually delete anything from S3. Just return the list of files that would be deleted if you ran it for real (dry\_run => false). Safe to run repeatedly.
3. older\_than => now() - INTERVAL ‘1 hour’ — only consider files whose schedule\_start (the timestamp they were placed in `ducklake_files_scheduled_for_deletion`) is older than one hour ago. This is a safety window. A file only becomes eligible for deletion once it’s been sitting in the “scheduled for deletion” queue longer than this threshold, so an in-flight query that opened against an older snapshot moments ago doesn’t have its file yanked out from under it.

![](https://substackcdn.com/image/fetch/$s_!QZPC!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fab0bd028-3b00-4f43-8950-ecf10124ed6b_2352x1672.png)

The dry run is nice because it lets us see what’s over there in S3 before actually deleting things.

Everything looks correct so let’s permanently delete older data files associated with the expired snapshots. This will permanently remove them from our S3 bucket.

```markup
CALL ducklake_cleanup_old_files('my_ducklake', dry_run => false, older_than => now() - INTERVAL '1 hour');
```

Going back to our S3 bucket we can see we now ONLY have data files for the last 7 days of snapshots.

![](https://substackcdn.com/image/fetch/$s_!MvmB!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F264714d0-0109-4a29-9bf1-cd2868daeeb4_2794x1326.png)

Those two functions can be called by the Python API as well, so we can simply schedule a daily maintenance pipeline in MotherDuck’s Flights to keep our Time Travel policy on track moving forward.

#### Checking for and Deleting Orphaned Files

OK, so there’s this thing called an “orphaned file,” but what is that exactly?

Orphaned files in DuckLake are data files that are no longer tracked by the DuckLake metadata catalog.

For these types of files, the `ducklake_delete_orphaned_files` function is here to delete them. A dry run will tell us whether there are any files first.

```markup
-- dry run read of orphaned files
CALL ducklake_delete_orphaned_files('my_ducklake', dry_run => true);
```

![](https://substackcdn.com/image/fetch/$s_!UPxy!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ebfb1a1-9610-4047-8885-5cc1975c67c9_2342x268.png)

We see here that we do, in fact, have an orphaned file. I didn’t know this existed, so that’s yet another reason why these maintenance functions are so useful.

Let’s clean up this file now:

```markup
-- delete orphaned files
CALL ducklake_delete_orphaned_files('my_ducklake', dry_run => false);

-- check orphaned files again
CALL ducklake_delete_orphaned_files('my_ducklake', dry_run => true);
```

![](https://substackcdn.com/image/fetch/$s_!NMRu!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F43313bab-38fb-4f92-9193-b5a2fd574e87_2340x534.png)

Great, we can see that the orphaned file was deleted and we no longer have random untracked data files. We now have the maintenance routine that will keep our snapshots, data files within our time travel window and any orphaned files deleted. For our use case, this is the perfect routine to run each day after the gold layer table is created!

#### How Does it Become Production-Grade?

I spent [all of the last DuckLake article](https://thefulldatastack.substack.com/p/ducklake-in-production-pipelines) going over how to use [MotherDuck’s Flights](https://motherduck.com/product/flights/?utm_term=motherduck%20flights&utm_campaign=US_Search_Brand&utm_source=adwords&utm_medium=ppc&hsa_acc=6957541599&hsa_cam=23133838754&hsa_grp=203159932027&hsa_ad=824367558910&hsa_src=g&hsa_tgt=kwd-2485832040947&hsa_kw=motherduck%20flights&hsa_mt=p&hsa_net=adwords&hsa_ver=3&gad_source=1&gad_campaignid=23133838754&gbraid=0AAAAApg_UmAczVRp1JQHw85H2Wwtnf4W9&gclid=CjwKCAjwlY3WBhANEiwApsNrLREqgXH8yXxQ-aPCilAsuOI4aHGnkVg2T3nyF08a0n85OK7zpTjX4RoCv2UQAvD_BwE) feature so I won’t repeat that again. But what we would do at this point is take all these commands, pass them to our Agent and tell it to build a MotherDuck Flight Pipeline scheduled for after the gold layer is created everyday. These functions will be ran each day and your DuckLake maintenance is complete.

---

## This was Really Cool, So What’s Next?

This is the FINAL installment of my Production DuckLake mini series and I’m so glad I went through this exercise. If you haven’t yet read any of my other DuckLake or DuckDB articles I have a [full DuckDB/DuckLake learning path page](https://thefulldatastack.substack.com/p/duckdb-learning-path) where you can see them all in order of importance. As far as what comes next, we are going to start to show ways that AI can be used with and incorporated into a DuckLake. I’m very excited about this so stay tuned!

---

![](https://substackcdn.com/image/fetch/$s_!ZzA1!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15ea4386-27a1-449e-b66a-4a6c8f766693_1456x364.webp)

Hi, my name is Hoyt. I’ve spent different lives in Marketing, Data Science and Data Product Management. Other than this Substack, I am the founder of [Early Signal](https://www.earlysignal.tech/). I help data tech startups build authentic connections with technical audiences through bespoke technical content and intentional distribution. Are you an early stage start up or solopreneur wanting to get creative with your technical content and distribution strategy? [Let’s talk](https://www.earlysignal.tech/contact)!