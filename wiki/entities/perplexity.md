---
tags: [data-n-ai, entity, agents, security]
sources: ["wiki/sources/perplexity-how-we-engineer-safer-agents.md"]
updated: 2026-10-02
---

# Perplexity (AI)

AI search/agent company; publishes [agent security engineering](../concepts/agent-security-defense-in-depth.md) research and open-source security tooling, and co-founded the **Open Secure AI Alliance** with NVIDIA. Launched the **Secure Intelligence Institute** (March 2026) to fund/run agent security research with Stanford, CMU, Duke, Columbia, Ohio State, and UVA.

## Agent Products

- **Computer** — cloud agent platform; every task runs inside **SPACE**, a per-task Firecracker microVM sandbox (credentials outside the sandbox, outbound traffic controlled at the node level, rollback via snapshots).
- **Comet** — browser agent with a layered prompt-injection defense (BrowseSafe classifiers + untrusted-content marking + user confirmation on sensitive actions).
- **Portable Computer** — local-first, on-device agent run by a deterministic (non-LLM) orchestrator inside an always-on, fail-closed OS-level sandbox; escalates to a cloud "advisor" model only with explicit per-action user approval and a PII pre-filter.
- Employee coding-agent endpoints — secured by **Numbat** (cross-harness security monitor) and **Bumblebee** (supply-chain scanner), both open-sourced.

## Open-Source Security Tools

- **Numbat** — security monitor that sits outside any single agent harness (works with Claude Code, Codex, OpenCode, Pi); blocks dangerous actions pre-execution, flags suspicious multi-step sequences, preserves session timelines.
- **Bumblebee** — open-source supply-chain scanner.
- **BrowseSafe** — open-source prompt-injection/hostile-content detection classifier, with a public benchmark (BrowseSafe-Bench) that itself demonstrates no single detector is fail-safe.

## Related Pages

- [Agent Security: Defense-in-Depth](../concepts/agent-security-defense-in-depth.md) — the architecture this entity's products implement
- [Source: How We Engineer Safer Agents](../sources/perplexity-how-we-engineer-safer-agents.md)
