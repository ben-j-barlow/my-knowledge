---
title: "Lecture 11. Making the Agent's Runtime Observable"
source: "https://walkinglabs.github.io/learn-harness-engineering/en/lectures/lecture-11-why-observability-belongs-inside-the-harness/"
author:
published:
created: 2026-09-11
description: "A project-based course on designing the environments, state, verification, and control systems that make Codex and Claude Code reliable."
tags:
  - "clippings"
---
[中文版 →](https://walkinglabs.github.io/learn-harness-engineering/zh/lectures/lecture-11-why-observability-belongs-inside-the-harness/)

> Code examples: [code/](https://github.com/walkinglabs/learn-harness-engineering/blob/main/docs/en/lectures/lecture-11-why-observability-belongs-inside-the-harness/code/) Practice project: [Project 06. Build a Complete Agent Harness](https://walkinglabs.github.io/learn-harness-engineering/en/projects/project-06-runtime-observability-and-debugging/)

You ask an agent to implement a feature. It runs for 20 minutes, touches a pile of files, then tells you "done, but two tests are failing." You ask why — "not sure, might be a timing issue." You ask which critical paths it changed — "let me look at the code..."

This scenario is all too common, and the root cause isn't the agent's capability — it's the harness's lack of observability. When an agent executes a task without visibility into the actual runtime state, every decision it makes is essentially a guess.

**Without observability, agents make decisions under uncertainty, evaluations become subjective judgments, and retries become blind wandering.** Both OpenAI and Anthropic frame reliability as an evidence problem: the harness must expose runtime behavior and evaluation signals in a form that can actually guide the next decision.

## The Real Cost of Missing Observability

When a harness lacks observability, four categories of problems appear systematically.

**Cannot distinguish "correct" from "looks correct."** A function looks perfectly right in code review — correct syntax, sound logic. But at runtime, a boundary-condition handling error produces incorrect results under specific inputs. Only runtime traces can reveal that the actual execution path deviated from expectations. Code review shows "what was written"; runtime tracing shows "what actually ran." You need both.

**Evaluation becomes mysticism.** Without scoring rubrics and acceptance criteria, evaluators (human or agent) have to rely on implicit assumptions. The same output can get wildly different assessments from different evaluators. Quality evaluation becomes non-reproducible.

**Retries become blind guesses.** When the agent doesn't know why something failed, its retry direction is random. It might hammer away in the wrong direction — fixing unrelated code paths while ignoring the real root cause. Every blind retry burns tokens and time.

**Session handoff information cliff.** When incomplete work is handed to the next session, missing observability means the new session has to diagnose the system state from scratch. Anthropic's observations of long-running agents show that this redundant diagnosis can eat up 30-50% of total session time.

## A Real Claude Code Scenario

Consider a harness using a "planner-generator-evaluator" three-role workflow, executing the task "add dark mode to the app."

**Without observability:** The planner outputs a vague description. The generator implements dark mode based on that vagueness, but the result doesn't match the planner's implicit expectations. The evaluator rejects it based on their own implicit standards but can't articulate what's specifically wrong — just "it doesn't feel right." The generator retries blindly on vague rejection reasons. The cycle repeats 3-4 times, taking about 45 minutes, and barely produces an acceptable output.

**With full observability:** The planner outputs a sprint contract listing which components to modify, verification standards for each, and exclusions (e.g., no print styles). The generator implements according to the contract, and runtime observability records each component's style loading and application process. The evaluator uses a scoring rubric to evaluate dimension by dimension, citing specific evidence: "Button color contrast is insufficient (WCAG AA standard 4.5:1, measured 2.1:1)." One iteration produces a high-quality result, in about 15 minutes.

3x efficiency difference. The only variable is observability.

## Layered Observability

Observability isn't just "add more logging." It operates on two layers, and both are essential.

<svg id="mermaid-59" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 1363.671875px;min-width: 0px; width: auto !important; max-width: 100% !important; max-height: min(56vh, 520px) !important;" viewBox="0 0 1363.671875 212.5" role="graphics-document document" aria-roledescription="flowchart-v2"><g><marker id="mermaid-59_flowchart-v2-pointEnd" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-59_flowchart-v2-pointStart" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-59_flowchart-v2-pointEnd-margin" viewBox="0 0 11.5 14" refX="11.5" refY="7" markerUnits="userSpaceOnUse" markerWidth="10.5" markerHeight="14" orient="auto"><path d="M 0 0 L 11.5 7 L 0 14 z" style="stroke-width: 0px; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-59_flowchart-v2-pointStart-margin" viewBox="0 0 11.5 14" refX="1" refY="7" markerUnits="userSpaceOnUse" markerWidth="11.5" markerHeight="14" orient="auto"><polygon points="0,7 11.5,14 11.5,0" style="stroke-width: 0px; stroke-dasharray: 1, 0;"></polygon></marker><marker id="mermaid-59_flowchart-v2-circleEnd" viewBox="0 0 10 10" refX="11" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-59_flowchart-v2-circleStart" viewBox="0 0 10 10" refX="-1" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-59_flowchart-v2-circleEnd-margin" viewBox="0 0 10 10" refY="5" refX="12.25" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 0px; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-59_flowchart-v2-circleStart-margin" viewBox="0 0 10 10" refX="-2" refY="5" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 0px; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-59_flowchart-v2-crossEnd" viewBox="0 0 11 11" refX="12" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-59_flowchart-v2-crossStart" viewBox="0 0 11 11" refX="-1" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-59_flowchart-v2-crossEnd-margin" viewBox="0 0 15 15" refX="17.7" refY="7.5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 1,1 L 14,14 M 1,14 L 14,1" style="stroke-width: 2.5;"></path></marker><marker id="mermaid-59_flowchart-v2-crossStart-margin" viewBox="0 0 15 15" refX="-3.5" refY="7.5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 1,1 L 14,14 M 1,14 L 14,1" style="stroke-width: 2.5; stroke-dasharray: 1, 0;"></path></marker><g><g></g><g><path d="M256,155.652L260.667,156.918C265.333,158.184,274.667,160.717,283.333,161.984C292,163.25,300,163.25,304,163.25L308,163.25" id="mermaid-59-L_Contract_Generator_0" style=";" data-edge="true" data-et="edge" data-id="L_Contract_Generator_0" data-points="W3sieCI6MjU2LCJ5IjoxNTUuNjUxNTIzMTM4MzQ3NDF9LHsieCI6Mjg0LCJ5IjoxNjMuMjUwMjIzMTU5NzkwMDR9LHsieCI6MzEyLCJ5IjoxNjMuMjUwMjIzMTU5NzkwMDR9XQ==" data-look="classic" marker-end="url(#mermaid-59_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path><path d="M427.686,137.75L435.017,134C442.348,130.25,457.01,122.75,468.341,119C479.672,115.25,487.672,115.25,491.672,115.25L495.672,115.25" id="mermaid-59-L_Generator_Signals_0" style=";" data-edge="true" data-et="edge" data-id="L_Generator_Signals_0" data-points="W3sieCI6NDI3LjY4NjA2NzY5MzA1OTY3LCJ5IjoxMzcuNzUwMzA3MDgzMTI5ODh9LHsieCI6NDcxLjY3MTg3NSwieSI6MTE1LjI1MDE3NzM4MzQyMjg1fSx7IngiOjQ5OS42NzE4NzUsInkiOjExNS4yNTAxNzczODM0MjI4NX1d" data-look="classic" marker-end="url(#mermaid-59_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path><path d="M244.403,56L251.003,52.125C257.602,48.25,270.801,40.5,293.04,36.625C315.279,32.75,346.557,32.75,377.836,32.75C409.115,32.75,440.393,32.75,481.366,32.75C522.339,32.75,573.005,32.75,623.672,32.75C674.339,32.75,725.005,32.75,754.362,33.842C783.718,34.934,791.765,37.117,795.788,38.209L799.812,39.301" id="mermaid-59-L_Contract_Review_0" style=";" data-edge="true" data-et="edge" data-id="L_Contract_Review_0" data-points="W3sieCI6MjQ0LjQwMzM1MTUxNzU1MTY0LCJ5Ijo1Ni4wMDAwNDU3NzYzNjcxOX0seyJ4IjoyODQsInkiOjMyLjc1MDAwNTcyMjA0NTl9LHsieCI6Mzc3LjgzNTkzNzUsInkiOjMyLjc1MDAwNTcyMjA0NTl9LHsieCI6NDcxLjY3MTg3NSwieSI6MzIuNzUwMDA1NzIyMDQ1OX0seyJ4Ijo2MjMuNjcxODc1LCJ5IjozMi43NTAwMDU3MjIwNDU5fSx7IngiOjc3NS42NzE4NzUsInkiOjMyLjc1MDAwNTcyMjA0NTl9LHsieCI6ODAzLjY3MTg3NSwieSI6NDAuMzQ4NzA1NzQzNDg4NTE2fV0=" data-look="classic" marker-end="url(#mermaid-59_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path><path d="M747.672,115.25L752.339,115.25C757.005,115.25,766.339,115.25,775.028,114.158C783.718,113.066,791.765,110.883,795.788,109.791L799.812,108.699" id="mermaid-59-L_Signals_Review_0" style=";" data-edge="true" data-et="edge" data-id="L_Signals_Review_0" data-points="W3sieCI6NzQ3LjY3MTg3NSwieSI6MTE1LjI1MDE3NzM4MzQyMjg1fSx7IngiOjc3NS42NzE4NzUsInkiOjExNS4yNTAxNzczODM0MjI4NX0seyJ4Ijo4MDMuNjcxODc1LCJ5IjoxMDcuNjUxNDc3MzYxOTgwMjN9XQ==" data-look="classic" marker-end="url(#mermaid-59_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path><path d="M1051.672,74L1056.339,74C1061.005,74,1070.339,74,1079.036,75.273C1087.734,76.546,1095.796,79.092,1099.827,80.365L1103.858,81.638" id="mermaid-59-L_Review_Verdict_0" style=";" data-edge="true" data-et="edge" data-id="L_Review_Verdict_0" data-points="W3sieCI6MTA1MS42NzE4NzUsInkiOjc0LjAwMDA5MTU1MjczNDM4fSx7IngiOjEwNzkuNjcxODc1LCJ5Ijo3NC4wMDAwOTE1NTI3MzQzOH0seyJ4IjoxMTA3LjY3MTg3NSwieSI6ODIuODQyMjA1MjQ4MzgwOTZ9XQ==" data-look="classic" marker-end="url(#mermaid-59_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path><path d="M1134.944,174.5L1125.732,179.5C1116.52,184.5,1098.096,194.5,1063.551,199.5C1029.005,204.5,978.339,204.5,927.672,204.5C877.005,204.5,826.339,204.5,775.672,204.5C725.005,204.5,674.339,204.5,623.672,204.5C573.005,204.5,522.339,204.5,491.644,202.144C460.95,199.787,450.227,195.073,444.866,192.717L439.505,190.36" id="mermaid-59-L_Verdict_Generator_0" style=";" data-edge="true" data-et="edge" data-id="L_Verdict_Generator_0" data-points="W3sieCI6MTEzNC45NDQ0ODcyNjQ1NzMsInkiOjE3NC41MDAzMDg5OTA0Nzg1Mn0seyJ4IjoxMDc5LjY3MTg3NSwieSI6MjA0LjUwMDMwODk5MDQ3ODUyfSx7IngiOjkyNy42NzE4NzUsInkiOjIwNC41MDAzMDg5OTA0Nzg1Mn0seyJ4Ijo3NzUuNjcxODc1LCJ5IjoyMDQuNTAwMzA4OTkwNDc4NTJ9LHsieCI6NjIzLjY3MTg3NSwieSI6MjA0LjUwMDMwODk5MDQ3ODUyfSx7IngiOjQ3MS42NzE4NzUsInkiOjIwNC41MDAzMDg5OTA0Nzg1Mn0seyJ4Ijo0MzUuODQzMjk2MzQ2MzgwMTYsInkiOjE4OC43NTAxMzkyMzY0NTAyfV0=" data-look="classic" marker-end="url(#mermaid-59_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path></g><g><g style="font-size: 14px !important;"><g data-id="L_Contract_Generator_0" transform="translate(0, 0)" style="font-size: 14px !important;"></g></g><g style="font-size: 14px !important;"><g data-id="L_Generator_Signals_0" transform="translate(0, 0)" style="font-size: 14px !important;"></g></g><g style="font-size: 14px !important;"><g data-id="L_Contract_Review_0" transform="translate(0, 0)" style="font-size: 14px !important;"></g></g><g style="font-size: 14px !important;"><g data-id="L_Signals_Review_0" transform="translate(0, 0)" style="font-size: 14px !important;"></g></g><g style="font-size: 14px !important;"><g data-id="L_Review_Verdict_0" transform="translate(0, 0)" style="font-size: 14px !important;"></g></g><g style="font-size: 14px !important;"><g data-id="L_Verdict_Generator_0" transform="translate(0, 0)" style="font-size: 14px !important;"></g></g></g><g><g id="mermaid-59-flowchart-Contract-0" data-look="classic" transform="translate(132, 122.00013732910156)"><rect style="" x="-124" y="-66.00008773803711" width="248" height="132.00017547607422" fill="none" stroke="currentColor"></rect><g style="font-size: 14px !important;" transform="translate(-100, -54.00008773803711)"><rect></rect><foreignObject width="200" height="108.00017547607422"><div xmlns="http://www.w3.org/1999/xhtml" style="display: table; white-space: break-spaces; line-height: 1.5; max-width: 200px; text-align: center; width: 200px;"><span style="font-size: 14px !important;"><p>Define the task upfront<br>which files to change / what not to touch / pass criteria</p></span></div></foreignObject></g></g><g id="mermaid-59-flowchart-Generator-1" data-look="classic" transform="translate(377.8359375, 163.25022315979004)"><rect style="" x="-65.8359375" y="-25.49991512298584" width="131.671875" height="50.99983024597168" fill="none" stroke="currentColor"></rect><g style="font-size: 14px !important;" transform="translate(-41.8359375, -13.49991512298584)"><rect></rect><foreignObject width="83.671875" height="26.99983024597168"><div xmlns="http://www.w3.org/1999/xhtml" style="display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span style="font-size: 14px !important;"><p>Generator</p></span></div></foreignObject></g></g><g id="mermaid-59-flowchart-Signals-3" data-look="classic" transform="translate(623.671875, 115.25017738342285)"><rect style="" x="-124" y="-52.50017166137695" width="248" height="105.0003433227539" fill="none" stroke="currentColor"></rect><g style="font-size: 14px !important;" transform="translate(-100, -40.50017166137695)"><rect></rect><foreignObject width="200" height="81.0003433227539"><div xmlns="http://www.w3.org/1999/xhtml" style="display: table; white-space: break-spaces; line-height: 1.5; max-width: 200px; text-align: center; width: 200px;"><span style="font-size: 14px !important;"><p>Collect at runtime<br>logs / traces / health checks</p></span></div></foreignObject></g></g><g id="mermaid-59-flowchart-Review-5" data-look="classic" transform="translate(927.671875, 74.00009155273438)"><rect style="" x="-124" y="-66.00008773803711" width="248" height="132.00017547607422" fill="none" stroke="currentColor"></rect><g style="font-size: 14px !important;" transform="translate(-100, -54.00008773803711)"><rect></rect><foreignObject width="200" height="108.00017547607422"><div xmlns="http://www.w3.org/1999/xhtml" style="display: table; white-space: break-spaces; line-height: 1.5; max-width: 200px; text-align: center; width: 200px;"><span style="font-size: 14px !important;"><p>Check item by item against the list<br>functionality / tests / boundaries</p></span></div></foreignObject></g></g><g id="mermaid-59-flowchart-Verdict-9" data-look="classic" transform="translate(1231.671875, 122.00013732910156)"><rect style="" x="-124" y="-52.50017166137695" width="248" height="105.0003433227539" fill="none" stroke="currentColor"></rect><g style="font-size: 14px !important;" transform="translate(-100, -40.50017166137695)"><rect></rect><foreignObject width="200" height="81.0003433227539"><div xmlns="http://www.w3.org/1999/xhtml" style="display: table; white-space: break-spaces; line-height: 1.5; max-width: 200px; text-align: center; width: 200px;"><span style="font-size: 14px !important;"><p>Point out which item failed<br>and where to fix it</p></span></div></foreignObject></g></g></g></g></g><defs></defs><defs></defs><linearGradient id="mermaid-59-gradient" gradientUnits="objectBoundingBox" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#cccccc" stop-opacity="1"></stop><stop offset="100%" stop-color="hsl(180, 0%, 18.3529411765%)" stop-opacity="1"></stop></linearGradient></svg>

**Runtime observability:** System-level signals — logs, traces, process events, health checks. Answers "what did the system do."

**Process observability:** Visibility into harness decision artifacts — plans, scoring rubrics, acceptance criteria. Answers "why should this change be accepted."

## Core Concepts

- **Runtime observability**: System-level signals including logs, traces, process events, and health checks. Answers "what did the system do."
- **Process observability**: Visibility into harness decision artifacts including plans, scoring rubrics, and acceptance criteria. Answers "why should this change be accepted."
- **Task trace**: A complete decision-path record from task start to completion, analogous to request tracing in distributed systems. Every step the agent takes, along with its context, is recorded — so when something goes wrong, you can replay the entire process.
- **Sprint contract**: A short-term agreement negotiated before coding begins, specifying task scope, verification standards, and exclusions. The core tool for process observability.
- **Evaluator rubric**: Transforms quality evaluation from subjective judgment into evidence-based structured scoring, enabling different evaluators to reach similar conclusions for the same output.
- **Layered observability**: System-layer and process-layer observability designed simultaneously and reinforcing each other. Runtime signals explain behavior; process artifacts explain intent.

## Why Agents Can't Solve This Themselves

You might be thinking: "Can't the agent just print its own logs?" The problem is:

1. **Agents don't know what they don't know.** They won't proactively record signals they don't realize they need. Without harness-level constraints, agents only log what they think is important — and what they think is important is usually not enough.
2. **Log formats are inconsistent.** Different sessions use different log formats, making systematic analysis impossible.
3. **Process observability can't be solved by logging.** Sprint contracts and scoring rubrics are structured artifacts that require harness-level support — adding a few print statements won't cut it.

## How to Build Observability

### 1\. Build Runtime Signal Collection into the Harness

Don't rely on the agent to print its own logs. The harness should automatically collect the following signals:

- **Application lifecycle**: Startup, ready, running, shutdown phase states
- **Feature path execution**: Execution records for critical paths, including entry points, checkpoints, and exits
- **Data flow**: Records of data flowing between components
- **Resource utilization**: Abnormal resource usage patterns (e.g., continuously growing memory)
- **Errors and exceptions**: Full error context, not just error messages

### 2\. Implement Sprint Contracts

Before each task begins, the generator and evaluator (which may be different invocations of the same agent) negotiate a contract that defines what to build and what "done" looks like:

```markdown
# Sprint Contract: Dark Mode Support

## Scope
- Modify the theme toggle component
- Update global CSS variables
- Add dark mode tests

## Verification Standards
- Visual regression tests pass for each component
- Main flow end-to-end tests pass
- No flash of unstyled content (FOUC)

## Exclusions
- Not handling print styles
- Not handling third-party component dark mode
```

### 3\. Establish an Evaluator Rubric

Turn "is it good or not" into quantifiable scoring:

```markdown
# Scoring Rubric

| Dimension | A | B | C | D |
|-----------|---|---|---|---|
| Code correctness | All tests pass | Main flow passes | Partial pass | Build fails |
| Architecture compliance | Fully compliant | Minor deviations | Obvious deviations | Serious violations |
| Test coverage | Main + edge cases | Main flow only | Only skeleton | No tests |
```

### 4\. Standardize with OpenTelemetry

Create a trace for each harness session, a span for each task, and sub-spans for each verification step. Use standard attributes to annotate key information. This way observability data integrates with standard toolchains (Jaeger, Zipkin).

## Anthropic's Three-Agent Architecture Experiment

In March 2026, Anthropic published a systematic harness experiment. They ran the same task ("build a browser-based DAW using the Web Audio API") with three different architectures and recorded detailed phase-by-phase data:

| Agent & Phase | Duration | Cost |
| --- | --- | --- |
| Planner | 4.7 min | $0.46 |
| Build round 1 | 2 hr 7 min | $71.08 |
| QA round 1 | 8.8 min | $3.24 |
| Build round 2 | 1 hr 2 min | $36.89 |
| QA round 2 | 6.8 min | $3.09 |
| Build round 3 | 10.9 min | $5.88 |
| QA round 3 | 9.6 min | $4.06 |
| **Total** | **3 hr 50 min** | **$124.70** |

Each of the three agents had a distinct role, and each played a clear part in observability:

**Planner:** Receives a 1-4 sentence user requirement and expands it into a full product spec. It was instructed to "be bold in scope" and "focus on product context and high-level technical design rather than detailed technical implementation." The reasoning: if the planner prematurely specifies granular technical details and gets them wrong, those errors cascade downstream. A better approach is to constrain deliverables and let the agent find its own path during execution.

**Generator:** Implements feature by feature, sprint by sprint. Before each sprint, it negotiates a sprint contract with the evaluator defining what "done" means for that feature block. It then implements according to the contract, self-evaluates, and hands off to QA.

**Evaluator:** Uses Playwright MCP to interact with the running app like a real user — testing UI functionality, API endpoints, and database state. It scores each sprint across four dimensions: product depth, functionality, visual design, and code quality. Each dimension has a hard threshold — if any falls short, the sprint fails and the generator receives detailed feedback for fixes.

Example feedback from QA round 1: "This is a visually impressive app with good AI integration, but several core DAW features are presentational only, lacking interaction depth: clips can't be dragged/moved, there's no instrument UI panel (synth knobs, drum pads), and no visual effects editor (EQ curves, compressor meters)." These aren't edge cases — they're the core interactions that make a DAW usable. Specific, evidence-backed feedback — not "it doesn't feel right."

The evaluator wasn't always this sharp. Early versions would identify reasonable issues, then talk themselves into dismissing those issues as not severe, ultimately approving the work. The fix: read the evaluator's logs, find the points where its judgment diverged from human judgment, and update the QA prompt to address those specific problems. After several rounds of this development loop, the evaluator's scoring became reliable.

> Source: [Anthropic: Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)

## Key Takeaways

- **Observability is a harness architecture property.** It's not a feature you add after the fact — it's a core capability that must be designed in from the start.
- **Both observability layers are essential.** Runtime signals explain "what happened," process artifacts explain "why it was done this way."
- **Sprint contracts front-load alignment.** They prevent the generator from building something the evaluator immediately rejects for foreseeable reasons.
- **Scoring rubrics make evaluation reproducible.** Different evaluators produce similar scores for the same output.
- **Missing observability wastes 30-50% of session time on redundant diagnosis.**

## Further Reading

- [Observability Engineering - Charity Majors](https://www.honeycomb.io/blog/observability-engineering-book) — Theory and practice framework for modern observability engineering
- [Dapper - Google (Sigelman et al.)](https://research.google/pubs/pub36356/) — Groundbreaking practice in large-scale distributed tracing
- [Harness Design - Anthropic](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Introducing sprint contracts and evaluator rubrics
- [Site Reliability Engineering - Google](https://sre.google/sre-book/table-of-contents/) — Systematic application of observability in production systems

## Exercises

1. **Observability Gap Analysis**: Audit your current harness for system-layer and process-layer observability. Find system states that can't be distinguished from existing signals, and propose additions.
2. **Sprint Contract Practice**: Write a sprint contract for a real task. Have the agent execute according to the contract, and compare efficiency and quality with and without the contract.
3. **Task Trace Construction**: Record every step an agent takes during a complete coding task. Annotate using OpenTelemetry semantic conventions. Analyze the trace for information bottlenecks — which steps lack sufficient signal support for their decisions.