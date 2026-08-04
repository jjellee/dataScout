---
ticker: RGTI
company: Rigetti Computing, Inc.
title: "Rigetti Computing, Inc. (RGTI) Q1 2026 Earnings Call Transcript"
published: 2026-05-12T11:20:56-04:00
article_id: 4902675
source_url: https://seekingalpha.com/article/4902675-rigetti-computing-inc-rgti-q1-2026-earnings-call-transcript
---
Rigetti Computing, Inc. ([RGTI](https://seekingalpha.com/symbol/RGTI#source=section%3Amain_content%7Cbutton%3Abody_link "Rigetti Computing, Inc.")) Q1 2026 Earnings Call May 11, 2026 5:00 PM EDT

**Company Participants**

Subodh Kulkarni - CEO, President & Director  
Jeffrey Bertelsen - Chief Financial Officer

**Conference Call Participants**

Brian Kinstlinger - Alliance Global Partners, Research Division  
Sreekrishnan Sankarnarayanan - TD Cowen, Research Division  
Quinn Bolton - Needham & Company, LLC, Research Division  
Craig Ellis - B. Riley Securities, Inc., Research Division  
Vijay Rakesh - Mizuho Securities USA LLC, Research Division  
Antoine Legault - Wedbush Securities Inc., Research Division  
Troy Jensen - Cantor Fitzgerald & Co., Research Division  
John McPeake - Rosenblatt Securities Inc., Research Division

**Presentation**

**Operator**

Good day, ladies and gentlemen, and thank you for standing by. Welcome to the Rigetti Computing's First Quarter 2026 Financial Results Conference Call. [Operator Instructions] As a reminder, this conference call is being recorded. At this time, I would like to turn the conference over to Mr. Subodh Kulkarni, CEO of Rigetti. Sir, please begin.

**Subodh Kulkarni**  
*CEO, President & Director*

Good afternoon, and thank you for joining us for Rigetti's First Quarter 2026 Earnings Conference Call. I'm pleased to be joined today by our Chief Financial Officer, Jeff Bertelsen, who will walk you through our financial results in more detail following my overview.

Also with us is our Chief Technology Officer, David Rivas, who will be available to participate in the Q&A session following our prepared remarks. We appreciate your continued interest in Rigetti, and we look forward to answering your questions at the conclusion of our remarks. Before we begin, I would like to remind everyone that today's call, along with our first quarter 2026 press release, contains forward-looking statements. These statements reflect our current expectations, objectives and underlying assumptions regarding our outlook and future operating results.

These forward-looking statements are subject to a number of risks and uncertainties that could cause actual results to differ materially from those anticipated. Such risks and uncertainties are described and discussed in greater detail in our filings with the Securities and Exchange Commission, including our Form 10-K for the year ended December 31, 2025, our Form 10-Q for the 3 months ended March 31, 2026, and other periodic reports filed by the company from time to time with the SEC. We encourage you to review these filings for a comprehensive discussion of these risks and uncertainties that could cause actual events and results to differ materially from those contained in the forward-looking statements. Rigetti undertakes no obligation to update any forward-looking statements made during this call, except as required by law.

During today's call, we will refer to certain non-GAAP financial measures. For details on these measures and reconciliations to comparable GAAP measures, and for further information regarding the factors that may affect Rigetti's future operating results, please refer to today's earnings release on Rigetti's website at investors.rigetti.com or to the 8-K furnished with the SEC today after the close.

Before I begin, I want to frame today's discussion around 3 key takeaways. First, with the general availability of our 108 qubit Cepheus-1-108Q system on Rigetti Quantum Cloud Services, Amazon Braket, Microsoft Azure Quantum and qBraid, we believe we have delivered one of the most powerful generally available quantum computers in the world and the largest modular quantum computing system on the market today.

Second, we are seeing growing adoption of Rigetti systems across government, academic and commercial customers, including new on-premises Novera QPU sales that support meaningful year-over-year revenue growth. Third, we remain focused on disciplined execution against our roadmap to Quantum Advantage continuing to improve fidelity on Cepheus-1-108Q and advancing toward higher qubit, higher fidelity chiplet-based systems underpinned by a strong balance sheet and prudent capital deployment.

Now I'll step back and put the quarter in context. Q1 was an important proof point in our strategy to combine technical progress with real-world use, access and usage. Quantum computing remains a long-cycle opportunity, but we are increasingly seeing the ecosystem coalesce around platforms that can scale in a practical way and that are available to users where they already run their workloads. Our progress this quarter reflects that reality.

Let me start with our technology and product milestones. Last month, we announced the general availability of our 108 qubit Cepheus-1-108Q quantum computing system, accessible to customers via Rigetti Quantum Cloud Services and through Amazon Braket, the quantum computing service by AWS as well as Microsoft's Azure Quantum service and qBraid.

Cepheus-1-108Q is our highest qubit count system to date and the industry's largest modular quantum computing system, built from 12 interconnected 9-qubit chiplets. This system triples the number of qubits and chiplets from our previous 36-qubit Cepheus-1-36Q system, and more importantly, validates our proprietary chiplet-based scaling architecture in a production setting.

Today, Cepheus-1-108Q has achieved a median 2-qubit-gate fidelity of approximately 99.1% with gate speeds of roughly 60 nanoseconds and a medium single-qubit gate fidelity of 99.9%. These are meaningful performance levels at this scale, and we expect to continue improving fidelity throughout 2026 as we refine the performance of our individual chiplets, innovate across materials and fabrication and incorporate learnings from our prototype and R&D platforms.

We achieved a median 99.8% 2-qubit gate fidelity with 40-nanosecond gate speeds on our 9-qubit system by using a proprietary adiabatic CZ gate scheme. Leveraging the same gate scheme, we also demonstrated 2-qubit gate fidelities as high as 99.9% at 28 nanosecond gate speeds on a prototype system and those advancements are informing how we operate Cepheus-1-108Q and design future systems. From a systems engineering perspective, this launch is about more than just adding qubits. During development, we identified and mitigated coupling interactions between 2-level couplers that become more pronounced beyond the 100 qubit scale.

By defining our chip architecture to address those interactions, we effectively shifted the primary performance limitation from coupler behavior to coherence time, which we are confident we can address as we continue to optimize our entire stack. Also I want to highlight what this means for users. With Cepheus-1-108Q now available on Rigetti QCS, Amazon Braket, Microsoft Azure Quantum and qBraid, researchers and enterprises can access our highest qubit count system on platforms they already use for classical and Quantum R&D.

Cepheus-1-108Q is the first gate-based device on Amazon Braket with more than 100 qubits, offering improved fidelities that enable wider and deeper circuits for applications such as material science, optimization and quantum simulation. AWS is the leader in cloud infrastructure, so extending our relationship with Amazon Braket and now Azure Quantum and qBraid is an important validation of our technology and our go-to-market strategy.

Stepping back, we continue to believe that superconducting gate-based quantum computing with chiplet-based scaling offers a compelling combination of speed and scalability. Our current systems achieved gate speeds on the order of 50 to 70 nanoseconds, which is roughly 1,000x faster than some other alternative modalities such as trapped ion or neutral atom systems. As we scale, we intend to maintain those speed advantages while driving fidelity higher and integrating error correction ready gate at operations into the stack.

Let me now turn to customer momentum and market traction. Our strategy is to meet with customers where they are, whether that is on the public cloud, on hybrid infrastructure or in dedicated quantum centers. On the cloud side, the combination of Rigetti QCS, Amazon Braket, Microsoft Azure Quantum and qBraid provides global access to our systems, including Cepheus-1-108Q, and we are seeing strong interest from researchers who want to experiment on one of the most capable generally available gate-based platforms in the market today.

In parallel, we continue to expand our base of on-premises Novera QPUs. The Novera QPU is designed to integrate into a customer's existing cryogenic and control systems, providing a high-performance on-premises platform for Quantum R&D. Recent Novera wins include an order from the University of Saskatchewan, where our QPU will support quantum research and education. And we have also announced Novera QPU and Novera system sales to additional research organizations globally.

These on-premises systems deepen technical engagement, create multiyear usage pathways and showcases the flexibility of our product portfolio from 9 to more than 100 qubits. As discussed in our prior call, Novera and other system deliveries contribute to significant year-over-year growth, albeit with some variability quarter-to-quarter based on shipment timing and contract mix. For example, we expect a meaningful portion of previously announced Novera purchase orders to be recognized in the first half of 2026, and we are executing on additional system-level contracts, such as the C-DAC order we announced earlier this year. While the timing of revenue recognition can move between quarters, these contracts underscore growing demand for Rigetti QPUs and systems among national labs, universities and quantum computing centers.

We are also encouraged by continued engagement from commercial customers who are exploring quantum-inspired and hybrid use cases. While commercial revenue remains early, we are seeing increased interest from industries such as materials, logistics and financial services as they look to understand where quantum computing can augment classical high-performance computing over time. More broadly, we are starting to see tangible examples of how even relatively small-scale quantum systems can impact real-world workloads. For example, a team in China recently demonstrated that a 9-qubit quantum system could outperform classical reservoir networks with thousands of nodes on a realistic weather forecasting task, highlighting how modest-priced quantum devices can begin to disrupt AI and modeling applications.

We view results like this as early validation of the commercial opportunities like systems like our Novera QPUs and Cepheus class devices are positioned to address as they mature. Let me briefly connect this back to our long-term roadmap. We remain focused on a clear sequence of milestones that we believe positions Rigetti to reach quantum advantage in roughly 3 years. Near term, that means driving Cepheus-1-108Q to a medium 2-qubit gate fidelity of approximately 99.5% later this year while maintaining our gate speed advantages. Beyond that, we are working towards deploying systems that leverage our chiplet-based architecture as the foundation for eventually scaling more than 1,000 qubits with fidelities and gate speeds that support error-mitigated and ultimately fault-tolerant computation.

In support of this roadmap, we recently announced our intention to invest up to $100 million in the United Kingdom over the next several years to accelerate quantum computing development. This will be our first major investment outside the United States and builds on our existing 36-qubit system deployment at the U.K.'s National Quantum Computing Center as well as U.K. government's multibillion-dollar commitment to quantum technologies.

In parallel, we continue to collaborate with partners such as Riverlane and others to integrate error correction-ready capabilities into the stack. This includes support for high fidelity native gates, improved circuit compilation and control electronics enhancements that are designed to be compatible with future error-corrected architectures. Our intention is to update our published technology roadmap later this year once we have incorporated operational data from Cepheus-1-108Q and can provide more detail on the specific steps we expect to take toward quantum advantage.

Turning to the financial framework, our approach remains straightforward and disciplined. We exited last year with a strong cash position and no debt, giving us the flexibility to continue investing behind our technology roadmap and customer opportunities. Our spending remains concentrated in core R&D, including fabrication, chip designs and control electronics development, along with the CapEx required to support higher qubit count systems and associated cryogenics infrastructure.

While this results in elevated CapEx in the near term, we believe these investments are directly tied to the capabilities that will differentiate Rigetti in the market. We are not managing the business around short-term revenue optimization. We are managing it around credible progress towards large-scale, high-fidelity quantum systems that can deliver commercially meaningful value. To that end, our capital allocation remains focused on organic execution and we will consider M&A only where we can clearly accelerate our roadmap without compromising our financial discipline.

To close my remarks before turning it over to Jeff, I want to reiterate the 3 key messages we hope you take away from today's call. First, Cepheus-1-108Q is now generally available through Rigetti QCS, Amazon Braket, Microsoft Azure Quantum and qBraid, and we believe it represents one of the most powerfully, generally available gate-based quantum computers in the world and the largest modular system on the market today. Second, customer adoption continues to build across cloud and on-premises channels with Novera sales and other contracts, supporting strong year-over-year revenue growth and deepening our engagement with leading research institutions and emerging commercial users.

Third, we remain committed to disciplined execution on the roadmap that targets quantum advantage in about 3 years, anchored in our chiplet-based architecture, high-speed superconducting qubits, improving fidelity, a strong balance sheet and strategic initiatives such as our planned $100 million U.K. investment that enables us to invest with patience and control.

Thank you for your continued support and interest in Rigetti. I'll now turn the call over to our CFO, Jeff Bertelsen, who will walk you through our financial results in more detail.

**Jeffrey Bertelsen**  
*Chief Financial Officer*

Thank you, Subodh, and good afternoon, everyone. I will spend a few minutes walking through our first quarter 2026 financial results, our balance sheet and how we're thinking about capital deployment as we continue to execute on the roadmap Subodh described. For the first quarter of 2026, revenue was $4.4 million compared to $1.5 million in the first quarter of 2025. The year-over-year increase was driven primarily by on-premises Novera QPU deliveries and related contracts as well as certain government and research projects.

Gross margin for the first quarter was 31% compared to approximately 30% in the first quarter of 2025. Our first quarter 2026 gross margin was impacted by contract mix, including a higher contribution from QPU and system deliveries that include lower-margin third-party refrigeration. Total operating expenses for the first quarter were $27.3 million compared to $22.1 million in the same period last year. Spending remains concentrated in research and development, including engineering headcount, fabrication and system integration, consistent with the priorities we outlined on our fourth quarter call.

Stock-based compensation for the quarter was $5.9 million compared to $4.2 million in the first quarter of 2025. Operating loss for the first quarter was $26 million compared to an operating loss of $21.6 million in Q1 2025. On a GAAP basis, net income for the first quarter of 2026 was $33.1 million compared to net income of $42.6 million in the prior year period. The first quarter of 2026 included $53.7 million of noncash gains from the change in fair value of derivative warrant and earn-out liabilities compared to $62.1 million in the prior year period.

As a reminder, these noncash fair value adjustments can introduce significant volatility into our GAAP results quarter-to-quarter and do not affect how we operate the business or allocate capital. On a non-GAAP basis, which excludes stock-based compensation and fair value adjustments to warrant and earn-out liabilities. Net loss for the quarter was $14.7 million or $0.04 per diluted share, compared to a non-GAAP net loss of approximately $15.3 million or $0.05 per diluted share in the first quarter of 2025.

Let me provide a bit more color on revenue drivers and how we are thinking about the remainder of the year. As we outlined in our fourth quarter call, we expected strong year-over-year revenue growth in the first quarter of 2026, driven by shipment of a portion of the $5.7 million of on-premises Novera quantum computing system purchase orders announced late last year. The first quarter results are consistent with that view, and we continue to expect the remaining Novera revenue to be recognized primarily in the second quarter of 2026.

We also continued to execute on the $8.4 million C-DAC order for an on-premises 108-qubit system in India, which we expect to recognize in the fourth quarter of 2026 following installation and performance acceptance testing. As we said last quarter, the initial C-DAC order did not include ongoing maintenance and support. We still expect to receive a separate purchase order for those services. More broadly, our revenue profile continues to be influenced by the timing of system deliveries and government-funded projects. We continue to view this variability as inherent to the current stage of the market and not as a driver of our long-term capital allocation or technology strategy.

Turning to the balance sheet, we ended the first quarter of 2026 with approximately $569 million in cash, cash equivalents and available-or-sale investments compared with $209.1 million as of March 31, 2025, and approximately $589.8 million at the end of 2025. The year-over-year increase relative to Q1 2025 reflects the capital raised and strategic investment activity we have previously discussed, while the sequential decline from year-end reflects ongoing operating spend and capital expenditures.

We continue to operate with no debt. At our current operating profile, we believe our capital position provides sufficient runway to execute against the technology and system deployment milestones we have laid out, including continued progress on scale, fidelity and system integration as well as our planned investment in the United Kingdom.

Capital expenditures in the quarter were primarily driven by investments in Fab-1 and additional dilution refrigeration capacity to support higher qubit count systems over the next several years, consistent with the framework we outlined in the fourth quarter. We continue to expect 2026 CapEx to be elevated relative to prior years, largely due to refrigeration and infrastructure needs rather than major changes to our fab footprint.

Our approach to capital deployment remains disciplined and consistent with what we have discussed on the Q4 call. The majority of our spending is directed toward core R&D activities that directly advance our technology platform, including our chiplet-based architecture, control systems and cloud integration. We are not managing the business around short-term revenue optimization. We are managing it around credible long-term progress toward Quantum Advantage and commercially relevant systems.

To close, our financial strategy is unchanged from what we outlined last quarter. We are focused on maintaining flexibility, funding innovation responsibly and aligning capital deployment with the long-term value creation potential of our technology roadmap. While quarterly results will continue to reflect the early-stage nature of the quantum computing market and the timing of large system contracts, we believe our balance sheet and capital discipline position us to execute with patience and control.

With that, I will turn it back to the operator, who will open the call for your questions.

**Question-and-Answer Session**

**Operator**

[Operator Instructions] Our first question or comment comes from the line of Brian Kinstlinger from Alliance Global Partners.

**Brian Kinstlinger**  
*Alliance Global Partners, Research Division*

I'll ask 2. The first one is can you talk about the announced NVIDIA quantum models, when you expect they might be available and when you might begin to test them to see the impact it has on reducing your error rates?

**Subodh Kulkarni**  
*CEO, President & Director*

Thanks, Brian. NVIDIA did announce an open source model NVIDIA Ising to help out with calibration and bring up of quantum computers as well as error corrections. We continue to look at that as a possible means of accelerating our roadmap. We continue to talk to NVIDIA, and we also continue to talk to other partners in the industry, such as Riverlane in the U.K. where we are partnering to do error correction. They are not replacements for each other. They can work in a complementary fashion. So certainly, the announcement made by NVIDIA to help accelerate quantum computing in terms of calibration bring up, but also error correction, we are taking a close look and we'll definitely take advantage of those tools that are available now. Hopefully, that answers your question.

**Brian Kinstlinger**  
*Alliance Global Partners, Research Division*

Yes. Great. My follow-up, the $100 million investment in the U.K. Are those people, infrastructure, offices? And will that be expensed or capitalized? And if it's expensed, when will we start to see that begin to increase the OpEx?

**Subodh Kulkarni**  
*CEO, President & Director*

So let me put that U.K. investment in context. I mean, U.K. has announced a fairly ambitious program that they call ProQure, where it's a multistage program. Right now, the first phase will kick off this July or August for a couple of years. The next phase that they call MegaQuOp will kick off at that time for another year or 2 and then GigaQuOp and so on. MegaQuOp means 1 million error-free quantum operations per second, GigaQuOp means 1 billion error-free quantum operations per second and so on.

So it's a very well structured layout program. Right now, applications are being requested. We will be one of them. Assuming we are chosen for the preliminary phase, we definitely plan to increase our headcount, so there will be additional people cost. We definitely plan to increase the number of quantum computers we have in the U.K. Right now, if you visit the National Quantum Computing Center, outside Oxford in the U.K., you will find our quantum computer in that center.

But for the next phase, we definitely plan to include our Cepheus-1 like 108-qubit or higher qubit quantum computers over the next couple of years as we make them available. So there will be some capital costs involved, but also facilities. I mean, right now, our quantum computer sits in the NQCC facility, we definitely plan to have -- and we have a relatively small office in London right now. We definitely plan to have a bigger facility in the U.K. as we go forward. So the $100 million is over the next few years, but captures all the cost, in the rough order of magnitude that we talked about so far. Hopefully, that answered your question.

**Operator**

Our next question or comment comes from the line of Krish Sankar from TD Cowen.

**Sreekrishnan Sankarnarayanan**  
*TD Cowen, Research Division*

Subodh, I just wanted to ask you on the integrated error mitigation. Is this on-chip with the qubit gate? Or is it a separate control chip? Is it ASIC or FPGA. Can you give us some color on that?

**Subodh Kulkarni**  
*CEO, President & Director*

Krish, are you talking about the NVIDIA specific announcement?

**Sreekrishnan Sankarnarayanan**  
*TD Cowen, Research Division*

Yes, the one [ inside ] the integrated error mitigation, yes.

**Subodh Kulkarni**  
*CEO, President & Director*

Yes. In general, right now, we don't do error correction on the quantum chip itself. There are approaches that are being looked at to do that kind of stuff. But right now, our quantum chip is not doing error correction at the chip level. So most of the error correction and all the experiments we do are outside in the ambient conditions in the control systems area, and we are sending the signals to the quantum computer and then getting them back from the quantum computer.

**Sreekrishnan Sankarnarayanan**  
*TD Cowen, Research Division*

Got it. And just a question on the QPU pipeline. How is it looking? Has it evolved? Like is it -- over the last one quarter, I understand, besides the University of Saskatchewan, is the funnel expanding? Is it stable? How to think about it?

**Subodh Kulkarni**  
*CEO, President & Director*

You're talking about the overall demand for QPUs in general, I assume. That's what your question is?

**Sreekrishnan Sankarnarayanan**  
*TD Cowen, Research Division*

That's right. Yes. Yes.

**Subodh Kulkarni**  
*CEO, President & Director*

Yes. As we mentioned, interest in quantum computing continues to increase rapidly. And as we start getting closer and closer to that quantum advantage, which we defined roughly a 1,000 qubit, 99.9%, 2 qubit gate fidelity, less than 50 nanosecond gate speed and some form of error mitigation or control. And we roughly think that's about 3 years from now. Definitely, we are already starting to see increase in interest from not only academic and government national lab kind of customers, but also commercial customers who want to do quantum computing-related R&D activities, not necessarily use them for their data center operations.

We definitely expect that interest to continue to increase rapidly as we get closer to the quantum advantage milestone, roughly 3 years from now. And we're already starting to see that, as you can see in our disclosures and sales numbers. But overall, definitely expect quantum computing interest to increase, even though we are still in the R&D stages.

**Operator**

Our next question or comment comes from the line of Quinn Bolton from Needham and Company.

**Quinn Bolton**  
*Needham & Company, LLC, Research Division*

I guess about just maybe a follow-up on Krish's question there, just with the adiabatic CZ process, that you're already showing on prototypes getting to 99.9% 2-qubit gate fidelity. How long does that take to get into process? It sounds like you're targeting at 99.9% over a 3-year period that would be part of the system that gets to the quantum advantage. Why does it take so long to get there? Or just what are the steps you need to bring that process from sort of a prototype level into kind of higher volume production level?

**Subodh Kulkarni**  
*CEO, President & Director*

It's a good question, Quinn. I mean, we will obviously push as fast as possible to get adiabatic CZ and fast gates into higher scale systems. We are already using adiabatic CZ in our Cepheus-1-108Q 8, but it's not a very fast gate adiabatic CZ that we have been able to get at the prototype stage. You're right. At the prototype stage, we have 99.9% with gate speeds of 28 nanosecond. So you can see that our 108Q is still 2x slower than our prototype system and fidelity is not as high as the prototype system. So we definitely take the learnings from the prototype system and then try to include that in our larger scale systems as soon as possible.

It just takes time. I mean, these are extremely complex problems to solve at scale. It's relatively easy to demonstrate on prototype stages. And that's why you see many announcements from many different organizations about quantum computing and they are typically in the sub 10-qubit type level. It's only when you start getting to 100-qubit or above, and you hardly find 2 or 3 companies that have enabled quantum computers at that scale, and we are one of them.

We are proud to be one of them with the 108Q system right now that is available for anyone to use. It's -- that's where the problems becomes quite significant to tackle and solve. So yes, we have demonstrated very, very good performance with adiabatic CZ fast gates at a few qubit level, being able to take -- we need to take that learning and push it as fast as possible.

Definitely, it will be part of the final system that will approach quantum advantage in 3 years, but I'm pretty sure it will be included much before that, whatever we will start deploying next year and the year after that. We will definitely see adiabiatic CZ and fast gates coming in there.

**Quinn Bolton**  
*Needham & Company, LLC, Research Division*

Got it. And then I guess sort of related question. As you look to that system that gives you quantum advantage, would you expect that system to run quantum error correction? Or would you still be thinking about implementation of on-chip quantum error correction sort of being out beyond the quantum advantage chip in 3-ish years.

**Subodh Kulkarni**  
*CEO, President & Director*

It's a good question. There's a lot of TBD still right now on when it comes to quantum error correction. Specifically, we touched upon earlier -- in earlier question, I touched upon NVIDIA Ising model and how that could improve -- that could change, improve our roadmap, accelerate our roadmap. Our view right now is that the quantum advantage system, roughly 1,000 qubit system at 99.9% 2-qubit gate fidelity level. We'll use some form of error mitigation, not necessarily full fledge quantum error correction, the way we envision quantum error correction to be in roughly 4 or 5 years.

So our view is, for quantum advantage, we will have some form of error mitigation, error correction. But for full implementation of QEC, particularly when we talk about like qLDPC quantum, linear density parity core kind of error correction. We are talking about fault-tolerant quantum computing, which we are talking about hundreds of thousands of qubits. And that, we think, is in the 5- to 7-year kind of a time line period. That's when you really start looking quantum error correction in its full manner. For the quantum advantage, you'll be talking error mitigation and some form of error correction. Hopefully, that answers your question.

**Quinn Bolton**  
*Needham & Company, LLC, Research Division*

That does. I appreciate it. And then maybe just one quick one for Jeff. You said on the $5.7 million of Novera QPU sales that you had announced last year, you expected to capture most of the remainder in the second quarter. Looking at the Q you filed today, it looks like you had about $3 million of hardware-based sales. So is the remainder of that $5.7 million, roughly -- $2.7 million to be recognized in Q2? Is that sort of the right ballpark to be thinking about how the $5.7 million split between Q1 and Q2?

**Jeffrey Bertelsen**  
*Chief Financial Officer*

Yes. Of that $5.7 million, we recognized a little bit less than half of that in Q1. And then we expect the remainder to go in Q2.

**Operator**

Our next question or comment comes from the line of Craig Ellis from B. Riley Securities.

**Craig Ellis**  
*B. Riley Securities, Inc., Research Division*

Subodh, I want to start following up with some of the comments you made about the 108 qubit Cepheus' availability on Rigetti QCS and then on Amazon Braket and Microsoft Azure Quantum and qBraid. The question is this, as it's attained general availability, what are you seeing in terms of engagement across the various platforms? And are you getting any feedback in terms of what the workload tests are framing up as?

**Subodh Kulkarni**  
*CEO, President & Director*

Good question, Craig. It's still relatively early to talk about usage and what we are seeing since we just deployed the system as a month or so ago. Definitely, interest is high. Definitely, we are seeing usage to be quite high, but it's too early to make judgments on the basis of early data. Certainly, we expect this to be used very well over the next few months as word gets around and people explore and use it. And we will continue to improve the system, as we mentioned. We'll continue to improve the fidelity, so we'll deploy higher fidelity 108Q system sometime later this year. And we definitely expect usage to continue to improve as we improve the performance of the system.

**Craig Ellis**  
*B. Riley Securities, Inc., Research Division*

That's helpful. And then the follow-up question relates to one of your partnerships. So we established the Quanta partnership in 1Q of '25, the investment in Rigetti was formalized in early 2Q '25. As you look back at the first year of that deal, what would you identify as the top 2 or 3 things that are really going well and helping you in your ambition to scale up qubit count and system capabilities. And what would be the 1 or 2 things that you would hope that partnership could do this year?

**Subodh Kulkarni**  
*CEO, President & Director*

Thanks, Craig. That's a really good question. We entered into a strategic partnership agreement with Quanta. As you mentioned, they did invest at that time about $40 million in Rigetti. But more importantly, there was a commitment on both sides to invest. We continue to invest in the quantum computing side. Quanta investments are more on the non-quantum computing, but the rest of the hardware part of the stack.

And they have done that. We -- definitely one of the key accomplishments we can point out to is how well they have designed the new control system that we have started including in our most recent offerings. So our latest deployments that we are talking about to commercial customers and other customers are, we are exploring use of Quanta made control systems instead of our home-built systems. And Quanta, obviously, is a large company with extremely high capabilities in CPU, GPU cloud servers.

So they know how to build server boxes, control system electronics, and we can clearly see that their professionalism in building those boxes. And they have a dedicated team working on control systems that work with our systems. And going forward, we definitely will be using Quanta's control systems as part of our stack. It's not an exclusive arrangement. We will continue to maintain our capabilities in that area. And Quanta will also talk to other quantum computing companies as well.

So it's not like a mutually exclusive thing. But we definitely are benefiting with Quanta's expertise in control systems, and we definitely expect them to be contributing to other parts of the stack. So the first year, I would say, definitely control system. Next year or 2, we expect them to not only continue to develop better quality control systems, meeting our overall system requirements, but also get into the rest of the hardware stack.

Hopefully, that answers your question.

**Operator**

Our next question or comment comes from the line of Vijay Rakesh from Mizuho.

**Vijay Rakesh**  
*Mizuho Securities USA LLC, Research Division*

Just a quick question. So as you look at the Cepheus-108 qubit one, any thoughts on how -- what are you getting on the price uplift versus the 36 qubit one? And how the customer response has been on the Cepheus 108 qubit show availability on Azure and Braket, et cetera? And I have a follow-up.

**Subodh Kulkarni**  
*CEO, President & Director*

Yes, Vijay, it's still relatively early. We deployed the system just over a month ago. So it's still very early to talk about usage and what we are seeing. Definitely, interest is high. Definitely, we are seeing a lot of customers use the system right now. But it's still early to quantify that and talk about uplift over 36Q in terms of usage. Regarding price, I mean, we really are still talking about research kind of customers. So we are not talking about jobs that are very long in duration.

Most of the usage is on order of a few seconds to a few minutes at the most because people are still experimenting with quantum computing and fundamental understanding of quantum computing, how it can be used, basic algorithm development type research applications. So we are not really seeing commercial customers with data center type operations, trying to engage with quantum computing.

And frankly, we shouldn't be seeing that for the next year or 2. It's only when we start approaching quantum advantage in about 3 years should we expect those kinds of engagements to increase on cloud quantum computers. Cepheus-108 is one of the most powerful quantum computers on the cloud that is generally available for anyone right now. So definitely, I think this is what leading usage of quantum computing is what we are seeing right now.

So as we continue to improve the performance, increase the qubit count, increase fidelity, we definitely expect more and more commercial customers to start using quantum computers. Having said that, right now, we are still in the early stages. So hard to quantify the usage and the uplift over 36 qubit.

**Vijay Rakesh**  
*Mizuho Securities USA LLC, Research Division*

Got it. And then on the C-DAC, the $8.4 million win there, when do you start to see that layering into, the guide or when do you start to see shipments there?

**Subodh Kulkarni**  
*CEO, President & Director*

As we have stated, when we disclosed the order, our plan is to fulfill that order in the second half of this year, most likely in the Q4 time period, that's when we will physically shift the 108-qubit system. There are, I mean, quantum computer comprises various parts, dilution refrigerator, the parts inside, the cables and all that stuff. So overall, our plan is to get them up and running before the end of this year. And that's when we expect most of the revenues -- our revenues will get booked.

**Operator**

Our next question or comment comes from the line of Antoine Legault from Wedbush Securities.

**Antoine Legault**  
*Wedbush Securities Inc., Research Division*

Just, Subodh, could you remind us how you remain confident that the architectural fix that you recently achieved with tunable couplers. How durable is that as you scale beyond 108 qubits to a few hundreds, eventually over 1,000 qubits.

**Subodh Kulkarni**  
*CEO, President & Director*

That's a good question, Antoine, and we look at that very carefully as we continue to update our roadmap. Our fundamental architecture still continues to be square grid and tunable couplers. By the way, that's what we see other large companies too. Google's architecture similar to ours. IBM recently changed their architecture from fixed coupler to tunable coupler technology, so very similar to what we are doing right now.

So all 3 of us are deploying more on a similar architecture at that level. Tunable coupler, we all like them because it gives you an extra degree of flexibility to adjust the coupling between the qubits. So we definitely take advantage of that when it comes to parking the qubits at the right frequency and the couplers at the right frequency too. As of today, we -- where the difference is coming in is our view is that when we scale up qubit count, we need chiplets. So far, we have not seen IBM, Google or anyone else, at least get data on chiplets. We continue to monitor that area very closely. Our reasons for the use of chiplet is because it's fundamentally a lot easier to build a smaller dimension, chiplet than a larger dimension monolithic chip.

We have not seen any concerns with tunable coupler and a square grid architecture because of using chiplets. So we feel very confident that the roadmap we have from the current 108 qubit to improve the fidelity as well as the qubit count using chiplets is pretty solid, and we believe we will be able to execute it to get us to quantum advantages roughly 3 years.

**Operator**

Our next question or comment comes from the line of Troy Jensen from Cantor Fitzgerald.

**Troy Jensen**  
*Cantor Fitzgerald & Co., Research Division*

Just going right off of what you just said here. Quantum advantage is 3 years away for you guys. Is it safe to say that 2 chip cycles away? And I guess on that point, can you just talk about chip cycles. I think, previously, it was probably like 9 months, you guys were spitting out new chips and is it going to be a little slower going forward, 12 to 18 months? Any help on that would be great.

**Subodh Kulkarni**  
*CEO, President & Director*

Yes. Troy, I mean, as you know, we basically own our own fabs. So we have been operating our fab in Fremont, California for the last several years. So it depends on how many changes we do in the chip when it comes to chip cycle. So yes, we do launch a major revision of the chip once a year. But honestly, because we control our a fab, we can do it much faster if we decide to just focus on some particular aspect of the chip.

So we can turn around chips at a faster rate than once a year, maybe even twice a year. So 3 years gives us plenty of turns of chips in terms of major revisions. Certainly, a big part of getting to quantum advantage from where we are today comes from the chip side. But I don't forget there are other components coming on the stack that are quite important when it comes to quantum Advantage. The design part of the chip, obviously, but also the dilution refrigerator, the cabling, the control systems, the other error corrections, the error mitigation parts, the other parts of the software parts of stack, all of them contribute in terms of the performance, and we need to keep improving on all parts of those to get to quantum advantage.

So 3 years, we think, is a realistic time line. We have seen some other companies claim quantum advantage faster than that. Frankly, we are a little skeptical if you look at Cepheus right now, it's one of the best quantum computers in the world out there, if not one of the best, probably the best. And we think it still will take us roughly 3 years to get to quantum advantage. So when then there are companies out there who will talk about quantum advantage this year, some of them also talked about quantum advantage last year, to be honest, so we remain skeptical when companies make all kinds of claims without any data to support that.

We feel pretty good about Cepheus-1 performance right now at 108 qubit level. We think 3 years is a realistic time line to get all the metrics in the right place to deliver quantum advantage. Hopefully, that answers your question.

**Troy Jensen**  
*Cantor Fitzgerald & Co., Research Division*

Yes, that's perfect. But let me follow up. You mentioned dilution refrigeration. That's one area where your competitor is, not so much IBM and Google, but competitive methodologies can to hammer you guys on. Can you just talk a little bit about what needs to happen there? And once you're at this quantum advantage, what is the dilution refrigeration costs? Because I get it, if superconducting is the only technology that can commercialize quantum, who cares about dilution refrigeration cost? But if there's others that can and don't have that, can you just kind of hit that? That'd be great.

**Subodh Kulkarni**  
*CEO, President & Director*

Sure. So in superconducting quantum computing, we definitely need dilution refrigeration to cool our chips down to get the superconducting effects. So we are talking about cooling our chips down to 10 millikelvin and dilution refrigeration is a critical technology that enables us to get the most extremely cold temperatures. Dilution refrigeration itself is the technology was invented several decades ago.

So it's been around for select military space type applications. It's only finding its way in the commercial world now with quantum computing. So it's not like -- it's a brand-new technology that we are dealing with. It's been around for a while. There are 4 or 5 companies that have entered this area. They make dilution refrigerators that we can get off the shelves. We have relationships with 3 of them right now, and we'll continue to discuss with their roadmaps and how they plan to improve it.

If you look at a superconducting quantum computer, whether it's ours or IBM or Google or other companies, a dilution refrigerator looks like -- little bit like a large kitchen refrigerator, frankly, about 3 feet x 3 feet, maybe 4 feet x 4 feet and a cylindrical kind of a form factor.

The chip itself is fairly small. Our 108-qubit Cepheus with 12, 9-qubit chiplets, each of the chiplet is about 6-millimeter by 6 millimeters. So we are not talking large dimensions for 108 qubit. Even when we get -- go to several hundred to 1,000 qubit, we are not going to be talking very large dimensions here, we are talking few centimeters by few centimeters. So to cool that dimension to 10 millikelvin, the roadmaps that we have seen from commercial companies such as Bluefors or Oxford Instruments or Maybell allow us to get the 1,000 qubit and tens of thousands of qubit in the dilution refrigerator along with the roadmap. We certainly watch developments of those companies very carefully, and we take advantage of their developments as they come along.

It's a complex technology, but it's clearly not a bottleneck for getting superconducting quantum computing to quantum advantage and beyond. So I realized that other modalities don't have that issue to deal with dilution refrigerator. But frankly, when we look at the benefits we get because of superconducting, which are speed and scalability, I mean, our speeds are 1,000 to 10,000x faster than some of those other modalities that operate at room temperature. And that's a huge advantage when it comes to computing, obviously, when you have 1,000 to 10,000x speed advantage. But also scalability because we are dealing with chips, we can scale them up much faster than eletromechanical things like trapped ion or pure atom.

So we look at the challenges and opportunities that come with superconducting gate and frankly, the challenges with dilution refrigerator are relatively small compared to the benefits we get in terms of scalability and speed.

**Operator**

Our next question or comment comes from the line of John McPeake from Rosenblatt Securities.

**John McPeake**  
*Rosenblatt Securities Inc., Research Division*

Subodh and Jeff, congrats on getting the Cepheus out on the cloud. And I just have a question on that one. You're saying later this year, I think, to get to 99.5% from 99.1%. Maybe we could just dig in a little bit there on what needs to happen? And then I just have a quick follow-up. I know these questions kind of been asked, but maybe you can dig in a little bit more.

**Subodh Kulkarni**  
*CEO, President & Director*

Sure, John. As we disclosed in our earnings release, right now, the limiting factor for fidelity, particularly at 2-qubit gate facility, is our coherent strategy. That's the amount of time we can maintain the quantum states in. And right now, it's in the 25 to 30 microsecond range. We need to roughly double that, ideally triple that to get to the 99.5% type fidelity. So we know exactly where the fidility is being lost, if you will. We have several experiments that we are working on. We know what coherence depends on. So we feel pretty good about improving our coherence time and therefore, the fidelity as the year goes on.

Hopefully, that answers your question.

**John McPeake**  
*Rosenblatt Securities Inc., Research Division*

It does. The lab machine at 99.9%, I think it was a lab machine. What -- how many physicals were on? Is that a 9 qubit?

**Subodh Kulkarni**  
*CEO, President & Director*

The prototype was even smaller than 9 qubit, but we recently had data that we disclosed with 9 qubit. So we are already with the fast adiabatic CZ scheme, we have reached 9 qubit at high fidelity now. We need to get that to 36 qubit next and then 108 qubit, so we'll push on that as fast as we can.

**John McPeake**  
*Rosenblatt Securities Inc., Research Division*

Okay. And then the other question is just on DARPA. Any kind of update there? I think you guys were going to reengage.

**Subodh Kulkarni**  
*CEO, President & Director*

Well, we continue to be part of DARPA, so it's not a question of reengage. We continue to stay engaged with DARPA, we are part of the QBI program. They gave us feedback towards the end of last year, we are working on those things, error correction, the scaling area are some of the challenges we have. So we continue to work on that. We continue to stay engaged with them. So we feel pretty good that way. And it's an open-ended program as we hit certain milestones, they will get us into Phase B and eventually into Phase C and so on. So it's a program with 7 to 8-year time line with milestones-based graduation into the next phase, if you will. So we continue to stay engaged and we feel confident that as we continue to improve our performance, we'll get to Phase B and eventually to Phase C and beyond.

**John McPeake**  
*Rosenblatt Securities Inc., Research Division*

And you have a full U.S. supply chain, which I'm sure helps. And I did one more. The end of the year, I think we were talking about 150 machine. Should I still think about that 150 qubit machine?

**Subodh Kulkarni**  
*CEO, President & Director*

Yes. I mean, overall, what we have said is, the most important big milestone we have is the quantum advantage, which is roughly 3 years from now. And that's on 1,000 qubit at 99.9%, 2-qubit gate fidelity. So we are clearly -- we are right now at 108 Q at 99.1%. If you go smaller, we are at significantly higher fidelity, but they are smaller.

So we need to increase our qubit count roughly by 10x. We need to improve our fidelity from the low 99s to high 99s. So you are going to -- it's going to be a staircasing situation where we will -- there will be times as we increased the qubit count without increasing the fidelity and there will be times when we increase the fidelity without increasing the qubit count. Ideally, we'll do both simultaneously, but sometimes it gets difficult to do that kind of stuff, both at the same time.

So as this year goes on, definitely expect us to introduce a higher fidelity 108 qubit. We will be talking about 150 qubits or higher. We are not quite sure whether we will be able to include the higher fidelity at the 150 qubit levels or not. But definitely, the goal is to try to increase both qubit count and fidelity.

**John McPeake**  
*Rosenblatt Securities Inc., Research Division*

Okay. It's not easy stuff.

**Operator**

Our next question or comment comes from the line of Richard Shannon from Craig-Hallum Capital Group. I'm unable to promote his line. We will not be able to pull up Mr. Shannon's line. At this time, I would like to turn the conference over to Mr. Subodh Kulkarni for any closing remarks.

**Subodh Kulkarni**  
*CEO, President & Director*

Thank you for your interest in Rigetti earnings call and the thoughtful questions and discussions today. We are encouraged by the progress we are making on our technology roadmap, the growing engagement we are seeing from customers across cloud and on-premises channels and the strength of our balance sheet to support disciplined execution. We remain focused on delivering against the milestones we have laid out and on building a business that can create durable long-term value as quantum computing matures. On behalf of the entire Rigetti team, thank you for your continued interest and support, and we look forward to updating you on our progress next quarter.

**Operator**

Ladies and gentlemen, thank you for participating in today's conference. This concludes the program. You may now disconnect. Everyone, have a wonderful day. Speakers, standby.