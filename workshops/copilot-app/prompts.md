---
layout: default
title: Prompt cards
description: "Small prompts for the task you are doing now. Do not paste the whole workshop into one request."
permalink: /workshops/copilot-app/prompts/
workshop: true
---

## Investigate without editing
{: #investigate}

```copilot
In this shopping-cart repository, reproduce the repeated-add bug:
add one €10 Notebook twice; expect quantity 2 / 2000 cents, actual 1 / 1000.
Trace the UI, POST /api/cart/items and persistence path.
Do not edit yet. Explain the cause, relevant files and smallest testable plan.
Keep removal and query optimization out of this ticket.
```

## Use the test skill

The [skills chapter](/workshops/copilot-app/skills/) distinguishes installation
from loading. Its [installation section](/workshops/copilot-app/skills/#install-skills)
is for another project; the workshop's pinned skills are already installed.

```copilot
Use java-junit to review CartContractTest against the acceptance criteria.
Show the skill guidance you actually read. Do not change the supplied test.
Run its three tests and identify the intended failures before fixing code.
No new dependencies, Docker, skipped tests or unrelated refactors.
```

## Generate a feature

```copilot
Add removal to the accepted cart implementation. Use spring-boot-testing.
DELETE /api/cart/items/{productId} returns 200 with the updated cart;
a missing line returns 404 without changing the cart. Add a Remove button per line.
Preserve other products, quantities, server prices and totals.
Review the plan first, then implement and run the existing tests plus removal tests.
Keep the query unchanged; that is a later ticket.
```

## Investigate through MCP

```copilot
Use java-hibernate-jpa and the connected BootUI MCP server.
Read get_live_activity with query "/api/cart", limit 8.
Select the recent GET /api/cart for the eight-product workload;
read get_request_profile with that returned ID.
Check that the request matches this workload and explain the product SELECTs.
No dashboard tour, scans, extra tools, source edits or server restart yet.
```

## Canvas and UI feedback

Stay in **Cart: remove item**. Use the
[startup-instruction prompt](/workshops/copilot-app/canvas/#startup-instructions)
first, then the [Pick & polish prompt](/workshops/copilot-app/canvas/#pick-and-polish)
on a selected UI element. The chapter saves `workshop-feature` only after
the reviewed instruction and UI changes, so the query session keeps them.

## Rubber duck and subagent implementation

Stay in **Cart: boundary tests**, on the checked combined result.
Use the [rubber duck prompt](/workshops/copilot-app/rubber-duck/#review-prompt)
for a read-only critique. Then use the
[five-subagent chapter](/workshops/copilot-app/subagents/) to prepare one
feature branch, approve the contract and **implement mock checkout**.
Each prompt names its scope and approval boundaries;
do not paste both tasks together or launch another set of worktree sessions.

## Review the diff

```copilot
Review the complete change from workshop-start to current tracked files,
including committed tickets, current edits and untracked new files.
In a separate checkout of the reference solution, use v2-start as the base instead.
Do not edit.
Look for behavior regressions, weakened tests, wrong totals or scope creep.
Cite specific code and evidence. Separate findings from unverified assumptions.
Do not infer that the running app uses this revision or that CI is green.
```

## Improve usage

Before selecting cost tips, follow the
[Chronicle privacy decision](/workshops/copilot-app/tokens/#decide-before-analyzing-history).
The command may immediately access history beyond this workshop; a later scope
prompt cannot undo that. Opt out and use your local workshop transcript if that
access is unsuitable. If you decide to run the analysis, request:

```copilot
Limit analysis to [workshop session IDs/names], [repository], [time window].
State which records you used. Do not inspect unrelated work or edit files.
Explain reported token/usage fields with their units and coverage;
mark missing data unknown. Identify two avoidable workflow patterns
with concrete examples, and suggest one better next prompt.
Keep acceptance tests, permission boundaries and review checks unchanged.
```

## Parallel worker cards
{: #parallel}

Both prompts are included directly in the
[parallel-sessions chapter](/workshops/copilot-app/parallel/), beside the
instructions for bringing the three accepted tickets into `main` and creating
both worktrees from that updated version.

- [UI prompt](/workshops/copilot-app/parallel/#ui-worker): paste only into **Cart: empty-state UX**.
- [Test prompt](/workshops/copilot-app/parallel/#test-worker): paste only into **Cart: boundary tests**.

The UI session improves the empty-cart screen; the test session adds HTTP
boundary tests without changing application code. They work on different files.

## Integrate with Agent Merge

First complete the [preparation PR](/workshops/copilot-app/parallel/#update-main)
so `main` contains the three accepted tickets.
Then use the [integration chapter's PR creation prompt](/workshops/copilot-app/integrate/#open-the-two-worker-prs)
once in each worker session. **Base** is the receiving branch,
`main`; **head** is that worker's branch.

Use the chapter's [UI PR steps](/workshops/copilot-app/integrate/#merge-the-ui-pr-first)
first: allow repairs with **Merge pull request** off, review the result,
then explicitly authorize merging.
After confirming the UI PR merged and its main-branch CI passed, use the separate
[test PR prompts](/workshops/copilot-app/integrate/#update-and-merge-the-test-pr).
Do not reuse the UI authorization prompt for the test PR.
Stay in **Cart: boundary tests** for the chapter's final checks of merged `main`.
No extra session is needed.
