---
ticker: S
company: SentinelOne, Inc.
title: "SentinelOne, Inc. (S) Discusses Independent Evaluation and Findings from Security Operations Market Report Transcript"
published: 2026-07-08T16:02:27-04:00
article_id: 4920701
source_url: https://seekingalpha.com/article/4920701-sentinelone-inc-s-discusses-independent-evaluation-and-findings-from-security-operations
---
SentinelOne, Inc. ([S](https://seekingalpha.com/symbol/S#source=section%3Amain_content%7Cbutton%3Abody_link "SentinelOne, Inc.")) Discusses Independent Evaluation and Findings from Security Operations Market Report July 8, 2026 1:00 PM EDT

**Company Participants**

Molly Maguire  
Anthony La Scala

**Conference Call Participants**

James Berthoty

**Presentation**

**Molly Maguire**

Hello, everyone, and welcome to this webinar. Before I hand things over to our speakers to officially get things started, while people trickle in, I'm just going to review some housekeeping items.

So first things first, this webinar is being recorded, and a copy of the recording will be sent to all registrants in the next couple of days. So look out for that in your e-mail, you can share that with colleagues or have a rewatch if you need. The second piece is that we are live. This is a live webinar. Our speakers are here. So you can use the Q&A box on your screen to ask them questions. And if we have time, we will be going over those at the end. We also have some moderators in the chat who will be able to answer some specific questions for you there. And then we also have a resources box on your screen, and that has links and downloads related to today's topic. And lastly, if you are a member of ISC2, CPE credits will be automatically credited to your account in the next 4 to 6 weeks from this webinar.

So again, this is being recorded and, a copy will be sent to all registrants in the next couple of days. And now that we're about 1 minute, 1.5 minutes in, I think that most people have joined. So I'm going to hand it over to our speakers, and they will get started. Anthony?

**Anthony La Scala**

Awesome. Thanks, Molly. Welcome, everyone. Glad you're here. We have a packed agenda designed to cover a lot of ground in 30 minutes. So I want to get right into it.

Security operations is one of the most crowded categories in our industry right now. Every vendor has a take, and most of them have slides that look pretty similar. What's genuinely hard to find is an independent evaluation built on real hands-on testing, not vendor submissions. Latio has just published their inaugural security operations market report, SentinelOne earned the SOC Platform Leader Designation. And today, you're going to hear directly from the analysts who evaluated us, see the data behind the report and watch the platform in action. Let's get into it.

My name is Anthony La Scala. I am Principal Technologist at SentinelOne, and I'm joined today by James Berthoty, Founder and Analyst at Latio. James, welcome. Great to see you again.

**James Berthoty**

Hello. Thanks for having me. Happy to join and talk to everybody.

**Anthony La Scala**

Yes. We are thrilled to have you join us today and chat about your background, Latio and the inaugural Security Operations Report. Before we get started, I'll give our viewers a quick look at the agenda.

All right. So we're going to start with introductions and a quick glance at James' history and why he built Latio the way he did. Then we'll cover the research behind the report, the categories evaluated and James' definition of a modern SOC platform. Before I dive into the platform, we'll discuss SentinelOne's ranking as platform leader, including our meaningful differentiators. I'll wrap things up by showing you the Singularity Platform in action, and we'll leave a few minutes for Q&A at the end. All right. With that, let's get things started.

**Question-and-Answer Session**

**Anthony La Scala**

All right. So James, tell us a little bit about your background. What does Latio do? And why did you build it the way you did?

**James Berthoty**

Yes. I'm super glad to talk about this. For the last 15 years, I've been a security practitioner, and so I worked across security operations teams in a big MDR environment, and then into cloud security and application security, was involved in compliance automation. So I've really touched most aspects of security. And the big missing piece that I found just from doing analysis and trying to find tools was the headache of, first of all, understanding like what a vendor actually does and what their security tools are actually capable of because everybody tends to use the same language to talk about pretty different things.

And the second piece was that there are all of these opinions that are out there and rankings of products and talking about how they work from people who don't even use or get hands-on time with the products. And so the #1 thing that we try to do is actually use the products, get a clear idea of the use cases, understand who they're actually built for and then just make that really clear to practitioners of like these are the circumstances under which you should look at vendors in this category, and here are the most relevant ones to look at based on our times in the tool.

**Anthony La Scala**

Yes. And that makes Latio genuinely different from how most of the analyst firms work, your hands-on keyboard approach. So this was Latio's first security operations market report. Why SecOps and why now?

**James Berthoty**

Yes. I think for a while, the SecOps industry has sort of -- was this consolidated like you have an EDR tool and you have a SIEM. And those were sort of the debates that were happening, and there weren't a lot of movement or specialized players within that. And then you had the evolution of like data pipeline tools and taking a lot more different approaches of how you can build an end-to-end SOC experience outside of just the EDR and the SIEM. And then, of course, there's a lot of movement around AI SOC and a hodgepodge of different vendors getting shoved into that as an emerging category. And once again, those are all pretty different and unclear, like the differences between one another, even though they all say the same thing.

So that's basically what we look for when we do a report is when there are a bunch of vendors saying they do the same thing, even though they're all pretty different. And so that's why the security operations industry is ready for evolution across all of the core technologies as well as modernization on those things. And then the data has to become more accessible than ever to enable teams to actually use AI beyond just this is a SOAR, but now has a chatbot in it.

**Anthony La Scala**

It always starts with that data foundation, which I know that we're going to hit on a little bit later today. So how many vendors did you evaluate for this report? And what does that process actually look like? Like are you running real attacks reviewing documentation or evaluating demos?

**James Berthoty**

Yes. So it's a mix of all of those things. We generally try to do about 50 vendors. Sometimes I get too excited with our reports and do like up to 100, and that is always complicated. But yes, we try to get as hands on with the tool as possible, sometimes because of the nature of certain tools, we can't get hands on. And in those cases, we try to look at test environments and get really granular in the demos that we're going through with people, always looking at the documentation and understanding the use cases to then understand like the relative maturity of those use case capabilities and mapping them to the use cases that practitioners have.

**Anthony La Scala**

Awesome. So what were your expectations going in? Did anything about SentinelOne's approach surprise you?

**James Berthoty**

Yes. I mean I think for a long time, the differentiator with SentinelOne was being very early to invest in a data lake architecture. And so if you have a lot of history in SIEMs like I do, like the Elastic Stack is how most of these things work, where they're ingesting logs and doing a bunch of crazy data optimization strategies to make search possible across them. And what gets lost in that is you're treating logs isolated from their larger environmental context.

And so I think SentinelOne like made an investment a long time ago, that's really paying off into building a data lake architecture to where there is asset context, combined with the EDR telemetry, combined with just general SIEM telemetry and now augmented by the SOAR and data pipeline technologies as well to where now SentinelOne is one of the few providers that actually has like a competitive offering across every lane of those independent pieces of building a SOC platform and then putting all of that together to deliver results that whether it makes AI querying underlying data easier, or it's about driving like that asset context and making it clear to people where the alert sits in their environment. Those are the things that I think really are at the heart of paying off now as many vendors are trying to rebuild their architecture into more data lake pieces. Yes.

**Anthony La Scala**

Data, data lake foundations, it's going to be a recurring theme today. But no, I'd love to hear that from you. And it's also a great segue into the report. So let's dive into some of the survey results here. Now we're setting the foundation on what tools teams are using. So our research found that most teams use an MDR managing SIEM and EDR. Tell us more about what this means for dedicated SOC teams?

**James Berthoty**

Yes. I think there's really trends across all 3 of these. And the first is really interesting, even though it's the vast minority there haven't invested in SOC. I think it's important to talk about because a lot of cloud-native organizations, like their security journey sort of started with CNAPP and then is evolving into the other pieces. And so they don't have a traditional understanding of security operations of sort of that EDR plus SIEM combination. And really for them, it's about expanding what does log collection look like for us outside of the cloud more specifically. And they're sort of expanding into the traditional to endpoint telemetry as they're sort of having to builds, Entra ID and all of these, like Windows components creeping their way into their architecture over time, like those companies are sort of transitioning into that MDR category.

And I think that's where really running a SOC is really hard, and it's also just really scary. Like if you're a 1- to 5-person security team, which is a lot of like the mid-market for security, you might have the technical capability to run a security operations team. But first of all, you're going to get like drowned in alerts. So if you're not constantly tuning all of the rules and making sure everything is up to date. So nobody wants to do that alone. And then responding to an incident, like I've had to respond to a bunch of incidents, and it's really scary to do it alone. Like there's times I've been the only on-call person and being the one who has to like wake everyone up is a big thing to do. And you never want to feel like you're -- like the tug-and-pull of am I making a big deal out of nothing? Or is this a critical incident that I'm overlooking? Like that's something that people want partnerships to do.

And so even people who have dedicated SOCs are typically augmenting with some kind of managed service, whether that's like threat intelligence or forensic services, like really operations is a team sport, and everyone is sort of getting involved. And I think that's the theme that we saw with a lot of the data.

**Anthony La Scala**

At 2 in the morning, every log, every alert looks like a full-scale breach. So no, I totally understand that. And we have a little bit more info on the tools that teams are using here in this next slide. So SIEM and EDR technologies, they're remaining at the top for monitoring security operations, how does this impact a customer security environment?

**James Berthoty**

Yes. I think this is just -- this really highlights that there have been a lot of start-ups over a long period of time who have tried to eke out some of these subcategories. But far and away, the backbone of the SIEM -- of the SOC is the SIEM and EDR technologies. And this goes into when we talk about a modern security platform. At this point, just the vast majority of people that we surveyed for the report, my own experience is wanting to have it at a bare minimum, someone who is combining the SIEM and the EDR offering into a single location because it's constantly this tug-and-pull on how many -- how much of our EDR telemetry should we send to our SIEM? Is that enough? Is it too much? And that is a huge bulk of the telemetry in and of itself in the day-to-day work. and having SOC analysts have to like pivot between the data, write all these custom searches to stitch that data together, creates a lot of just the friction of just trying to manage those 2 technologies. Never mind if you're trying to bolt on like a data pipeline tool in front of it, a SOAR on the back end of it and trying to build automations. Like there's a lot of complexity that gets introduced very quickly.

And I think with this, one of the things I was surprised to see is that a lot of people having multiple SIEMs is like a big talked about part of the industry because it certainly affects large enterprises who are on that. But I think more and more people are dealing less with having multiple full-fledged SIEMs and more with just having multiple places that have data that they want to access. Like if their data team is sending some stuff to Snowflake, sending things to Databricks, sending things to S3, like they want to be able to access that data as though it was native as well.

**Anthony La Scala**

Absolutely. And the -- we're talking about centralization here and pulling things together so that they're more unified. And so for organizations that have disparate tools, we're seeing actually a little bit of resistance or concern before they would migrate to a different SIEM. So there are concern that the migration may be not worth the investment? Or what do you think is the main driver of the dissatisfaction with current SIEM implementations?

**James Berthoty**

Yes. I think the general takeaway here is a SIEM is -- one of my first MSP jobs, there was a guy who said a firewall is a firewall, right? Like he doesn't care if they're using XYZ brand of firewall, like they're all going to work sort of the same. And I think a lot of security practitioners have that approach with SIEM, right, like a SIEM is a SIEM. Some of them have better query languages, some of them have worse ones. Some of them are a little better in one way or another, but they all generally work the same as sort of like the prevailing opinion because they are based primarily on an elastic type of architecture, even if it's not elastic happening, like that is the driver behind a lot of what I'll say like, SIEM technologies for maybe the last like 15 years.

But I think what we've seen is that architecture is rapidly changing to where now there are benefits towards more of these data lake models that make it so that everything from query time to flexibility to data storage to long-term storage, a lot of those concerns are finally getting addressed in an intuitive way. And I think that's pushing people towards being willing to migrate, but they're afraid that they're going to lose all of this 15 years' worth of detection engineering that they've done and log ingestion and log health and custom log sources, like everything they've built, they don't want to lose that in the migration. And so there's this delicate balance happening right now of teams that want to migrate because they see the benefit, but don't want to lose the technical debt that they've built over the last 15 years. And so I think a lot of vendors are trying to figure out how to help with that transition and make it as smooth as possible for people.

**Anthony La Scala**

Yes, absolutely. It's the usability of the platform, but also the ability to move the data in there. And we're going to be diving into the usability of the platform a little bit later. But I want to move on to the stat that you've all been waiting for, AI within the SOC. I know everyone here is tired of hearing AI, but it is the future, and it is a critical component of security operations.

And so the stat -- it really caught my interest. So in the report, you argue that AI SOC tools fit within traditional categories, but vendors mark them as if there's something entirely new. What's the real distinction practitioners should make when evaluating these tools?

**James Berthoty**

Yes. I think the first thing, and it's what this stat highlights is that we don't need to believe the hype that it's like if you're not doing this in-house or if you're not using an AI SOC tool, you're falling behind or you're in the underworld of security or something like far and away, that's what this -- 80% of people we surveyed when they talk about AI SOC as being a part of their budget, they are picturing analysts using tools like Claude to help in their incident response process. They are not talking about buying a new tool that does like agentic response actions or something like that. And so when it really is coming down to how do we help enable analysts with the best data access possible with the best AI tools possible to help speed up all of their end-to-end interactions.

And so then to answer the second part of that question of like how do we think about how AI SOC tools should be assessed in general. Broadly, you have a couple of different categories where there's ones that are purely focused on incident response, and they're just running a bunch of federated searches and having AI stitch the data together. And the challenge that, that creates is anyone who's worked in a SOC knows that searches are never just like, "Oh, I wrote a perfect search, and now we're done." It's a lot of trial and error and trying to stitch data together. And without direct access to the underlying data, things can get very complicated.

On the other side of like AI SOC solutions, you have tools that focus more on like the data ingest side or on the detection engineering side. And what those tools can do is like be really focused on the building of the detections and management piece, but they tend to do less on the incident response piece. And I think, all in all, it comes down to access to the underlying data and getting that to an agent in the most effective way possible. And in my opinion, teams shouldn't shoehorn themselves, as much as possible should avoid shoehorning themselves into particular vendor approaches for AI. Because at the end of the day, these tools are changing so fast, where we saw how quickly everyone was on ChatGPT and then everyone goes to Claude and then people go to Codex and then people like this stuff is changing so quickly that it's all about trying to avoid vendor lock-in.

**Anthony La Scala**

Yes, absolutely. And we're hitting on multiple points here. But when we talk about AI, you really also have to think about the underlying data. And the report's conclusion is essentially like fix your data architecture first and then automate. So James, for an organization that's still in the middle of that, still fighting data quality issues, where do you tell them to start?

**James Berthoty**

Yes. I mean this is -- every single organization out there is struggling with this. And I think, from my approach, it's starting with data pipelines. And that doesn't have to mean buying a data pipeline tool, that can mean manually tracking this in a spreadsheet or whatever. But you have to have a clear sense of what are your log sources and where are those -- what are the destinations of those log sources. And without tracking that and trying to figure out what are the applicable visibility layers that we need and where do those logs even exist when we need them, it sort of makes anything else that happens down the line even harder to achieve.

But then once you have that visibility, you have to figure out where is the best place for this data to live. And that's a very challenging question because for some organizations, and to me, it's just about being realistic. If you are a 1- to 5-person security team, you're not going to try to build or at least you shouldn't try to build the world's most distributed best-in-class data storage architecture of like this is in Databricks, this is in Snowflake, this is in SentinelOne, this is -- like you should pick like a simple all-in-one place to point your logs at. And so in the report, we have like a box for like vendor data lake solutions are like probably what you're going to look for.

But then depending on if you have particularly noisy log sources that you don't need to access on a daily basis, or you have ones that provide nice context for additional alerting, that's where you start to bring in other storage strategies to augment the approach. So just to reiterate for me, it goes to starting with the data pipelines to get that visibility, and then thinking about how do we want to route this. And then the final piece is how do we want to build detections on top of this? Do we have the detection engineering capabilities or tools to make sure that we're building detections on top of the relevant log sources? And a lot of that comes into wanting to maintain and manage your detections in a single place, hopefully, it's code, hopefully deploying out on a regular basis, but that itself is a transition, a lot of teams are trying to work on as well.

**Anthony La Scala**

Yes, absolutely. And it all goes back, we call it the foundation because everything else is really built upon it. So let's shift now to how Latio thinks about the modern SOC? And let's hit our report framework. In 2026, every vendor calls themselves an AI SOC provider. The category is real, but the marketing has gotten ahead of what most teams actually have in place. So James, let's ground this. How do you actually define a SOC platform? And what has to be there for it to qualify?

**James Berthoty**

Yes. I think it's sort of the culmination of everything we've talked about so far, where from a pure feature perspective, to me, it involves some sort of EDR offering because that's a core tenet of what the SOC does, some type of SIEM capabilities and then some kind of managed SIEM MDR capabilities. And really like at a bare minimum, those 3 pieces are what probably 90% of the security operations market is looking for from a core capabilities perspective.

And then when we talk about, okay, then broader picture, like how do we figure out which SOC platform to go with, this is where sort of this diagram comes in as far as like, here's what a traditional SIEM looks like and why it's so complicated. Because when I was a part of managing these SIEM architectures for tons of companies of all sizes in an MDR context. And you had 3 different full-time roles that are very challenging for teams to take on. One is a team that's actually doing the SIEM engineering and managing a complex SIEM architecture, especially if you're self-hosting it. The second is a team of analysts that are like doing the day-to-day responding to alerts. And then the third and most important was the detection engineering team or threat hunting team and trying to have them -- like they are the ones upon which everything else rest because all of the -- if the analysts are getting flooded with 500 alerts due to a bad rule, they are basically unable to work until the rule gets fixed.

And so a lot of teams, I think, would overinvest if you haven't done this before, like over invest on the analyst side and then wonder why the -- all of your alert metrics are off because the detection engineering team is the one that is the most significant to reduce those downstream burdens on teams.

But now we're really seeing that traditional locked-in architecture is really exploding as far as the diversity of people want to store the data where they want to be able to store it, and they want to be able to access it quickly and with flexibility. And so that's when we're starting to think about what does a modern SOC architecture look like from a best-in-class SOC platform? It's going to have more of that data lake architecture. It's going to bring asset context in together with the incident data, and it's going to allow teams to build detections, build ingest across a wide variety of storage use cases for people.

**Anthony La Scala**

Yes. Security always comes back to layers, and this is really what we're seeing with modern SOC architecture is you have that layering, that data foundation and building up from there. And one misstep, one wrong detection rule can negatively impact everyone downstream of that, the analyst downstream of that.

So let's dive into where SentinelOne landed for the SecOps market report? Now James, you named us, SentinelOne, the SOC Platform Leader. Walk us through what you actually saw in the evaluation that earned that designation, and what differentiated us from the other platforms you assessed?

**James Berthoty**

Yes. I think, it really comes down to those things we've been talking about as far as when it comes to what makes a SOC platform leader, it is that combination of covering all of the core use cases that a SOC would have, along with managed services, all built into the same place. And then around SentinelOne specifically, like it's how the data lake architecture plays into the AI SOC story, combined with some of the emerging like attack surface management, attack testing, like red teaming light approaches to find some of those exploitability issues and help with prioritization as well. And really just getting a ton of value for a security operations team to use SentinelOne as an all-in-one tool. And I think SentinelOne's primary strength is there's a genuine cohesion to how all of the products work together as far as building on top of that data lake architecture. As far as a lot of other platforms, you're like pivoting between pretty drastically different products in order to accomplish some of these same outcomes. But yes, it all comes back to that data lake investment early on.

**Anthony La Scala**

Starting with that solid data foundation and layering it from there with a unified approach, absolutely.

So let's -- I want to pull up some of what you've described here into a visual. So we've captured 6 areas where SentinelOne really stood out in the evaluation. And I think that this maps closely to what we've been talking about throughout the webinar. So the one that I want to highlight specifically here is AI security. So James, you described this as one of the most comprehensive AI security solutions you've evaluated. With the Prompt Security acquisition, we're covering everything from AI red teaming to MCP proxy controls in one platform. In a category that's moving this fast, can you say more about why the breadth here stood out?

**James Berthoty**

Yes. I think, even though our next report is the AI Security Report to plug it here. So we'll be going into some more depth on like AI security tools and what makes them good or bad. But I think, from our last report in 2025 on AI security, like Prompt Security was one of the clear leaders of that category. And of all of the acquisition -- because basically, a ton of companies did these like first-generation AI security acquisitions with different bets on what's going to help people the most, and it was a lot of like network security companies doing a lot of that. And I think Prompt Security stood out for both its breadth of different approaches very early on and was really a leader across like thought leadership and research and the tool itself in terms of delivering everything for protection from like ChatGPT-style plug-in monitoring to endpoint monitoring more in depth of tools like Claude as well as like the runtime access control pieces. And so it really just comes down to of the acquisitions to make.

I think the team at Prompt is a great one and continues to do great work. And yes, as far as comprehensiveness of a solution, a lot of other entries into the category have been through much more like niche or pointed offerings of things like model scanning or creating AI bombs or just runtime protection or monitoring. And so it really is that combination of approaches that creates the breadth that teams really need for AI security because it's moving so fast. And the best thing, most organizations are no longer talking to me about monitoring Hugging Face, for example, not because -- it's just not the primary use case anymore, even though there are many companies betting big and it's paying off in terms of like self-hosting a lot of this stuff. It's just not the primary use case compared to like Claude is the AI use case of the moment.

**Anthony La Scala**

Yes, absolutely. SentinelOne definitely backed the right horse, and Prompt has been a fantastic acquisition, a super strong team and the product is incredibly strong. I've gotten to play with it and demo it myself, and it is incredible the protections that you can implement on AI now, especially as enterprises are adopting them at en masse. Now what ties all of this together is that unified data plane though. And so with Purple AI, which is our AI within singularity, being able to reason across endpoint cloud and identity logs altogether all in one place, is really an important differentiator for us because we're pulling in and able to analyze the data without switching to different consoles or separate products to be able to actually understand the full story.

So let's -- I want to pull what you described here, and this quote is from the report and it says, I'll just read it directly actually here. SentinelOne is a strong fit for organizations, either looking for a complete security platform or those with endpoint coverage looking to extend into SIEM, AI SOC and AI security without adding vendors. So that's really 2 conversations we have most often with customers. Organizations who want one place for everything and those who started with endpoint and are ready to extend the platform they already have. Either way, there's no new vendors, no new contracts and no new data silos. James, any final thoughts before I show what this looks like in the platform?

**James Berthoty**

Yes. I think I really just want to give a practical example of why the single data model matters for the AI queryability of things because the way most tools in this category work from like a start-up perspective is basically having AI write queries across different tools. And that's what creates a lot of surprising either results or hallucinations or things not working or driving costs up because at the end of the day, they don't know if the data is there or not. And so they're trying to infer and build memories over time of like, here's how your log sources work, here's how your data structures work across all these different SIEMs. And then they're trying to write federated searches across a bunch of different data sources. And that's really what creates the mess is like the AI just doesn't have the full context to understand what's going to be there when it goes to look for it.

And that's the key challenge that drives up costs and drives down performance of a lot of these systems. And that's why whether it's SentinelOne or any system, like having a consolidated data model or even if you're buying a start-up in this category, it's like it's just important that they are also trying to map and consolidate the data in some way and that it's not just the AI doing like a best guess over and over again to try to see if that data is there.

Because the other thing is what's really important when you're doing an investigation is knowing what data is not there to understand like, is there a way you can make an actual judgment on if an incident happened or not. Sometimes it's really important to know we can't make that judgment because we need to turn on the firewall logs or we need to turn on the endpoint logs or there's something that got missed. And really, it's just that full context of like what is and isn't there is so important for making these things work effectively.

**Anthony La Scala**

Those are the gaps in visibility that threat actors live in. And so having all of that data available, queryable, and searchable within one place is critical. So now I think it's time that we dive into it. For anyone who hasn't seen the platform, I'm going to show you some of the moments from the evaluation that map directly to what you've been hearing from James.

Every SOC starts with the data problem. Teams burn hours normalizing noisy, inconsistent telemetry, storage costs spiral, analysts work off low fidelity signal, acting as data janitors instead of defenders. Most SOCs investigate only about 20% of the alerts they see in a day. Observo AI changes where that work happens. In its stand-alone console, you watch the pipeline filter, enrich and route data in-flight before any of it's ingested. Observo cuts noise by up to 80% upfront. Analysts start with clean, high confidence signal instead of raw low-fidelity noise. When the data is right, every downstream tool performs better, and every decision is more confident. That is what turns data janitors into threat hunters.

Before an attack begins, the smartest move is to find the door an attacker would use and close it first. That is what the offensive security engine does. Most vulnerability management ranks findings by CVSS score, a theoretical measure of how bad a flaw could be in principle. OSE goes further. It safely tests your live public-facing assets the way an attacker would and shows you what is genuinely exploitable right now.

Here is a Log4J Remote Code Execution finding. This is not a severity rating, it is proof. You can see the actual exploit evidence, the JNDI-LDAP string OSE injected and the DNS request that came back confirming the callback fired. The vulnerability did not just score high, it executed. That is the difference between a list of theoretical risks and a verified path into your environment. OSE tests real assets, not hypothetical scenarios and surfaces evidence of exploitability instead of a number. So you harden what an attacker can actually reach first, proactive hardening backed by proof before anyone has to respond to an alert.

Now the threat arrives. Attackers achieve lateral movement in under 48 minutes. This scenario is modeled on Scattered Spider, social engineering into identity compromise into cloud lateral movement. The question is not whether an attack will happen, it's whether your team can move faster than the attacker. Traditionally, an analyst chases that attack across 5 or more consoles, correlating alerts from different tools. Unified alert management removes the pivoting. Native SentinelOne alerts sit in the same queue as Proofpoint phishing detections and Palo Alto command and control alerts, same format, same enrichment, partner intelligence surfaces right alongside your own with the same context. Faster triage, no context switching, analysts stay in one view.

Piecing that attack chain together by hand takes hours. Behavioral AI does it automatically. It flags OS level events as they happen and maps them to MITRE ATT&CK, drill into storyline and the full attack reconstructs down to the command level. From initial access to lateral movement, the story assembles itself with 0 manual correlation.

Here is the reality most teams live with. Most alerts are never investigated. The ones that are take hours because the analyst hits the bottleneck. Watch what happens instead, a critical EDR alert fires with a malicious detection, an agentic investigation triggers automatically with no analyst action. By the time anyone opens the alert, the report is already waiting. It carries an AI verdict, an executive summary, key findings, a threat summary, a full time line and recommended next steps. The investigation is complete before the analyst even looks. Verdict-ready, actionable from the start, response is just as immediate because hyperautomation already fired on the true positive verdict.

Normally, the analyst creates the ticket, notifies the team and works containment one step at a time. that administrative work burns hours. Here, a single true positive verdict triggers 1 playbook. It notifies Slack at once, opens the Jira ticket and provides containment options directly within that ticket. The execution log shows the average resolution time. Response executes across every tool in the stack from one trigger. SentinelOne's own SOC runs this way, resolving alerts in an average of 4 minutes across 250,000 alerts a month.

This extends to managed service. MDR is usually opaque. You get expert coverage but lose control of the response logic. Here, MDR actions and escalations feed directly into hyperautomation. MDR becomes the trigger, hyperautomation becomes your customizable response layer. You get the expertise of a managed service and the freedom to define what happens next.

All right. All right. Thank you, everyone. It's time to get into questions. We've got a few minutes. Let me pull up what's coming from the audience here. James, for a security team starting their SIEM evaluation today, what's the first question they should ask a vendor before anything else?

**James Berthoty**

Yes. I mean the short version of this is to ask to see a demo. I know that was always my first question that I would always have. But I think the things to look for through a demo or through the questions is trying to really understand, first of all, their underlying data model and trying to understand the -- how that data model is going to map to the day-to-day operations of your environment?

I think just I can use like a mistake I almost made early on in my career was I was doing a lot of DevOps work. We had a lot of work in a DevOps tool. I wanted to use that as our primary SIEM. But I was taking a pretty selfish approach because we had an existing SOC team that had a different SIEM for their use case. And I think it would have been the wrong decision for us to try to like split the data in that way to try to make teams happy like that, and that's how you end up in this sort of like sprawling data mess.

And so I think it's unfortunately like a series of compromises that teams have to make to try to pick a place where you're getting the most value out of having as much consolidation as possible or taking the opposite approach, frankly, and trying to take on the burden of you want to store the data and ingest it however is best. And then you're asking yourself, okay, how am I going to run unified detections across this disparate data architecture that I'm going to have.

**Anthony La Scala**

Yes. Avoiding data silos and making sure that everything is monitored or unified in a way where it can be monitored, absolutely. Now I want to -- I have one from me here. Is there a category in the evaluation where you expect your vendors to be further along than they actually were?

**James Berthoty**

Yes. And it's really a flip of -- you can almost see the top-down demands around AI optimization that are happening because, frankly, I was shocked at how advanced most AI features are from most of the larger platforms, like including SentinelOne, to be frank, where most major providers have SOAR capabilities at this point that they have really rushed to build AI capabilities on top of, whether that is like a chatbot or like an agent builder or an orchestration layer. Like teams invested, especially the platform players invested really quickly into AI SOC-style capabilities. And so I was surprised at how quickly those have materialized.

I think what's been slower to materialize is some of that underlying data flexibility support from people where there's -- basically, there's 2 pressures that have happened at once. One is on the -- towards the being able to run decentralized detections across all of your environment and the other is the AI push. And teams really, by and large, invested in AI first and then are still trying to figure out their approach to consolidated versus distributed data architectures.

**Anthony La Scala**

Got you. So we saw organizations pushing the AI before the data and now needing to really rebuild that foundation that we've been talking about.

**James Berthoty**

Yes.

**Anthony La Scala**

Awesome. Well, it looks like we have one last question here. For practitioners in the audience who don't know what OCSF is, why does it matter for day-to-day investigation work?

**James Berthoty**

Yes. I think OCSF is really fun because it reminds me of like open source security tooling where you either have almost no opinion and don't care at all, or you are super in the weeds and have like an incredibly strong opinion about it. And so I tried to tread really lightly on it because I think OCSF is an amazing initiative with a goal that is really important around knowing how do I -- when I query data like an IP address, I want a standard way to do that. And there are so many different logs that have similar enough log types that it should be simple to do that.

And where that becomes especially important for AI is because it needs to know if the data is there or not, like we were talking about earlier, and OCSF is an amazing standardized way to know if the data is there or not. But the biggest downside to OCSF is, if a vendor does not support it, it sort of breaks the whole thing because then you have this like elegant OCSF query that you've done and then you have to start slapping vendor data across it. And so the biggest weak point for it at the moment is just mixed support from different log sources and vendors. But at the end of the day, it's incredibly important, and it's only grown more important for AI to be able to have some of these standardized queries. Yes.

**Anthony La Scala**

Yes. It's the standardization, the normalization of the log so that they are easier to query to find and OCSF really does support that. And it looks like we had one last-minute question coming in that I might be able to answer here. Srishti, I've always known S1 to provide SIEM capabilities, hence, the AI SIEM branding. But I noticed on one of the platform extension slides that it list SIEMs or just to clarify, does S1 natively include all of these core features, now?

Yes, everything that we showed today is a SentinelOne feature. And so they are all available with the Singularity Platform.

All right. So that, we are at time. Thank you so much, James, for being here. Now before we sign off, go check out the full Latio security operations market report. It's available for download right now. And the link should be on your screen. It's worth your time. It's practitioner-led research built on hands-on evaluations, and it gives you a real framework for assessing your security stack independent of any vendor. And if you want to see more of what I showed today, request a demo. We can set up a session tailored to your specific environment.

Well, James, thank you so much. I really appreciate your time today. Thank you to our audience for joining us today. I hope you all have a great rest of your day and signing off from SentinelOne. Thank you.

**James Berthoty**

Thanks for having me.