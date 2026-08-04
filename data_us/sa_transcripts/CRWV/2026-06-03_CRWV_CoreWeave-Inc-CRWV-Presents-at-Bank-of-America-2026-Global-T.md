---
ticker: CRWV
company: CoreWeave, Inc.
title: "CoreWeave, Inc. (CRWV) Presents at Bank of America 2026 Global Technology Conference Transcript"
published: 2026-06-03T16:41:59-04:00
article_id: 4911609
source_url: https://seekingalpha.com/article/4911609-coreweave-inc-crwv-presents-at-bank-of-america-2026-global-technology-conference-transcript
---
CoreWeave, Inc. ([CRWV](https://seekingalpha.com/symbol/CRWV#source=section%3Amain_content%7Cbutton%3Abody_link "CoreWeave, Inc.")) Bank of America 2026 Global Technology Conference June 3, 2026 1:40 PM EDT

**Company Participants**

Nicholas Robbins - VP of Corporate Development & Investor Relations

**Conference Call Participants**

Tal Liani - BofA Securities, Research Division

**Presentation**

**Tal Liani**  
*BofA Securities, Research Division*

I'll start. I was asked to present myself. My name is Tal Liani, and I'm the analyst that covers CoreWeave. Here we go. It's for the transcript.

So Nick, thank you so much for joining us. Your stock has been terrific, and we have a few questions about your position in the market, your longevity. I -- because this is the first time I interview you in this kind of setup, just I want to start with 30 seconds what we think about the space and your company, and then we'll go to our Q&A. That's what I'm doing in all these kind of sessions.

So we recently launched with a buy rating on all 4 data center companies. We call them the GPU companies, CoreWeave, Nebius, Oracle and Microsoft. And the reason why we had a buy is -- on all 4 names is because we have a terrific cycle. This cycle, I don't see -- at least at this point of time, I don't see the sign of slowdown. We're going to talk about it. We're going to ask about it. Hopefully, this thing is okay.

Here we go. And what I want to focus on in this discussion, I want to focus on the differentiation of CoreWeave. I want to focus on the value you bring to market. I want to focus on the longevity of -- and visibility of orders and things like that.

**Question-and-Answer Session**

**Tal Liani**  
*BofA Securities, Research Division*

And the first question I have is what makes you different? What is the difference between the way you are structured and the way that hyperscaler is structured from a conceptual point of view?

**Nicholas Robbins**  
*VP of Corporate Development & Investor Relations*

Absolutely. And I think what makes us stand out, there are a few things that are absolutely true and then there are a few things that are relatively true, right? And it's, okay, are you comparing us to Microsoft? Or are you comparing us to a smaller neocloud, right?

In the context of comparison to hyperscalers, it's the technology stack. It's fundamentally what we did on a first-principles basis is rearchitect the way that cloud stack is built. And the reason we did so is AI cloud is based on a different type of workload. It's based on parallelized compute, which is quite a bit different than the way CPU workloads historically were based, which is serialized compute.

Serialized compute is -- the concept is built for redundancy. The workload is small enough, it's going to be run on a CPU over here. And if that CPU breaks, I'll run it over here. And so I'll be able to serve the problem no matter what. Parallelized compute is the workloads are really big. And so actually, what you're going to do is you're going to have a bunch of GPUs working together on a single problem. The challenge with that is when the GPU breaks over here, it can't be replaced over here. The entire system is down, right?

And we built the technology stack geared towards optimizing a few different things, which are, one, the efficiency of the overall ecosystem, right? We effectively ripped out the virtualization layer that lives in a hyperscaler's cloud stack. But on top of that, we built a proprietary orchestration layer that's gotten uniquely good at provisioning GPUs of understanding are they healthy or not, of predicting when they might not be healthy and ensuring the workload remains safe.

And you combine those 2 things and you end up with a cloud stack that is more performant. And what that allows you to do is, one, be kind of the cloud partner of choice for virtually every sophisticated user in this ecosystem. And I think we're the only independent cloud company that does service both OpenAI and Anthropic and Meta and Google and Microsoft and NVIDIA and the next layer down, whether you want to call that a Cursor and a Cognition and Perplexity or a Cohere and Mistral, right? Like we're pretty singular in that capacity because of the unique quality of what we can deliver. And what it also allows you to do economically is ultimately charge a higher price per GPU hour while still delivering a lower TCO to your customer because you are delivering a much more efficient and performant product.

**Tal Liani**  
*BofA Securities, Research Division*

When I first -- I interviewed all the companies because I had to launch coverage and I spoke with Microsoft, the first thing they told me when we spoke about the space was this is a temporary solution. When we build enough data center capacity, we'll bring all the capacity in-house. What's the risk of you being a temporary solution versus a permanent solution?

**Nicholas Robbins**  
*VP of Corporate Development & Investor Relations*

I think highly limited. And I think it's highly limited for a litany of different reasons. One, I think that the hyperscalers were the first large consumers of this infrastructure, but that is not the steady state of this. Already, you have OpenAI and Anthropic rivaling just how much compute they want to consume relative to a Microsoft. Already, you have a long tail of enterprise customers looking to consume directly, right?

Already, you are seeing like even our reliance, like when we went public, Microsoft was 85% of our revenue backlog, right? Today, they're not even our largest customer, right? They're not even our second largest customer, right? And so the natural diversification that has come into this industry has diversified away that risk. On top of that, the way I kind of think about the renewal problem because I've been getting this question, particularly with regard to Microsoft since 2023, right?

And I got the question as an adviser to the company. I got the question as an investor of the company. And now I get the question as an employee of the company, right? And the way I look at it as I try to study the history of the cloud in general. And 2 observations I've made that no one has really pushed back on yet are, one, I am not aware of any point in time in the history of the cloud when a hyperscaler has chosen to actively reduce their data center footprint of revenue-generating data centers. To not renew is to shrink.

That seems to defy the history of the cloud. The other part of it is using the CPU cloud as the analog. If you look at the Azure portfolio of data centers for CPU, a lot of it is owned and some of it is leased, right? I think the steady state of GPU cloud or AI cloud looks like a lot of it is owned and some of it is leased. The core difference being when you were building CPU cloud, about 2/3 of your cost was the shell itself and about 1/3 of the cost was what goes in the shell.

When you build AI cloud, it's the inverse, right? 2/3 of the CapEx goes towards what goes inside and about 1/3 is the shell itself. So I think it stands to reason that for the portion of a hyperscaler book that is leased that they probably are going to want to not only avoid the CapEx of the shell, but avoid the CapEx of what goes inside given it's twice as expensive. So you put that all together, and frankly, that is just not -- that's not the thing that keeps us up at night.

**Tal Liani**  
*BofA Securities, Research Division*

Got it. Let's talk about visibility. Spending CapEx growth has been phenomenal for the last 2 years, including this year. How confident you are that this spending cycle continues? And I know we don't have the answer. I'm trying to get to your thinking process, meaning what are the drivers?

**Nicholas Robbins**  
*VP of Corporate Development & Investor Relations*

sure. So I do come back to what are the drivers and how we think about it or maybe even slightly different things. What are the drivers? It's adoption and productivity expansion, right? And you're seeing so much of it happen this year right now, right? If you look at the growth of the Anthropics of the world, right, and the OpenAIs of the world, like you are seeing enterprise adopt, you are seeing AI diffuse. We are seeing it show up in our pipeline with a long tail of enterprise customers who want to consume this technology directly as opposed to indirectly.

The how we think about it is directly informed by the pipeline, right? In so many ways, our business benefits from a flywheel that starts with the fact that we uniquely serve and are the trusted engineering partner to virtually all of the sophisticated users and consumers of this technology in the world. We understand where they want this to go, and we build towards it. The anecdotes I would give you are back in 2023 and early '24, we were building with InfiniBand.

And a lot of people were saying, why are you spending all this money on InfiniBand? All the hyperscalers just build with Ethernet and they say it's cheaper and they say it's just as good, right? And models are going to get quantized down to a single GPU or a fraction of a GPU. And what do you need all this dense network fabric for? And then what happens in September of 2024? O1 comes out. And all of a sudden, you have inference being run not on a single GPU or even a single node, but across nodes. And you need a denser network fabric to run that efficiently, right?

And all of a sudden, building so much with InfiniBand almost seemed clairvoyant, right? Like I would say a similar thing about focusing our kind of efforts on procuring liquid cool data center capacity back in 2024, right, building ahead of GB coming out in 2025. We've made very similar investments and bets in the portfolio across things like storage and CPU to position ourselves to take advantage of those tailwinds over this course of this year and next.

And I would say a similar -- like we're doing that because we know what the customers are going to need. We are working closely with them, and they are telling us because they want more from us because of the quality of what we deliver. And what they are telling us is this is not going to slow down. And frankly, they're telling the world that, right? Like in 2023 and 2024, even for a lot of last year, it seemed almost contrarian to believe that this cycle was going to continue and in orders of magnitude larger, even though Jensen and Elon Musk and Sam Altman and Dario Amodei and Satya Nadella and Sundar Pichai and all these people were telling you it would, right? Like just believe them, right? Like they're telling the truth.

And like what is a better data point of that than Google raising $40 billion yesterday, right? And like who had on their bingo card that Google is going to be raising equity securities this year in tens of billions of dollars of scale. I think that there's no one. Why are they doing that? It's not because they intend on slowing down anytime soon.

**Tal Liani**  
*BofA Securities, Research Division*

Got it. Another question we're getting a lot is about understanding the business model, meaning people ask me about unit economics. And so -- but I'll start with a kind of high-level question. What's your business model? How -- when you sign up a customer, how do you think about the first period, renewal, other customers? What value can you extract from a GPU?

**Nicholas Robbins**  
*VP of Corporate Development & Investor Relations*

Yes. And so I'll speak to the core business model and how it's evolving over time. The core business model, and you got to think about where we got started is you sign longer-dated contracts with customers where they're contractually bound to pay you a fixed price per GPU hour regardless if they use it or not, it's called the take-or-pay contract for the next 4 to 6 years.

Why did we start there? We started there because to build a cloud business is equal parts technology and infrastructure. Scaling technology often comes without capital intensity. Scaling infrastructure never comes without capital intensity. And so to build a hyperscale business, which is our aspiration, and arguably, we're there already. We're more than 1 gigawatt of active power at this point in time, right?

But to do that, part of the name of the game is you want to be able to have as much access to capital as possible at the cheapest price imaginable, right? And signing these longer-dated take-or-pay contracts, taking them to the asset-level financing market has been a way where we could borrow capital at costs that are way closer to our customers than our own, right? And that is how you build scale as quickly as we have.

I would say we are the only company in the world in this ecosystem that has built the scale that we have as quickly as we have. No one is even close, right, who didn't have an investment-grade balance sheet to begin with, right? Like we are singular in that world. And so you got to start, right, with that core foundation with the beauty of it being, hey, a 5-year contract is going to pay for all the financing costs and all the CapEx associated with standing up that cluster. It's going to cover all of the OpEx during the life of that cluster, and it's going to pay for another 5 years of data center expense on top of that.

And so what you're buying yourselves is -- or what you're positioning yourselves for is 4 years from now, 5 years from that initial contract, you're going to own infrastructure that is your own to monetize. And every dollar you get out of it is just cash flow accretive to what you paid initially. And being in control of that massive infrastructure that is of critical importance is incredibly valuable.

So that's been the foundation for a while. It will continue to be, right? But what we've been able to do as we've gotten bigger, right, and access to capital has gone up and cost of capital has gone down is we've been able to position the portfolio, right, to include some shorter-dated contracts, too. And we like shorter-dated contracts, right, in that what it exposes you to is a higher margin, a higher ASP, right?

If you're committed for fewer years, you're willing to pay a higher price. And what it allows you to do is to take advantage of the increasing demand for this technology such that, hey, a contract 2 or 3 years or a piece of [indiscernible] 2 or 3 years from now might be more valuable and you might get a higher price than what you're charging today. That's been our experience with Hoppers, right? We're selling Hoppers today at higher prices than we were 3 years ago. And the reality is no non-investment-grade business can build a hyperscaler of on-demand product without diluting their shareholders by like 80% or 90%, right?

Like you just can't do that, right? But as you get bigger, you get to twist the dial a little bit and that positions us to better take advantage of repricing existing infrastructure of selling more on spot over time. And that is why in Q1, we announced our spot product, right? Like we are getting to the point where we are hitting escape velocity and we're able to take advantage of those market dynamics better at scale.

**Tal Liani**  
*BofA Securities, Research Division*

Yes. What happens to the value -- what happens to the GP -- so there is an initial -- I'm talking about the big contracts. There's an initial contract, let's say, 5 years. What happened -- what is your margin during that time? And what happens after that with the residual value?

**Nicholas Robbins**  
*VP of Corporate Development & Investor Relations*

Sure. So the margins in that time for that base contract are mid-20s contribution margin. And we consistently underwrite that for new infrastructure for that 5-ish year deal, right? If it's a shorter deal, that has higher contribution margin. What's the opportunity after that? The opportunity after that is you go sell it in the on-demand market. You go sell it at spot, which when you're signing a 5-year commitment, right, you are signing at a price that is lower than on-demand, right, because you are paying for -- or you're selling 100% utilization for every second of every hour of every day of every month of every year for 5 years, right? But what you can start to do is take advantage, right, of, okay, this is paid for. I don't need to go finance it. And what that allows me to do is go sell it at spot where pricing might be higher.

**Tal Liani**  
*BofA Securities, Research Division*

The fact that the technology at that point is going to be 5 years old, does it mean that you have to find new types of customers or...?

**Nicholas Robbins**  
*VP of Corporate Development & Investor Relations*

I think it's more likely that you find new types of workloads than new types of customers, right? Like the -- what we can observe, right, is Ampere and Hopper pricing has gone up pretty consistently, right, over the past few months and maybe even a bit longer than that. And I think it's highly unlikely that Ampere, which for us went up in Q4, ASPs went up and in Q1, they went up again, right?

I think it is unlikely that a bunch of people are contracting Amperes, which is at this point now rapidly approaching 6 years old, right? I think it's a late 2020 SKU for training, right? That is we have workloads that run very well for this -- from an inference perspective, and we are making really attractive returns by buying this. So we are willing to pay more for it. And so I think the customer might evolve. The customer might be the exact same. They might just match a different workload to it.

Like I almost think of OpenAI's router model, right? Like people hopefully haven't already forgotten that like 6 or 9 months ago, you got to pick your OpenAI model, right? You can be like I want o1 or I want o3 or I want GPT-4. And I was the person who was like, okay, I want like the most performing model for everything. It doesn't matter what the query was. And that was probably an irresponsible use of compute, right?

But what they did is they introduced a router model where they said, okay, based on the query, I'm going to map this to GPT-3 that might be running on Ampere or o4, which might be running on a B200 or GB200. I think you will also see more of that where customers get more sophisticated about, okay, this workload goes here, that workload goes there.

**Tal Liani**  
*BofA Securities, Research Division*

Got it. I always tell my fiancee, don't thank ChatGPT, you're just burning tokens. There's no need...

**Nicholas Robbins**  
*VP of Corporate Development & Investor Relations*

I remember when Sam Altman [indiscernible] but when the machines take over, you want to be nice to them.

**Tal Liani**  
*BofA Securities, Research Division*

You're accounting -- you're depreciating your assets for 6 years, the GPUs for 6 years. Will they survive 6 years?

**Nicholas Robbins**  
*VP of Corporate Development & Investor Relations*

I think every data point that we can observe in the market suggests that the answer to that is, if anything, we're being conservative, right? Like the analogs we can point to are Voltas and Teslas, right, like older GPU SKUs are still running in clouds. Those are late 2010 SKUs that are still being monetized today, right? I imagine a similar thing could be said of TPUs that are 6-plus years old, right?

And again, we're looking at Amperes, like we're getting to 6-year-old SKUs and those things are humming, right? And so I think it feels to me like this debate part of it has maybe waned a little bit in the last few months as people have seen Hopper pricing be higher today than 3 years ago, right? They're like, oh, I guess it wasn't a 3-year useful life. I think it will continue to wane. But like a fear of the unknown is definitionally unknowable until you get there.

And Hopper is a late '22 SKU. So we'll see 2 years from now. But everything we see suggests that they will be monetizable. And what I would say if there is true risk from a hardware perspective of will it perform, I feel way, way, way better about Hoppers running in CoreWeave cloud than any other cloud in the world, right? Because what our orchestration layer does, what Mission Control does in large part, is it keeps GPUs healthy. And the healthier that you keep the thing, it's more likely that it's going to run for longer, right?

**Tal Liani**  
*BofA Securities, Research Division*

Got it. Yesterday, I hosted for a keynote, the founder of a company called TECfusions, and they build data centers. They have -- it's a real estate with power company. And he said, half of the companies that tell you they're going to build data centers, they're not going to make it on the time. And the question I'm asking you is your backlog had grown up tremendously, your revenues, the outlook is great. Talk about the operational risk, talk about the operational challenges in bringing capacity online to meet your liabilities or your commitments.

**Nicholas Robbins**  
*VP of Corporate Development & Investor Relations*

So CoreWeave exists because we are excellent at 3 things. Like -- and you need all 3 to build the business we have in the time period we have. We deliver excellent technology, most performant cloud out there, right? And that's -- ask our customers, ask experts. I think that's the consistent feedback. We are excellent at scaling this infrastructure and delivering cloud, right? And we are excellent at navigating the capital markets to permit us to do so, right?

You can't exist and build a business from zero to hyperscale without being excellent at those 3 things. We feel exceptionally good about our ability to deliver on the time lines that we've agreed to with customers. I think our track record is, I would argue, wildly underappreciated in the market. And what I mean by that is we have close to 50 data centers online. The overwhelming majority of them have been on time, some have been early, a few have been late.

We did get on our Q3 earnings call, right, and say, look, this is an industry-wide thing. We have one data center development partner who's struggling more than others, and they're delayed, and that's impacting our Q4. It was not an overwhelming impact to Q4, right? But it was an overwhelming reaction from the market because I don't know that they appreciated that things are going to be delayed.

I think that what is unique and my guess about this is in terms of what's going to happen. There are 6 companies in the Western world who have delivered AI cloud at scale, right? It's Microsoft, it's Meta, it's Google, it's Amazon, it's Oracle and it's us. right? I'm not saying there aren't other people who are signed up to do it or who may do it in the future, but the reality is those are the 6 companies that do it. And 5 of those companies have gigantic other beautiful businesses that obscure away the economics and what's actually going on quarter-to-quarter of AI cloud, right?

And then there's us who we don't have those businesses to obscure it away. There are going to be more companies, neoclouds that are scaling real size of infrastructure in the coming quarters. And they're going to try to do it multiple times, which is something we've done. Like I said, we have close to 50 data centers as of the end of Q1. I think 49 was the number. I think the world is going to see more delays and more struggles and the world is going to think that things have gotten worse, not better, whereas I don't think that is true.

I think you are just going to see more people attempt to do it who can't obscure things away. But do I think working through operational challenges is something that is part of this job? I think it absolutely is. And why do I feel that we're well positioned to do it? Well, one, we've done it a bunch of times. We have an excellent track record in this regard. And two, one of our real superpowers is we are able to take a power shell and turn it into a supercomputer that's part of AI cloud in something like 6 weeks.

It takes most guys 3 to 6 months to do that. And so when you're able to do things as efficiently as we have and by the way, we think we're going to keep getting better there, we are able to offset some of those challenges that other people face in operational delays, oh, something is -- we were planning it would take 3 months to deliver this. Well, oh, we only need 6 weeks. So if you're 2 weeks late, we can still be early, right? I think that is the biggest part of it.

**Tal Liani**  
*BofA Securities, Research Division*

Got it. And what about supply constraints? How do you manage the fact that cost supply -- component cost is going up constantly?

**Nicholas Robbins**  
*VP of Corporate Development & Investor Relations*

We pass it through to customers, right? The reality is you do that in 2 ways. The overwhelming majority of our CapEx is spent on servers, where we're signing purchase orders with our partners. At the same time, we're signing order forms from customers. And so we're able to say, Oh, the pricing just went up. Great. We have to charge more for it, and then we lock it in.

**Tal Liani**  
*BofA Securities, Research Division*

That's before you sign the contract, at the time of signing contract...

**Nicholas Robbins**  
*VP of Corporate Development & Investor Relations*

At the time. Think of those things as concurrent. And then for smaller parts of the business where you have a bit of exposure like storage, I would think of some of our pricing mechanisms as a bit more like cost-plus oriented where there can be an escalator in price if there's an escalator in cost.

**Tal Liani**  
*BofA Securities, Research Division*

Got it. Got it. Enterprise customer. So enterprise and other -- you spoke about other types of customers. Talk about your efforts to go after the inferencing opportunity of enterprises. Some of the other -- another neocloud company, much smaller cloud company, they make it their vision. They only focus on the enterprise. What about you?

**Nicholas Robbins**  
*VP of Corporate Development & Investor Relations*

I think there's difference between making it your vision and only focusing on it, right? I actually think those are 2 disparate things, right? I think to -- I don't know that there's actually any neocloud out there that actually only focuses on the enterprise, right? Because if you actually look at what -- who's paying them revenue, I think it's not even research labs, it's hyperscalers.

**Tal Liani**  
*BofA Securities, Research Division*

I'll stop you for a second because I'll define it better. They use hyperscalers in order to fund the build-out, but they say we take all -- once we build it out for Oracle, for whatever, once we build it out, we're going to shift it and only address the enterprise. They really only want to focus on enterprise.

**Nicholas Robbins**  
*VP of Corporate Development & Investor Relations*

So what I think I'm hearing from you is you're saying they're going to take a longer-dated contract, use it to pay off the infrastructure.

**Tal Liani**  
*BofA Securities, Research Division*

Exactly.

**Nicholas Robbins**  
*VP of Corporate Development & Investor Relations*

Then take that infrastructure and sell it to other people because it will be entirely theirs.

**Tal Liani**  
*BofA Securities, Research Division*

That's their strategy.

**Nicholas Robbins**  
*VP of Corporate Development & Investor Relations*

I would say that sounds like the business model that we brought to market in 2023 and defined, and it seems like a lot of people have adopted it.

**Tal Liani**  
*BofA Securities, Research Division*

What about go-to-market? The other part?

**Nicholas Robbins**  
*VP of Corporate Development & Investor Relations*

So we've invested pretty heavily in building out that muscle, right? We hired Jon Jones last year, who is a senior go-to-market leader at AWS, who is now our first CRO, and he's been building out that part of the sales force. It is of extreme focus to us. And I think the way we think about how we allocate capacity because it really is an allocation conversation is one of you want to -- like hyperscalers are really nice in that they also give you a prepayment, right, a lot of the time, and that gives you a more effective way of financing.

We want exposure to research labs, right? Like we want to be a trusted partner to OpenAI and Anthropic and Meta, right, and the next tier of the list. But we also want to be partnering with the enterprises. And we've had real success there. In Q4, we announced folks like Mercado Libre as customers. In Q1, we announced that 10% of our $100 billion revenue backlog was financial services companies, right? That's close to $10 billion of enterprise within a single vertical, right? That's not accounting our success in industrials and health care, et cetera. And I think you will see us continue to add new logos and continue to allocate capacity to those enterprise customers.

**Tal Liani**  
*BofA Securities, Research Division*

Great. I used up most of the time. Is there any question from the audience? Raise your hand. Yes. Instead of waiting for the mic, just shout it out.

**Unknown Analyst**

[indiscernible]

**Nicholas Robbins**  
*VP of Corporate Development & Investor Relations*

So when you talk about performance, I guess, let's take a step back and maybe I'll hit on 2 things. One, you're absolutely right. I think what you will see in the agentic era is more use -- the attach rate or the ratio of the CPU to GPU will go up. The necessity for storage, right, and keeping data close to the GPUs will go up, right? And I think what you've heard from us, right, in Q3, we started talking about our storage business, how it eclipsed $100 million of ARR, and it was growing like a weed, and it was a business we're really excited about.

And then similarly, we started talking about our CPU business in January. And obviously, I think that today, the world has a better appreciation of why we started talking about it in January. When it comes from a performance perspective, what you are doing is making a complex system more complex. You're making it bigger, you're adding more directional data flow and communication. The bigger clusters get, the more complex workloads get, the more differentiated our software stack proves to be. That was true in training. That's been proven true in inference as well. And I think that feeds into our competitive advantage and differentiation over time.

**Tal Liani**  
*BofA Securities, Research Division*

Great. Is there a risk -- last question, but is there a risk of capacity commoditization over time?

**Nicholas Robbins**  
*VP of Corporate Development & Investor Relations*

Yes. But it's a question of when. Is there a risk of that this decade? I do not think so, right? But to be clear, right, this platform -- like we've been the guys since 2023 when I first met Brian and Brannin and Mike and Peter, they were saying this was a rest of the decade problem. And a lot of hyperscalers are saying this was a 6-month problem, right? In the same way they said, "Oh, neocloud short-term thing" and then they go out and sign $80 billion of more neocloud stuff, right?

But our view has always been what is your right to survive and thrive as a cloud participant, right, in a world in which you do hit supply-demand equilibrium. And our simple thesis has been this is what you need to achieve. Hyperscale, I think we're well on our way. Competitive cost of capital, I think we're well on our way, right? We've cut our cost of debt by close to 700 basis points since the beginning of 2024. And you need to deliver interesting technology, I think we're already there, right? And if you can do all those 3 things, then you will have a right to compete and an ability to compete from a cost of capital perspective in a more balanced world.

**Tal Liani**  
*BofA Securities, Research Division*

Got it. Great. Thank you, Nick. We ran out of time. We could have continued another hour. Thank you so much.

**Nicholas Robbins**  
*VP of Corporate Development & Investor Relations*

Thanks so much, everyone.