---
layout: default
title: Learn GitHub Copilot App through a realistic Java scenario
description: "Fix and extend a Java shop, polish its UI in a Canvas, get a rubber duck critique, and coordinate five subagents to build mock checkout."
permalink: /workshops/copilot-app/
workshop: true
next: setup
next_title: Set up your App workspace
---

## The scenario

> **“I added the notebook twice. Why is there still only one in my cart?”**

In this **hands-on workshop**, use **GitHub Copilot App** to take a small Java
shop from a reproducible bug to a reviewed result. Fix cart quantities,
generate item removal, then use a shared **Browser canvas**, **Pick & polish**
and **impeccable** to improve an observed UI issue.

Investigate an N+1 query using **MCP** evidence. Build independent improvements
in two worktree sessions, then integrate their PRs with **Agent Merge**.
Get a second opinion from **rubber duck** and coordinate **five subagents**
to implement mock checkout with an order receipt and safe cart clearing.
The orchestrator delivers it through a reviewed PR into your own **`main`**
and verifies the merged application.
Finish with **Chronicle** and a clear handoff.

The shop is intentionally small: Spring Boot, H2 and plain JavaScript.
You do not need Docker, a payment provider, a frontend build or advanced
Hibernate knowledge. BootUI supplies runtime data **through MCP** for the
performance exercise.

<p><a class="btn btn-ink" href="/workshops/copilot-app/setup/">Set up your App workspace</a> <a class="btn btn-ghost" href="https://github.com/jdubois/copilot-shopping-cart-workshop" target="_blank">Get the template</a></p>

<figure>
  <a href="/workshops/copilot-app/assets/cart-bug.png" target="_blank"><img src="/workshops/copilot-app/assets/cart-bug.png" alt="The real starter shop after adding the €10 Notebook twice: the server cart still contains quantity 1 and a €10 total." width="1600" height="1000" fetchpriority="high"></a>
  <figcaption>The starter application after adding the Notebook twice: a bug to investigate and fix with Copilot.</figcaption>
</figure>

## One shop, four tickets

Here, **tickets** are exercise briefs, not GitHub issues.
You do not need to create issues in your repository.

| Ticket | Customer outcome | App practice |
|---|---|---|
| Fix adding the same product twice | Quantity and total accumulate correctly | Plan, use a Java skill, reproduce a failing test and guide the fix |
| Generate item removal | Remove one product without losing the others | Define expected behavior, generate backend and UI code, then preview and polish in a Canvas |
| Fix repeated product queries | The cart keeps its contents with fewer SELECTs | Use MCP evidence, diagnose with a skill, verify the query budget |
| Build and deliver mock checkout | Place a local order, see a receipt and start shopping again from the app on `main` | Agree on contracts, coordinate five subagents, verify failures/retries and let the orchestrator deliver a reviewed PR |

Start with **Fusion Standard**, or a strong coding model if Fusion is unavailable.
Use higher effort when a problem calls for it, not by default.
Review permissions, tests and changed files at every stage.
The first three tickets and reviewed UI/boundary-test improvements are
integrated before checkout. Five subagents then build the fourth ticket on
**one feature branch** in the existing session. **Mock means no real payments**:
the order, receipt and cart clearing must actually work.
The feature branch is a staging point, not the finish line: after your scoped
approval, the orchestrator merges its checkout PR and verifies actual `main`.

## Workshop flow
{: #workshop-flow}

Start with [setup](/workshops/copilot-app/setup/), then follow the chapters in
order. There are no chapter deadlines. Take a break before the parallel work
and ask for help whenever you need it.

<figure>
  <a href="/workshops/copilot-app/assets/illustration-shop-to-checkout.svg" target="_blank"><img src="/workshops/copilot-app/assets/illustration-shop-to-checkout.svg" alt="Conceptual workshop journey: investigate the notebook quantity bug, build with Copilot, then verify a working order receipt." width="1440" height="760" loading="lazy"></a>
  <figcaption>From a reproducible cart bug to a verified checkout: the workshop journey, illustrated.</figcaption>
</figure>

1. [Investigate with Copilot](/workshops/copilot-app/ticket/), using a reproducible cart bug.
2. [Choose modes, effort and permissions](/workshops/copilot-app/fusion/), then [install and use skills](/workshops/copilot-app/skills/) with the bundled Java guidance and a regression test.
3. [Review and verify changes](/workshops/copilot-app/verify/) to the repeated-add behavior.
4. [Generate and iterate with Copilot](/workshops/copilot-app/generate/) to add item removal.
5. [Use Canvas and Pick & polish](/workshops/copilot-app/canvas/), with startup instructions and **impeccable**.
6. [Investigate runtime with MCP](/workshops/copilot-app/tools/), using the N+1 query as the example.
7. [Merge the three accepted tickets into main, then start two isolated sessions](/workshops/copilot-app/parallel/) to improve the empty-cart experience and add boundary tests.
8. [Merge PRs with Agent Merge](/workshops/copilot-app/integrate/) into `main`, one worker at a time.
9. [Review with rubber duck](/workshops/copilot-app/rubber-duck/).
10. [Coordinate five subagents](/workshops/copilot-app/subagents/) to build mock checkout, then have the orchestrator deliver one reviewed PR and verify the merged app on `main`.
11. [Improve token usage with Chronicle](/workshops/copilot-app/tokens/) using the workshop sessions.
12. [Review the full change and hand off](/workshops/copilot-app/finish/#final-review).

## What you will leave with

- A reviewed shop on your own `main` with four tickets, usable UI improvements, a working mock checkout and regression coverage.
- Evidence from previews, tests, MCP, PRs and the independent critique, with unavailable or unfinished work recorded.
- A merged checkout PR showing how five specialists coordinated code and shared decisions, plus a workflow improvement from Chronicle.

## Before you begin

You need JDK 21+, Git and a supported Copilot App account. Create your own
repository from the template; the three Java skills are already included.
The integration exercise also needs GitHub Actions and permission to push
branches and merge PRs; local recovery is documented for blocked participants.
The skills chapter also explains how to install them in another project.
The App's Browser canvas, Pick & polish, bundled **impeccable**, rubber duck
and `/fleet` are used in later exercises; availability depends on your build
and policies. Each chapter explains how to record a blocked step or demonstration.
Keep the [prompt cards](/workshops/copilot-app/prompts/) and
[worksheet](/workshops/copilot-app/worksheet/) nearby.
