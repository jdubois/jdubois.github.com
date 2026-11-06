---
layout: default
title: Work in two isolated sessions
description: "Give independent tasks clear ownership, a shared accepted base and separate worktrees."
permalink: /workshops/copilot-app/parallel/
workshop: true
next: integrate
next_title: Merge PRs with Agent Merge
---

## What you will learn

Run two Copilot App sessions in separate worktrees, starting from the same
reviewed version with clear file ownership.

## Bring the reviewed work into main
{: #update-main}

First, stay in the session where you finished the query fix, normally
**Cart: query investigation**. After reviewing the completed cart, removal
and query changes, put those **three completed tickets into `main` through
one reviewed PR**. This gives both workers a normal, up-to-date starting point.
Paste this prompt in the query session:

```copilot
Confirm origin is my own workshop repository, not the template repository.
Commit only the accepted workshop changes, if not yet committed.
Fetch origin and show this session's complete diff against origin/main.
Confirm it includes the quantity fix, removal feature, query optimization
and all 12 supplied acceptance tests, plus the reviewed Canvas AGENTS.md
and UI changes. Run ./mvnw -q test and report counts.
Stop if any test fails or an acceptance case is skipped.
After I review and approve, publish only this session's branch without
force-pushing and open one PR targeting main for the three completed tickets.
Do not push directly to main or merge the PR yet.
```

Open that PR in the App. Review **Files changed** and the **tests** CI job;
resolve failures and obtain any required approvals. After accepting its
complete diff and checks, ask Copilot:

```copilot
Merge this reviewed three-ticket PR into main in my own repository only
once the tests job and all required checks and approvals pass.
Do not bypass protections or include unreviewed changes.
Confirm GitHub reports the PR as Merged.
```

**Do not start the workers until the PR is Merged.** In the query session,
ask Copilot to fetch `origin/main`, confirm its merged result contains all
three tickets, the reviewed Canvas instruction/UI changes and the 12 acceptance
tests, and report the new starting commit.
This includes squash merges; the original ticket commits need not be ancestors.
Keep the PR link and shared starting commit on the
[worksheet](/workshops/copilot-app/worksheet/#parallel-handoff).

## Start two tasks from updated main

In Copilot App, create two project sessions with **isolated worktrees**,
selecting **`main` as the base branch** for both. Name them as shown below.
Each session must start at the same updated `origin/main` commit reported
above, not a stale local copy of the starter. The worker prompts check this
before editing. Keep each worker on its own branch; **do not have both edit
`main` directly**.

If GitHub or CI prevents the preparation PR from merging, use the
[local recovery steps](#local-recovery) instead of claiming `main` is updated.

| Session | Owns | Done means |
|---|---|---|
| Cart: empty-state UX | `src/main/resources/static/` only | Empty cart includes a clear link back to the catalogue, accessible by keyboard and usable on mobile |
| Cart: boundary tests | A new `CartBoundaryTest.java` only | HTTP tests cover missing quantity, non-integer quantity and exactly 99 units; no production edits |

These tasks touch different files, so the two sessions can work at the same
time without overwriting each other's changes. Each prompt belongs in only
one session. **Both prompts are below; you do not need to open another page.**

### Cart: empty-state UX
{: #ui-worker}

Select **Cart: empty-state UX** in the App sidebar. Paste this prompt into
that session's composer to improve the screen users see when their cart is empty:

```copilot
Fetch origin and confirm this session starts at the shared updated origin/main
commit from the preparation handoff, with all three accepted tickets and tests.
Stop if it does not match; do not edit a stale checkout.
Only change src/main/resources/static/.
Improve the empty-cart state with a clear keyboard-accessible link to the
catalogue; preserve cart behavior and mobile usability.
No API changes or dependencies. Preview the UI, review the diff, commit,
and report the actual branch/commit, checks and limitations.
Do not open or merge a PR yet.
```

### Cart: boundary tests
{: #test-worker}

Now select **Cart: boundary tests** in the App sidebar. Paste this different
prompt into its composer to check inputs at the limits of the quantity rules:

```copilot
Fetch origin and confirm this session starts at the shared updated origin/main
commit from the preparation handoff, with all three accepted tickets and tests.
Stop if it does not match; do not edit a stale checkout.
Use spring-boot-testing. Only add CartBoundaryTest.java beside the existing tests.
Use HTTP integration tests for missing quantity, non-integer quantity
and exactly 99 units. Do not change production code or existing tests.
If a test exposes an application bug, report it for my review.
Do not fix application code or weaken an assertion to make the test pass.
Run the new cases and full suite. Commit the test file and report the
actual branch/commit, executed counts, any failures and limitations.
Do not open or merge a PR yet.
```

The testing skill helps this second session write and run the HTTP tests.
If those tests reveal a bug, **you review the finding and decide how to fix it**.
The test session must not change application code: that would go beyond its
assigned task.

## Supervise without sharing a working directory

**App tip:** separate worktrees let both sessions edit without overwriting
one another. Their changes still need review and integration.

Check progress and clarify the task when needed. Give each session time to work
instead of repeatedly asking for updates or starting more agents.
Each worker reviews and commits its changes, then reports its branch, commit
and test results.

Tests use random ports and isolated H2. Do not start two persistent shops or
reuse evidence from a different branch. The existing MCP investigation is
finished; these tasks do not need additional BootUI work.

Before integration, preserve unfinished branches and review what is actually
ready. Ask for help if either worker is blocked.
Do not let the workers open or merge PRs yet. In the next chapter, you will
target both worker PRs at **`main`**,
and use **Agent Merge** one PR at a time.

<details markdown="1" id="local-recovery">
<summary>Recovery: the preparation PR cannot be merged</summary>

Ask the facilitator for help. Do not bypass protections or continue with
failing acceptance tests. If GitHub, CI or approvals are unavailable but the
reviewed local query-fix version passes all 12 tests, ask Copilot to commit
only that accepted work and report its actual branch and commit.

Create both isolated worker sessions from **that recorded local branch**
instead of `main`. In each worker prompt, replace the remote-main check with
a check against the recorded local starting commit and the three accepted
tickets. Keep the tasks and file boundaries unchanged.

Record **main not updated: local recovery used** and any open preparation PR.
Continue with the integration chapter's local recovery, not its remote PR
steps. Do not report local integration as GitHub or Agent Merge completion.

</details>

## What you have learned

- Merge the three accepted tickets into `main` through a reviewed PR, then create two isolated sessions from the same updated starting point.
- Assign each session a specific task and set of files so it can work independently without changing the other session's code.
- Supervise progress and collect reviewed commits, test results and limitations for integration.
