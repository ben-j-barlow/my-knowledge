---
title: "We're Missing Data: The Other Half of AI Transformation"
source: "https://ericdataproduct.substack.com/p/were-missing-data-the-other-half?utm_source=tldrdata"
author:
  - "[[Eric Weber]]"
published: 2026-05-03
created: 2026-05-19
description: "We're not spending enough time talking about the operating model"
tags:
  - "clippings"
---
### Technology before people

Every conversation about AI in data and engineering orgs right now is about tools. Too few are about the operating model that needs to come with them. That gap is the next failure mode.

I have lost count of how many conversations I have had in the last two months about AI productivity in engineering and data teams. The shape is consistent. Codex, Claude Code, and Cursor are making engineers ship faster. Coding agents are taking on tickets that used to take days to complete. Eval infrastructure is enabling teams to ship AI features with greater confidence. Internal AI assistants are being adopted across functions. The conversation is mostly technical, and the measurements are mostly technical: tokens used, throughput, time saved, lines of code accepted.

Almost nobody I talk to is investing the same level of attention in what happens to the org beneath those tools.

This is the next failure mode, I think we are about to hit. It is not the AI investment itself; that is real, and the productivity gains are real (or I think will be in the limit). It is what happens when an organization deploys AI capability without updating its operating model to absorb what the capability is producing. The technical investment compounds for the first six months and then plateaus, because the org was not redesigned around the new shape of work.

I want to propose a way of thinking about this that I have found useful in both my own work and the conversations I have with leaders.

### Two halves

I have started thinking of AI transformation as having two halves. This isn’t revolutionary, but what is important is that I don’t think the two halves are additive, they are multiplicative.

The first half is the technical transformation: which tools to deploy, how to evaluate them, how to integrate them into workflows, and how to measure their impact. This is the half that gets the budget, the executive attention, and the vendor pitches. Most of what is being written about AI in data and engineering orgs right now is about this half. It is also the half that is **comparatively** easy to know what to do about (this is not in fact easy at all).

The second half is what I will call the operating transformation: how roles change, how managers operate, how teams are composed, how careers progress, how decisions get made, and how trust gets established between the team and the rest of the company. This is the half that almost nobody is funding deliberately. It is happening anyway, but as drift, not as design. In the best case, it is being handed to the people team, and they are being told to “figure it out”. The result is that the technical investment underdelivers, and the people in the org are quietly absorbing the cost.

I think these two halves multiply rather than add. A serious technical investment with a stuck operating model produces a productivity bump and then plateaus. A modest technical investment, combined with an updated operating model, yields lower initial throughput but greater compounding capability over time. The teams I see doing this best are the ones funding both halves on purpose, not just the technical one.

### What operating transformation actually looks like

I want to be specific about what I mean by operating transformation, because the phrase can sound like change-management consulting from the 1990s. In a data or engineering org in 2026, it is something more concrete.

**Manager redesign.** The manager-as-router model (assign tickets, unblock obstacles, run standups) is dissolving. The manager-as-coach model (develop judgment, set quality bars, calibrate review of AI output) is what works in an AI-augmented org. Most companies have not retrained their managers for this shift. The people who were excellent managers under the old model are often struggling under the new one, and nobody is helping them.

**Career architecture**. The IC ladder built around “associate to senior to staff,” with “data scientist” or “ML engineer” titles, no longer maps to the work. Engineers who curate AI output are doing different work than engineers who write algorithmic primitives, and both are doing different work than engineers who orchestrate end-to-end product surfaces. The ladder has not been rewritten to reflect this. People are getting promoted and skipped on criteria that were calibrated for a different job.

**Team composition**. Most teams are still sized as if everyone produces work the same way. The teams that are working well right now have rebalanced: more people on data, evaluation, and trust functions; fewer people on pure feature execution. This rebalance is being treated as headcount drama at most companies and as a deliberate operating choice at a few. The deliberate ones are getting better outcomes.

**The data and product partnership**. Product managers used to ask for analyses and wait a few days. They now generate first-pass analyses themselves in a Claude or ChatGPT window in fifteen minutes. The data leader who used to be valuable as the source of those analyses is now valuable in a different role: defining what the analysis should actually mean, calibrating what counts as evidence, and building the measurement infrastructure the product team uses to make decisions. The data-to-product motion that has been the through-line of how good companies operate for the last decade is rewriting itself in real time. Most data leaders have not yet articulated how much of what they used to deliver is no longer the work. Most product leaders have not yet articulated what they actually need from the partnership now. Both sides are operating on a contract that is no longer current.

**Trust with the rest of the company**. Stakeholders outside the data or engineering org used to know your team was producing valuable work because they could see throughput. With AI in the loop, throughput is a noisy signal. The orgs that handle this well are investing in new ways of demonstrating value: shorter feedback loops, more visible decisions, plain explanations of what was actually changed and why. Without this work, stakeholders quietly conclude that the team has become less valuable, even when it has become more valuable.

**Communication norms**. The way data teams talk about their work has to change. “We ran an analysis” used to be enough. In an AI era, it is not, because anyone with a Claude window can run an analysis. What lands now is “we made this decision based on this evidence and here is what we expect to see.” The shift sounds small. It is actually a redesign of how the team relates to the rest of the company.

### A new way of thinking

The thinking I want to propose is this. Stop treating AI transformation as a technical investment with a change-management wrapper bolted on at the end. Start treating it as two parallel stacks that have to be funded together: a technical stack and an operating stack. Budget for both. Measure both. Hold leaders accountable for both.

The technical stack you already know how to think about. You probably have a slide somewhere with model providers, eval infrastructure, agent frameworks, and applications. You can reason about which layers to build and which to buy. The operating stack is what most companies are leaving to chance. If your engineering or data org has a multi-million-dollar AI tooling budget and no equivalent budget for manager redesign, career architecture, team rebalancing, trust mechanics, and communication norm updates, you are funding one half of the transformation and hoping the other half happens for free.

### What do we do?

I keep thinking about what data and engineering leaders should be doing differently right now. The honest answer is that most of us are probably doing the technical half well enough, and most of us are probably doing the operating half as an afterthought, waiting for change to play out.

This newsletter has always been about the path from data to product. The thing I want to make explicit is that the path itself is changing, and the operating stack is what determines whether your team can still walk it. The measurement engineering work I wrote about last week is one piece of that stack. The data and product partnership is another. There are more, and the leaders who figure them out over the next eighteen months are going to be the ones whose AI investment compounds instead of plateaus.

If any of this matches what you are seeing in your own org, I would like to hear about it. The pieces I am working on next are about specific parts of the operating stack, and the conversations I am having with readers are shaping which ones I write first.