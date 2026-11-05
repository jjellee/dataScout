---
ticker: LSCC
company: "Lattice Semiconductor Corporation"
title: "Lattice Semiconductor Corporation The Six Five Summit: AI Unleashed 2026 Earnings Call Transcript"
published: 2026-08-27
quarter: "FY 2026"
event_id: 738857
source: stockanalysis
source_url: https://stockanalysis.com/stocks/lscc/transcripts/738857-the-six-five-summit-ai-unleashed-2026/
audio_url: https://files.quartr.com/audio-files/fbdec0549aeb9e5448ac2d23aa7d50f0-2026-08-27-19-18-53.mpeg?ref=U0E=
---

# Lattice Semiconductor Corporation — The Six Five Summit: AI Unleashed 2026 (2026-08-27)

## 요약(stockanalysis 자동 생성)

### Strategic rationale and integration

- Acquisition brings together complementary strengths in low-power FPGAs and foundational firmware for AI data center infrastructure.
- Combined solutions aim to accelerate customer time to market by offering pre-validated, turnkey management and control platforms.
- Both entities emphasize open system neutrality and broad ecosystem support, operating close to hardware for real-time, low-latency control.
- Integration targets reduced customer integration costs and enables focus on IP development.
- Commitment to open source and community-driven development, with aspirations to be the 'Red Hat of firmware.'


### Industry trends and market shifts

- AI is driving massive changes in infrastructure, with a shift from training to inference workloads and rapid adoption of new architectures.
- Data center complexity is increasing, with up to 1,200 sensors per server and widespread use of FPGAs for secure management and control.
- Security requirements are evolving, with post-quantum cryptography solutions being implemented ahead of regulatory mandates.
- Disaggregation of compute, power, cooling, network, and storage racks is a key trend, requiring advanced management solutions.
- Future infrastructure will require self-diagnostic, self-healing, and autonomous management capabilities, especially as data centers expand to new environments like space.


### Customer benefits and solution impact

- Modular, open-source firmware supports heterogeneous architectures (x86, Arm, RISC-V) and all major BMCs and companion chips.
- Customers gain faster time to market, lower integration costs, and simplified management of complex, heterogeneous environments.
- Joint solutions enable secure, real-time control across both data center and physical AI applications, including industrial robotics and autonomous vehicles.
- Rack-wide and data center-wide management capabilities are being developed to address growing scale and complexity.
- Predictive maintenance and AI-driven self-healing infrastructure are positioned as future differentiators.


### Financial outlook and growth targets

- Near-term focus is on accelerating growth, adding resources, and delivering integrated solutions.
- Current revenue run rate is $1 billion, with expectations to exit the year at $1.2 billion.
- Aspirational goal to reach $3 billion run rate by 2030, requiring a 25% annual growth rate.
- Significant growth opportunity highlighted by doubling revenue from $520 million in 2025 to current levels.

---

## 전문

**Moderator**

Hey, everybody. Welcome to The Six Five Summit 2026. The theme of this year's show, we're seven years in here, is AI Unleashed. As you've seen, there's a tremendous amount of unleashing of benefits downstream, but also some challenges related to security, and control, and doing all this silicon through firmware. We're joined today by Ford Tamer, CEO of Lattice, and Sanjoy Maity, Senior Vice President of the AMI Business Unit Leader of Lattice. Sanjoy, welcome to The Six Five, and Ford, welcome back.

**Ford Tamer**  
*President and CEO / Lattice Semiconductor*

Thank you.

**Sanjoy Maity**  
*SVP of AMI Business Unit Leader / Lattice Semiconductor*

Thank you.

**Moderator**

Yeah. First of all, congratulations on the deal. It was interesting, I got it the first time, having worked at a bunch of systems companies and silicon companies before, but I just wanted to say congratulations on that.

**Ford Tamer**  
*President and CEO / Lattice Semiconductor*

Thank you, Pat.

**Moderator**

So Ford, let's start with you. You and I have talked a ton about Lattice and where the company is headed. Now with AMI coming into the family, into the picture, we've got Sanjoy here as well. But before we get into some of the bigger market shifts, can you give a little bit of context to our viewers on the new acquisition and strategically, what made this a fit?

**Ford Tamer**  
*President and CEO / Lattice Semiconductor*

Excellent, Pat. Thank you. Thanks again for the opportunity to be at your Six Five Summit.

**Moderator**

Thank you.

**Ford Tamer**  
*President and CEO / Lattice Semiconductor*

Good morning or good evening to your Six Five audience. Sanjoy and I will maybe ping-pong and do this together. We are very excited about this session. Let me start with a quick overview of Lattice and AMI for your audience. I will do Lattice, and Sanjoy will do AMI. As some of you know, and some of you may be new to our story, Lattice is the low-power programmable companionship for data center AI and physical AI. Our small and mid-range FPGAs provide companion functions for secure management and control and data plane processing. We do things like booting, power sequencing, security management, control, bridging, I/O expansion.

**Moderator**

Yeah

**Ford Tamer**  
*President and CEO / Lattice Semiconductor*

Sensor fusion, and data processing. We do this for partners on the data center AI such as XPUs, GPUs, CPUs, DPUs, microprocessors, microcontrollers, but also networking function and switch and NIC, the board management controllers. On the physical AI, we also do this for all kinds of sensors, from image to LIDAR, to radar, infrared, thermal cameras, and then industrial motion and various other industrial sensors. Sanjoy, can you say a few words about AMI, please?

**Sanjoy Maity**  
*SVP of AMI Business Unit Leader / Lattice Semiconductor*

Sure. Thank you, Ford. AMI is making the foundational firmware for the last 40 years. That uses very essential for the AI data center infrastructure. We make firmware to boot, manage, and secure them. These are very, very essential for the data center. At the same time, the AI data centers are very complex, right? There are so many components, so many infrastructure elements. We also provide holistic view of the data center through a single pane of glass view. From telemetry to monitoring, 24/7 monitoring, error correction, and boosting uptime all together. The data center administrator in a hyperscale data center environment can have a total view of the AI data center. Ford, you can elaborate why we join hands.

**Ford Tamer**  
*President and CEO / Lattice Semiconductor*

Thank you, Sanjoy. We have been dating for six years. We have known each other for that long, Pat, so we service very similar customers on hyperscaler, Neocloud, major server and networking system OEMs, as well as silicon and system partners that we work with very closely. Both of us ascribe to this open system neutrality across the whole ecosystem. We both operate very close to the hardware, so fundamentally, our FPGAs are very close to all the sensors I just discussed. We are the first chip that it goes from the sensor to before they go to digital type of processing. We provide these deterministic, real-time control, low latency, parallel processing capabilities near these sensors and partners. Similarly, AMI is also very low-level firmware, booting, managing, securing all of these hardware. You can see we're very complementary, and our customers now have a tremendous pressure to go shift left and go faster time to market. Together, we believe we're going to provide secure management control solution, a turnkey, and speed up our customers' time to market, and tremendous benefit to them. Do you want to elaborate on that, Sanjoy, before we go back to Pat?

**Sanjoy Maity**  
*SVP of AMI Business Unit Leader / Lattice Semiconductor*

Yes, absolutely. As Ford mentioned, our strategic intent is pre-validated, proven solution, handing over to our customer. So the customer do not spend their time in the integration issues, and they can focus on their IP development and focus on their business. This is a massive, faster to market advantage that we are going to give them. That's the main intent for us to do together.

**Moderator**

Yeah, I've been a fan of the two companies coming together, and it's great to hear it in your own words here. Ford, I want to pull out a little bit, go macro here. AI is obviously changing more than the processors themselves, right? We've seen a lot of massive changes, not just subtle changes, massive changes in power, connectivity, security, how do you control these systems and also the devices themselves? Even how the system itself are managed. Ask you, how is AI changing the overall end-to-end infrastructure that surrounds the compute?

**Ford Tamer**  
*President and CEO / Lattice Semiconductor*

Yeah, no, thank you, Pat. Look, I've been in this industry too long. I've been working for the past 20 years with the hyperscaler server networking OEMs, ODMs, starting at Broadcom on the networking side, where we spearheaded the switch architecture that you've got today, then going to Inphi, creating and growing the optical interconnect. From the boards of Marvell, Teradyne, and Groq before coming to Lattice, I've never seen a massive scale up, out, and build-out like we're having today, so it's just phenomenal. 2025 was the year of training, so we saw a lot of our revenue being driven by GPU and associated infrastructure. In 2026, we've seen a tremendous move to inference, and this has been driving the agentic revolution, has driven tremendous growth in CPU storage and associated networking. We're benefiting from both of these trends. We're witnessing rapid adoption of, as you said, a whole bunch of new architecture on the networking being disaggregated on the scale up, scale out, scale across, on the liquid cooling being widely adopted, on the move to 800 V. But over the past couple of years, the number of sensors in a server has motioned

**Moderator**

Yeah

**Ford Tamer**  
*President and CEO / Lattice Semiconductor*

to 1,200 sensors, controlling all the various aspects, from fan to CDUs to optical interconnect. We sit near each and every one of these sensors. So this has driven the adoption of our low power FPGA from when I joined Lattice two years ago, to tens of FPGAs per rack, to hundreds of FPGAs per rack. This is across millions of server and across tens of thousands of data centers. So you could see providing this secure management control of this very complex infrastructure becomes very key. We work very closely with all the various board management controller, microprocessor, micro-controller in a very complementary way. We provide, again, the deterministic low latency connectivity, high precision parallel processing function very close to the hardware. Let me give you two examples. On the data center AI, security has been our calling card, and we're really excited to the latest executive order mandating protection against crypto quantum with post-quantum cryptography or PQC. We've really done a great job providing this PQC solution ahead of everyone in the space. What's great about FPGA is we stay ahead of the bad actors.

**Moderator**

Yeah

**Ford Tamer**  
*President and CEO / Lattice Semiconductor*

ASICs can't because ASICs are fixed functions, and these algorithms keep changing faster than the ASIC can react. Having the FPGA in the field allows our customers to constantly adapt and constantly change to the fast-moving requirement that security is imposing on server and networking type of infrastructure system. The second example I'll give you on our physical AI, on physical AI, we're seeing all of these system now adopting a brain with AI, and we're providing very important bridging from the analog world on the sensor to the physical world, to the digital world with the AI. A good example is what we do with our key partner, NVIDIA, where we provide a function they call Holoscan, us and their other partners where we take a whole bunch of different sensor, do the sensor fusion preprocessing according to some algorithm they gave us, and feed Thor and Orin on the physical system, the metadata, making Thor and Orin more efficient. We're very excited about this partnership. You could see how our capabilities are really helping AI tremendously across both data center AI and physical AI.

**Moderator**

That was a great explanation. Sanjoy, it was one thing to control and manage an XPU or a single GPU, but now we've gone from that to a tray, to a rack, to pods or fleets, and it's increasingly heterogeneous, right? We've got five to six flavors of XPU at any one moment. CPUs are cool again as well. I'm trying to be funny there. Let me ask you this, from a management increase in complexity, what changes when the infrastructure has to be managed at that kind of scale?

**Sanjoy Maity**  
*SVP of AMI Business Unit Leader / Lattice Semiconductor*

Great question. Let me tell you that what are the challenges that the industry is facing today for this. Yes, there is a massive level of fragmentation in terms of technologies, in terms of architecture. x86 is not the only architecture.

**Moderator**

Yeah.

**Sanjoy Maity**  
*SVP of AMI Business Unit Leader / Lattice Semiconductor*

We have Arm, we have RISC-V, and everything. Scalability, security, sustainability, these are the three major challenges that the ecosystem is facing today. Heterogeneous architecture is massively, I would say, hugely complex to manage from one single pane of glass. That is why I mentioned single pane of glass, because each one has to be managed differently. AMI firmware, we implement a very modular firmware using the open source such a way that it can support with a single version of code. We support all architecture, all BMCs, all companion chips, and that is the greatest value that we bring to our customer. That is the customer benefits. What is the customer benefits? It is time to market because it is proven and pre-validated. What is another customer benefit is lower integration cost. They do not even have to worry about Lattice FPGA, AMI firmware, together, we bring that. As Ford mentioned, that this disaggregated and all these different solutions that CDU, sensors, environmental sensors, the CPU sensors, GPU sensors all are coming together. Who is going to manage that heterogeneous sensors even? We provide the brain behind it. This together, that we bring the tremendous benefit to the customer.

**Moderator**

Yeah. As the environments get more complex and heterogeneous, you are meeting your customers where they are, and that is a really good place to be. Let us look forward ahead here. You mentioned already some of the forces that were coming together, right? Started off with a lot of training and back of the envelope, we were 80/20 training and inference, now we are 80/20 inference and then training. Agentic AI, right? Three years ago it was LLMs, right? Now we have swarms and order of magnitude of agents per employee that we are forecasting. We have brand-new architectures. Brand-new architectures in the rack, outside of the rack of the entire data center. Then we have physical AI, which has not busted open yet like we have seen inside of the data center, but it is the clear next thing. On top of that, security requirements are evolving as well. Who thought that the biggest headline two weeks ago would be about jail-broken models, that the zoo animals got outside of the sandbox? All these things going. I know they are all coming together, Ford, but which market shift do you think will have the greatest impact on infrastructure over the next few years?

**Ford Tamer**  
*President and CEO / Lattice Semiconductor*

Yeah. Pat, what we'll do, it's a partnership between us and AMI, so we're going to do the same here. I'll have Sanjoy cover a couple of trends and let me cover a couple. Sanjoy, please go ahead.

**Sanjoy Maity**  
*SVP of AMI Business Unit Leader / Lattice Semiconductor*

Yes. Ford, as mentioned previously, that inference agentic trends are going on, and this will be beyond 2028. It'll continue. In the infrastructure side, what is the change that we are seeing? Because we support the infrastructure, right, the hardware level. We see disaggregation, massive level of disaggregation. Because of the scalability, the racks are disaggregated. Compute rack, power and cooling rack, network, storage. These are all disaggregated. Even within the compute rack, we see the heterogeneous architecture. It could be CPU- GPU, NPU, everything. This disaggregated solution has two major element. One is called HPM, which is the host processor module, where the CPU, GPU, NPU sits. Another one is the SCM, where secure control module comes into the picture. There, these are the two components. We, Lattice and AMI, has lot to contribute because we are open, secure, manage, and control that we are bringing to this element. So this is disaggregated.

**Ford Tamer**  
*President and CEO / Lattice Semiconductor*

Yeah.

**Sanjoy Maity**  
*SVP of AMI Business Unit Leader / Lattice Semiconductor*

It comes into the power and cooling rack where FPGAs are used. You have heard that hundreds of FPGAs are used today in the CDUs, power cell, everywhere. Network and storage comes. When you have all these disaggregated elements, somebody has to manage overall. There is one more item that we are doing is rack wide or data center wide, port wide management. That is the more critical things. So these are the trends that we are seeing in the industry. Rack management, port management, data center management is coming. Customer benefits is, again, integration, lower integration cost, time to market, and I will. Ford, please elaborate. With this Lattice firmware and Lattice FPGA and AMI firmware, what else we can offer to the industry?

**Ford Tamer**  
*President and CEO / Lattice Semiconductor*

Yeah. Thank you. If you take this to ultimate frontier, that's going to be space, right? There's a lot of talk about this data center in space, and I think eventually it's going to happen, but it will happen first on Earth. The interesting part is you won't be able to have humans go out there and manage these data centers. You're going to have to go from predictive maintenance, predictive failure, where telemetry is going to be monitored by FPGA and firmware, then go from human intervention to self-diagnostic, self-managed, self-controlled, and self-healing infrastructure, right?

**Moderator**

Right.

**Ford Tamer**  
*President and CEO / Lattice Semiconductor*

Human repairing defaults to AI predicting the failure and having these robots fix the failure ahead of time. This is where our joint solution can come in. We, again, our lower power FPGA are hardened for space. We're in this FDSOI process, which is very reliable process in the U.S. fab in Austin, Texas. We also have the firmware be part of the solution. For example, if a bit has been wrongly flipped, the firmware can fix it. If a processor is hung, the firmware can restart it. If a component is about to fail, the firmware can flag it and direct the robot to replace the part. Again, further evidence of our synergistic solutions. The final one, as I hinted before, is we see the rise of physical AI being a huge benefit for both of us-

**Moderator**

Yeah

**Ford Tamer**  
*President and CEO / Lattice Semiconductor*

in industrial robotics, humanoids, autonomous vehicle like drones and robotaxis, HMI, AGI, AR, VR. You could see we together could provide secure management and control across both of these data center and physical AI.

**Moderator**

Yeah, I'm really glad we ended on space there and the thought of you can't just send a service person up there. This thing better be self-healing. If it's not self-healing, you better have a one-button push-

**Ford Tamer**  
*President and CEO / Lattice Semiconductor*

Right

**Moderator**

where you can update not only the software but the firmware and also all the FPGA codes. I am really glad we did this. Hey, guys, it has been a great conversation. We started why Lattice and AMI are coming together, and you spent some time really doing a good job kind of interspersing the magic of the two companies. Let us try to just summarize this as we look ahead. Sanjoy, maybe you can answer this one first. What does the combined Lattice and AMI company look like going forward? Just very simply

**Sanjoy Maity**  
*SVP of AMI Business Unit Leader / Lattice Semiconductor*

Both the companies, we are very committed to support the neutrality first and support a broad ecosystem, and most importantly, open source.

**Moderator**

Yeah.

**Sanjoy Maity**  
*SVP of AMI Business Unit Leader / Lattice Semiconductor*

Open community, open source community is very important. There are, in our estimation, probably 12,000 firmware engineers around the world. Guess what? 10% are at AMI. What see the challenge is there are many contributors. Everybody contributes to the open community, but the code gets fragmented.

**Moderator**

Yeah.

**Sanjoy Maity**  
*SVP of AMI Business Unit Leader / Lattice Semiconductor*

with no single ownership and accountability. At AMI, we continuously merging those, validating them, and providing a single version of truth to all our customers. Our aspiration is to become like a Red Hat of firmware, so we can provide-

**Moderator**

Yeah

**Sanjoy Maity**  
*SVP of AMI Business Unit Leader / Lattice Semiconductor*

customers such a way that customers can have a massive time to market advantage. Ford, with this Lattice and AMI story, you can tell the audience now, where do you want to take the company next level?

**Moderator**

Yeah.

**Ford Tamer**  
*President and CEO / Lattice Semiconductor*

Thank you, Sanjoy. If that's okay, Pat, I'll just give you a quick view on what this means financially.

**Moderator**

Please

**Ford Tamer**  
*President and CEO / Lattice Semiconductor*

Near term, we're very focused on accelerating both companies, adding more resources, delivering on the commitment to customer, and going faster to market together with solutions. Long term, as I said, we aspire to be the leader in secure management and control for both data center AI and physical AI. Financially what it means, we at the last earnings call, guided to a midpoint a Q3 of a $1 billion run rate, $1 billion run rate together on the revenue side. We expect to exit this year at about $1.2 billion run rate. We also outlined on that call our aspirational goal to reach $3 billion run rate exiting 2030. That would require only just over 25% annual revenue growth rate, so very doable for us. Considering we only did $520 million in revenue last year in 2025, you could see it's a very significant growth opportunity we're delivering for our customers, for our partners, and our shareholders.

**Moderator**

Yeah, guys. Yeah, I didn't even congratulate you on the earnings. They were stunning. I do like the charts in particular that you pulled together, but I thought you did a really good job expressing financially and your long-term guide was strong as well, and really does show in the end the power of the two companies together and what that can mean financially. Guys, I really appreciate this conversation. I knew the connection of these two. I got it the first time you briefed me, and now the hard part starts.

**Ford Tamer**  
*President and CEO / Lattice Semiconductor*

Yeah

**Moderator**

Making it happen, and sounds like the two of you are up for the task.

**Ford Tamer**  
*President and CEO / Lattice Semiconductor*

Thank you, Pat. Yeah, we're looking together to a bright.
