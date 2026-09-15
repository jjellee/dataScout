---
ticker: MDB
company: "MongoDB, Inc."
title: "MongoDB, Inc. The Six Five Summit: AI Unleashed 2026 Earnings Call Transcript"
published: 2026-08-25
quarter: "FY 2026"
event_id: 738843
source: stockanalysis
source_url: https://stockanalysis.com/stocks/mdb/transcripts/738843-the-six-five-summit-ai-unleashed-2026/
audio_url: https://files.quartr.com/audio-files/dbdb44476d68d68c80b70048d0eed540-2026-08-26-19-22-26.mpeg?ref=U0E=
---

# MongoDB, Inc. — The Six Five Summit: AI Unleashed 2026 (2026-08-25)

## 요약(stockanalysis 자동 생성)

### Evolution of enterprise data infrastructure for AI

- Enterprise data architecture is shifting from static, deterministic code to supporting autonomous AI agents that perceive, reason, and act dynamically.
- Early attempts to integrate generative AI with legacy systems led to operational challenges, highlighting the need for unified data platforms.
- Flexibility in data models is crucial, as agentic applications require evolving schemas and seamless adaptation to changing requirements.
- Real-time operational signals, historical records, and explicit business rules must be unified to provide trustworthy context for AI.
- Databases are evolving from passive storage to active orchestration layers, directly influencing application behavior.


### Importance of context and memory in AI agents

- Reliable AI agents depend on access to high-quality, real-time context, not just raw data.
- Integrating operational context enables AI to make smarter, business-impacting decisions, as seen in reduced unnecessary dispatches and downtime.
- Statefulness and memory are essential for agents to handle complex, multi-step processes and maintain continuity over time.
- Large-scale AI deployments require databases capable of supporting billions of conversations with sub-millisecond latency and zero downtime.
- Consistency and reliability in agentic applications build trust and enable enterprises to use AI for core operations.


### Customer use cases and operational value

- Organizations are moving beyond experimental chatbots to deploy agentic workflows in mission-critical business processes.
- Success is driven by real-time performance and architectural flexibility, enabling sub-second responses and massive data throughput.
- Flexibility in deployment allows agents to operate across clouds and on-premises environments without rewriting functionality.
- Hybrid data sourcing, including public and partner data, is increasingly common in enterprise AI use cases.
- Resiliency, fast throughput, and low latency are key to supporting millions of transactions and autonomous agents.


### Practical steps for AI readiness

- Avoid proliferation of niche databases and point solutions to minimize synchronization, security, and technical debt risks.
- Build an operational data layer in front of existing systems to unify and enrich data without replacing legacy databases.
- Use flexible platforms to generate vector embeddings and provide secure, contextualized data to AI agents.
- Connect unified data layers to models and enterprise data using established standards for seamless integration.
- This approach enables organizations to prepare efficiently for scalable, production-grade AI applications.

---

## 전문

**Jason Andersen**  
*VP and Principal Analyst / Moor Insights & Strategy*

Hello, and welcome to The 2026 Six Five AI Summit: AI Unleashed. Today, we're continuing the data and observability track. I'm Jason Andersen, and today we're exploring how enterprise data infrastructure is evolving to support the next generation of AI applications and agents. I'm really excited to be joined today by Ashish Kumar, SVP and Technical Fellow at MongoDB. What we're going to be discussing over the next few minutes is why context, and not just data, is becoming the key to building not only reliable AI agents, but also highly scalable AI agents. Thank you for joining me, Ashish. Welcome to the show. I'm glad to have you here.

**Ashish Kumar**  
*SVP and Technical Fellow / MongoDB*

Great to be here, and I'm excited to talk about how enterprise data architecture is needing to change with these rapid advancements we see in AI. How the conversation has shifted from which models we have to use to the trusted context these models need in production.

**Jason Andersen**  
*VP and Principal Analyst / Moor Insights & Strategy*

Perfect. You're the right guy. You've been doing this data stuff for a long time, so I'm really excited to dive right in. What changed in the market that made the evolution necessary, and why is it especially relevant as organizations begin the AI and agentic buildup?

**Ashish Kumar**  
*SVP and Technical Fellow / MongoDB*

Great question, Jason. If you look back, MongoDB started as a database developers loved because it made building apps fast and intuitive. What really shifted in the market is that software itself is changing. We're moving from this static, deterministic code to these autonomous AI agents that are perceiving, reasoning, and acting on the fly. When generative AI first exploded, a lot of teams reacted by pulling together the standalone vector databases onto their legacy stacks. Pretty quickly, that became an operational nightmare of data sync issues and latency. Organizations realized that in order to run AI in production, you cannot have your vector sitting in one place, your operational data in another place, and your security rules somewhere else. You need a unified platform. It's not just about running AI, it's about how software is being built. Emergent Labs is a great example of why flexibility matters here. They are one of our customers. They tested Postgres first but decided on MongoDB Atlas because when agents are building applications, the data model is constantly evolving. See, with Atlas, the schema evolves right alongside your application rather than forcing you to run migrations every time something changes. That is why they have been able to power around 2 million agentic applications on MongoDB.

**Jason Andersen**  
*VP and Principal Analyst / Moor Insights & Strategy*

Wow. It is funny you mentioned about the fluidity of data and how data evolves over time. The attention level we have seen so far on what we will call the foundation and frontier models has been enormous in this space. But as we are seeing enterprises start to wade into this in a more meaningful way, like Emergent, we are starting to see that it is not just about the models. It is about performance and context and really making these things work in a very customized way for those organizations. When we think about context in general, how do you define what makes for good context, and why is it such a critical ingredient in the mix?

**Ashish Kumar**  
*SVP and Technical Fellow / MongoDB*

Yeah. I think of foundation models as these very brilliant reasoning engines, like the Einsteins of the engineering world. But without context, they know zero facts about your actual business. The way I define good context is pretty simple. Bring together real-time operational signals with historical records and explicit business rules into something that can be together consumed by the AI that it can trust. If you feed these models raw text without that operational context, it is just making educated guesses. But when you give it real context, it can actually make smart decisions. Another customer of ours, AT&T, is a great example of this. They are bringing together real-time network signals with historical outage data, so combine all of that together so their AI can make better decisions about where repair crews actually need to go. That has physical implications. That is real business impact. In their case, 3.1 million unnecessary dispatches avoided, $12 million-

**Jason Andersen**  
*VP and Principal Analyst / Moor Insights & Strategy*

Wow.

**Ashish Kumar**  
*SVP and Technical Fellow / MongoDB*

...of downtime saved. When an agent is dispatching physical crews or touching billing systems, bad context isn't just an inconvenience or minor hallucination. It's a massive financial impact.

**Jason Andersen**  
*VP and Principal Analyst / Moor Insights & Strategy*

Yeah. Wow. When you start to think about these impacts, and you start to think about context as a part of it, one of the things that I was doing when I was preparing to talk to you today was to look at some of the things you've been writing. MongoDB does a nice job of educating the market in terms of the blogs and the research you publish, and I know that's a big part of your role. When we get into things like statefulness of AI and memory, which is now becoming a much hotter topic. These things are getting increasingly important, especially as we get towards production-grade applications. When we think about this, how does that drive reliability? Ultimately, how does reliability help organizations adopt better, or feel more confident and trustworthy of what AI is able to deliver, maybe is a better way for me to frame that up.

**Ashish Kumar**  
*SVP and Technical Fellow / MongoDB*

Yeah, look, I like to say agentic applications, everybody's building them. But an agent is only as smart as the context it has access to.

**Jason Andersen**  
*VP and Principal Analyst / Moor Insights & Strategy*

Okay.

**Ashish Kumar**  
*SVP and Technical Fellow / MongoDB*

An agent without memory is really just an expensive chatbot. You are talking about general knowledge and whatnot. It cannot hold onto a thread, it cannot learn, and agents now need to handle complex multi-step processes. Without memory, it just cannot do that. When we talk about state and memory, we are talking about an agent's ability to maintain this continuity. Remembering what happened three steps ago, keeping track of what the user was trying to accomplish, and then remembering their user preferences over time. If you want an agent to handle a process that takes three days and requires five different approvals, it has to hold onto that state without dropping the ball. Doing that at scale, though, immense data problem. That is a core data problem. A great example is one of the top frontier AI labs actually moved more than 50 billion conversations off Postgres and onto MongoDB Atlas in just four weeks to solve this.

**Jason Andersen**  
*VP and Principal Analyst / Moor Insights & Strategy*

Really? Wow.

**Ashish Kumar**  
*SVP and Technical Fellow / MongoDB*

That is AI model, unbelievable scale. Hundreds of petabytes of conversational state that has to stay available with sub-millisecond reads and zero downtime reported. When you anchor an agent's memory in a database built for that kind of scale, you are taking out the unpredictability. That is how you build agents that enterprise can actually trust with core operations. It has to give you the same answer with the same inputs, and something that customers can vouch.

**Jason Andersen**  
*VP and Principal Analyst / Moor Insights & Strategy*

Right. I think that's been one of the, kind of as a side note here, that's been one of the challenges I think we've seen with customers ourselves, my research is the consistency gap. They're so used to 60+ years of deterministic applications, and they're like, "Well, I want it to be the exact same output every time." Well, that's when you build a deterministic application, but the world isn't as black and white as that, which is where agents add a lot of value. I think it's an interesting kind of expectation reset as well as a technology reset.

**Ashish Kumar**  
*SVP and Technical Fellow / MongoDB*

That's right, Jason. This is an exciting time because what we're seeing is databases, that's an area that I work in. I enjoy databases. I've loved them for a while. Infrastructure software is my game. What I'm finally seeing is that databases, which used to be these passive entities that people, you write an application, you decide a schema, and then you read and write into the database. They're now getting up-leveled into being part of this application stack. They're directly-

**Jason Andersen**  
*VP and Principal Analyst / Moor Insights & Strategy*

Right.

**Ashish Kumar**  
*SVP and Technical Fellow / MongoDB*

...making orchestration. They're actually determining how your application works. That's the beauty of this. That's why these are exciting times for people like me.

**Jason Andersen**  
*VP and Principal Analyst / Moor Insights & Strategy*

Let's take that thread and extend it a little bit. You've mentioned a couple of customer scenarios already, which is always super helpful for people who tune into these sessions. When you're talking to customers or when your team is talking to customers, what are the things they're, what's exciting them the most in terms of what they're getting? You mentioned cost savings a few times and deferring bad service calls. But in terms of where organizations are getting the greatest value from great context, what's getting them excited where they're coming back saying, "I love this stuff, and here's why"?

**Ashish Kumar**  
*SVP and Technical Fellow / MongoDB*

Yeah, I think, for the longest time, I say longest, all of this has been developing over really the last 18 months, especially with agentic AI that is coming in. What we are seeing, though, is that companies are now starting to move past the science project chatbots and building agents that are driving real operational value. I have talked to perhaps 100-odd customers over the last nine months, MongoDB customers that are building these applications. As I talk to them, I am realizing that they are bringing these agentic workflows directly into their core mission-critical business processes. The organizations that are seeing the most success are the ones that are focused on two things. One is real-time performance, and the second is architectural flexibility. On the performance side, it is all about sub-second responses. Essentially, you now have this army of agents that are going to be accessing this data. They are going to be accessing conversational state, conversational history, memory, enterprise context. They need to be able to do semantic searches, full-text searches, and access this on live operational data so they can operate with current. They need to operate instantly. They cannot deal with historical data at this point. Being able to support this massive spike in reads and writes in real time is something that an operational data layer can provide. The second piece is this idea of having the flexibility of deployment. That value is equally important. One of our customers, as an example, Macquarie, is a great case study for why this matters. They built this retail business payments platform that needs to be always on, and they did not want to get themselves locked into one specific cloud provider. MongoDB Atlas, as you know, our ethos is around providing that open-

**Jason Andersen**  
*VP and Principal Analyst / Moor Insights & Strategy*

Right.

**Ashish Kumar**  
*SVP and Technical Fellow / MongoDB*

...flexible environment. Atlas gave them that portability while they scale to supporting millions of transactions. At the end of the day, you see, whether you are running payment systems, autonomous agents, the value eventually comes down to resiliency. Fast throughput, low latency, and the freedom to run wherever your business needs to be. Especially, I talk to a lot of customers. Many of them, as an example, have pinned themselves. They have decided that they are working on one cloud. But when I talk to them, they realize that agents now need to run close to wherever the data is. Their data, they might be working with customers that run in a different cloud. Now they need to run the agents over there, or they might have applications that need to run on-prem in a, perhaps in an air-gapped network. They need to run the agents there. You don't want to write the same agent functionality three times. You want to have the same agent run unchanged in all these environments. That's the power of having this complete flexibility and openness.

**Jason Andersen**  
*VP and Principal Analyst / Moor Insights & Strategy*

It's an interesting point because there's also, you're starting to see the notion of data sources changing in terms of, you had kind of internal data and then data maybe you shared with a trusted partner. But now people are going and getting data from, say, Google Maps, photographic sources to do things. I just heard of a case where a waste management company was looking at dumpsters just to see the sticker to see who the competition was. They'd go into a town, and they would just scrape data from maps. That's an absolute hybrid case, right? Because that's just publicly available stuff. There's a lot going on there for sure.

**Ashish Kumar**  
*SVP and Technical Fellow / MongoDB*

Absolutely. These are exciting times, Jason, for sure. Yeah.

**Jason Andersen**  
*VP and Principal Analyst / Moor Insights & Strategy*

Let me just ask you a final question. To your point, it's exciting times, right? People are, I think, starting to wake up, right? They're starting to realize, "I need to get things into production. I see the benefits that other customers are having. I want a piece of that," right? Maybe they're realizing that when they look at their data architecture, they're not quite there yet, right? What's the first practical step a company should take when they're looking at this? Where do they get started? Obviously, they could call you guys up. I'm sure you could help. But just in terms of a practical step and in terms of just starting the readiness process, what do you think?

**Ashish Kumar**  
*SVP and Technical Fellow / MongoDB*

Look, I think single biggest piece of advice, stop the sprawl. I've been saying that for a long time, but I think now-

**Jason Andersen**  
*VP and Principal Analyst / Moor Insights & Strategy*

Okay.

**Ashish Kumar**  
*SVP and Technical Fellow / MongoDB*

...it's becoming even more real than ever. Resist the urge to going to buy another niche vector database or a single-purpose tool just to get a quick AI pilot off the ground. Every time you add another point solution, you're creating this synchronization lag, security risk, technical debt. I've lost a bunch of my hair dealing with all of that, and I can tell you enterprises are struggling with this today.

**Jason Andersen**  
*VP and Principal Analyst / Moor Insights & Strategy*

Okay.

**Ashish Kumar**  
*SVP and Technical Fellow / MongoDB*

The sooner they realize that, the better it becomes. So instead, what they should do is start by building an operational data layer in front of what they already have. You don't need to keep-

**Jason Andersen**  
*VP and Principal Analyst / Moor Insights & Strategy*

Right.

**Ashish Kumar**  
*SVP and Technical Fellow / MongoDB*

...you don't need to sort of clear out your legacy databases or anything. They can stay. But you need, I think, Jason, you've described it as a system of action previously, right. So you need-

**Jason Andersen**  
*VP and Principal Analyst / Moor Insights & Strategy*

Yeah.

**Ashish Kumar**  
*SVP and Technical Fellow / MongoDB*

...a flexible platform that pulls that data together, enrich it with the metadata that you need, generate your vector embeddings right where that lives. And now you can provide that context directly to your agents with the proper metadata, with the proper security and guardrails that makes it available. And you can connect that unified data layer to your models, and to your enterprise data with MCP and other standards that are available already. It's the cleanest, most practical way to get ready for this future.

**Jason Andersen**  
*VP and Principal Analyst / Moor Insights & Strategy*

Perfect. That's great advice. I think it's great, good cross-industry advice right there. So Ashish, thank you for your time, and thanks to everybody else for tuning into this data and observability spotlight at this year's The Six Five Summit. Don't forget to subscribe, follow us on the socials, and check out all of our summit coverage at sixfivemedia.com/summit. And we'll see you next-
