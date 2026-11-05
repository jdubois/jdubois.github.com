---
layout: default
title: Work in two isolated sessions
description: "Give independent tasks clear ownership, a shared accepted base and separate worktrees."
permalink: /workshops/copilot-app/parallel/
workshop: true
next: integrate
next_title: Integrate the branches
---

## What you will learn

Run two Copilot App sessions in separate worktrees, starting from the same
reviewed version with clear file ownership.

## Start two tasks from the same version

Prepare the shared base and two isolated sessions.
After reviewing the completed cart, removal and query changes, ask Copilot:

```copilot
Commit only the accepted workshop changes, if not yet committed.
Create a branch workshop-complete at this commit without switching branches.
Do not replace an existing branch. Confirm it includes the quantity fix,
removal feature and query optimization, and the working tree is clean.
```

`workshop-complete` marks the shared starting point.
In Copilot App, create two project sessions with **isolated worktrees**,
selecting **`workshop-complete` as the base branch** for both. Do not silently
use the project's default branch. Ask each worker to confirm that its starting
commit matches `workshop-complete` and contains the full accepted solution
before editing.

| Session | Owns | Done means |
|---|---|---|
| Cart: empty-state UX | `src/main/resources/static/` only | Empty cart includes a clear link back to the catalogue, accessible by keyboard and usable on mobile |
| Cart: boundary tests | A new `CartBoundaryTest.java` only | HTTP tests cover missing quantity, non-integer quantity and exactly 99 units; no production edits |

Use the [worker cards](/workshops/copilot-app/prompts/#parallel).
The test worker may use `spring-boot-testing`. If it finds a behavior defect,
report it rather than editing the other worker's files or weakening assertions.

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

## What you have learned

- Create two isolated App sessions from **workshop-complete** and verify their shared starting point before editing.
- Assign each session a specific task and set of files so it can work independently without changing the other session's code.
- Supervise progress and collect reviewed commits, test results and limitations for integration.
