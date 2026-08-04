---
ticker: CRDO
company: Credo Technology Group Holding Ltd
title: "Credo Technology Group Holding Ltd (CRDO) Presents at Bank of America 2026 Global Technology Conference Transcript"
published: 2026-06-04T15:12:56-04:00
article_id: 4912092
source_url: https://seekingalpha.com/article/4912092-credo-technology-group-holding-ltd-crdo-presents-at-bank-of-america-2026-global-technology
---
Credo Technology Group Holding Ltd ([CRDO](https://seekingalpha.com/symbol/CRDO#source=section%3Amain_content%7Cbutton%3Abody_link "Credo Technology Group Holding Ltd")) Bank of America 2026 Global Technology Conference June 4, 2026 12:20 PM EDT

**Company Participants**

William Brennan - President, CEO & Chairman  
Daniel Fleming - Chief Financial Officer

**Conference Call Participants**

Vivek Arya - BofA Securities, Research Division

**Presentation**

**Vivek Arya**  
*BofA Securities, Research Division*

BofA semiconductor semi-cap equipment research team. I'm really delighted to have the team from Credo Technology with us today. Bill Brennan, President and CEO; and Dan Fleming, the Chief Financial Officer. And as usual, I'll go through my questions, but please feel free to raise your hand if you would like to bring something up. Really delighted to see you, Bill and Dan.

**William Brennan**  
*President, CEO & Chairman*

Happy to be here.

**Question-and-Answer Session**

**Vivek Arya**  
*BofA Securities, Research Division*

Thanks for joining us. I know Bill we'll get into the nitty-gritty of the quarter and what's happening here and now, but I was really hoping you could kind of step back, zoom out and give us kind of what is your 5-year strategic vision? Because it feels like people think of Credo as a copper company. And if optics is the end goal, then copper doesn't have a long life. And that seems to me like such a subjective and perhaps incomplete way of describing, right, what your opportunity set is. So I think it would help to hear from you what your 5-year vision is.

**William Brennan**  
*President, CEO & Chairman*

Sure. But let me first maybe address the debate between copper and optical. I kind of view it as there's companies on stage maybe having the debate, if I imagine it that way. NVIDIA, Broadcom, Marvell, Astera, Credo. And I think the debaters have stopped talking. Debate is over. It's going to be a heterogeneous world. I think all of the companies have communicated that. It's not one or the other. It's in different parts of the network, how do you solve for reliability and signal integrity and power efficiency and reach. These types of things will drive the decisions that our customers make as to which connectivity solution will be used for different parts of the network.

I think we all see the pluggable market. When we think about pluggable, we think about optical. And we see that pluggable market growing extremely quickly. I view our AEC products as part of the pluggable market. It's just the short reach pluggable. And so if you believe that optical is growing, which we all see it growing at leaps and bounds, that's what you're going to see in AEC as well. The pluggable market will grow, both will grow together. If we talk about scale up, that's where it gets interesting, and we can talk more about that. So let me zoom out a bit and talk about where we've been and where we're going. So I feel incredibly great about our earnings call on Monday of this week.

We just announced our fiscal '26. And to put things in perspective, if we go back 2 years ago to fiscal '24, we were sub $200 million in revenue. Fiscal '24 to fiscal '25, we more than doubled to $437 million. This year that we just reported, we more than tripled. So there's an acceleration in our revenue from less than $200 million to greater than $1.3 billion. And the trajectory I expect to continue, as Dan alluded to a greater than 80% number, not 80%, but greater than 80%. And there's a lot of numbers that are greater than 80%, 81% is, and there's a lot of numbers that are also larger.

So I feel great about just the transformation of the company. If you zoom in on that, we're really recognized as the pioneer of the AEC market. A lot of people didn't believe the market was a large market. Now we see competition confirming they're coming to the market because the market is growing. I see that market growing for the foreseeable future. I was asked the question yesterday, when do you see the peak? And I don't see the peak. So I see our AEC business continues to grow over the next 5 years. I will say that to frame it at a high level, what we've been working on the last 2 years, everything that we've been working on investing in and bringing to market, reliability has been our North Star.

Reliability is becoming much, much more important in clusters because the connections between NICs and the first switch, the TOR, there's no redundancy. And in a cluster of say, 10,000 GPUs or 100 or 1 million, all of these first links from GPU to switch, no redundancy. If you do have link instabilities, it can literally bring the entire cluster down. We learned this from our customers. We learned it first with AECs because we had customers that were converting their rack architecture from -- or a row architecture from connections that were longer than 7 meters.

That's why we did 7-meter cables was because xAI, in particular, asked us because they were going to re-architect with liquid cooling so they could connect all of their GPUs, switches with AECs, which are fundamentally bulletproof from a reliability perspective, 1,000x more reliable than laser-based optics. So fast forward to the discussion about ZF Optics, which we'll get into and just describing that product was designed for that link or eliminating link instabilities between GPUs and switches, not at a core technology level, but by going up the stack. So designing a custom DSP that was capable of lighting up rich telemetry on every link. It's not -- you go -- there's 6 links between a GPU and a switch.

So there's one to the switch and one from the switch to the NIC. And so there's one link to the module, module to module and then module to switch. So lighting up rich telemetry on all of those links so that we can predict when a link instability is going to happen because we're monitoring signal integrity continuously across the entire cluster where ZF Optics are deployed. So basically bringing up a cluster quickly time to stability, which is dollars. If you buy billions of dollars of gear and it takes you 8 weeks or 12 weeks to bring the cluster up to a stable point so you can start generating revenue, that is hugely expensive compared to bringing it up in a week and then keeping it at near 100% uptime.

Again, that's a financial return for the company. So generally speaking, the ZF Optics part of our business, we're now addressing the complete pluggable TAM. And it's not as if we're competing with commodity optics. What we're doing is we're offering an upgrade to something that's much more rich from a feature standpoint to address that portion of the market. And so I think that market is -- can be a very large market. And so when we think about the profile of just those 2 pieces of business for us, imagine AEC is growing over the next 5 years. And then add to that an even faster-growing ZF Optics portion of our business, not going to be one in lieu of the other. It's going to be additive.

And so I feel great about both of those core businesses for us growing. And then we think, okay, what else are we doing, right? And so we're going to be viewed much more than an AEC company because in reality, we're bringing the full spectrum of connectivity products across the entire data center from short copper links all the way to facility-wide optical links. But also we're going closer to the die. So there's a lot of die-to-die innovation that we're doing. We call that effort OmniConnect, and it leverages our position with very, very optimized SerDes and also gearboxes to enable GPU makers to do a composable design.

The first thing we're attacking is the memory wall on inference, and we're really unlocking the fan-out problem that you have physically on a die edge area as well as how far you can get the memory away from the main die. So our first customer, Positron, is really turning a lot of heads because they've introduced an inference engine that has 2 terabytes of memory. That compares to 128 gig for other solutions in the market. So AI-generated real-time video is now going to be super high performance, and that's a huge market. It's one of the markets they're addressing. But when we think about ourselves, we think of ourselves as a full spectrum company from die-to-die to facility-wide with reliability as our North Star.

**Vivek Arya**  
*BofA Securities, Research Division*

Got it. Absolutely. Before I go into -- as I was coming in, one investor actually asked me, does Credo have a role in these new agentic CPU clusters that are seen as kind of an incremental or that is not an addressable market for you?

**William Brennan**  
*President, CEO & Chairman*

Yes. Short answer is absolutely. Those servers need to be connected to the TOR. So it looks like a front-end connection. So if you see a surge in CPU demand driven by agentic, you can count on the fact that all of those will need to be connected. So AECs will play a role.

**Vivek Arya**  
*BofA Securities, Research Division*

It's kind of just a similar application expanded.

**William Brennan**  
*President, CEO & Chairman*

Right. So when we think about the AI connectivity market in general, I don't think we've ever been in a better place. The cluster sizes are increasing, but applications are becoming more diverse. Training, a lot has been talked about with inference even being larger than training and now agentic is like the third leg of the stool. So all of those opportunities make the AI connectivity opportunity at large much, much better, much more exciting.

**Vivek Arya**  
*BofA Securities, Research Division*

Got it. You mentioned the $1.3 billion in sales last year and the growth rate, which, by the way, if I'm right, is actually faster than the growth rate of any optical company, right, that I cover. So that first principle shows, right, that you're not -- you're actually gaining share in the connectivity market, right, not losing share. Yes. But if you look at the next 5 years, what is the right way, Bill, to size how large the AEC market? Like is there a first principles way of doing how large that market would be? Because -- and is there a point at which the per lane speed gets to a point, I don't know whether it's at the 200 gigabit per lane generation or the 400 gigabit per lane generation where even AECs cannot keep up.

**William Brennan**  
*President, CEO & Chairman*

Well, I think to address the speed question first, the 200-gig per lane horse is out of the barn, right? We showed 6-meter solutions at OFC. And we showed every next-generation potential rack and row deployment, all connected with AECs for the scale-out network. For 400, we're going to be developing solutions across the entire portfolio. And there's a new product that we're developing that's based on wide and slow that has the equal reliability to copper. And so we believe copper absolutely will exist for 400, but we'll also have an alternative product with micro LED as the light source that's wide and slow that delivers same reliability, same power efficiency and a longer connection up to 30 meters. So I think from a standpoint of the pluggable portfolio, that 400-gig question is already answered from our perspective. There will be heterogeneous solutions even...

**Vivek Arya**  
*BofA Securities, Research Division*

There's no...

**William Brennan**  
*President, CEO & Chairman*

Wide and slow optical. Yes. And so when we talk about what the potential size of the market is, there are certain forecasters that put it out at the $10 billion level. I'd like to think about it from the standpoint of there's so many reasons why that market is going to grow along with the rest of the connectivity market. So it's hard for me to say where is the peak, but I definitely agree that it's going to be in that ZIP code.

**Vivek Arya**  
*BofA Securities, Research Division*

Got it. Okay. Now you have also invested a lot in expanding the optical part of the portfolio, right, whether it's through silicon photonics, right, whether it's through your DSP. So maybe walk us through how large is the optical part of the business as part of the $1.3 billion? And I think you gave some forecast, right, for what the growth might be in fiscal '27, I believe.

**William Brennan**  
*President, CEO & Chairman*

So maybe it's a little known because of our revenue profile, but we've been investing in optical DSPs for many years. And so we have absolutely best-in-class DSP solutions that are ramping. So that -- the comment that I made about the optical DSPs, SiPho PICs and ZF Optics that all of them will grow to more than $100 million, and all of them are growing faster than the company is growing. Interesting point. Gave a total of greater than $600 million.

**Vivek Arya**  
*BofA Securities, Research Division*

$600 million.

**William Brennan**  
*President, CEO & Chairman*

All 3 of those markets are multibillion-dollar markets. And so we're emerging as a DSP supplier at the same time Dust was emerging as a SiPho PIC company and at the same time that ZF is going to ramp. The -- I think the collective market there is -- it's the largest addressable opportunity that we've got when we think about selling components to the commodity market and doing feature-rich solutions that are reliability first with ZF Optics. So I think that we're going to see that be a very fast-growing part of our business that layers in on top of a growing AEC business.

**Vivek Arya**  
*BofA Securities, Research Division*

Got it. On the competitive landscape, and $600 million, just to put that in context, based on what was said about next year would be almost 1/4 of the business, right? So it's not small anymore, right?

**William Brennan**  
*President, CEO & Chairman*

It's definitely not small. And the market opportunity is not small. And it's important to point out that you have to have the right products with the right customer engagements at the right time and you have to match supply with that demand. And so it's important to point out, especially on ZF Optics as we look to take responsibility for the entire transceiver. We've been in the demand generation mode for probably 6 months or so since OCP last year. But we've been in a mode of locking in supply for more than 12 months. And so leaning in with 3 partners that will assemble these transceivers, locking in supply of lasers, locking in supply of every component and the overall capacity.

I mentioned on the call that exiting this year, we'll be producing numbers that are measured in 100,000 unit increments monthly, and then we're going to be doubling and tripling that in the following year. So we're going to have the supply to match the demand that we're generating. And you can do the numbers on that and the numbers can be quite large. So I think it's going to be a much faster-growing part of our business than well, a much faster growth to say, $1 billion in revenue than we achieved with AECs because we're going into a market -- the market exists and the market needs like more and more reliability is the answer to the challenges that the customer base is having. That's why it can grow quite quickly.

**Vivek Arya**  
*BofA Securities, Research Division*

Got it. So on the competitive landscape, it's interesting that in the AEC market, you are the incumbent. And you have folks such as Marvell or Astera, other, right, talking about their AEC products. In DSP, Marvell is the incumbent, and you're talking about, right, the potential for, right, and you know Marvell quite well. So how do you look at the competitive landscape? Like is there a certain market share where the leader says, you know what, this is good enough for me, and it is okay to have others come in. And then the same thing as on the -- similar question on the DSP side. What is your sort of, I don't know, natural market share, right, is a phrase.

**William Brennan**  
*President, CEO & Chairman*

Yes. I will say that I don't think Marvell is going to ship cables.

**Vivek Arya**  
*BofA Securities, Research Division*

Right. They're only approaching a part of the market.

**William Brennan**  
*President, CEO & Chairman*

And I say that in a way that really highlights the fact that we're a different business model. And the reason we ended up here taking ownership of the entire system solution, we're not that smart, right? We originally thought we could sell DSPs to copper cable companies. But what we found out was that the challenge is much, much more difficult than it appears, just add a chip to a cable and you're good to go. It's really -- it's -- there's challenges across like the entire development cycle from SerDes to silicon development to system-level design to firmware to the software, to qualification to owning the supply chain.

We have learned so much in the last 5 years that there's really no other way that we can imagine doing it. And so we've got a team that I have more than 20 SKUs in flight -- new SKUs in flight at any given time based on any one of our customers asking and when they ask for innovation, we'll do special things that are above any kind of IEEE spec. We've got the ability to qualify those internally in parallel at the same time. We've got more than 20 thermal chambers down in Taiwan, where I take my customers' switches, my customers' NICs, we run traffic at full speed, and we do crazy things like varying temperature, varying voltage from high to low, power cycling.

The whole goal is to break the link. When you break the link, you quickly diagnose what failed and then you come up with a strategy to make the solution more robust so the link doesn't fail in those conditions. You do that iteratively until the link doesn't fail anymore. You add 2 to 3 orders of magnitude of error rate improvement. And then when we go into qualification with our customer, we never fail. And they know that because we're providing all of this qualification data to them. To my knowledge, we're the only company that is going this deep and you can talk about competitive advantage.

I also believe that being completely responsible for the supply chain, not just handing off a DSP and hoping, handing off and hoping is really not a great strategy on satisfying the likes of these hyperscalers. And so the depth of relationship that we've got with our entire supply chain is one where we have ramped an incredibly large capacity very quickly and flawlessly. Everybody has -- we've never stood in the way of a cluster deployment. And so in a way, becoming a trusted partner from a design, development, qualification and production, I think that's the competitive playing field.

It's no longer just saying, I've got a DSP and I'm going to take market share. It's natural that we're not going to have 100% market share. We've never aspired to that. The way that we compete is each customer delivering first, qualifying first, ramping first and being flawless with delivery. And so that's how I think we can maintain high market share.

**Vivek Arya**  
*BofA Securities, Research Division*

Got it. As many of your large customers make the move towards Vera Rubin, right, and other NVIDIA, there is a perception that NVIDIA is able to bundle a lot of products as part of that cluster, right? Because if you look at just how they plan to monetize per gigawatt, it shows as if it's a lot of their content. So when it comes to the decision on this front of rack, NIC-to-TOR connection, who makes that decision? Is it somebody like an NVIDIA who's providing the whole cluster? Or is it the hyperscaler who is making that decision?

**William Brennan**  
*President, CEO & Chairman*

We feel definitely it's the hyperscaler, but more and more, it's the neocloud as well. So when we talk about the customers we're working with, I mentioned that we're deeply engaged with 5 of 6 of the hyperscalers. But more and more, we see the neocloud category is raising a lot of money. The CapEx numbers are growing. The size of clusters are growing. And everybody's got the same challenge. Even for the neoclouds, it's more than the hyperscalers. How do you stand up a cluster quickly and how do you keep it up? And so it's a combination of either AECs or ZF Optics. And more and more, we're seeing that the end customer is making the decision.

**Vivek Arya**  
*BofA Securities, Research Division*

Got it. Anything from a supply constraint? I mean, doubling, tripling every year, I imagine, brings a lot of its own, right, set of good problems to have challenges in terms of ramping supply. So any place where you are seeing constraints that can hold back the kind of growth rates that you're aspiring to for next year?

**William Brennan**  
*President, CEO & Chairman*

So we've got 2 operations team. We've got our silicon operations team, and we've got our system solution operations team. And the -- let's talk about silicon first because that's a hot topic today. And let's talk specifically about 1.6T because everybody sees that's where the market is going. Every solution that we're aware of that does 200 gig per lane, 1.6T, 8 lanes of 200 is done at 3-nanometer. So there's -- I don't think there's any 5-nanometer that are going to go to volume production because power is simply too high.

So you're talking about a potential real crunch in 3-nanometer capacity. It's been discussed at an industry level for several months now. And there's an indicator from TSMC, they're bringing on huge capacity in Taiwan and Japan and Arizona, but that's really a '28 kind of time frame. This is what they're signaling. And so I'll talk about it from a Credo perspective first. I feel comfortable that we've underpinned through '27 based on our growth trajectory. Now you've got to understand that we're not building big GPUs. We're not building NICs, and we're not building switches. And so the challenge from a wafer capacity standpoint is a much less of a challenge than these other larger chips.

So -- and by the way, TSMC fully understands that these small complementary connectivity chips are needed to deploy clusters. If you take this small amount of wafers and you short those, you're basically locking in disruption in the entire deployment. So I feel confident that we'll have our needs underpinned. But I will say, generally, I think it's going to cap 200-gig per lane deployments. If people aren't as thoughtful as they can be. And one of the things I said on the call was that from a connectivity standpoint, there's a way to get 1.6T of bandwidth without necessarily doing 200 gig per lane.

A lot of these sleds are designed with 2 physical ports. And if you populate those 2 physical ports with either 4 lanes of 200, totaling 8 lanes of 200, you can get there that way or you can get there by doing 8x100 and 8x100. So just that in itself can ease the 3-nanometer supply chain crunch. And -- but I would say that even with that said, I think there's going to be tremendous growth in the next year for the industry.

**Vivek Arya**  
*BofA Securities, Research Division*

Got it. What proportion of your product is on 200 right now and as -- or if you have it for 50, 100 and 200? And then I imagine that every time you make a jump to the next higher port speed that there is a content expansion opportunity.

**William Brennan**  
*President, CEO & Chairman*

Yes. So right now, 200 gig per lane is not taking off in high volume. We're ready. Our portfolio is ready across the board from copper to optical. But I see that really that transition in deployments happening maybe towards the end of this year.

**Vivek Arya**  
*BofA Securities, Research Division*

That's still more in scale-out aggregation layers.

**William Brennan**  
*President, CEO & Chairman*

Yes, absolutely. There's always going to be a content increase as you go to faster lane speeds and higher bandwidth. So that is a -- that's a tailwind for the connectivity market for sure. So you'll see -- you saw an uplift from 400 to 800. You'll see an uplift from 800 to 1.6T. And it's regardless if there's 2 ports of 100-gig solutions or a single port of 200 gig.

**Vivek Arya**  
*BofA Securities, Research Division*

Got it. Okay. Maybe if I could bring Dan into the conversation on margins. So one thing that has been fascinating is that despite the growth that you have had, you've kept a very tight lid on expenses. And I know every time I get on the call, I always ask you the question, are you investing enough? Like how much more leverage is in the model? So Dan, maybe just walk us through how you are kind of allocating capital, right? Are you investing enough in the business? And can margins still go up from here?

**Daniel Fleming**  
*Chief Financial Officer*

Yes, we certainly believe that we're investing enough. And just to reiterate some of the points that we made on Monday, in terms of OpEx and revenue growth. So as Bill mentioned, 80% plus year-over-year revenue growth in our fiscal '27 is our expectation. And on the OpEx side, 50% year-over-year growth, which is meaningful investment in additional R&D resources. Key note from an operating leverage standpoint is the growth rate of revenue was 1.5x that of OpEx. So there's continuing leverage in the model.

But what's most important, of course, is that we are investing appropriately in the future. We've laid out over the last few quarters, a large multiyear roadmap. But bear in mind that at the very core of all of our products is our core SerDes technology. So that's highly leverageable across everything. So that's maybe the key point not to overlook. While we go into some new markets, silicon photonics was a new addition of course. So there's investment there. But many of these things that we've laid out from a roadmap perspective are really core SerDes-based products.

**Vivek Arya**  
*BofA Securities, Research Division*

Got it. I think you peeked at my next question because that was going to be the next one on SerDes. And that's -- I think the other thing to actually call out, right, about Credo that unlike some of your peers, you actually do own your own SerDes. And the question to you, Bill, is that do you think that is leverageable in products that we have just not heard about? Are there areas where you can even collaborate, participate, even license your IP like switches you mentioned, right? I mean that's a critical part. I mean the one thing that has made the largest switch company what it is, is SerDes, right? So how do you think about leveraging your SerDes capability?

**William Brennan**  
*President, CEO & Chairman*

I don't want to be too outspoken, but I'm sure happy that as I sit here talking about the connectivity market and knowing that from our perspective, the SerDes unlocked the entire opportunity and created the differentiation that has put us in business and has caused us to be able to accelerate our growth so much. We think it's absolutely critical to be able to make optimized application-specific core technology. It's all about reach, power, size. When you have the ability to deliver that at a core level, and that ultimately leads to your silicon product that ultimately leads to your system-level product. And then you can wrap it with firmware as well as this telemetry software now that we're doing, we think it's just absolutely critical.

**Vivek Arya**  
*BofA Securities, Research Division*

Right. So no new products to announce right now.

**William Brennan**  
*President, CEO & Chairman*

I mean when we look at the amount of innovation that's going to happen as the world goes to NPO solution and CPO, that SerDes capability to be on both sides of the connection or just looking at the entire connectivity piece, I think it becomes critical to have the ability to be on the leading edge of innovation. It gives you that fundamental tool that we think is necessary.

**Vivek Arya**  
*BofA Securities, Research Division*

Got it. And then just maybe last question. Your decision to invest in silicon photonics, the DustPhotonics acquisition, walk us through how it fits into your strategy? And what is the synergy with your pipeline today and what it can be going forward?

**William Brennan**  
*President, CEO & Chairman*

Yes. So we work closely with the Dust team on several optical module designs for our DSP customers. So we knew the technology was absolutely leading edge. It's very unique in a sense that there's a reduction in the number of lasers needed with the solution, where typically you would need 8 lasers. They require only 2. So a 75% reduction.

**Vivek Arya**  
*BofA Securities, Research Division*

So SiPho plus CW gets you.

**William Brennan**  
*President, CEO & Chairman*

Yes. So it's really a great solution. And that leads to better reliability, better power, better cost. It leads to all of the things that the market is looking for. And so from a component standpoint, they bring with them a lot of momentum. And that's momentum for 800 gig, 1.6 and 3.2. So they're pretty deeply engaged with a wide group of players. As it relates to our ZF Optics business, it means that we can do a tighter integration. We can do better from a telemetry standpoint. We can do better from a diagnostic standpoint. We can make the overall system solution better.

And it also is good from Dan's perspective because when you're coming in at cost as you build up your BOM and you're not buying an $80 DSP, you're buying -- we basically got something that's a fraction of that going into your cost. Same with the PIC, that's the second most expensive component. So you're coming in at cost on that. It really enhances your margin profile to have that be something that you're vertically integrated with. And you could think about other components and we worked on other components in the past. You can think about us adding to that vertical stack in the future.

**Vivek Arya**  
*BofA Securities, Research Division*

Okay. With that, thank you so much, Bill. Thank you, Dan. Really appreciate you taking the time.