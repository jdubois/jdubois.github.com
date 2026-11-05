---
layout: default
title: Review and hand off
description: "Review the complete change, check your results and record what remains unfinished."
permalink: /workshops/copilot-app/finish/
workshop: true
---

## What you will learn

Use Copilot App to review the full workshop change, verify the final result and
prepare a clear handoff.

## Final review
{: #final-review}

Inspect **Changes** in the App, then ask Copilot for a full comparison with
your original starter. Include already committed tickets, current edits and
new files—not just the latest uncommitted change.
If continuing from a separate reference checkout, compare from **`v2-start`**
instead and note that your work is based on the reference.
Ask for a review without edits:

The comparison starts at the **`workshop-start` tag**, not the PR's integration
target. This only selects the diff to review; it does not move your code or
change where a PR merges.

```copilot
Review the full starter-to-current change, including committed tickets,
staged/unstaged edits and new files, for cart behavior, validation, server
prices, removal, the query change and both parallel workers' contributions.
Use workshop-start as the comparison starting point only
(v2-start only in a separate reference checkout).
Do not edit, reset branches or retarget PRs. Identify concrete regressions or missing evidence,
not style preferences.
```

Inspect findings yourself, request precise corrections, then rerun the suite
below. Preview repeated adds, removal, empty state and the sample cart.

## Check your results

| Outcome | Evidence |
|---|---|
| Fixed repeated additions | Notebook added twice → quantity 2 / €20, persists after reload; regression tests pass |
| Generated removal | Correct DELETE response, working button, other products and totals preserved |
| Investigated N+1 | Matched MCP before/after request profiles, same workload, query tests green |
| Coordinated parallel work | Two isolated sessions with the same starting point, two reviewed PRs merged sequentially with Agent Merge, and a tested combined result; or an explicit local-recovery record |
| Reviewed token usage | Chronicle report or a note that it was unavailable/not run, plus one improvement based on the workshop sessions |
| Used Copilot App effectively | Reviewed plan, loaded skills, inspected changed files and checked test output |

Use the [worksheet](/workshops/copilot-app/worksheet/); mark demos, reference
solutions and unavailable features. Use tool responses and test output to
support the results, not just Copilot's final summary.

## Verify before committing

After all three tickets and the parallel integration, run the **full suite**,
including the generated boundary tests:

```sh
./mvnw -q test
```

The supplied classes contain **12 tests**, with no failures/errors/skips;
the integrated boundary tests add further cases. Check the reports for every
acceptance class and `CartBoundaryTest`; no supplied case may be removed.
If a ticket or worker remains unfinished, record that explicitly rather than
presenting partial work as the complete workshop result.

Ask Copilot to show the intended file list and diff, including new files.
Review them in **Changes**, then ask it to commit only the accepted changes
and provide a concise handoff:
what changed, what was checked, what is still unknown.

## Where your result lives

The integration exercise landed the two worker PRs on **`workshop-complete`**,
not `main`. Review that combined branch in your integration session and retain
both PR links and CI results. No additional PR to `main` is required.

If you used local recovery, keep the local combined branch and record the
GitHub, CI or Agent Merge blocker. Do not describe open PRs as merged or local
results as completed CI checks. Record any unfinished work in the handoff.

## Keep one useful habit

Leave with the reviewed result, a record of unfinished work,
and the reusable prompt or usage habit you chose with Chronicle.

The transferable loop is **reproduce → plan → implement → inspect → verify**.
Skills provide procedure, MCP provides evidence, and Chronicle helps you improve
how you work. None replaces your judgment.

## What you have learned

- Ask Copilot to review the entire change from **workshop-start**, including earlier commits, current edits and new files.
- Use **Changes**, test output and a shop preview to assess the result, and record unfinished work or unverified features.
- Prepare a concise handoff with the integration branch, actual PR/CI status and any local recovery or unfinished work.
- Carry forward one improved Copilot habit from the workshop, such as a clearer initial prompt or more focused context.
