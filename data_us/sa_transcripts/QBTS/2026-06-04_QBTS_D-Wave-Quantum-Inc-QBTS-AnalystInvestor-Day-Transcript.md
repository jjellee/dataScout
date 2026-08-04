---
ticker: QBTS
company: D-Wave Quantum Inc.
title: "D-Wave Quantum Inc. (QBTS) Analyst/Investor Day Transcript"
published: 2026-06-04T18:42:54-04:00
article_id: 4912087
source_url: https://seekingalpha.com/article/4912087-d-wave-quantum-inc-qbts-analyst-investor-day-transcript
---
D-Wave Quantum Inc. ([QBTS](https://seekingalpha.com/symbol/QBTS#source=section%3Amain_content%7Cbutton%3Abody_link "D-Wave Quantum Inc.")) Analyst/Investor Day June 1, 2026 1:00 PM EDT

**Company Participants**

Kevin Hunt - Senior Director of Investor Relations  
Alan Baratz - President, CEO & Director  
Trevor Lanting - Chief Development Officer  
Robert Schoelkopf - Chief Scientist  
Lorenzo Martinelli - Chief Revenue Officer  
John Markovich - Executive VP & CFO

**Conference Call Participants**

Lucus Haugen  
Sreekrishnan Sankarnarayanan - TD Cowen, Research Division  
Matthew Cimaglia  
John McPeake - Rosenblatt Securities Inc., Research Division  
Antoine Legault - Wedbush Securities Inc., Research Division  
Craig Ellis - B. Riley Securities, Inc., Research Division  
Quinn Bolton - Needham & Company, LLC, Research Division  
Troy Jensen - Cantor Fitzgerald & Co., Research Division  
Tyler Perry Anderson - Craig-Hallum Capital Group LLC, Research Division  
Daniel Stevens  
Vijay Rakesh - Mizuho Securities USA LLC, Research Division  
William Kingsley Crane - Canaccord Genuity Corp., Research Division

**Presentation**

**Unknown Attendee**

Please welcome to the stage Senior Director, Investor Relations, Kevin Hunt.

**Kevin Hunt**  
*Senior Director of Investor Relations*

Okay. Thank you, and thank you all for joining us today for D-Wave's first ever Investor Day. Thank you for all of you in the room for joining us, making all the way down to the NYSE, and thanks to all the hundreds that are listening to the live stream online. We 've got a great lineup of presentation for you today. So hopefully, you'll all be quantum experts by the end of the day.

Just a few notes on the agenda. We will be having several opportunities to ask questions during the day. Our CEO, Dr. Alan Baratz, will have -- answer some questions from people in the room following his keynote. We'll have two other places you can ask questions. For those of you in the room, please raise your hand, and we will bring a microphone to you. We ask that you identify yourself before you ask a question and that you limit yourself to one question.

Following the end of the last Q&A session at the end of the day, we will be having a reception for people out in the room -- in the back room there from 4 to 5. You'll be able to see some demos and meet with the members of the D-Wave management team. For those viewing online in the live stream, you also can ask questions via the Ask button and we'll try to get to as many of those as we can.

So turning to the ever popular disclaimers, we will be making -- members of D-Wave's management team will be making forward-looking statements over the course of the afternoon. There are always risks and uncertainties associated with any such forward-looking statements. You can see a list here in the slide behind me. And this investor deck has been posted to our company website. So you can see the list there as well. If you want even more risks, you can go to our 10-K filed with the SEC and also available on our company website.

We also will be referring to some non-GAAP financial metrics such as bookings throughout the day. And we may -- in case that other non-GAAP financial metrics come up during Q&A, you can see a full list and descriptions of those in our earnings releases, which are available on our company website.

So with that, I'll turn it over to our CEO, Dr. Alan Bars.

**Unknown Attendee**

Please welcome to the stage, D-Wave's President and CEO, Dr. Alan Baratz.

**Alan Baratz**  
*President, CEO & Director*

Good afternoon. So my name is Alan Baratz. I am the CEO of D-Wave. I have no clue who that guy in the picture is. It's a real pleasure to be here with you all today. I thank every one of you who took the time to come down here to the New York Stock Exchange and be here in-person. Thanks also to those of you that are joining us via the live stream.

There's quite a bit that we would like to cover with you today. But honestly, the Q&A sessions are equally, if not more, important. We want to make sure that there's plenty of opportunity to ask questions. And so we've allocated three different times for Q&A. And hopefully, through that, we'll have the opportunity to answer most, if not all, of the questions.

So I'm going to start with the obligatory picture of Richard Feynman, although hopefully, you haven't seen this version of the picture before since our excellent graphic design has made it up. Richard Feynman, of course, coined the term quantum computer back in 1981. And he's famous for a number of other interesting and important commentary on quantum mechanics and quantum computing.

One that I think is particularly relevant to us, and by us, I mean the entire quantum computing industry here today; is the one that we have up on the screen. If you think you understand quantum mechanics, you don't understand quantum mechanics. This is very complex technology.

The problem with that is that it's way too easy to say misleading things and to spew hype into the marketplace, and it's hard for all of us to be able to separate all that noise from the signal. And so part of what I'm hoping to do here today is at least for D-Wave, help you think about how to separate the signal from the noise and how to think about D-Wave in the context of what we are telling you against, if not the science, at least sound logical thinking.

So I'm going to start at the very top. What is quantum computing? For me, quantum computing is energy-efficient computing for solving hard computational problems. That's typically not where people start when they talk about quantum computing. But I start there because quantum computers consume very little power.

And on top of that, they use quantum mechanics to compute the solutions to problems very, very quickly. And that combination truly allows them to be much more energy efficient at solving problems than classical computers.

Now there's more than one approach to building a quantum computer. And this is particularly important in the context of understanding D-Wave and how we are different from every other quantum computing in the industry. There are two main approaches to building a quantum computer. One is called annealing and the other is called gate model.

For those of you that have been following us over the years, you've heard us talk quite a bit about annealing because, frankly, we started with annealing, and we're the only company in the world today that brings annealing quantum computers to market.

As we go through the course of the day, we're going to talk not only about the power and value and road map for annealing, but we're also going to talk about gate model because we are now also a significant player in gate model, quantum computing.

But before I dive into it, let me just take a minute to try to explain the difference between gate model quantum computing and annealing quantum computing. And I'm going to start by talking about classical computers.

So typically, you'll hear people say that classical computers use to store information, and a bit can be either a 0 or a 1. And this means that at any point in time, the information that the computer, the classical computer is seeing is one possible solution to a problem. It's how 0s and 1s have been assigned to the various bits. That shows you one possible solution. It's like dropping a tennis ball into a landscape, and it hits at one point.

Now suppose you want to find the overall lowest point in this landscape, which is the valley to the left of this image, well, how do classical computers work? They basically perform computations and logical operations that attempt to explore the landscape one point after the next. They're moving that tennis ball around point by point, looking for the lowest possible point.

Now if your landscape is simple like a bowl, it's easy. There are very efficient algorithms for finding the lowest point. You can get there quickly. But if it's a complicated landscape, this is actually an exponentially hard problem. What it means is there's not enough structure in the problem to be able to efficiently find that lowest point. The amount of compute time is exponential in the size of the problem.

And this is exactly the kind of problem that's good for quantum computers, the very hard computational problems. So how does a gate model quantum computer work?

Well, gate model systems use qubits, and a qubit can be 0 and 1 at the same time, which means that at any point in time, you're able to see multiple possible solutions to the problem, not just one possible solution, and you're able to perform operations on those multiple possible solutions simultaneously, computations, logical operations.

So the problem becomes one of not kind of figuring out how to follow the ball to the lowest point, but you've got all the balls. You can see all the points. Now the algorithms are all about figuring out which one of those balls is actually at the lowest point. It's a different way of thinking about computation and how to program the computer.

But there's one other important point about gate model systems, and that is quantum mechanics was not really designed to support digital computation. So as we build these gate model systems, we're trying to implement digital computation on quantum mechanical systems.

We're pushing against nature, and that introduces errors. That's why gate model systems are so error prone and why without the ability to correct those errors, we're never going to be able to solve useful problems on gate model systems. So error correction is critically important for gate model systems.

Annealing quantum computers work in a very different way. Annealing quantum computers are really all about finding the lowest point in a large landscape. They're about using quantum mechanics to find what we call a low-energy state. It's working with quantum mechanics.

You can think of it like dropping water into the landscape and looking at where it pools. It pools at the lowest possible point because the water is able to tunnel through the hills and valleys and get to the lowest possible point.

Annealing quantum computers use quantum mechanics to do exactly that. They use superposition, they use entangle and they use tunneling. They work with nature to find the low point or solve the problem, right? And as a result, they're nowhere near as sensitive to noise and errors. And that's why our annealing quantum computers are solving hard customer problems today without the need for error correction.

But both are important. There are problems that require annealing, specifically, business optimization problems are well suited to annealing. Gate model systems are not very good at solving them. And there are problems that require gate model, quantum chemistry, for example, materials discovery. These are well suited to gate model systems, not very good at solving optimization problems, right? You need both annealing and gate in order to be able to address the full market for quantum.

Okay. So now how do we think about finding the signal within all the noise that's going on out there? Well, we think that to be successful in the quantum computing industry, you need three things.

One, you need to be able to address the full market for quantum, all the possible use cases. Two, you need to do that with viable commercial products, not research tools, but viable commercial products. And three, you need to be able to deliver measurable customer value in using those systems, address the full market with commercially viable products, delivering measurable customer value.

And we think that D-Wave is right now pretty much the only company in the world, the only quantum computing company that can address and deliver on all three of those, and I'm going to explain why.

Let's start with the first, address the full market. Okay. So there are many different TAM analyses that have been done by different consulting firms, TAM, total addressable market analysis. Boston Consulting Group has done it. McKinsey has done it, a variety of other consulting firms have done it.

But the one that most of the industry has latched on to for 5 years now is the Boston Consulting Group study. They put it out initially about 5 years ago. They refreshed it about a year ago.

BCG puts the total addressable market for quantum at just under $1 trillion in roughly the 20-year time frame. And they divide it into 4 different technological segments or use case areas: cryptography, optimization, machine learning or AI and simulation. And they assign a value to each of those adding up to the $850 billion total value.

Well, if you think back to what I said a few minutes ago with respect to annealing and gate model, gate model cannot address all of these, annealing cannot address all of these. Gate model, for example, is required for quantum mechanical simulation, drug discovery, materials design. It's also quite good at breaking codes, right? Annealing quantum computers are required for optimization problems, workforce scheduling, manufacturing plant floor optimization.

You need both to address the full set of use cases for quantum computing. And D-Wave is the only company in the world bringing both annealing and gate model to market. We're the only company in the world that can address the full TAM for quantum, the full set of use cases for quantum.

In addition, sometimes the gate model companies will have optimization envy. They vacillate between "Oh, we can do optimization as well. Look at -- we solved this optimization problem as well as it can be solved on a laptop. See, we can do optimization as well." Okay, as well as it can be solved on a laptop, what about solving it better than it can be solved classically? There's significant, both theoretical and experimental evidence that gate model systems just can't beat classical on optimization, but annealing systems can.

Then sometimes we'll hear, "Oh, annealing is just a niche. It only addresses a niche market." Well, is optimization a niche market? First of all, it's a full 25% of the TAM that we just discussed. But think about it, the numbers, $100 billion to $220 billion, bigger than the global semiconductor market, bigger than the global cybersecurity market. Are those niche markets? I don't think so.

The point being that there's only one quantum computing company that can address the full TAM for quantum. And each of our products, our annealing quantum computers and our gate model quantum computers, are addressing a very significant portion of the TAM.

Okay. Let's move on to commercially viable products. I want to start by defining commercially viable. You will hear every quantum computing company say, "We're commercial today. We've sold a quantum computer to this company or this company is using our quantum computer to work on this collection of problems," right?

Research experimentation with a quantum computer is not commercial use of the quantum computer. Commercial use of the quantum computer is using it as a part of your business operations on a daily basis, an integral part of your business operations. That's what it means to be commercial.

So again, lots of noise, lots of hype, "Oh, we're commercial." Next time, your favorite quantum computing company other than D-Wave because I know D-Wave is all of your favorite, but next time your other favorite quantum computing company says, "Oh, we're commercial," or say, "Who's the customer? What's the application? How often are they running it? Can I go talk to them?" ask us, we'd be more than happy for you to talk to our customers.

Every time we have an event, we actually have customers participating in the event with us. So you've got to cut through the noise. Commercial means in use on a daily basis as part of business operations. Now the customers that we bring on stage, some of them are commercial, some of them are still in the R&D phase. And we're clear to talk about that as we engage in those discussions.

Okay. So let's start with our annealing products. Our flagship annealing quantum computer is our Advantage2 system. It is a 4,500 qubit annealing quantum computer. We've also built a complete ecosystem of products around that. We have a quantum cloud service called Leap. This is designed to support business applications in production, building in the reliability, availability, security, privacy needed to be able to support commercial applications.

We also have a complete suite of software development tools, our Ocean SDK for building applications, leveraging our annealing systems. We have a suite of hybrid solvers that bring together classical and quantum to solve problems on the quantum computer that are larger than can natively fit onto the quantum computer.

And we have a professional services capability for helping our customers understand which applications can most benefit from quantum and how to build out those applications. This is a very comprehensive and very mature platform of products in the annealing arena.

We've got one of the largest aerospace companies working with our products, one of the largest airlines working with our products, one of the largest chemical companies working with our products, one of the largest mobile carriers working with our products. We're working with government contractors on national security and defense.

This technology space is quite mature today. Still more work that needs to be done, but nonetheless, quite mature today. And we've talked about some of the metrics associated with improvements that these customers have seen leveraging our quantum computers. We'll talk a little bit more about that later.

We've also pointed out that our annealing quantum computer, our Advantage quantum computer is the only quantum computer in the world that has been able to solve a useful real-world problem that cannot be solved classically, true quantum supremacy.

We published this in science a little over a year ago. This is computing properties of materials that were computed on our system in 20 minutes, that's the image on the right, and it would take nearly 1 million years, billions of minutes to solve it on the fastest supercomputers in the world.

Now I'm going to just diverge for a minute and talk about a little bit more hype, right? There are many people that would love to say we have not achieved supremacy on this system, and they try. And you may have seen a headline a week or 2 ago that a group of researchers just published a paper in science where they basically have shown that classical can solve the problem that we solve.

Okay. Go read the paper, right? The headline and the paper are very different things. They have not solved all the lattices that we solved, all the sizes of the lattices that we solved, all the evolution times that we solved and all the properties that we computed, all of which is required to achieve supremacy. They've done a small subset of what we have done.

This supremacy result has been out there for almost 2 years now. It was published in science a year ago. It was put on the technical archive a year before that, and it still stands. This is the one true demonstration of quantum supremacy.

As far as our annealing roadmap is concerned, we've talked about the fact that our Advantage3 system will have 100,000 qubits. We haven't really put dates around that previously, but now we are providing dates for the 100,000 qubit Advantage3 system and a smaller 20,000 qubit version.

There are two important technologies that are enabling our move from 4,500 qubits to -- or 4,400 qubits, sorry for rounding up, to 100,000 qubits. They are multichip, basically moving from more qubits on a chip to interconnecting processor chips, multichip and scalable control.

On the multichip front, basically, what we're talking about, and it's shown here, tiling in 2 dimensions, our 4,500qubit processor chips. So 4 to 5 chips to get to 20,000 qubits, 25 or so chips to get to 100,000 qubits. We need to be able to interconnect these things electrically through bonds that are superconducting and preserve quantum mechanical properties.

This is work that we've been doing with the NASA Jet Propulsion lab. We've developed the materials and the process for this, and we've actually been able to demonstrate the ability to bond the chips and preserve these properties. So that was one of the two technical challenges that we needed to overcome to drive to the Advantage 300,000 qubit system.

The second, scalable control. And this is a really important point because it's going to come back when we talk about the gate model systems as well. So typically, if you go ask anybody in the industry, how many control lines do you need to control a qubit, you'll hear 3 to 5 per qubit. So that would mean that our 4,500 qubit Advantage2 system would require 12,000 to 20,000 I/O lines.

We control that 4,500 qubit processor with 200 to 300 I/O lines because we've been able to build data pipelining, multiplexing, addressing onto the processor chip, which means we can much more efficiently control the qubits. And that's critically important.

Now when we go from 4,500 to 100,000 qubits, though, we can't have a 25-fold increase in the number of I/O lines. So we've been working on modifying our control architecture to make it even more scalable than it has been up until now. We've completed the design. We've completed the masks for the first chips to basically test out the design, and they're going through fabrication now. And that's the second important component of being able to scale to the 100,000 qubit processor.

Both of these technologies are well down the development path. But obviously, we have some time and work to test and really kind of ring out any issues associated with either of these technologies. But we're quite enthusiastic about the path to 100,000 qubit.

And why is this important? So if we think about our current 4,500 qubit system, when combined with our hybrid solvers, we can support problems with up to 2 million variables. And that's fine for solving a lot of problems. But if, for example, we wanted to solve full-up last-mile routing for FedEx or UPS, that we require 50 million variables. So we still have to continue scaling on the annealing side to solve larger and more complex problems.

All right. Now I want to spend a little bit of time talking about the gate systems. We announced quite a few years ago that we're going to start working on a gate model quantum computer as well. A lot of the work that we had been doing was looking at how you could take that control architecture that I talked about for annealing systems and move it into the gate model environment.

We have not spent as much time on high-quality qubits and the ability to error correct those qubits. But what you need in order to have a commercially viable gate model quantum computer is you need error correction and efficient error correction, you need scale and you need for the systems to be fast, right? Nobody wants a slow quantum computer.

And so we've been focused on how to advance the state-of-the-art and our technology development in each of those areas, efficient error correction, scalable systems, fast computation. So we are bringing together to solve this collection of problems two critically important technologies.

Relative to the ability to efficiently error correct and have fast computation, we closed the acquisition of Quantum Circuits in January. This was a company that was spun out of Yale University and founded to basically commercialize some very important new qubit technology advances that have been developed at Yale. And in a few minutes, you're going to hear from Rob Schoelkopf, who was leading all of that work at Yale and was the founder of Quantum Circuits.

The qubit technology that was developed at Yale, spun out into Quantum Circuits, acquired by D-Wave; is very revolutionary. First of all, it is superconducting qubit technology, which means it is fast. Superconducting qubits run 1,000 to 10,000x faster than trapped ion or neutral atom qubits. These are superconducting qubits. They're very fast.

But typically, the trapped ion or neutral atom folks won't argue that they're slower, but they'll say, "But our qubits are more natural qubits. They're more efficient qubits. They're much easier to error correct. Superconducting may never be able to error correct."

Well, here's the really important thing about the new qubit technology called dual-rail qubits. They have the same efficiency as trapped ions or neutral atoms. So think about it. These are revolutionary qubits that have the speed of superconducting and the efficiency or reliability when it comes to error correction of trapped ions or neutral atoms, the best of both worlds.

Then we are going to marry that with the control technology that we had developed for our annealing quantum computers to allow us to much more efficiently scale these gate model systems, essentially attacking all three of the elements required to truly have a commercially viable gate model system, efficient error correction, scalability and speed.

Think about it this way. Trapped ions or neutral atoms are like a bicycle. Simple and efficient, easy to error correct, but slow. Superconducting, the things that IBM or Google are using; very, very fast, but very complex, not all that reliable, kind of like an old piston airplane. D-Wave's dual-rail qubits are the best of both worlds. They are fast, but they are also simpler and far more reliable, like turbine jet engines, the best of both worlds.

Okay. Let me just provide some metrics now to help back this up. We think that there are two metrics that it's really important for everybody to start focusing on when it comes to getting to truly commercially viable gate model quantum computers. One is speed, and the other we're calling lambda. This is the error correction efficiency. And I'm going to spend a minute talking through this.

First of all, speed. The chart on the left shows you the time required to perform an error correction cycle on superconducting, trapped ion and neutral atom. Look at that. 5 microseconds for superconducting, 30,000 microseconds for irons, 200,000 for neutral atoms. They are very, very slow technologies.

Okay. So superconducting's fast. And I think everybody accepts that, right? The debate really has more to do with, "Yes, but can you actually error correct these superconducting qubits?" So that's where we think lambda becomes very important. Lambda is the rate at which you can reduce errors as the error correction code increases.

So if we look at the chart on the right, okay, at the top, I have surface code distances. Surface code is the typical code used to error correct gate model quantum computers. And there are 4 surface code distances shown there, distance code 3, 5, 7, 9. And typically, the number of physical qubits you need is the square of the distance of the surface code, okay, surface because it's got a length and a width, okay?

Okay. So at distance 3 -- okay, 9 we're saying 17 physical per logical qubit. Distance code, distance 5, 25, 49, there's a factor of 2, which I'm kind of glossing over; 7, 49 times 2, 97, 9, 81 times 2, 181, okay? So distance 3, distance 5, distance 7, distance 9 are increasingly larger surface codes for doing error correction. And the larger the code, the better the error correction.

At the bottom is the number of physical qubits that you need per error-corrected qubit -- logical error corrected qubit for each of those distance surface codes. Now look at the 2 lines. Currently, in the industry, we're looking at a lambda of 2. What this means is that as you increase the surface code distance, you half the errors. So you get 1/2 the errors for each increment in the surface code. That's the gray line, okay?

What we are looking at with our dual rail qubits is a lambda of 10. With each increment in the surface code, we get a factor of 10 reduction in errors. This becomes really important if you think about what you need to actually be able to use a gate model quantum computer. You need to be able to perform computations. And you need the errors to be low enough that you can perform all those computations before an error emerges.

We think that we're going to need about 1 million computations to start doing useful work. This means we need an error rate of 10 to the minus 6, 1 error in 1 million in order to be commercially viable. So now look at those 2 lines. At a lambda of 10, you can get to 10 to the minus 6 with a distance 9 service code, roughly 100 to 200 physical to logical qubits. That's the path we're on with our gate model program. That's very viable, right?

The gray line where the industry is right now, what would it take to get to 10 to the minus 6? We're talking 1,000 or more physical qubits per logical qubit by the time that gray line gets out to 10 to the minus 6. okay? That's the power in the dual-rail super qubits. They are superconducting, fast with a very rapid decline in error rate as we increase the error correction.

So for our product roadmap for gate model, we've divided it into 2 errors, what we call the post-NISQ era, where we start seeing some error detection capability that we can use in the computation; and then the fault-tolerant era, which is where we're actually at the point where we can really perform up to 1 million computations and do useful work.

So this is what you can expect from D-Wave over the course of the next roughly 6 years, with the goal being that in 2032, we would have 100 logical qubits built on 10,000 to 20,000 physical qubits with an ability to support up to 1 million gates or computations, actually the beginning of commercial viability.

So this is what you need to be asking others about. "Well, what's the speed of your computation? How rapidly are you going to be able to reduce errors as you increase the error correcting code? And when will you be able to support at least 1 million computations?" Those are the key elements, okay?

The only other thing I'm going to say about the products is we were really, really pleased to be a part of the U.S. government announcement a week or so ago, basically talking about the fact that the U.S. government is providing D-Wave along with a number of other companies, funding to basically support R&D work around the development of quantum computers.

This was really important for D-Wave for two reasons. First of all, this was the first time the U.S. government had actually endorsed D-Wave. And secondly, they not only endorsed D-Wave, but they endorsed both annealing and gate. So now the U.S. government has finally started to realize annealing is important alongside gate. They are both important. And this was an endorsement of both of those approaches to quantum computing.

Okay. Now what I want to do is transition and start talking about customers and customer value. And I want to start by, in a minute, asking Lucus Haugen to join me up here on stage. Lucus is from AT&T. To be fair, AT&T is not in production today, but they are working with our quantum computers on a variety of applications.

Lucus is an Innovative Director of Data Science at AT&T's Chief Data Office, where he leads a world-class team of data scientists, ML engineers, developers and solution architects to deliver enterprise-scale impact. He's recognized as a leader in digital transformation, leveraging agentic AI, advanced machine learning, automation and big data engineering to drive operational excellence and create business value approaching $1 billion annually for AT&T.

Lucus and his team began exploring D-Wave's impact on their operation at AT&T less than a year ago, and he's here to talk a little bit about that experience. Lucus?

Okay, Lucus. So maybe -- yes, go ahead.

**Lucus Haugen**

Hello, everyone.

**Alan Baratz**  
*President, CEO & Director*

So maybe you can start by telling us how AT&T is working with D-Wave quantum computing technology.

**Lucus Haugen**

Yes, sure. So again, we're kind of getting started. We've been working on it for a little bit. We're kind of focusing on two main problems. Of course, we're working on tackling traditional optimization problems that we're doing with classical compute today. And then we're also trying to adapt the solvers to do kind of tackle our high-intensity compute problems to see if we can get a little bit of a quantum HPC advantage out of that.

**Alan Baratz**  
*President, CEO & Director*

Can you maybe talk a little bit about some of the use cases you're exploring or planning to explore?

**Lucus Haugen**

Yes. So basically, we're looking at pretty much use cases across the full spectrum or all facets of our network operations front. Some examples are going to be our technician routing optimization. That's a big one, of course.

We're also looking at -- another big one is identifying network outages and then managing those. How can we make them more efficient and more quickly? We're moving into network build optimization and even some of the network traffic optimization is kind of the use cases we're exploring.

**Alan Baratz**  
*President, CEO & Director*

And how has it been to work with D-Wave?

**Lucus Haugen**

I will say that I think one of the, at least in my opinion, understated benefits of the D-Wave solvers is how easy they are to use. You take my team, a group of data scientists and engineers and myself, and we're onboarding right away with it. We've got a little bit of -- basically, anyone with a data science background who used to cranking through algorithms can pick them right up. You don't have to have a physics background.

The other thing, this is very profound as well. Because you mentioned the Ocean SDK, we can do much of the, I would say, heavy lifting, but much of the upfront work is in our own environment. And when we take the quantum use, we're basically just sending off a little array, I say little, right? It's simple, but very big array of bits or points in 2-dimensional space. That's derived from our problem set. It has nothing to do with AT&T data. It protects all of our private sensitive IP. Nothing goes to D-Wave.

Not to imply that it's not secure, it's just -- I'll tell you, it takes a tremendous burden off of my team to not have to go to governance -- data governance and security and it's safe, it's safe. We're not sending anything. We're literally sending nothing because we don't have to. I'll also point out that every time we've needed it, your solvers have been available. That's a massive advantage in kind of our space where we're cranking through quite a bit. So overall, it's very easy for my team and me to use.

**Alan Baratz**  
*President, CEO & Director*

Yes. I actually just want to reinforce the security comment for a minute. First of all, we have SOC 2 Type II compliance for our platform all the way through to the quantum computers. We focus heavily on security and privacy.

But the point you made is really important. It's not that you don't send things, you actually send a lot of data to our systems, but what you're sending is a matrix and a vector to set of numbers that cannot be reversed engineered into any user data or even the problem that you're trying to solve. So it's a very opaque data transfer that provides protection.

**Lucus Haugen**

And we can't stress that enough because I don't have to worry about masking data encrypting data or anything of that nature. All it is, is a drive set of numbers from our problem set, which is meaningless otherwise without that context.

**Alan Baratz**  
*President, CEO & Director*

Yes. So as you look to the future, where do you see the opportunities for AT&T with quantum computing?

**Lucus Haugen**

I think I touched on it a little bit. I think for us, it's two profound opportunities with D-Wave. Again, we're kind of looking at with the quantum tunneling, [ abatic's ]. It's one of my favorite words, by the way. The architecture itself is to optimize what we're doing today. We can take what -- in seconds we can accomplish what's taking us hours and days to do with classical optimization problems.

The second thing is we've got a tremendous -- we probably crank through hundreds of billions of signals in our real-time data use cases. And what we're trying to do is leverage the solvers to offset a lot of that. And so basically kind of twisted into kind of a high-performance computing thing.

So with optimization, I think we've got an application. We've already cranked from an hour down to less than 15 seconds. And then we're looking at exploring the HPC aspect. We can see with kind of preliminary results, the potential for magnitude of order of improvement in what we're seeing today just in our speed and efficiency.

**Alan Baratz**  
*President, CEO & Director*

So maybe just one last question. What advice would you give to other companies who may be curious about or interested in quantum?

**Lucus Haugen**

That's a good way. I think upfront, and you kind of touched on this as well, is don't be afraid of the, I guess, the aspects of the quantum physics part of it. You don't really need the background to work with it.

Also, having said that, be careful that quasi-echo chamber of experts and pundits and academics saying it's not real, it's not available. It's not ready yet. It is, give it a try. It's pretty profound.

For us, I think it's just a matter of -- again, we don't have a background in physics. I can't explain annealing perfectly, but we can use it, and it's a huge lift for our operation. Most importantly is knowing how to formulate your problems in your operation, your domain. That's the trick, honestly.

**Alan Baratz**  
*President, CEO & Director*

Yes, exactly. Lucus, thank you. Appreciate it. And in just a minute, when Lorenzo comes up, he'll talk a little bit about how we work with customers to help kind of evaluate problems, understand which can benefit from quantum and how to build out proof of technology or proof of concept to really validate them. But thank you for being here, Lucus. Appreciate it.

So I'm pretty regularly now asked about the relationship between quantum and AI. I guess, because everybody has kind of got AI on the brain these days. So let me just spend a minute talking about my view on this.

I think that AI and quantum are very synergistic. And they work well with one another in two ways. One, they're each good at different sorts of things. and you can use them together to solve a problem, letting each work on the part of the problem that it's best at addressing.

For example, you might use AI to predict product demand for the future and then use quantum to optimize the supply chain to meet that demand. So here, you have the two technologies working side by side to solve a problem, each addressing the portion of the problem that it's best at solving.

The second, quantum can help make AI model training and inference better, faster and more power efficient. We have been working for a little over a year now with a Japanese pharmaceutical company called Shionogi. They essentially trained a model to generate molecular structures for new human drugs. And they trained the model classically, and they were getting good results.

They retrained the model using our quantum computer. And what they found was that 10x, 10x more of the structures generated were well suited to human drugs. In other words, the model was more accurate. It was also trained faster and consumed less power.

So here, we have a situation where we're actually using quantum to make AI even more efficient and more powerful. And I think over time, AI and quantum are going to come together in both of those ways, the latter potentially very transformative.

And then finally, I wanted to spend a minute on blockchain. There's some very interesting work going on right now in the quantum classical blockchain arena. We've been doing some work with a small company called PostQuant Labs. They've developed a testnet for a new approach to proof of work. The proof-of-work computation can be done either classically on CPUs and GPUs or it can be done using a quantum computer.

They currently have over 18,000 people mining in the testnet and 1,600 compute nodes on the net. Those compute nodes are mostly CPUs and GPUs and then our advantage to quantum computer.

Now our quantum computer is not online all the time. We put it online for about 5 minutes a day. When it goes online, it wins almost all the blocks. In other words, it's much faster at doing the mining. It's also more power efficient. And so what we're trying to do here is demonstrate on the one hand, using a problem that can be solved by either quantum or classical, the value that the quantum computer brings over classical, another example perhaps of quantum advantage, right?

But in addition to that, showing that if you use the quantum computer, we can actually do the mining more efficiently and with lower power consumption. And by the way, it's quantum safe. In other words, a quantum computer can't break the system.

So this is an interesting new application area for us. We're quite excited about the early results we're seeing. We have started a more substantial benchmarking phase to really understand the difference between the classical and the quantum on this test net. And at some point in the not-too-distant future, we will publish those results.

Okay. So before we kind of do the first Q&A session, let me just wrap up by going back to Feynman and just reiterating. Quantum mechanics is hard. And as a result, it's easy to spew nonsense and convince people of things that just aren't real. And you always have to challenge. As I said, customers, who's the customer? How are they using it? Can I go talk to them? Scientific results, we've been able to solve this optimization problem better than classical.

Well, okay, where is the paper? Let me go read the paper and see, are they really doing that? Or is it kind of like, well, we can solve it as well as laptop can solve it, not better than classical. Always challenge.

So for us, we are focused on addressing the full market for quantum, every use case by bringing both annealing and gate model systems to market. We've proven our ability to deliver commercially viable products through our Advantage to annealing system and the technological platform that we have built around that, and we're bringing that expertise into the gate model world as we speak.

And we actually have customers that are using us today as a part of their business operations. In Q1, we announced a Fortune 100 company had signed a 2-year $10 million Quantum Compute-as-a-Service agreement for us. I can tell you, they have moved their first application in production. So it is now running on a daily basis in production, and we are working with them on several other applications. This was our first, if you like, enterprise site license.

With that, I would be happy to take some questions. Wow. Okay. Let's go to the very back of the room.

**Question-and-Answer Session**

**Sreekrishnan Sankarnarayanan**  
*TD Cowen, Research Division*

Alan, it's Krish Sankar from TD Cowen. A quick question on the dual-rail technology. At what point would the technology incorporate D-Wave's design compared to the current QCI technology it's using? And in the future, would you move from transmons to fluxonium qubits or any decision on that?

**Alan Baratz**  
*President, CEO & Director*

So QCI had a 3-year roadmap that was 8 qubits, 7 qubits, 49 qubits, 181 qubits; which is a road map that we strongly believed in, and that is the plan for the next roughly 3 years.

What we are doing now is working across the teams on what happens after 2028, how do we get to the 1,000 physical qubit, 10 logical qubit processor in 2030 and the 100 logical qubit able to process 1 million operations in 2032. That's where we'll start to see the technologies between what was D-Wave and what was Quantum circuits really starting to come together.

As far as transmon versus other, I'm going to wait until Trevor and Rob talk about the roadmap, and maybe they'll call on you to ask that question to [ Ken ].

**Matthew Cimaglia**

Matt Cimaglia, Quantum Coast Capital.

**Alan Baratz**  
*President, CEO & Director*

I know you, Matt.

**Matthew Cimaglia**

Yes, you do. So a question for you. How has the -- what was the impetus essentially for the move to Florida? And also, how has that been going along so far and some of the energy behind it? And I think lastly, the FAU Advantage2 system, what are some of your hopes and dreams out of that?

**Alan Baratz**  
*President, CEO & Director*

It's almost like Matt is a plant. So I will tell you, the first -- Matt connected with me like a year plus ago and said, "You should really move to Florida. Let me show you around." And so we got in a car together, drove around Palm Beach. He showed me all the different areas. So that's -- in sense is where it all started.

Look, we are well down the path of getting the headquarters facility up and running. Our goal is to have that up end of September, early October. And then the R&D center will take a little bit longer, hopefully, before the end of Q1 of next year. So we are well down the path of moving the corporate offices as well as getting the R&D center set up. And we're quite excited to be there.

And the relationship with Florida Atlantic is very important. I mean, interestingly, it's not just Florida Atlantic. One of the things I really liked about the environment in Florida is the universities there all work together.

So we may have a relationship with Florida Atlantic, we may be putting a quantum computer at their site. But they're actually a conduit to all the universities in the area and frankly, a variety of other really important high-tech companies that we can work with. So we can't get there fast enough, and we're really excited about it.

**John McPeake**  
*Rosenblatt Securities Inc., Research Division*

John McPeake at Rosenblatt Securities. Good to see you. So could you, not a technical question, but talk about the importance of on-qubit or on-chip qubit control, what kind of ratios you can get? Because I think you mentioned the 3 to 4 that the competitors use, and the scalability issue is really big as you get out with more physicals.

**Alan Baratz**  
*President, CEO & Director*

Yes. Okay. So it's -- sometimes we call it cryogenic control. In the annealing processors, what we were able to do was put control logic, not so much the actual control, but more how the control signals get down to the qubits so that we didn't have to have massive numbers of I/O lines coming in and lots of electronics.

We're able to put active components on the same chip as the qubits to be able to facilitate that. And so that dramatically reduced the control infrastructure, the control costs, the I/O lines that were going down into the chip. And with annealing, we are actually able to put that all in the same chip as the qubits.

With gate model, the qubits are far more sensitive. They're much more fragile than the annealing qubits are. And as a result, we don't think we can put that on the same chip as the qubits. But that bonding technology I talked about for the multichip annealing processor, that we're going to reuse to be able to have a control chip that is bonded to the qubit chip, right?

So that we still have the cryogenic control. We still have the control in the refrigerator. We're still able to dramatically reduce the control infrastructure and the number of I/O lines going down to the chip, but it's not all on the same chip. It's control chip processing chip bonded together.

So I'll probably say something that Trevor -- they'll make Trevor and Rob go [ square ] me in their chairs. But our goal is the same thing that we've been able to do for annealing. I mean, we say orders of magnitude, fewer, right? I mean, for me, if we did square root of N for N cubic, square root of N control lines, I think that would be great. But that is orders of magnitude fewer.

**Antoine Legault**  
*Wedbush Securities Inc., Research Division*

Antoine Legault from Wedbush Securities. You have some important customers in Pattison Food Group, Ford Otosan in Turkey. What would you need to achieve to replicate what you're doing with, say, Ford Otosan with Ford and GM and the big 3 automakers in Detroit? Like is it once you reach the 20,000 qubit annealing system or 100,000 qubit? Just give us a sense of what you need to do to unlock larger customers in the future.

**Alan Baratz**  
*President, CEO & Director*

Yes. So moving from one automotive manufacturer to another isn't really so much about a larger system. It's about convincing them, a, that the system can solve their problems. Now as customers that are seeing good results with our systems become referenceable, that helps that piece of it.

The other piece is, honestly, integration within their IT environment, right? So the biggest challenge to getting something into production is getting the data that's needed to formulate the problem to be sent to the quantum computer. And that ends up being, frankly, most of the heavy lifting.

I mean the customers that have moved into production, we got through the proof of concept and the benchmarking in maybe 3, 4, 5, 6 months, and then it could be another year after that to get the IT environment and the infrastructure set up to be able to accept the problem. As we go to larger companies, that becomes harder. And that's really the bottleneck. It's not so much about the technology.

**Craig Ellis**  
*B. Riley Securities, Inc., Research Division*

Craig Ellis, B. Riley Securities. Alan, thanks so much for doing the event. I know it takes a lot of work. The question goes back to the point you made about U.S. government recognition and the award. You've talked for years about your view that the government didn't appreciate what the company was doing, and now it does, clearly.

So the question is this, what are the specific opportunities that open up for D-Wave? Then, are there commercial businesses that might not have been as open to you without that endorsement that now are? And what does it take to execute there?

**Alan Baratz**  
*President, CEO & Director*

Okay. So first of all, as important as the participation in the CHIPS funding was with respect to the U.S. government endorsement, -- the thing that more caused our phone to start ringing off the hook or whatever they call it, that brings back an old image of a telephone; was when Anduril participated in our customer conference back in January. That really changed the view within the U.S. government.

And we created a new organization to go after U.S. government opportunities headed by Jack Sears, and he's got a very significant pipeline now of opportunities across many different parts of the government, mostly Department of War and Defense, but some broader than that as well.

So I think maybe even the CHIPS funding was in part as a result of that. I don't know that to be a fact, but that was very transformative for us, the fact that we were able to be successful with that use case and that they were very willing to talk about it.

Maybe one last question. Anybody on this side of the room?

**Unknown Attendee**

Matt Ross, an individual investor. Do you see D-Wave or any other quantum companies rather following the annealing path once you show what you're doing and it's successful, do you think someone else is like, oh, we should have done that?

**Alan Baratz**  
*President, CEO & Director*

Yes. I love your shirt. So -- and we didn't make that shirt. So there are some companies that are starting to experiment with it, very small, like 4-qubit. There are some neutral atom companies like QuEra that are trying to explore running an annealing protocol within their neutral atom processors. But here's what I'll say. First of all, trying to do annealing within a neutral atom or trapped ion or any gate model processor is a loser. It's kind of like if you want to do gaming on your system. Do you want to run graphics software? Or do you want a GPU, right? That's the difference between trying to actually get annealing to work on a gate model system versus having an annealing processor. So I don't think those approaches will ever be truly competitive to what we're doing with our annealing processors.

As far as some of the attempts to build annealing systems, I think we could start to see more of that, but you need to keep 2 things in mind. First of all, we've got a 20-year head start, and we're not standing still. And we had to solve a lot of really hard problems to get to this point. Second, we have a huge patent moat. I mean, we've been patenting a significant number of patents every one of those 20 years, right? Many of them still active. So it's going to be really hard for anybody to compete with us in the annealing space. Okay. Thank you all. I think next is Trevor.

**Operator**

Please welcome to the stage Chief Development Officer, Trevor Lanting.

**Trevor Lanting**  
*Chief Development Officer*

Good afternoon, everybody. It's great to see so many people here in person, and I understand there's several hundred people that have dialed in via online via Zoom. My name is Trevor Lanting. I am the Chief Development Officer at D-Wave. I lead our research and product development teams. I want to thank all of you for being here in person. I want to thank the people who are calling in online.

Over the course of this session, me -- I, along with my colleague, Dr. Rob Schoelkopf, are going to do a deeper dive on our product road map, both on the annealing side first, and then Rob will come up to the stage and talk about our gate model development path. Alan gave a lot of details on why we think we're going to be the first to deliver fault tolerant gate model systems. We're going to talk about really the exciting applications that we're unlocking with our annealing systems and where we're most excited in terms of applications for the gate model space and really hope to give you a sense of where we're going with the technology over the next several years.

Our mission at D-Wave from the beginning and continues to be developing quantum computing technology to solve our customers' hard problems and making that technology available to our customers as soon as possible. We have a dual platform approach to building technology. Alan spoke a little bit about annealing and gate model technologies and how they're complementary. Annealing addresses a wide variety of use cases. Fundamentally, quantum optimization is one of the killer apps of annealing technology, but there are some use cases or applications that annealing is not going to be able to address effectively.

Conversely, gate model systems will address a wide range of use cases. We're very excited about quantum chemistry as one of these early application areas. But gate model systems really -- and I'll talk a little bit about the growing experimental, empirical and theoretical evidence that gate model systems will not be able to attack optimization problems.

We chose to start our development platform, our development strategy with annealing systems now 15-plus years ago for several reasons. First, engineering the qubit controls for annealing systems is quite a bit easier than for gate systems. So this has allowed us to scale up our annealing systems quite a bit faster, and we're now at the scale of over 4,400 qubits in our Advantage2 annealing systems.

The second reason is that annealing systems are quite a bit more resilient to errors. Alan spoke a little bit about the models, the fact that we are driving down to minimum energy or low energy landscapes. We're actually exploiting the natural tendency of systems to want to be in low energy or ground state configurations. So we're working with nature and with quantum mechanics rather than against it.

And finally, and probably most importantly, there's a natural set of use cases broadly in that we call the class of problem called combinatorial optimization that map very naturally on to this process of trying to find a minimum energy in the landscape. Optimization problems occur everywhere. Alan spoke about some of the use cases, some of the customers that are getting value solving their problems today. Optimization, at its core, you're posing an objective function and you're trying to minimize -- come up with a variable combination that minimizes that objective function.

For example, you're an airline, you're trying to map flights to routes, crews to flights. You want to do this in a way that, say, minimizes your fuel cost or minimizes the downtime or the maintenance activities. This is a hard computational problem, and it's combinatorial. And when I say combinatorial, I mean, when you start adding variables, if you're an airline and you start adding routes, new cities to your overall network, the search space that you have to search over blows up quickly. It's not just a marginal increase in complexity, but it blows up combinatorily. And this is really where classical computing techniques and technologies are starting to struggle.

And then there's a class of problems between annealing and gate model system where we think that depending on the nature of the use case or the specific use case, either annealing systems or gate model systems, we'll be able to attack. And broadly, this is in the class of cryptography or linear algebra problems, machine learning problems. And I'll speak about some exciting research and exciting work that we're doing in the machine learning space with our annealing systems in a few minutes.

Our development strategy for our products really falls along this dual platform strategy. We are driving intensive investment in our annealing portfolio. Our current flagship annealing systems are Advantage2 quantum computing systems with over 4,400 qubits. We're hard at work enhancing Advantage2 with some new capabilities, some new protocols that I'll speak about in a second to really expand the use cases and the ways that we can use our commercial scale and annealing systems to solve problems.

But like Alan spoke about a few minutes ago, we're really focused on driving up scale for our Advantage3 technology. And the way we're doing this is by bringing together multiple superconducting integrated circuits, interconnecting them to form larger qubit fabrics, larger annealing fabrics to unlock larger scale. And larger scale will be able to allow us to address a broader set of use cases.

We're also taking the Quantum Circuits road map. Alan spoke about that a few minutes ago. In the near term, we're really focused on developing and delivering an increasing set of dual rail processors starting this year with a 17-qubit dual rail processor, next year, increasing that to a 49-qubit processor and then the year after that, 181-qubit dual rail processor.

Now the goal with this series of increases in processor sizes to show fundamentally the advantage of the dual rail system in quantum error correction and to allow our customers to start exploring algorithm development with this new capability with the high fidelity, high-speed dual rail systems as soon as we can make them available.

We're also making all of our technology available via our Leap cloud platform. We introduced a quantum classical solver, the Stride solver, and I'll say a little bit more about the Stride solver in a few minutes in 2024, and we've been intensively investing in the capabilities of the Stride solver can support up to 2 enterprise-grade optimization problems with over 2 million variables.

As we develop the dual rail technology, we are making that dual rail technology, first, the simulator and then the dual rail technology itself available in Leap. And then going forward, we're actually seeing quite a bit of interest. And my colleague, Lorenzo Martinelli, will speak a little bit about the on-prem interest in this interest from high-performance computing centers in integrating quantum systems, annealing systems and eventually gate systems into their overall computing infrastructure. And so this is an important part of where we're driving with our technology, what is the best way to integrate our systems, annealing CPUs and our gate model systems into high-performance computing centers.

Our flagship annealing quantum computing product is our Advantage2 annealing system. This is our sixth generation of annealing system product. We focus on 3 key pillars when we were developing Advantage2 to drive performance. The first is qubit connectivity. Qubit connectivity, as you increase it, you're able to actually represent more complex, more complicated optimization problems and map them directly into the fabric of the annealing processor. With Advantage2, we've gone to 20-way connectivity. That means in the fabric of the processor, every one of the qubits is tunably coupled under user control to 20 other devices. This enables you to pose and solve more complex problems with the technology.

The second thing we focused on was qubit coherence. Now coherence is critical for driving faster time to solution. And over the last several years, we've been able to fundamentally make a connection between higher coherence architectures and faster time to solution. We've reengineered our fabrication stack, including materials and processes to produce the Advantage2 integrated circuits, and we're actually seeing more than double the coherence times in the processors. And this is important. This drives dramatically faster time to solution for hard optimization problems.

And finally, we've increased the energy scale. You can think of energy scale as sort of the strength of the interactions that we can actually represent between the qubits or how precise or how high fidelity you can represent these hard optimization problems in the fabric of a processor. Increased energy scale delivers higher quality solutions. So we've pushed hard on all 3 for the Advantage2 technology.

Our Advantage2 systems are accessible today through our quantum Leap cloud platform, and they're available for customers that want on-prem delivery, an on-prem Advantage2 system. And like Alan said, they support enterprise-scale hybrid applications. Our Stride solver is backed by our Advantage2 QPUs and our Stride solver can support enterprise scale optimization problems with up to 2 million variables and constraints.

I want to say a few more words about coherence and the connection between coherence and performance. Coherence in general is what quantum computing technologies are harnessing to deliver computation utility. And as we've driven up the coherence in our processors, we've seen better performance in terms of faster time to solution for optimization problems. I'm illustrating this in the graph on the right, where I'm showing some optimization benchmarking data comparing Advantage2 and Advantage on a fairly standard hard benchmark class of problems that we use internally as a report card or a test of how well the technologies are working.

Shown in the orange are data from Advantage2. Shown in the blue are data from Advantage. And what I'm plotting along the y-axis is relative error. So you can think of this as distance to the optimal solution. You want to be driving down to 0, to 0 relative error. Along the X-axis, I'm plotting anneal time. So how much time you're using per cycle to actually do the annealing process, the calculation.

You can think of this as computational effort, how much time I'm willing to spend to get an answer to the problem. You can see that for Advantage2, compared to Advantage, uniformly across all of the annealing times is outperforming Advantage, often by an order of magnitude or more in terms of the relative error that we can drive down to.

But as importantly, you can see that if you pick a relative error, say, a few parts per hundred and just draw a line across the chart to compare Advantage versus Advantage2, the increases in coherence are not just marginal. They're not just 20% or 30%. But in some cases, for some relative error targets, you're seeing orders of magnitude reduction in time to solution. And this is the power of delivering more coherent processor technology and more coherent qubits in the fabric of our annealing technology.

Alan spoke about our quantum supremacy demonstration. Two years ago now, we posted on to the archive our preprint beyond classical computation and quantum simulation, where we took the Advantage2, in that case, it was even a smaller scale prototype of Advantage2, this was before we released Advantage2, and we studied how well Advantage2 could actually simulate the properties of a magnetic material or separate magnetic materials that were undergoing phase transitions and study their dynamics.

And we worked with a team, an international team of experts and the best classical methods for solving this problem. We actually consumed tens of thousands, I think, up to 100,000 hours on the Frontier supercomputer at Oak Ridge. And we established this classical scaling, how hard this problem was for the best known classical methods. And there's a massive gap between what the classical methods can do and what we can do with our Advantage2 processor.

Alan spoke again a few minutes ago, we can solve this problem in 20 minutes, and we're projecting for the largest problem sizes that we studied would take up to 1 million years on Frontier. We're harnessing quantum coherence to deliver computational advantage. In this case, it is beyond classical. So this material simulation calculation just can't be done with classical computers.

So I want to dig a little bit into annealing's long-term advantage and optimization because you can ask the question, and Alan asked this in his keynote, well, why not use gate model systems, including today's gate model systems to solve optimization problems. Well, there's a growing set of evidence, both empirical and theoretical that suggests that annealing systems will always have a leg up our long-term advantage over gate model systems in solving optimization problems.

In the near term, you can actually just horse race the technologies today against each other. And in fact, there's a large number of empirical studies I'm pointing to at the top of this chart, a set of data from a reset of researchers at Los Alamos National Labs, where they did exactly that. They studied our -- in this case, our Advantage annealing system and compared it against some emerging gate model platforms. And what they found was the Advantage system could solve optimization problems at a larger scale to higher accuracy to lower residual energy closer to the optimum at orders of magnitude faster execution times than the gate model platforms. There is a fundamental gap in problem scale, solution quality and execution time between annealing systems and gate model systems for optimization.

But to be fair, you could say, okay, well, what if gate model systems, as they scale, like if I hand you a scaled up fault-tolerant gate model system, what about that system? How can it compare in solving to -- how can it actually -- how will it do in solving optimization problems? And I want to point to some work that actually came from Google's Quantum applications team, where they actually studied several gate model algorithms, and they did a very, very detailed analysis of the overhead required in running quantum error correction.

And the conclusion was that unless the algorithm that you're running on your fault-tolerant gate model system has a steeper than progratic scaling over classical approaches, all of the benefit from running on that fault tolerant system is erased by the overhead of fault tolerance.

Now it's not to say that there's a lot -- there aren't a lot of algorithms that have very steep advantage over classical approaches, exponential advantage. Optimization is not one of them. And this is some recent benchmarking data that my colleague, Andrew King, who leads our performance research team, ran on our Advantage and Advantage2 systems on a slightly different flavor of optimization. In this case, it was a response to an initial paper from IBM on multi-objective optimization. Here, it's a more complicated optimization task. You're actually given a range of objective functions and you're asked to optimize over that portfolio of objective functions.

What I'm showing in the plot here are in the blue and the orange are data from our Advantage2 and Advantage system on how well we do at that portfolio of optimization, that multi-objective optimization against the red, which is empirical data from the IBM system. And you can see that we're orders of magnitude, up to 1,000x faster in terms of that performance differential, in terms of the execution time for this hard multi-objective optimization function.

Also interestingly, in the green, it shows a perfect noise-free simulator of how well that gate model system could do. And even in that case, we're still opening up the gap and have opened up the gap by orders of magnitude. This is just more evidence that annealing systems have this long-term advantage in hard optimization problems.

Alan spoke about our annealing scaling road map that we're incredibly excited about. With the Advantage2 system that we launched in 2025, the fabric of our processor at the core is a single superconducting integrated circuit that contains just over 4,400 qubits. We're hard at work on packaging technologies, superconducting interconnects that would allow us to take multiple superconducting integrated circuits and assemble them into a larger processor fabric and tile out this processor technology to grow the scale of the systems.

Why do we want to do this? Well, as we grow the number of qubits, as we grow the qubit count, we expect to be able to unlock broader utility in quantum optimization along with a lot of other use cases. And so we're quite excited about scaling the technology up to, first, 20,000 qubits, with the eventual goal of hitting 100,000 qubits. But the other piece of this is scalable control.

We want to do this without blowing up the number of control lines that go into our cryogenic enclosure. So like Alan said, we have just recently completed a design for some prototype scalable I/O that should bend and reduce the amount of lines that we need to control our devices by even more than we actually have right now. And this really should -- our goal is to get to this technology node without substantially growing the number of lines that need to go into our cryogenic enclosure.

I spoke a little bit about some work we're doing with Advantage2 on new protocols, broadly unlocking what we're calling analog digital quantum computing, but specifically capabilities, new capabilities that we're making available in our commercial scale annealing systems. And again, specifically, the ability to target per qubit in situ excitations in the fabric of the processor and then the ability to read out the state of the qubit in an arbitrary basis.

Why do we think that these 2 capabilities are important? Why are we actually putting some resources into this development? Well, fundamentally, we think that these 2 capabilities, and we've actually seen this with some initial results, should unlock a major expansion in our ability to do magnetic material simulation. So we're incredibly excited about these tools to basically unlock our ability to simulate the behavior of the magnetic materials at even larger scale and more complicated lattices.

But looking forward, the ability to read out in an arbitrary basis will allow us to pull much more complex rich distributions from our annealing GPUs. And we have some great ideas on how this could actually really drive more utility in both machine learning and blockchain applications. And I'll speak about these 2 exciting emerging application areas in a minute.

But I want to highlight some of the data that I and the team are particularly proud of, which is basically a demonstration of this excitation and these readout protocols within the fabric of our Advantage2 systems, where, in this case, in this plot, we've arranged a subset of qubits in the Advantage2 processor, a 1D chain in a line, 120 qubits, have a uniform coupling between these qubits, and then we deliver an excitation pulse to the middle of the chain, and then we watch that pulse coherently propagate both in time and space across the chain and over time.

You can see here, Qubit index on the plot really shows where in the chain you're seeing that excitation and along the Y-axis, and along the X-axis is basically a delay. You can think of this as an evolution time. So you can see these coherent oscillations. This excitation get delivered to the center of the chain and then propagate coherently exactly like you'd expect from theoretical predictions.

I want to speak a little bit about our Leap cloud platform. We're incredibly proud of the Leap cloud platform. We launched it in 2018, and it's a means by which our customers access all of our technology, both our hybrid solvers and human CPUs and very shortly, our dural rail technology. We make available to our customers a set of tools in the Ocean software development kit. This is an open source software kit written in Python, and it's meant to make it extremely easy for formulating hard optimization problems for our technology. And we have a growing set of tools for researchers that are really interested in using our technology to explore new use cases and new algorithms.

The Leap cloud platform has high-performance, high-availability APIs, the suite of quantum classical hybrid solvers and a dashboard that allows you to kind of monitor your usage and really keep track of how you're using the Leap cloud platform and the solvers that you have available to you. And at the core, we have fast fiber connection from the Leap cloud platform to each one of our annealing systems. Both Advantage2 and Advantage are available. We have 4 production systems online available through our Leap platform today.

But this isn't a research platform. This is engineered to support business, to support enterprise-grade operation. This is a platform that is really singular in the industry in terms of its performance. We've engineered to be high availability. We want the solvers to be available to enterprise to business to solve their problems at any time. We don't want the solvers to come in and out. This is high availability, and we've had over 99.9% availability since we launched Leap in 2018.

It's a real-time platform. There's no extensive queuing. There's no need to wait. There's no need to reserve your time ahead of time. You submit a problem to our Leap cloud platform, you get an answer back in subsecond response times. We have SOC2 Type 2 compliance to give our enterprise customers the assurance that we have high security and that they can trust the platform to be there and to be good stewards of their data.

And finally, we're actually offering -- we're putting our money where our mouth is. We're offering service level agreements to our enterprise customers to basically guarantee the uptime, the availability of the platform for their operations. And I want to say this is, again, differentiated, and I think gives us a very strong advantage in the quantum computing marketplace. And we've, from the ground up, engineered this to support business.

One of the flagship solvers that is currently available in the Leap Cloud platform is a Stride hybrid solver. We launched Stride in 2024. And Stride at the core is combining classical and quantum resources together to solve enterprise-grade optimization problems. Stride can support up to 2 million variables and constraints and is really starting to deliver differentiated performance on a growing wide class of use cases. Something that we're particularly excited about that we've introduced into the Stride solver several months ago is surrogate modeling, the ability to import a machine learning model directly into your optimization workflow.

So why is this important? Well, going back to one of the examples that Alan spoke about where you may want to use a machine learning model to predict demand if you're a retailer, and then optimize that demand using our optimization solver or engines. And it's sometimes very hard to come up with a closed mathematical form for that data set for that demand. So what you can do is train what we call a surrogate model, machine learning model that can actually serve as a model for that demand and then embed it directly into your optimization workflow. So we're actually very excited because this is really enhancing the behavior and the ability of the Stride solver to open up a growing set of use cases.

And one particular example of a hard optimization problem that we benchmarked the Stride solver against, I'm showing in the graph on the right is a problem called satellite placement. And this is actually a fairly hard problem because there's a discrete components like where are you putting satellites in a particular orbit in terms of an ordering operation. And there's also a continuous component. How do we actually do the fine-tuning of where those satellites go with the overall objective of minimizing my gap coverage.

I want to actually have no gaps in my satellite coverage in terms of the ground coverage. So what we're showing is benchmarking data from the Stride solver along with several other solvers, traditional solvers for solving this problem. We're on the Y-axis and plotting median gap. So you can think of this as distance from optimal, you want to drive down to 0 gap as a function of the number of satellites in your constellation.

So different -- all the different run times and comparisons for this problem class, the Stride solver is getting very close to or is getting the optimum gap driving to 0 gap and is outperforming the other solvers.

I want to switch gears in the next minute or 2 and talk about 2 emerging application areas that Alan spoke a little bit about in his keynote, quantum AI and blockchain. In quantum AI, one of the things that we're particularly excited about is directly using our annealing CPUs to enhance and to improve machine learning models. Now at a high level, you can think of a machine learning model as the training of a model and construction of the model as an exercise in compression. You've got a very large data set. You want to learn the structure of that data set, you want to lower the dimensionality and come up with as compact a model as you can to represent your data and then use that model to generate new high-quality versions of the data.

Our vision for how to integrate our annealing CPUs directly into this process is to go through an encoding process where we take our initial data set and we use a classical neural net and encoder that then map that data set into a compact lower dimensional latent space. And in that latent space, our annealing CPU learns the best structure in that latent space to compress that data and to represent that data in as few variables as possible. And at the output, you basically take samples or new samples from that latent space to generate new versions of your data.

Now the critical thing here is that you want to train the QPU simultaneously with your encoder and decoder neural nets. So when you do that training simultaneously, the QPU is able to learn the best distribution, the best sort of shape of that latent space to compress your data to high quality and deliver a particular sort of objective function in terms of what you're trying to train towards. So then when you're actually prompting the QPU or prompting your model for new versions of the data, you're sampling from the QPU and then decoding new versions of your image and new versions of your data set.

So where do we think that there's long-term value in this overall structure? Well, the first is that the QPU is incredibly good at learning complex distributions and the QPUs are incredibly good at generating high-quality samples quickly. And in fact, there's some growing evidence that sampling -- that core sampling capability, generating novel samples from a learn distribution, CPUs have an advantage of our classical approaches. And so we're harnessing that directly and wiring that into the generative AI models.

And a great example is what Alan spoke about a few minutes ago. This is a drug discovery application where the data set instead of images is a molecular data set. And we use the QPU to learn the structure of this molecular data set. And we saw -- we were able to compare this quantum classical data set to a classical-only version of the model.

And what we found is across 3 different metrics, the quantum classical model outperformed once trained, outperformed the classical model, both in the metric of molecular weight. It was able to deliver high-quality samples that were smaller and therefore, more valuable because they're easier to test and develop, a metric called lipophilicity, which is a measurement of sort of how sort of fat soluble the molecule is, and we could get much better lipophilicities with the quantum classical model.

And then finally, something called drug likeness. The structures were sort of best suited for kind of human drug candidates. Across all 3 of these metrics, the quantum classical hybrid model outperformed the classical model. Again, the key view here is providing discrete samples from a complex distribution and then those samples are translating to better outcomes, to better drug candidates.

The second emerging application area that we're quite excited about is Quantum blockchain. So Alan spoke about post-quant labs. This is a partner that we're working with on a quantum classical blockchain and the testnet is currently operating. And actually, there's been an immense amount of interest across the globe. This is kind of a map of the different participants and the kind of the compute nodes that are currently online as part of this testnet. There's over 18,000 users of the testnet and over 1,600 compute nodes currently running in testnet phase. And when the QPU is on, our Advantage2 CPUs are always available in Leap, but we're making them available for the testnet up to 5 minutes per day. And when those CPUs are on, they're completely dominating the mining rewards. So like Alan said, we're moving to a phase where we do a detailed benchmarking study where we really show the performance of the QPU as is competing with classical miners, a set of GPU and CPU miners to win token rewards.

But longer term, we're very excited about fundamentally a quantum-only proof of work. We published a research paper about 2 or 3 months ago, a peer-reviewed paper that demonstrated both a proposal for quantum proof of work along with the demonstration using 4 production Advantage and Advantage2 systems that were online distributed through North America. And we showed that we could run a stable blockchain with a quantum proof of work at the core indefinitely using these annealing GPUs.

Why is this important? Well, from the ground up, this is a quantum-safe protocol because the fundamental proof of work for this blockchain is quantum, there's no way it can be spoofed classically. So it's quantum safe by construction. The other thing that we're quite excited about is that we've estimated that blockchain supported by this particular quantum proof of work could be 1,000x more energy efficient, orders of magnitude more efficient than a classical analog of a quantum proof of work blockchain. So fundamentally, you have a potential for a quantum-safe technology that is substantially more energy efficient.

I'm going to switch gears now and spend a couple of minutes kind of talking a little bit about our gate model program. And then I want to invite my colleague, Rob, up to the stage, and he's going to do a deep dive on the dual rail technology and where we're going with the gate model program.

So why are we developing gate model systems? Alan did a fantastic job of motivating it. We really see annealing and gate systems as complementary. We want to address the full addressable market, the full TAM for quantum computing technology. We see use cases that are complementary to the annealing systems, and I'll speak a little bit about which use cases we see as really emerging as important in the near term for gate model technologies. And we have a road map for delivering 100 logical error-corrected qubits. And we think that this will unlock early commercial utilities with gate model systems.

So why now? Well, the merger with Quantum Circuits is bringing a leading superconducting qubit technology to D-Wave. We have cryogenic control that allows us to scale superconducting systems. We can use our 15-plus years of experience with engineering this control and apply it to the dual rail technology. And the combination of these 2, we think, will allow us to win the race to be the first to deliver fault-tolerant systems to the market.

Alan spoke a little bit about the TAM. I won't get into the numbers in detail, but I just want to double-click into some of the use cases that we're most excited about. I think some of the likely earliest use cases are broadly in the novel drug discovery, novel materials discovery domain. So this is broadly quantum chemistry, pharmaceuticals, trying to build your molecules and measure them ahead of time with your gate model systems before building in the lab. We see a massive opportunity in the near term. This is a huge space and is a big segment of that TAM that Alan spoke about. We see value beyond our annealing system for gate systems as a scale and really doing heavy lifting for machine learning use cases.

There's a broad set of use cases in the finance industry on sort of solving hard differential equations to drive sort of better performance for portfolios, better trading outcomes. We see this as probably needing larger systems, so maybe later-stage use cases, but an incredibly large market that we've identified.

And finally, there's a space of cryptography. So this algorithm really was the algorithm that helped launch the birth of the quantum computing industry. Gate model systems are going to be able to start attacking encryption as they scale out. All of these use cases here are motivating and the breadth of them are really motivating our investment in building gate model quantum computing technology.

So with all the pieces that we have in front of us, we're ready to scale and win the race. We have an industry-leading qubit technology that Rob will speak a little bit more about. This technology and its current performance gives us an achievable path to fault-tolerance systems with an order of magnitude fewer physical qubits required to encode our logical qubits and get to fault tolerance.

And finally, our experience with cryogenic multiplexing, our scalable manufacturing and our experience with cryogenic -- reliable cryogenic platforms is opening up the path to a commercial gate model technology that's reliable, that's production grade that we're excited to put in the hands of our customers as soon as we can.

With that, I want to welcome Rob to the stage, and he's going to do a deep dive on where we're going with the gate model technology.

**Robert Schoelkopf**  
*Chief Scientist*

Thanks, Trevor. Yes. So hello. It's nice to be here this afternoon. Thank you all for coming and for your time. So yes, I'm going to begin here by describing in simple terms, what is a dual rail qubit and why is it so different?

So the first thing you need to know is that it's a completely different paradigm. It's something we call an erasure qubit, which has the ability to detect errors kind of built into the hardware. And it's shown in kind of cartoon form here. It's a composite object that's composed of a few simple parts, some of them being the Transmons, which we actually developed in our lab maybe 20 years ago at Yale that or what everybody else uses, but they're really just used here for the input and output. It's to create excitations in the heart of the system, which are a pair of microwave cavities. And what we do is we store a single microwave excitation in those cavities and it's the stability and long lifetime of those cavities, which make this the most coherent superconducting qubit that's out there in the marketplace.

So let's talk a little bit about how in the dual rail, we store information and process it. So the logical states of this dual rail qubit are those in which a single microwave photon excitation that sort of cellphone frequencies of the electromagnetic field is shared between these 2 microwave cavities. And you can have the photon existing in the left cavity, let's say, call that logical 0, or it could be in the right cavity, call that logical 1, and then we can manipulate that information by sending an electrical signal to another superconducting device called a coupler that allows us to exchange this exitation without losing it between the 2 cavities. That also allows us to create states like a super position, which is 0 plus 1, where the photon is actually shared at the same time between these 2 superconducting boxes or cavities.

Now what's special about this dual rail and this erasure qubit is that 90% of the errors, the dominant errors are just those in which after a sort of a millisecond or so, the exitation is lost. And that leaves us in this unique state where both of the cavities are empty. And so I like to say sometimes that the dual rail has a 0 in a 1 like regular qubits, but it also has this third state, which basically flags that there's -- it's invalid. There's been an error, and you can use that to either boost the performance by rejecting those shots or to give you extra information that dramatically aids in the full task of error correction and making that more efficient.

And so this ability to detect the errors is really one of the key capacities. It's also something which is interesting for algorithm developers and designers because it gives you more information than you get on a traditional kind of machine.

We've talked about how this dual rail is really unique in the space in its performance characteristics. And I already mentioned that we can detect 90% of the errors and boost the fidelity. So we can have 2-qubit operations with something exceeding 39s, 99.9% fidelity. That means an error only occurs about 1 in every 1,000 operations. And that's the kind of fidelity that you usually don't associate with superconducting platforms.

And so this chart sort of shows 2 of the key metrics, right? One is the fidelity on the vertical axis and the gate speed on the horizontal axis. And in the quantum space, very broadly, there are kind of 2 main types of qubits. There are trapped ions and neutral atoms, I call them the God-given qubits, the sort of natural qubits they will tell you, microscopic objects that usually have higher fidelity, but are also associated with much slower operation times on the order of milliseconds.

The other category is solid state, mostly superconducting qubits, which are very fast, but are usually noisier and more error prone. So they're kind of on the lower right. And with the dual rail and our ability to detect the errors, we retain the manufacturability, the scalability and the very high speed, microseconds rather than milliseconds of superconducting systems, but we're able to boost the fidelity and the performance and get sort of the best of both worlds.

Okay. So where are we today in gate model computing, and where are we going? So to unlock the full potential, as we've already discussed this afternoon of gate model computing, you really want to be on the right in this fault-tolerant era. In that realm, you are using something called logical qubits to dramatically suppress the errors of the computer below those of the physical pieces to extend operations and make much more complicated and more powerful computations. Maybe you want to do 1 million computations, which is 3 orders of magnitude lower error rates than you can get with physical qubits today.

Now most of the industry is in what we call the NISQ era on the other side of the chart, NISQ, standing for noisy intermediate scale quantum. Here, you just have physical qubits. You can do maybe tens or hundreds of operations and the use cases and the applications are somewhat limited. At D-Wave, we're the first to be in what I like to call the post-NISQ era. So we have this error aware feature of our machine. The NISQ machines just give you out a result. It's mostly noise, and your job is to try and figure out what the quantum computer or the quantum algorithm was trying to tell you.

But with our error detection, you can either reject shots that have noise and keep only the pure shots or you can learn how to do other sorts of things. Now an important point here is that really, this is learning how to program the quantum computers of the future. Even when we're in the fault-tolerant regime, we're going to have to deal with errors. You're always going to want to run a computation a little bit longer than you can, given your amount of error correction. And so you will want to use the information of error detection on top of error correction. But in this post-NISQ era, we're also very excited because now we really can attack the problem of error correction and doing so efficiently to get us into the fault tolerant era.

Okay. I want to do my version of explaining this chart, which Alan already presented and explain for you again kind of the general way that error correction works and what efficiency means in that context. So the general idea of error correction is that you will construct out of some collection of physical qubits, the number of which is sort of the horizontal axis on the bottom, you will construct a logical qubit that redundantly encodes one usable bit of quantum computable information in that distributed among that collection of physical qubits.

And the idea is that the error rate now shown as the sort of difference from one, right? So lower error rates here being smaller and smaller errors or longer and longer computations is shown in a logarithmic scale on the vertical axis. And if, and only if, your performance of the elements is good enough, then the idea is that you can increase the amount of redundancy, you increase the number of physical qubits making up your logical qubit or you increase what's called the distance of the code. Those are the numbers going across the top 3, 5, 7, 9. And for each increment in the code, you get another multiplicative factor that reduces the errors. This factor is the number called lambda or the error reduction rate.

And in conventional superconducting systems, they've been working on error correction for 15 years or so, and they've been able to get now finally to a lambda of about 2, meaning that you halve the error rate. But with the performance we've observed already in our prototype systems with the dual rail qubits, we anticipate that this lambda factor can be as high as 10. And that means that every time I increment the code, I'm going to reduce the errors by another order of magnitude. And so let's say, I want to get to a part per million, I want to run a computation that's 1 million steps long. On a conventional machine, which is this upper graph, you'd have to go way out to the right with a very large distance code and a massive number of physical qubits making up your logical qubit, and you have to wait for that scaling to happen. But on the other hand, with the dual rail, you can get down to parts per million with maybe only a few hundred qubits. And the near-term part of our road map is we're building these systems to do distance 3, 5, 7 and 9 and to demonstrate this high value for lambda and suppression of errors down to this kind of hopefully part per million level.

Okay. So that's something that now makes sense to scale in gate model. And what do you need to do in order to be able to carry out that scaling? Well, one of the challenges is for a still large number of qubits for a usable computer, you have a large number of signals and wires that need to be brought down into the cryogenic environment.

And so a solution for that is to use some amount of cryogenic control and logic and to be able to sort of multiplex and bootstrap your way to using one wire to control many qubits. And D-Wave knows how to do this. They've done this in terms of scaling the annealing processors to this point. And so we're very excited about being able to now combine the technology of the dual rail that we had developed at Quantum Circuits with this knowledge base and intellectual property that D-Wave has. And so that's the other ingredient in scaling efficiently.

Another important aspect of scaling is to have systems which are mass producible and reliable and manufacturable. And the dual rail, although it's a different concept in superconducting qubits, it uses very much the same kinds of materials and fabrication processes. And so we're able to adapt the -- some of the techniques from the semiconductor industry and various foundries in order to be able to engineer these systems and make more larger scale and more useful machines.

This is, again, repeating a kind of table that we had before, emphasizing kind of speed and performance or -- but for logical qubits. So we want to move the industry to starting to talk about what your error correction really does and what's the performance of your logical qubits. And so you still care about speed. Now in your error-corrected machine, it's the time it takes you to measure one round of error correction that is basically the basic clock speed, and that's a small multiple of the individual gate speed, it's less than 5 microseconds for us and for superconductors. And for trapped ions and neutral atoms, it's many orders of magnitude longer, milliseconds or even more in some cases.

And again, the state-of-the-art is really only to be able to produce marginal gains in your error correction, not these lambda factors of 10. And so that's the second column, this important error reduction rate, which tells you, again, how fast you're able to suppress the errors or how you're able to make a high-performance logical qubit with over an order of magnitude fewer actual physical elements.

So we're very excited to be talking about our gate model road map. And it's divided here into 2 eras. The near-term era, this post-NISQ era that I mentioned, we are delivering over the next 2.5 years or so a sequence of these dual rail processors that are based on our existing prototypes and deliver the first error correction layered on top of the error detection that's built into the qubits.

And as we go from the 17, which can do a distance 3 code to the 49, which does distance 5, we expect to see one extra multiplicative factor of lambda in the error reduction factor. So this 20x is the net error reduction. And then with the 181, we can do distances 7 and 9 and get 2 more of those factors to get to error suppressions that are overall more than a factor of 1,000, we hope. And so that is the near-term road map.

And then really, when we have this proof in hand of the error correction efficiency, we really have a blueprint for how to scale into this fault tolerant era rapidly and efficiently. And so we're targeting in 2030 systems with of order 1,000 physical qubits which would house 10 logical qubits, but at error rates of perhaps a part in 10 to the 6, allowing millions of computations on those qubits. And then with just another factor of 10 increase in the number of elements to get to 100 logical qubits with millions of gates, which we anticipate could bring us to the sort of initial quantum utility for these systems.

Just drilling down a little bit on this near-term road map. I've already mentioned how the 17, 49 and 181 are very useful proof points for error correction. But also, they allow us to begin having people use these systems and learn how to program in these new error-aware ways. So they're dual-use. And so you can use it as 49 physical qubits, but with the boosted fidelity that you get that's beyond what ordinary superconducting qubits can yield.

Okay. So that's what I wanted to tell you about. I think with this acquisition of Quantum Circuits and joining forces with D-Wave, we're really in a very interesting place where we're ready to scale and win the race to fault tolerance. So we have the most performant, highest coherence and best qubit out there, the dual rail. It has these unique capabilities that allow you to do error correction much more efficiently. That extra information, the higher performance allows you to deliver logical qubits with over an order of magnitude fewer elements. And then by utilizing the already developed techniques for multiplexing robust cryogenic systems and mass-produced manufacturability in foundries, we're really excited about being able to bring to market these series of machines.

So with that, I think Trevor is going to join me, and then we'll take a few Q&A after one more slide.

**Trevor Lanting**  
*Chief Development Officer*

Thanks, Rob So, again, we are focused on a dual platform strategy because we see annealing and gate systems as complementary. Rob talked about our path to the fault tolerant era and the path actually unlocking utility with gate model systems and bringing to the stage where they're commercial alongside our current commercial annealing technology.

**Trevor Lanting**  
*Chief Development Officer*

So with that, I think we have a few minutes for Q&A, I think. Thanks. So John?

**Unknown Attendee**

Trevor, I appreciate you putting that slide up last. I had a question about that one before. The either/or annealing versus gate model, it's very interesting. I really haven't seen you talk about that in detail before. How do you delineate those problems, those very important problems, machine learning, cryptography, drug discovery about which ones D-Wave might be able to handle versus gate model, the size of the problem? Is it the system road maps? Because that could bring that -- those opportunities 5 years forward versus waiting for gate model. So I'm curious about that.

**Trevor Lanting**  
*Chief Development Officer*

Yes. I mean that's a good question. There is that overlap in the TAM, like when Alan showed the TAM slide, there are some of those areas where we expect annealing and gate systems to address and broadly in the area of cryptography and linear algebra. In fact, I spoke about sort of what our near-term plans are in quantum AI, where we're really using our annealing systems as critically important sampling engines to make machine learning models potentially smaller, more efficient, make the training faster and to make inference faster.

And so we actually see real near-term wins with annealing architectures. But there are some algorithms that are fairly exciting, including one that was proposed by the -- again, the Google Quantum Applications team, where they show that once you have error-corrected logical qubits with a qubit count in the 50 or 60 there's actually a signal processing algorithm you can run to really allow to compact data sets for machine learning applications. And I can forward you the link to that paper. So that's an example of a machine learning use case that is emerging as important that could be enabled by gate systems. So the short answer is I think we're going to learn a lot over the next several years, but we're actually attacking some of these use cases with our annealing systems today.

**Unknown Analyst**

Konrad, Morgan Stanley. Thank you for these very informative presentations. Really an infrastructure-related question. Can you address the cryogenic environment? Because the cooling systems operating at absolute Kelvin like outer space at all really hits the bottom line. And as much as you can get energy efficiency through rapidity, that is also a critical factor. So just a little bit of color on that subject.

**Trevor Lanting**  
*Chief Development Officer*

Yes. I can take it and you can add commentary. So cryogen -- it's true, we need to cool our technologies, both gate and the annealing are superconducting technologies that need to be at millikelvin temperatures to be in cryogenic enclosures. But I see cryogenics as a solved commercial problem. We buy off-the-shelf fridges from vendors for both our annealing and our gate development. Those fridges are high reliability. We've actually spent at D-Wave 15-plus years engineering out all of the issues that happen when you try to run these systems for years at a time. And we've had systems in customer data centers for almost 5 years running continuously with no interruption.

Our current systems, we are drawing about 12 kilowatts of power. And that for our annealing systems, we've had the same cryogenic enclosure for 6 generations of annealing system. And so that overall 12 kilowatts of power is a fixed power cost over multiple generations. So it is true that they do consume power, but I really don't see this as a cost driver for the technology. And in terms of overall complexity, I see this as an off-the-shelf technology that is -- basically is commercial today.

**Unknown Attendee**

So Trevor, what do you think we'll need for the 100,000 qubit system?

**Trevor Lanting**  
*Chief Development Officer*

A slightly bigger fridge, but not much bigger. Still something that we can build off the shelf -- we can pull off the shelf.

**Robert Schoelkopf**  
*Chief Scientist*

Good point, not much bigger.

**Alan Baratz**  
*President, CEO & Director*

And what you need is a different size and shape of the enclosure, but not necessarily more refrigeration. So you can still adapt kind of the conventional machines that are out there.

**Robert Schoelkopf**  
*Chief Scientist*

I mean I think these comments that superconducting requires a football field size system and $1 billion is nonsense. That's part of the hype. It's just nonsense.

**Unknown Attendee**

Just a quick question on -- there are a ton of road maps out there, a lot of different companies with big goals. I wanted to just get your thoughts on -- and it was great to see you put out the gate-based road map this morning. But in a scenario where the other people do what they say they're going to do. What would be your plan to compete with them, let's say, in a situation where someone else had a really fault-tolerant computer in the market before yours, and you have the leverage with the annealing side, but how would you plan to compete then?

**Trevor Lanting**  
*Chief Development Officer*

That's a great question. What Rob showed in terms of our road map to fault tolerance, I consider a credible, achievable road map but still aggressive. So there's still a lot that we are doing to integrate the multiplexing, the cryogenic control, and we're needing to scale up the technology. So I see this as a credible, achievable but aggressive road map. I see some of the other road maps as I'd be very excited if some of the other efforts actually nailed exactly what they're saying on those time lines. But I think we are really focused on how to actually do this properly and achieving this in a realistic way.

**Robert Schoelkopf**  
*Chief Scientist*

So I want to say just a little bit more. Okay, let's suppose for a minute. Let's suppose for a minute that we get a scaled error corrected neutral atom or trapped ion system 2 years ahead of us. Okay. And then 2 years later, we have a system that's 1,000x faster. I don't care about the 2 years, right? I mean, at 1,000x faster, they're out of business. And let me just kind of give you a data point to hang your hat on.

I think we're all kind of intrigued, maybe even excited when a few weeks ago, Google said, "Hey, we can break the Bitcoin protocol with 500,000 superconducting qubits and we can perform the computation in 9 minutes." They actually didn't say we can perform the computation in 9 minutes. They just said we can break it with 500,000 qubits. Then John Presco from Caltech and [indiscernible] came out and said, "Well, with neutral atoms, we can do it with only 10,000 qubits." Okay. Good. 10,000, a lot less than 500,000.

Go read the paper. How long will it take to perform that computation with those 10,000 qubits? Months, not 9 minutes, months, okay? That doesn't break the protocol, right? Because you you're not going to win a block if it takes you months to perform the computation. Google at 500,000 qubits would win it. So the point is once we get superconducting anything, we think it will be us because we have that error correction advantage, the ability to error correct with far fewer logical qubits. But once we have superconducting, it's game over for everybody else. Nobody is going to want a slow quantum computer. It's just physics.

**Alan Baratz**  
*President, CEO & Director*

And the point is we scale faster. Our capabilities will go faster as the number of qubits increases. So that also helps.

**Quinn Bolton**  
*Needham & Company, LLC, Research Division*

Quinn Bolton with Needham. Trevor, I just wanted to follow up on the machine learning example you gave where you mapped to the latent space. How broadly applicable is that? The work that Shionogi did seems like it's given them an advantage. It certainly seems like it could give others advantage. So are there limitations to that approach? Or do you see pretty wide interest in...

**Alan Baratz**  
*President, CEO & Director*

Yes, that's a great question. We're actually doing some internal development on a diffusion-based model. So where the latent space is able to act as a prior for image generation for image data sets. But we chose that basically because there's a lot of image data that is kind of publicly available and a lot of benchmarking results out there. So it gives us basically a really good sandbox for doing model development.

But I'd say that this general idea of compression using the QPU to learn the structure of the latent space and then efficiently sample is very generally applicable. We're just choosing to focus on, for example, the customer project, they brought us some molecular data set, and we're actually using public image data sets to actually do the model development on. But we see this overall protocol, this overall approach of enhancing a generative model as very generally applicable. And we're actually getting quite a bit of -- a growing set of interest from customers.

In fact, we've had a more research-focused customer, high energy physics customer use exactly this type of technique for generating sort of simulated data for high energy physical experiment. Again, they're seeing a real computational challenge in terms of Monte Carlo simulation of next-generation experiments in CERN in Switzerland. And so they have a quantum-assisted AI model that they've built using a very similar structure, and they're seeing up to a 10x faster sort of inference and sampling capability as compared to GPUs. So I think it's extremely and broadly applicable.

And we have two questions from the virtual audience. Kevin?

**Kevin Hunt**  
*Senior Director of Investor Relations*

The first one is around manufacturing and particularly related to the announcement a couple of weeks ago from the government about funding for Global Foundries and IBM's Anderon. Does that change D-Wave's manufacturing strategy at all?

**Alan Baratz**  
*President, CEO & Director*

So I think our strategy from the beginning when we first started developing our Annealing Systems was to harness commercial foundries to build our technology and adapt those processes to build our systems. And so that continues to be our strategy. I mean we are looking and open to new foundry capabilities as they come online, including new foundry capabilities that could come out of the kind of the portfolio of efforts that the CHIPS office recently announced funding for. And that continues to be our strategy. We want to actually use like commercial foundry services and adapt them to produce our technology.

**Kevin Hunt**  
*Senior Director of Investor Relations*

Okay. And the second one is, I guess, I'll call it the user experience. We spoke about solving problems that are impossible to solve on a classical computer. So the question is, what do users do today? If it's impossible, they must be doing something. So how are they solving problems? And then do we expect any closing of the gap from the -- or response from the classical computer companies?

**Robert Schoelkopf**  
*Chief Scientist*

So I mean, Alan spoke about sort of companies that are getting ROI from using our technology to solve their optimization problems and running their production operations. And so those are the class of customers that are actually accessing and benefiting from our technology today. I mean there are always advances in classical computing methods. So -- and we'll look carefully at all of those advances as the field progresses.

But the gap that we're opening up means fundamentally, quantum computing technology, both annealing and gate systems are harnessing quantum mechanics to solve problems that just can't be solved classically at scale. And so unless classical computers can figure out how to harness quantum resources, they become quantum computing technologies, we think that we will continue to open up a gap of classical approaches for a lot of these hard problems.

**Alan Baratz**  
*President, CEO & Director*

So maybe just say a little bit more.

Yes, a lot of these hard optimization problems, companies are solving today. But what they're doing is trying to simplify the problem and use heuristics to come up with what they hope are good enough solutions. The quantum computer is able to solve the complete or more of the problem faster with better solutions. So even if we're not talking about problems that can't be solved classically, they can be solved just not to optimality, there's still a significant benefit for the quantum computer.

**Kevin Hunt**  
*Senior Director of Investor Relations*

Okay. With that, we're going to wrap it up and get back on schedule here. Thank you.

**Operator**

Please welcome to the stage Chief Revenue Officer, Lorenzo Martinelli.

**Lorenzo Martinelli**  
*Chief Revenue Officer*

I'm shifting gear here, okay, from all these technologies. Hopefully, you know all about it. Bid you can't go home until you fill in the test and you can pass everything was presented. But I'm going to talk to you for only 10 minutes on the commercial side.

I've been here as Chief Revenue Officer for 2 years. So I'll tell you what we've done and address one of the questions that came up is how do we get more people to take advantage of it. And to be honest with you, I see this one event. You're my evangelist. So take what you have, and we'll tell you, and hopefully, you help us get more people to ask a question that we can address. So my team is a global team that helps customers like AT&T figure out how to use our quantum computer successfully. And what do they care about it? Well, not that many people care about the quantum, all the questions have been covered here. What they just care about is I got a complex problem. It takes a long time on classical or I can only have a simplified version of that problem solved.

And just my background, I'm an engineer. I'm an optimization for 25 years. What you do, you simplify the problem so you can solve it. That means it's not an optimal answer. It's not the best answer. So I go look for people that have a problem, they know quite well that is either a simplified problem, so they don't have the best answer or it takes too long and see if we can do a better job. And then you got people like AT&T. The problem is people like me do not know that quantum exists. When the recruiter tell me 2 years ago to D-Wave, I said, that stuff is 20 years away. Part of the confusion this gate versus annealing. People do not know about an annealing because we are people that offer an annealing. So what's the best proof that we're getting some traction?

Well, over the last 18 months, we've had 26 customers just like AT&T publicly say, "Hey, this thing is actually real. I must be solving problems today." You can find this in our press releases. You can find people that presented our events or industry events, an event like today. And of those 26, the one I'm most focused on is what I call Lighthouses. Lighthouses are customers that are leader in the industry and they get the attention of their peers, like AT&T, for example. This is a list of 15 of them that in the last 18 months went out and said, "Wow, I solved the real problem, I get a better answer and get it faster."

For example, in conversation came up, Andrew, when Andrew spoke, in their industry, people paid attention. When BASF, which is the leader in chemical, issued a press release with us, people pay attention. Shionogi, same thing in their industry. And of course, some of those are also big global brands that we all know about it. So my team's whole job is to go after these kind of companies and ask them what are your complex problems and then see if we can provide you a better answer, a faster answer. And we now have a very well-proven method that I'm going to go through here to basically go from identify the problems. We go through a discovery process, but we figure out which problems do you have today. So this is not an experimentation.

Don't come to me with a problem that you can do on classical and you just want to try on quantum, because it makes no value at that point to try. If you can solve it on classical, you solve just as one quantum. It's like having -- I have a bicycle to go to get my milk at the corner store, somebody comes to me with Formula One car, I'm not going to get that any faster, okay? So I'm looking for problems that are that complicated. Usually, people come to us with that. There are people like AT&T that knows exactly what those problems are in their business. And we go through and take a look at it and make sure that the mathematics of that problem is good fit for our systems.

The second thing we always ask is the data available because a lot of the time, we're talking about data sets that they don't have because classical can't do it. And then we prioritize. Let's start with one. It's critical to find the landing use case that is just a killer, with home run. And then we go through what we call a proof of technology. We want to prove to you with your data set because they don't care about generic benchmark. Let's run your data set for that use case, and I can tell you exactly how much better is the answer for you and how much faster is it with your data. If we can do that, great. Otherwise, let's go on to the next problem.

Once we know that it is the right problem, then you got to turn it into a formulation that can work for all your permutation combinations. So we call a proof of concept. We need many data sets. And we're talking about maybe a couple of months in proof of technology, proof of concept, maybe same time frame. By the end of gate 2, the customer has a formulation that is production ready. Of course, that's only the calculation side. They have to do the work to get the pipeline of data, which usually is more data into our systems. And then once we provide an answer quickly, feed it back into the process. So for the first use case that we tend to look for, hey, one way, you already have a pipeline ready, you know you can just feed into your existing, so there's a minimal amount of work to do that.

And then we want to test it out in production, but limited just to compare, is this giving us results and also to prove out that the value we expected in dollar terms actually matches expectations. And then we go full blast production. We have customers that have been running for 3 years in production. We have systems that can handle that, no problem. The whole process here, maybe 6 months to 9 months to 12 months, depending, not so much how dependent, but how quickly can they get the data set ready and they're ready to go. For example, the customer that Alan was talking about that went through the whole process of Fortune 100 companies in a bit less than a year. And the major bottleneck was waiting for to get some of the data pipeline ready for full production.

Now here are some of the example people that have talked about their results publicly. Interesting enough, if you get into some really interesting use cases, they're not so keen on sharing that they are achieving that because they don't want their competitors to know. So getting them to speak is a little hard. But Andrew, for example, talked about it, it's a defense type application, threat mitigation type of effort. You imagine you have a whole bunch of inbounds and you got to figure out how to take them down. And we could come up with an answer that it's 10x faster than what they could do with their classical systems and about 9% to 12% better hits. That's meaningful in their industry.

To me, it doesn't mean very much, but they got super excited. And you can hear excited there in the video on YouTube, if you want to listen to it. BASF is a chemical environment, so it's process manufacturing, filling out containers and so on and so forth, reducing the scheduling time from 10 hours to just seconds. Imagine your demand changes, you go to make a decision if you have to wait 10 hours. A better example that we're working on here that is not listed here is how many of your people have flown here or you all local. Well, how many times you get stuck on a plane that maybe there's a weather issue, equipment issue and there is some change, recovery disruption. Well, that's an interesting problem that I'm very excited about it to fly a lot. And it's not feasible in classical computing to solve that problem.

So we're aggressively going after that. If you can solve that problem in less than 20 minutes, it would be great. And I think we're getting pretty close there. NTT DOCOMO, it's one that published results. The real problem they wanted to solve takes about 1,000 variables and constraints. You can see the paper. They can't do that in classical. They had to simplify it down to about 13% of those, 130 constraints, and it takes them 26 hours to run. They're now down to -- first of all, they want to figure out if I can do 1,000, how much better is result. And the result in their network with their complexity is 15% better utilization.

Now they can turn that into merit value. The other interesting thing is the 26 hours for only having 30, now they're down to the last trip and I did in Japan, they're telling us they can do 1,000 less than 30 seconds, 26 hours, 30 seconds. Those are the things I look for. And you see Ford Otosan, Pattison Food Group, Shionogi, we talk about it, all example. Now as the revenue sales guy, what I'm looking for is any example of companies making big commitments. And that was what we achieved last quarter, where we had a Fortune 100 companies that after getting results of the first use case, a POT. So wait a second. That's going to go on. But if we can get the results with that, we want to go massive across and looking at all the other use cases that we're looking at. And so we have a $10 million deal for 2 years to take as many use cases as they can in production.

And so that came up with a recipe that we're looking for. We're looking for people that already know exactly this is a hard problem. They're not asking for quantum. Hey, this is the problem. I got the data ready. I know exactly the business case I'm going to get for it. The management team, the technical people, everybody is on board because they understand that. Then we make sure, okay, let's make sure that all the data sets, the full data set is ready to go, make sure the compelling value is there. Do we have a technical folks or business folks all ready to go? And that the adoption doesn't require a major change. If I do that, all those 5, that's how you get to these kind of deal sizes.

And this is one company that hopefully soon, they're going to be talking about it that can achieve these kind of results, and those are the companies I'm looking for to prove out the model. Now interesting enough, these -- all these people are using what we call QCaaS. They just need a fast computing engine. Since the last year, 1.5 years, we have seen a huge demand for people that actually want to buy a system. 6 major categories of people. Research labs. This is like Jülich in Germany. That was the first that kind of triggered this whole wave for us because if you own the system, you can access to a bunch of more controls on it, we call it research controls, so they can do a lot of things that you can't do with a production environment and push the envelope in research.

The same thing with research university. We heard about the FAU business cases. We have more universities that want to get more into this. We also have seen national quantum programs. We announced one in Italy where they wanted to have us come from, obviously. And there's going to be a quantum computer installed very much where I came from. Lake Como is my family is from and it's going to be located there. The same thing you saw an MOU we did with Korea. Again, all the companies -- countries around the world are thinking, how do I establish this expertise in this quantum technology.

And then given results that Trevor covered, we're getting interest from people that are into AI space and blockchain to see if we can get these kind of results, we want a dedicated machine or machines to get some of that. And last but not least, in highly secure environment like defense, for security reasons, they want systems. So we're seeing demand for both Quantum as a service and as well systems. And so far, I'm talking about annealing, stuff that is a little right now and so on. But we are now getting inbound interest. We haven't even announced our offering yet in terms of accessing to our gate model quantum computer. I get a company comes to us almost weekly saying, "Hey, we are spending money with other vendors in gate, but we don't have much to show for." We're really interested in this dual rail approach and be able to develop error-aware applications that are -- we can't do with any other quantum gate model quantum platform.

So in this area, we're seeing folks that want to buy a system. We're seeing people that want access to the QCaaS. And you've seen in Q1 already in the gate model market, we're seeing paid research, which is a different thing that we never had as an annealing beforehand. So that kind of covers my quick overview. Of course, I'm available to answer any questions afterwards. We'll be part of a group. Hopefully, you get a sense. It is probably the funnest job I've ever had because where can you be in a place that you have a technology that customers get excited about it. They're actually willing to come and talk about it. And the light bulb goes on at that POT, when they see their data and their results, all of a sudden, they light up. It's a fantastic moment, and I'm looking forward to having many more.

So thank you very much. And now John can talk about the numbers.

**Unknown Executive**

Please welcome to the stage, D-Wave's Chief Financial Officer, John Markovich

**John Markovich**  
*Executive VP & CFO*

Good afternoon, everybody. Thank you so much for joining us this afternoon. We really appreciate the allocation of time and the travel it took to get here. I'm going to highlight on several elements of our revenue and then share some metrics, some of which you've seen before perhaps and some of which you have not seen before.

So let's first talk about our revenue model. So we derive revenue, and this is historically, we derive revenue from 4 particular or specific products or services. As you've heard earlier today, last year, we started to commence the sale of systems. We sold our first system to Jülich Supercomputing Center in Germany last year. And in the first quarter of this year, we booked a $20 million system sales transaction with Florida Atlantic University. And as you just saw from Lorenzo, we've got a lot of interest in that area. So that's a relatively new category of revenue for D-Wave. QCaaS, we have been offering access to our quantum systems through our Leap Cloud system since 2018. This is where the vast majority of the number of our customers are engaged. And then we have the professional services organization that Lorenzo outlined the various steps there. The principal focus of the professional services organization is what we call a means to an end.

Our objective is to utilize professional services as a pipeline to get customers into long-term production QCaaS contracts. Lastly, we have some other revenue, not of the order of magnitude of the first 3. We have service and maintenance on the systems that we sell. These are typically multiyear contractual arrangements. And then we also provide a pretty broad curriculum of training. This is for our customers and for our prospects. And actually, this is all available online. So this is available to basically the general public. We also have a number, and you've heard us talk about this today of professional or potential revenue opportunities going forward. AI, blockchain and then you've heard us talk a little bit about the opportunities within government.

Historically, D-Wave has not recognized much, if any, material revenue from sales to the United States government or any agencies. That is starting to change in a very significant manner, particularly given the highlights of the blessing, if you will, that we got last week from the United States Department of Commerce, along with a capital commitment. And then lastly, the very vast majority of our revenue and our customer engagements have been through our direct sales organization. We are now to the point where we are starting to expand those touch points through channel partners, particularly ISVs and systems integrators. This is a composition of our revenue cut by 3 different ways: by geography, by customer type and by product type. The time frame here is the last 2 fiscal years and the first quarter of this year. As you can see with respect to geography, we've got a pretty substantial footprint in Europe.

Revenue type or by customer type, pretty diversified across research, government and commercial. In our most recent quarter, our commercial customers represented more than 50% of the total revenue. And then revenue by product type, you'll see last year, there's a very large orange portion of the bar here, which is system sale. That is the sale of our first system to the Jülich Supercomputing Center. The reason that bar or a portion of the bar is so large is that our targeted sales price for our annealing quantum computers are in a $20 million to $40 million range. The chart to the far right is what we think that it's probable that the revenue mix by product type is going to look at scale. And we're defining scale as the point at which the company becomes profitable. Notice there's no numbers on that, okay? Because I know I was going to be asked that question.

So we're anticipating based upon the interest that we're seeing on the systems side that revenue mix should be roughly 40% QCaaS, 40% systems, about 15% professional services and the balance being the other revenue categories that I defined earlier. Revenue recognition. So our -- the manner in which we're recognizing revenue varies pretty significantly across our various products and services. The one that's probably the most complex that we get the most questions about is on our systems sales. When we sell a system and we install it, there's a variety of different steps necessary between the actual physical delivery of the system and when it becomes fully operational. The revenue recognition is what's called a percentage of completion.

So through that process, we are recognizing revenue through the process up until the point in time that, that system is turned on, fully tested and is fully operational. That could range from a couple of months to a couple of quarters. Within QCaaS, we now have 2 broad types of QCaaS contracts. One, which I'll characterize as our regular our historical QCaaS contracts are contracts with customers that are accessing our Leap Cloud system for a variety of different reasons. It's a subscription-based contract. So it's very similar, if not identical to a SaaS revenue model. We recognize the revenue on a straight-line basis or ratably over the term of the underlying contract, which can range from a couple of months to a couple of years.

Last quarter, with the enterprise license agreement that Lorenzo just outlined, we have a new type of QCaaS model. We're calling this an enterprise license, and it actually incorporates 2 elements of revenue. It incorporates professional services and it incorporates QCaaS. That particular contract for $10 million is a 2-year contract, and it will be recognized on a straight-line basis over that 2-year time frame, and that commenced in the first quarter of this year. Node placement. This is something we haven't talked a lot about publicly, but I thought it was warrants mentioning because I think we're going to see more of these types of arrangements going forward.

The contract that we announced last year in Italy, the Q-Alliance contract, it's a EUR 10 million contract. This is what we are calling a node transaction. And what we mean by a node transaction is we place a company-owned quantum computer at the customer site, and we do this on the basis that, that customer has contractually committed to buy a significant portion of the compute capacity of that system over a multiyear period of time, typically for a defined field of use. Lastly, professional services, Lorenzo just took you through the 3 preproduction steps in advance of an application actually transitioning into production.

Each one of those steps, which is roughly averages about 3 months, again, we're utilizing the percentage of completion. So if you've got one of those steps that takes 3 months or 4 months, the revenue associated with that step, such as the proof of concept is recognized on a percentage of completion based upon what the contract value is for each step. An example of that is our engagement with Shionogi, and you heard reference earlier to a large major global airline that we're currently working with. So those are both the examples of professional services type of agreements.

Key metrics at scale. Remember how I define scale. So these are the gross margins that we are anticipating. QCaaS, 65% to 75% professional services in the range of 40% to 50% and then quantum computing systems between 75% and 80% or 90%. And the variability there could have to do with the actual specifics of that type of contract because there could be different types of elements associated with that. With respect to operating expenses, we are going to continue to invest very heavily in research and development to support both the annealing program as well as the gate model program as well as our investments in the areas of AI and blockchain. Sales and marketing, we will continue to expand our capabilities on a global basis. And the net of that is the general and administrative expenses.

Given that we now have 2 substantial research and development centers, the first one being in Burnaby, the most recent one being in New Haven, Connecticut through the acquisition of Quantum Circuits and the one that's on the way in Florida, which will be located in Boca, there's going to be an amount of capital expenditure that's going to be necessary on an ongoing basis to fully facilitate those 3 locations. So we're anticipating that our annual recurring CapEx investment is going to be in the $15 million to $25 million range. We're frequently asked what our capacity is, our QCaaS capacity. Each one of our production systems can support between $25 million and $30 million of annual QCaaS revenue.

As Trevor highlighted earlier, we have 4 production systems that are supporting the LEAP cloud system today. So that translates to about $100 million to $120 million of annual revenue capacity. So there's a tremendous amount of operating leverage inherent in that. To the extent that we want to expand that capacity, it costs us approximately $2 million to build, calibrate and install an annealing quantum computer over roughly a 4-month time frame. From a liquidity perspective, we ended the first quarter with $588 million in cash. During Q1, we invested $250 million of our cash in the acquisition of Quantum Circuits, along with the issuance of common shares as well.

Over the last 9 quarters, we have raised slightly more than $1 billion in equity. Roughly 70% of that was derived from curious when we reach different ATM programs. Last year, we had nearly -- by the end of the year, 100% of our warrants were exercised. That contributed about $203 million to the balance sheet. And the balance is made up of closing out or topping off the equity line of credit program that we put in place when we first went public several years ago. And then there was contributions from the employees exercising their options.

You've heard some references today to our patent portfolio. This quantifies the magnitude of the portfolio. D-Wave has consistently been ranked as having one of the largest quantum computing patent portfolios in the industry. Through the acquisition of Quantum Circuits, we just added in a very significant manner to that. So we have over 270 U.S. granted patents. We have about another 320 that are pending in the United States and internationally. So that provides us with more than 590 issued and pending patents. And through the acquisition of Quantum Circuits, we became the exclusive licensee to a very substantial patent portfolio at Yale University, much of which Rob was very involved in patenting, and that is a patent portfolio in excess of 220 patents. So we now have total patent count of over 800.

We categorize our patents into 2 principal categories by type. And as you can see here, 70% or 82% of our patents are systems-based patents and the balance are software patents. And then we also characterize or categorize our patents by the quantum computing architecture. So 46% of our patents support both the annealing architecture and the gate model architecture. 31% are exclusive to the gate model architecture and 22% are exclusive to annealing.

We are fortunate to have 14 security analysts that follow the company and regularly publish on them. I'm honored that most of them are sitting here in front of me. 8 of the 14 analysts are ranked in the top 1% of over 12,000 analysts that are ranked by tip ranks. And as you can see here, I have taken the consensus numbers from all 14 for the price target, the estimated revenue for fiscal '26, which is a little under $43 million and the estimated EBITDA loss, which is approximately $118 million.

Lastly, there are a lot of bullet points on this slide in terms of investment considerations, but I want to highlight a handful that are entirely unique to D-Wave. One, as you heard earlier today, we are the only dual platform quantum computing company, which means we are the only quantum computing company that is positioned to address the entire target market, the TAM. Second, we have developed and we operate the world's most powerful and largest quantum computer. That's the advantage to annealing quantum computer. Third, we have demonstrated quantum supremacy on that system, and that has not been successfully challenged. We demonstrated that on a real-world problem, not a contrive problem, which constitutes most of the other claims to quantum supremacy. We are the only quantum computing company that has got applications in production, meaning that our customers have actually incorporated access to our quantum computers in their day-to-day workflows.

And lastly, 100% of our revenue is derived from either the sale of quantum computers, access to our quantum computers or services associated with our quantum computers, not other revenue categories that might have the word quantum attached to them, such as quantum sensing or quantum networking. Thank you.

**Kevin Hunt**  
*Senior Director of Investor Relations*

Okay. Now John and I are going to tag team for the last Q&A session. I'll let you select, John.

Troy?

**Troy Jensen**  
*Cantor Fitzgerald & Co., Research Division*

It's Troy from Cantor Fitzgerald. Maybe a question for John, if you can share what are the technical milestones that you guys have to reach to capture all of the $100 million investment from the U.S. government?

**Alan Baratz**  
*President, CEO & Director*

I'm actually going to ask Trevor to address that question because he was very intimately involved in developing those milestones.

**Trevor Lanting**  
*Chief Development Officer*

So it's a mix of tooling that we want to actually buy for our own research foundry facility as well as tooling that we will put into our production foundry partners. There is fabrication development and part of the milestones are delivery of prototypes that basically showcase the results of that fabrication development. So there's in all about 9 initiatives, including a tooling initiative and milestones over the 5 years that unlock the funding for the CHIPS office from the CHIPS program.

Now broadly, it's in the areas of things that we are pushing on and developing right now, including the high-density interconnects that Alan spoke about, the superconducting interconnects to connect integrated circuits together, novel high-performance dielectrics for our annealing fabric to drive up coherence times, new wiring and interface engineering to really drive up coherent and multilayer stacks and then some fundamentally new fab techniques for driving potentially higher performance and Jülich technology. So the details of all the milestones haven't been made public yet, but there's a series of basically tool installs, fab process nodes and prototypes that get delivered that make use of those process nodes.

Well, now they've been made public.

**Tyler Perry Anderson**  
*Craig-Hallum Capital Group LLC, Research Division*

Tyler Anderson from Craig-Hallum. I just want to add on to that. And my main question is, for the tooling, is this 300-millimeter capacity or at least additions or add-ons to tooling that you can purchase?

**Trevor Lanting**  
*Chief Development Officer*

So our current tooling is in our current node is 200-millimeter tooling. And so we don't have any immediate plans to move away from that. So it's really focused on how do we enhance the process at that wafer scale.

**Daniel Stevens**

Daniel Stevens with RF Lafferty. My question is more about when you go through your milestones and your chips become more advanced, you built some of your computers on the campuses of other clients. How easy is it to replace those -- the previous chips with your new ones? And how are those clients affected with spending upgrading those computers?

**Trevor Lanting**  
*Chief Development Officer*

Do you want me to take that? So it actually depends on the generation. Some generation transitions just require a chip change. Others require chip change and maybe some control and I/O changes. But they all use the same refrigerator. At least they all have used the same refrigerator up until now. So for the most part, it's actually pretty straightforward for us to do an upgrade. We warm the system. It maybe takes a week or 2 weeks to install a new chip, any new control or I/O and then cool it back down and calibrate it. So it's actually pretty straightforward.

**Kevin Hunt**  
*Senior Director of Investor Relations*

Gentleman in the white shirt.

**Vijay Rakesh**  
*Mizuho Securities USA LLC, Research Division*

Vijay from Mizuho. Just a quick question. On the same $100 million government funding, is that something that you can achieve on Advantage2? Or do you need to get to Advantage3 or multichip Advantage3 to get the entire $100 million? And then back on the POST-NISQ roadmap that you showed in the FAULT-TOLERANT roadmap, the POST-NISQ showed the physical qubits, but not the logical qubits. And on the FAULT-TOLERANT side, I thought you guys showed the logical qubits, but not the physical qubits that you need to get to that. So if you could just hit those two.

**Robert Schoelkopf**  
*Chief Scientist*

I'll take the second one first and then Trevor can answer the first question. Yes, the reason why we didn't really talk about logical qubits in the POST-NISQ arena is because, a, there's not really enough error correction to be able to consider them error-corrected qubits and b, the number -- the total number of physical qubits is small enough that really what we're talking about is like one logical qubit on the chip, right?

So it's more about the error detection capability and new algorithms using the error detection capability and then our ability through our own scientific research to show what the fidelity of that one logical qubit would be. It's not do we get into the FAULT-TOLERANT with 1,000 and 10,000 qubit systems that we have multiple logical qubits.

**Trevor Lanting**  
*Chief Development Officer*

So I can address the first part of your question, which is the kind of, again, getting at the deliverables for the CHIPS program. So there's multiple initiatives that were funded under the CHIPS program. One of them, for example, I just spoke about is improved dielectrics. So dielectric materials that have much lower loss, so that should drive higher coherence. To the extent that those dielectrics become available as we develop them, we will incorporate them into our products, including Advantage2 over the next couple of years.

But another milestone, another initiative really is, again, around the multichip packaging. So -- and that, obviously, the prototypes would need to be multichip prototypes that exercise that packaging technology.

**Alan Baratz**  
*President, CEO & Director*

I think it was communicated, but I'm not sure. It is a 5-year program from start to finish. And the funds are released as the various milestones are achieved.

**William Kingsley Crane**  
*Canaccord Genuity Corp., Research Division*

Kingsley Crane, Canaccord. If we think about gate model, as complex as the technology is it's still -- the go-to-market is a little bit more one dimensional. It's sort of like build it and they will come. For annealing, it's a bit more dynamic. I mean you have 4 systems out there. The ceiling is $120 million spend, the ARR is still a little bit lower today. So on the technology, you can do a lot with 2 million variables. We've seen that with the likes of AT&T. You can do a lot more with 50 million. So I'm curious when we reach 50 million? Is that 2029 or 2031 or later?

And then in terms of the go-to-market, you have that framework of different gating factors within Leap. And we've talked about data availability is a big roadblock. But what can we really do to unlock that, whether that's data availability or other parts within Leap to kind of unlock and get closer to $120 million?

**Robert Schoelkopf**  
*Chief Scientist*

Yes. So on the annealing side, it's an ongoing process, right? I mean, part of the reason why we have a limitation on the number of variables right now with the current solvers and the current processor is because remember, what the hybrid solver is doing is it's trying to essentially find hard sub problems and send them off to the quantum computer. And right now, we're limited on the size of the sub problem, and that limits the size of the total problem. So as the quantum computers become larger, the size of the sub problems become larger, and that allows us to solve even larger total problems. And that's an ongoing process.

At 100,000 annealing qubits, would we be able to support a 50 million variable problem? I would say probably not. We still need to keep growing, but two things will happen at 100,000 qubits. One, we will be growing the number of variables that we can support. And two, for the problems that we even could solve on the 4500 system, we'll be getting even better solutions because we're able to let the quantum computer do even more of the heavy lifting.

**Trevor Lanting**  
*Chief Development Officer*

What was the second question -- the data pipeline and what can we do to help address that. So part of what we are trying to do is to have those discussions early on with our customers so that we identify problems right upfront that are not only challenging for them, but for which they have an environment that if we are successful, we can sooner rather than later move into production or if they don't, at least the right people are engaged to start thinking through and working through how to do that.

So in the early days, like now, it's really all about making sure that we increase our probability of success in getting to production so that we can get a reference-able customers that can then help us communicate to other customers the value and how to go about evolving your infrastructure to support this.

**Unknown Analyst**

I think another question here. For you, Alan. If you look at the road map, it looks like you guys are assuming about 100:1 physical to logical ratio. I guess I would have thought given you guy's better fidelity that you guys would have a much better ratio like that. We know we've got one company out there claiming a 2:1 ratio. So can you just talk about how good we can get to and what type of ratio can get to?

**Alan Baratz**  
*President, CEO & Director*

2:1 ratio. Okay. Don't get me started. Rob, do you want to talk about 2:1 ratio or Robert.

**Robert Schoelkopf**  
*Chief Scientist*

So we're being conservative there, I would say, in the ratio of physical to logical qubits. We're kind of showing you projections for the best known code, the surface code, which is not necessarily the most efficient. But you have to be careful a little bit about some of these newer codes where people know that if you can encode, it's more efficient, but not yet like how you do operations or -- so if they don't have a complete set of operations defined for that, it's not so clear to me whether you can really realize that amount of low overhead.

**Alan Baratz**  
*President, CEO & Director*

I guess the way I would say it is that there are approaches to error correction that are well understood and for which you can have -- you can kind of develop a viable road map. And then there are approaches that are great on paper, but not all that well understood and for which there are huge challenges that remain if we can ever overcome the challenges. So when somebody says, I'm going to be able to error correct to 6 or 7, 9s with 2 physical qubits per logical qubit, maybe in 20 years, I don't know.

**Kevin Hunt**  
*Senior Director of Investor Relations*

I think we'll go online. Yes, there's a couple actually. The first is how long does it take to build the system from start to revenue production? And then do we actually put systems in inventory? Do we build them to order?

**Alan Baratz**  
*President, CEO & Director*

Yes. So if we have all the parts, then it generally takes on the order of 2 to 3-weeks to actually build the entire system, then we have to cool it down, and it can take a week to get it cooled down, and then we have to calibrate the processor. And the calibration is what takes the bulk of the time. Calibration can take 3 to 4 months. At that point, the system is operational.

So we basically say 3 to 6 months from start to finish to have a fully operational system. As far as the parts are concerned, we're constantly evaluating our supply chain. We do a quarterly report on the supply chain. Today, we have no problem with access to all the components that we need to build the systems. And in the past, when we're primarily a quantum compute as a service business, and so we don't didn't need a lot of systems, we weren't ordering in advance. Now that we're moving into a more system sales model, and we've got what looks to be like a very, very strong pipeline, we are now preordering to be able to build as we sell.

**Kevin Hunt**  
*Senior Director of Investor Relations*

The second question is regarding the customer examples Lorenzo talked about, how much custom engineering is required? And is any of that transferable to other customers in the same industry?

**Alan Baratz**  
*President, CEO & Director*

I don't know, Lorenzo, do you want to answer that question?

**Lorenzo Martinelli**  
*Chief Revenue Officer*

Yes. Well, the formulation is very specific to the customer data set. Of course, you get expertise. And if you look at manufacturing problems, you start seeing repetition across. Sometimes we come up with an area that Trevor's team jumps in, and that's an extension. And those goes into the core products of the next customer has the same benefit.

For example, the most recent one, if you want to improve a variable that is driven by a machine learning algorithm, for example, that we can embed it in, and now that's available for every customer. So that's kind of the general path. And so in general, we're seeing now we have a team focused on -- you get expertise in one class of use case and figure out, okay, what are the customer, what other industries of similar ones. For example, scheduling, service repairment that go and have to show up with parts and so on. guess what? There is a lot of similarities there in, let's say, the airline industry. So any kind of -- so you start seeing those similarities. In general, we're organized by industry, so we can kind of leverage those learning curves.

**Craig Ellis**  
*B. Riley Securities, Inc., Research Division*

Craig Ellis at B. Riley Securities. So I wanted to ask a finance-related question. So thanks for all the inputs to the scale model. And I would love to ask what's the revenue number, but I'll ask the question in a different way. And I'll put it this way. I'm sure you're looking at a number of prerequisites across the different businesses to get there, whether it's utilization levels with your 4 or more QCaaS systems or certain points on Rob's road map or number of system sales. Can you just help us understand how you as an executive team and in your discussions with the Board are looking at those issues so we can have a better sense of the path from here to there?

**John Markovich**  
*Executive VP & CFO*

So is your question an actual revenue question? Or is the path how to get there?

**Craig Ellis**  
*B. Riley Securities, Inc., Research Division*

Well, do you want to give me the revenue...

**John Markovich**  
*Executive VP & CFO*

I'm sure you would. I thought I addressed that earlier. Craig, is your question capacity to get there? Is your question capacity to get there?

**Craig Ellis**  
*B. Riley Securities, Inc., Research Division*

Well, utilization on the [indiscernible].

**John Markovich**  
*Executive VP & CFO*

I heard it, John, more as, okay, if at profitability, it's 40% systems, 40% QCaaS and then some of the other stuff. How many systems is it going to take to get us there, which, of course, if we tell you, we'll also mathematically get you all the data you're looking for.

**Alan Baratz**  
*President, CEO & Director*

And if I gave you the capacity utilization on the QCaaS, which I've already given you that number, you can kind of back in.

**John Markovich**  
*Executive VP & CFO*

So look, here's what I'll say. And this is kind of a repeat of what I said on the earnings call. When we first started talking about System sales, I said, think 1, a year, right? A year later, I said, think 2 to 3, a year. But I'm seeing a really strong pipeline right now, and I see that growing nicely into the future. And so I think if you start thinking about like natural progressions off of 1 to 2 to 3 to -- you can probably figure out how to get there.

**Unknown Analyst**

So this is for Rob and Trevor. Non-Clifford gates are what give quantum computers all their power. So I'm really curious about the overhead associated with magic state factories in your road map and how you address that overhead?

**Alan Baratz**  
*President, CEO & Director*

So full marks, yes, this is correct. So there's been a lot of recent theoretical progress on how to reduce the overhead associated with [indiscernible] state production and the like. And one of the things that's interesting and pretty exciting there as well is the idea that you -- of course, when you're preparing these states, you get to cheat a little bit. You can use repeat until success and detection. So something that we're looking at more closely is like how far up the ladder of fidelity we can be as a starting point for producing those states. So I think that's another place where you can see a good bit more progress potentially coming from that.

**Unknown Analyst**

So it's almost on the software side [indiscernible]

**Alan Baratz**  
*President, CEO & Director*

I think it's a combination of both. So it's the point that we have the hardware that can place some new tricks and the learnings that people are making on the theoretical side.

**Unknown Analyst**

Maybe just one more question. Part of the U.S. government's recent investments included $1.35 billion to secure the world's first Quantum foundry with IBM and $350 million at Global Foundries. You've had one of your foundry partners in the process of being acquired. Can you just share your thoughts on would you be willing to use IBM as a potential customer -- sorry, competitor? Would you be willing to use Global Foundries? Just any thoughts on the process technologies of those two companies?

**Alan Baratz**  
*President, CEO & Director*

I mean we didn't know ahead of the announcement by the U.S. government who would be getting funding in this round. But as soon as I heard the announcement, I send an e-mail to Trevor and I said, can we use the IBM Foundry? Absolutely. If they have technology that we can make use of, and it's open to other potential companies to leverage, which I suspect it will be given that it's got a significant U.S. government investment, then we would absolutely use them. I think that there are some owners of foundries that I have a bit more comfort working with than others. And yes, I mean, if IBM has got technology that we can leverage and the U.S. government is a significant investor and partner, I would be very open to using it.

**Kevin Hunt**  
*Senior Director of Investor Relations*

Okay. I think that, that wraps for the day. We do have some refreshments out in the entry way, and thank you all for joining us. You have a good day.