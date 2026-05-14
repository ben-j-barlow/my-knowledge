---
tags: [data-n-ai, entity]
sources: ["raw/data-n-ai/articles/Build iterative repair loops with Codex.md"]
updated: 2026-05-14
---

# OpenAI

**Type:** AI research company  
**Founded:** 2015  
**Website:** https://openai.com

## Overview

OpenAI is the creator of the GPT model family, ChatGPT, and the OpenAI API. It is one of the dominant commercial providers of large language model infrastructure and tooling.

## Key Products / APIs

| Product | Description |
|---------|-------------|
| GPT / o-series models | Foundation LLMs (chat, reasoning, embeddings) |
| [Codex](codex.md) | Agentic coding tool and CLI |
| Responses API | Current API for chat completions (`client.responses.create`) |
| Evals API | Framework for evaluating model and agent outputs |
| OpenAI Cookbook | Public repository of practical usage examples and patterns |

## API Conventions (current as of 2026-05)

- Chat completions: `client.responses.create` (replaces `client.chat.completions.create`)
- Tool use: current tools schema (replaces legacy function-calling schemas)
- Embeddings: `text-embedding-3-large` is the preferred embedding model

## Related Pages

- [Codex](codex.md)
