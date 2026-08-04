---
ticker: SNOW
company: Snowflake Inc.
title: "Snowflake Inc. (SNOW) Analyst/Investor Day Transcript"
published: 2026-06-03T06:51:55-04:00
article_id: 4911200
source_url: https://seekingalpha.com/article/4911200-snowflake-inc-snow-analyst-investor-day-transcript
---
Snowflake Inc. ([SNOW](https://seekingalpha.com/symbol/SNOW#source=section%3Amain_content%7Cbutton%3Abody_link "Snowflake Inc.")) Analyst/Investor Day June 2, 2026 4:00 PM EDT

**Company Participants**

Katherine McCracken - Head of Investor Relations  
Sridhar Ramaswamy - CEO & Director  
Christian Kleinerman - Executive Vice President of Product Management  
Brian Robins - Chief Financial Officer

**Conference Call Participants**

Karl Keirstead - UBS Investment Bank, Research Division  
Sanjit Singh - Morgan Stanley, Research Division  
Aleksandr Zukin - Wolfe Research, LLC  
Ittai Kidron - Oppenheimer & Co. Inc., Research Division  
Robbie Owens - Piper Sandler & Co., Research Division  
Brad Zelnick - Deutsche Bank AG, Research Division  
Michael Cikos - Needham & Company, LLC, Research Division  
Adam Tindle - CGS International

**Presentation**

**Operator**

Please welcome Head of Investor Relations at Snowflake, Katherine McCracken.

**Katherine McCracken**  
*Head of Investor Relations*

Hi, everyone. Welcome to Summit and welcome to Investor Day. Thank you for joining us here, whether you're joining in person or virtually. We appreciate you making the effort. So I'm going to kick things off with a quick overview of our agenda today. We will have presentations from Sridhar from Christian and from Brian, Sridhar will give an overview of really his vision for Snowflake and what that means for both our core data platform opportunity as well as our AI opportunity. Christian will then take the stage and go over a lot of the product announcements you heard from us this morning and really detail how those are fulfilling the vision that Sridhar will lay out.

And finally, Brian will come up here and share our financial outlook and the implications of that vision. We will wrap with a Q&A, so we'll take questions from the audience. Sridhar, Brian and Christian will all be on hand to answer your questions. As a reminder, we will be making certain forward-looking statements today. So this is a statement on our non-GAAP financial measures as well as our safe harbor. Both are available on our Investor Relations website.

And with that, I would like to pass it over to Sridhar.

**Sridhar Ramaswamy**  
*CEO & Director*

Thank you. Thank you, Katherine. It's great to see all of you. And Summit continues to be an event whose scale I have trouble absorbing. One of my friend who came last year, Sara, thank me for inviting her to a rock concert. It's kind of funny to be in the world of data and be able to have that kind of excitement and impact.

I'll start with a big picture view of both the disruption and opportunity that AI provides for many companies. Snowflake definitely in that list. For most of us work is an endless sea of tabs. And we are responsible for figuring out how to organize over time, how to organize the information that we consume and then to figure out what to do with it. I joke to people that command, shift, A on Chrome is life changing. But it's really -- that's really hard. And what we are beginning to see is AI changing the very nature of information work.

And what this means is that the data that your AI agents have access to -- we'll get into what an agent is and so on, is critical. Integrations with the different pieces of software that all of you use, that I use that is also critical. And overall, for an organization, governance overall of this data, security, is also a big, big deal because these coding agents are immensely powerful, but also sometimes don't have good judgment about what's okay to do with what data. And so this means that for an analyst, somebody that wrote SQL for a living, things are just very different.

They go from effectively creating dashboards or writing one-off sequels to creating what looks closer to software within Snowflake, for example, we deployed skill packs that were specialized to different departments within Snowflake in a matter of like 4 weeks, and we've been continuously iterating on them and using these kind of agent products, so super, super intuitive for all of the nontechnical folks at Snowflake. Brian is going to talk to you a little bit about sort of the CFO experience doing that. And for our data scientists and our data engineers, they now think in terms of how do you automate creating an entire pipeline.

For them, even adding a single column in a table used to be like this endlessly tedious work of making stuff propagate across hundreds of files manually with people looking it over. That stuff is getting automated. And so for a lot of these end users, myself included, when I need to look at like sales data, I don't want to be writing SQL, data integrations are seamless, which means that all of the information that I want is just available kind of thought analysis at our fingertips and deliverables for the smartest people that know how to take advantage of these products is no longer limited by how many hours they work.

It comes down to how effective are they at using agents to get their work done. In fact, one of the idioms that we are trying to teach our software engineers at Snowflake is that they really need to be thinking of their work as being a tech lead of agents rather than an individual contributor that writes code one line at a time. It's a huge, huge mentality shift.

Now I'm not claiming that we saw all of this. I don't think anyone saw all of this. But I've talked previously about just the transformative power of even being able to access data faster even in a pre-coding agent era. And so we started investing into this in earnest, starting early 2023. And one of the things that, Christian, I, and many others have consistently believed is that AI is going to make the value of and easy to use, connected and trusted data platform like Snowflake, even more than before. And these are our growth rate numbers over the past many quarters. And as I said, during much of this time, our focus very much was on how do we create the definitive data platform that people would want to use if they wanted to get value from AI.

And all along this journey, we also worked really hard as a company, and I mean it, in discovering the basics of what does it take to create great products and launch them. Two years ago, I talked to you folks about how we are basically rethinking how we took new products to market about farming we teams that brought every specialized function back into a small collapse team that could sit in one room and take a new AI product to market.

I talked last year about how it was really, really critical that not just software engineers, but all of the solution engineers within our team. These are the presales folks that show the art of the possible with our customers that help them get projects done. I talked last year about how it was really important that they become AI native because they could just get more things done faster. And a lot of our success as a company. This was a trend 3 years ago, it was going down and clearly, it's not. If anything, it's going up and going up well, has come from this back-to-basics approach of we need to create great products. And we need to figure out as a company, as a team, how we take them to market.

And even in this pre-agentic world, we are seeing the results of that effort which a lot of people had to painfully reinvent how they work because people are happy sort of doing their own specialization. It's awkward to suddenly say, you're responsible for the whole and you need to iterate a lot faster. And all of that work has been paying off in things like productivity numbers. We measure the productivity of our expansion account executives in terms of how many quality use cases do they win per unit time, per quarter, per month. Similarly, we measure the effectiveness of our sales engineers, solution engineers by how many use cases did they help their customer take to production.

And so the number of use cases won per AE, this is not the size of the AE team increasing, but it's per AE. It's increased by 86% year-on-year as we look at the quarter that just transpired. And the number of use case go-lives per SE has increased by 58% year-on-year. These are hard numbers to move because the average AE wins a handful of use cases per quarter. And even now, the way I think about scale processes within the team, and it's often an awkward conversation is I routinely boil it down to what's the top decile doing even within a population that, on average clearly is doing better. And we press it very, very hard on what is the top decile doing that the rest of the team needs to learn.

And it's the process of continuous self-improvement that we think is really important for us. And in many ways, that's the structural transformation of Snowflake as a company. And now fast forward again to now. I have talked about -- this is what my keynote was about. This is what Christian covered a lot of. I think the future of work is very much all of us, all of you, me included, living in a new kind of environment, just like all of us got used to living in a browser for most of our work life or using our phones 24/7. What we see happening very, very clearly is that there is a new category, the agentic control plane. And that is going to be at the center of how work gets done.

A lot of companies are going to be competing for it. But for it to be effective, it needs to have amazing enterprise data in context. It needs to have all of the applications that particular user is using and has context. For, these are the Salesforces and the Workdays and the ServiceNows and the SAPs of the world. And obviously, the awesome models that seem to have no bound in their capabilities for what they can do. What we are very proud of is we have created products that can capture what this work is going to be. But in a way that is true to what Snowflake is. I'm under no illusions that competing with Anthropic on the quality of large language models that my team can create is a winning strategy. It's not. It's a failing strategy.

But on the other hand, we can go head-to-head with Claude Code when it comes to CoCo, and say, here are the reasons why we are actually an important part of every customers and increasingly every partner's data ecosystem. Most of our partners are here. I've spoken to several executives already about how do we effectively have CoCo as a de facto implementation platform for all of the data work that their teams do, and this is hundreds of thousands of people in some of these organizations. And on the CoCo side, we have like measurable proof on a product that is very young. So our services team delivered a Spark migration 60-odd percent faster working on behalf of a Global 2000 hospitality customers.

And a financial services firm saved over $500 on a job that they were doing. We often hear about migrations. At this point, the number of things that are possible with CoCo honestly exceed our imagination. We hear of people doing things, doing migrations but honestly, we would not have thought about it. What we did do with it was set the details for creating a product that would truly be great when you work with Snowflake. To me, this is the other reality of the current moment, which is a little bit of what the judge says about what they saw. You know a quality product when you see one and you use it. And having that bar for creating amazing products matters more than ever.

CoWork is even more ambitious. Obviously, it has its origins in Snowflake intelligence. But back when we first launched Snowflake Intelligence, which was November of 2024, we saw it as a place where all analytic data came together. But part of what we are realizing, again, driven by large-scale use within Snowflake is that it can be so much more. Once you are able to access all of the common applications that you have, whether it's a Gmail, a drive and now even things like a Salesforce. And you have a platform in which work can be abstracted, work becomes very, very different.

And again, is available like right in your pocket or your laptop. We are earlier with these kinds of very large deployments of CoWork, but customers like WHOOP, tech-forward companies are figuring out how to use a combination of CoCo and CoWork to transform how their teams operate. And in the analytics world, CoWork has already proved its mettle with any number of large customers, folks like United Rentals or Domino's in Australia or one of the largest banks, which is delivering a personalized solution for all of their exec staff using CoWork. And as I said, an important element of all of this product work is leaning in to what is possible, starting with Snowflake as customer zero.

We have talked about Snowflake being customer zero before, but I think we are practicing it at a very, very different scale and speed right now. Things are being codeveloped. And I want to show you one glimpse of how we are using these agentic platforms to transform how work gets done internally by our teams. This is an example of our support team using CoCo to transform itself. Let's watch the video.

[Presentation]

**Sridhar Ramaswamy**  
*CEO & Director*

And so benefiting from data gravity. We think we occupy a key position in the world of AI. And we are very cognizant of continuing to be world class in this. A lot of what Christian announced today was around continuing to be that trusted data platform, that governed data platform. And things like the Natoma acquisition are going to make that even more true in this world of agentic AI and agent control planes. And we think there's a significant amount of opportunity, areas like observability or data-intensive problems that are ripe for disruption from people that are willing to think from first principles about what software should be.

And honestly, we also get inspired by customers like Emmanuel that you saw yesterday. Who came to us and said, hey, this is our data. We want to rethink how my salespeople should interact with that data. And I have the guts to say, I'm willing to do that from first principles.

I think that's the disruption. That's the opportunity that's there in front of us. I've stressed this in the previous 2 Investor Days that I have done with you folks. Strategy is fine. We think supercharged great agentic AI products, AI control planes built on top of this incredible data foundation can be a great company, but I stress execution a lot. And that execution manifests itself in how are we able to move quickly in creating value. It's not lost on me or on Snowflake that we need to rethink speed when it comes to software. But living it is really important.

I'll give you folks like another example that's like visceral, right here. There's one engineer, just one that's been working on a CoCo mobile app. This is one of these like remarkably productive people that knows how to juggle 8 balls at the same time. And yesterday, before we met a set of reporters. I had like this momentary pang of doubt that I didn't know all of the launches that were going to happen at Summit, I had a list, but it's a long list. And I asked Christian, hey, where can I look? Christian is helpful and he gives me 4 documents, not 1 but 4. I was like, really, dude, 4? I paste it into CoCo. MCP support has not yet been added. And so CoCo, I got MCP support. So thankfully, I put it into CoWork and that part worked. So I had the list of launches, which was cool.

But the more cool part was I go back to the Slack channel after we did the interview with the press folks. And I tell this person, hey, when is MCP support coming. They go into slight panic I usually like preferencing all my Slacks with like low priority because people act faster than you really want them to and you're the CEO, but he's like, no, no, no, we'll get it to you. And 2 hours later, he's like, MCP support just added, just update the app, you got it. And sure enough, I paste the same prompt back into the CoCo app. It gives the same summary.

And so execution really, really matters right now. And on things like durable advantages need to be thought through. Christian speaks to some of these things. So we pay attention to that. If software is truly easier to create, what does that mean for the future of Snowflake? Where is the ongoing enduring value? What are the products that we can create, for example, that can make CoCo much better out of the box than a Claude Code. And how can it make it even more better for everyone else in the company if a set of folks use it. These are the feedback loops. I tell people, it's clear to me that Airbnb doesn't care about the cost of creating software going down because they create a network in the real world. And so companies need to be thinking about what's like the additional value, what makes these products better with usage.

So we spend a lot of time thinking through how do we execute to that kind of a vision in addition to being a great data platform. We want to be efficient on the go-to-market side. It's an enormous team. We get enormous leverage. And we have talked to you many times about things like new logos. And this was a remarkable quarter for us because both the number of new logos that we won and the ACV, the total contract value that we got out of these new logos, both went up significantly year-on-year. That's because there are a set of people who obsess about this motion, who obsess about getting these customers onboarded, getting these customers live. And that's the efficiency that I push for, that we push for.

What are the happy accident that happened with CoCo CoWork and AI in general with Snowflake is the act of making these products broadly available to the entirety of employees at Snowflake basically led to this explosion of creativity and ideas. You didn't tell people, you can't use CoCo because, well, you're not an engineer like anyone can use CoCo, you can only access the data that you're supposed to see. We have governance controls on the data, but sure, you can build anything. And so we saw amazing things like JB, our Head of Sales. He built a Streamlit app to look at his travel and entertainment expenses because he was sick of e-mails from Brian complaining about it. Let me just look at it. And that clearly changed his mind about what is possible.

And so if you folks talk to JB, he will talk excitedly to you about how we can shift right in a massive way and have more of Snowflake sales team focused on delivering projects for our customers. So it's like we need to create outcomes faster. And software engineering, as I said, is undergoing a complete revolution. Anyone that thinks that's software engineering is about white coding. It's firmly stuck in early 2025. We are producing a set of -- not we, like the world is producing a set of rocket scientists that are way smarter, can get way more done then the ordinary software engineer or even the excellent software engineer could do last year. And so by focusing on the basics of what Snowflake is about, what do we do?

We make software, we sell software, we run software, that's the SREs. They've gone through a complete change similar to what you saw with the support team. They have completely redone how they look at operational problems, again, built on top of CoCo. And we did this without buying new software. That's the magic also of the moment. And we are focused heavily on how do we make deployments go faster because I see that as a final remaining hurdle. Obviously, we work with partners, but we are also investing into a -- it's going to be a small team, I don't think of them as thousands of people. But these are folks that know the best of what Snowflake has to offer as a platform go deep to understand what it means to solve a customer's problem and solve it as quickly as possible.

And you saw the results of some of that with Sanofi yesterday on stage. These are among the healthiest collaborations that we've had with a very motivated customer. We're doing similar things for large banks. And we anticipate that we'll be leaning into something like this as the impact of products like CoWork becomes obvious, and people realize that their data teams like our own have to modernize themselves for them to be relevant in this age of AI. And the final comment that I want to make is that because we have invested so much in transforming ourselves, in being more effective as a company. And because of our ability to increase non-GAAP operating margin, but also bring SBC firmly under control, we feel confident enough to say that we'll be reaching GAAP profitability at the end of next year.

And Brian will walk us through more of the details of that. But I see this as the culmination of the work that we have done over the past 3 years to reinvent ourselves to be more driven, more product focused, more quality obsessed, continuously self-improving company. With that, I'm going to hand it off to Christian.

**Christian Kleinerman**  
*Executive Vice President of Product Management*

Hello, everyone. How's it going? So good to see -- round showed that was this morning. No, awesome to see so many familiar faces. I assume most of you attended the keynote this morning? Okay. So sort of awesome clapping, good. CoCo is the answer. You got that so I will recap some of those innovations that we're launching at the conference. But I will also contextualize it for what is probably most interesting for all of you to think about it and how do you think about it as a company.

To get started, I use the exact same diagram visual that we started with because it is truly a set of innovations that reinforce what we're trying to do here. The more we've thought about this picture of the agentic enterprise, the clear we are that the elements are data, AI models, connectivity to enterprise systems and something that drives it. Sridhar in the keynote last night said something that is resonating 1,000% with customers that we talk to, which is, the differentiation is not the access to the AI models. The differentiation is the access to the right data. And that has created a sense of urgency in many of the customers that we talk of to on, oh, I really need to go get my data estate in order. We have been saying for a number of years, you have all heard us say it consistently, no AI strategy without the data strategy and we're living it more and more on a regular basis.

The question that I think many of you are usually trying to infer or to get us to provide color is, okay, how do we differentiate? How do we stand out from the alternatives that customers have. And Sridhar just mentioned it, but I cannot emphasize enough the easy connected and trusted. The keynote this morning had some fancy words, but it was the exact same easy connected and trusted. And I've arranged the set of launches and announcements that we have into these 3 buckets. So with that, starting with easy, you know the answer, right? Coco.

Someone is whispering CoCo. And it is true. It is not only on brand to how we thought about differentiating for a long time. You've heard us talk a lot, we may be willing to give up some use cases where someone wants to turn knobs all day long because we just want people focus on productivity, business outcomes, business value. And what has happened with CoCo is truly just we materially change that. I would like to say 10x that, but 10x doesn't quite capture it. I shared this morning at Openflow, we added all these APIs. And now we went from Openflow is cool, but it's hard to configure to, I just ask CoCo and it configured for us. Something that at the encouragement of Sridhar, give credit, every single launch that we're doing has to come with how is the experience simpler with CoCo. And in some instances, in many instances, we're starting to use CoCo first, then you go build the UIs and the APIs and all of that.

Because in reality, if you can just ask, hey, give me governance, give me interactive analytics. And CoCo figures it out. It's easier to build for CoCo private interfaces or internal interfaces, then go and make it easier from a user experience or a UI. So the emphasis on CoCo is not unwarranted. There are parts of their product that today at Summit, they're only accessible via CoCo. And in reality, many instances probably you'll never need any other way to access it. So I cannot emphasize enough the role that it's playing for us. And as we established in our earnings call last week, it is that nature that is helping the entire of the usage and use cases for Snowflake. We announced a number of capabilities this morning. The way I would think about it, I don't want to go too deep into the technology, we're trying to eliminate the differences between the form factor.

The beginning, CoCo has a command line version, which is incredibly powerful but it's accessible to a smaller set of users because not everyone is comfortable with a terminal window and a bunch of shell commands. On the other side of the spectrum, we have CoCo in Snowsight, which that one, the usage is quite broad because it's in the phase of all of our users, but it's not as powerful because it didn't have the right sandboxing and security guarantees.

A lot of what is in here, and I'm happy to answer questions at the end, but I don't think we need to go into those details, a lot of it is eliminate that friction. Bring the power of a command line interface, bring it into a desktop experience, bring it also into the hosted version of Snowflake. And now what we say is you get full power but you still can sleep well at night in terms of the scope of actions taken by CoCo are constrained, whether it's on-prem or a new machine or whether it's hosted.

And the other thing that we're very excited is the CoCo desktop. For those of you, I know that you actually are tracking very much or very closely a lot of what we do. Initially, when we had announced this research review call SnowWork, it was all about we released the desktop internally to Snowflake. It took off like wildfire. Everyone transform how they work. And that's when we said, okay, maybe this is a different way of working. At the end of the day, we have clarity that desktop experience is CoCo. And I think we're going to also follow with something like that, for CoWork, which is the more governed experience. But the desktop form factor has product market fit inside of Snowflake. We made it available in public preview a couple of weeks and at the conference is generally available. We expect this to drive some additional usage of CoCo.

And maybe I'll highlight here the Excel form factor, the VSCode form factor as additional ways and services for our customers to be able to get value of CoCo. And it's not on this slide, but I mentioned it this morning on the stage, which is we also put a CoCo plug-in into the Claude Code marketplace. Of course, we would like to say that for data management operations, you don't have to use the interaction of Claude Code to CoCo. But if someone is already very committed to cloud code, there's a very easy way to plug in, and we've already heard from some customers in that situation, hey, this is ideal. I can use Claude Code for application development completely unrelated to data or Snowflake, but I can delegate to CoCo all of the data management activities. Sridhar just mentioned migrations.

And the way to think about what's going on in migrations is truly a reboot based on what AI has enabled. You all have quiz us for years now on how quickly customers consume the contracts, how quickly they start with consumption and we are seeing a massive acceleration of time to migrate. I'll caveat, not everything in our migration is just what the technology needs to do. That piece, material acceleration. But sometimes there's things like I will not be able to run this test because it's end of quarter, end of year or I do a production freeze in the Q4 of my fiscal year. There's a number of constraints outside of the pure technology. Those were working and some of the FTE efforts that Sridhar mentioned help, but at least the pure coding, testing, all of that is materially changed.

The middle column in here, actually, I talked about the middle column, the one on the right, Spark. We've been working on more and more compatibility. I've been the ones sharing with all of you that, our engine is amazing. People that want to move from Spark, they want more compatibility. Guess what? In a world we're migrating from one type of API to another type of API is borderline free, we're starting to see different reactions. I mentioned this morning, there's a customer that wanted some legacy Spark API, and it's a pain to support that legacy Spark API. We've been working on it, and we know that at the end of it is going to be compatible, but not super fast. And we're busy doing that. And in the meantime, the customer said, oh, we tried CoCo, we converted to Snowpark, and we're done, we're good, and it's 5x faster and cheaper by implication.

So we're actually -- we have a renewed push on Snowpark. We mentioned it to some of you that we are seeing increased momentum of Spark migrations, use of Snowpark just because, hey, the pain that represented converting code is no longer as painful as it is, so it's just easier to do. And then the last piece that I'll mention is the first column here is the productization of an acquisition we made a company called Datometry. What that company does and what is now part of our migration suite is lets us virtualize a Teradata experience. So we hear from many customers. I want out of Teradata, but I have all this stuff around it, I have scripts and applications and reporting systems and changing all of that takes time.

That's why some migrations of Teradata we've done are 2 years, 3 years. What this virtualization lets us do is say, if this is Snowflake and these are the apps, we put a layer in between. And that layer, let's take everything else in the enterprise environment, think that it is Teradata. It looks like Teradata, it has Teradata SQL, it has Teradata scripts and Teradata is a really rich function of product. To the rest of the ecosystem, it looks like Teradata. And what it's doing behind the scenes is translating into Snowflake. So when we did the acquisition, the converting it to support Snowflake took a few months. I don't know how long ago, that was 6 months or so. Now we're ready to start accelerating migrations through this. So we're excited about the opportunity to help customers move off of Teradata quicker. Next Sridhar mentioned it, CoWork CoWork is super important.

We do believe that it is the enabler to change how people go about their jobs. I think both Sridhar and I talked a lot about these apps because at least personally, we use a lot of different apps and you need to know where to go for what as opposed to, let's be more user-centric, and let's ask the questions for the request and something that you need to take action on, just say it and then let us systems figure out the details. That is what's being enabled.

That's why it's a big part of the shift of what we're doing here with the personal work agent. It's not about even more systems, they move from tabs to different agents. No. I have one entry point. It knows me learns about me. It learns about what I like, what I don't like. I was mentioning to a few folks that, now there are so many things that I go do something interesting and analysis. And then I say, hey, I would love to get a refresh of this once a week. And I have CoWork doing all these things all the time, and I'm just getting regular reports. And now we introduce automation. So I can say, oh, by the way, if you ever see this type of condition, just go take an action, e-mail someone else or do something like that.

So you can see how workflows are getting reinvented with the power of CoWork. I have one slide on our artifacts and dashboards. This is, in my mind, what BI should look like if you were to start from a pure AI native perspective. It's not the goal of, I have a dashboard and then I'll see if it went up and down and then I have to click 100x. No, you ask a question. And then you get the visualization that most helps you understand what happened, and that's what then you go and share with others. It's not the other way around. And by the way, BI was amazing for when it was introduced, right? It changed the accessibility of the data, but it's still, here's a set of static views and you need to figure out the answer.

It should be the other way. You asked the question, we give you the answer, and here is a visual that helps you understand that. So that's what we're doing with Artifacts tool, live data, governed data, authored in CoCo, published with CoWork or made available to business unit CoWork, and we have the way for you to pin them down and say, oh, I arrange these files, effectively, it looks like the modern version of a dashboard but it's curated for each user on what they want.

Cortex Sense, we introduced it this morning, I'll be the first one to say, it is early on, but the insight behind it is we have the ability to gather a lot of information that can help both CoCo and CoWork produce better results out of the box. And I say out-of-the-box as a contrast to today, if you curate enough semantic views and enough information, you can get all the results that you want with CoWork and with Cortex agents. But what we're increasingly seeing is customers wanting, I need answers now. I need to be able to roll something live as soon as possible. That's what Cortex Sense enables.

And in a few of the conversations we had last week, there was this question on how does it compare what you're doing relative to what a coding agent does I'll caveat, this is one evaluation set, it's not a fictitious. It's a real customer valid use case. But all of this will say mileage may vary. So I still pride on not generalizing where you don't have the power to generalize. But what you see in the front row is leading coding assistant, trying to interface with MCP for SQL and asking questions about the data. Second one is CoCo and CoWork as we know it right now, and the last one is CoCo and CoWork with this run time content that Snowflake gathers to say, I know enough about the user, the data, all of this to say, here's additional information, and you see both material improvement in quality, but a lower cost. And if you're thinking like, how can it be lower cost. There is a huge amount of cost and tokens that go into, oh, yes, my bad. I didn't get it right. Sorry, let's do it again.

That burns a lot of cycle as opposed to, if you know what the question is, how do you answer the question? It translates to better economics. So we're extremely excited about this. And again, I'll caveat it to, we're in the early process of testing the different scenarios, different customers, et cetera. But this is a big differentiator for how we think about out of the box, our agents, CoCo and CoWork just produce better results for customers. And Sridhar mentioned the acquisition of Natoma, this is 1 of those 3 key elements on the agentic enterprise, important differentiators, both for data administrators as well as for users. They're administrators.

One, it connects to 100-plus business systems out of the box. Number two, it enables those administrators to have policies on what agents using these MCP connectors can do. We were sharing the example, at Snowflake the way we configure the e-mail connector of Natoma was you can ask your agent, CoCo or CoWork to send an e-mail. If the e-mail is going to an internal recipient, it sends it. If the e-mail is going to an external recipient, it puts it in your drafts as a way to force humans to do it. That's a policy we chose. The cool thing is Natoma lets our customers decide what policy they want. If they just want to spam people, that's fine. If they want to be more conservative, even for internal, they can do it.

Third benefit is see and audit everything that's happening with these agents because if it's the new way for data to get pushed out, then, oh, we just sent a bunch of your sensitive data to a connector that was going to do, I don't know, Slack or e-mail, you want to know all of those things. And from a user perspective, instead of me authenticating with 100 different systems, I authenticate 1 to the gateway, Natoma and that gives me authentication to the other 100 systems. We introduced Datastream this morning. The goal of this is to move Snowflake upstream such that it can have a streaming solution, capture data when it's created, whether it's a sensor, a device, a website and be able to land it into Snowflake with almost no administration, very little management and very low latency.

We're very excited about this. It's in the category if it's early, but quite promising. Pillar #2 is connected. The integration, the interoperability that we're showing with iceberg, I would say, second to nobody. That's a hard statement to make, and I do it based on facts. We are truly committed. We are steering the Iceberg standard, but we're also being amongst the first at implementing it. Right now, we're the broadest in terms of the implementation of the V3 spec, and we're steering the V4 spec. I mentioned this morning, we integrated all the rest catalog APIs into horizon to make sure that we can interoperate with data regardless of where it sits. Even if it's on Databricks,

We can read and write data, other engines with Glue and others, they can read and write data that sits in Snowflake. So this whole notion of I'm locked in, and I put my data like that's not excuse. Customers, please use whatever gives you the best experience and the best performance, the best economics. And okay, this one is super important for all of you in this room. When we introduced Iceberg and I think some of us regrets how much noise it costs. But one of the things that was factual was with Snowflake, you store in our format and you pay for storage. With Iceberg, we always said, it's customer-managed storage, but there's no reason for that trade-off.

So we introduced and is generally available here at Summit. Snowflake manage storage for Iceberg, so you can still be interoperable, but we'll do the management of the storage, we'll give the economics. So that, I think, is going to be an even better tailwind relative to at least how we thought and modeled the adoption of Iceberg. Sharing, I think all of you know, I'm personally passionate about the network effect, personally passionate about the unsiloing of data and helping organizations connect. I am very excited that we're finally breaking out of the -- its 2 parties, unidirectional, how do we do multiparty collaboration and symmetric. It starts all with our data clean room.

This is productization and evolution of an acquisition we did a couple of years ago. But we're starting to see very interesting media use cases advertiser, buyer type of collaboration use cases that helps collaboration. And this already gives us some structural advantages, the more parties you have exchanging data via Snowflake. We also talked about zero-copy partnerships. The marquee one that is when GA actually last month was with SAP. We have a few initial deals of people buying into this integration. And today at the conference, we announced the expansion of some of the Workday integration we've done, new integration with IBM and new integration with AVEVA.

And then I could spend as many hours as you want on the importance of trust, we gave it a decent amount of air cover this morning because I think this is what changes how Snowflake fits into the adoption of AI for enterprises, rolling out AI is easy. Rolling out AI in a way that people can truly sleep well at night is not as easy. Horizon, the catalog is where all of this comes together, Horizon context, is where we brought all the explicit semantics and information for agents to be able to work well together.

And again, there was a slew of announcements. I left a number of things out from this morning. There's a lot more during the conference on how do we help govern agents which is security policy, identity for agents, data movement, it's filtration protection, all of those. We also talked about Adaptive Compute, I put it in here just because there's something I want all of you to be clear on. Massive performance improvement, but we're doing the exact same thing that we did with Gen2, we priced it in a way that we're aiming for revenue neutrality.

So our customers get the benefit that is materially faster, but none of you need to go change your models, we're still good even though we're trying to push very hard for the adoption of all of this. Interactive analytics for responsive experiences, you can say this gets into the ClickHouse type of workloads. I am always very careful to make absolute statements, but it's incredibly competitive to the alternatives customers have out there, and we're going to be making a big push to get adoption of this.

And with this, there's the Data Cloud as a whole. This is the data for enterprise data, manage governed part of the solution and wrap it up back into the, it is part of the bigger picture that we share. Happy to chat more at Q&A.

Hopefully, this was useful. And now we're going to turn it over to Brian. Thank you.

**Brian Robins**  
*Chief Financial Officer*

Thank you, CK. Super, super fascinating all the product releases and product velocity that we're seeing. And thank you to each of you for coming out today. There are some of you that have been around the story for a long time. There are some of you that are relatively new, so I'll walk in and talk about the market, some of the revenue drivers, get into GAAP profitability, capital allocation and so forth. So the market today is roughly $225 billion. We expect that market over the next 5 years to more than 2x to over $460 billion. AI is expanding our market opportunity. Last year, we went through this. And over the 5-year period, our market has grown roughly 30%.

We really have conviction on this when we look at our large customers. And so the top 25 large customers, they spend, on average, $34 million a year with us. That's grown over the last 2 years from $22 million a year. When we look at our Fortune 2000 customers, G2000 customers, in FY '26, they, on average, have only spent $2.4 million with us. We feel that we have the right to actually increase those customers up to our large customers' spending. We'll jump into the core growth drivers of the business, primarily in the core data platform and our AI workload.

Let's jump into the core data platform. Landing new customers is absolutely essential for us. When we land new customers, they don't add that much in year 1 or 2 from a revenue perspective, but it's fundamental to long-term durability of the business. And then also, when we land those customers, expanding them are really important. We have one of the best-in-class net revenue retention rates, this really drives stability and expansion into our customer base.

We're able to expand our customers on a lot of the AI workloads that Christian and Sridhar talked about. When we go to our customers, we sell business outcomes, which is really helpful. I got a lot of favorite charts in the deck, but this is one of my favorite charts. With the high gross retention in all cohorts expanding, you can see from FY '19 to FY '20, FY '21, those customers are delivering the majority of the revenue this year. And so with the land motion, then they expand over time with the high gross retention rate, this is really a powerful revenue engine for the company. We do that through a number of different ways, but I want to touch on migrations and use cases.

Migrations from FY '25 to FY '26 grew 1.9x. Use cases grew 1.7x, very meaningful increase. We actually are able to get this wallet share from a number of different sources and where the real benefit comes in for us and our customers is when they're consolidating all this into a single platform at Snowflake. All right, let's talk a little bit about sales compensation. We use sales compensation to incentivize growth. You can look in FY '24, we did not compensate on new customers. We made that change in FY '25 and it really paid off in FY '26.

We actually will go through and continue to make tweaks to the sales compensation model to get the most out of the sales organization to deliver the most for our customers. This is the fundamental pillars of our sales incentive compensation. We announced a new CRO in first quarter, JB as we call him. there's really 2 core focus that JB has. One is stability and two is AI.

From a stability perspective, JB has been with the company for over 10 years. He actually -- we joke about it internally that JB actually bleeds blue blood because he's been here so long. He actually pioneered the use cases to customers, which is used throughout the entire sales force today. He's taken that and other things that he's learned and actually using that to leverage AI. Every rep today within the company uses CoCo and CoWork. When we go to a customer, we're actually using synthetic data and creating applications to deliver outcomes to our customers. We've actually changed the way that we're selling to our customers and do an outcome-based pricing.

So our reps have first-hand knowledge of the capabilities of our products and how to deliver that. We're extremely pleased with the first quarter that JB delivered and look forward to many more quarters. So AI accelerates growth. I got 3 charts up here. If you look at the chart to the left, the sales cycles are accelerating. When we -- when I went back and looked at the average days sales cycle for this last quarter, it was the lowest in the last 4 quarters. You would expect with more choices and more evaluation out there that the sales cycle has actually expand and actually take longer, they're actually doing the opposite of that.

So the sales cycles are accelerating. We constantly talk about how we are using our AI tools to actually get new customers to consume faster. We've taken that from 10 months down to 7 months and we're continuing to see how we can decrease that. And then for all customers, migrations are accelerating. And so we've shown a 40% improvement. And so AI across the business is having a dramatic improvement on our time to ramp.

All right. Let's talk about a couple of customer examples. Before I dive into the specific examples, I'll talk about some broad trends that we're seeing. And so one of the things that we talked about on the last earnings call was there are secular tailwinds that we're actually benefiting from in the overall industry. And then second is CoCo is actually expanding our personas that we're selling into and allow more people to consume. And then thirdly, in our base business, we saw an acceleration of the base in the last quarter as it relates to CoCo and the secular tailwinds.

And so this particular customer was a large customer that was an equipment company, and they adopted Snowflake cohort. And they adopted cohort because they had over 1,600 locations and the reps were having a tough time getting the information out to the customers and answering them in a unifying way. And so they use AI agents to actually build the responses with CoWork and they're able to answer with greater consistency across all the 1,600 locations, faster answers and increase the customer satisfaction. If you look at the next example, this is a semiconductor company.

They originally bought -- deployed CoCo to optimize their queries and save money. Their supply chain department then actually picked up on CoCo and start using them. And within the supply chain department, it was -- they were having a problem because it's really complex manual calculations on ordering inventory. Through the use of CoCo, they're able to decrease the time, increase the accuracy and reduce the cost. And so this is another example of how we've seen CoCo play out in our customer base. In both of these, as you can see, CoCo is actually increasing the consumption of those customers.

All right. Let's talk about how this is working at Snowflake. So I've joined Snowflake a little less than a year ago. And when I first got here, I started playing around with AI tools. And I can tell you that CoCo has dramatically changed the way that I work. I worked so differently today than I worked a year ago. I think each of us with AI are trying to retrain the way that we actually work. And so I'll give a couple of examples on this. I've talked to some of you about my good morning CFO skill. So every morning when you come into the office, there's probably a number of websites you go through, reports you look at, structured data, unstructured data. When I get in the morning, I go into CoCo and it's like, good morning, CFO. And it basically takes all this data from structured to unstructured sources and actually puts it into an easy-to-read format within minutes. And I'm able to go through changes in the sales forecast, new hires that joined the company, customer releases and what's going on from a news perspective, major account wins, a number of different things. But not only can I do that.

I can turn it into visualization, automation within CoCo. Our Natoma acquisition then allows me to connect it through our MCP servers to Gmail, Slack and so forth, at the application layer. So now I'm using CoCo really as a destination spot to actually work out of in the morning where it's bringing all this stuff together saving an immense amount of time and allow me to actually send e-mails out around the world, understanding all this data in one simple place. It's also changed the way that I actually work with my FP&A team. And so historically, you'd have a list of reports that you periodically get.

And on those reports, it'll always be like one number that you would look at. And you would say like, what's going on with this number. And you go back to your power user and say, could you go extract that data and actually give me another set of reports, so I can look at this data. And that process would go back and forth for probably 2 or 3 different times until you could draw a hypothesis about what the conclusion was. Now with CoCo, if I see something, I actually through natural language, not through a SQL query, it does it for me, go and query the data and inquire what's going on. And I can drill all the way down to an account level, to a product feature level and understand anything about the forecast.

And so it takes something that would take weeks to do down to minutes. We're also using CoCo in a number of different ways in the CFO organization. We have over 139 use cases deployed today. And as Sridhar said, there's heroes popping up all over the company. People love to use CoCo and see what they can do with it. So they're automating and transforming the way they work across every aspect. Let me talk about how this is resonating with customers. I have the good fortune speaking to a lot of customers. Two weeks ago, I was in London, I met with over 20 CFOs. And there's 2 trends that are actually emerging. One is there's a different persona that we're selling to. And two is there's a big -- there's a larger sense of urgency.

And so when you take some of those use cases into a CFO and show them what you can do through natural language, not through a list of static charts through a BI company. But what you can do through natural language and automatically drive that into visualization automation, like the light bulb clicks like that. There's a couple of accounts today where it's a CFO of a $10 billion company, where they're going to do a big contract renewal and I'm actually the lead with him on the purchase. And so we're selling to a new persona. So we're constantly going in and selling to CFOs.

The second thing is the sense of urgency. When I go to our customer executive center and meet with customers, not only are you seeing just the Chief Data Officer come in, you're seeing the entire management team, in some cases, the board, and in some cases, they're actually bringing in a whole list of partners and so it really is changing. I think when the newer models was released and now people are deploying AI more broadly, I really do believe there's a greater sense of urgency around deploying something.

All right. Let's get into margins and capital allocation. Sridhar and I are 100% aligned. You can grow while getting operating leverage in the model. You can see in FY '25, we delivered 6.4% non-GAAP operating margin. And on the last call, we just guided to over 13 point -- we guided to 13.5% over 2x within the 2 years. And we're doing that by keeping non-GAAP product gross margin flat at roughly 75%. We talked about the AI products have a lower gross margin than our core. So how are we doing it? We're doing it really 2 ways.

One is we're being extremely disciplined on headcount. And so last quarter, we reported absent of the Observe acquisition, net head count increased only by 17, the quarter before that, only 37. And so we're changing the way we work by using AI tools and necessarily not adding heads to get work done, but transforming how we're working. On the other hand, cloud spend has gone up a little. The offset of these 2 is giving us operating leverage in the model. The billing payment terms for the company have been really consistent.

Over 80% of the people pay in advance. You can see last year, it was 86%, 2 years before, that was 82%, but really remains consistent. There is some noise between billings growth and revenue though. And so you can see on the far left-hand side in FY '24, revenue grew 36% and we had 29% billings growth. But in FY '26 it has actually reversed. When our customers actually come to the end of their capacity or use the capacity that they purchase, they really have 2 choices. And we allow them to do either the following. They can actually do an addendum and actually extend the current contract when the contract renewal comes up or they can actually do an early renewal. And so this causes some noise between billings and revenue. But over a long period of time, this actually normalizes out. So if you look at the 3-year, they actually are normalized.

All right. Let's talk about GAAP profitability. We're super excited to announce this today and the leverage that we're getting in the model while seeing the revenue growth that we have. So we announced that we'll be GAAP profitable in 4Q FY '28. There's 3 levers to do this: revenue, operating expense and SBC we actually went and just played with the bottom 2, operating expense and SBC. This is not a discussion about FY '28 revenue. And so we're seeing greater operating efficiency and operating expense for modeling purposes to help you out, assume the same trend in SBC that you've seen for the following few years. And so we're at 41% of revenue. Last year, we were at 34% of revenue. And this year, we said we'd be 27% of revenue. So that should help you from a model perspective on how we're going to reach GAAP profitability in 4Q '28.

With that as well as we don't expect to do any large M&A. Okay, we'll jump into capital allocation. Three primary areas. One is organic growth, R&D and sales and marketing. You heard Christian talk a lot about from a product perspective, what we're releasing into the marketplace and the velocity that Sridhar talked about in his presentation. We'll continue to do that. From a sales and marketing perspective, it's really adding capacity to the capacity model where needed. We have about $800 million left of authorization, or $4.5 billion that was announced earlier. And then from an M&A perspective, we have typically done small tuck-ins on a buy versus build more of an acqui-hire perspective.

So in conclusion, we have a very large and growing market. We have durable growth drivers with the land and expansion motion that we have. Our customers are fanatical about the products and services that we deliver. AI is accelerating all aspects of the business. And we've given you the framework today for us to reach GAAP profitability in 4Q '28. So with that, I'll invite Sridhar and Christian back up on stage, and there will be some mic runners running around, and we have roughly, call it, 25, 30, 35 minutes, clock is still going up for some Q&A. So if you have some Q&A, please fire away.

**Question-and-Answer Session**

**Brian Robins**  
*Chief Financial Officer*

We got one up here. Karl.

**Karl Keirstead**  
*UBS Investment Bank, Research Division*

Okay. Great. Yes. Happy to kick it off, and thank you for today. Maybe this is for Sridhar and Christian. OpenAI did an event this morning. I'm sure you're too busy to have listened to the live stream, but they announced a new data analytics product. So the spirit of the question is how ambitious do you think the frontier model companies will be over time in vertically integrating down into the data layer? Or do you feel like the way this is going to play out in the next 3 to 5 years is that they'll partner with firms like Snowflake and your peers rather than go after it with first-party products?

**Sridhar Ramaswamy**  
*CEO & Director*

Yes. I can take a first cut at this. I think the market in front of them in the enterprise, which is to roughly get every company to rethink how work should get done, starting with things like software engineering is very, very large. I suspect that, that is where the bulk of their attention will go. Running products like Snowflake is -- it's a whole new set of both practical and operational skills. Having said that, I emphasize that software is changing so rapidly that people should not be in the business of making long-term predictions about what is possible and what is not. But that's my current best answer.

**Christian Kleinerman**  
*Executive Vice President of Product Management*

I don't think I have much to add other than a lot of what we talk about that acquiring data not so hard doing, so with correctness, with trust, with all of that. That's takes some more time. But I share the alertness that Sridhar has instilled in all of us, which is we just need to pay attention to what's out there, what's working, in many ways, I am seeing the dynamics with the AI model providers similar to what has happened with the cloud providers, where, yes, there may be some overlap but at the end, there were more complementary than not at many customer sites. And so far, it seems to be very similar dynamics.

**Sridhar Ramaswamy**  
*CEO & Director*

Yes. And if anything, just building on what Christian is saying, absolutely, that cloud providers, as you know, have data platforms. And -- but they also quickly get into this mode of yes, we both need to partner and compete. So in certain sets of customers, we will be competing, and we'll sort of stay separate in that and be in our lanes, while in others, we collaborate. We have an excellent working relationship with both the model providers. And I actually think that the world is headed to a place where most companies want certain amount of model independence. It doesn't -- you don't have to squint that hard to understand that being reliant entirely on one model provider introduces the same kind of dynamics that sitting on exactly one CSP does for your business, especially if it's large and ready.

And we didn't get as much into it, but we spent a fair amount of time making sure that both Coco and CoWork work effectively across all models. And as others, you saw the partnership with SpaceX, but we also watch the open source models carefully, where if their performance rises up, that's actually it's very positive for us because we rent GPUs from the hyperscalers, and we have excellent infrastructure teams that can help us run that at scale. And it obviously produces just different margin profiles than working with the large model makers. It's pretty early for all of this.

**Christian Kleinerman**  
*Executive Vice President of Product Management*

Let me add one more. Sorry, but we're ripping on each other. Your comment, we're starting to hear customers tell us, oh, I made a big commitment to this AI model company, but now I want to use the other one. And that dynamic, we saw with the cloud providers, and it's starting to benefit us, which is, hey, you may have made commitment to Snowflake, we'll give you model choice. And that I think would make me pause on do I want to go all in with one company in a world where nobody knows what the world looks like 3 months from now.

**Sanjit Singh**  
*Morgan Stanley, Research Division*

Sanjit Singh from Morgan Stanley. I think as a management team, you guys have been very front-footed in terms of acknowledging that the world is changing and it's changing fast. And even with the presentation today, I think you gave us a clear sense of where you're making your bets and where you're going to invest behind products. I'd love to get a sense of, having been at multiple of these Analyst Days, you guys have reached a tremendous amount of innovation in terms of products.

Can you give us sort of the real-time view of, I got a good sense of where you're focusing going forward. Are there parts of the product portfolio that maybe we've discussed before? I don't know, just container services, Unistore, the data engineering portfolio that you're pulling back because the world is changing and this is where you want the team to focus. It's more of a kind of like a portfolio allocation question, Sridhar and Christian, can you give us a sense of where we're headed.

**Sridhar Ramaswamy**  
*CEO & Director*

Yes. I think one of the principles I live by is all of us can have theories for what's a great product and what's going to achieve product market fit. But none of us are, in fact, capable of willing that into existence. And that's just how it goes. And by the way, all of the usual instincts that people have for how to build PMF into existence, which is usually some variation of I'll give them more attention, and I'll give them more people, like some unhappy combination of both of these typically produces the opposite outcome of actually trying to get product market fit. And so even in the world of AI, the thing that I told Christian, flatly in July, I was a sponsor, the first sponsor of the CoCo project. I told him, if by September, October, we didn't have traction, we should walk.

And because, as I said, everybody talks a big game about their ability to do things like super app announcements, galore, but PMF is something very special. And so in areas where we perhaps had a thesis for what could be, I would put something like native apps into that. where we made a substantial investment. In my mind, substantial investments in early products are a mistake, but you can't change the past. If we basically deconstructed that into what are the core capabilities that are -- that come as a result of that way of thinking. And Native app is just another way of saying, I want to share both data and code from a provider to a customer and have some rules for who can see what data and who can see what code.

And so we went, we deconstructed that into a set of capabilities, and we are not native apps as an end all be all concept for applications quite so aggressively. It's a very slimmed down team. And so we are being thoughtful about where do we pull away from and we -- or Vivek is actually really good at extracting leverage from the teams. I mean the SRE project, just like the ta-da part of the project, which is, hey, you don't need to spend so many time dealing with annoying pages at 2 a.m. in the morning. And so this concept called KTLO, keep the lights on, a bunch of our teams have this, that number has dropped by a lot.

And so Vivek side is here is like, okay, what am I getting for it? Or do we need to move some people from this team over to this other team where we think there is promise. So that kind of reallocation is very active. And where there are -- this is not product and where there are tougher decisions to be made about disciplines changing, Christian and I came to the unfortunate and joint conclusion that tech writing didn't need to be kind of like this independent job thing anymore. And we effectively disbanded the team. It gave us -- we got a bunch of grief because of it, but our take is like PMs are better at writing documentation today using a coding agent and a specialist whose job it is to write documentation. Like looks obvious in retrospect, but when you make it, it's still painful.

So I think we're being pretty flexible about where we are allocating, where we need to pull away from, and we'll continue to do that.

**Christian Kleinerman**  
*Executive Vice President of Product Management*

Actually, so 100%, I have more examples. For example, SPCS as a third-party customer bring your workload, yes, has not gone the way we envisioned it. But I just shared the cloud agent sandbox, that is enabling a lot of power to CoCo. That is the same team and borrowing technology from what was built there. The momentum with Notebooks, the momentum with Streamlit came from, hey, instead of pushing SPCS so hard as something external, make sure that you have a great rental environment. So some of that reallocation is happening for sure.

I'll give you one other example. The interactive workloads, that borrowed so many changes that have been done for Unistore which is why we were able to go turn something around in way less than a year. And the performance of that technology is amazing. So yes, there's for sure reallocation and there is reuse of technology we built.

**Brian Robins**  
*Chief Financial Officer*

We'll go right here and then.

**Sridhar Ramaswamy**  
*CEO & Director*

I just looked up the data analytics announcement from OpenAI, these look like lightweight skills that run on top of Snowflake. So we knew about this, I didn't quite make the connection. I think it's -- think of this more as a set of skills that let you answer analytic questions and can generate SQL for Snowflake but also a bunch of other platforms that have -- that were mentioned. I mean, first of all, it's not like under the data layer.

It's more about how do you use these from Cortex and this is something that they've actually talked to us about. I mean, I have to give both the model makers credit for being really good partners. You saw that with Daniela yesterday. We work effectively together.Yes, there will be some cases where they would prefer, obviously, to have Claude CoWork rather than CoCo, or Snowflake CoWork. That's fine. I think there's an element of maturity that we have about how we approach this relationship.

**Christian Kleinerman**  
*Executive Vice President of Product Management*

That's 100% calling into our MCP SQL connector, we gave them a quote on Friday.

**Aleksandr Zukin**  
*Wolfe Research, LLC*

Alex Zukin with Wolfe Research. I think -- and you guys are riffing on each other, I'll riff on Karl and Sanjit. The question, I think, a lot of investors and even customers have like we watch the presentation. It's full of innovation, it's full of new products. I think we're having a little bit of a hard time seeing or understanding the collapse of functionality and the consolidation of functionality across the models, the hyperscalers and the apps.

They all seem to be in this world of delivering you the answer that you want from any question that you asked. And so I guess -- I think I know the answer, the answer is CoCo. But the question is, is CoCo your way of driving a lot more consumption of the core? Or is it more about expanding beyond?

Like when Brian is talking about new personas that you're selling to, how those look, how those feel, the sales cycles, those lands, how does this landscape, like when is CoCo the right answer versus Claude Code versus Cortex versus whichever model Microsoft launched today?

**Sridhar Ramaswamy**  
*CEO & Director*

First of all, I think like CoCo and Snowflake CoWork are really like 2 sides of the same coin. They share an enormous amount of infrastructure underneath, it's just tailored for different personas. All companies, definitely Snowflake need to have a clear-eyed view of what they're good at. Everyone can aspire to more, but you need to be very clear about what you're good at. And we are amazing at being a data platform. And CoCo is all about how do you get value faster from the data platform.

It's pretty much how do you bring -- it's equivalent of your AUM, how do you bring more assets to be managed by Snowflake, either directly into Snowflake or on Iceberg, they're increasingly indifferent to those things. And then how do you take data through its value life cycle. And we feel very confident. And we have published benchmarks comparing Claude Code to CoCo on things to do with Snowflake. Of Coco being a really good, perhaps the best solution in the world for sort of working with Snowflake.

You can say like that's not a big deal, it's your platform. Yes, it's not a big deal, but it's not like everyone has the equivalent of CoCo for the products that they are creating, still is a lot of work. And while we have -- clearly, we have a lot of work to do in terms of driving CoCo adoption by each and everyone of our customers. It's still pretty early. When we talk about the 7,000 customers. It will be more the case that there's like one user that's gone and done it. It's not that they have switched over to this agentic way of operating.

And it's not like we have made migrations easy enough that anyone can migrate from anything into Snowflake. So there's work to be done. I would say in the near term, there's just -- that's where there is enormous potential for us. But it's sort of playing our game of be a good data platform. CoCo accelerates, everything that you can do with that data platform including creating products like CoWork that people can get even more value from. And so in that sense, CoWork is an expansion play from where we are, and it's early. And my aspiration, our aspiration there is that we get some mega deployment. When we first created AI products, and I'm positive. I said this last year here, I usually like having clarity about priorities.

When we talked about AI, I've always said create world-class products first, like that matters more than anything else. Great products that customers love, get marquee folks to adopt the products that you create. And any such breakthrough is inevitably, exceptionally difficult because you have to prove and you have to get the customer to trust you and then drive scaled adoption, then drive revenue. The margin will come if you have done 1, 2, 3, 4, right. CoWork has to go through this kind of a motion. Snowflake intelligence, it's predecessor, which is mostly an analytic product, has done well. It placed us firmly on the AI map. We generated a lot of momentum and relevance for Snowflake as a product but CoWork is like a giant step ahead in terms of the things that it can do.

But we very much have to prove ourselves in terms of getting the product deployed by large departments like we have with Snowflake. And the fact that I can get Brian to talk to every CFO and look them in the eye and say, this is all I transform, how we operate is a huge asset. And it's the same for JB and team. But we have to translate that into the logos, into the 10,000 user deployments. We have to get customers happy with the cost of spending money on AI. We have to convince them that the per unit cost of using CoWork is a lot less than aim for some number of -- some amount of subscription software. So that's the potential, but I'm the first person to say, like, that is early and we have to prove the scaled use cases to you.

And between the 2 like CoCo sells itself. Why? Because we have, whatever, 14,000 customers that love Snowflake, I just go to them and say, everything you do with Snowflake is going to be 10x faster. They'd be foolish to not like go try it out. CoWork, we have work to do to sell it and prove ourselves.

**Brian Robins**  
*Chief Financial Officer*

No. We got one third row right there. Can you just try to get the microphone a little bit back.

**Ittai Kidron**  
*Oppenheimer & Co. Inc., Research Division*

Ittai Kidron from Oppenheimer. Maybe I'm going to ask a little bit of Alex' question and the opposite of Karl's question a little bit earlier. Going back to CoCo. Sridhar, the first thing you said in your presentation right here right now is that data gravity is a major advantage that you have compared to everybody else. And on top of that context, which again, you have compared to everybody else, if we skip forward in time 2, 3 years, How do you think about what CoCo can really evolve and develop into becoming because Karl asked the question of what happened if the model companies go down into the data.

I would argue that based on what you've said, you have a far greater improvement and advantage right here right now. Why not go aggressive upwards, not into the model itself, but more general coding agents and many other things that you can attach to the data and the context that you bring to the table that others don't have.

**Sridhar Ramaswamy**  
*CEO & Director*

I mean it's a great question, but execution eats strategy for breakfast. I have the strategy, just have to get the other part right.

**Ittai Kidron**  
*Oppenheimer & Co. Inc., Research Division*

So what are you planning for us then 2 years from now?

**Sridhar Ramaswamy**  
*CEO & Director*

Open up the kimono a little bit. It's -- you should not be in the prediction game when things are improving by 20% every month. I'll just honestly tell you.

**Ittai Kidron**  
*Oppenheimer & Co. Inc., Research Division*

That's a toughest job for us. We're analysts.

**Sridhar Ramaswamy**  
*CEO & Director*

That is, I think, part of the conundrum of the world right now. I read this in this amazing book where he basically says all history writing is teleological. People usually write history by assuming that the path that you took to get there was preordained and then they write the history. I think it's just really hard to tell right now. I think we have clear ambition. We have a team that is willing to execute and live up to what we think other companies can be. We have value to show.

But the rest of it whether we do it with our own people that can help with deployment and set the stage for what is possible or whether we come up with a set of effective partners that can drive change through a lot of customers. I think that is part of like difficult execution.

**Brian Robins**  
*Chief Financial Officer*

We'll go over here to Rob.

**Robbie Owens**  
*Piper Sandler & Co., Research Division*

Rob Owens from Piper. Great day from a new product perspective. One thing I'd love for you to double-click on is just the data streaming opportunity. And is this something that's customer-driven? Is this part of your bigger vision as to where Snowflake is going to fit in the future? And the answer can't just be CoCo. It's got to be something else.

**Unknown Executive**

Actually, this is a very unique and -- please go for it.

**Christian Kleinerman**  
*Executive Vice President of Product Management*

No. So it's both. It's part of our core direction of travel, which is we want to help customers through the entire life cycle of data. And those are not empty words. It's truly the entire life cycle and there was a big gap upfront. Today, customers deal with technology that is frankly complex to manage and expensive to go from web logs and sensors and devices and apps and mobile phones all the way to Snowflake.

So one piece is directionally. But the other piece is we do meet with our closest customers. We have a forum we call it the Black Diamond Council. And the signal was, they are very clear. Like if you guys were to solve this, Snowflake style, we'd love to do it. And as soon as we started sharing details, the interest is very high. And maybe the third piece that I'll say that is very interesting in that space is there's a technological disruption happening there, which is the original streaming systems all kept the data in memory. Which made it insanely fast, but also incredibly expensive. And we've seen a number of entrants and players delivering something that has a separation of storage and compute.

The data is in cloud storage. It's materially cheaper, a little bit slower, and many customers have said, many of you companies that are represented here in the room saying, we're totally fine with that trade-off. All of these things come together, that's what led to the opportunity. And what's Sridhar have -- normally he reminds me on, literally one-on-one, but just said, like the thesis is there. Now it's on us to make sure that it's a great product and delivers on the thesis.

**Sridhar Ramaswamy**  
*CEO & Director*

I'll stress that point again. I think the act of recreating something is people tend to look at it much more as there's something over here. It's a product. It's some system that works. It's a company. And they think they can essentially deconstruct that and somehow get to that point. As many of you know, I spent a lot of time at Google. I used to have endless arguments with Larry about what innovation meant.

And part of the thing that he drilled into my head that stays with me to this day is you will never win by aspiring to be someone else. You have to find your path. It's a journey that matters. And that journey usually starts with a brilliant new insight. Much of streaming was designed for all of you, was designed to minimize the amount of time that it took to get data from the stock exchanges of New York; two, the data centers in New Jersey. This is like all of your teams wanted to squeeze that millisecond out. So everything was in memory, everything was RPC, like remote procedure calls, machine to machine, like people optimize the heck out of it. Obviously, it's sort of expensive. That insight that's been had a few times before, is that most people don't really care that data shows up in 20 milliseconds.

If it's 400 milliseconds, they're like, it's fine. Is it 10x cheaper? That's like -- that's the core underpinning of Datastream, which is still a bright new insight. By the way, if the model companies were to want to disrupt Snowflake, it has to be some new thesis like I can think about this just very differently. It's not, I'm going to compete with Snowflake and operate at 22.5% margin, whatever the margin they want to operate at instead of something. That's kind of -- maybe it works for Bezos once upon a time with the retail industry that was unwilling to see the Internet. It's just not something that works in a general way. And so it starts with this bright insight thought, this is how you rethink. I mean this is the origin story of Snowflake.

All of you folks know it. It started with that one core kind of thesis. But still, it's the journey that matters, whether we can create a successful product, get people to adopt it. There's a lot of hard work ahead.

**Brad Zelnick**  
*Deutsche Bank AG, Research Division*

Brad Zelnick, Deutsche Bank. Great Summit. I mean it feels like an innovation blizzard this year. So hats off to the entire team. I guess my question is in a world where enterprises are overconsuming tokens, beginning to question ROI and even putting in curbs and usage limits, it was great to see, Christian, in your slide comparing CoCo plus CoWork and the promise of sense ahead versus general-purpose codegen. How does Snowflake position itself to be insulated from an inevitable wave of token optimization to come and even be part of the solution and to be able to benefit from it?

**Sridhar Ramaswamy**  
*CEO & Director*

Yes. I think absolutely, how much tokens are used, what models are used, what cost is a big issue. But I also think there are lots of really good technological solutions that we feel confident. This is where having like control over the harness, the thing that's actually executing the plan is so very important. One of the things that one of the engineers and I co-developed together a few weeks ago, was a skill that would generate like a plan for how do you solve a complex problem.

And part of what you can do when you do things like that is you can have subagents work with smaller models. And similarly, I'll point back to our advantage, if there's an open source model that's perfectly great at some job that also happens to be hosted by Snowflake, we can use one of those models. You don't always have to use like the marquee name models for every job. In fact, we make these models available within every model garden and people run a lot of jobs using much smaller models as well.

Similarly, I think techniques like skill compilation, a skill is an English language recipe, but 90% of the time, the skill is actually doing something fairly deterministic. You don't need a fancy element to do the deterministic part. And so there's an experimental project for the most common use cases or value skills, how do you compile that thing down into code where basically the code is involved instead of the big giant LLM interpret, the English. So I see a slew of techniques like this show up as there are concerns about cost. And honestly, we also want to put them into products like CoCo and CoWork as we continue to innovate with them.

One of the things, ironically that Christian and I are quite happy about is that things like Snowflake optimization is a lot easier with CoCo. And even though people optimize more with CoCo, we actually get more consumption anyway because they just do a whole lot more. And that's the benefit of a general purpose Swiss Army knife like tool that CoCo is. And we have already worked on things like per user limits, per account limits or how much some tool should be used. In fact, I'm having a conversation with a company about deploying CoWork for 3,000-odd sales folks within that company. And part of the guarantee that they want is a per user limit.

And our model, which is pure consumption.

We don't charge a per user fee for CoWork is actually very beneficial here because customers end up getting the best of both worlds. They can both place a limit on how much one user can consume. But if users don't consume anything at all, they spend 0. So you see little innovations like that actually be helpful, especially in a consumption model that starts at 0, that does not have a seat-based license. Many of the quoting agent providers do like a blended seat plus token pricing. And I'm actually pretty happy that we stayed away from those.

**Christian Kleinerman**  
*Executive Vice President of Product Management*

I'm 100% happy that we stayed away from per seat. The other thing is -- it doesn't fully inoculate us, your question is actually very insightful and valid. But we did learn a lot on when someone is consuming with Snowflake, let's go and have a conversation with the customer and make sure that it's valuable consumption. If there's -- I have lots of medium-sized regrets, but there's one big one from my time at Snowflake is, when things were going amazing and all of you were grabbing your models. We never went to and asked the customer, are you getting value out of this?

And we learned that and we're not going to let it happen. Is there a risk of some technical disruption that changes? Sure, we'll cross that bridge, but at least correlating value with spend matters a lot. And that's why the control that we talked about matters so much for us.

**Unknown Analyst**

Sridhar, if all these products take off, low 30% growth doesn't really feel right. I mean, it feels like this is a 40% market, your primary competitor is growing that twice as fast as you. So when you think about ultimately what you think these new solutions can do to help accelerate growth? I know you're not giving guidance here, but it doesn't feel like you're a cruise altitude from where the rest of the industry is at right now.

**Sridhar Ramaswamy**  
*CEO & Director*

I don't know what to say. Absolutely. .

**Christian Kleinerman**  
*Executive Vice President of Product Management*

We aspire for more, but showing is the new doing.

**Brian Robins**  
*Chief Financial Officer*

Right, our guidance is based on rooted observed behavior, and we did conservatively guide up this last quarter. As we see things happen, that's when we'll update our guidance.

**Sridhar Ramaswamy**  
*CEO & Director*

And having said that, I can't resist the ask for a GAAP profitability guidance from said person you mentioned.

**Michael Cikos**  
*Needham & Company, LLC, Research Division*

Mike Cikos with Needham. Given the larger number of personas you guys are addressing the applicable use cases, can you talk to the population growth within your existing customers? Like you're obviously not a seat-based model, but I was trying to make an analogy to your NRR, how is that seat growth trending within the existing customers. Are we actually seeing an acceleration in the number of seats for those organizations?

**Christian Kleinerman**  
*Executive Vice President of Product Management*

I do think that we're seeing a broadening of the reach of Snowflake but as Sridhar said, when he was talking about CoWork, it is harder to go beyond our core audience. But those examples that we're quoting on, we have customers say, hey, I'm going to put this in front of 500 users, 600 users, 3,000 users, it is happening and it reaches different functions and disciplines. So I still think that it's early on in our journey with CoWork, convincing customers to deploy something to every employee in our organization. It takes time, it takes effort, and we're very early on. So from a number of people that in an organization that leverages Snowflake, we're very underpenetrated. But to be clear, we just started on that journey.

**Sridhar Ramaswamy**  
*CEO & Director*

And this is something we track pretty extensively internally in the context of Snowflake intelligence/CoWork which is the number of unique users for each of the customers that we have. How do we drive that up, how do we get entire departments to adopt it. The journey is still early. Hopefully, we'll have more updates for you in the coming quarters.

**Brian Robins**  
*Chief Financial Officer*

We got time for one last question. And so Keith, if you could give the microphone to someone for the last question, then I'll wrap it up.

**Adam Tindle**  
*CGS International*

Appreciate it. Adam Tindle, Raymond James. I recognize the announcement on GAAP profitability is going to play well to this audience, but I want to ask a challenging question on that, Sridhar, you outlined a generational growth opportunity. Brian talked about the TAM here. Your business is accelerating. Why is GAAP profitability important at this juncture and why not pour more investment in now versus being governed by this promise?

**Sridhar Ramaswamy**  
*CEO & Director*

Because it isn't clear that simply throwing more humans at problems gets more things done. That's like my honest assessment. I think more of my energy should go into having each and every one of my engineers think and act like the person that like reliably got the feature out in 2 hours. That is going to drive more leverage for us than simply hiring more people. And the other thing that you should also take into consideration is similar to the point about tech writing, there is a transformation of the workforce itself that is going on, where pretty much every team, this is not just engineering or sales is going to be quite different.

And we are going through a process internally for what does it mean to have a particular function operate in a true AI forward way. What does the team structure look like? What do the job definitions look like? And how do you go from here to there? And so beneath what looks pretty conservative, there's a massive amount of churn and reinvention that are going on. I think, as I said, I will end with like scale no longer needs to be driven by the number of humans that you have working on some problem, getting super linear scale from highly effective people is what business is going to be about.

**Brian Robins**  
*Chief Financial Officer*

With that, I want to thank our IR department and all the other Snowflakes who make this event possible, and thank you for your support. Have a wonderful day and enjoy the rest of the Summit. Thank you all.