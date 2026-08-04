---
ticker: LSCC
company: Lattice Semiconductor Corporation
title: "Lattice Semiconductor Corporation (LSCC) Presents at J.P. Morgan 54th Annual Global Technology, Media and Communications Conference Transcript"
published: 2026-05-19T14:20:51-04:00
article_id: 4906618
source_url: https://seekingalpha.com/article/4906618-lattice-semiconductor-corporation-lscc-presents-at-j-p-morgan-54th-annual-global-technology
---
Lattice Semiconductor Corporation ([LSCC](https://seekingalpha.com/symbol/LSCC#source=section%3Amain_content%7Cbutton%3Abody_link "Lattice Semiconductor Corporation")) J.P. Morgan 54th Annual Global Technology, Media and Communications Conference May 19, 2026 10:45 AM EDT

**Company Participants**

Fouad Tamer - CEO, President & Director  
Sanjoy Maity - CEO & Director  
Lorenzo A. Flores - Senior VP & CFO

**Conference Call Participants**

Mark Garcia - JPMorgan Chase & Co.

**Presentation**

**Mark Garcia**  
*JPMorgan Chase & Co.*

All right. Welcome back, everyone. My name is Mark Garcia with JPMorgan, and very happy to be hosting the management team here of Lattice Semiconductor. We have Fouad Tamer, CEO; Lorenzo Flores, CFO; and special guests, Sanjoy Maity, CEO of AMI. Great. So for those who have questions on AMI, this is great opportunity.

**Question-and-Answer Session**

**Mark Garcia**  
*JPMorgan Chase & Co.*

So Fouad, it's been over 18 months for you now. Maybe you can just sort of catch us up and what did you inherit there at Lattice? And then -- but really importantly, what's changed the most operationally today?

**Fouad Tamer**  
*CEO, President & Director*

Yes. Thank you. So when I joined, the vision of the company was to do a full portfolio of FPGA all the way from low end to high end, and there was a road map to do chips with millions of gate and -- including SoC, which is integrating the processor inside the FPGA. And when I joined, we refocused the company on the small and midrange, no SoC, meaning we have refocused the company on what's called -- the small FPGA is called our Nexus product line, N-E-X-U-S, and our midrange is Avant. And we have 3 product lines, what we call the pre-Nexus, Nexus and Avant. So Nexus, it goes up to about 200,000 logic cell, Avant to about 600, and that's the focus of the company. And we did this because our belief is that this is our sweet spot for FPGA. This is where FPGA make a lot more sense being deterministic, being low power, being low latency, being fast boot time as a companion chip to our silicon partner on the CPU, on the GPU, on the board management controller, on the NPU and MCU, on the networking switch and NIC, on the variety of different sensors. So on the sensor, we sit near an image sensor, let's say, we've got partners like Sony on the radar, for example, we announced a partnership with TI. We've got a variety of sensor work with ADI, so image, LiDAR, radar, infrared, ultraviolet as well as all kind of industrial sensor like temperature and then a variety of motor control, so different actuators. And so we feel this is the sweet spot for FPGA.

We're a high-volume supplier. So this year, we'll do over 200 million units, on our way to over 250 million. And this is our focus. So what's different is we don't try to go after these large FPGA or the millions of gate where, in my background, when we were -- I was at Broadcom and eventually Inphi, onboard at Marvell, I saw these large FPGA going in for 18 months and being replaced with ASIC because they are very high power, very expensive. So what we do is the small FPGA. We're literally on a rack of server today. We went from 10 FPGAs per rack to 100 FPGAs per rack, very low cost, very cost effective, very fast boot time.

On the SoC, we go partner with folks like NXP or ST or Renesas, where we, instead of trying to put the processor inside of the FPGA and then you're stuck with designs, our competitors like Altera and Xilinx have these SoC, they are 10-, 12-, 15-year old with really old interfaces and et cetera, we go partner with the greatest -- latest and greatest from NXP and ST and Renesas where we go jointly to market. And what we show, like, for example, we go partner on industrial control and humanoids where, together, we're going to have the best of both worlds. So you end up with the best deterministic low latency from an FPGA and the best latest tool set, the latest DDR, the latest PCI from NXP. And together, we're actually going to bring a solution that's lower latency, lower power. It's counterintuitive. If you put 2 of us together, we're together lower power because the deterministic task get done on FPGA versus the high-level stuff in NFP.

And then we refocus on data center. Data center has been growing very fast for us. The server market for us had been growing 85% year-on-year. Demand is strong for the foreseeable future, well into second half '27 and up in to the right. So that's a quick summary.

**Mark Garcia**  
*JPMorgan Chase & Co.*

Great. Actually, well, let's stick with data center then talk about your segments. Compute and Communications, as you said, has been growing more rapidly than the very high growth CapEx market. So can you kind of take us through that? What are the drivers there in terms of attach rates and ASPs for you, especially on the AI side within the Compute segment?

**Fouad Tamer**  
*CEO, President & Director*

Yes. So if you look at these, we -- it's a multiplication of various factors, right? So 5 factors, if you wish. Number 1, we grow along with -- obviously, we grow along with CapEx, and CapEx, you could think of CapEx as a number of servers. So we grow along with the number of server and that's been the CPU, and the CPU has -- recently has been growing faster because of agentic. So that's number one. Number 2 factor that's multiplicative is AI as a percent of the total server because we do have higher content on the AI server than traditional servers. So Number 1, number of server; Number 2, AI content. Number 3 is attach rate. So attach rate, we've got a number of applications that are continuing to grow. When I joined Lattice, we had 10s of FPGAs per rack, today we have 100s of FPGAs per rack. So the number of application we're finding and quite a few we can talk about are growing. Number 4, the needs continue to grow. So security has been, for example, a big application for us. Over time, the security needs have been growing higher and higher, driving a bigger FPGA per board and hence, a higher ASP.

And finally, Number 5, recently with agentic, it's not only CPU, but also storage has been growing. And so that's Number 5. The second part of Number 5 is the architecture have been changing. So if you look at the -- disaggregated architecture have taken over, disaggregated drives more FPGA because like, for example, right now, you go from 1 board being the main processor board to 2 boards, HPM where you've got the processor and where we have I/O expansion, and the second board, SEM, which is a satellite board where we do the security with root-of-trust. But also the unit of compute has migrated to where before it was 1 rack with everything in it to now 4 racks, a compute track, a communication rack, a power rack, a cooling rack. And so with that, you could see we end up having a variety more application, variety more needs for FPGA.

So you really take maybe it's really 6 factors together, and you can see that's why we're growing faster than CapEx. The latest numbers that we've seen for CapEx were just the hyperscaler for next year in '27 is going to be over $1 trillion, over $1 trillion. This number continues to grow, and this is just the hyperscalers. This doesn't include the neo cloud, does not include the sovereign, it doesn't include enterprise, so this number continue to grow very fast and will grow faster than the CapEx.

**Mark Garcia**  
*JPMorgan Chase & Co.*

It's interesting, [ Harlan ] was just up here before and talking about the growth in custom in the data center space. And what's really different this time because it seems like custom and FPGAs are really going to coexist here now going forward. So even with the growth of custom, the FPGA business is going to continue to grow at a more rapid rate.

**Fouad Tamer**  
*CEO, President & Director*

Yes. This is a very good comment. I mean, this is probably Number 7, the growth of custom. So that's another factor. We are actually totally agnostic to whether it's custom, whether it's standard product, we do want to stay Switzerland, and that's why this AMI acquisition was so powerful is we are Switzerland for companion chip for silicon and whether it's standard or custom, AMI comes in as Switzerland agnostic for firmware. And so together, we're bringing these solutions to customer and continue to support the wide ecosystem. But you're right. It's very interesting today to see the custom going against the standard product, but we support all of them. So we don't take sides. We support all of them, and we're friends with everyone.

**Mark Garcia**  
*JPMorgan Chase & Co.*

Great. Okay. So moving on to the Industrial and Embedded segment, and this is potentially the next big wave of growth from physical AI, big opportunity. Maybe you could take us through that opportunity.

**Fouad Tamer**  
*CEO, President & Director*

That's an excellent question. So yes, you're going to see these factors superimposed when you get to '27. So not only do we have growth in data center and see demand for the foreseeable future, on the Industrial and Embedded, which is what we call now our segment for industrial, for medical, aerospace, defense, consumer, we put everything in this Industrial and Embedded segment, automotive, that segment had been dragged down by inventory situation. When I joined Lattice about 18 months ago, we had 6 months inventory in the channel. We said we were going to bring it down to 2.x, and we are 2.2 as of last quarter. Our goal is to go under 2 this quarter, and we're on our way to go under 2 this quarter.

The last time we're at 1.x, we had 10 quarters of strong demand ahead. And we do believe we're entering this phase now where Industrial and Embedded should see a really strong -- a number of years ahead of strong Industrial and Embedded. So Number 1, we are growing now to natural demand as opposed to undershipping demand because inventory in the channel has been normalized. But even more importantly, we've got some phenomenal design win across all these application, industrial, humanoid, drones, autonomous vehicle, aerospace, defense, medical, consumer that are all going to market this year and will inflect into '27. And content of some of these like humanoid is very significant. So we do feel like Industrial and Embedded is going to be another growth vector for us.

If you go back to the Lattice in the '22, '23 time frame, the growth was all from Industrial and Embedded. And now you put these 2 on top of each other and should be very strong. So 3 growth vectors if you think of us in the future, data center being one, Industrial and Embedded being 2 and AMI coming on top, being 3.

**Mark Garcia**  
*JPMorgan Chase & Co.*

That's great. Well, let's go to AMI as the next catalyst of growth here. So I think a lot of folks in the audience maybe weren't familiar with AMI, which has this incredible history and is very close to the server, CPU, the GPU customers. Can you take us through what does AMI add for Lattice? And how does it change what you can offer your customers?

**Fouad Tamer**  
*CEO, President & Director*

Yes. So I'll give a high level, and I'm going to turn to Sanjoy because he's the expert. AMI started 43 years ago and a very rich heritage of -- in this space. And so when we started like last week, we did a couple of calls with the sell side because on our earnings call, we -- it was -- it's not clear what it is. So -- and then we're going to -- today, is one of the many calls hopefully we'll have on the buy side and we'd be organizing some of these calls as move forward. When -- the first question when I ask folks on the call, hey, what do you think after we explained the acquisition, people said, "Oh, let me go get my software analyst." I said, no, no, wait a minute, this is not software, okay? So that's why I think we want to explain this from the basic level.

So there's 2 businesses in AMI. It's a simple business, 2 businesses. Number 1, 55% of the business come from what's called boot firmware. And the second one, 45% of the business come from manageability, okay? So that's it. Very simple.

Number 1, boot firmware, what's boot firmware? Without AMI, there is no server. There's no data center. So AMI basically run on a flash near the CPU. it sits near Intel, AMD, ARM, NVIDIA, custom processors. And it's -- fundamentally, that firmware brings up the CPU. It boots the CPU. And then it looks on the server, it looks what components are in the server, recognizes the components on the server and then it boots the operating system. And then the software run on top of the operating system. So think of this AMI as a fundamental layer that's even underneath the hardware. You should think of AMI as hardware. That's how we think about it, okay? So this firmware is like hardware. And -- so that's about 55% of the business. And we had some great calls with all the different partners on the CPU side.

On the manageability, which is about -- and by the way, that AMI business is 75% server when it comes to boot, okay? On the manageability side, think about it, this is firmware that runs with the board management, the BMC, the board management controller. And these are board management controller from it could be ASPEED, could be Nuvoton, could be an NXP, could be new guys that are coming to market and not announced yet. So a variety of different BMC. And what -- think about the extreme example of having data center into space. And I think whether you think is going to happen or not 10 years from now, it will definitely drive the right behavior, which is, if this data center, in this space, you can't really sell a human over there to go change some stuff. So you want this data center to be totally self-managed, self-healing.

We've got -- Number 1, you want to collect a whole bunch of telemetry. We actually have customers on the telecom side of the world. They are coming to us and saying, "Look, we want to collect the same telemetry on voltage, temperature, et cetera, to be able to do, instead of doing predictive maintenance, we want to do predictive failures." The failure rate of some of these components is actually extremely high, higher than you would think. And so collecting all of this telemetry and be able to do predictive failure on AI model based on this data, which by the way, does not exist in the [ common ]. So this data on 43 years of predicting all of these failures attached to voltage, temperature resides within the 4 walls at AMI, does not exist in an open domain.

So you don't -- even if you wanted to train Claude, you don't have the data, the data is AMI. We are training the models to be able to do this kind of stuff. So Number 1 is phenomenal thing on collecting all this thing. Number 2, you want to be able to operate even if the OS is down, and that's what they do. So AMI operates even if the OS is down and you want to recover from a failure, they would be able to do it. And then they have a view of all the different components in the data center. And the high level you could think about the main cockpit for the data center where you control the whole data center, data center management could be enabled by the AMI firmware. And so very, very fundamental, very strategic.

Finally, the value prop is that they do it across all of these vendors. So you have different people that in turn may have their own boot, AMD may have their own boot, ARM may have their own boot, NVIDIA may have their own boot, but AMI works across all this. Again, different BMC folks may have their own BMC firmware, but AMI works across all this. So being this agnostic Switzerland firmware across all of these different components is a humongous value proposition that we bring. If you want, for example, to do plug and play. So today, you're working on certain components, tomorrow you want to bring a different component. That's what -- and by the way, that FPGA companion chip is tremendous because we have a low latency. So let's say you want to do a leak detection for cooling, with the FPGA sitting down with a very low latency being able to shut down that leak faster than any component you ever see because our latency is very low, okay?

Think about if you want to optimize the performance of the GPU. You want to be able to direct cooling to the GPU that's actually more -- that's being more tasked and doing more performance than the one that's idle, well, guess what, AMI allow you to do this kind of stuff. So very powerful together. Longer term, we think we'd will bring solutions to market. There is a presentation on the website that talks about some of this, but that's a high-level view. And Sanjoy, I'll turn it over to you for more detail.

**Sanjoy Maity**  
*CEO & Director*

Yes. Thank you. So yes, as Fouad mentioned, right, I will just give another analogy why it is foundational for every server or every data center. So without AMI firmware, I would say that the servers are basically metal and electronics. It's not operational in that state. So its analogy goes like a car, right? You see the ignition system. When you turn on, there is an engine check, there is a transmission check, there is airbag check, all these checks happen and then it starts the car. That's our boot firmware. Then if you think of the continuous, when you were running and driving the car, there is a system continuously checking the temperature, checking the -- everything is -- engine, transmission, everything is running optimally. If it is electric car, you have a battery management, everything is going, that's our manageability. Without these 2, car will be not functional. And same way, our boot firmware and the manageability firmware, the servers will not be functional.

And as we talk about software, operating system and software, that is the software like infotainment system in a car or a navigation system in a car or something other than playing some apps or CarPlay, those are the software. So we are foundational in this data center. And as he mentioned, I will get into a little detail that there are inflection points in the industry today based on 3 things: scalability, security and sustainability. And nobody can ignore these 3 today. And that is driving and changing the technology landscape tremendously. And we see a totally different way of making servers and the racks and powering up and the data centers are built that way.

So there are a tremendous amount of opportunity to accommodate that because it needs a runtime programmable hardware at the fleet. It cannot be determined at the beginning. And FPGAs are very critical to do that. It's the same analogy I will give. If you connect to a device to your USB port, it could be camera, it could be storage device, it could be printer, it could be anything else, but the software and operating system recognize and do this automatically. In case of hardware, there is no programmability. Only programmability you have is FPGA. So these technologies are coming because of the scalability reasons. And that is why the growth of this kind of programmable hardware is growing tremendously. And AMI is working with the large hyperscalers as well as the neo clouds, as well as the enterprise level customers and ODMs and try to make sure that this kind of technology shift, which is happening in the industry are well pre-PoCs level it is done, and it is delivered by these companies together ahead of time.

**Mark Garcia**  
*JPMorgan Chase & Co.*

Great. So Fouad, so then take us through the -- how you will expand Lattice solutions through or across that AMI footprint, which, as you just explained, is a very, very deep relationships?

**Fouad Tamer**  
*CEO, President & Director*

Yes. So the one thing I'd tell you is, as I said on the earnings call and I've done this twice before, I've done at Broadcom. When I joined Broadcom, we were Number 2 on the switch, Marvell was Number 1. And we acquired a company called LVL7 that brought us protocol firmware that we used to come up with this reference design. And we had reference design, hardware and software that were turnkey tested that we provided to our ODM partners in Taiwan. And very early on, partnered with ODMs in Taiwan to create the white box server and the white box switch. And pre-Broadcom, these were all OEMs. Broadcom invented this white box switch, white box server and LVL7 was an important piece of the puzzle to bring these reference design to market.

The second time I did it at Inphi. And at Inphi, we were selling PAM DSP inside the data center, and we had a very difficult decision to decide to go into the module space to do a DCI for Microsoft between data center 80 kilometer, very different business because we went from a component vendor to be a subsystem vendor, we're selling these modules. And the modules ended up being 20% of the Inphi business at the time, but that knowledge that we had of having silicon photonics, having these system being designed and tested were tremendous for the component side of the business because when the component side of the business had a question on how to test, on how to take the stuff to market, the knowledge was in-house.

And so these are 2 examples in my career where adding this capability was tremendous. And when we made this acquisition, Inphi, they were not -- people did not understand them. So we acquired a company called Cortina and people thought we were acquiring Cortina to go into telecom framer and mapper business, little they know that we acquired them because they had high-speed analog people that we wanted. When we acquired ClariPhy, which was a coherent DSP at Inphi, again, people thought we're getting in telecom DSP business, well, guess what, nobody knew we're doing this for Microsoft. When Microsoft announced this, it was a shock in the industry going to this DCI business. And so these are 2 examples in my career where I've done this before.

We believe AMI would open up a similar opportunity for us. We've got a slide on our website that shows some of these solutions that we are working on together with customers. And Sonjoy talked about PoC, things like rack boot. So people don't want us to boot a server at a time, they want to be able to boot the whole rack. We're working on solutions together. Things like power and cooling, things like retrofit, so people want to go back to the old fleet and be able to retrofit the old fleet with solutions for security. Things like plug and play, where you want to be able, for example, to plug and play new components inside of your existing server. So all of these are going to be enabled by a combination of AMI and Lattice.

Now where does this take us? Well, Number 1, it opens up a short-term opportunity to build a multibillion-dollar company. We said we'll exit this year at $1 billion run rate in Q4, and we're confident this will happen at very good gross margin, very strong cash flow and very strong EBITDA. So we're saying it would be at least 40% free cash flow. Next year, we grow even much faster. And taking this through the longer-term vision, this could be the first one of our many acquisitions that move the company from just a component supplier to a solution supplier. And today, we're into all these markets where we're seeing the various market across from -- today, this is just compute, but there's COMs, there's power and cooling, there's a whole bunch of industrial embedded type of market along vision and motion control, et cetera, that we can get into. So that's where we take the company.

**Mark Garcia**  
*JPMorgan Chase & Co.*

Great. And how about on timing, timing of closing and then thinking ahead maybe to the integration and how to think about success going forward?

**Fouad Tamer**  
*CEO, President & Director*

Yes. So look, integration is very important. I've done it like 25 times. At Broadcom, I had 18 different companies. Inphi, we had like half a dozen. Even Groq, we acquired a very key piece of Groq that enabled the $20 billion acquisition by NVIDIA. So integration is very key. Sonjoy and I are going down to Atlanta together, it'd be my second trip there. We're going to spend a few days with the team. Then we're going to go to China -- not to China, to Taipei for Computex and visit. They've got 600 people in Taiwan. Then we're going to go to Chennai and Pune where they've got 700 engineers. Here is a very interesting data point. There's only 5,000 -- I'm not sure if this data is correct, but if that's correct, it's like crazy. There's only 5,000 firmware engineers in the whole world, 5,000. That's it, 5,000. Over 1,000 of them are at AMI. Over 20% of the firmware engineers in the whole world are at AMI. And if this is correct, this is like totally crazy. Is that correct?

**Sanjoy Maity**  
*CEO & Director*

Yes.

**Fouad Tamer**  
*CEO, President & Director*

So integration is going to be important. We're on top of it. As far as delever, we think we delever very fast. The regulatory just U.S., we think we get this done in 45 days. And we've got an inside date of July 6. We think we'll close by then. Delever, let me at least ask Lorenzo to -- he has at least 1 question, so you talk about delever, Lorenzo.

**Mark Garcia**  
*JPMorgan Chase & Co.*

He's up next. Yes.

**Lorenzo A. Flores**  
*Senior VP & CFO*

Well, so while Fouad brought it up, Fouad said, we expect to have combined, very strong free cash flow and the debt we're taking on will be a little bit less than $1 billion from this acquisition. We are going to delever rapidly and be at or under 2 by the end of next calendar year. So we'll be well positioned. We've always had a strong balance sheet, and we intend to maintain that.

**Mark Garcia**  
*JPMorgan Chase & Co.*

Great. There is 1 question here to see in the back first.

**Unknown Analyst**

How is it that your return on invested capital over the past few years has been low? Or am I wrong?

**Lorenzo A. Flores**  
*Senior VP & CFO*

It's fundamentally the depressed profitability we've had given the decline in revenue from -- in the mid-700s 2 years ago down to the low 500s where we were. So that's what's driving the lower ROIC. We get a lot of leverage out of our business model as we grow revenue, both the -- the OpEx will not grow nearly as rapidly as revenue. This year, we're investing. That rate of growth in investment will slow down. And then our fixed capital investments have been really high, relatively high in the past couple of years because we've been doing some catch-up investments in infrastructure, that should tail off also. So the ROIC should improve significantly.

**Fouad Tamer**  
*CEO, President & Director*

Think about Q1. In Q1, we delivered 40% year-on-year revenue growth, over 80% EPS growth. So EPS is growing at twice the rate of revenue, and we should be able to get much better as revenue scale.

**Mark Garcia**  
*JPMorgan Chase & Co.*

Thank you for the excellence. That's really appreciated. So 2 questions, 1 for Fouad, 1 for Sanjoy. So the question about FPGA is, obviously, you guys have placed a lot of investment into Ultralight. Can you talk a little bit about, obviously, the AI Edge use case? Obviously, there's a lot of questions around new devices going online, localized AI processing. And then for Sanjoy, in terms of AMI, are you -- do you have any plans to open source some of the AMI frameworks for OS development or custom OS development, obviously, with a lot of AI going up online, looking to run the orchestration layer beyond what AMI is doing?

**Fouad Tamer**  
*CEO, President & Director*

Two great questions. Let me start with the first one and turn it over to Sanjoy for the second one. On the first one, we distinguished between near Edge AI, which is really the heavy processing. And there, we do believe that's the domain of NVIDIA, Qualcomm, our partners. We don't want to go into this new Edge AI. The other FPGA competitors, they do, and that's fine, more power to them. But we are very focused on called far Edge AI, which is near sensor. We call it contextual intelligence, near sensor intelligence. There, our Number 1 role is to be this companion chip where we ingest all of the whether vision, motion control and then do the preprocessing. So our role, we think, is adding AI as a preprocessor to make the near Edge AI being NVIDIA, Qualcomm more efficient and more productive. Sanjoy?

**Sanjoy Maity**  
*CEO & Director*

Yes. So for the open source and open architecture perspective, it's not a plan, we already did that. And we are the only -- we are the platinum member of OCP, and we are the only firmware company in the world who has contributed the boot and the manageability format the open source. As a matter of fact, today, we are actually doing a major event in the -- jointly with Meta at Meta's campus. And across the industry, including Meta, Microsoft, Google, all the speakers are there, and it is happening today about our open source strategy and what we are doing. We are doing it for last 3, 4 years. We are a big contributor to Linux Foundation OpenBMC. We had, as I mentioned, the most secured, OCP S.A.F.E. is the security compliance stack. At OCP, we're the only one who contributed that and maintaining it for the industry.

**Fouad Tamer**  
*CEO, President & Director*

And Lattice is also very committed to open source. We've also been a big contributor on OCP. And we do believe that together, we want to be the Red Hat for the space. So with open source, Red Hat grew a great company by contributing to Linux, and we'll do the same on manageability and control.

**Mark Garcia**  
*JPMorgan Chase & Co.*

Okay. Clearly, demand is very strong. So maybe, Lorenzo, we can talk a little bit about the supply side. What actions have you had to take, or are you taking in order to ensure that you have the supply, which is very tight out there in order to meet the demand?

**Lorenzo A. Flores**  
*Senior VP & CFO*

Sure. I'd first start -- should give some credit to our Head of Operations, who started to sense the tightness in the fourth quarter of last year and laid the groundwork for getting supplier commitments through the year, starting on the wafer side, which we are fortunate we use older nodes. They tend to be less constrained so our wafer supply got locked in. And we did actually buy in advance of the demand we saw so that we have a wafer supply. So we have a fundamental inventory strategy of building inventory in-house, and we've begun to execute that, like I said, as soon as the Q4 last year.

Then the other side of the assembly -- of the overall process is the assembly and test process. And that's where we've seen and the industry has seen a little bit more constraint. When we started to identify that, we went out and we were in a program of diversifying our supplier base, multiple size from the same vendor and more vendors. But we're still seeing what everybody else is seeing in the industry and some pressure on costs, price increases from our suppliers, but we've been able to manage that both with negotiations as well as obviously passing it through where we can to our customers.

So we feel we're in a good position from ability to support the demand. We're in the -- we have the fortunate problem -- good news problem of demand keeps increasing. So we have to keep working at it. And so far, we've been able to manage the cost side and sustain our gross margins, and we expect to be able to do that for the rest of the year.

**Mark Garcia**  
*JPMorgan Chase & Co.*

Great. And we're out of time.