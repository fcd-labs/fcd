---
title: "How Demo was made"
---

This showcase was made by a product owner, a chat and an AI squad. The answer to the experiment: one intent and one sub-product description are enough, provided the harness is in place.

## Knowledge in the model

AI did not invent FCD. The FCD model bundles professional knowledge of quality, testing, audit, releasing and continuous delivery: the principles, the quality gates, comply or explain, one source. That knowledge forms the harness. AI helped to work out the model and to build the showcase.

## One intent

It started with one sentence: as a guest I want to choose from a menu, so that my order reaches kitchen, bar and till. And with one question: is one intent, with a description of the sub-product, enough for an AI squad?

## Two tracks at once

The model and the showcase grew in parallel. The model gave the showcase direction; the showcase showed where the model did not fit yet. The model grew first in conversations in the chat; the showcase followed in nine days. All in spare time, alongside other work.

## Three roles

| Role | Who | What |
|---|---|---|
| Product owner | sim007 | The what and why, the decisions, the Approval |
| Thinking partner | Claude in the chat | The model, the FCD language, the site and the pictures; the assignments for Claude Code |
| AI squad | Claude Code | ShowKitchen, the Pipeline and the Dashboard; first a proposal, then push |

## A circle too

An intent became an assignment in the chat. Claude Code made a plan, the product owner chose, and Claude Code built, tested and reported back. With that report the site was updated. What was learned became the next intent.

## What chafed, and what it brought

- **The site lagged behind the showcase.** That led to one source: the configuration lives in fcd and goes to the showcase, not the other way round.
- **Words matter.** The process picture became the Full Circle Delivery picture, process became delivery, and the FCD language got a name.
- **The AI found a contradiction in the principles:** a deviation on a principle where explain was not allowed. Now the generator checks this itself.
- **The harness is not finished.** What is missing is backlog: a choice, not a gap.

## The answer

Yes, provided the harness is in place. What the AI squad made went through the same steps and quality gates, and the decisions stayed with the product owner. AI needs delivery. Delivery needs AI.

## The evidence

The intent: [mvp0-fcd-demo.md](https://github.com/fcd-labs/fcd-demo/blob/main/docs/mvp0-fcd-demo.md) (in Dutch). As of 23 November 2026:

| Repository | Commits | With the AI squad as co-author |
|---|---|---|
| [sk-bestellen](https://github.com/fcd-labs/sk-bestellen/commits/main) | 34 | 29 |
| [fcd-pipeline](https://github.com/fcd-labs/fcd-pipeline/commits/main) | 53 | 42 |
| [fcd-dashboard](https://github.com/fcd-labs/fcd-dashboard/commits/main) | 56 | 50 |
| [fcd-demo](https://github.com/fcd-labs/fcd-demo/commits/main) | 59 | 46 |
| **Total** | **202** | **167** |

See for yourself: the "Co-Authored-By" line in a commit shows that the AI squad co-wrote it.
