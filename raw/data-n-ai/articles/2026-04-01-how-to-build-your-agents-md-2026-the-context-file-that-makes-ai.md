---
title: "How to Build Your AGENTS.md (2026): The Context File That Makes AI Coding Agents Actually Work"
source: "https://www.augmentcode.com/guides/how-to-build-agents-md"
author:
  - "[[Ani Galstian]]"
published: 2026-04-01
created: 2026-06-05
description: "Build an AGENTS.md that improves AI coding agent performance. Covers structure, writing patterns, modular org, and ETH Zurich research on context file quality."
tags:
  - "clippings"
---
AGENTS.md is a Markdown file placed at the root of a repository that provides AI coding agents with persistent, project-specific operational guidance: build commands, coding conventions, testing rules, and constraints the agent cannot infer from the codebase alone. Building an effective AGENTS.md requires writing only what agents cannot discover independently, structuring rules for machine parsing rather than human readability, and accepting a measurable inference-cost trade-off that pays off only when the file is human-curated rather than auto-generated.

## TL;DR

The central question isn't whether to create an AGENTS.md. It's whether yours will improve agent performance or just add token overhead. The ETH Zurich study found that LLM-generated context files reduced task success rates by approximately 3% on average, increased inference costs by over 20%, and required 2-4 additional reasoning steps. Human-curated files provided a marginal 4% performance gain, but still incurred the same token overhead. This guide covers the structure, content decisions, and modular organization that determines which side of that line your file lands on, plus how tools like Intent address the maintenance problem manual files can't solve at scale.

### See how Intent's living specs keep parallel agents aligned across cross-service refactors.

[Build with Intent](https://www.augmentcode.com/product/intent)

Free tier available · VS Code extension · Takes 2 minutes

ci-pipeline

···

$ cat build.log | auggie --print --quiet \\

"Summarize the failure"

Build failed due to missing dependency 'lodash'  
in src/utils/helpers.ts:42

Fix: npm install lodash @types/lodash

## Why AI Coding Agents Need a Context File

Every [coding agent](https://www.augmentcode.com/guides/top-ai-coding-tools-2025-for-enterprise-developers), whether Claude Code, Cursor, GitHub Copilot, or Codex, starts each session blind to your project's specific conventions. The agent knows how to write Python or TypeScript in general, but it does not know that your team uses Pixi instead of pip, that your API client never throws exceptions, or that the vendor/ directory should never be modified.

Before AGENTS.md emerged as a standard, teams maintained a patchwork of tool-specific files to communicate these constraints. An Augment blog post describes the experience: "Open a typical project that's been through a few months of AI-assisted development. You'll find some combination of CLAUDE.md,.cursorrules, and copilot-instructions.md, AGENTS.md, and maybe a Gemini.md for good measure. Almost the same content in each one. Slowly drifting apart."

The [spec repo](https://github.com/agentsmd/agents.md) defines AGENTS.md as "Think of AGENTS.md as a README for agents: a dedicated, predictable place to provide context and instructions to help AI coding agents work on your project." OpenAI helped pioneer the AGENTS.md format for Codex, and in December 2025, it was donated to the Agentic AI Foundation (AAIF), a directed fund under the Linux Foundation, alongside Anthropic donating the Model Context Protocol (MCP) and Block donating Goose.

| File | Primary Audience | Purpose |
| --- | --- | --- |
| README.md | Human developers | Project overview, installation, usage |
| CONTRIBUTING.md | Human contributors | How to submit PRs, code style for humans |
| AGENTS.md | AI coding agents | Build commands, test runners, conventions, constraints for autonomous agents |

## The Quality Threshold: What ETH Zurich Found About Context File Effectiveness

The [ETH study](https://arxiv.org/abs/2602.11988) evaluated multiple coding agents and LLMs across two benchmarks, comparing LLM-generated and developer-written context files and their performance relative to no repository context. The findings challenge two common practices.

**LLM-generated context files hurt performance.** In 5 out of 8 tested settings, LLM-generated files reduced task success rates. Agents took 2.45 to 3.92 additional steps per task, and inference costs increased by 20% to 23%.

**Developer-written context files help, but modestly.** Human-curated files outperformed LLM-generated files for all four agents tested, with a gain of roughly 4 percentage points on the AGENTbench benchmark.

| Context File Type | Cost Increase | Task Success Change |
| --- | --- | --- |
| LLM-generated (auto-init) | +20 to 23% | −0.5% (SWE-bench Lite) to −2% (AGENTbench) |
| Developer-written (human-curated) | Up to 19% (shorter files, lower cost than LLM-generated) | Marginal improvement (AGENTbench) |
| No context file | Baseline | Baseline |

A critical follow-up experiment removed all other documentation from the repository before re-evaluating. Under those conditions, LLM-generated files improved performance by 2.7%, confirming the core insight: LLM-generated context files are redundant with existing documentation that agents already access independently. Duplicating that content adds cost without adding signal.

### What "Non-Inferable Details" Means in Practice

The study concludes that human-written files should describe only minimal requirements, custom-built commands, and specific tooling choices, while avoiding content that agents can already discover independently.

| Content Type | Include? | Reason |
| --- | --- | --- |
| Custom build commands not documented elsewhere | Yes | Non-inferable |
| Highly specific tooling choices (e.g., pixi instead of pip) | Yes | Non-inferable |
| Codebase overviews and architecture summaries | No | Agents find these independently |
| Anything already in README or existing docs | No | Redundant; increases steps and cost |

Architectural overviews "do not provide effective overviews," per the study: removing an "Architecture" section while keeping only commands, constraints, and non-standard patterns produces the same agent behavior at a lower [token budget](https://www.augmentcode.com/guides/mastering-ai-context-and-why-it-matters-more-than-token-count).

## Core Sections for Every AGENT.md Needs

[GitHub analysis](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/) and [OpenAI docs](https://developers.openai.com/codex/guides/agents-md) converge on the sections that consistently improve agent behavior. Each section targets a specific class of agent errors.

### Section 1: Stack Definition With Exact Versions

Without version constraints, the agent defaults to whichever API conventions are most represented in training data. The [Inngest repo](https://github.com/inngest/website/blob/main/AGENTS.md) illustrates the principle, specifying versions hard, signaling non-negotiable constraints explicitly:

```markdown
## Tech Stack

- Framework: Next.js 15 (App Router + Pages Router hybrid)
- Language: TypeScript
- Package Manager: pnpm (always use pnpm, never npm)
- Node Version: 22.x (required)
```

### Section 2: Executable Commands With Full Flags

Place commands early; the agent references them repeatedly throughout a task. From [mcollina/skills](https://github.com/mcollina/skills/blob/main/AGENTS.md):

```markdown
## Common commands

\`npm install\`
\`npm run typecheck\`
\`npm run lint\`
\`npm test\`
\`node --test path/to/file.test.ts\`
\`node --test --test-name-pattern "pattern"\`
```

Per [OpenAI docs](https://developers.openai.com/codex/guides/agents-md), AGENTS.md can specify programmatic checks Codex will attempt to run before finishing a task. These are advisory, not mechanically enforced: agents may skip checks if they judge them unnecessary, so clarity of instruction matters more than assumed compliance.

### Section 3: Coding Conventions and Patterns

One real snippet showing your style beats three paragraphs describing it. The most valuable convention to document is the counterintuitive one. The [NetCore repo](https://github.com/NetCoreTemplates/nextjs/blob/main/AGENTS.md) includes this:

```
All client \`api\`, \`apiVoid\` and \`apiForm\` methods never throws exceptions -
it always returns an \`ApiResult<T>\` which contains either a response for
successful responses or an error with a populated \`ResponseStatus\`, as such
using \`try/catch\` around \`client.api\` calls is always wrong.
```

Without this, an agent wraps every api call in try/catch. The file explains the mechanism that enables the agent to generalize correctly to novel situations.

### Section 4: Testing Rules

From [phodal/auto-dev](https://github.com/phodal/auto-dev/blob/master/AGENTS.md.example):

```markdown
## Testing Guidelines

- Write unit tests for all new functionality
- Mock external dependencies when appropriate
- Ensure tests are deterministic and isolated
```

For complex build systems, exact commands matter more than guidelines. The [CBMC repo](https://github.com/diffblue/cbmc/blob/develop/AGENTS.md) includes:

```bash
cmake --build build
ctest --test-dir build -V -L CORE -j$(nproc)
cd unit && ../build/bin/unit
```

### Section 5: "Don't Touch" Zones and Permission Boundaries

"Never commit secrets" was the most common helpful constraint across 2,500+ repositories per [GitHub analysis](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/). A three-tier system gives the agent an explicit priority hierarchy when rules interact:

```markdown
### ✅ Always
- Run linting before committing
- List only human authors in git commits

### ⚠️ Ask First
- Database schema changes
- Adding new dependencies

### 🚫 Never
\`.env\`
- Force push to main
- Modify content within [protected] blocks
```

This particular Vercel template's AGENTS.md file begins with an "Architecture Guidelines. Repository Page Structure." section; this file does not start with security rules or use a CRITICAL: severity prefix, though security guardrails are recommended in related docs.

### Section 6: Non-Standard Tooling

AGENTS.md delivers the highest ROI for tools underrepresented in LLM training data:

```markdown
## Package management

\`pixi run <command>\`
\`pixi run python script.py\`
\`pixi run pytest\`
```

For standard tools like npm, pytest, or cargo, agents already know the conventions. Focus on what the agent genuinely cannot know.

## Tool-Specific Variants: CLAUDE.md,.cursorrules, and copilot-instructions.md

AGENTS.md is converging as a cross-tool standard. Claude Code includes [auto-memory](https://docs.anthropic.com/en/docs/claude-code/memory), building persistent learning across sessions without manual configuration. A claudeMdExcludes config prevents instruction bleed in [large monorepos](https://www.augmentcode.com/guides/ai-coding-assistants-for-large-codebases-a-complete-guide). Cursor's.cursor/rules/ system uses YAML frontmatter to scope rules by glob pattern. [GitHub Copilot](https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot) uses.github/copilot-instructions.md for repository-wide defaults and path-specific.instructions.md files for targeted rules.

| Feature | CLAUDE.md | Cursor.mdc | copilot-instructions | .windsurf/rules |
| --- | --- | --- | --- | --- |
| Format | Plain Markdown | Markdown with required YAML frontmatter | Plain Markdown | Plain Markdown |
| Multi-file support | Yes | Not documented as.cursor/rules/ | Yes,.github/instructions/ | Not documented as.windsurf/rules/ |
| File-based scoping | User vs. project level | — | Path-specific.instructions.md | — |
| Auto-memory | Built-in | Unknown | Yes (Copilot Memory) | Yes (Memories) |
| Agent-decided rule inclusion | No | Yes (description field) | No | No |
| AGENTS.md interop | No (uses CLAUDE.md) | Yes | Yes | Unknown |

For multi-tool teams, the symlink pattern keeps files from diverging: "Note: CLAUDE.md is a symlink to AGENTS.md. They are the same file."

## Modular Rules: When and How to Split Your Context File

A monolithic AGENTS.md loads every rule into the agent's context on every invocation. Start with a single file; split it into subdirectories when it exceeds 150-200 lines. The [maas repo](https://github.com/canonical/maas/blob/master/AGENTS.md) represents the upper bound: a 371-line root file. Beyond that scale, modular organization becomes necessary for [token budget](https://www.augmentcode.com/guides/mastering-ai-context-and-why-it-matters-more-than-token-count) reasons.

Place context files at any directory level; the agent reads the file closest to the file being edited:

```
project/
├── AGENTS.md              # Root: org-wide standards, global commands
├── apps/
│   ├── web/
│   │   └── AGENTS.md      # Web app overrides and additions
│   └── api/
│       └── AGENTS.md      # API service overrides and additions
└── infra/
    └── AGENTS.md          # Terraform/infrastructure rules
```

Per the [Codex spec](https://openai.com/index/introducing-codex/), more deeply nested files take precedence in case of conflicting instructions.

| Condition | Approach |
| --- | --- |
| Single root file under 150 to 200 lines | Monolithic root file sufficient |
| Rules exceed 150-200 lines | Split: root for org standards, subdirectory files for specifics |
| Cross-cutting concerns (security, testing, CI) | Cursor.mdc files per concern with glob patterns |
| Multiple AI tools in use | Canonical AGENTS.md + tool-specific symlinks |
| Enterprise compliance requirements | Windsurf system-level rules + workspace rules |

## The Cost Tradeoff: Roughly 20% Inference Overhead

The [ETH study](https://arxiv.org/abs/2602.11988) measured the following overhead across context file types:

| Metric | Value |
| --- | --- |
| Inference cost increase (LLM-generated context files) | 20 to 23% |
| Inference cost increase (developer-provided context files) | Up to 19% |
| Reasoning token increase (GPT-series, LLM-generated files) | +14% to +22% |
| Reasoning token increase (GPT-series, human-written files) | +2% to +20% |

Using Claude Sonnet 4.6 pricing ($3.00/MTok input, $15.00/MTok output) with a baseline agentic task of roughly 50K input tokens and 5K output tokens:

| Monthly Task Volume | Monthly Overhead Cost |
| --- | --- |
| 1,000 tasks | ~$45 |
| 10,000 tasks | ~$450 |
| 100,000 tasks | ~$4,500 |

Prompt caching is the primary mitigation; cache reads are 90% cheaper than standard input pricing. The 20% overhead applies regardless of whether the file is auto-generated or human-written. LLM-generated files give negative returns: worse performance at higher cost. Human-curated files yield roughly a 4-percentage-point improvement. Writing manually is worth the overhead. Auto-generating and committing is not.

## Failure Patterns That Undermine AGENTS.md

**Auto-generated files perform worse than no file.** Per the [ETH study](https://arxiv.org/abs/2602.11988), LLM-generated files reduced task success rates by 0.5% to 2% while increasing inference costs by over 20%. Rules should respond to observed failure, not be generated speculatively.

Open source

augmentcode/review-pr★36

[Star on GitHub](https://github.com/augmentcode/review-pr?utm_source=blog&utm_medium=cta&utm_campaign=github&utm_content=how-to-build-agents-md)

**Context file bloat reduces task success.** More rules do not produce better performance. Every time an agent makes a mistake, the default reaction is to add another rule. Rules are rarely removed. The file accumulates contradictory patches and one-off fixes, working directly against effective [context engineering](https://www.augmentcode.com/guides/7-ways-context-engineering-supercharges-enterprise-ai-dev).

**Silent rule dropout in long sessions.** [Documented Claude Code issues](https://github.com/anthropics/claude-code/issues) report agents ignoring CLAUDE.md instructions, the "lost in the middle" phenomenon. Keep files short, place critical rules early, and start new sessions for new tasks. [Anthropic guide](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) notes that as context grows, agents preserve architectural decisions while discarding redundant tool outputs.

**Stale structural references actively mislead.** Context files documenting repository structure become liabilities when the codebase changes. Per the [ETH study](https://arxiv.org/abs/2602.11988), architectural overviews increased inference cost and encouraged broader file traversal without improving task success.

### Explore how Intent's coordinator, implementor, and verifier agents reduce manual reconciliation across long-running work.

[Build with Intent](https://www.augmentcode.com/product/intent)

Free tier available · VS Code extension · Takes 2 minutes

## Complete AGENTS.md Template

This template synthesizes patterns from [OpenAI docs](https://developers.openai.com/codex/learn/best-practices/), [GitHub analysis](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/), and production repositories, including [Vercel Next.js](https://github.com/vercel/next.js/blob/canary/AGENTS.md) and [Inngest repo](https://github.com/inngest/website/blob/main/AGENTS.md).

```markdown
# AGENTS.md - [Project Name]

## Project Overview

[One sentence: stack, versions, what makes it architecturally non-standard]

## Key Commands

\`npm install\`
\`npm run dev\`
\`npm run build\`
\`npm run typecheck\`
\`npm run lint\`
\`npm test\`
\`npx vitest run src/path/to/file.test.ts\`

## Project Structure

\`src/\`
\`src/components/\`
\`tests/\`
\`src/App.tsx\`

## Code Style

[Insert one representative code snippet from this codebase here]

- Named exports only, no default exports
- Keep files under [N] lines when possible

## Non-Obvious Patterns

[Document counterintuitive architectural decisions with mechanism explanations]

## Testing Rules

- Write tests for all new functionality
- Tests must be deterministic and isolated
- Mock all external dependencies
\`npm test\`

## Boundaries

### ✅ Allowed without asking
- Read files, list directory contents
- Run lint, typecheck, single test files

### ⚠️ Ask first
- Install or remove packages
- Delete files
- Push to git or open PRs

### 🚫 Never
\`.env\`
- Force push to main or protected branches
\`vendor/\`

## Key Files

\`src/main.ts\`
\`src/config/\`
```

[Version-control](https://www.augmentcode.com/guides/13-enterprise-version-control-integrations-ai-powered-git-workflow-automation-for-development-teams) this file and treat updates as code changes. Remove the "Project Structure" section if your directory layout follows framework conventions the agent already knows. The "Non-Obvious Patterns" section is where AGENTS.md delivers the highest signal-to-noise ratio.

## From Manual Context Files to Automated Context Management

Manual AGENTS.md files face a fundamental maintenance challenge: context files drift as codebases evolve, and there is no automated way to detect staleness.

When used as an MCP server alongside a manually maintained AGENTS.md, Augment Code's Context Engine is most useful during [cross-service refactoring](https://www.augmentcode.com/guides/4-ai-solutions-for-multi-service-refactoring) tasks. The Context Engine semantically indexes and maps the codebase across hundreds of thousands of files, maintaining a live understanding of how files connect without requiring manual updates.

[Intent](https://www.augmentcode.com/product/intent) takes this further with spec-driven development. Instead of maintaining a static instruction file that agents read before acting, Intent introduces living specs that agents update as they work: "When an agent completes work, the spec updates to reflect reality."

| Dimension | Manual AGENTS.md | Intent's Context Engine |
| --- | --- | --- |
| Maintenance | The developer writes and updates manually | Agents update the living spec as they work |
| Scope | Single Markdown file at repo root | Real-time semantic index across hundreds of thousands of files |
| Staleness risk | Requires manual remediation after refactors | Real-time indexing |
| Work isolation | Shared across all work | Per-workspace git worktrees |
| Dependency tracking | Not built-in | Cross-service dependency tracking |

Intent's coordinator agent analyzes the codebase, drafts the spec, generates tasks, and delegates to [specialist agents](https://www.augmentcode.com/guides/5-autonomous-agents-for-end-to-end-feature-automation). Implementor agents execute tasks in parallel waves. A verifier agent checks results against the spec and flags inconsistencies. The spec auto-updates to reflect what was actually built, addressing the staleness problem that manual AGENTS.md files cannot solve at scale.

## Start With a Minimal Number Of AGENTS.md Before Context Drift Sets In

The hardest part of AGENTS.md isn't writing it. It's keeping it accurate as the underlying codebase changes. Non-inferable details, counterintuitive patterns, and custom tooling constraints deliver the highest signal, but they drift fastest as codebases evolve.

Start with the template above. Focus the first version on commands, boundaries, and the one or two architectural decisions that look wrong to an outsider but are intentional. Version-control changes and review them like code. When the maintenance burden outgrows what manual curation can sustain, that's the point where tools like Intent solve a real problem rather than a theoretical one.

### See how Intent's living specs and isolated workspaces keep multi-agent development aligned as codebases change.

[Build with Intent](https://www.augmentcode.com/product/intent)

Free tier available · VS Code extension · Takes 2 minutes

## Frequently Asked Questions about Building AGENTS.md

## Related Guides

- [5 Autonomous Agents for End-to-End Feature Automation](https://www.augmentcode.com/guides/5-autonomous-agents-for-end-to-end-feature-automation)
- [Top CLI AI Agents for Enterprise Developers](https://www.augmentcode.com/guides/top-cli-ai-agents-for-enterprise-developers)
- [7 Ways Context Engineering Supercharges Enterprise AI Dev](https://www.augmentcode.com/guides/7-ways-context-engineering-supercharges-enterprise-ai-dev)
- [11 Best AI Coding Tools for Enterprise](https://www.augmentcode.com/guides/11-best-ai-coding-tools-for-enterprise)
- [12 AI Coding Use Cases to Accelerate Software Development](https://www.augmentcode.com/guides/12-ai-coding-use-cases-to-accelerate-software-development)

### Written by

![Ani Galstian](https://www.augmentcode.com/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Foraw2u2c%2Fproduction%2F68545e0f765ac7ec41ac8be27ff7164b3e21a0b9-288x288.png&w=128&q=75)

#### Ani Galstian

Ani writes about enterprise-scale AI coding tool evaluation, agentic development security, and the operational patterns that make AI agents reliable in production. His guides cover topics like AGENTS.md context files, spec-as-source-of-truth workflows, and how engineering teams should assess AI coding tools across dimensions like auditability and security compliance