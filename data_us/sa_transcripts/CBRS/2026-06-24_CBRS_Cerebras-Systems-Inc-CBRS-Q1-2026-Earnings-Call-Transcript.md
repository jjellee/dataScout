---
ticker: CBRS
company: Cerebras Systems Inc.
title: "Cerebras Systems Inc. (CBRS) Q1 2026 Earnings Call Transcript"
published: 2026-06-24T17:12:14-04:00
article_id: 4917476
source_url: https://seekingalpha.com/article/4917476-cerebras-systems-inc-cbrs-q1-2026-earnings-call-transcript
---
Cerebras Systems Inc. ([CBRS](https://seekingalpha.com/symbol/CBRS#source=section%3Amain_content%7Cbutton%3Abody_link "Cerebras Systems Inc.")) Q1 2026 Earnings Call June 23, 2026 5:00 PM EDT

**Company Participants**

Sean Dorsey  
Andrew Feldman - Co-Founder, CEO, President & Chairman  
Robert Komin - Senior VP, CFO & Treasurer

**Conference Call Participants**

Timothy Arcuri - UBS Investment Bank, Research Division  
Thomas O'Malley - Barclays Bank PLC, Research Division  
Quinn Bolton - Needham & Company, LLC, Research Division  
Atif Malik - Citigroup Inc., Research Division  
Joseph Moore - Morgan Stanley, Research Division  
Joshua Buchalter - TD Cowen, Research Division  
Matthew Bryson - Wedbush Securities Inc., Research Division  
Vijay Rakesh - Mizuho Securities USA LLC, Research Division  
Richard Shannon - Craig-Hallum Capital Group LLC, Research Division

**Presentation**

**Operator**

Good afternoon, and welcome to Cerebras Systems' First Quarter Fiscal Year 2026 Earnings Conference Call. [Operator Instructions] Please note that today's call is being recorded.

I will now turn the call over to Sean Dorsey, Head of Investor Relations. Please go ahead.

**Sean Dorsey**

Thank you, operator. Good afternoon, everyone, and welcome to Cerebras Systems' first earnings call as a public company. Earlier today, we issued our press release and posted our supplemental earnings presentation to the Investor Relations section of our website. A replay of this webcast will also be available on our Investor Relations website following the call.

Joining me today are Andrew Feldman, our Co-Founder, Chief Executive and President; and Bob Komin, our Chief Financial Officer.

Before we begin, I would like to remind everyone that today's discussion will include forward-looking statements under the safe harbor of the Private Securities Litigation Reform Act of 1995. These statements include, but are not limited to, statements regarding our future financial performance, business strategy, market opportunity, customer demand, product road map, technology leadership, supply chain, operating model and outlook for Q2 and full year 2026.

Forward-looking statements are based on current expectations and assumptions and are subject to risks and uncertainties that could cause actual results to differ materially from those expressed or implied. These risks are described in our SEC filings, including our final prospectus related to our IPO and our future periodic filings with the SEC. We undertake no obligation to update these forward-looking statements, except as required by law.

During today's call, we will also discuss certain non-GAAP financial measures. Reconciliations between GAAP and non-GAAP results are included in today's press release and supplemental materials, which are available on the Investor Relations page of our website.

With that, I'll turn the call over to Andrew.

**Andrew Feldman**  
*Co-Founder, CEO, President & Chairman*

Thank you, Sean, and thank you, everyone, for joining us today. This has been an extraordinary several months, and I want to begin by thanking our customers, our partners, suppliers, employees and shareholders. We would not be here without your trust and your support.

Earlier today, we posted our Q1 2026 results, and we delivered a strong quarter. We delivered core revenue of $191.3 million, up 92% year-over-year. Core hardware revenue contributed $111.6 million, up 60% year-over-year, while core cloud and services revenue contributed $79.8 million, up 167% year-over-year. Bob will share more color on our financial results shortly.

Before Bob digs into that, I'd like to say a few things about the market. I'll divide my comments into several sections. I'll begin by spending a few minutes sharing my views on the larger drivers underpinning the AI revolution, their impact on the compute market and why speed wins. I'll then turn to our successes in Q1 with special attention to our progress with OpenAI and AWS. And finally, I will talk about how we expect to avoid many of the supply chain challenges that bedevil others in our space.

To understand the dynamics in the compute market, it's important to realize that AI provides new capabilities to computers. AI gives computers purchase on whole swaths of the world that had previously been foreclosed. This is why AI is so transformative and why its impact is so profound and why we believe it increases the size of the market addressable to compute by many thousands of times.

Computers have historically been good at math, very good, but they were relatively poor at everything else. They did not provide much insight into text or images. For these modalities, all they could do is store and retrieve. Computers were at their best in a 2D world of numbers. In a real world of 3 dimensions, they were challenged. AI opens up the world of human experience to computers. As a result, the size of the market increases exponentially.

It is as if prior to AI, computers worked in black and white and in 2 dimensions and after AI, they address a world of color in many dimensions. This is why AI has spurred an explosion in the demand for compute. Computers can now do things they have never done before and why, in our opinion, demand will continue to accelerate for many years to come. Text, images, video, agents, robotics, these are all part of how AI expands the computer's ability to understand, participate and take actions in the world. These all represent opportunities for Cerebras.

Let's look at the specifics of how this is unfolding. Prior to 2025, AI was a parlor trick, a novelty, interesting, but not useful, cool, but not valuable. AI is now valuable because it has become profoundly useful. Led by OpenAI, the foundation model providers pioneered the way, the foundation model makers and shortly thereafter, the open source models made models smart enough to be useful across many domains. And once something is useful, people use it. And once people start using the technology, speed determines its productivity.

Fast is productive and slow is unproductive. Speed provides answers in less time, providing competitive advantage. Speed makes the largest and smartest frontier models interactive. Speed enables agents to complete tasks faster. Fast tokens are the most valuable tokens because they get more work done in less time. And today, Cerebras delivers the fastest AI in the world, bar none, not by a little bit, but by an order of magnitude. And we do this for small models, for medium models and for the largest models in the industry. We do this for models with small KV cache, with medium KV cache and with giant KV caches.

We generate tokens faster than anyone else. What I'd like to show you right now is a quick demo. Just how much faster we are than GPUs on [ Kimi K2 ], a trillion parameter open source model. We're going to run the exact same prompts. On the left, it's Cerebras. On the right is a leading GPU. The only difference, same model, we're finished already. Same model, right, same prompt, the difference is hardware, and we're finished. It took us 21 seconds. We're now waiting on the GPU. Still waiting.

Now we've increased the speed 5x in the video to not make you wait as long as you otherwise would. Still waiting. Okay. Cerebras did in 21 seconds. It took 4 minutes and 37 seconds for the GPU to do. The same model, the same prompt. That's what it means to be 13x faster. In AI, inference speed is productivity. Slow isn't productive. But this should not come as a surprise. It is in line with each of our everyday experience.

How big is the market for slow search? How big is the market for slow Internet access? Any of you still use dial-up? How long will you wait for a website to resolve? Why would it be different for AI? In fact, not only does speed increase the value of tokens, but speed accelerates the adoption of AI. When AI is fast, it's more fun to use. People use it. They use it more often for more things, and they use it to solve more important problems. With fast AI, users invent things that never existed before. They solve problems in new ways. They develop new offerings, new business models. This is what speed does. And this is what Cerebras' speed enables.

A final point on speed. There recently has been a great deal of focus, especially at the frontier model level on safety and the importance of guardrails. How do guardrails work? Guardrails add a layer of compute on top of the AI to create a safer experience. This compute takes time, and it takes more time on slow infrastructure. Traditionally, guardrails force the trade-off between safety and user experience, between safe and fast. Cerebras eliminates this trade-off. Fast AI inference allows guardrails to work without inserting crippling delays. AI is safer with these guardrails and AI is safer and more productive when it's [ extremely ] fast.

Our performance advantage is borne of our wafer-scale architecture. We're more than an order of magnitude faster than GPUs because we solve problems that haven't been solved or couldn't be solved by others. The problems of yield, cross-reticle connectivity, mismatches in thermal expansion, power delivery and cooling are all problems that the industry struggles with, but the Cerebras solved years ago. Moreover, the advantages of wafer-scale are durable. By building chips that are 58x larger than the largest competitor, we're able to use SRAM and benefits from its blistering speed, while competitive offerings use HBM, which is slow, expensive and in short supply.

We see the advantage of wafer-scale technology expanding our performance lead as we bring next-generation solutions to market. In fact, the technology underpinning of wafer-scale fundamentally advantages additional technologies in the future. For example, wafer-scale technology brings profound advantage to memory stacking and optical integration. And as we look further into the future, data centers in space are also advantaged by wafer-scale integration. Not only does wafer-scale compute deliver faster speeds and for latency-sensitive workloads, less power per unit compute than do GPUs. But most importantly, it requires less chip-to-chip communication. And chip-to-chip communication is one of the fundamental limitations of terrestrial data centers and a yet to be solved problem for data centers in space.

So with this as a backdrop, in the first quarter of 2026, how did we meet this extraordinary market? And how do we leave Q1 even better positioned? In this section, I'll focus on our partnership with OpenAI and AWS as they took shape in this quarter. We signed a definitive agreement with OpenAI on December 24, 2025, for the purchase of more than $20 billion of Cerebras compute over the next several years. By February 1, we were in production, running a model we've never before seen, 35 days from signature to production deployment.

Beyond the transformative revenue ramifications, our collaboration with OpenAI gives us a direct view into frontier model development and the direction it is moving. By pairing frontier model intelligence with the world's fastest inference, we build products and technologies that others simply can't. In fact, the boundaries of these capabilities have yet to be fully explored. OpenAI and Cerebras are excited that GPT 5.4 is now running on Cerebras. This collaboration brings together OpenAI's frontier models with Cerebras' wafer-scale inference infrastructure to enable highly responsive model interactions. GPT 5.4 on Cerebras is currently available to OpenAI engineers and to select OpenAI customers as part of OpenAI's strategic rollout. OpenAI and Cerebras are also actively working to bring GPT 5.5 onto Cerebras as part of the next phase of this rollout and expect to share more shortly.

In March, continuing this trend, we signed a binding term sheet with AWS to deploy Cerebras and AWS data centers. Our solutions will combine AWS' leading Trainium 3 chips with Cerebras' CS-3 in a disaggregated solution that is expected to be an order of magnitude faster. Trainium will do prefill and Cerebras will be decode. And together, the solution is expected to deliver the fastest tokens at massive throughput.

Remember, disaggregated solutions are a significant opportunity for Cerebras. The technical strategy is one of divide and conquer. It is based on the recognition that inference has 2 computational components. The first is where we process the prompt. This is called prefill and it's highly parallelizable. The second is where we generate the response. This is called decode and it's strictly sequential. By using different processors for the prefill and for the decode, we can deliver truly exceptional results.

We are also proud to announce that we have, as of this week, completed a definitive agreement with AWS and we will begin our technical collaboration as well as prepare for deployments in their data centers. As you all know, AWS is a leading cloud compute company and one of the most important providers in the world for developers and enterprises. And many enterprises want to run AI where they store their data and where they have existing agreements and where the environment is familiar and is secure. As a result, AWS provides an easy way for Cerebras solutions to meet the world's enterprises where they already are.

Let's for a minute now turn to supply chain. Keeping up with this extraordinary market growth has brought supply chain challenges to many in our industry. At Cerebras, we have several fundamental advantages. First, the binding constraint in the market right now is HBM memory. It's in short supply, it's expensive, and we don't use it. So we avoid this constraint entirely. We use SRAM. And SRAM is printed on our logic wafer. It's not a separate chip. As long as you can make the chip, you can make SRAM. Its supply is approximately infinite.

The second binding constraint is the CoWoS process at TSMC. We don't use it. So again, we sidestep this constraint. Third, 3-nanometer capacity at TSMC is a constraint. And again, we don't use it. We're the fastest in the world and happily at the 5-nanometer node, where there is less contention for fab resources and where manufacturing is less expensive.

Our partnership with TSMC deserves special mention as they know more about chip making than just about anyone else on earth. They believed in the wafer-scale approach from the time we were a tiny team with nothing but a PowerPoint slide, and they've been with us along the way. They have proven themselves to be an extraordinary partner. Just as a reminder, our salable unit is not our wafer, but our CS-3 system. We sell the CS-3 for on-premise deployments or time on the CS-3 through our Cerebras cloud or through our partners' cloud. We manufacture our CS-3s in the U.S. And in fact, to the best of my knowledge, we are the only accelerator maker to manufacture exclusively in the U.S.

We have added hundreds of thousands of square feet of manufacturing and clean room space to support our growth. We've expanded our partnership with Flextronics and are proud to have added Sanmina as our second major contract manufacturer to assist us in managing our expansion.

Finally, it's no secret that data center capacity is at a premium. It's a dog fight out there. Despite this, we've added data centers around the world. We've added data centers across the U.S. and Canada, Europe, including France and the Nordics, and we're in early discussions for data centers in Israel, the UAE, Australia, Singapore, India and Indonesia. We're expanding the capacity. We need to serve customers, and we're doing it with urgency. The demand environment is strong, but this is just not -- this is not just about demand. It's about building the infrastructure required for the next phase of AI.

So to wrap up, there is a tectonic shift in compute demand brought about by AI's ability to make the world around us tractable for computers. As a result, the market will need vastly more compute, in my view, for decades. AI power users represent today a tiny fraction of the world's population, by some estimates, less than 1% and compute and memory is already in tight supply. Just imagine. To this AI revolution, we bring leadership technology, which in turn enables us to deliver the fastest AI inference in the world by more than an order of magnitude. Fast tokens are more valuable tokens and Cerebras tokens are the fastest. The result was a record quarter.

With that, I'll turn things over to Bob, and he can provide more color on the financial results. Bob?

**Robert Komin**  
*Senior VP, CFO & Treasurer*

Thank you, Andrew, and good afternoon, everyone. I want to also add my thanks to our customers, partners, team Cerebras and the investment community, both new and who have gotten to know us over the last several years. Cerebras is more than 10 years into the journey, and we're still just at the very beginning. I want to thank everyone for joining us today on our first earnings call operating as a public company. Opportunities we see ahead for us with fast AI are massive, and we appreciate everyone who has chosen to join us for the road ahead.

Today, I want to describe the financial framework we will use to discuss our results. It's the same way that we evaluate our financial performance and make resource allocation decisions internally, provides additional visibility to amounts that are embedded in our reported GAAP revenue and cost of revenue that we believe provide more transparency as well as direct comparability to our prior historical results to better analyze our trends.

Beginning in Q1 '26, we have data center costs, which are contract with OpenAI has us pass through to them with a 3% markup. These data center pass-through items are reported gross, so they increase both our cloud and other services revenue and cost of services, but are at a significantly lower margin than the rest of our business. These amounts start out small in Q1, but they'll become more significant over time. Also, OpenAI has the option to choose whether to receive its future committed amounts in our cloud or in its own data centers, which would mean there would be no future corresponding pass-through amounts for that capacity. Because these amounts can be highly variable and are outside of our control, we're excluding them from our core business metrics.

We also now have noncash amortization of customer warrants that is recorded as a reduction in revenue for both our hardware and cloud and other services GAAP revenue line items, depending on the related services the customer is purchasing. So we're adjusting our GAAP numbers to exclude the impact of these items and a few other common ones like stock-based compensation and onetime items, and we define the resulting non-GAAP amounts as our core business metrics. I will only be discussing these core metrics today. Reconciliations to GAAP for all of our non-GAAP items are available in today's earnings material and on our website.

Let's start with revenues. Q1 was another record quarter for Cerebras. Our core total revenue was $191.3 million, representing 92% year-over-year growth. Now looking at revenue by type. Core cloud and other services revenue reached $79.8 million and grew 167% year-over-year. Market demand for Cerebras Inference Cloud remains incredibly strong. We are ramping our capacity rapidly, and we saw a meaningful pickup in revenue across Q1 as we began our ramp with OpenAI in February as well as from other customers using the Cerebras Cloud.

We expect increasing year-over-year growth rates for each quarter in 2026 with more of this revenue coming later in the year as the ramp in our cloud capacity deployments accelerates. Core hardware revenue was $111.6 million, up 60% year-over-year. We plan to see decreasing hardware revenue for the next few quarters as our existing POs are delivered and our mix shifts towards the majority of our hardware production being deployed in Cerebras Cloud to fulfill our significant contracts. This trend could change relatively quickly, however, as OpenAI and AWS as well as other customers make decisions about when and how they prefer to deploy our hardware solutions in our data centers or theirs.

Now moving on to gross margin. Core gross margin was 46.5% in the quarter compared to 42.1% in the prior year period and 41% last quarter. Core cloud and services margin improved significantly to 52.9% in the quarter from lower levels we saw last year as we launched the Cerebras Cloud service. The primary reasons for the increase were higher pricing as the market is now valuing higher speed inference at a premium and market demand exceeds supply. The utilization of our systems that we began to deploy in late 2025 improved quickly. And there was a small amount of [ ramp back ], relatively speaking, to increase capacity from a customer.

For the rest of 2026, in order to accelerate our ability to service the significant near-term demand in our contracted backlog, we've chosen to make more capacity available sooner by temporarily renting our own systems back from an existing customer while we aggressively build out and deploy our own data center capacity. The additional cost of renting third-party capacity will depress core cloud and other services margin temporarily from current levels. We expect the impact to be a decrease of 10 to 15 margin points based on the volumes we are now anticipating before beginning to [ ramp back ] towards our target margin of 60% plus as we transition away from our rented systems.

Core hardware margin was 42% compared to 30.6% in Q1 '25. Over the last few quarters, we benefited from the timing of incremental performance-based incentive pricing after the target was achieved, but was recognized prospectively for the remaining systems that have not yet been shipped. We expect core hardware margin to be more similar to the first half of 2025 and return to the low 30s as this contract pricing normalizes.

As a reminder, when we sell hardware systems and recognize that revenue upfront, we also include support and other services, which have significantly higher margins. As a result, total profitability over the life of the individual contracts is much closer to our target overall gross margin. These additional elements of revenue are required to be recognized over the contracted life of the services and are recorded as core cloud and other services, so are not included in our core hardware revenue and gross margin.

We are focused on improving gross margin over time through scale economies, improved product throughput and performance, manufacturing efficiency, utilization of cloud capacity and performance-driven pricing improvements to achieve our long-term overall gross margin target of 60%. At the same time, we will continue to be aggressive and creative, including potentially investing ahead of demand when we see attractive long-term opportunities to gain key customers, accelerate revenues and drive gains in market share.

Now I'm going to talk about operating expenses. Our non-GAAP operating expenses were $92.6 million, up 51% from a year ago at just more than half the rate of core revenue growth of 92%, demonstrating the strong operating leverage available as we grow our business. R&D was our largest area of investment at $69.8 million. We believe sustained R&D investment is essential to maintaining our technology leadership and requires being at the frontier of AI across silicon, systems, software, models and cloud infrastructure to deliver the fastest performance.

We have an exciting product road map to bring to market over the next several years, including near-term innovations such as the implementation of disaggregated inference solutions, with multiple hardware partners, which we expect to begin to deliver in the second half of this year. Sales and marketing expense was $12.9 million, reflecting continued investment in customer engagement, field capacity, developer adoption and go-to-market infrastructure to support increasing market demand. G&A expense was $9.9 million and will continue to step up significantly next quarter due to incremental costs associated with operating as a public company and rapid growth in the size of the business.

Moving on to profitability. Core non-GAAP operating loss improved to near breakeven at minus $3.5 million with operating margin of negative 2%, a significant improvement from a year ago when core operating loss was minus $19.3 million and operating margin was negative 19%. There was also a nice improvement sequentially from Q4 '25 when operating margin was minus 10%.

Core non-GAAP net loss was $2.5 million, while the temporary reduction in gross margin I described earlier that will result from renting back our systems until we deploy significant capacity in our own data centers will cause these metrics to regress somewhat for the next few quarters. We believe the steady improvement that we delivered over the past several quarters highlights our ability to achieve our target profitability profile of approximately 60% gross margin and 40% operating margin in the medium to long term.

Moving on to our current cash position. We ended the quarter with $3.3 billion in cash, cash equivalents, restricted cash and marketable securities. We've accelerated the pace of our fundraising over the last several quarters to support our increasing growth rate and provide us with the liquidity we need to scale. As a reminder, we raised $1 billion in Series G equity in September 2025, another $1 billion in Series H equity in February 2026, added a revolving credit facility for up to $850 million in April '26. And then just a few weeks ago, completed the largest semiconductor IPO in history, raising another $6.4 billion. We are well positioned with the financial flexibility to accelerate the sourcing and deployment of data centers and our supply chain to support significant near-term growth of our cloud business.

Now turning to our outlook. We'll typically provide quarterly guidance, but since this is our first earnings call, we'll also provide some color on the year. In our core business in Q2, we expect core revenue of approximately $194 million, representing year-over-year growth of 88%. Core gross margin in the range of 36% to 38%; core operating margin in the range of minus 30% to minus 32%. And for the full year 2026, we currently project core revenue in the range of $855 million to $865 million, representing year-over-year growth of 69% at the midpoint. Core gross margin in the range of 38% to 41% and core operating margin in the range of minus 28% to minus 32%.

In summary, we made significant progress in our business during the first quarter. We delivered strong revenue growth, gross margin improvement and meaningful customer momentum. We significantly strengthened our balance sheet through our IPO and our fundraising activities, and we're poised to continue executing on the enormous amount of opportunity we see. We're working hard to bring more data center capacity online as soon as possible to meet robust demand.

With that, I'll turn the call back to Andrew for closing remarks. Andrew?

**Andrew Feldman**  
*Co-Founder, CEO, President & Chairman*

Thank you, Bob. Cerebras was founded on the belief that AI infrastructure needed a new approach, one that was built from a clean sheet. The progress we report today reinforce this belief, the world needs faster AI. Faster AI like faster versions of all technologies before it drive adoption, usage and customer experience. When given the choice, who wants slow. And we're built to deliver fast AI. That's what we do.

As AI continues to expand its footprint, so will we. We're proud to be a public company, and we're redoubling our effort on the work ahead. We continue to fuel our culture with fearless engineering and with the ability to delight our customers with experiences that are unavailable elsewhere. We also will work diligently to communicate with our stakeholders and our investors and to do so with transparency and with discipline.

We thank you for joining us today. Operator, please open the line for questions.

**Question-and-Answer Session**

**Operator**

[Operator Instructions] Our first question comes from the line of Timothy Arcuri of UBS.

**Timothy Arcuri**  
*UBS Investment Bank, Research Division*

Andrew, now that you have the definitive agreement with AWS, can you just sort of help us to think about the timing on this and your ability to supply that customer? I know you had to put in your wafer orders back in February. So can you just give us a little bit of help in terms of when you could start to ship to them?

**Andrew Feldman**  
*Co-Founder, CEO, President & Chairman*

Sure. I think TSMC has been extremely good to us. We are in the happy position of having supply for our plan and beyond in 2026. I think you should expect to see AWS' impact in 2027.

**Timothy Arcuri**  
*UBS Investment Bank, Research Division*

Got it. And then if I can ask a quick follow-up. I also heard, Andrew, you talked about multiple partners for disaggregated solutions. Does this imply that there's another customer beyond AWS? And I guess I asked because I did see that Cerebras had a presence at Microsoft Build. So I'm just wondering what you mean by the multiple partners.

**Andrew Feldman**  
*Co-Founder, CEO, President & Chairman*

I think the opportunity to provide decode for people who have GPUs is real and in front of us. I think that's exciting. I think that the GPU as an architecture struggles with the sequential nature of decode, and we are extraordinary at it. So it makes sense to explore partnerships on that vector.

**Operator**

Our next question comes from the line of Tom O'Malley of Barclays.

**Thomas O'Malley**  
*Barclays Bank PLC, Research Division*

Congrats on the nice results. Andrew, I wanted to ask you a question on your TAM. I think that during the process, there was a lot of conversation about your ability to handle larger models. When you look at Kimi, that's one example of a large model. You're again showing a demonstration today about attacking larger models as well. Jensen spent time talking about 25% of the inferencing market is fast inferencing and maybe even took a step back on that on the last call. But what do you think your TAM is when you look at the broader AI market? Would love to get your opinion there.

**Andrew Feldman**  
*Co-Founder, CEO, President & Chairman*

Thanks for the question. We look out into technologies and can't find examples of where slow has owned meaningful portions of the market over medium periods of time. And I think you should think very carefully about the example of search, right? There is no slow search because nobody wants it, right? There's no more dial-up because nobody wants it. And I think when given the choice on the same model between fast and slow, I don't think it's a very hard decision. And so when we look out at the space, we see the entire inference market as available to us for fast inference.

I mean who doesn't want answers in less time? And who doesn't want more productive agents? So that's what we see. I know that's at odds with GPU makers. And both of our arguments are, I think, in some way self-interested. We build fast and I think the market is big for fast. So I'm not surprised at that.

**Thomas O'Malley**  
*Barclays Bank PLC, Research Division*

Super helpful. And then we might find this out in the filings, but just wanted to give it a crack on the call. Did you have any top 10% customers? And are you willing to share on the call how large they were?

**Andrew Feldman**  
*Co-Founder, CEO, President & Chairman*

I don't think we should share on the call. I think you'll see in the filings.

**Operator**

Our next question comes from the line of Quinn Bolton of Needham & Company.

**Quinn Bolton**  
*Needham & Company, LLC, Research Division*

Andrew, Bob, congratulations on your first call as a public company.

Andrew, I wanted to follow up on the inference TAM question. Just obviously you guys are addressing the fast inference portion of the market, which you think allows you to address the entire market. But your tokens may be more expensive. And so I was just wondering if you could address the higher token cost for fast inference. How much of the market do you think is willing to pay a premium for fast inference? And then I've got a follow-up on the road map.

**Andrew Feldman**  
*Co-Founder, CEO, President & Chairman*

I think there -- today, in many instances, fast is priced at a premium. I think you saw Anthropic offer a service. In fact, most now offer services in which fast tokens are sold at a premium. I think they're sold at a premium because they're more valuable, right? And I think you can look to your own experience with your Internet provider. If dial-up were free, do you want it? I think the answer there is quite the contrary. You have to pay quite a bit of money to get someone to take dial-up. And so I think that the reason right now that there's a premium is because people prefer fast. It's more valuable. I think we'll see over time how that shapes out.

**Quinn Bolton**  
*Needham & Company, LLC, Research Division*

Got it. And then the question just with the AWS definitive agreement now signed, if you look across the compute spectrum, oftentimes, these AI compute deals can extend into the gigawatt range. Just wondering, can you give us any sense of the scale? Is this tens of megawatts, hundreds of megawatts? Could it reach a gigawatt? Just any sense on the size of the AWS partnership and definitive agreement?

**Andrew Feldman**  
*Co-Founder, CEO, President & Chairman*

I don't think we're going to -- we're sharing that at this time.

**Operator**

Our next question comes from the line of Atif Malik of Citi.

**Atif Malik**  
*Citigroup Inc., Research Division*

Congratulations on the debut. Andrew, on the OpenAI and AWS partnerships, what is the decision tree for them to take the future commitments in cloud or as hardware and data centers?

**Andrew Feldman**  
*Co-Founder, CEO, President & Chairman*

So first, greeting Atif, good to hear from you, I guess. Second, with AWS, they are deployed in AWS data centers. That's the deal. I think OpenAI has a choice. They can deploy it in their data centers in a model where they buy the hardware or they can receive the compute via cloud service. I think it will depend on OpenAI sort of a portfolio decision of their data centers and their various capacity versus what we can bring in data centers. I think that's likely to be the determining factor, but I think that's really an important question for them.

**Atif Malik**  
*Citigroup Inc., Research Division*

Got it. And Bob, as a follow-up, I mean Andrew talked about the dog fight in terms of data centers and power availability and whatnot. When you look at your full year outlook, and thank you for providing that on this call, how much of that are new data centers or new power shells versus renting back from your existing G42 customer or your Cerebras Cloud?

**Andrew Feldman**  
*Co-Founder, CEO, President & Chairman*

This is Andrew, Atif. We're trying to add data center space as fast as we can. I mean we are engaged with builders throughout North America, data center operators in Europe, in the Middle East. We have new data centers coming on board in Q3, Q4, Q1, Q2, Q3, Q4 of next year and are adding more. We're in discussions with literally dozens of different data center owner operators. And so I think the answer is all of the above. We are going to -- the demand for our product right now is so significant. We are seeking data center capacity around the world as quickly as we can.

**Operator**

Our next question comes from the line of Joe Moore of Morgan Stanley.

**Joseph Moore**  
*Morgan Stanley, Research Division*

On the same lines as the last question, is the constraint on your growth 5-nanometer wafer capacity? Is it space and power and the kind of build-out of your cloud? Or are there some other constraints that we should be thinking of? It feels like demand is not the constraint here. It's how quickly you can ramp.

**Andrew Feldman**  
*Co-Founder, CEO, President & Chairman*

Demand is not the constraint. Supply is not the constraint. The constraint is data centers.

**Joseph Moore**  
*Morgan Stanley, Research Division*

Okay. That's helpful. And to the extent that your gross margins are better than we had modeled, is that a function of sort of a quicker ramp of that internal capacity versus the G42 rental? Or just what are the dynamics of gross margin through the rest of this year?

**Robert Komin**  
*Senior VP, CFO & Treasurer*

Thanks, Joe. There's a few things going on. One is actually higher pricing. So we -- because there's tremendous demand, we've been able to see higher pricing from existing customers. So even as OpenAI is starting to ramp, that's been an upside to our gross margin profile and something that we're reflecting now in the outlook for the rest of the year.

Another way to think about it is the competition has also increased in price. They have higher cost for HBM and other things. So I think the floor in the marketplace has come up a bit. And then we've been able to look at the timing of the amount of capacity that we need to bring on and the economics around it, which we were estimating a couple of quarters ago. And that's also turned out to be a bit more favorable, both in terms of how much is coming on when and also the amount that we're paying. So I think all of those factors as they play out for the rest of the year will allow us to be at higher gross margins than what we had predicted at the beginning.

**Operator**

Our next question comes from the line of Joshua Buchalter of TD Cowen.

**Joshua Buchalter**  
*TD Cowen, Research Division*

Welcome to the fun world of earnings calls. Maybe -- sorry to keep pulling at this thread, I wanted to follow up on sort of Tom and Quinn's earlier questions about the ability to service some of these -- the larger models. Maybe using the demo that you guys provided of the supporting the trillion parameter Kimi model, like any details you can give on the specs that were in that benchmark you showed, like how many CS-3s were used to support Kimi and maybe what the competing GPU-based rack architecture was?

**Andrew Feldman**  
*Co-Founder, CEO, President & Chairman*

We used the leading -- by way of comparison, we used a leading inference cloud. So we try to do our best to compare top of tree to top of tree. My understanding is that they're using B300s to serve as an endpoint for this model, but I can double check that for you. I think there is a fundamental misunderstanding propagated by some analysts who just didn't understand that our architecture was perfectly suited for these models of large size, small size, medium with big caches, small caches and that we can do them and are doing them not just in this demo, but for OpenAI at frontier models. right?

There are only 2 hardware vendors that currently serve OpenAI models, and we're one of them. And so it is sort of a proof point, right, an empirical validation that big models work just fine on us, and we have the same advantage as small models.

**Joshua Buchalter**  
*TD Cowen, Research Division*

Okay. Understood. And then maybe for Bob, as we think about the annual guide you gave, I think it implies sort of 20% plus half-over-half growth. Any help you can give us on how much of the second half growth is from pricing or maybe OpenAI contribution that we should expect for that first -- as you build up to the first 250-megawatt build?

**Robert Komin**  
*Senior VP, CFO & Treasurer*

Yes. Look, I think this initial guide coming out in the -- which is really focused on the first quarter and looking forward for the rest of the year, where we have data centers coming on largely in the back end of the year. A lot of the improvement is going to come from OpenAI being deployed in our cloud, and it's back-end loaded.

As I mentioned in my remarks at the beginning, we actually have in the forecast that hardware will come down a little bit sequentially for the rest of the year. So I'm being conservative for the second half as we're still pretty early in the year, data center capacity is coming on. And as we move throughout the year, we'll update you as we have more information about the progress and timing.

**Operator**

Our next question comes from the line of Matt Bryson of Wedbush Securities.

**Matthew Bryson**  
*Wedbush Securities Inc., Research Division*

Just going back to trying to figure out the market, it sounds like there's some more opportunity for what we're seeing with Amazon, where they're using Cerebras solutions to decode. We're thinking about the amount of value that you're capturing in that type of architecture versus [ prefetch ]. Is there any chance you could take a swag at kind of what portion of the value is in the Cerebras system?

**Andrew Feldman**  
*Co-Founder, CEO, President & Chairman*

Not exactly. Let me share maybe a different crack at the problem. A decode prefill, a disaggregated solution, is really good in some instances. And in particular, if you know the shape of the work, it's intended to support. When you specialize, right, when you buy some hardware for prefill and some for decode, you embed in your hardware deployment an assumption about the shape of the traffic. And if the traffic looks different, then you have stranded compute and low utilization and higher cost.

This is obviously a huge opportunity for a hyperscaler like AWS because they have technology that can drive traffic, right, of the shape they expected to their disaggregated solution and route it to other solutions if it's different from that assumption. Right? So the value of the solution is highest to a hyperscaler. The exact split of value between us and Trainium is very difficult to say. And as nobody has yet has deployed a true disaggregated solution, we have a lot to learn in the market still.

**Matthew Bryson**  
*Wedbush Securities Inc., Research Division*

Understood. That's helpful. And then just one for you, Bob. We're thinking about you renting out capacity from a customer to fill that OpenAI demand. Is the full rental requirement baked into your quarterly guide? And -- or is there any chance that there's a further impact on gross margins in Q3? Basically, I'm trying to figure out if gross margins in Q2 are trough.

**Robert Komin**  
*Senior VP, CFO & Treasurer*

So the rental costs that we're assuming for the rest of the year are baked into Q2 and the annual guide.

**Operator**

Our next question comes from the line of Vijay Rakesh of Mizuho.

**Vijay Rakesh**  
*Mizuho Securities USA LLC, Research Division*

Congratulations on a good quarter and guide. Just wondering, you mentioned 50 megawatts per month ramp into 4Q '26. I'm just wondering how that is going? And how do you see that scaling into 2027? And I have a quick follow-up.

**Andrew Feldman**  
*Co-Founder, CEO, President & Chairman*

I don't think I mentioned that. I'm -- maybe I didn't hear the question right. Could you repeat the question?

**Vijay Rakesh**  
*Mizuho Securities USA LLC, Research Division*

I think you had talked about 50 -- I believe you had talked about a 50 megawatts per month ramp into 4Q '26. And then just wondering how that is going and how you see that beyond -- how that capacity ramping into '27?

**Andrew Feldman**  
*Co-Founder, CEO, President & Chairman*

Yes. Okay. I don't remember giving specifics on the monthly ramp. We are seeking, on average, a huge amount of capacity in through the end of '26 and into '27. As you know, we signed our agreement with OpenAI at the end of '25, which means you probably need 6 or 8 or 10 months at a minimum to bring on vastly more capacity. And as our business ramps, we are signing large deals as well, many of which will come on in the first part of 2027.

I think we announced a 120-megawatt deal with Bell Canada, for example, in a facility there that does have room to expand. So I think the -- while we haven't given specifics, we are working our hardest to add as much capacity as we can between now and the end of '27.

**Vijay Rakesh**  
*Mizuho Securities USA LLC, Research Division*

Got it. And then obviously, you mentioned fast inference is very disruptive. You see a lot of LLM frontier model guys try to move to fast inferencing. Just wondering on how you see your customer pipeline broadening out into '27 if you were to look out beyond OpenAI and AWS?

**Andrew Feldman**  
*Co-Founder, CEO, President & Chairman*

Sure. Look, we're pleased with the way the customer pipeline is going. I think, obviously, deals of the size of OpenAI or the size that AWS could do are few and far between. But the business is robust, and we're happy at the rate at which we're signing new customers. We're also happy at the rate at which existing customers are doubling down, growing their footprint and the rate at which sort of their token consumption is up and to the right. And so on all fronts, we're pretty pleased.

**Operator**

Our next question comes from the line of Richard Shannon of Craig-Hallum Capital Group.

**Richard Shannon**  
*Craig-Hallum Capital Group LLC, Research Division*

Congrats on the first quarter call here. Andrew, my first question is following up on one of your -- a couple of your prepared remarks regarding OpenAI. You talked about stepping up a new model under 35 days here. Then you also mentioned about doing some work with GPT 5.4. I'd love to hear about your experience in bringing up the [ serving ] model, the Codex-Spark, and what you've learned from that and how you apply that to working with the [ GPT 5.4 ] that you might see going forward with OpenAI and/or other customers?

**Andrew Feldman**  
*Co-Founder, CEO, President & Chairman*

I think foundation model providers are fundamentally different. They are at the absolute cutting edge. What you see when you engage with them is really quite extraordinary. And the amount of work that goes into a foundation model and the visibility that we have is really one of the exceptional advantages that we get from this partnership.

So I think beginning with Spark, we got better. I think it improved us. It challenged us. We were up to the task. We very much enjoy working with their engineering team. And I think from the feedback we've gotten, they found a kindred spirit and enjoy working with our team as well. And so I think the way to temper metal is with fire. And I think we're proud of our work with them and our continued work. And so I think it's a really thoughtful question. I think having access to extraordinary customers and partners is a fundamental and long-term differentiator.

**Richard Shannon**  
*Craig-Hallum Capital Group LLC, Research Division*

Andrew, my follow-on question is regarding AWS. There are media reports out there that Amazon may be trying to sell the Trainium-based hardware externally, not just in their own data centers. Do you view this as an opportunity for Cerebras?

**Andrew Feldman**  
*Co-Founder, CEO, President & Chairman*

I do.

Thank you. And with that, I think we'll wrap up.

**Operator**

Yes, sir. We have reached the end of the Q&A session, and that does conclude today's conference call. Thank you for participating. You may now disconnect.