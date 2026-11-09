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
reset the cart, then add one €10 Notebook twice, waiting for each response
before the next click; expect quantity 2 / €20, actual 1 / €10.
Trace the UI, POST /api/cart/items and persistence path.
Do not edit yet. Explain the cause, relevant files and smallest testable plan.
Keep removal and query optimization out of this ticket.
```

## Use the test skill

The [skills chapter](/workshops/copilot-app/skills/) distinguishes installation
from loading. Its [installation section](/workshops/copilot-app/skills/#install-skills)
is for another project; the workshop's pinned skills are already installed.

```copilot
/java-junit
Generate src/test/java/com/juliendubois/workshop/CartContractTest.java
from the acceptance criteria in our plan, using the existing test fixtures.
Cover quantity accumulation, totals, new products and rejected input.
Do not copy the teaching test or change production code or dependencies.
Explain how you used the skill and show me the diff for review.
After my approval, run the tests and confirm they expose the quantity bug.
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

## Canvas and UI feedback

Stay in **Cart: remove item**. Use the
[startup-instruction prompt](/workshops/copilot-app/canvas/#startup-instructions)
first, then the [Pick & polish prompt](/workshops/copilot-app/canvas/#pick-and-polish)
on a selected UI element. The chapter saves `workshop-feature` only after
the reviewed instruction and UI changes, so the query session keeps them.

## Investigate through MCP

```copilot
Use java-hibernate-jpa and the connected BootUI MCP server.
Read get_live_activity with query "/api/cart", limit 8.
Select the recent GET /api/cart for the eight-product workload;
read get_request_profile with that returned ID.
Check that the request matches this workload and explain the product SELECTs.
No dashboard tour, scans, extra tools, source edits or server restart yet.
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

## Rubber duck and subagent implementation

Stay in **Cart: boundary tests**, on the checked combined result.
Use the [rubber duck prompt](/workshops/copilot-app/rubber-duck/#review-prompt)
for a read-only critique. Then use the
[five-subagent chapter](/workshops/copilot-app/subagents/) to prepare one
feature branch, approve the contract and **implement mock checkout**.
Each prompt names its scope and approval boundaries;
do not paste both tasks together or launch another set of worktree sessions.

## Deliver checkout to main

After reviewing the integrated code, tests and preview, use the
[checkout delivery prompt](/workshops/copilot-app/subagents/#deliver-checkout)
in the same **Cart: boundary tests** session. Give the orchestrator scoped
approval to commit, push, open one checkout PR and merge it after checks and
required approvals pass. The five specialists do not publish or merge.
Do not reuse the earlier worker PR.

Then use [merged-main verification](/workshops/copilot-app/subagents/#verify-merged-checkout).
Record the actual merge commit and verified main revision. Restart the one shop
from that verified directory before checking Place order and the receipt.
Local-only or blocked delivery is not the completed normal path.

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

## Review the diff

For a separate reference checkout, replace `workshop-start` with `v2-start`.
Otherwise keep the personal starter tag:

```copilot
Review the complete change from workshop-start to current tracked files,
including committed tickets, current edits and untracked new files.
Do not edit.
Look for behavior regressions, weakened tests, wrong totals or scope creep.
Cite specific code and evidence. Separate findings from unverified assumptions.
Do not infer that the running app uses this revision or that CI is green.
```
