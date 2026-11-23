---
title: "Terminology"
---

Borrow words where the market has them, only add what the market lacks. The market term per object is in [the FCD model](model.md). Dutch terms in italics.

## Full Circle Delivery

| Term | Meaning |
|---|---|
| Full Circle Delivery (FCD) | The term for the whole: the full circle, not just continuous delivery. A way of working, not a framework. Not software development lifecycle. |
| Circle | Intention → delivery → product → learning → intention again. |
| User (*gebruiker*) | Who uses the product. Not customer: that is the business. |
| Senang | At ease, satisfied. Now and later. |
| Perspective | A view on the circle, with its own principles. |
| Principle (*kader*) | One guiding statement. Together the principles are the guardrails for AI. Not a standard (straitjacket), not an agreement (non-committal). In the code `Principle`. |
| Comply or explain | You follow the principle, or you explain why not. |
| Deviation (*afwijking*) | The explain for a principle. A human approves it: the owner. In the code `Explanation`. |
| FCD model | One language: the building blocks, placed per perspective. Not CD model. |
| Your FCD model | Where you are, where you want to go, which perspective needs attention. |
| Declarative file | Your FCD model captured: what and why, reproducible. It produces the pictures, not the other way round. |
| FCD language (*FCD-taal*) | One language for people and machines: the words and rules of the FCD model (intent, sub-product, principle, quality gate), using words the market already knows. The declarative file (`*.fcd.yaml`, `apiVersion: fcd/v0`) is the FCD language for machines. |
| Continuous delivery | A perspective within FCD: there is always a working path to production. |
| Backlog | What the FCD model asks for and is not yet filled in. Not "gaps". |
| FCD criteria | Reliable, secure and safe, complete, effective, efficient and budget. For the product and for FCD. |

## From intent to product

| Term | Meaning |
|---|---|
| Intent | What the user wants, from the persona: persona and user story, why (objective), measure (key result), behaviour as scenarios. Intent is intent, not a norm. |
| Persona | The user of the product. |
| Product | Sub-products together form a product. It runs in production. |
| Sub-product (*deelproduct*) | The unit of deployment and of release. Consists of one or more containers, each with its own lifecycle. A squad owns it. |
| Container | A service runs in it. Built from code and libraries. |
| Build, deploy, release | Building delivers a container, deploying puts a sub-product on an environment, releasing makes a version of a sub-product available to the user. |
| Squad | Owns sub-products. Composition: humans, humans and AI agents, or AI agents only. |
| Contracts | Agreements between sub-products. Contract first; the schema is part of the contract. |
| Output | The software. |
| Outcome | What it delivers for the user. |

## Showcases

| Term | Meaning |
|---|---|
| Showcase | Shows working how it can be done. It opens the conversation. |
| ShowKitchen | The product in the showcases: software as a service for restaurants. |
| Demo, Classic, Ideal | The three showcases: the same product, three ways of working. Each showcase is a pair: fcd-X (the way of working) and sk-X (the product). |
| Product picture (*productplaat*) | What is in what, generated from the declarative file. |
| Full Circle Delivery picture (*Full Circle Delivery-plaat*) | How the product comes into being and stays alive, generated from the declarative file. |

## Earlier work: the model with axes

These terms belong to the [earlier model](eerder-werk/index.md).

| Term | Meaning |
|---|---|
| Axis | A choice with two poles. |
| Precondition (*randvoorwaarde*) | Axis on which the position is given. |
| Knock-out | Precondition where the model does not apply on the wrong side. |
| Shaping (*vormend*) | Precondition where any position is allowed; it determines the setup. |
| Starting point | Axis on which you choose the position. |
| Opinion / strong belief | My position on an axis; the convictions from the why. |
| Scenario | A set of positions on the axes. |
| Route | The distance from a scenario's position to the opinion. |
| Setup (*invulling*) | The result of the route. |
| Right practice | Good in this situation. Not best practice. |
| Factory (*fabriek*) | The organisation and AI; a collection of right practices. |
| Showcase practice | One right practice as working code. |
| Map (*kaart*) | Role: task, user, domain division and budget per domain. |
| Terrain (*terrein*) | Role: everything within a domain. |
| The how (*het hoe*) | Role: the work within a subsystem. |
| Domain division | What the map decides, instead of portfolio. |
| Professional | *Proposal* for the role of the person, instead of people. |
| Stable teams | *Proposal* instead of long-lived squads. |
| AI in the team | *Proposal*, with as axis: from AI as a tool to a team that is largely AI. |
