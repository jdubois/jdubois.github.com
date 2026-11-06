---
layout: default
title: Review and hand off
description: "Review the complete change, check your results and record what remains unfinished."
permalink: /workshops/copilot-app/finish/
workshop: true
---

## What you will learn

Use Copilot App to review the implemented shop and its evidence, then hand
off the completed application on **`main`**, alongside the independent critique,
five-agent contributions and delivery evidence.

## Final review
{: #final-review}

The checkout chapter already reviewed and delivered the code. Keep this final
review **read-only**, using the verified merged-main revision. If delivery was
blocked, review the preserved local result and state that limitation instead.
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
prices, removal, startup instructions, Canvas UI changes, the query change
both parallel workers' contributions and the checkout implementation.
Check stored order snapshots, atomic clearing, retry behavior and receipt UI.
Distinguish local checkout code from what is actually merged into main.
Use workshop-start as the comparison starting point only
and do not edit, reset branches or retarget PRs.
Identify concrete regressions or missing evidence, not style preferences.
```

Inspect findings yourself. If corrections are needed after delivery, ask Copilot
to create a new follow-up feature branch from the verified result before editing;
do not commit on the verification checkout, reuse the merged checkout PR or push
directly to `main`. Review the corrections and rerun the suite below. A follow-up
PR needs its own publishing and merge approval, passing checks and post-merge
verification. Do not leave accepted corrections unmerged while claiming a
completed main-branch result.

## Check your results

| Outcome | Evidence |
|---|---|
| Fixed repeated additions | Notebook added twice → quantity 2 / €20, persists after reload; regression tests pass |
| Generated removal | Correct DELETE response, working button, other products and totals preserved |
| Used a Canvas | Reviewed startup instructions, running shop preview, selected UI issue and checked correction, or an explicit fallback record |
| Investigated N+1 | Matched MCP before/after request profiles, same workload, query tests green |
| Coordinated parallel work | Preparation PR merged into `main`, two isolated sessions from that updated version, two worker PRs merged sequentially with Agent Merge, and a tested combined result; or an explicit local-recovery record |
| Requested an independent critique | Actual rubber duck findings, decisions and evidence for corrections; or a recorded unavailable critic |
| Delivered mock checkout with five subagents | Actual contributions, reviewed code, checkout PR merged into `main`, passing merged-revision checks and receipt/cart preview from verified main; or an explicit incomplete/demonstration record |
| Reviewed token usage | Chronicle report or a note that it was unavailable/not run, plus one improvement based on the workshop sessions |
| Used Copilot App effectively | Reviewed plan, loaded skills, inspected changed files and checked test output |

Use the [worksheet](/workshops/copilot-app/worksheet/); mark demos, reference
solutions and unavailable features. Use tool responses and test output to
support the results, not just Copilot's final summary.

## Verify before handing off

On the merged-main revision verified in the checkout chapter, run the **full
suite**, including generated boundary and checkout tests. For local recovery,
use the preserved result and explicitly record that it is not merged:

```sh
./mvnw -q test
```

The supplied classes contain **12 tests**, with no failures/errors/skips;
the boundary and checkout tests add further cases. Check the reports for every
acceptance class, `CartBoundaryTest` and `CheckoutContractTest`;
no supplied case may be removed. If checkout was blocked, mark its cases as
not completed rather than treating an earlier 12-test pass as checkout evidence.
If a ticket or worker remains unfinished, record that explicitly rather than
presenting partial work as the complete workshop result.

Ask Copilot to show the intended file list and diff, including new files.
Review them in **Changes**. On the normal path the accepted workshop work is
already merged; do not create another commit just to finish. If you made corrections
on a follow-up feature branch, deliver them through their own reviewed PR before
claiming they are on `main`.
Ask Copilot for a concise handoff:
what changed, what was checked, what is still unknown.

## Where your result lives

The three-ticket preparation PR and both worker PRs landed on **`main`**,
followed by the orchestrator's **checkout PR**. Stay in **Cart: boundary tests**
on the verified main revision, not the old worker or checkout feature branch.
Retain all three earlier PR links and CI results, plus the checkout PR,
feature head, merge commit, verified main commit, checks and running directory/URL.
If boundary tests required a separate production-correction PR, retain its
review, checks and actual merge status too.

**Checkout merged and verified on `main` is required for the completed normal path.**
The orchestrator performs that delivery under the checkout chapter's explicit
approval; no fixed PR number is required. Do not claim checkout is on `main`
merely because the earlier PRs merged.
If checkout remains unfinished, preserve its branch and hand off the earlier
reviewed result with that limitation, not a fictional successful order.

If you used local recovery, keep the local combined branch and record the
GitHub, CI or Agent Merge blocker. Do not describe open PRs as merged or local
results as completed CI checks. Record **verified locally; delivery blocked**
or **merged; post-merge verification blocked**, as appropriate.

## Keep one useful habit

Leave with the reviewed result, a record of unfinished work,
the independent review decisions, the delivered checkout feature
and the reusable prompt or usage habit you chose with Chronicle.

The transferable loop is **reproduce → plan → implement → inspect → verify**.
Skills provide procedure, Canvas grounds UI feedback, and MCP provides runtime
evidence. Rubber duck challenges your reasoning; subagents coordinate focused
work. Chronicle helps you improve the workflow. None replaces your judgment.

## What you have learned

- Ask Copilot to review the entire change from **workshop-start**, including earlier commits, current edits and new files.
- Use **Changes**, test output and a shop preview to assess the result, and record unfinished work or unverified features.
- Prepare a concise handoff with updated `main`, actual PR/CI status and any local recovery or unfinished work.
- Include the independent critique and checkout branch/commit, checkout PR and verified main revision, with actual verification and local-versus-merged status.
- Carry forward one improved Copilot habit from the workshop, such as a clearer initial prompt or more focused context.
