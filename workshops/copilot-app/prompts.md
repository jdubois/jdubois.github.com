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
Do not retrieve reference tests or solutions, or change production code
or dependencies.
Explain how you used the skill and show me the diff for review.
After my approval, run the tests and confirm they expose the quantity bug.
No new dependencies, Docker, skipped tests or unrelated refactors.
```

## Generate a feature

```copilot
Stay in this session and on the current branch, with the committed quantity fix.
Plan removal from this accepted implementation.
DELETE /api/cart/items/{productId} returns 200 with the updated cart;
a missing line returns 404 without changing the cart, including a catalogue
product never added. Add a Remove button per line. Removing the last line
leaves zero count/total. Preserve other items, quantities, server prices/totals.
No new dependencies, checkout or query changes. Do not edit yet.
```

After reviewing the plan, return to **Interactive** and generate tests first:

```copilot
/spring-boot-testing
Generate src/test/java/com/juliendubois/workshop/RemoveContractTest.java
from our reviewed removal criteria using the existing HTTP test fixtures.
Cover partial/last removal and missing lines, checking returned and stored state.
Do not retrieve reference tests or solutions, implement removal or change
earlier tests.
Show me the assertions for review; after approval, run the tests and confirm
they demonstrate missing removal behavior before implementing the feature.
```

## Canvas and UI feedback

Stay in **the same workshop session, on its current branch**. Use the
[startup-instruction prompt](/workshops/copilot-app/canvas/#startup-instructions)
first, then the [Pick & polish prompt](/workshops/copilot-app/canvas/#pick-and-polish)
on a selected UI element. Commit the reviewed instruction and UI changes,
then continue to the query exercise in this same session.

## Investigate through MCP

```copilot
Use java-hibernate-jpa and the connected BootUI MCP server.
Read get_live_activity with query "/api/cart", limit 8.
Select the recent GET /api/cart for the eight-product workload;
read get_request_profile with that returned ID.
Check that the request matches this workload and explain the product SELECTs.
No dashboard tour, scans, extra tools, source edits or server restart yet.
```

After reviewing the evidence, generate the query-budget tests:

```copilot
/spring-boot-testing
Generate src/test/java/com/juliendubois/workshop/QueryContractTest.java.
Require 1 SELECT for completed HTTP GET /api/cart with 8 and 16 distinct
products. Seed first, clear Hibernate statistics, then record counts immediately
after the response and before verification queries. Assert all returned cart
fields and totals against seeded data. Use existing real HTTP/database fixtures.
Do not retrieve reference tests, change production code or add dependencies.
Show the assertions for review; after approval, run the tests and confirm
the query budget fails before optimizing. Test counts may vary.
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
