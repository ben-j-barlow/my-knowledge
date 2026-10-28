---
title: "[FREE] A file format claims to be 100x faster than Parquet"
source: "https://vutr.substack.com/p/free-a-file-format-claims-to-be-100x?utm_source=tldrdata"
author:
  - "[[Vu Trinh]]"
published: 2026-10-22
created: 2026-10-28
description: "...for random access."
tags:
  - "clippings"
---
> To celebrate reaching 20,000 subscribers, I’m offering **==50% off FOREVER==** ==on the annual plan.==
> 
> Once you claim the offer, the 50% discount will automatically apply to all future renewals.
> 
> You have only **==1 day left==** to claim this offer.
> 
> I couldn’t have achieved this without you guys! Thank you soooo much!

---

![](https://substackcdn.com/image/fetch/$s_!8hiF!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6bce512-e49c-4438-8a55-f8d0d493f703_2000x1429.png)

---

## Intro

Data engineering workloads have evolved.

From historical tabular data for humans to vector embeddings, images, or documents for AI.

From sequential scans, we now also need random access- the one that used to only belong to the “transactional“ world- now is required in our field.

When an AI model needs to perform a semantic search (e.g., find a document or an image), the system performs a random-access read to retrieve a small number of rows.

Parquet wasn't designed for this kind of operation: it works best on sequential data scans, but random access is another story.

—

To fill this gap, new file formats have been introduced.

One of them is Lance, which claims to be 100x faster than Parquet for random access.

In this article, I will discuss Lance's main technical decisions that enable robust random-access performance, as well as other improvements compared to Parquet.

> ***Note**: This article is not sponsored by or affiliated with any organization.*

---

## Parquet

## Revisit

This article will cover some low-level Parquet concepts. So I think it's helpful to revisit Parquet internals here so you don’t have to switch between tabs to search for those concepts.

—

Parquet organizes data in the Partition Attributes Across (PAX) layout, commonly called the hybrid format. It first divides data into “row groups,” each containing a subset of rows (horizontal partition).

![](https://substackcdn.com/image/fetch/$s_!Egzc!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3b72df42-a81d-4d83-a028-3ded66930f4e_856x784.png)

Within each group, it stores values from a column together. Each column is stored in chunks. Each chunk consists of pages, the unit for encoding/decoding and compression/decompression.

> Keep in mind this detail: **page is the smallest unit you can read in Parquet.**

Each page has a header that includes information such as value, definition, and repetition encoding (the latter two are used to handle nested data). The application uses the header to decode and read the actual data.

![](https://substackcdn.com/image/fetch/$s_!LeoA!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2aed45ef-9293-4e23-ade5-3b0755b41d57_1176x740.png)

Every Parquet file has a **FileMetadata** object in the footer. It has information such as the number of rows, the data schema, and row group metadata. **FileMetadata** is the entry for any Parquet read operations.

![](https://substackcdn.com/image/fetch/$s_!BrZG!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdf441959-ee84-4688-8eeb-76cebe676976_1358x456.png)

## The problem with random access of data

In Parquet, a page is the smallest unit you can read. For data scans, reading and decoding a whole page at a time is ideal. But when you need only a few rows in a page, that is a different story.

> To celebrate reaching 20,000 subscribers, I’m offering **==50% off FOREVER==** ==on the annual plan.==
> 
> Once you claim the offer, the 50% discount will automatically apply to all future renewals.
> 
> You have only **==1 day left==** to claim this offer.
> 
> I couldn’t have achieved this without you guys! Thank you soooo much!

---

—

![](https://substackcdn.com/image/fetch/$s_!twET!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F61c52959-689f-48dd-b3b4-476f3756e732_394x380.png)

To read a row in a page, the engine must fetch the page from disk, then decompress (if it’s compressed) and decode the whole page to reach the target row. Spending time on the whole page when you only need a single row will increase random-access latency.

The larger the page size, the higher the latency.

## The problem with random access of column schema

Parquet FileMetadata is encoded using Apache Thrift or Protocol Buffers. However, Thrift and Protocol Buffers don't support random access; the reader must deserialize the entire FileMetadata object to get the schema, even if it needs only a single column.

![](https://substackcdn.com/image/fetch/$s_!A8Fr!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb2ffa6e4-be26-466e-81fc-bc9a85c217c0_1386x796.png)

AI workloads such as training machine learning models require many descriptive attributes, or features. Each is stored as a column. It’s no surprise that a table used in machine learning has 10,000 columns.

The more columns, the higher the latency to retrieve a single column schema from FileMetadata.

## The row-group constraint

The row group in Parquet is tied directly to the physical I/O unit. The write engine cannot flush a partial column chunk, so it must buffer the entire row group in memory before writing. This is a common cause of out-of-memory (OOM) failures, especially with large column values like AI vector embeddings.

![](https://substackcdn.com/image/fetch/$s_!JKvt!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9b3b22d5-eeba-4a17-bcde-0fd34ecef5ee_722x430.png)

Even without OOM, you may still run into other problems when storing a very large column. Imagine one column with 4KiB values (e.g., 4,096 bytes); a 512 MB Row Group would contain only 125,000 rows (512,000,000/4,096).

![](https://substackcdn.com/image/fetch/$s_!gqF6!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F886f91d8-6648-4576-bd7e-8bfecf1d0301_582x698.png)

Because all columns in the row group must have the same number of rows, all other columns must also be capped at 125,000 rows, although an Int32 column could have 128 million rows (512,000,000/8).

Because each row group will be small, the Parquet file must contain many row groups. This could be inefficient:

- More metadata to manage
- More, smaller reads: within a row group, columns are stored one after another. Reading one column across many row groups means many separate, non-adjacent reads. Reading data from disk is best when it's as sequential as possible, but more row groups don’t encourage that. More reads also mean more GET object storage requests.
- Ineffective compression: large row groups provide a larger sample size of data for each column, allowing compression and encoding algorithms to be more effective.

---

## Lance

[Lance](https://github.com/lance-format/lance) is a modern, open-source columnar data format designed for machine learning and multimodal AI, launched around 2022 by LanceDB (a YC W22 startup) to address Apache Parquet’s performance limitations in AI workloads.

In the Lance spec, there are roughly 4 sections:

![](https://substackcdn.com/image/fetch/$s_!Jo1r!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a4404fd-c3ad-4647-abd6-6409ab88c9c6_1148x350.png)

- The data pages: each page holds some or all of one column’s data. Every page in the file is located by an absolute offset.
- The column metadata: it provides information about the data pages and is located near the end of the file. It includes a set of protobuf messages; each column has its own message, including information such as pointers to the data pages or the encoding scheme.
	- A column metadata offset tableprovides the position and size of each column’s metadata message. It’s stored right next to the column metadata.
- The offset array and the footer live at the end of the file. The array contains the offset to the column metadata, and the footer contains the offset to the array.

## Page Layout

Lance handles random access differently depending on value size.

For small values like integers and short strings, Lance uses **mini-block** encoding. The data page is organized into chunks; each is around 4–8 KiB, with at most 4,096 values.

![](https://substackcdn.com/image/fetch/$s_!dvVT!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F53f1f18e-56b1-4981-84c9-e9e15873e310_1278x412.png)

Like Parquet’s page, the engine still reads and decodes a chunk to get one value. However, because it's much smaller, the decoding is faster.

![](https://substackcdn.com/image/fetch/$s_!F2Bp!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff71da5c8-5b81-41f4-9a5a-35f171bca858_612x424.png)

For large values (vector embeddings, images, large text, 256 bytes per value as threshold), Lance uses “ **full-zip** ” encoding, which interleaves each value’s metadata directly with its data and stitches these metadata-data buffers right next to each other.

![](https://substackcdn.com/image/fetch/$s_!Myaj!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcfd85445-ddfa-4b35-94f4-49f144f6e6d2_1332x418.png)

The compression used is restricted to “transparent” encodings, meaning you can decompress a single value without decoding neighboring values. So if you need embedding #48, you jump directly to it and decompress just that one value.

—

With **transparent encoding,** you can decode each value on its own, as long as you know where it is. Example:

- Dictionary: `["red","blue","red","green"]` becomes indices `[0, 1, 0, 2]`. Index #3 is `2`, which maps to `"green"`.

With **opaque encoding,** decoding one value requires decoding other values too. Example:

- Delta: `[100, 102, 105, 106]` stored as base `100` plus differences `[2, 3, 1]`. Value #3 = 100 + 2 + 3 + 1, so you need every difference before it.

Opaque encodings could save more space, but the values depend on each other, so you can’t decode just one.

Mini-block can use opaque encodings, while full-zip is strictly limited to transparentencodings.

## Abandon Row Group

The Lance file structure abandons the row group concept completely. The column’s data is stored across multiple disk pages. Each page defaults to 8MB.

![](https://substackcdn.com/image/fetch/$s_!Wtkb!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3193477f-dce5-43e9-9d39-6457d2e8ae0d_1410x696.png)

Different columns can have different numbers of pages. Because a page is referenced by an absolute offset, Lance doesn’t require the pages in the same column to be contiguous.

![](https://substackcdn.com/image/fetch/$s_!c_aP!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F787e3245-1afc-469d-8ee7-95ede8451280_986x672.png)

This gives a freedom Parquet can’t offer: the writer can use separate buffers for each column instead of buffering the whole row-group.

Each column's page count simply follows its data size. Take a file with 1 million rows. A boolean column is about 128 KiB, so it fits in a single page. A 3 KiB embedding column is about 3 GiB, which becomes roughly 384 pages of 8 MiB each.

No longer does every column have to share the same row group size.

—

The same freedom applies on the read side.

In Parquet, the row group is usually the unit of parallelism. Ten threads usually means ten row groups. If a file has only one big row group, there’s not much to split.

Lance lets you split the file at any row boundary.

![](https://substackcdn.com/image/fetch/$s_!sv-9!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff0322230-5075-420d-aef2-97a75a5912fa_646x642.png)

Say two threads share a 2 million-row file. One reads rows 0 to 999,999; the other reads from 1,000,000. Row 1,000,000 might sit in the middle of a page, but that’s not the problem.

Each page records the row it starts at, and its internal layout (mini-block chunks, or full-zip byte offsets) maps any range of rows to a range of bytes.

So each thread reads only its own page slice by locating the required byte.

## Schema Random-access

Because each column is described by a separate protobuf message, the reader can retrieve the metadata for the required columns without decoding other column metadata as in Parquet.

![](https://substackcdn.com/image/fetch/$s_!G5dd!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdbeb3700-02d2-4965-bc94-6baadfa5afe6_1032x700.png)

---

## Outro

In this article, I revisit Parquet's current limitations and then discuss Lance. From its specification to its page layout, why it abandons row groups, and how it can now access column metadata in O(1).

Thank you for reading this far.

See you in my next article.

---

## Reference

\[1\] Weston Pace, Chang She, Lei Xu, Will Jones, Albert Lockett, Jun Wang, Raunak Shah, [Lance: Efficient Random Access in Columnar Storage through Adaptive Structural Encodings](https://arxiv.org/pdf/2504.15247), 2025

\[2\] [Lance v2: A columnar container format for modern data](https://blog.lancedb.com/lance-v2/), 2024

\[2\] Julien Le Dem, [Column Storage for the AI Era](https://sympathetic.ink/2025/12/11/Column-Storage-for-the-AI-era.html), 2025