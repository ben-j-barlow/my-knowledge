---
title: "Write-Ahead Intent Log: a Foundation for Efficient CDC at Scale"
source: "https://www.infoq.com/presentations/write-ahead-intent-log/?utm_source=tldrdata"
author:
  - "[[Vinay Chella]]"
  - "[[Akshat Goel]]"
published: 2026-06-18
created: 2026-07-23
description: "Vinay Chella and Akshat Goel explain why they outgrew traditional CDC at scale. They share how they built Write-Ahead Intent Log (WAIL) using a proxy layer to decouple data replication."
tags:
  - "clippings"
---
[AI, ML & Data Engineering](https://www.infoq.com/ai-ml-data-eng/ "AI, ML & Data Engineering")

[QCon San Francisco (Nov 16-20): Deep technical sessions. Peer conversations that change how you think.](https://qconsf.com/?utm_source=infoq&utm_medium=referral&utm_campaign=infoqyellowbox_qsf26)

- Vertical
- Horizontal
- Full

- 1x
- 1.25x
- 1.5x
- 2x

![](https://imgopt.infoq.com/fit-in/1288x0/filters:quality(80)/presentations/write-ahead-intent-log/en/slides/Doi-1781788191276.jpg)

## Summary

Vinay Chella and Akshat Goel discuss the challenges of running traditional CDC across heterogeneous databases during peak order traffic. They explain how Debezium hit limits under high load and share how they built Write-Ahead Intent Log (WAIL) - a custom architecture that utilizes a dumb producer proxy and a smart consumer pattern to cleanly separate the intent from the state payload.

## Bio

Vinay Chella is an Engineering Leader at DoorDash, where he leads the Storage and Streaming Infrastructure organization that powers mission-critical systems across the marketplace. Akshat Goel is a Staff Software Engineer at DoorDash, where he builds the Storage Access Platform, a unified abstraction layer powering all online data stores.

## About the conference

Software is changing the world. QCon San Francisco empowers software development by facilitating the spread of knowledge and innovation in the developer community. A practitioner-driven conference, QCon is designed for technical team leads, architects, engineering directors, and project managers who influence innovation in their teams.

## Transcript

**Vinay Chella:** We spend our days at DoorDash making sure when someone places an order, we prepare the food, take it up in a car, deliver it. No, we don't do that. We ensure when someone places an order, the sequence of events that has to happen across varied systems go through smoothly. That includes a part where we panic slightly. We panic slightly when database hiccups happen exactly during the peak hours, when there's a rush hour and a lot of orders coming in. Today, we are going to talk about something that sounds deeply technical, but yet, that's actually the center of what we do at DoorDash. All the way from ensuring you get your delivery ETA on your screens, to a ping on the merchant tablet preparing your food.

That topic is change data capture, and how we eventually got tired of traditional way of leaning on these traditional CDCs and started building our own approach, which we call Write-Ahead Intent Log. Before we dive into the details, I really want to start with a small story, show why this problem actually matters.

I'm Vinay Chella. I lead storage and streaming infrastructure at DoorDash. I help build distributed databases and also distributed teams.

**Akshat Goel:** I'm Akshat. I'm a Staff Software Engineer at DoorDash. I help Vinay in building the distributed data applications.

**Vinay Chella:** Together we spend a lot of time building distributed database abstractions so that our business teams can focus on solving the business problems rather than dealing with all the databases and streaming shenanigans.

## The Order Flow at DoorDash

Imagine it's peak dinner time, orders are pouring in, restaurants are slammed with orders, and drivers are zipping through the streets, and customers are both hungry and impatient to get their orders delivered. On the screen you see a real perfect world, ideal world, where one tap on the screen, on the app, flows through the system beautifully. The order lands in the order database, and restaurants get notified, and your driver gets dispatched, and the app updates instantly. In the real world, these steps are tightly connected and highly choreographed. Even if one signal fails, there is a possibility of the sequence of steps falling out of sync, and teams often try to glue things together with things like dual writes. You write to the database, and also send an event to the streaming system. It sounds simple, but it's pretty brittle.

One could succeed, and the other could fail, and suddenly your systems have different truths. The real problem here is not the UI, or not the chef in a restaurant. It's making sure that the intent of you need to get your grocery delivered, or your food delivered, flows through all of our complex systems in a way that it needs to, and all of our logistics system gets notified. Really want to pause and provide some analogy here. I'm sure all of you have tried to fold a fitted sheet at your home. It's pretty hard. You try hard, you try for a lot of time, and you end up shuffling it in a closet, and say that's what's expected. Trying to choreograph these systems, trying to dual write these systems is exactly like folding a fitted sheet.

Let's see what happens when one intent fails in this complex system. The order is in the order database, but the restaurant never got notified, and the delivery was never dispatched. The customer is stuck at their order screen, staring at that processing spinner while getting hungrier by the minute. One missing update could end up turning into refunds, escalations, and unhappy customers. Oftentimes, you lean on to solutions like, you poll the database, but that isn't a real solution either. It adds load on your database, it lags, and you still end up reacting pretty late in the game. That's exactly why systems like CDC are in place, and CDC matters. CDC gives us a real time stream of changes, so every downstream system can stay aligned and do the work that they need to. CDC, change data capture is not a magic, it's not a silver bullet.

It has a lot of tricky edges. You have connectors that could break. You have sinks that could go down. You have different databases speaking different dialects. This world is real, and we need to ensure that data is also real. What it means for DoorDash is that every order update has to be real-time and move reliably throughout our chain of microservices. The rest of the talk today will focus on how we moved from this brittle architecture to more durable, more visible, recoverable, and much less painful system, and we are calling that intent log. Again, if you remember from these two slides, one thing that you can walk away with is that it's not about the state, it's about the intent, like what is that you're trying to do. Ensuring that intent flows through sequence of your system is the key, and everything else is plumbing.

## Content

On a high level, we'll cover why CDC matters to us, our business, and what are the typical challenges in the CDC, and talk about what is the foundation that we are building on, and also some of the operational learnings that we are taking as we are rolling it out across our system.

## Setting the Stage (CDC at DoorDash)

CDC powers a majority of the things at DoorDash. CDC shows up directly in our business problems. A huge part of our customer and merchant experience depends on having the real-time data, real-time state. When an order is placed, or updated, or canceled, or delivered, dozens of systems need to be notified, and react pretty much instantly. For business analytics, teams rely on fresh data to understand the marketplace health, to understand the delivery time, to understand the quality. If the data is stale, then we are not moving the business needle in the right way, and not having the impact that we would like to. For user experience, think about, a restaurant is running out of an item, and they updated item availability.

A grocery store running out of a certain product, and updated it, but on the user side, if you don't see that update, you end up placing the order, and it leads to item unavailability. Your delivery is getting delayed, and your customer is seeing something that is not on the store, and that's basically business chaos. CDC isn't nice to have for us, and CDC is basically foundational for what we do. Our marketplace works reliably when data flows through these systems much more instantly, in a much more reliable way. Engineering problems behind the CDC is also quite challenging, and quite complex. You might have systems like searching and caching, those could be customized in-house solutions, which are different from your source-of-truth database.

The data in CDC basically keeps your source-of-truth database with your derived datastores, like search and caching systems, in sync, that enables us to serve our business functionality on our application. Then I also call something called outbox pattern, where oftentimes your developers might end up building this outbox pattern, where you have transactional table, and also outbox table, which basically informs your downstream consumers about all the changes that are happening. CDC would make it much more easy, if there is one. Also, multi-data or materialized views, or keeping the heterogeneous datastores in sync would be another technical need as well. As you have heterogeneous stores, things like indexing for searching and caching system to serve really fast data. Your transactional data or source-of-truth database, could all be different systems. The best way to keep them in sync is through systems like CDC.

This is how the traditional CDC would look like. You have an application writing to a database, and database, through some connectors, ends up in your systems like Kafka event streaming systems, and then your applications consume from that. It's a pretty proven pattern, but the moment something goes wrong, like schema change breaking your connector, or the downstream sync slowing down, the whole pipeline gets tangled. Traditional CDC ends up coupling us tightly to the database internals and how these systems work. That becomes pretty hard to operate when you are trying to scale your systems.

## Challenges with CDC

Now that we have seen how traditional CDC works in theory, let's talk about what are the real-world problems that show up when you try to run this kind of system at scale. The first one that comes to my mind is abstraction challenge. Every database speaks a different CDC dialect, and I'm sure you are in an environment where you have various databases that you are running. Postgres has logical replication, Cassandra-like systems have commit logs, and Scylla has a different format. Some systems do not even have CDC. Instead of one clean pipeline, you get a zoo of connectors and guarantees and quirks that you deal with. If you are a platform team, and trying to offer a unified storage solution, storage abstraction, like we are trying to do, that becomes painful real fast.

You're basically acting as a database translator between different databases, and you're trying to work with these databases which stubbornly refuse to align on the common dialect and common vocabulary about CDC, common guarantees about CDC. Especially when you're trying to put this at scale, that gets even worse. Any small difference in a minor update of a database, semantics, or auditing guarantees, or checkpoint formats, or transaction behavior, just leaks upward to your customers. Every consumer of your CDC now needs to understand what the underlying database is trying to do. That's exactly opposite of what we want by building this layer of indirection and platform abstractions. That's why building abstraction become the first major challenge in CDC, because you can't reliably build this foundation on top of bricks which don't speak to each other.

Then comes the scalability and simplicity. This is the next big decision in CDC architecture, is the tradeoff. Do you want to optimize for fast and quick setup, or do you want to have a sustainable scale of architecture? Oftentimes, teams start with very simple route, a single CDC connector, very minimal configuration, and one service to manage. It works greatly when you start your product. As the traffic grows, as the number of tables onboarding to your system grow, then that connector becomes bottlenecked. Eventually, that even becomes your single point of failure. Then the alternative is your production scale architecture with distributed components. You have buffering built in. You have routing, you have observability, all of this built in. It's more resilient, but it also requires a lot of upfront investment going into building this kind of architecture. That is exactly where we met our experience with Debezium.

It's a great open-source option. As we put it to scale and do the scale test, it struggled pretty badly. We saw CPU spikes. We saw almost double the latencies, duplicated messages in a multi-region setup, and several limitations around routing and its reliability. It just couldn't keep up with the scale test that we were performing. Our lesson was very clear. Choosing the simplicity gives pretty good early returns, but hidden complexity that comes along with it over a period of time makes it pretty hard for you to scale.

Then the next challenge in the traditional CDC architecture is the ecosystem itself. If you go browse around a lot of these databases and their CDC features, there are good open-source options, but they work really simply enough. When you need complex features and features that you expect in production, like exactly once semantics, and schema evolution handling, and stuff like that, they often sit behind the paywall. You get the basics for free, but when you actually need production requirements, you end up paying a lot of money. If you think about these connectors' maturity, they are pretty uneven as well. If you look around, Postgres CDC connector is well-tested, widely accepted. If you explore options like Cassandra, Scylla connectors, they vary in reliability and infrastructure that you need to set up, things like depending on Kafka Connect and stuff like that.

Then you end up dealing with a lot of inconsistencies while you're operating this centralized database platform. That makes it really hard for you as a platform to provide any kind of guarantees. In that mix, if you have any cloud-managed services like DynamoDB and stuff like that, then for those specific services, CDC might look more convenient, but they create a strong vendor lock-in over a period of time. Once you adopt them, it's pretty hard for you to keep up with your evolution and providing any flexibility in how you design systems. If you think about it, even before you start your business and your business logic gets involved, the ecosystem itself introduces a lot of friction and long-term constraints around your CDC architecture.

That brings us to the next challenge, is about the fragility in the CDC pipelines itself. Even with the right tooling, CDC pipelines tend to be more fragile than they look. Let me walk you through a few examples. There are many moving parts in the CDC ecosystem, like connector, your downstream consumers, and stuff like that. Each have their own limitations, their own failure modes. For example, a schema change in your upstream database could break your connector, or a commit log in your Cassandra can arrive late or out of order. Maybe if your sink is Kafka and downstream consumer is lagging behind, that backpressure builds up and breaks your entire pipeline. When something goes wrong in this complex architecture, recovery becomes rarely seamless. You may need to replay the logs. You may need to do the full load of the database, and debug why certain events dropped.

Especially when you're operating terabytes or petabytes of data, it becomes real hard. That fragility is why relying purely on the traditional CDC becomes pretty risky when you start to scale. Think about this. The system only works as well as its weakest component. When you design this beautiful system, and when you have that CDC, the center of everything that you're orchestrating, it becomes chaotic. These are the challenges that really pushed us to take a step back and rethink the foundations entirely, which leads us to the principles that we are building this solution on, and the principles that helped us shape the solution that we are going to talk about.

## Foundations for our Solution

Now that we talked about why CDC matters to our business, and why the traditional CDC wasn't enough, now let's get into how we actually are solving it. Now for that part, because I'm just a talker, I don't do stuff, Akshat is the one who is building that stuff, and being foundational in designing that, and what we are learning.

**Akshat Goel:** One thing that I want to get out of this talk is, everyone's solutions look different, everyone's problems look different, so even if we don't align on the final solution that we are implementing for DoorDash, I want you to take away what are the key foundations, or what are the key principles you need to keep in mind when you are designing your own systems for scalability, as well as decoupling from your databases. That brings us to the first part of our foundation, which is decoupled by design. Vinay talked about how different database technologies talk about CDC in different ways, they have different semantics, different technologies they use.

One thing that we want to tackle early on in our design is that our CDC connectors, our CDC change feeds should totally be decoupled from the technology that we are using for our database, and that is our first principle. The next principle is, each system, no matter how complex you make it from the day one, it evolves to be even more complex in the future. What we want to do is bring down that complexity when we start developing our solution, and let our business or technical use cases evolve the complexity of the system, rather than we building the complexity from day one. The next part with the licensing and ecosystem challenge, we want to break free from the licensing or ecosystem requirements. If you haven't seen, Redis moved from open-source license to Valkey, which gave birth to Valkey.

What we want to do is make the system flexible enough so that we can swap out different parts as their licensing needs, as their ecosystem changes, and we should have the flexibility enough to use any open-source technology that we desire. Then, finally, Vinay talked about how schema changes break your connectors, breaks your change feeds, so what we want to make sure is as our business evolves, as our technical challenges evolve, our contract also evolves with them. Our system, the architecture should not bog us down in figuring out that my contract changes, so I need to rethink my whole design. My design should accommodate the need for evolving our data contract from day one.

## Solution

Now we have these foundations built in, let's see what the solution based on these foundations look like. That brings us to our Write-Ahead Intent Log. Now, one question that may come up is, I've heard about Write-Ahead Log, but what is Write-Ahead Intent Log? If you compare it to a Write-Ahead Log, Write-Ahead Log publishes your dirty keys, your operations, some metadata, and then it also publishes what is the payload that is being mutated. In the case of intent, we don't do that. We don't write the payload to our change feed, and that's intentional because we don't want to, again, go down the path where our data contract becomes embedded into our CDC system. We want our data contract to evolve independently of how we do CDC. That brings us to the first component in our design, which is dumb producer.

My dumb producer, we decouple from figuring out what is the CDC connector, what is the database technology I'm choosing, and just focus on writing my mutations to the log. What that allows me to do is to skip all sorts of validations that I need to perform at the right time, and it doesn't block on any consumer or any final destination for these change feeds to be ready before I can move forward. This is what a dumb producer looks like. You have your application. Traditionally, it connects to the database, but in our case, it connects to this dumb producer, which we call proxy. The proxy takes care of handling the mutation and then writing it to your Kafka, which is our intent and log, and then finally persisting it to the database that you need.

If you notice this diagram, proxy, in this whole flow, never understands what is the data model it is handling. It just works on taking in the mutation and writing it to the appropriate places. This is what we mean by dumb producer.

Now the next question that may come up is, if producer is not handling the complexity, where does the complexity live in the system? Any CDC system, any large-scale distributed system has complexity built in. Whether you see it in one part of the system or another part of the system or as a system as a whole, this complexity must lie somewhere. This is where our complexity lies, which is the smart consumer. Smart consumer is responsible for tracking different topics, different tables, different state of the system. It understands what is your data model, and then it takes actions on those based on whatever business or technical needs your organization may be facing. Moving forward from that dumb producer, that dumb producer wrote your intent to Kafka. This is the intent consumer, which is our smart consumer. It polls for the intent. It goes through that proxy again.

It verifies the state. This is, again, based on the business needs that we had. It verifies the state with the database and figures out whether the intent was actually actualized or not. Then, finally, once it has verified the state, it goes ahead and publishes that event to our event bus. One question that, again, may come up is, where is the data model, where is the metadata that is associated with this event, where does that live? That lives in our schema repository. If you notice, that schema repository is not directly in our data plane path. That allows our schema, our data models to evolve independently of how our consumer handles the change feed itself. If your data model changes, you just need to change your schema repository, handle that failure into your intent consumer, and then your change feed continues to operate.

You don't need to go and update your design or change any connector to accommodate your new data model. In the previous diagram, we had this event bus where we were publishing the final state. Event bus is nothing but a DoorDash internal push-based event streaming solution. If you want to understand at the high level what event bus does, it basically abstracts away the Kafka, the partition, offset tracking for our product teams, and just provide them with a push-based model for any events.

Now we have the basic anatomy of how the modern CDC or this Write-Ahead Intent Log looks like, the next challenge that we talked about was, how does the system, which is simple to build, scale really well? For that, what we built is called a concurrency backbone. Every time you see an arrow or a handoff happening from one component to the other component, that's a chance for you to either bog down your system if it's not designed for scalability or to make it really scalable. What we are doing at DoorDash is basically increasing or making it more config driven on how handoff happens between these different components. For example, if I am expecting or if I am seeing a huge load on a particular table, I can go ahead and increase the number of partitions I have on Kafka.

That in turn can help me in increasing the number of consumers that are attached to that Kafka and help me scale the amount of messages or intents I can process at a given time. What happens if intent consumer has a lot of messages but it can't talk to proxy fast enough? In that case, again, you can increase the connection pool you have for the proxy and scale that independently from how many messages you are getting from your Kafka. Then, finally, when you talk to database, you can scale that with whatever driver you are choosing for your database. Then when you publish your final message to the event bus, you can again scale that independently because, again, that is like a gRPC connection.

To do a recap, this is what we started with. You have an application. It talks directly to your database. You depend on the database blessings to figure out what is going to be your CDC strategy. You publish to one or more Kafkas, and then you have applications listening on top of them which can result in drift if any of those applications or Kafka messages flicker. This is what we ended up with. Application doesn't talk to database anymore. It talks to a proxy. Proxy is our dumb producer. It doesn't understand data model. It doesn't understand your business needs. It just writes to Kafka. It writes to database. Then your intent consumer polls from this Kafka. It handles all the complexity for your business and technical needs, and then it polls from schema to figure out what are the validations or data models you need.

## Learnings

This is all good and fine, but systems don't work like that. There are learnings. Whenever you build a system, someone will always come up and say that I need this thing as well. That's exactly what happened with us. Developers and business don't always want the same thing. They want different failure modes. All of us or most of us have known the problem with dual writes. We are writing to two different systems which are not captured in a single transaction. How do you handle the failures of both of them failing independently? What we do is we hand off this responsibility to our end customers and let them tell us whether they want a transactional or an independent failure. In this case, what we mean by transactional failure is if the write to your Kafka topic fails, we don't write to your database.

We fail the whole transaction, we reject your mutation, and there's no message. Nothing happened. What if the write to Kafka fails but I'm doing something like statistics. I'm tracking the number of stars I got or number of YouTube counts I got. I don't necessarily need to fail my database transaction in this case, I can have reconciliation at the end of accounting period, I can have a tail on the database going forward. In this case, I can independently fail. I don't need to fail my database transaction just because I was not able to write my intent. Again, this is something that you can derive from your business and from your technical use case of how you want to solve problems for your business. Quick question, what happens if the write to Kafka succeeds but write to database fails?

We can, but in this case, our customer or consumer already verifies the state. When it verifies the state, it knows that the intent actually never materialized, so it rejects that message and moves forward. You don't need to handle that case. Again, this is very business specific. If you need to, you can go ahead and handle that event according to your business needs.

We have all this Kafka and database but one question that comes up is, what happens if my table doesn't fit with other tables living on the same broker? What happens if my consumer doesn't talk to the same Kafka topic? What we built is a dynamic traffic reshaping which allows us to scale these tables or move them to different Kafka topics as we see fit. This is what we started with. We have an application, writes to proxy, writes to database. You have seen this diagram multiple times now. This Kafka is really weighing down. We have a table doing millions of QPS and there are other tables on this Kafka causing noisy neighbor issues. What we do is we spin up a new Kafka broker. We attach a new intent consumer. It follows the same business rules because everything is being derived from the schema registry.

There is nothing inherently happening in that intent consumer which other intent consumers can't know. Once we have all that set up, we allow proxy to talk to that Kafka. The way we do that is we publish a routing info to this proxy. We tell the proxy that, ok, for this table, instead of talking to this Kafka now, you need to talk to this new Kafka which understands the new table semantics, and anything which was preexisting in the old Kafka broker, all the messages which were not consumed, they can still be processed by the same intent consumer but any new message won't be published to the existing Kafka. Another problem that we have is now how do you scale different sinks or different consumers that you have on top of these event bus topics.

For us, the solution is simple because now since we have decoupled our database from our CDC pipeline, we can scale or attach as many number of CDC consumers as we want on top of that event bus. Since event bus is responsible for push-based mechanism, it allows us not to worry about partition handling, when should we compact our broker or topic, and allows event bus to continuously move forward.

## Key Takeaways and Considerations

What are the key takeaways? In traditional CDC, we talked about the issue of abstraction where different databases talk different languages which make it harder to standardize on a single way. The scalability is a concern because your change feed is tightly coupled to your database itself so the change feed is running on the actual pod so you can't scale that really well. You have vendor lock-in, you are dependent on what is the change feed mechanism that a particular database provides. If a database doesn't have a change feed mechanism, you can't do anything. Then, finally, once that CDC change is broke down, how do you move forward? How does your application recover? That's all the challenges that we saw in the traditional CDC. Then the modern CDC helps answer some of those questions. The design itself is evolvable.

You can pick and choose the parts that suit your needs rather than fixating on one particular aspect of any particular design. It offers you high leverage. Since we have these reusable components in form of intent consumers and schema logs, you can move things around. You can increase the leverage you have from the overall architecture. You can share resources. You can optimize things. Then, finally, it is very loosely coupled with your whole environment. It doesn't matter what database you are using, what streaming solution you are using, you can follow the same architecture principles to build the change data capture around that.

No system is perfect. Again, this is not a perfect system. We have some tradeoffs. A couple of tradeoffs that we want to talk about is read your write semantics. In the consumer, we saw how you have to go back to your proxy to verify the state. That leads you to a read your write semantics, where for each intent or each mutation, you are doing at least one readback to your database before you even publish that message to any other client. One thing that you may have noticed is what happens if multiple writes are chasing or racing with each other when sending out to consumers. In this case, what this modern CDC allows you to do is to capture state instead of any individual change data field. In our case, that's an acceptable solution.

Not every time do you need to capture the actual change that happened. Most of the times, product teams or applications are interested in what is the latest state of the system rather than what was changed to bring the system to this state. Then, finally, when you're verifying the state, how do you make sure that the write actually failed? I should just reject this intent, or is it just delayed enough that I can't verify its state? That is, again, something you can negotiate with your technical or business team to figure out what is the right amount of waiting period for your application.

## Summary

Tying it all together, how performant is the system? Since the dumb producer is dumb, it doesn't understand data model, it doesn't need to do any kind of validation. It allows your database to remain performant. You can get maximum power out of whatever database technology you are choosing because it doesn't have to worry about extra stuff around CDC management. Each component has single purpose. Proxy has a single purpose of pushing everything out to Kafka or your database. Your consumer has a single purpose of polling from Kafka and then figuring out what is the schema validation I need to do, and then just pushing it. Then event bus is responsible for making sure that each sync gets the latest state from the system. It is cost effective because now, since you have different Kafka brokers, different consumers and proxies, you can do a just-in-time scaling.

If you need to increase the amount of writes you are processing, you can just scale the proxy and Kafka to handle those writes. If you are also concerned about the delay in processing those intents, you can increase your consumers just in time to accommodate those scales. Then scale it back once that need is over.

## Questions and Answers

**Participant 1:** At what level of scale did you start to see the Debezium connector break down in terms of quantity, like volume of data or transactions?

**Vinay Chella:** What are the struggles that we have seen with the Debezium connector?

**Participant 1:** Yes, at what level of scale did you see it start to break down in terms of data volume and transactions per second?

**Vinay Chella:** Especially when we did the load testing with the Debezium, we especially used it for Cassandra. As we are scaling up Cassandra, Debezium was consuming a lot of CPU from the main process, and Debezium connector, especially when it is operating in a multi-region mode, it ends up leading to out-of-order writes. Our latencies were almost getting doubled, and being too much hungry for the CPU, it's costing our Cassandra process to starve for CPU and leading to the availability SLOs.

**Participant 2:** My question relates back to that scenario that you called out earlier, where the write of the intent succeeded, but the database write failed. My question elaborates a little bit more on that scenario. I want to ask, what if the application under that scenario wants to also have or execute some form of graceful service degradation in such a scenario where it could say, fall back to another service, which provides a less good experience of the same service or instructions to a user to manually bypass, something to that effect where you somehow lessen the impact. My question then is, in this scenario, does the proxy relay information back to the application about this failure to thereby give it that opportunity to make that decision?

**Vinay Chella:** Yes, absolutely. When any of these failures happen, proxy in its response would tell whether it is persisted, whether the intent log is persisted or not, so that response code would have those details and the services could take appropriate action as the need. This also operates at a table configuration level. When you're configuring a table in proxy, you design it to say, you want transactional model or independent model and take required actions.

**Participant 2:** Based on your value mode you can react to it accordingly.

**Participant 3:** I have a question about the proxy. Is it a singleton in terms of single writer? You can have multiple applications writing to the proxy but you always write in order, one at a time to the Kafka queue?

**Vinay Chella:** The proxy internally is called Taulu. It's a key-value abstraction on top of this database. It's a distributed one. It uses the write intention time log that is synchronized across all of the proxy instances, and that timestamp is what gets carried to Kafka and that timestamp is what gets persisted to your database as well.

**Participant 3:** It's the timestamp of the proxy itself.

**Vinay Chella:** Correct.

**Participant 3:** Then one related question is, if data lineage is important, how would you change this to also capture ordering as well as the exact changes that are made and not just the final state?

**Vinay Chella:** Unfortunately, the ordering is not guaranteed. The ordering is guaranteed by the timestamp that is being maintained in the proxies. We intentionally choose not to read before write on the path of write to really know what has changed. In a traditional CDC, there is a pre-image and post-image when you get that log from traditional databases, you see the pre-image and post-image then you can reconstruct. That isn't part of the system.

**Participant 4:** My question was related to the proxy service talking to the database. There could be a case where you would have more than one kind of data source where the data needs to be persisted. How does the proxy maintain that information based on the request from the application to understand where this request needs to be persisted?

**Vinay Chella:** That's part of the table metadata. There is a table metadata which says what is the type of table, whether it should be persisted in a system like Redis or Cassandra or Postgres, and that table metadata enables us to know where to persist the data.

**Akshat Goel:** When we publish this routing info to proxy, so this doesn't only have the info about the new Kafka, it also contains the info about the database.

**Participant 5:** I remember in the beginning of the talk, it is mentioned that the proxy writes the intent, it actually does not include the payload. Where in this path where the payload is picked up, and I assume the payload is eventually sent to the event bus?

**Vinay Chella:** Yes, correct. The intent consumer is the one which picks up the payload from the database and puts it in the event bus, and that is abstracted away with all the complexities. The payload is big. There's a flexibility for us to put the payload in S3 and put the pointer in the event bus. That decoupling is abstracted away for us.

**Participant 5:** In that case, for each write, there's an intent which is persisted into Kafka. The intent consumer needs to read from the database to pick up the payload. Will that cause any issues, like it adds extra workload to the database, because each write now has to incur a read on the database in order to do the CDC.

**Vinay Chella:** That's one of the considerations we put. We intentionally chose that design to have the read after write scenario. These are the ideas that we have in the future as we hit into those scale limits, like if you are using a traditional database, you can always extend to your read replica, with the intent consumer talking to proxy, we intelligently route that request so that your main traffic doesn't get interrupted. If you're using distributed no master databases like Cassandra, you can always lean on having one data center which its only job is to respond to this proxy. We haven't seen that yet as we are still rolling out, but those are the ideas in our back pocket.

**Participant 6:** How do you deal with when the intent consumer consumes something from Kafka but that's not being written yet to the database? That could happen because they are independent. We just retry, or how does that work?

**Akshat Goel:** We do retry and we let our customers choose how long should we retry. By default, we allow up to 10 seconds for that message to be visible or that write to be visible. You can choose how long should a particular message be retried when we are verifying the state. After that point, we consider that write failure.

**Participant 7:** With the intent consumer, you're receiving the pushes onto Kafka, but then you then have to check the database. That may not have already happened yet or various other things that you then have to check. How do you make sure that that stays still in a push mindset instead of just pulling that database?

**Vinay Chella:** There are several things that we consider as part of the intent consumer. One is the timestamp that metadata has carried. We check the database with that particular timestamp to see if it is something old or if it is the latest state. Get that and put it onto event bus. Event bus is the one which takes care of pushing it. Event bus by design is a push-based approach with all the CDC consumers who subscribe to event bus, would get notified with these changes.

**Participant 8:** What is intent?

**Akshat Goel:** In our case, intent is just the dirty keys and the operation and the metadata around the table. It's val without the payload. That's our intent.

**See more [presentations with transcripts](https://www.infoq.com/transcripts/presentations/)**