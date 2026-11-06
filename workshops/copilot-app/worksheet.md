---
layout: default
title: Workshop worksheet
description: "Keep enough evidence to explain your result without copying your entire history."
permalink: /workshops/copilot-app/worksheet/
workshop: true
---

## A small record for each ticket

Copy this once per ticket into your own notes, then use the exercise records
below in workshop order:

| Field | Your observation |
|---|---|
| Ticket and acceptance criteria | |
| App session, source directory and handoff branch | |
| Mode, model and effort | |
| Repository/file-access and MCP approvals, denials or unresolved permissions | |
| Skill loaded and guidance used | |
| Initial failing tests and assertion messages | |
| Reviewed production/test/UI changes | |
| Test command and results (tests, failures, errors, skipped) | |
| Commit and preview outcome | |
| Worked alone, with a partner, or from a demonstration/reference? | |
| Unfinished work or results not yet checked | |

Do not include API tokens, passwords, cookies or unrelated personal work.
If you use a reference solution or watch a demonstration, note which steps
you also ran yourself.

## Canvas: one observed improvement

| Field | Your observation |
|---|---|
| Active session/directory, startup instructions reviewed and server owner | |
| Browser canvas URL and selected element | |
| Observed UI issue and accepted scope | |
| impeccable guidance actually used, or unavailable | |
| Before/after keyboard and narrow-screen observations | |
| Regression results and reviewed feature handoff | |
| Native picker used, browser fallback or demonstration | |

## MCP before and after

| Field | Before | After |
|---|---|---|
| Reviewed source directory/branch | | |
| Workload: eight distinct products, GET `/api/cart` | | |
| Request ID, method/path and time | | |
| Tool names and actual arguments | | |
| Observed SELECT count | | |
| Product fields, count and total preserved? | | |
| Source: MCP call in the App, saved reference or demonstration | | |

Restart the reviewed copy after the fix and capture a fresh request profile.
Reusing the baseline profile does not show whether the optimization worked.

## Parallel handoff

Keep the preparation PR link and actual **Merged** status, its CI results,
and the updated `origin/main` commit used to start both workers.
Then keep each worker's handoff: its branch/commit, owned files, executed checks
and limitations. Both must start from that same updated `main` commit; let
Copilot capture the commit details. If preparation used local recovery, record
the accepted local starting branch/commit and **main not updated: local recovery used**.
Only record a preview or runtime result if that worker ran the
matching application. Mark integration checks **pending** until you test the
merged result.

If a boundary case needed a separate production correction, record its
reviewed branch/PR, checks and actual merge status, then the test worker's
passing rerun. A failing test is not permission for that worker to edit production.

## Agent Merge and integration

| Field | Your observation |
|---|---|
| Own repository, preparation PR status and worker PR target (`main`) | |
| UI PR link, same PR linked in its worker session, head and CI results | |
| UI PR merge authorization and actual status | |
| Tests and preview after the UI merge | |
| Boundary-test PR link, head (worker branch and updated commit) and fresh CI results | |
| Boundary-test PR merge authorization and actual status | |
| Agent Merge corrections or conflicts reviewed | |
| Merged main commit checked in Cart: boundary tests before checkout, both contributions and full-suite results | |
| Recovery used, open PRs and unfinished work | |

Keep the PRs sequential. A running agent, local test pass or enabled merge
permission is not confirmation that GitHub merged the PR. If using local
recovery, record **Agent Merge not completed: local recovery used**.

## Rubber duck: critique and decision

| Field | Your observation |
|---|---|
| Checked result and comparison starting point | |
| Actual critic invocation/model if exposed, or unavailable | |
| Finding, code/evidence and impact | |
| Accepted, rejected or deferred, with reason | |
| Follow-up branch and executed verification if corrected | |

## Five subagents: mock-checkout implementation

| Field | Your observation |
|---|---|
| Shared goal, reviewed base and checkout feature branch | |
| Approved contract, owned files and dependency order | |
| Five actual assignments/contributions; concurrency observed | |
| Questions/answers exchanged, directly or through the orchestrator | |
| Implemented API, order snapshot, atomic clearing and duplicate handling | |
| Conflicting proposals resolved or decisions still open | |
| Full-suite counts, including original classes, boundary and CheckoutContractTest | |
| Rollback, snapshot and concurrent/later-retry evidence | |
| Browser canvas receipt, cleared cart, keyboard and narrow-screen observations | |
| Reviewed checkout commit, local status and optional PR status | |
| Delegation or messaging unavailable, or demonstration | |

Mark checkout **implemented and verified**, **unfinished**, or **demonstrated**
according to the evidence. Record actual contributions, not the illustrative
exchange. Write **none exchanged** if there were no questions/answers, and
**unknown** for concurrency you did not observe. Local checkout code is not on `main` until a separate PR actually
merges. Keep the approved plan and agent activity available for Chronicle.

## Chronicle: one better habit

| Field | Your observation |
|---|---|
| Privacy choice and scope controls checked before running | |
| Requested session IDs/repository/timezone/window | |
| Returned scope and coverage | |
| Reported input/output/cache/usage values **with units**, or unavailable | |
| Usage pattern and supporting session/example | |
| One prompt/workflow change | |
| Acceptance and review checks retained | |
| Result observed, or improvement not yet checked | |

There is no required savings percentage. Different tasks are not controlled
trials. Do not convert a usage multiplier or byte count into dollars/tokens.
Keep your full Chronicle output private; share only the relevant, reviewed excerpt.
