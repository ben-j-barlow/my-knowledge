---
tags: [data-n-ai, entity, agents]
sources: ["raw/data-n-ai/articles/Build iterative repair loops with Codex.md"]
updated: 2026-05-14
---

# Codex

**Type:** AI coding agent / CLI tool  
**Creator:** [OpenAI](openai.md)

## Overview

Codex is OpenAI's agentic coding tool. It can review, edit, and execute code autonomously. A CLI (`@openai/codex`) enables headless operation from scripts and notebooks, making it programmable rather than requiring a chat UI.

## CLI Headless Mode

The `codex exec` command accepts a prompt via stdin and returns structured output. Key flags:

- `--model` — specify the model
- `--sandbox workspace-write` — sandbox scope
- `--ask-for-approval never` — fully non-interactive
- `--output-schema <file>` — enforce a JSON schema on the response
- `--output-last-message <file>` — write the structured response to a file
- `--config model_reasoning_effort=<level>` — control reasoning depth (low/medium/high)

This makes Codex composable as a component in larger agent workflows — callers pass in a prompt and schema, get back machine-readable JSON.

## Use in Repair Loops

Codex is well-suited to [iterative repair loop](../concepts/iterative-repair-loops.md) architectures: one `codex exec` call per phase (review, repair, validate-judge), with structured schemas enforcing clean handoffs between phases.

## Related Pages

- [OpenAI](openai.md)
- [Iterative Repair Loops](../concepts/iterative-repair-loops.md)
- [Source: Build Iterative Repair Loops with Codex](../sources/codex-iterative-repair-loops.md)
