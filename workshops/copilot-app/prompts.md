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
Keep the query unchanged; that is the next ticket.
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

Start both from `workshop-complete`, in separate worktrees.
Verify that each session's HEAD matches that branch before editing.

```copilot
UI worker: only change src/main/resources/static/.
Improve the empty-cart state with a clear keyboard-accessible link to the
catalogue; preserve cart behavior and mobile usability.
No API changes or dependencies. Preview it, review the diff, commit,
and report the actual branch/SHA plus checks and limitations.
```

```copilot
Test worker: only add CartBoundaryTest.java beside the existing tests.
Use HTTP integration tests for missing quantity, non-integer quantity
and exactly 99 units. Do not change production code or existing tests.
Run the new cases and full suite. Commit and report branch/SHA,
executed counts and any real defect you found.
```
