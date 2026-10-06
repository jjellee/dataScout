---
ticker: PENG
company: "Penguin Solutions, Inc."
title: "Penguin Solutions, Inc. Rosenblatt's 6th Annual Technology Summit: The Age of AI (Part II) Earnings Call Transcript"
published: 2026-08-17
quarter: "FY 2026"
event_id: 731740
source: stockanalysis
source_url: https://stockanalysis.com/stocks/peng/transcripts/731740-rosenblatt-s-6th-annual-technology-summit-the-age-of-ai-part-ii/
audio_url: https://files.quartr.com/audio-files/cab7aa0137e7421ca262502b705ea1e2-2026-08-17-20-06-20.mpeg?ref=U0E=
---

# Penguin Solutions, Inc. — Rosenblatt's 6th Annual Technology Summit: The Age of AI (Part II) (2026-08-17)

## 요약(stockanalysis 자동 생성)

### Company transformation and AI platform evolution

- Transitioned from hardware-centric HPC provider to full-stack AI factory platform, leveraging 25 years of expertise in scalable compute and memory solutions.
- Inducted into the Space Technology Hall of Fame for early supercomputing innovations, now applying those learnings to enterprise AI infrastructure.
- Focuses on customer-centric, workload-first solutions, integrating best-in-class technologies from partners like NVIDIA and AMD.
- Accumulated over four billion GPU cluster runtime hours, feeding operational insights into proprietary software.
- Emphasizes open, flexible architectures tailored to customer needs, including support for diverse silicon and custom deployments.


### Product differentiation and technology

- ClusterWareAI software distills years of operational data, enabling predictive maintenance and automated remediation for large AI clusters.
- OriginAI provides validated blueprints for rapid, cost-transparent AI infrastructure deployment, supporting both NVIDIA and AMD architectures.
- MemoryAI platform delivers high-performance, low-latency memory appliances for AI inference, using DDR5 and CXL expansion to optimize token processing.
- End-to-end services (design, build, deploy, manage) wrap around hardware and software, ensuring seamless customer experience and ongoing support.
- Differentiation increasingly resides in software and services as hardware becomes more commoditized, with integration value shifting up the stack.


### Market strategy and customer segments

- Serves enterprises, sovereign AI, and Neo Cloud customers, each with distinct buying criteria and deployment timelines.
- Neo Clouds move quickly at scale, sovereign projects require more customization and compliance, while enterprises focus on secure, private AI deployments.
- Enterprise adoption is shifting from experimentation to production, with growing demand for application-level support and managed services.
- Land-and-expand model drives growth, with significant expansion from initial deployments as customers scale use cases.
- Partnerships with Dell, CDW, and SK Telecom extend reach, with Penguin providing software, operational expertise, and integration above standard hardware.


### Competitive landscape and future outlook

- ClusterWareAI is licensed via subscription, offering deployment, monitoring, and AI-driven remediation, differentiating from open-source and vendor-specific tools.
- Customers increasingly choose on-prem AI infrastructure for security, data proximity, and cost predictability as workloads scale.
- Penguin aims to move further up the stack, focusing on software, orchestration, and application development to deliver greater value.
- Ongoing learning from deployments continuously enhances product capabilities and customer outcomes.
- Growth will be tracked by software/services adoption, customer base expansion, and deeper integration into customer AI workflows.

---

## 전문

**Sajal Dogra**  
*Semiconductor Analyst / Rosenblatt Securities*

Good afternoon, and welcome to the Rosenblatt Securities Sixth Annual Age of AI Scaling Tech Conference. My name is Sajal Dogra. I am one of the semiconductor analysts here at Rosenblatt. It is my pleasure to introduce Mark Adams, Penguin Solutions' Senior Vice President of Global Marketing. Mark has extensive leadership experience in the design and implementation of complex enterprise infrastructure for cloud computing, AI, big data storage, and high-performance computing. We have a buy rating on Penguin with an $80 12-month price target. Penguin is a leading provider of MemoryAI and AI computing solutions for enterprise sovereign AI and Neo Cloud. Penguin is built on 25 years of engineering expertise, bringing together differentiated software, advanced MemoryAI, ComputeAI systems, and industry-leading partner solutions in a full-stack AI factory platform. I will kick off the fireside chat with a few questions, and we will take questions from the audience. To ask a question, click on the quote bubble graphic on the top right-hand corner, and I will read the question to Mark. Please keep in mind that Penguin is in their earnings quiet period. The purpose of this chat is to understand Penguin's market strategy. Mark, thank you for joining us again this year.

**Mark Seamans**  
*SVP of Global Marketing / Penguin Solutions*

Hey, it is great to be here, Sajal. Thanks so much for having me. Looking forward to the conversation.

**Sajal Dogra**  
*Semiconductor Analyst / Rosenblatt Securities*

Likewise. Mark, back when I used to design chips at Qualcomm in San Diego where you live, Beowulf cluster was this first high-performance compute engineering marvel at NASA that Penguin then commercialized through ClusterWareAI, taking compute and using software to make it work like a scalable, high-performance system. With that historical context, Penguin has undergone a fairly dramatic transformation. The company is now transitioning into an AI factory platform. Can you discuss the steps with us that has brought Penguin to this stage?

**Mark Seamans**  
*SVP of Global Marketing / Penguin Solutions*

Sure. It's a great question, and it's interesting you mentioned NASA and the heritage of where this goes back. Penguin actually was inducted just a couple of years ago into the Space Technology Hall of Fame, going back all the way to that work with NASA. The origins of this were really around as supercomputing was evolving, was this idea of taking scalable nodes and then being able to assemble those nodes into very high-performance compute clusters that could take large problems, break them down into smaller problems, work on them in scalable parallel ways, and then to put the results back together. What's interesting is that while Penguin has gone through a pretty significant transformation, primarily from being a more hardware and maybe research organization-centric, high-performance computing solution provider to where we are today, operating at the intersection of really large memory solutions, which we'll talk about a little bit later, and AI infrastructure. The core infrastructure and the core architectural model that really underlies what's going on today in this explosion of AI really is actually quite consistent and evolved from that original model. What we bring to this is this 25 years of heritage and skill set that we've been honing for this, and that we have been now in the right place at the right time, where the thing we've been training for for over two decades has evolved as being this skill set that almost every enterprise now is looking to take advantage of.

**Sajal Dogra**  
*Semiconductor Analyst / Rosenblatt Securities*

That's awesome. If I try to understand Penguin versus competitors, there's these open agnostic end-to-end solutions versus proprietary vendor lock systems. Penguin just became an NVIDIA AI factory partner. How does that work, and will ClusterWareAI and OriginAI support AMD racks at a similar feature level, or does it need changes in software and tooling?

**Mark Seamans**  
*SVP of Global Marketing / Penguin Solutions*

That's another good question. I think philosophically, one of the things Penguin's always done, has tried to operate with a mindset of living with a foot in the world of our customer, and really thinking about the workload first, the customer first, and then really looking at the palette of technologies that are available, and trying to think about how can we best pick from everything that's out there to assemble for the customer's objective, the best possible solution. Rather than just no matter what problem someone shows up with, taking the same architecture and the same solution and jamming it down, we like to think that we take a much more thoughtful approach of combining the best of the best. Now, with that much said, NVIDIA's done tremendous work. As you mentioned, we actually for some time have been a DGX-ready managed services partner, which means that we've demonstrated the top level of experience in managing and operationalizing large AI clusters. They announced a new program that is an AI factory specialized partner, specific to producing these large AI factories, and we were an initial inductee into that. We've got tremendous depth specific to NVIDIA clusters. In fact, we manage these alongside our customers and have accumulated over four billion hours of runtime experience of managing GPU clusters at scale. With that much said, we're also completely open. Just as you know in our heritage, we were delivering both Intel-based CPU architectures and AMD-based CPU architectures. In today's world, where there's an explosion of silicon options coming available for customers, we're equally happy to bring to a customer that needs it an NVIDIA cluster, an AMD cluster, or other clusters. One example that I think we talked about in a recent earnings call that we did was the delivery of a cluster to Sandia National Laboratories, a system called Spectra. Which was based on a Kneron silicon advanced accelerator, which was very nicely mapped to the workload that the customer wanted to run. That's another example, even beyond NVIDIA or AMD, where there's other silicon becoming available. I think agnostic is maybe too generic a word. I think we're opinionated in many regards, but we think that we're opinionated as an advocate for the customer. We'll look at what they're trying to do and recommend what we think would work best.

**Sajal Dogra**  
*Semiconductor Analyst / Rosenblatt Securities*

You mentioned these billions of GPU runtime experience in massive clusters. How does that inform the value in ClusterWareAI that can easily be recreated by a competitor? Is it a learning flywheel, or is it just purely a moat based on all the engineering knowledge and best practices you've had?

**Mark Seamans**  
*SVP of Global Marketing / Penguin Solutions*

Yeah, it's been an interesting journey as we've gone along. As we implemented these large GPU systems really starting in 2016, 2017, before really this whole AI mania that's gripped the world had even fully crystallized. We were outputting these systems together using that HPC architecture, but now with the incorporation of GPUs. As you start to do that at that scale, you start to learn not just about how these systems run, but you start to learn about how they fail. Ideally, you start to learn about how they start to signal the potential for failures of individual components before those components actually fail. What we've really done is taken the learning that as each of those failures would occur, we would go back after the fact and say, "Was there anything in the logs we could have seen that would have given us a clue that that GPU was going to fail or that that network adapter was going to fail?" Let's continue to compile all of that learning. Then really what's happened now with our core software platform called ClusterWareAI that we use to deploy and manage these systems, is that we've distilled all of that learning, just as if you had a top engineer who was your best data center engineer who just had a knack for keeping your systems running well. We've tried to take that learning and using analytics techniques, distill all that learning into the software. So now while we do have top services engineers who work in the data center alongside our customers managing these systems, you've got this silent assistant that's running with ClusterWareAI that's doing things that no person could do, and that it can watch millions of data points at every minute of the day as a cluster runs and being able to start to spot, you know what? There's going to be a network issue over there. Why don't we gracefully take that node out of the cluster before it fails and maybe causes disruption to a user job and put it on the side where a technician can repair that and gracefully put it back in. The end result of this whole thing we're talking about here is higher operational throughput for our customers, fewer disruptions, more uptime as they run these very large systems. By the way, we're continuing to learn every day. I don't want to even make it sound like we're done. As new GPUs become available, new system elements become available, we're constantly taking that learning and feeding it back into the engine.

**Sajal Dogra**  
*Semiconductor Analyst / Rosenblatt Securities*

Got it. I just want to take a deeper step into understanding your key product offerings. What is OriginAI platform and what does it add around ClusterWareAI? What problem is it solving for in deploying AI versus, say, buying racks from Dell?

**Mark Seamans**  
*SVP of Global Marketing / Penguin Solutions*

It's a great question. Why don't I do this? I'm going to bring up a graphic that maybe would be helpful as a backdrop to answer this question. You should be able to see that, and we'll just leave this up. As you go back to where we started, Penguin ourselves have made a huge transformation over the last few years from being someone who was more of a hardware provider and HPC system provider to an organization that's all in on delivering these full-stack AI factory platform solutions. If you look at the picture on the left, I'll talk around some of the different pieces that come together to produce these solutions, and maybe I'll do them a little bit out of order. If you look at the right edge, where it says OriginAI, as we engage with customers who are looking to solve either an AI training or an AI inference or agentic AI inference solution, one of the things that we've done is taken all that learning, and we've distilled it down into repeatable architectures that are this proven starting point, both from a technological perspective and also from a system sizing and quoting perspective. Because one of the questions a lot of times customers have, especially customers who are running primarily in the cloud today, is going to be, "If I were to bring this solution in-house, what would it take? What would it look like? And roughly how much would it cost for me to get going?" It doesn't have to be perfect, but everyone wants to get that idea. OriginAI is this set of validated blueprints that we've developed. In fact, there's OriginAI blueprints for NVIDIA training architectures, for AMD-based training architectures, and inference-based solutions. We would start with an OriginAI architecture. If you look on the left edge, ClusterWareAI, which we were talking about, that's a software platform completely developed from the ground up by Penguin. In fact, it's not just been developed, but it's been redeveloped several times over Penguin's 25+ year history, going all the way back to that NASA environment you started with. It's a highly tuned environment today, itself incorporating AI that you can go in and you can ask questions about your cluster to the ClusterWareAI software. It does three things. It transforms hardware into a high-performing cluster. It's the first thing it does very efficiently. Once you have a cluster, it does the 24/7 monitoring I talked about of looking at those million data points. The third piece is what's called an auto remediation system, which is that distillation of knowledge that when something shows up that needs attention, it's ClusterWareAI that can automate the repair of that in many cases. The other pieces are things people would likely be familiar with beyond the hardware stack. We do, though, from a hardware stack, you see ComputeAI. That's a set of curated server offerings, but these are offerings that are completely compliant and compatible with the NVIDIA reference architectures, with AMD-based servers, and then with agentic CPU-based servers that might incorporate Intel or AMD-based CPUs. ComputeAI is standard products that we offer. Beyond us offering our own ComputeAI, you see a level below. We also offer Compute from Dell. We offer native NVIDIA DGX servers, and so we have our own tuned offerings, but we also, for customers that are used to working with industry dominant providers, we can embrace those architectures and deliver. From a differentiation perspective, the other two pieces that I think are pretty highly differentiated for Penguin are the thing labeled number two, MemoryAI. We can touch on this a little bit more deeply later, but essentially, agentic AI workloads and AI inference workloads in general are highly dependent on large amounts of memory. Because of Penguin's deep expertise in the area of scalable memory, we've actually produced, you heard me mention this term operating at the intersection. MemoryAI is a platform that we offer. It's an integrated appliance for a piece of the inference process called a KV cache server. What that means is it allows you to, as you're doing AI workloads, once you've computed tokens that are part of an answer that you've been calculating or working on, it can store those tokens. So if you see a similar question come along in the future, you don't need to go to the GPU to redo that workload. You can go to our Token Factory or our MemoryAI server environment and just rapidly, without compute requirements, resurface that. It's highly efficient. It makes compute much faster, and it's a piece of our architecture that's sort of a unique to Penguin offering. The piece at the very bottom is end-to-end services. It's this idea that we work with customers starting at the design to the actual construction of the AI solution, to the deployment of that solution, and the management. You'll hear us use that term if you work with Penguin called DBDM, which means design, build, deploy, manage, and it's this whole life cycle of how we work. All of those things together, from our perspective, wrap around the standard mechanical, electrical, plumbing, data center work, and we embrace all of that. But the pieces shown in yellow really are the core components of what we bring as a differentiator to market.

**Sajal Dogra**  
*Semiconductor Analyst / Rosenblatt Securities*

As a follow-up on the MemoryAI piece, what problem does CXL attached memory solve for in inference TCO? Can you help us understand what's the competitive landscape here?

**Mark Seamans**  
*SVP of Global Marketing / Penguin Solutions*

It's a great point. I'll put one more graphic up. This is basically what a MemoryAI server looks like. It takes these Penguin-developed CXL memory expansion cards that are 1 TB each, and it takes a whole set of these and places them into a server appliance such that this box that we're looking at here adds 11 TB of ultra-high performance memory-based storage that can store these tokens and deliver them over a low latency network to a whole host of inference servers that are running your workloads. Within this area of KV caching, there are approaches people take using much, much slower, 100 times slower, flash-based storage. Because of our experience with memory and because of our awareness of latency as being a big issue for this token-type workloads, our differentiation for what we produce here is that our solution today is 100% based on the fastest DDR5 memory to give, again, that lowest Time to First Token and then offloading a lot of work that would normally be going back to GPUs that could be done using pre-computed tokens.

**Sajal Dogra**  
*Semiconductor Analyst / Rosenblatt Securities*

Understood. I wanted to understand, NVIDIA and now AMD are moving to rack scale products. Does this further commoditize hardware, and how does the integration value migrate from hardware to software and services? How does that impact Penguin? I guess what I'm trying to ask is, five years from now, does Penguin's differentiation reside in hardware, or is it software and services?

**Mark Seamans**  
*SVP of Global Marketing / Penguin Solutions*

That's a great question. I smile a little bit because as we operate in parallel with NVIDIA, I think we've all heard Jensen Huang present at GTC and other more visionary events where we've seen the world go from GPU adding cards to then the DGX, which then combined eight of these GPUs onto a physical board that was, not getting too technical, but SXM high speed connected, and then taking multiple of those and starting now to integrate them, as you just mentioned, into full rack scale solutions, to where now racks become the new server, right? Becoming larger and larger. As we see that expansion occur, in any case, it seems to be increasing the value and the opportunity for Penguin because of the specialization of this equipment, the unfamiliarity of a lot of these technologies. Again, things like rack scale GPU, highly sensitive liquid cooling systems, which are going to be new for a lot of customers as they work in the data center. Highly tuned, 800 gigabit InfiniBand networking, right? Which is also, depending on your IT team, unfamiliar territory. This idea of taking all of this technology, it is just happening at a different scale. It is not that the value of what customers can use from a services and integration perspective goes down. Now, with that much said, it is going to be a combination, I think, of hardware and software. Interestingly, if we go back to our high-performance computing heritage, thinking back to the workloads our customers at Penguin have always run, have been things like Computational Fluid Dynamics for simulating airflow, for example, over a car or an airplane wing, or weather forecasting or climate simulation or what is called seismic processing for oil and gas. The nature of each one of those problems was that what you really needed to do to help a customer solve that was to understand the workload and then to bring at it an architecture which was tuned to run that. As we get into agentic AI, we are seeing exactly the same thing because you have customers where you have got the agent part of the workload, which is likely going to run on CPU-based infrastructure, which is doing something. Depending on your workload, if it is insurance claims processing, if it is fraud detection, if it is drug discovery, the nature of what the agents are doing is going to require probably wildly different amounts of CPU combined with variable amounts of GPU, different network latency, difference importance of backend storage. I think, the value of Penguin is, again, to be able to work side by side with a customer, understand their workload, and then to be able to create a tailored configuration that is going to be just right, where you did not overbuy and you also did not introduce a bottleneck. Again, I think it is that specialization. Penguin does not do everything, but the things we do in this intersection of AI and memory at this agentic workload arena, I think we do as well or better than most of those that are out there.

**Sajal Dogra**  
*Semiconductor Analyst / Rosenblatt Securities*

Great. Switching gears to market trends, I think you increasingly describe three major customers, enterprises, sovereign AI, and Neo Clouds. How different are the buying criteria, the sales cycles across these groups, and where are you seeing the fastest conversion from interest or pilots into production deployments?

**Mark Seamans**  
*SVP of Global Marketing / Penguin Solutions*

Wow, that is a really good question. First of all, you mentioned three areas, enterprise customers, Neo Cloud, and sovereign AI. By the way, some of those, the Neo Cloud and sovereign, there is overlap there. For people that are on the session here, when we are talking about sovereign, typically we are talking about something running in a completely private isolated way. That could be if you think about national sovereign, a good example is the SK Telecom Haein cluster that Penguin designed and deployed and manages till today. We have people in the data center as we do this session right now managing that cluster in Korea. One of the requirements, that is a sovereign cluster, it is also a Neo Cloud servicing demand for a Neo Cloud user base. The requirement there was that all of the network traffic needs to occur within the bounds of South Korea. We are also seeing this requirement, interestingly, for enterprise sovereign. You have got enterprise customers who are saying, "We want to deploy private AI infrastructure, which needs to be totally within our boundaries of our network. It is going to be for secure internal use cases." There is a blending of these. With that much said, the characteristics of Neo Clouds are scale, right? It is most of the Neo Clouds, they understand deeply, in most cases, or many cases, what they want. Although we do work regularly with Neo Clouds who have access to a data center, have access to power, have access to a customer, and who really need help with the technology part of it. The good news in those cases is they can typically move quickly, and what they are going to do is going to be at some scale. Because they are looking to put capacity online. Sovereign tends to be proving it out, but also it is more hand-holding and more where our design build, deploy, manage, and through a series of workshops we typically run comes into play. With enterprises, what is interesting is we can clearly see now through the engagement that we have with enterprises that AI is, particularly agentic AI and AI inference,

**Sajal Dogra**  
*Semiconductor Analyst / Rosenblatt Securities*

Yeah.

**Mark Seamans**  
*SVP of Global Marketing / Penguin Solutions*

Is moving from this experimentation to where these companies are really ready to put this into production. Differently than maybe what is going on in the Neo Clouds, they are not training models as much as they are looking to use these trained models from sources like either Hugging Face or using Nemotron style models that can be acquired from like NVIDIA as part of their AI enterprise suite. But they are looking for help in actually the application portion of it. Not just building infrastructure, but they are looking for help and saying, "Can you help me take advantage for the business problem I am trying to solve, helping me with software infrastructure as well as the hardware?" The scale initially may not be as big, but what we do see is it will be a flywheel where it is going to be use case number one comes online, and then there is going to be 50 use cases behind that that are going to be deployed over time, and that we think will drive the demand for more infrastructure. So each one with its own kind of characteristics and timelines, but each one certainly with a CAGR associated with it.

**Sajal Dogra**  
*Semiconductor Analyst / Rosenblatt Securities*

I just wanted to double-click a little bit on the SK Telecom piece since we have received a lot of questions on it.

**Mark Seamans**  
*SVP of Global Marketing / Penguin Solutions*

Sure.

**Sajal Dogra**  
*Semiconductor Analyst / Rosenblatt Securities*

Now, it is somewhat unique because simultaneously they are a strategic investor, they are a customer, and they are a technology partner. Following Haein, how should investors think about SK, both from memory supply and AI factory deployments? Was that a bespoke Korean deployment, or does it establish a repeatable blueprint that Penguin can then take into other sovereign AI projects? Do you think SK Telecom has huge ambitions of being this big AI supplier within APAC? Do you see Penguin benefiting from both within Korea and broadly across APAC through its partnership with SK Telecom?

**Mark Seamans**  
*SVP of Global Marketing / Penguin Solutions*

Sure. As you mentioned, SK Telecom is an investor in Penguin Solutions. But the collaborations that we have had really transcends that investment and has really just come about through pure business collaboration and having a synergistic ability to go to market together. The project that we did, the Haein cluster, it is award-winning now. It has won numerous awards for its rapid deployment time. Its uptime that it has been able to deliver. When I talked earlier about the ClusterWare, because that is a ClusterWare-managed cluster that is operated by our Penguin Solutions services team and services the needs of the SK Telecom customer. So that customer is in full deployment. It is actually consumed on a 100% sort of a sovereign Neo Cloud basis. And there are tremendous opportunities for us to work with SK and SKT, SK Telecom, on other opportunities. People that are attending this session can search and can see that SK Telecom has announced intents to expand their business meaningfully over the overall APAC region specific to AI deployments. You also mentioned SK hynix, another division kind of operating independently of SK Telecom. From our memory side of the business, SK hynix is a company with whom Penguin's had a long-term relationship and partnership. As they look to get more into the AI space, it's an area as well where we have an opportunity because of the work we're doing at that intersection of AI infrastructure and memory to participate with them, and I look for areas where we could offer value as well.

**Sajal Dogra**  
*Semiconductor Analyst / Rosenblatt Securities*

Got it. Thank you for that. I just want to, I guess since we are on this topic of partnerships, maybe talk about Dell, actually. Dell has its own AI factory positioning. It sells the underlying hardware. Where does Penguin contribute that Dell doesn't want to or can? You have offerings, MemoryAI, KV cache, we went through that, ClusterWareAI, sitting alongside Dell. Is Penguin effectively becoming the software and operational layer above standardized Dell hardware?

**Mark Seamans**  
*SVP of Global Marketing / Penguin Solutions*

Yeah. The partnership with Dell has been tremendous, and it's evolved pretty naturally. I'll step back maybe just one second to talk about partnerships in general because we've got a tremendous partnership with Dell, a great partnership with CDW, partnership with entities even like WWT that we work with. As we engage with each of these partners, the focus, kind of as I talked about our customers creating, living with the world in the customer's world to try to create a win for them. Partners, it's the same philosophy. We start the relationship looking for where that win is, looking for where their current strengths are and where Penguin can help. Because if you've got collisions or dissonance in a partnership model where they're feeling like, "Oh, I think you're going to try to come in and do something detrimental as a sales team," to me, then it's hard to get lift off. We started with a model that understood where can Penguin add value to Dell. It's clearly, as you mentioned, in areas around the compute that they provide, the networking that they provide, the storage that they provide, which are all top-tier capabilities, to the relationships they've had with customers for decades. So we can come in and say, but we can offer ClusterWareAI to be able to deliver high performance clusters. We can offer the MemoryAI platform that I talked about when it's an inference use case and where people are looking for those superior token economics. We can offer the end-to-end services, not just to build a system and stand it up for a customer, but in many cases, people are looking for that private cloud experience where somebody will come in and do the in the data center break fix, the software management, guaranteeing the uptime, and adhering to an SLA for a customer. That is a big piece of our business from the services side. So it is really playing in areas where we can add value for Dell customers and then also the ability to continue the motion with selling the Dell equipment. We were actually named, just this summer, a Dell AI Partner of the Year for the work that we have been doing and the growth that we have been seeing in the customers that we have been deploying with.

**Sajal Dogra**  
*Semiconductor Analyst / Rosenblatt Securities*

Now, I know you have mentioned CDW, but that is a very different partnership that really gives you a lot of distribution and customer reach. How does that change your channel motion and go to market?

**Mark Seamans**  
*SVP of Global Marketing / Penguin Solutions*

Yeah. So again, you take each partnership and look for how do we add value. In the case of CDW, as you mentioned, it is an organization with tremendous customer reach, tremendous established traction with customers as a supplier of everything under the sun from a top-tier basis. The partnership with Penguin is, in that case, more where we can bring that full expertise that I showed you on the diagram earlier to be able to work with a customer who says, "I am looking to do an AI solution, but I am looking for someone to come in, help me identify the components." Then in those cases, the other thing that is nice is that Penguin can leverage the in-place supply chain relationships that CDW has with those enterprises, so that it becomes a single source of the customer being able to procure products across the board, but for Penguin then to step in and become a fulfillment arm for putting the whole thing together, and again, for the customers that want it to be able to do that long-term management. Slightly different motion, but one as well that has been very valuable for us in terms of customer access.

**Sajal Dogra**  
*Semiconductor Analyst / Rosenblatt Securities*

I guess we can maybe go a little deeper on the software offering. Is this licensed or is it a hardware attached? If it is a hardware attached, does it increase as deployments get complex? Can you help me understand the competitive landscape in software for the market versus NVIDIA Stack, Dell's own tooling? You have Slurm and Kubernetes. Maybe just talk about the land and expand model. What does that look like in practice? What does a customer buy from Penguin initially, and what gets added 12 months, 24 months later, ComputeAI, ClusterWareAI, managed services, et cetera?

**Mark Seamans**  
*SVP of Global Marketing / Penguin Solutions*

Kind of whole bundle of-

**Sajal Dogra**  
*Semiconductor Analyst / Rosenblatt Securities*

I threw a lot at you. I know.

**Mark Seamans**  
*SVP of Global Marketing / Penguin Solutions*

Questions there. Let's unpack it, and let's talk through that. From a software perspective, the software is licensed on a subscription basis, so that you can keep, A, you keep the cost tied to the value that the customer is obtaining over time. As they're getting value from the software, they're paying for it, for the capabilities that it delivers. Typically, it also can run alongside the agreements that we would do with a customer to deliver services. Like those managed services would kind of coincide, and in those cases, it's a combination of both our Penguin Services team and members of the customer's IT staff that can leverage that platform to be able to be squeezing the most value out of the system that they can. Competitively, the way I try to think about ClusterWareAI is I mentioned earlier that it does the three things. It does the deployment, it does the ongoing monitoring and management, and then it does the AI-driven automatic remediation and repair of issues. What we typically see is that other platforms, maybe it will target one of those things, but not necessarily all three in the kind of holistic manner that we target. You might leverage an open source platform that says, "Oh, great, you can give me some instructions, and I can set up your network and be able to set up a base cluster." But it'll kind of stop there. It won't tune it. It won't squeeze the most performance out of it. It just kind of gets you to step one in a 50-step journey, right? I think the work that we do to constantly be adding the value back, and also because we're not producing just a standalone product, what we deliver is because of we're living these deployments ourselves, and so we're building in constantly the experience that we're seeing from being in the market. In terms of the way the deployments go, it's actually interesting in that it's not that dissimilar what we're seeing in this world of AI from sort of Penguin's history over time. Maybe I'll just mention culturally, for customers that work with Penguin, and in my history at Penguin, a role that I had early on was actually leading our services team, including our professional services, our managed services, and myself getting very involved in a lot of our early days large AI rollouts. I had a customer say to me one time, "You know why I go with Penguin? I go with Penguin because I know that you won't let me fail." I always thought that that was. It stuck with me, I guess, because that's a real statement for someone to say, "I trust you that you're going to operate with my best interest. I'm not just your customer. We're partnering on this thing." I think because of that, what we tend to do is to get in and deliver solutions to customers, and then we're there for them, and we're listening as new solutions come around or opportunities for expansion. We're in those conversations, and we have our shot to be able to earn that business. This idea of land and expand is in this era of AI near and dear to our heart. I think our CEO, Kash Shaikh, I think on our most recent earnings calls, and people can check me on this, but we've began to talk about that more openly on the earnings calls to not just talk about kind of a 12-month look back and about new logos. But for those new logos that we have onboarded over that 12-month period, what percentage of those have actually come back to us and said, "I want to do an expansion of some size, not just I needed to buy a little extra cables, but I wanted to come back to you and expand meaningfully the system that we put in place." I think the numbers are pretty significant. That's a trend that we track and that we'll continue to, I think, talk about, but also that's really important to how we operate each day.

**Sajal Dogra**  
*Semiconductor Analyst / Rosenblatt Securities*

As we think about this is great, actually. As we think about enterprises adopting AI, where do you think is the bottleneck right now? Is it use case? Is it data readiness? Is it some GPU, skill level? Or I guess part of that is why do this at all? Why not rent capacity from CoreWeave or Nebius? How does owning versus renting work in this market?

**Mark Seamans**  
*SVP of Global Marketing / Penguin Solutions*

Yeah. That's a great question, and sort of the answer a little bit is, yes, I have customers I'm working with at every phase in this that are working through their learning experience. Because for a lot of people, they're just really getting into this at scale and really looking to say, "How do I take on agentic AI?" One of the things is agentic AI is AI doing work versus a chatbot, right? Chatbots are neat in that you can ask a question, it gives you an answer. But the holy grail for us as enterprise is going to be deploying these systems that actually have agency and are doing work 24/7 on our behalf. Customers make a decision to say, "We want to do AI." They then go through ideation to figure out what workloads would give us the biggest bang for the buck. Then they typically, as you mentioned, need to find the data, and there's work to be done, right, to put that together, and even to put together the agent flow itself of how is the combination. It's not just AI at this point. It might be tapping into your ERP system and tapping into your customer database and tapping into a healthcare information system if you were in healthcare or insurance, right? All of those pieces become part of this. But the rationale for why does someone want to bring that on-prem increasingly is for ownership of that very sensitive and secure environment, right? The systems that you're going to be tapping into many times are the lifeblood of your enterprise. And so having a secure deployment that's sitting right up next to those environments that you're running in production kind of gives you the most power and the most flexibility, and it also gives you the most cost predictability in that from a token perspective, it's almost. I use the analogy sometimes, if I knew that I needed to drive every day as a key part of my job, well, going and renting a car from a rental car agency wouldn't be the best economic way to do it. I'd probably say, "You know what? I should buy a car, because over time, that's going to be far cheaper than paying for a car rental or paying by the mile. I should be owning a car because I'm going to be doing this on a deep basis forever." I think that's what's happening now with this AI infrastructure, is people realizing experimentation was great to do a pay as I go, but now that I know I'm going to be doing this at scale forever, I should really be thinking about this becoming a core enterprise asset.

**Sajal Dogra**  
*Semiconductor Analyst / Rosenblatt Securities*

Got it. Mark, if we sit down again years from now and Penguin's AI factory platform strategy has played out, what do you think looks different? What do you think investors are currently underestimating the most? How should we track milestones over the next 12 months, 24 months? Is it becoming a much bigger software services business? Is it more GPU adoption? Is it more ClusterWareAI MemoryAI? Is it a bigger customer base? Help us understand the journey you've been on.

**Mark Seamans**  
*SVP of Global Marketing / Penguin Solutions*

Yeah. I guess I'll summarize it in a couple of words, that I think you're going to see us be customer-led. Because we're going to be customer-led, I think what you're going to naturally see is for us to increasingly become interested in the above the infrastructure level of things, which means the software and the services that operate up the stack, right up at Kubernetes and up at AI orchestration and up at helping customers develop those purpose-built applications for the workloads they're going to run. I think because we're just going to naturally want to get pulled up in that direction to provide them the maximum amount of help. It won't be in any way an abandonment. The infrastructure is fundamental to this whole thing. But the more insight that we get as we move up, I think it will be greater value that we are going to deliver, and it will continue to fuel our growth.

**Sajal Dogra**  
*Semiconductor Analyst / Rosenblatt Securities*

That is awesome. Well, you know what? We are out of time, actually. This has been great. I really appreciate your time.

**Mark Seamans**  
*SVP of Global Marketing / Penguin Solutions*

Oh, no, this has been a great conversation. Maybe we will connect in person when you are in San Diego sometime.

**Sajal Dogra**  
*Semiconductor Analyst / Rosenblatt Securities*

Of course. I miss San Diego. Call me anytime. Yeah.

**Mark Seamans**  
*SVP of Global Marketing / Penguin Solutions*

Okay, great. Thanks for the time today. Appreciate it.

**Sajal Dogra**  
*Semiconductor Analyst / Rosenblatt Securities*

Take care. Bye.
