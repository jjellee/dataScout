---
ticker: RGTI
company: "Rigetti Computing, Inc."
title: "Rigetti Computing, Inc. Canaccord Genuity Virtual Quantum Symposium Earnings Call Transcript"
published: 2026-05-21
quarter: "FY 2026"
event_id: 671900
source: stockanalysis
source_url: https://stockanalysis.com/stocks/rgti/transcripts/671900-canaccord-genuity-virtual-quantum-symposium/
audio_url: https://files.quartr.com/audio-files/cbcf8b6303cf0c7c53291bfa1ffa8fd7-2026-05-21-16-28-19.mpeg?ref=U0E=
---

# Rigetti Computing, Inc. — Canaccord Genuity Virtual Quantum Symposium (2026-05-21)

## 요약(stockanalysis 자동 생성)

### Industry breakthroughs and funding

- Recent advances in quantum error correction have accelerated timelines for cryptographically relevant quantum computation, with sovereign capital investments increasing globally.
- The U.S. Department of Commerce awarded $2 billion to nine quantum companies, including $100 million in equity and funding to Rigetti, supporting technology development and infrastructure.
- Additional government initiatives, such as DARPA's QBI and Canada's Project OPTIMISM, are fueling rapid maturation of the quantum sector.


### Technology positioning and differentiation

- Superconducting gate modality is favored for its speed and scalability, with over 90% of quantum investments directed here.
- Rigetti's modular chiplet architecture enables scalable quantum systems, with the 108-qubit system built from 12 9-qubit chiplets and plans to reach 1,000 qubits using 36-qubit chiplets.
- The company emphasizes open, modular integration with third-party partners, contrasting with mainframe-like closed approaches.


### Commercialization outlook and milestones

- Quantum computing is expected to become commercially relevant in about three years, reaching a critical inflection point called quantum advantage.
- Four key requirements for commercial viability: at least 1,000 physical qubits, 99.9% two-qubit gate fidelity, sub-40 nanosecond gate speed, and robust error mitigation.
- Current systems are primarily used for research, with around 1,000 AWS customers accessing the 108-qubit system.


### Strategic partnerships and manufacturing

- U.S. government funding supports miniaturization of electronics and cryostat architecture to scale to thousands of qubits.
- IBM's quantum foundry initiative, backed by $1 billion, offers a future manufacturing path for Rigetti, reducing the need for large capital expenditures.
- Partnerships with AWS, Microsoft Azure, NVIDIA, and others enable rapid integration of innovative solutions.


### Industry expectations and investor guidance

- Some investor expectations are ahead of technological reality, with commercialization and meaningful sales still several years away.
- Focus remains on advancing technology metrics rather than short-term sales growth.
- Long-term investors are encouraged to be patient as the industry approaches commercial quantum advantage.

---

## 전문

**Kingsley Crane**  
*Senior Research Analyst / Canaccord Genuity*

Welcome back, everyone. I'm Kingsley Crane, a technology analyst here at Canaccord Genuity, covering quantum computing, infrastructure software, and AI. The timing of today's event is important on two fronts. First, the science the last 18 months have produced genuine breakthroughs in quantum error correction and have helped to shorten estimates of what it takes to reach cryptographically relevant computation. Second, on the capital, today the U.S. Department of Commerce announced it's awarding $2 billion to nine quantum companies, including direct equity stakes and some of the names we're hosting today, including Rigetti. That's on top of initiatives like DARPA's QBI, Canada's Project OPTIMISM, and similar European programs. Broad strokes, the technology is maturing faster than expected. Sovereign capital is flowing in at scale, and arguably for the first time, the public quantum universe is large enough for real portfolio construction. With us today in this session is Rigetti. It's a leading U.S. pure-play superconducting quantum company. It's listed on Nasdaq under RGTI. They're a full-stack player. They're designing and manufacturing their own quantum chips in-house at Fab 1, the industry's first dedicated quantum device manufacturing facility. Earlier this year, they deployed Cepheus-1-108Q, a 108-qubit modular system built from 12 9-qubit chiplets. Again, as of this morning, they're one of three names participating today receiving $100 million from the U.S. Department of Commerce, with the government taking minority stakes. Joining us today is Dr. Subodh Kulkarni. He's been President and Chief Executive Officer since December 2022, and he brings three decades of semiconductor leadership to the role. We're thrilled to have you today, Subodh.

**Subodh Kulkarni**  
*President and CEO / Rigetti Computing*

Nice to be here. Thank you, Kingsley.

**Kingsley Crane**  
*Senior Research Analyst / Canaccord Genuity*

Maybe just to set the stage for the audience, it's a mixture of generalists and quantum specialists. Where does Rigetti sit in the quantum stack today? What do you view as your most important point of differentiation? What milestones should investors be tracking over the next 12- 18 months?

**Subodh Kulkarni**  
*President and CEO / Rigetti Computing*

Yeah. Overall, as you've mentioned, quantum computing is going through an exciting phase right now as we approach commercialization. Expectations are significant. We are talking about in the next 15- 20 years, quantum computing is expected to be hundreds of billions of dollars a year kind of a business opportunity, maybe approaching a trillion dollars a year type opportunity. That's because fundamentally, we do computing significantly faster than CPU or GPU. We are not talking factor of two or three, we are talking factor of a million or maybe even a billion times faster, but also consuming a lot less energy at the same time. It's a combination of significantly better speed at a significantly lower energy consumption. That's what makes quantum computing so exciting. Having said that, we are still in R&D stages. We are still perfecting the technology. It's still going to take us some time before we can say quantum computing is commercially relevant. At Rigetti, we believe we are roughly about three years away from a critical inflection point that we call quantum advantage. That's when we can start demonstrating quantum computing is superior over classical computing for practical applications. We are still perfecting the technology. In quantum computing, there are many different ways of quantum. Quantum, by definition, means subatomic state. There are many different ways of creating subatomic states. We use something called superconducting gate modality. Basically, we are creating IC chips and creating superconducting loops, and we are creating quantum states with electrons, essentially. We are using those quantum states to generate gates, and then we use those gates to do computing. That part is similar to what classical computing does. The key part is that we are generating superconducting loops and creating quantum states, and that uses IC chip technology. There are other ways of doing quantum states. There are modalities like what is called trapped ion or neutral atom or photonics or spin. Frankly, all these modalities have their pros and cons. We in the superconducting gate modality. Along with us, you have many other players in superconducting gate. You have players like IBM, Google, Amazon, Microsoft, Fujitsu, Toshiba, the government of China. I would say more than 90% of the investments in quantum computing are going in superconducting gate modality. The main reasons for that are fundamental strengths we have in this modality are speed and scalability. We are using chip technology very similar to semiconductor chips. We have five, six decades of experience on semiconductor industry. We know once the chip is defined, how to shrink it, increase the numbers, and so on, using all the standard knobs that semiconductor industry has learned for several decades now. Speed, we are dealing with electrons, so we are very commensurate with CPU, GPU gate speeds, so we deal with nanoseconds kind of speeds. Some other modalities like trapped ion or neutral atom, they deal with physical ions or atoms, and by definition, they're much bulkier than electrons. Their speeds are 1,000- 10,000 times slower than we are. They have the benefit. The one weakness in superconducting modality is what we call fidelity, the accuracy of information transfer between the qubits. We are building man-made circuits. By definition, that means we get a few errors, and that creates a challenge for us. Whereas when you're dealing with things like ions or atoms or photons that are intrinsically purer in nature, and they have better fidelity. Those are the trade-offs. One of the main reasons we in the superconducting camp, and as I said, most of the investments in quantum computing are going in this camp, and we believe our challenges of improving fidelity are more engineering-like challenges. Whereas some of these other modalities like trapped ion, neutral atom, or photonics, they are fundamental physics challenges. It's fundamentally, as far as we know, it's impossible to make a 10,000 times larger ion or atom move as fast as an electron. That's Newtonian physics 101 kind of stuff. Fundamentally, it's difficult for photons to entangle. That's what makes photons so unique. Those are the real physics challenges that some of those other modalities have. Our challenges are much more on the how do we decrease the error rate, exactly the kind of challenges semiconductor industry has dealt with for decades now. We feel our challenges are more manageable engineering-like challenges. Nevertheless, they are challenges. We need to continue to improve where we are with fidelity. As I mentioned, we are roughly about three years from the critical inflection point.

**Kingsley Crane**  
*Senior Research Analyst / Canaccord Genuity*

Yeah. I think you've answered some of my follow-up questions on your thoughts on modalities and comparing superconducting to the other modalities. I guess maybe just to press on that a little bit more, what would you say to maybe someone in the trapped ion camp or an investor still figuring things out that views superconducting with a higher cost for physical overhead per logical qubit, and what you could do to reduce that? Then just in general, your thoughts on what the ecosystem could look like in five years? How important is it to be first to commercial viability, and could there be room for multiple modalities?

**Subodh Kulkarni**  
*President and CEO / Rigetti Computing*

Well, I'll start with the last question first. There absolutely could be room for multiple modalities. When you are dealing with complex technologies and science like quantum physics, a lot of things are still unknown. We believe that it's going to take several years, if not a decade, maybe even more, to figure out which modality is suitable for what kind of stuff. It's definitely possible that multiple modalities coexist, and it will take several years to figure out how to make the best use of each modality. Very similar to what happened in semiconductor industry. If you go back 40 years ago, there were multiple kinds of technologies, bipolar, BiCMOS, various versions of CMOS. It took almost a couple of decades before we standardized around what currently we use, the form of CMOS technology that we use right now for most applications. Bipolar and BiCMOS and those technologies still exist. There is a small percentage of semiconductor manufacturing that still uses those technologies. We expect something similar to happen in quantum computing. Our view is that superconducting gate has the highest chances of becoming the majority because of its strength in speed and scalability, and will offset the disadvantage of fidelity over time. One of the things that you mentioned is where things may go, and from trapped ion or neutral atom or other modality standpoint, what we have said is to get to commercial quantum advantage, there are four things that are important to get to. None of us are there today, so none of us can claim quantum advantage today. A few companies that claim quantum advantage today, you need to really dig carefully to see what they are saying. They use a very vague definition of quantum advantage. They use a general definition of quantum advantage, means we should be able to go to a data center manager, make a convincing case that they should start using quantum computers. That's our practical definition. None of us are there yet. What is it going to take? We have quantified four things. We have said you need a minimum of 1,000 physical qubits. You need a minimum of 99.9% two-qubit gate fidelity. We believe you need a maximum of 40-nanosecond gate speed to be able to talk to CPUs and GPUs. Last but not least, you need to have some form of error mitigation or error control, because you will always have some errors, and you need to subdue them or correct them. Those are the four things we have said you need to get to before quantum computing becomes commercially viable. There are many companies, obviously, different modalities. We believe you need to get to those numbers before you can really claim anything relevant with data centers.

**Kingsley Crane**  
*Senior Research Analyst / Canaccord Genuity*

Mm-hmm. I do want to touch on the CHIPS Act. I want to make sure that the gravity of the moment is not lost on the audience. It's a significant investment, a significant commitment and validation. Would just love to get your thoughts on what it means for Rigetti, what it means for the quantum industry on the whole. Then I have a couple other strategic thoughts as well.

**Subodh Kulkarni**  
*President and CEO / Rigetti Computing*

We are excited to see the announcement from the U.S. government this morning. Clearly, the Trump administration is putting a big stake in the ground, saying that quantum computing is an exciting technology. It's getting mature. The U.S. government is going to invest sizable amount, we are talking a couple of billion dollars, to help grow quantum computing. Along with it, also to have a clear picture that our vision that the U.S. wants to be a leader in quantum computing. We do not want to relinquish our leadership that we seem to have right now to countries like China or some other countries. Those are the main high-level objectives of the U.S. government to take a clear, bold stand that we are going to invest in quantum computing, and we want the U.S. to be a leader in quantum computing. We are excited to be part of the initial nine companies that the U.S. government has chosen. You can see the list of the different modalities. IBM and we do superconducting gate modality similar. From what we can see, IBM's task is to put together a quantum foundry with the U.S. government. That seems to be the part of the most of the $1 billion is for building a quantum foundry. In our case, they are giving equity, which is strategically very important, but they're also giving us about $100 million to advance specific parts of the roadmap. We disclose that in this case, the roadmap areas are miniaturization of electronics that we do in readout circuitry, and also cryostat architecture that we need to improve on to get to the several thousand qubits. From what we can see, it's been done very thoughtfully, where they have taken strategic equity in key companies that they believe are going to succeed in this space, and they are asking us specifically to do things so that collectively, the U.S. comes ahead. We are very happy to be part of this overall initiative.

**Kingsley Crane**  
*Senior Research Analyst / Canaccord Genuity*

Yeah. We've mentioned this earlier in terms of the total investment and interest behind superconducting is vast and globally. Looking at CHIPS Act, IBM receiving that funding is definitely a validation of superconducting. In terms of what you mentioned too with the foundry aspect of that, and you've been pursuing this full-stack approach, how do you view that element from IBM? Is it sort of a complement? Does it kind of change the conversation in the space? Again, the backdrop is all very encouraging.

**Subodh Kulkarni**  
*President and CEO / Rigetti Computing*

It's actually exciting to have that option for us. One of our challenges that we have been trying to address is our existing fab, we have our own fab in Fremont, California, and it does a wonderful job, but it is a 6-inch fab, it's a manual fab. We view it more as a pilot fab, not a manufacturing fab by any means. To get to manufacturing, you need 300-millimeter equipment, you need automation, and our fab was just not there. We knew that the current fab that we have was good enough for the next three to five years, but beyond that, we need to go to a manufacturing fab setup. We have been exploring options as to which ones make sense. One of the options that obviously we are exploring is foundry options, because that's well known in the semi world as to how you use a foundry option. There are a few foundries that potentially are capable of building our kind of chips, so we have been investigating with those foundries. Certainly, the U.S. government and IBM committing roughly $2 billion to build a state-of-the-art quantum foundry fab somewhere in the U.S. opens up a big option for us, and they have openly said that they are going to encourage companies like us to be their customers. That's great. We would love to take our technology and use that setup. IBM is spinning off a separate company, Sure, IBM has some ownership in that company, along with the U.S. government. We are not quite sure who's going to run the operation. Maybe that's where GlobalFoundries comes in. After all, GlobalFoundries business is a foundry business model. We are not quite sure exactly where it will be and who owns how much or who runs the fab. Anyway, it doesn't matter. All those details don't matter. As long as we have access to that foundry and we can use it for our chips. We would love to take advantage of a fab like that, a state-of-the-art 300 mm fab focused on quantum chips. Given the fact that IBM technology and our technologies are so similar, it's going to be very similar materials and processes and stuff like that. We don't think we are going to need significant CapEx to become a customer of that foundry. Frankly, it opens a big option for us. It takes away a big burden off us. One of the challenges we had ahead of us was if we had to build our own fab, it would have costed us something like that number, which a couple billion dollars or at least $1 billion. Now that that option is open, it makes life a lot easy from that standpoint.

**Kingsley Crane**  
*Senior Research Analyst / Canaccord Genuity*

Okay. Yeah, that's really helpful, I think we're trying to figure out that in real time. We've talked about superconducting, but I think it's important to note that even within these modalities, the approaches can be, relatively different. Your 108-qubit system, it's 12 9-qubit chiplets tiled together, so it's modular by design. You've been modular for years. Could you just help our audience understand how the chiplet approach helps to solve the scaling problem in a fundamentally different way? You don't need to fit as many qubits on one chip. If there's just a moment where you could separate from the pack or that modular architecture could separate.

**Subodh Kulkarni**  
*President and CEO / Rigetti Computing*

Overall, our philosophy is to be open and modular architecture from across the board. If you look at our stack compared to IBM, for instance, IBM has designed a quantum computer like a mainframe computer. They control everything from chip design, fabrication, the dilution refrigeration, all the layers of hardware, all the layers of software, including cloud deployment. We have opened up just about the entire stack to third-party solutions, and that allows us to integrate innovative solutions, sometimes big giants that are playing in this area faster. Some of the well-known, publicized partnerships we have are with AWS and Microsoft Azure for cloud deployment, with NVIDIA for distribution layer software, the CUDA-Q and NVQLink, with Quanta Computer in Taiwan for control system. There are a few other smaller companies like Riverlane in Cambridge for error correction, or QphoX in Holland for microwave optical transduction. We have opened up our stack so that we can incorporate third-party solutions quickly. We believe that's a better way to go about building a quantum computer ecosystem than the way IBM is doing it with a mainframe-like approach. You get into the details of the chip design and fabrication. You go there, the modularity comes in. We fundamentally believe that chiplets are needed to scale up a quantum computer. Chiplets have been common in the semiconductor industry for more than 10 years. The main reason chiplets took off in the semiconductor industry, most of our advanced GPU, CPU applications use chiplets today. The main reason for that is because it's a lot easier to build a smaller dimension chip than a larger dimension chip, and it helps yields and how you put the whole package together. We find the same to be true in quantum computing. It's a lot easier to build a smaller dimension quantum chip than a larger dimension quantum chip. Why shouldn't it be? After all, we are using similar equipment, similar etching, similar deposition equipment. All the reasons why chiplets are needed in the semiconductor industry are the same reasons why we believe chiplets are needed in quantum computing. We were one of the first companies to realize that. We have a lot of patents in that area. We have almost 15 or so patents covering the concept of chiplets in quantum computing. We have been developing chiplet-based quantum computers for a while now. As far as we know, we are the only company as of today that has deployed a chiplet-based quantum computer on the cloud and make it available to anyone. Our 108-qubit system is indeed 12 9-qubit chiplets. Going forward, when we go to 1,000 qubits roughly three years from now, we will be talking about 36-qubit chiplets and about 30 of them. That comes to about 1,080-type qubits. It's a huge advantage we have, we believe, in how we can scale up a quantum computer using chiplets. IBM has openly said that they are going to do what they call couplers, they are taking single chips and connecting them with cables effectively, and then they're going to use a network of quantum computers to get to 1,000-qubit. We believe our approach is much more elegant. It's a lot cheaper when we look at how you build a 1,000-qubit computer compared to IBM or other approaches. We firmly believe in the concept of chiplets. We have a lot of IP in that area, and we'll continue to push that approach.

**Kingsley Crane**  
*Senior Research Analyst / Canaccord Genuity*

On the 108-qubit system, so it's on AWS Braket. It's been up there since earlier this year. Just any color on adoption, what you're seeing from researchers and enterprises that split, and then just what that system can unlock versus the 84-qubit system?

**Subodh Kulkarni**  
*President and CEO / Rigetti Computing*

Yeah, definitely it's a lot more powerful a system, not only because of the 84- qubits going to 108 qubits, but also because the fidelity improved. That also helps. Gate speeds also improved. It's overall a much more powerful quantum computer than the 84-qubit we had on AWS and Azure for the last couple of years. Initial reactions are very promising. We don't see the exact list of customers that are using it, but roughly there are 1,000 customers that are using the system right now on AWS. We see the type of customers and the amount of time they're using. We can say that most of the customers that are using the system today are using it for research applications. They are using it for a few seconds to a few minutes. Very few of them are using it for hours. Those are the customers that are really going deep into the system to try to find out the limitations of the system and so on. Most of the work that we see is done by national labs, universities, a few commercial organizations that are interested in understanding quantum computing as a research activity. It's still research going on with those quantum computing systems. This is definitely high. We are talking with AWS about doing joint marketing with them, given the increasing interest in quantum computing.

**Kingsley Crane**  
*Senior Research Analyst / Canaccord Genuity*

Mm-hmm. Again, it's a monumental day for the space and for Rigetti. If you were to look across the industry and think about where investor expectations or expectations from scientists could be running ahead of schedule, or where the technology is, where do you think that might be? Then what do you think is most important for Rigetti to prove over the next two years?

**Subodh Kulkarni**  
*President and CEO / Rigetti Computing*

Yeah, I believe some of the investor expectations, and based on comments made by some other companies, may be running ahead in terms of commercialization. There are a few companies that have hyped up this area a little bit, and they are claiming that they will have quantum advantage this year. I'll also note that the same company said they would have quantum advantage last year, and clearly they don't. There are a few companies that have been very aggressive in their marketing and potential for quantum computing in the very short term. That, we believe, has led to some investor confusion. Some companies just talk about sales and sales growth right now, but clearly, sales is lumpy, and it's all research related. We don't tend to focus on sales as much as we focus on the technology metrics. When you're in R&D phase that we clearly are in, it's a lot more important to focus on technology metrics than sales and sales growth. Some companies have gone that way, and that has led to some investors thinking that this is like you should be talking about doubling or tripling of sales every year right now. Frankly, that's not the right way to look at it when you are still perfecting the technology.

**Kingsley Crane**  
*Senior Research Analyst / Canaccord Genuity*

Well, again, thank you, Subodh, for the time. I think we're running up on our time here. Is there anything you'd like to leave our audience with?

**Subodh Kulkarni**  
*President and CEO / Rigetti Computing*

Well, thank you for the opportunity. Overall, it's an exciting space. It's going to be a huge growth opportunity. All I am saying is you have to be cautious about the rate of growth. It's not going to happen next year by any means. We are talking about three years to get to commercial quantum advantages, and that's really when you are going to see sales and all those numbers start becoming very meaningful. Exciting opportunity for long-term investors who believe quantum computing is going to play. This is definitely an exciting space to play in, and we think Rigetti is very well positioned to be one of the winners in this space.

**Kingsley Crane**  
*Senior Research Analyst / Canaccord Genuity*

Yeah. I think investors and the market are very receptive to longer-term technology stories right now, and the optimism is high. Again, because the technology is proving itself, it just may take time. Again, thank you again for your time and your participation, Subodh.

**Subodh Kulkarni**  
*President and CEO / Rigetti Computing*

Thank you, Kingsley.
