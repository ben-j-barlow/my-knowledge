---
title: "AI for the Real World: A conversation with Yann LeCun"
source: "https://x.com/AnneliesGamble/status/2054219457451733382?utm_source=tldrai"
author:
  - "[[@AnneliesGamble]]"
published: 2026-05-12
created: 2026-05-14
description: "Are today’s language models the path towards machine intelligence, or are they just a commercially viable local maximum?@ylecun is one of th..."
tags:
  - "clippings"
---
![Image](https://pbs.twimg.com/media/HIINoITasAA-QQ3?format=jpg&name=large)

Are today’s language models the path towards machine intelligence, or are they just a commercially viable local maximum?

[@ylecun](https://x.com/@ylecun) is one of the clearest and most consistent voices arguing for the latter. In his view, LLMs are not intelligent, however useful they may be. Systems trained to predict sequences of discrete tokens don’t have an understanding of the world, which is a fundamental building block of intelligence.

I sat down with Yann a couple weeks ago to explore this idea and his vision for the future.

"There's one question of whether the models we have today are useful? Is there a market for them? Yes." But on the bigger question, "Will these models take us to human-level intelligence or something similar to it? Absolutely no."

Yann recently founded [@amilabs](https://x.com/@amilabs), a [@ZettaVentures](https://x.com/@ZettaVentures) portfolio company, to build what he thinks the alternative will look like: world models that can understand the physical world and predict the consequences of actions.

## Why language isn't intelligence

"Much of human knowledge and thought has nothing to do with language," Yann said. And yet we credit anything that speaks fluently with understanding. "We're biased towards attributing intelligence to things that can express themselves through language."

He walked me through a calculation he's done before. A four-year-old has been awake for roughly 16,000 hours. The optic nerve carries about one byte per second per fiber, with roughly a million fibers per eye. If you multiply it out, you get something on the order of 10^14 bytes of visual data reaching the brain in the first four years of life, roughly the same order of magnitude as the entire text corpus used to pretrain a modern LLM.

"It would take any of us something like 400,000 years to read through that," he said. In other words, a small child has already absorbed, through vision alone, about as much raw information as the largest language models see in training. "We're never going to get to human-level AI by just training on text. It's just not going to happen."

What LLMs do have is an ability to accumulate and retrieve declarative knowledge. This means they look smarter over time without developing deeper models of reality. They simply become more familiar with the kinds of questions people ask.

"If you want a system to act intelligently," he said, "it has to be able to predict the consequences of its actions. And LLMs are completely incapable of doing this."

Yann believes in language models for two specific domains: coding and math. "The reason why it works so well in these two domains is because these are domains where the mere manipulation of symbols is actually kind of the substrate of reasoning." But these are narrow cases. "For everyday things that require a little bit of common sense reasoning and certainly planning, they're just never going to get there."

## What the alternative looks like

The alternative is what Yann has been working toward for over 15 years. It’s a system that learns how the world evolves, and can predict what the consequence of a sequence of actions is going to be.

"This is the only way to build an agentic system that is reliable," he said. "I do not understand how people can even think of building agentic systems that do not have this ability of predicting the consequences of their actions before they do them."

The hard part is learning such a model from real-world data. Next-token prediction works because symbols are discrete and compressible. The physical world is not. "I've been working on this for over 15 years, and essentially failing the first 10 years, because I was using generative architectures trying to predict what's going to happen in the video at the pixel level. This kind of data is just not predictable."

He gave the example of a pen balanced on your hand. If you let go, you can predict that it will fall. But you can’t predict the exact direction it will fall, or the precise configuration of every pixel in the next frame. If you train a system to predict all of those details, you’re forcing it to model noise and contingency as though they were the essence of intelligence. "When you try to train a system to predict every detail in a situation, you kind of kill it because you try to train it to do something that's impossible."

His proposed alternative is Joint Embedding Predictive Architecture (JEPA). Rather than predicting every pixel, the system learns an abstract representation of the world and makes its predictions there. "All the details about the input that are not predictable, all the noise, all the complexities of it are basically going to be eliminated from the representation so that the prediction can be reliable." You learn the latent state that matters for planning, even if you can't regenerate a photorealistic frame from it.

Once you have an abstract world model, reasoning becomes search through that model. That's what LLMs can't do, because they don't have a model to search through. "The idea that reasoning is a kind of search is really fundamental," he said. "LLMs don't do this. They don't have any ability to really search for an answer. They just produce an answer, a token." Chain-of-thought, in his view, is a workaround: "a very, very inefficient way of coercing autoregressive prediction systems to basically approach reasoning." Real reasoning, he argues, is internal simulation. This means manipulating mental models, running counterfactuals, planning hierarchically the way a human plans a trip to Paris (aka not at the level of muscle commands, but refining subgoals from the top down).

This is why he prefers the term [Superhuman Adaptable Intelligence](https://arxiv.org/abs/2602.23643) to AGI. "The true property of intelligence is to solve new problems you've not been trained to solve."

## AMI Labs and World Models

That thesis is now Yann’s company: AMI Labs, Advanced Machine Intelligence, (pronounced "ah-mee," just like the French word for friend).

AMI is building AI for the real world. "A lot of industry is just running things, right? Like physical things. And this is where current AI technology falls short," he told me. The company's stated focus is industrial process control, automation, wearable devices, robotics, and healthcare.

A huge portion of the economy depends on running physical systems (factories, supply chains, power grids, biological systems, transportation networks). These are environments where text is often the interface around the work, but not the work itself. "AMI is building generic foundation models that can be applied to any situation where you need an intelligent system to run something physical," Yann said.

The physical-economy layer of AI will be built on a different stack from what most companies are using today. Rather than predicting the next token, this is about predicting the next state.

There are a number of other companies also trying to build versions of world models. The approaches differ on what the model tries to predict: pixels and geometry versus abstract state.

[@drfeifei](https://x.com/@drfeifei)'s [@theworldlabs](https://x.com/@theworldlabs) is building, according to their website, "world models that can perceive, generate, reason, and interact with the 3D world." Their first product, [Marble](https://www.worldlabs.ai/labs), turns text, images, or video into 3D environments that designers can open in different creative tools. [@GoogleDeepMind](https://x.com/@GoogleDeepMind)'s [Genie 3](https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/) takes a different approach to a similar problem, generating interactive worlds in real time that users can navigate frame by frame.

[@1x\_tech](https://x.com/@1x_tech) and [@GeneralistAI](https://x.com/@GeneralistAI) are building video-pretrained world models specifically for humanoid robotics. 1X's model learns from internet video first, then from footage shot from a human's point of view, and uses a second model to turn its predictions of "what should happen next" into robot movements. Generalist combines ideas from world models and VLAs, training on roughly 500,000 hours of real-world physical interaction data collected from wearables worn by humans doing everyday tasks.

[@nvidia](https://x.com/@nvidia)'s [Cosmos](https://github.com/nvidia-cosmos) is building a platform to "help developers build customized world models for their Physical AI setups." Meanwhile, [@Tesla](https://x.com/@Tesla) is building a single AI model that can drive cars and control humanoid robots, treating both as different bodies running the same underlying intelligence.

What distinguishes AMI is the architectural bet around JEPA-style abstract representation rather than pixel-level generation. Pixel-perfect prediction is computationally expensive and, as Yann argued for years before the field caught up, trying to predict the unpredictable actively degrades the model's grip on what matters. Abstract representation preserves the causally relevant structure while removing the noise. If it works, it’s both a better model of physics and a cheaper one to deploy.

## Why this matters

For robotics specifically, the implications are significant. The dominant approach today, vision-language-action models that map observations directly to motor commands, runs into two well-understood ceilings.

The first is data. Teleoperated robot data is the highest-quality source but doesn't parallelize. It's bounded by the number of robots you own and the hours skilled operators can work. Researchers have developed workarounds: hand-held grippers like UMI that let humans collect demos without a robot, wearable rigs that record everyday activity, cross-embodiment datasets that pool data across robot types, and simulation pipelines. But there is an embodiment gap for each that has to be bridged. Meanwhile, the largest available corpus by far, human video on the internet, is hard to exploit directly because the actions aren't labeled. Recent work on inverse dynamics and latent action models is starting to unlock it, which is part of why world models have gained momentum.

The second is embodiment lock-in. Observation-to-action mapping tends to couple learned knowledge to a specific robot body. Transfer across embodiments is possible but imperfect. A policy trained on one arm typically needs significant adaptation to work on another. Knowledge ends up captured at the level of "how this robot should move in this specific setting" rather than "what should happen in the world."

World models attack both problems at once. If you learn an abstract representation of how the world evolves (how objects fall, how contact propagates, how liquids behave), you've learned something that is true regardless of which body is acting in it. That knowledge can be absorbed from video without action labels, because the goal isn't to predict the next motor command but to predict the next state. A model that understands physics can then be adapted to whatever embodiment is available, with calibration rather than retraining.

The opportunity extends well beyond robotics. "There are tons and tons of applications of this type," Yann told me. "You want to control anything in the real world: manufacturing plant, turbojet engine, chemical process. A human cell. You want to plan a sequence of treatment for a patient to, I don't know, control blood sugar. If you have a good predictive model of at least some aspect of the state of the patient, you might be able to do this kind of planning on a personalized basis."

## A system that thinks

It's easy, in a moment like this one, to mistake the shape of the market for the shape of the problem. LLMs are producing extraordinary value, and they will keep doing so in cases where symbolic manipulation is the actual work.

But most of the economy doesn't run on words and symbols. It runs on physical systems, environments where text serves as a wrapper, but isn't the work itself. The systems capable of operating in those environments will need something current models don't have: a base-level understanding of the world, the ability to predict the consequences of actions, and the capacity to adapt to problems they weren't trained on.

Intelligence is much more than language. Future AI systems will still use language, but language will no longer be their only substrate.

As Yann put it, "language will serve as an interface to a system that thinks."

Author’s note: An LLM was used for light copy editing only (spelling, grammar, and clarity). Content, meaning, tone, and structure remain unchanged.