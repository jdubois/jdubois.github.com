---
layout: default
title: Prompt cards
description: "Small prompts for the task you are doing now. Do not paste the whole workshop into one request."
permalink: /workshops/copilot-app/prompts/
workshop: true
---

## Investigate without editing
{: #investigate}

Stay in **Cart: quantity bug**, created in Setup. This prompt continues that
session; it is not the session's first prompt.

```copilot
In this shopping-cart repository, reproduce the repeated-add bug:
reset the cart, then add one €10 Notebook twice, waiting for each response
before the next click; expect quantity 2 / €20, actual 1 / €10.
Trace the UI, POST /api/cart/items and persistence path.
Do not edit yet. Explain the cause, relevant files and smallest testable plan.
Keep removal and query optimization out of this ticket.
```

## Use the test skill

Stay in **Cart: quantity bug**, in **Interactive**, with the reviewed plan.
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

Complete the quantity fix and
[merge its reviewed PR](/workshops/copilot-app/skills/#publish-the-quantity-fix)
before starting removal.

## Generate a feature

Prepare a **New worktree** session from the updated `main`, using **Plan**.
Send this first prompt:

```copilot
Plan removal from the merged quantity fix in this new worktree.
DELETE /api/cart/items/{productId} returns 200 with the updated cart;
a missing line returns 404 without changing the cart, including a catalogue
product never added. Add a Remove button per line.
Remove deletes the entire product line and all its units, not just one unit.
Removing the last line leaves zero count/total.
Preserve other items, quantities, server prices/totals.
No new dependencies, checkout or query changes. Do not edit yet.
```

Once the session has started, name it **Cart: item removal**.
After reviewing the plan, return to **Interactive** and generate tests first:

```copilot
/spring-boot-testing
Generate src/test/java/com/juliendubois/workshop/RemoveContractTest.java
from our reviewed removal criteria using the existing HTTP test fixtures.
Cover removal of one of two product lines, the last line and missing lines,
checking returned and stored state. Include a line with quantity 3:
removal deletes all 3 units and preserves the other product and its quantity.
Do not retrieve reference tests or solutions, implement removal or change
earlier tests.
Show me the assertions for review; after approval, run the tests and confirm
they demonstrate missing removal behavior before implementing the feature.
```

Then [implement the backend and UI](/workshops/copilot-app/generate/#generate-the-backend-and-ui)
and [preview the feature](/workshops/copilot-app/generate/#preview-and-iterate),
moving the running shop to this worktree. Continue to Canvas in this same
session; publish the feature and polish together afterward.

## Canvas and UI feedback

Stay in **Cart: item removal**, on its current branch.
[Open the running shop](/workshops/copilot-app/canvas/#browser-preview),
then invoke **`/impeccable`** with the
[Pick & polish prompt](/workshops/copilot-app/canvas/#pick-and-polish)
on a selected UI element. Then
[publish removal and Canvas changes together](/workshops/copilot-app/canvas/#publish-removal-and-canvas-changes).
Merge that PR before creating the query session.

## Investigate through MCP

Use the [first query prompt](/workshops/copilot-app/tools/#start-the-query-session)
to start a new worktree from merged `main`, then name it **Cart: query optimization**.
Follow the server handoff, [connect the MCP tools](/workshops/copilot-app/tools/#connect-runtime-tools)
and [create the eight-product workload](/workshops/copilot-app/tools/#reproduce-the-same-workload).
Use the [evidence prompt](/workshops/copilot-app/tools/#ask-copilot-for-evidence)
to inspect the matching request through `bootui-shopping-cart`.
Then use the [N+1 fix prompt](/workshops/copilot-app/tools/#fix-the-n1-query-issue)
to add regression tests and fix the issue in one step, then repeat the workload
to verify the runtime queries. Finish with the
[publication step](/workshops/copilot-app/tools/#publish-the-reviewed-result):
review the PR, merge it into your own `main` and verify the shared starting point.

## Parallel worker cards
{: #parallel}

Both prompts are included directly in the
[parallel-sessions chapter](/workshops/copilot-app/parallel/), beside the
App instructions for creating both worktrees from the `main` already verified
after the three task PRs merged. No separate preparation prompt is needed.

- [UI prompt](/workshops/copilot-app/parallel/#ui-worker): start the first session, then name it **Cart: empty-state UX**.
- [Test prompt](/workshops/copilot-app/parallel/#test-worker): start the second session, then name it **Cart: boundary tests**.

The UI session improves the empty-cart screen; the second adds boundary tests
and proposes fixes for any exposed bugs. Both may edit the same files;
Agent Merge helps reconcile their changes during integration.

## Integrate with Agent Merge

In each existing worker session, review the result and use **Create PR**,
[targeting `main` in your own repository](/workshops/copilot-app/integrate/#open-the-two-worker-prs).
Use the chapter's [UI PR steps](/workshops/copilot-app/integrate/#merge-the-ui-pr-first)
first: allow repairs with **Merge pull request** off, review the result,
then authorize merging in the App.
After the UI merge and its main-branch CI pass, use the
[test PR conflict-resolution prompt](/workshops/copilot-app/integrate/#update-and-merge-the-test-pr).
Authorize each PR separately. Stay in **Cart: boundary tests** for
[verification of merged `main`](/workshops/copilot-app/integrate/#verify-the-combined-application).

## Rubber duck and subagent implementation

Stay in **Cart: boundary tests**, on the checked combined result.
Use the [rubber duck prompt](/workshops/copilot-app/rubber-duck/#review-prompt)
for a read-only critique. On the normal path, deliver and verify any accepted
correction's follow-up PR before checkout; for local recovery, keep the checked
local result. Record deferred findings without applying them. Then use the
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
Record the actual merge commit and verified main revision.
Reuse the shop if it already runs from that directory, waiting for DevTools;
otherwise use the [server handoff](/workshops/copilot-app/setup/#move-running-shop).
Reload the Browser canvas before checking Place order and the receipt.
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
