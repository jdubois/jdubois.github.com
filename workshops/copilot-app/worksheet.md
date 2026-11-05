---
layout: default
title: Workshop worksheet
description: "Keep enough evidence to explain your result without copying your entire history."
permalink: /workshops/copilot-app/worksheet/
workshop: true
---

## A small record for each ticket

Copy this once per ticket into your own notes:

| Field | Your observation |
|---|---|
| Ticket and acceptance criteria | |
| App session, source directory and handoff branch | |
| Mode, model and effort | |
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

## Parallel handoff

Keep each worker's handoff: its branch/commit, owned files, executed checks and
limitations. Both must start from `workshop-complete`; let Copilot capture the
commit details. Only record a preview or runtime result if that worker ran the
matching application. Mark integration checks **pending** until you test the
merged result.

## Agent Merge and integration

| Field | Your observation |
|---|---|
| Own repository and integration target (`workshop-complete`, not `main`) | |
| UI PR link, head (worker branch and reviewed commit) and CI results | |
| UI PR merge authorization and actual status | |
| Tests and preview after the UI merge | |
| Boundary-test PR link, head (worker branch and updated commit) and fresh CI results | |
| Boundary-test PR merge authorization and actual status | |
| Agent Merge corrections or conflicts reviewed | |
| Final integration checkout, both contributions and full-suite results | |
| Recovery used, open PRs and unfinished work | |

Keep the PRs sequential. A running agent, local test pass or enabled merge
permission is not confirmation that GitHub merged the PR. If using local
recovery, record **Agent Merge not completed: local recovery used**.
