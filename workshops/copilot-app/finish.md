---
layout: default
title: Review and hand off
description: "Review the complete change, check your results and record what remains unfinished."
permalink: /workshops/copilot-app/finish/
workshop: true
---

## What you will learn

Use Copilot App to review the implemented shop and its evidence, then hand
off the result alongside the independent critique and verified checkout feature.

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
prices, removal, startup instructions, Canvas UI changes, the query change
both parallel workers' contributions and the checkout implementation.
Check stored order snapshots, atomic clearing, retry behavior and receipt UI.
Distinguish local checkout code from what is actually merged into main.
Use workshop-start as the comparison starting point only
(v2-start only in a separate reference checkout).
Do not edit, reset branches or retarget PRs. Identify concrete regressions or missing evidence,
not style preferences.
```

Inspect findings yourself. If corrections are needed, use the current reviewed
checkout feature branch. If recovery left you on a verification checkout,
ask Copilot to create a normal feature branch before editing; do not commit
on the verification checkout or push directly to `main`. Review the corrections
and rerun the suite below. Preview repeated adds, removal, empty state and
the sample cart, checkout receipt and return to shopping.

## Check your results

| Outcome | Evidence |
|---|---|
| Fixed repeated additions | Notebook added twice → quantity 2 / €20, persists after reload; regression tests pass |
| Generated removal | Correct DELETE response, working button, other products and totals preserved |
| Used a Canvas | Reviewed startup instructions, running shop preview, selected UI issue and checked correction, or an explicit fallback record |
| Investigated N+1 | Matched MCP before/after request profiles, same workload, query tests green |
| Coordinated parallel work | Preparation PR merged into `main`, two isolated sessions from that updated version, two worker PRs merged sequentially with Agent Merge, and a tested combined result; or an explicit local-recovery record |
| Requested an independent critique | Actual rubber duck findings, decisions and evidence for corrections; or a recorded unavailable critic |
| Built mock checkout with five subagents | Actual contributions, reviewed code, passing checkout regressions and receipt/cart preview; or an explicit incomplete/demonstration record |
| Reviewed token usage | Chronicle report or a note that it was unavailable/not run, plus one improvement based on the workshop sessions |
| Used Copilot App effectively | Reviewed plan, loaded skills, inspected changed files and checked test output |

Use the [worksheet](/workshops/copilot-app/worksheet/); mark demos, reference
solutions and unavailable features. Use tool responses and test output to
support the results, not just Copilot's final summary.

## Verify before handing off

After the first three tickets, parallel integration and checkout implementation,
run the **full suite**, including generated boundary and checkout tests:

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
Review them in **Changes**. The accepted workshop work is already committed;
do not create another commit just to finish. If you made corrections on a
follow-up feature branch, commit only those accepted corrections there.
Ask Copilot for a concise handoff:
what changed, what was checked, what is still unknown.

## Where your result lives

The three-ticket preparation PR and both worker PRs landed on **`main`**.
Stay in **Cart: boundary tests**, using the merged main version checked out
in the integration chapter as the starting point for the now-reviewed
checkout feature branch. Retain all
three PR links and CI results, plus the checkout branch/commit and checks.
Publishing checkout in a fourth PR is optional.

Checkout is **local feature-branch work** until you separately choose to publish
and merge it. Do not claim it is on `main` merely because the earlier PRs merged.
Any optional checkout PR needs its own review, checks and merge authorization.
If checkout remains unfinished, preserve its branch and hand off the earlier
reviewed result with that limitation, not a fictional successful order.

If you used local recovery, keep the local combined branch and record the
GitHub, CI or Agent Merge blocker. Do not describe open PRs as merged or local
results as completed CI checks. Record any unfinished work in the handoff.

## Keep one useful habit

Leave with the reviewed result, a record of unfinished work,
the independent review decisions, the reviewed checkout feature
and the reusable prompt or usage habit you chose with Chronicle.

The transferable loop is **reproduce → plan → implement → inspect → verify**.
Skills provide procedure, Canvas grounds UI feedback, and MCP provides runtime
evidence. Rubber duck challenges your reasoning; subagents coordinate focused
work. Chronicle helps you improve the workflow. None replaces your judgment.

## What you have learned

- Ask Copilot to review the entire change from **workshop-start**, including earlier commits, current edits and new files.
- Use **Changes**, test output and a shop preview to assess the result, and record unfinished work or unverified features.
- Prepare a concise handoff with updated `main`, actual PR/CI status and any local recovery or unfinished work.
- Include the independent critique and checkout branch/commit, with actual verification and local-versus-merged status.
- Carry forward one improved Copilot habit from the workshop, such as a clearer initial prompt or more focused context.
