---
tags: [data-n-ai, concept, etl, pipelines, llm]
sources: ["raw/data-n-ai/articles/Plan Mode All the Time, Substrait over SQL, and the End of the DE Role ft. Chris Riccomini.md"]
updated: 2026-05-28
---

# Substrait

A cross-language serialization format for relational algebra — a standard way to represent data transformations that can be passed between systems without re-parsing SQL. Website: [substrait.io](https://substrait.io/).

## SQL vs. Substrait

**SQL is purely logical.** A SQL JOIN statement says *what* to do ("join these tables on this key") but not *how* to do it. The execution engine chooses the physical strategy (broadcast, hash, merge, nested loop). SQL has no vocabulary for expressing physical operators.

**Substrait can express both.** It supports logical operators (like SQL) and physical operators (merge join, hash join, specific scan strategies). For those with a compilers background: Substrait can express both abstract and concrete syntax trees — both the logical IR and the physical execution plan.

## Why It Could Matter for LLMs

**1. Fewer tokens.** A structured binary/protobuf serialization of a query is more compact than the equivalent SQL text. Smaller token count → lower cost and potentially fewer hallucinations from the model filling in natural-language ambiguity.

**2. Client-side query optimization.** If an LLM speaks Substrait, it can reason about physical execution strategy — choose hash join over merge join based on table statistics — and pass a physical plan directly to the database for execution, bypassing the database's own optimizer for that query. This is not possible with SQL alone.

**3. Reduced hallucination.** SQL's natural-language proximity means an LLM can hallucinate plausible-looking-but-wrong clauses. Substrait's structured grammar constrains output more tightly.

**Caveat:** SQL is vastly overrepresented in LLM training data. Substrait is not. LLMs are currently less capable with Substrait than SQL — adoption would require deliberate fine-tuning or prompt investment.

## Status

Substrait is an emerging standard. It is not yet the default interface for any major database, but it's gaining traction as an interchange format for query plans between systems. It connects to the [Apache Arrow](../entities/apache-arrow.md) ecosystem — both aim at cross-language interoperability for analytical workloads.

## Related Pages

- [Query Optimization](query-optimization.md)
- [Apache Arrow](../entities/apache-arrow.md)
- [Chris Riccomini](../entities/chris-riccomini.md)
- [Source: Plan Mode All the Time](../sources/2026-05-21-plan-mode-substrait-de-role.md)
