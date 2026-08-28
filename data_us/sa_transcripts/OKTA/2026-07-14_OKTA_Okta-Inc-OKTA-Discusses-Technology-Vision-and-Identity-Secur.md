---
ticker: OKTA
company: Okta, Inc.
title: "Okta, Inc. (OKTA) Discusses Technology Vision and Identity Security Strategy Transcript"
published: 2026-07-14T00:20:20-04:00
article_id: 4921699
source_url: https://seekingalpha.com/article/4921699-okta-inc-okta-discusses-technology-vision-and-identity-security-strategy-transcript
---
Okta, Inc. ([OKTA](https://seekingalpha.com/symbol/OKTA#source=section%3Amain_content%7Cbutton%3Abody_link "Okta, Inc.")) Discusses Technology Vision and Identity Security Strategy July 13, 2026 3:00 PM EDT

**Company Participants**

Dave Gennarelli - Senior Vice President of Investor Relations  
Ely Kahn  
Harish Peri - Senior VP & GM

**Conference Call Participants**

Eric Heath - KeyBanc Capital Markets Inc., Research Division

**Presentation**

**Eric Heath**  
*KeyBanc Capital Markets Inc., Research Division*

So Ely, Harish, Dave, thanks for being here, Janice as well. I very much appreciate you all being here to hopefully get a technical session for people and go into a topic that I think is very interesting. So Ely, the Chief Product Officer; Harish, SVP and GM of AI Security. And then we all know Dave and Janice on the IR side of things. So I'm going to throw it over to Dave to hit the safe harbor, and then Ely and Harish have some prepared slides and topics to hit. So I'll throw it over to you, Dave.

**Dave Gennarelli**  
*Senior Vice President of Investor Relations*

Great. Thanks, Eric, and thanks for hosting us today. Really appreciate it. And just Janice is going to throw the safe harbor up. You guys are all familiar with the safe harbor language, just a reminder of that. And just to remind you that today's conversation is really about the technology. We're not going to be taking financially related questions today.

So with that, I'll throw it over to Ely.

**Ely Kahn**

Thanks so much. And once again, my name is Ely Kahn, Chief Product Officer here at Okta. I've been here about almost 6 months, but been in cybersecurity my whole career, first inside the U.S. government, U.S. intelligence community, doing cybersecurity, then a startup called Sqrrl that was acquired by AWS, spent 4.5 years there building products. Most recently before Okta, I was Chief Product Officer of SentinelOne. And yes, excited to be here to talk a bit about our vision, our road map and our strategy.

Okay. So just as a refresher, I thought I'd start with a reminder about what is the Okta platform. And really over the last 3 to 4 years, we've been building out a complete identity platform that covers all the major use cases that you need to protect your identities, pre-authorization, at authorization and then post authorization.

So maybe first starting with the pre-authorization focused products. We have our identity security posture management products. This was the acquisition that we did 3 years ago, a company called Spera. This gives us the ability to discover misconfigurations, identity-related misconfigurations in hundreds of your SaaS and other types of applications. So generally speaking, we're looking for overprivileged or misprivilege administrators or other identities, including administrators that haven't been -- accounts that have been used in a period of time or other examples of misconfigurations that increase your blast radius.

Next up, we have our Identity Governance products. This has become one of the fastest-growing products in our portfolio. And it just recently has crossed over 2,000 customers, which puts us on par now in terms of customer adoption with other IGA products like SailPoint. And so this gives us the ability to ensure that those users that you've onboarded to Okta have least privilege, allows us to access requests and access certifications to ensure that those users continue to have the right amount of privileges over time. This is also complemented with Okta Privileged Access, which I think about as the flip side of the coin to our IGA products. With Okta Identity Governance, you're provisioning access to sort of standard sorts of applications. And with our Okta Privilege Access, you're provisioning access to high risk, high trust resources, things like databases or Amazon EC2 instances. When we do that, we can do session reporting. We can also plug into on-prem resources, ensure that even if you're using a long-lived credential or API access key, we then short-term ephemeral tokens to ensure that even if there is a compromise, the blast radius is small.

Next up, at authorization time, we have a couple of products. Of course, our flagship MFA SSO product around access management, which provides secure cross-platforms, phishing-resistant authentication. And then we sync that up with Okta device access so that you can use the same login processes both into your device and into your applications.

And then lastly, Identity Threat Protection. This is our Identity threat detection response product. This gives us real-time signals that can be used to look for misbehaviors and anomalies during the session. And the real power here is we can -- these aren't producing just another set of alerts. We can tie this into other products so that we see users above a certain risk threshold. We can do things like universal logout or step up authentication to really contain that risk within that session. Now these products, they're not siloed. The power here is that they're part of a unified identity security fabric and they allow us to cover a broad set of users and devices, including employees, partners, contractors. It can plug into both modern SaaS applications and legacy on-prem infrastructure. And now most recently, we've extended the platform to support AI agents as a first-class identity in the platform. I'll get more into that, and Harish is going to go real deep into that.

In terms of that Unified Identity Security Fabric, let me give you just one example. So let's say, as part of our ISPM, our Identity Security Posture Management product, we've identified that a particular administrator is not being used. That account is not being used. We can use that information then kick off an access certification in our IGA product to officially recertify whether that user needs that administrator account? And if not, revoke it. So we have a bunch of out-of-the-box integrations across our products. We also have a low-code, no-code solution called Okta Workflows that lets you stitch together any other type of custom integration between the products that you might want.

And then lastly, and certainly not least important is our uptime story. So we're at [ 99.99% ] as our official SLA. This year, we're actually at 100% uptime. And over the last 3 years, this means that we've had roughly 69 minutes of downtime. And compare that to a Microsoft that's had over 2,000 minutes of reported uptime. This is a key differentiator for our platform and one of the reasons customers love us.

Next up. Okay. So a big move for Okta has been that we've been really pushing towards this identity platformization story. And we've been working with some of our largest most complex customers on this story where they're making a big bet, and they want to take a very complex set of legacy solutions and simplify. So this is a customer that we've been working with for the last year. We'll complete this platformization story this year. And they're very typical of a large Fortune 2000 company. In this case, they've used a legacy solution for identity management. I think they are using SailPoint here. And they're using another vendor for their access management, in this case, Ping, and then another vendor for privileged access management, in this case, CyberArk. And they have specialized teams for each of these vendor solutions. And it's not only a cost issue for them, but it's a complexity issue. And that complexity also translates to security, meaning the more complex your stack is, the more likely there are gaps in which adversaries can compromise. And so they wanted to solidify down into a single vendor, Okta, not only to reduce costs, not only to reduce complexity, but also to increase their overall security posture. And we're well on the way to this. We'll finish this complete replatformization this year, and the customer will be seeing significant -- they're estimating somewhere around 40% economies of scope gain in the form of cost savings.

All right. So maybe backing out now in terms of our 2026 product strategy. And this closely relates to that last slide there in terms of the platformization play that we're making. So we have 5 main elements to our product strategy. These are not the only things that we're working on, but these are the top 5 most important things that we're putting our efforts around. The first one is our Okta for AI agent story and ensuring that we have a first-class set of experiences across all of our products to support AI agents and to protect the identities of AI agents. I'll get more into that in just a second.

Next up, second and third, maturing our IGA and PAM solutions to be world class so that they can rip and replace legacy vendors like a SailPoint or like a CyberArk and even just win head-to-head in greenfield competitions where the customer may not even be using us for access management. And we're well on our way to that as well this year, and we have a number of wins where that happens. Identity Security Fabric. I'll actually talk about Identity Security Fabric in a little more detail in the next slide through the lens of Okta for AI agents, and how all of our products are coming together to provide that unified Identity Security Fabric for the AI agent use case. And then lastly, Okta, like a number of companies is all in on AI native product development. And we are aggressively using coding agents across all of our product teams and seeing 50% gains in product life cycle development which means we're shipping products and features faster to our customers while still maintaining the really high bar around uptime, resiliency and security.

All right. Let's jump into the AI agent story here quickly. I'm not going to go through this in detail, but I saw there were some questions and the pre-reads about what type of agents does Okta protect. This is a common question, and we actually built out an AI agent taxonomy to help with this. At a high level, the 4 major categories of agents as we think about them are embedded agents. These are things like your Zoom companion agents. Now embedded agents are the one type of agent that we do not try to protect. These agents are essentially hard-coded into SaaS applications. They don't expose APIs, so we can't really manage them.

Next up, stand-alone SaaS agents. So this would be something like a Devin or a Fin. So this is an AI agent that exists as a SaaS agent. We can onboard these types of agents into our platform to govern and protect them, agents associated with automation platforms, where the agent built into a Boomi, Torque or Times. That's also a type of agent that we're working to protect. Homegrown agents as well. So if you built out a fully custom agent using LangChain or an agent builder platform like Amazon Bedrock, those are also agents to support.

The other dimensions of agents that we oftentimes look at and have some unique characteristics in terms of how we protect them is the delegation pattern. So is this simply a human prompting agent? Or is there a set of subagents that are spawning. And then how long that agent exists? Is it a very short-term ephemeral agents or a long-lasting one. These are all considerations that we've gone through as we built out our Okta for AI agents platform. Let me talk about that quickly in the next slide.

Okay. So this is a busy slide here, but let me talk through it real quickly, and then Harish is going to, I think, touch on some of the details here in more depth. So when we talk about our Okta for AI agent story, at the top level, we think about it through 3 simple questions. Where are my agents, what can they connect to you and then ultimately, what can they do? And so what you're seeing here is our reference architecture. Most of these things are in place, not all of them yet, but these are all the things that we're building towards really over the next -- either we have now or building over the next 6 to 12 months. And it starts with discovering your agents. And so we built integrations with a number of different tools to directly import agents from those tools. This could be things like Amazon Bedrock or our Salesforce control tower. Any of those type of agents we can directly embed them into our registry through a direct import by calling their APIs.

Also, if you build a homegrown agent, you can use our SDK to then import that agent directly into our registry. But we also have the ability to discover unknown agents. And the first capability that we launched earlier this year is using our browser extension to discover OAuth claims between users and Agentic tooling and then giving the users a workflow or the administrators the workflow to register those unknown agents in our registry. Once they're in our registry, then they can be registered with a human owner or they can be registered as a fully autonomous agents. You can apply additional meta data to them to ensure they have a full identity and they can come under user entitlement reviews.

So is this a user that should have access to that agent and doing access requests and access certifications. Also, does this agent have the right access to resources and able to do access certifications over time on that. From there, once that agent is registered in our agent registry with a first-class identity, you can start giving it permissions in the form of scopes. So these are considered core screens permissions. And so you might give it sort of provisions to Slack or to GitHub or to Jira in terms of being able to read versus write, versus update, et cetera. And from there -- and this is really important because you want to give those agents the least amount of privilege possible, but enough privilege to fulfill their goals and objectives.

Now we've also shown some -- and we put some bots on this recently, how you can apply fine grain access controls to agents. So not only can you apply these core screen scopes, but if you also want to give it a more fine-grain access policy like say, "Hey, this agent can only view not sensitive data or they can't write sensitive data." Those would be additional fine grain access controls. This is where we bring in some of our of Auth0 capabilities in its FGA products to combine with our Okta for AI agents solution.

All right. So once you've defined the access policies, then it can start accessing resources. It can access resources through our MCP servers, authorization servers, our SaaS authorization servers. We also have a new agent to agent capability and ultimately, we are able to monitor these capabilities, produce logs that can be shipped to a SIEM. And perhaps most importantly, if things start going wrong, if that agent starts misbehaving, acting suspiciously, we also give you a kill switch that allows you to revoke tokens and ensure that those agents cannot continue accessing resources in a malicious way.

So like I said, there's a mix here of things that we've delivered and things that we're working on. But this is really the complete story that we're working towards and will ultimately help customers not only identify their agents but ensure those agents operate with least privilege and have a small blast radius if they're compromised.

All right. So with that, I'll hand over the mic to Harish.

**Harish Peri**  
*Senior VP & GM*

Yes. Yes. Thank you so much, Ely. And I see some questions trickling in. So I will keep this brief, so we can make sure everyone's questions get addressed because that is what is most critical.

For introduction, I am Harish Peri. I run the AI business at Okta. So I spent majority of my time with our customers in the field, making sure our everything to do with our AI security story resonates and that we're growing this business. So that is why I'm here. So some of the content I have is more around how we're positioning our capabilities and how we tell the story to the broader market, which I think will also be very helpful to this audience.

So if you go to the next slide. The goal that we have for every one of our customers and folks that are not our customers that are embarking on their Agentic journey is every company will become an Agentic enterprise in the next year, 1.5 years. What that means is many pieces of their product development, portions of how their employees interact with their tools, how they connect with their end customers, how they connect with our partners, suppliers, all those are going to become agentified. There's going to be agents in the flow there. Our appeal to all of them is you could be Agentic Enterprise or you could be a Secure Agentic Enterprise, which means you have a centralized security offering to be able to control the identity and access and authorization of everything those agents are connecting to. So that's the broader kind of hook that we have for the market, which is to say, how do you not just be an Agentic enterprise, but how do you do it in a way that's secure? Because the difference between building agents and rolling them out into production is security and scalability concerns. So that's really how we're starting our position.

Can we go to the next slide, please. And since we've embarked on this journey, we've engaged with hundreds and hundreds of customers. I mean we're talking CISOs, CIOs across some of the largest companies in the world. And the thing is the tongue-in-cheek way of putting this is the cat is out of the bag, everyone has agents they're rolling out. The question is, where did the cat go, right? And that gets into something -- some of what Ely was touching on, which is discovery is a really huge issue. But the common themes are, we are -- everyone in our company is going to become a developer at some point. How do I know that they're developing within the right guard rails. How do I ensure that all of my Claude code or my OpenAI or my cursors or all those development assistants are actually being controlled in the right way? And how do I ensure that they don't execute judgment and delete something important overnight with no human oversight, right? So this problem is very real. It is very top of mind for pretty much every one of our customers and every new company that we're talking to. So it is very much in the zeitgeist of the topic of securing AI agents.

If you go to the next slide, please. Now I want to spend a little bit of time on maybe some broader topics, which is -- I actually spend a ton of my time educating our customers about just the nature of the overall problem. And one of the topics I get pulled into a lot is, "Well, I have an AI gateway. I have guardrails around my LLMs." And to that, my response is that is necessary, but not sufficient. When you think about what it takes to secure agents, you really have to think about models, which is, of course, the brain behind the agent that is making decisions in response to a prompt and deciding what tools it can be accessed.

But there's a second part of it, which is how do I actually secure the identity and the authorization of what that agent is actually accessing. And that's a lot of what Ely was touching on. And so model is one piece, identity is another piece and the third piece is the data itself. So for those agents that are accessing your data at large scale, either for retrieval-augmented generation, or as part of what their -- just their daily operations also getting down to a level of, is this agent authorized to access this data at this moment in time given all environmental signals is a third big piece. So we like to think about model, identity and data and where Okta's really starting right now is this notion of how do we control the identity, the authorization and the access of every one of these enterprise agents that are running around your organization. So this is an important concept because people sometimes get hung up on the model side, but that's only 1 out of 3 things of the bigger problem.

So if you go to the next slide, please. And this is just an example. This is a completely hypothetical example, but this is -- as we see agents being rolled out, this is kind of a common pattern. One of the fundamental issues you're dealing with when it comes to agents is unpredictability. This idea that in response to a given prompt. So this is a hypothetical finance agent that's going to help your procurement team with contract or PO approvals. In response to the same prompt, there's going to be tools, there's going to be memory, there's going to be LLMs that are accessed and it might come out with different responses in each situation. And I bring up this slide because it's very critical for people to understand that this is actually -- you're not dealing with a deterministic piece of software. You're fundamentally dealing with something that at scale will get you a lot of efficiencies, but has a level of non-determinism to it that does require a level of human control, which is where identity comes in. So again, very powerful, but also has a very non-deterministic aspect to how they work.

If you go to the next piece. And there's a build here, so we can just kind of click through this. In the interest of time, we'll pause here. So when you take an average large enterprise. Once you think of their Agentic rollout at scale, and you think about their users, you think about their various functions, you think about the various applications and resources that this agent is accessing. When you start to do the math and you multiply through the various MCP servers, the various other agents that single agents are calling, when you think about the external services that they're accessing.

This is a little bit of a large number, but you could -- when you do the math, you're talking on the order of billions of access decisions that have to happen per day to get a truly Agentic Enterprise to work. Because, again, when you multiply the users, the applications, the resources, the agents, the agent-to-agent chaining, the complexity increases tremendously, and each one of these access arrows is a potential risk factor because what you're dealing with is not just a deterministic access claim, but it's an agent that is making a decision at that moment in time and could be exercising adjustment.

So that's why the notion of the attack surface becomes even more complicated when you're thinking about agents. And as you multiply that across the entire estate of technology that your average large company has, the complexity is quite mind-boggling and requires centralized control.

So if we go to the next slide. There's another thing that you would need to think about here, which is -- so I touched on non-determinism. There's also a notion of autonomy. Agents are going to take actions on their own, right? And traditional zero trust was not made for a world where you have these autonomous actors that are non-deterministic. So you really need to think about how do you control that.

The other important piece, which -- there was a question in the chat about differentiation, is this notion of delegation chains. So every regulator, every auditor out there is going to come knocking on a company's door to say, can you prove to me that a specific resource was accessed by a user, was accessed by an agent or was accessed by an agent acting on behalf of the user through a multi-agent access chain. And being able to centralize and track the delegation chain is the other important concern that breaks kind of Zero Trust as we know it today, which was made for humans really.

And then finally, there are more and more models emerging ephemeral agents, which is agents that spin up other agents that are short-lived that might execute a specific task. It's an entirely new paradigm of technology and software, and we really need to think about Zero Trust holistically and why we are so bullish on this is, the one common thread across all of this is that context is what was the intent of the original user that gave a prompt to an agent that then either spun up an ephemeral agent or call the subagent and then accessed to resource. It's the authorization and the identity that's the core of all that to be able to say we can actually control the chain of what is happening. So, I know there's a little bit of zoomed out, but it does require the industry at large to rethink what Zero Trust is all about and identity and authorization end up being at the core of all of this.

So if you go to the next piece. So again, when we think about what Okta for agents is really the direction that we're heading in, and actually, not even heading in the GA capabilities that we have in market today are really providing this notion of a control plane for every enterprise agent in your organization accessing every resource on behalf of any user in the organization. Centralizing that, governing every call, binding into user context, ensuring that access is provided just in time with least privilege, and then creating an immutable layered audit trail, so you know exactly what resource was accessed by who, on behalf of who at what moment in time, is the core of the platform that we're -- the capabilities we're adding on top of the Identity Security Fabric that Ely touched on earlier. So it's very powerful stuff. It's in market today.

And in the interest of time, I'll go to the next slide, which is which is actually this. So just I want to leave you with one -- maybe something a little provocative. So I said maybe a minute ago that I spent a lot of my time educating our customers. There's a lot of myths that are popping up that we end up doing myth-busting around, things like, "Oh, I have an MCP gateway. I think that's good enough." And the answer is that's good enough if you're not interested in full user agent to resource chain mapping and auditing, which is something that every company is going to need. So that's some education we have to do.

The other thing is "Oh, I use Bedrock Agent Core or a Copilot Studio today. And that has some identity stuff built in." But think about where Okta is today. We are an independent neutral central broker of human identity to every resource in your ecosystem. That's exactly what we're doing with agents. Separating the identity from the core agentic platforms actually gives you not only a level of control, but also a layered defense and depth strategy that reduces your single points of failure. So that's the other big myth that we spend a lot of time on.

And the third is, well, shouldn't -- this is just acting on behalf of a human. So why do I care, just going to carry the humans credentials? Sort of, but not really. When you have agents that really are helping your organization, these are multiplayer agents to use a term from Anthropic or these are enterprise agents that are accessing multiple resources. They do need their own independent identity that can be intersected with the permissions of the invoking user to then create the perfect permission chain.

So this is just an example of some of the education we're doing. The market is moving very fast. We are right at the forefront of it. We're spending a lot of time educating our customers, but there's tremendous momentum on that front. So I'll pause there, actually, I think we can call it a day on the slides because I want to make sure we have time for questions. And I don't know, Eric, if we hand it back over to you.

**Question-and-Answer Session**

**Eric Heath**  
*KeyBanc Capital Markets Inc., Research Division*

Yes. Thanks, Harish and Ely, for the comprehensive overview. So a lot of things I want to dig into. Maybe Ely, just coming back to where you started or one of the things you started with was the 4 different buckets of agents. Today, can you just high level give us like set the ground or just lay the framework for us in terms of what's the maturity of AI agents today in organizations that you're talking to? And secondarily, what are the most like prevalent types of agents that you're seeing?

**Ely Kahn**

Yes. One quick anecdote here. So we had a large financial services customer in our customer executive briefing center a month ago, and I was asking them how many production agents they had. And they responded with over 2,000. And when we were first doing our pricing analysis for Okta for AI agents, we assume there will be somewhere around 20 production agents in a large customer. And so we -- that was done back in October. And you can see like how fast the market is moving just from that one customer anecdote.

But in reality, the most prevalent type of AI agents that's out there in our customers right now are coding agents. So there's certainly a lot of -- and probably more sophisticated customers are building their own agents. But almost every organization we walk into has a Claude code or a Codex, or another coding agents. And so these are top of mind. And with those agents, it's not really about the number of agents, because typically you can think about that as like one agent for the entire development team. But it's the breadth of usage that's happening and the types of tools that those coding agents are able to connect to, and it's those developer to agent tool interactions that needs to be protected.

**Eric Heath**  
*KeyBanc Capital Markets Inc., Research Division*

Right. Okay. And then, Harish, one of the things that you said that you said that I thought was interesting, is I think you called out that discovery is the biggest issue that customers are facing right now. So can you just help us understand what Okta does today from a discovery of agents' perspective. And really, I mean, I think there's a lot of emerging vendors out there that we are familiar with and see getting a lot of momentum just -- what are they doing that's unique and novel, and like how differentiated is this capability that either you or the emerging vendors have when it comes to discovering agents?

**Harish Peri**  
*Senior VP & GM*

Yes. I think -- so more broadly, discovery is -- it's not enough to say I run something and I have a dashboard that shows me a list of 10,000 agents. Like that's fine, but then what do you do? And so where Okta is coming in is to say, where most likely are the most critical agents is going to be living and how can we find them the fastest. So that's what Ely touched on, there are known platforms like AWS, Copilot Studio, Azure Foundry, Agentforce, ServiceNow, there's a whole host of them that they're already partners of ours, and we can easily detect agents in their Agentic run times, and then import into Okta, that's one kind of discovery.

And the point I want to hit on is, discovery is half the equation. You also want to register those agents in a central identity directory and give them their own identities such that all the tool calls then get routed through Okta. That's the real value there is discovery is part of it, but giving them identity and then controlling the flow of access is the other part of it. So there's the known platforms. There's browser plug-in capabilities for a variety of browsers because one of the -- one type of agent is also sort of the SaaS agent that you're accessing through the browser. The other one are local endpoint.

And so the good news is we already have deep partnerships with the major cyber providers to be able to tap into their APIs and detect agents that might be running on the machine. But again, I want to emphasize that finding them and showing them on the dashboard is 50% of the equation. The other part of it is, say, now what? And that's the part where the full connectivity with Okta matters is to say, "Okay, now I'm going to give you a unique identity and ensure that there's no MCP calls, there's no tool calls that this agent is making that is not authorized and vetted and brokered by Okta." So it's really becoming in line and the flow is the end goal that we have here.

**Eric Heath**  
*KeyBanc Capital Markets Inc., Research Division*

Yes. From a product capability perspective, is Okta on equal footing with some of the emerging vendors out there when it comes to discovery? Or do you think this is an area for development, if you will.

**Harish Peri**  
*Senior VP & GM*

Yes. I mean I'll let Ely take that as he's deep in that on a day-to-day basis.

**Ely Kahn**

Yes. So right now, what Okta supports is one mode of discovery, which is browser-based discovery. This is for unknown agents. We also have those direct imports for known agents. But for unknown agents, we support browser-based discovery. You can see in our strategy slide, we'll be adding additional forms of discovery. I do think that there are some really unique aspects of the Okta platform that will allow us to differentiate, something that folks forget is that Okta is on every endpoint. Every Okta customer has an endpoint agent called Okta Verify, and this is a very powerful capability that can give us broad visibility into what is running on that endpoint.

This is -- I mentioned Okta Device Access. It's how we discover what's running on that device to ensure that you have a secure locking experience. So we'll continue expanding our discovery capabilities, including using the full power of the Okta platform to do so.

**Eric Heath**  
*KeyBanc Capital Markets Inc., Research Division*

Staying on the governance topic for one more question, and maybe switching to runtime, but on the governance side of things, I think one of the -- maybe things that one might theorize in terms of who has an advantage when it comes to the identity stack is the IGA vendors, the traditional ones have a lot of understanding of all the entitlements, and now the connectors to all these applications, and they have deep visibility into all those different fine-grained nuances that you need to know in terms of establishing access in the application. So, what's your perspective on the IGA vendors having that unique advantage? And I understand that Okta has IGA, so it's a little bit of your in both camps, but what's your perspective on that being a strategic advantage or moat?

**Ely Kahn**

I mean, my take is that we've caught up with the legacy IGA vendors, and again it's proven out through our customer adoption. With over 2,000 customers using Okta IGA, we have a very powerful IGA product, where some of the biggest customers in the world are looking at us from an IGA first perspective. So I think this is an area where we've invested significantly. We're going to continue to invest to close some of the long tail of feature gaps. But I'm very happy with where we're at on the IGA side. And yes, it's a critical part of our overall products to secure AI agents, but I'd say it's one component.

And frankly, it's a really important component, but it's not the most important one. The most important one is ensuring that the AI agents themselves have a least privileged identity that has a small blast radius. And the IGA piece can help you ensure that, that blast radius stays small over time, but we see it as an add-on capability, not the core central capability to our offering.

**Harish Peri**  
*Senior VP & GM*

Yes. What we hear from customers across the board is they're looking for a system of action versus like a system of record where you can keep track of rules and things. They need a system that can enforce the most critical thing, which is, is this agent allowed to execute this specific action on behalf of this user at this moment in time based on a variety of signals, some of them being entitlements in the governance system, but there are other signals like network signals and endpoint signals and other risk signals and that ability to do dynamic real-time authorization, managing the entire chain of custody, is the true ask that the requirement that the entire market is converging on.

And IGA is a portion of it, but it's not the all and all. And then that's where the identity piece comes in, is because we have a platform that can stitch together a user, agent, resource and that entire chain.

**Eric Heath**  
*KeyBanc Capital Markets Inc., Research Division*

Right. Maybe moving to the authentication runtime side of things. So we talked about the gateway, and I think there's been lots of mentioned the gateways from all sorts of vendors, et cetera. But can you just double-click on what you guys mean by agent gateway or access gateway, if you want to delineate the language there? And what role that is playing because, we did this in our piece, but Okta's role from the authentication side of thing is like, okay, we need to narrowly define the scope of what the user and the agent can do.

And if we do that right, the simple side of you might say, okay, it's all established in the token itself when they go to authenticate. But I think you and the market are saying, "No, you need the agent gateway on top of that." So just help us understand what the agent gateway is adding incrementally that's not defined in the agent's token.

**Ely Kahn**

Yes. So the agent gateway does a couple of things. One, you can think about it as a single endpoint or access point for a variety of Agentic tools. So if you're using Claude Code or Codex, the agent gateway is the access point for how those tools interconnect into our platform.

And then the gateway itself, once those Agentic tools are connected to the platform, serves as a policy enforcement point. And so it's where we enforce that those agents are accessing the tools that they're authorized to access. It's also where we provide the inventory of tools that those agents can access. So onboarding various MCP servers, each of those MCP servers have a variety of tools, will allow folks to mix and match those tools into least privileged virtual MCP servers that then those agents could access, and then it serves as the real-time policy enforcement points to ensure that they're only accessing things that they're authorized to.

**Eric Heath**  
*KeyBanc Capital Markets Inc., Research Division*

Can you just be more specific, Ely and Harish, with like real-time enforcement because, I mean, to be candid, I think we see that in a lot of product announcements and press releases, but just be a little bit more specific, if you could, on like what real-time policy enforcement is. Because to me, that seems like it is where the market is really trying to focus its efforts on when it comes to AI agents.

**Ely Kahn**

Yes. I'll start, Harish, feel free to jump in.

**Harish Peri**  
*Senior VP & GM*

Yes, go ahead.

**Ely Kahn**

Yes. Yes. And so each agent is granted a set of scopes in -- as part of its access policy. And the agents themselves can either be acting on behalf of the user or fully autonomously, we support both of those modes. If they're acting fully autonomous, if they're acting on behalf of the user, they actually get the intersection of the human's permissions and the permissions granted to the agents.

But ultimately, you need a policy enforcement point to decide whether that agent which is making a request to access certain tools should be granted that request. And that enforcement point is the agent gateway. So it's making the decision there or it's enforcing the decision whether that agent should get access to the tools based on the permissions of the agents and the permissions of the user if it's acting on behalf of the user. And that happens in the agent gateway.

But Harish, anything else to add on that?

**Harish Peri**  
*Senior VP & GM*

Yes. Maybe I'll give a different way of thinking about it, which is -- so let -- so, put coding assistance aside, because their access patterns are, I need to talk to Jira and to talk to my S3 buckets, I need to talk to Artifactory like those. But we have many large customers that are building internal agents to help their employees with like a finance use case. And so the downstream systems of that agent needs to touch or the ERP, in some cases the MRP inventory, very complex legacy systems that all may or may not have APIs and may or may not support cross-app access, for example.

So in -- the flow would be somebody in finance, they have the interface of the agent, they say, can you approve this PO, like the hypothetical example I gave. The LLM behind the agent will say, "Okay, I need to first go check inventory, then I need to go make an update in SAP, then I have to go talk to our system, then I have to send an e-mail," whatever it may be. There's different levels of scoping, meaning what level of access does this agent have to Workday or to SAP. That's the first piece that Okta is controlling.

But then there might be custom authorization rules that also need to be enforced depending on attributes in the users' profile, depending on other attributes that might be custom. You're chaining all those together and making a real-time decision based on all that available context, that's the core of runtime, the authorization that we're getting at. So the gateway brings all that together in a highly performant way, right? And so we can support some of this with our fine-grained authorization capabilities today, and we're pushing towards this notion of intent-driven, which is what is the other theme that you might be hearing in the market today, which is let's make sure this agent doesn't go off on its own and try to execute an action that was not matched with the intent of the original user.

So keeping track of that entire context at every transaction, and enforcing that in a highly performant way, based on things like OAuth scores, but then also custom authorization rules. That's the holy grail of this runtime capability that we're pushing towards. So having a central authorization point is critical, and that's a big part of what the Gateway does.

**Eric Heath**  
*KeyBanc Capital Markets Inc., Research Division*

So maybe kind of jump into the punchline, Harish and Ely. How do you see this market evolving in terms of where the point of differentiation is going to be an identity stack, whether it's the registry, the IDP, the discovery, the gateway, the token path like the actual issue of the tokens? So just, how do you think about it? Give us the framework of where you think the unique differentiated aspect is going to be in this market?

**Ely Kahn**

Yes. I think -- I'll double down on something Harish was just talking about. So and this goes to -- also touches on some of the other questions that came in. In terms of what is fundamentally different about AI agent identity versus human identity. And there's a number of technical differences, tactical differences, like agent-to-agent connectivity required a whole new type of standard because there wasn't a good corollary on the human side.

But I think one of the most interesting difference is where -- and Okta is making big investment here is the fact that we're going to have to fundamentally rethink identity management and access management with agents. Because the traditional process of defining static permissions and then every quarter reviewing those permissions to see if there's still a least privilege, that's eventually going to break down because AI agents are becoming more and more powerful and more and more autonomous.

And that means that it's going to become harder and harder for an administrator to predefine all the permissions that an AI agent might need upfront. And instead, we're going to need to move to a world where the permissions are granted to agents in a more dynamic, just-in-time basis. And they'd be granted if the tool invocation that's the agents attempting to do is not anomalous, is not -- does not drift too far from the original agent intent, does not contradict any guardrails that you want to ensure are adhered to. And so it's this mode of moving towards just-in-time dynamic permissions for AI agents that I think will become the biggest differentiator, and that's a big place where Okta is focusing.

**Eric Heath**  
*KeyBanc Capital Markets Inc., Research Division*

I wanted to hit maybe a little bit less of a technical question, maybe a little bit more market questions. But one thing I've noticed and picked up over the last several months is you guys seem to have a tight relationship with Anthropic when it comes to their identity announcements and with workload and integration, and I forgot the other things. But it seems like you have a tight integration. So can you just elaborate on what you do or don't have when it comes to partnerships, whether on product or go-to-market with these frontier AI labs?

**Ely Kahn**

Yes. Yes, go ahead, Harish.

**Harish Peri**  
*Senior VP & GM*

Yes. So more broadly, we have been and always will be an ecosystem player. The power of Okta is very much to do with how we can, one, help drive the right industry standard and then help bring all the ecosystem players along with us and implement that standard. And so Anthropic is one example. But yes, we have -- there's been a lot of -- kind of public announcements around how they're supporting cross-app access.

What that does is, one, that helps drive the adoption of the standard call cross-app access, which reduces things like continuous OAuth consent fatigue and also creates a central way to control permissions. So it helps drive anthropic adoption, it helps driver adoption, helps bring the industry standard up. But I would look at -- that's one example of many. We have -- to ultimately to make an enterprise a secure agentic enterprise, we have to make sure that our ecosystem integrations are tight with every player in that blueprint that Ely was showing.

Anthropic and their frontier models are one of them. We have integrations with the cybersecurity vendors like CrowdStrike and Zscaler. We have integrations with the Agentic platforms where agents are created. We need to think about integrations with other gateways that customers may have. And so it's the same story that we've had for human identities. We need to plug into all the players in the ecosystem to bring it to life. Same thing for agents. It's just a new set of players.

**Eric Heath**  
*KeyBanc Capital Markets Inc., Research Division*

One thing I wanted to ask you and get your perspective on is, I always tell clients, investors that like identity is probably the most fragmented market in cybersecurity. There's a whole slew of start-up vendors out there and point solution vendors out there and maybe help frame for us, if an organization spends $100 on identity today for humans, I don't know, Okta maybe can get 20% wallet share of that. Maybe it's 40% with IGA and PAM. And then we have agents. We can decide if that $100 for agents is equal to humans, and it's another $100, but do you agree with the premise that like your share of wallet opportunity is relatively small today in the grand scheme identity stack? And with agents, could that 20% of wallet share be 80% of wallet share, 90% of wallet share? Does that question makes sense? And does it resonate at all?

**Ely Kahn**

It's -- it resonates a bit. My take is that this is not the same wallet share and that the wallet is expanding. Meaning, as customers more quickly adopt AI, they are also adding budgets to protect those AI agents, and that's not coming from the same budgets that they are using to protect their other identities. So I think what we're tapping into with our customer base is new budget associated with AI adoption. And so it's not the same denominator.

Now putting that aside, the stack for protecting AI agents looks very similar at the 30,000-foot view as the stack for protecting human identities. I mean we have ISPM, we have ITDR, we have SSO. And so we're building out that full stack to protect AI agents and the identities of them. So I would say that our wallet share for human identities is very similar to our expected wallet share for AI agents. But it's a different wallet.

**Harish Peri**  
*Senior VP & GM*

Yes, I would agree...

**Eric Heath**  
*KeyBanc Capital Markets Inc., Research Division*

The simple part of the question is just the identity market is highly fragmented today. Does it look much more consolidated when it comes to securing AI agents is kind of the punchline.

**Harish Peri**  
*Senior VP & GM*

There is a consultant, yes. So the -- and it goes back to what Ely was saying, which is companies are taking a more centralized approach for rolling out AI. So like they're at a -- this is a decision being made at the CEO level, at the Board level to say, okay, we're going to spend X billion dollars on an agent to transforming our company with AI. Given that agents live in the application layer and identity authorization is a center of all of it.

Two things. We do believe that we have a shot to go and take a slice of that entire spend, which is a more elevated conversation. And the evidence there is fruit. I have conversations every day now with CISOs and CIOs who are coming and saying, "we need you to draw the reference architecture of how everything comes together." So we are in the middle of the ecosystem now and the evidence is showing that. So it's a different wallet. It's a bigger wallet and the mechanics are going to be different. It's going to be -- it's a slice of the entire thing because it's essentially a security blanket around your entire Agentic investment.

**Ely Kahn**

Yes. And Eric, I think to answer your question, is it fragmented or more fragmented or less fragment. I mean, it is a brand-new technology area, so there is a plethora of startups in this space, which makes it feel very noisy. But I think similar to what we saw with like cloud security vendors, there will be a consolidation because ultimately -- and we hear this from our customers, I don't want that -- our customers don't want different stacks to manage their human identities and their Agentic identities. They want one unified solution where they can manage all of their identity issues together. So I think there will continue to be consolidation and platformization in this area?

**Eric Heath**  
*KeyBanc Capital Markets Inc., Research Division*

All right. Well, Ely, Harish, David, thank you so much. Great place to leave it at the top of the hour here. Wish I could spend a lot more time with you guys, but it's been a pleasure of tracking what Okta has been doing in terms of leading and shape in this market for AI agents, so it's definitely been great to see. So I appreciate it. Appreciate the time. Thank you, everybody, for tuning and listening, and I'm here to help if anybody needs it.

**Ely Kahn**

Thank you.

**Eric Heath**  
*KeyBanc Capital Markets Inc., Research Division*

All right. Thank you all.

**Harish Peri**  
*Senior VP & GM*

Thanks, everyone.