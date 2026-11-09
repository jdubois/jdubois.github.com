---
layout: default
title: Merge PRs with Agent Merge
description: "Review two pull requests, use Agent Merge one at a time, and verify the combined application."
permalink: /workshops/copilot-app/integrate/
workshop: true
next: rubber-duck
next_title: Review with rubber duck
---

## What you will learn

Review contributions from parallel Copilot App sessions, use **Agent Merge**
to land their pull requests one at a time, and verify the combined result.

## What Agent Merge does

Agent Merge manages a GitHub pull request: it can address review feedback,
fix failing CI and resolve merge conflicts. With your explicit permission, it
can also merge the PR when GitHub allows it. It does not replace your review
or bypass repository protections. See the
<a href="https://docs.github.com/en/copilot/how-tos/github-copilot-app/managing-issues-and-pull-requests#merging-a-pull-request" target="_blank">App's Agent Merge guide</a>.

Use your own workshop repository, with GitHub Actions enabled and permission to
push branches, create PRs and merge them. Confirm your organization allows
Agent Merge and that any required reviewer can approve your work.
If these are unavailable, use the
[local recovery steps](#local-recovery) and record that Agent Merge was not run.

| Where you work | What you do there |
|---|---|
| **Cart: empty-state UX** session | Publish, review and merge the UI PR |
| **Cart: boundary tests** session | Update and merge the test PR, then check merged `main` |

Use the [worksheet](/workshops/copilot-app/worksheet/#agent-merge-and-integration)
to record each completed step.

## Inspect both results

Use the session view and **Changes** to inspect each worker's committed change
and handoff. Keep its branch and commit in the handoff; let Copilot use them
directly rather than copying commit IDs into commands.
Do not guess branch names from session titles.

Check that both began at the same updated `main` commit recorded in their
handoffs, changed only their assigned files
and preserved the existing 12 acceptance tests. Inspect the UI worker's preview
and the test worker's test output.

If a boundary case failed, first complete the
[separate production correction](/workshops/copilot-app/parallel/#boundary-fix).
Keep its reviewed handoff and passing rerun; repair-only Agent Merge does not
authorize production edits in the test-only worker.

**Both worker PRs target `main`.** The previous chapter already merged the
quantity fix, removal feature and query optimization there before the workers
started. **Keep the two existing worker sessions; do not create another session
or integration branch.** If the preparation PR is not merged, use
[local recovery](#local-recovery) instead.

## Open the two worker PRs

**Base** means the branch receiving the changes: `main`.
**Head** means the worker branch supplying the changes.

Paste this once in **Cart: empty-state UX**, then once in **Cart: boundary tests**:

```copilot
Confirm this session's branch tip equals its reviewed handoff commit and the
working tree is clean. If not, stop for renewed review.
Show my repository, this worker's branch and proposed PR target before pushing.
After I approve, publish only this worker branch without force-pushing,
then create a PR with base main and head this worker branch.
The diff must contain only this worker's contribution, not the earlier tickets.
Do not enable Agent Merge or merge anything.
```

In each PR's overview, check the repository and branch names:
**`base: main` ← `head: your worker branch`**.
Stop if the target is different or the diff includes the earlier tickets:
those should already be on `main`.

## Merge the UI PR first

Open the UI PR in the App. Inspect its diff and CI results; use the UI worker's
session for its preview evidence. The template's **Shopping-cart checks**
workflow runs on this target branch too. Its **tests** job must actually pass.

Return to **Cart: empty-state UX**. Open the dropdown beside **Create PR**
(or **Agent Merge**, if already selected), choose **Agent Merge**, and inspect
its options **before starting it**. Confirm its linked PR number, repository
and head branch match this worker, not the merged preparation PR.
If the worker PR is not linked, ask the facilitator to link the existing PR
in the App; do not create a duplicate or start automation on another PR.
First allow repairs only:
leave **Merge pull request** unchecked. This is the option that grants merge
permission. If you cannot confirm that merging is off, do not start it; ask
the facilitator.

Review the repair actions, then select the **Agent Merge** button to start it.
Tell Copilot to fix blockers only within the UI worker's scope, preserve all
acceptance tests and ask before any out-of-scope change. Do not authorize a
merge yet. Leave the test PR's Agent Merge off.

Review the UI PR's complete updated diff, including any repair commits, and
its latest CI results. Once you accept the result, ask:

```copilot
Merge this reviewed UI PR into main in my repository once the
tests job and all required checks and approvals pass.
Preserve the acceptance tests and UI worker scope. Do not bypass protections
or change the PR base. Ask before any out-of-scope correction.
Do not start or merge the boundary-test PR.
```

Enable **Merge pull request** in those Agent Merge options and confirm the
App's authorization prompt. After authorization, Agent Merge may make further
permitted repairs and merge without another review pause. Keep merging off
if you need to inspect another correction first.

**Done when:** the UI PR's status is **Merged**, not merely green or waiting.

<details markdown="1">
<summary>If checks or merging do not progress</summary>

A queued or running **tests** job means wait. A failed job needs a correction.
If no run appears, check your repository's **Actions** tab and whether Actions
is enabled; ask the facilitator to trigger checks for the current PR revision.
A skipped job is not a pass.

A denied permission, disallowed Agent Merge or unavailable required approval
is a blocker, not a reason to retry repeatedly or broaden permissions.
If checks pass but the PR remains open, check **Merge pull request** and the
PR's reported blockers. Never bypass repository rules.
If you cannot proceed, turn off Agent Merge in the worker session and use
[local recovery](#local-recovery).

</details>

## Check the UI merge
{: #check-ui-merge}

Confirm GitHub shows the UI PR as **Merged** and the **tests** job passes for
that merged revision on `main`. Stop if it fails. Next, bring that UI change
into the existing test worker branch; no new session is needed.

## Update and merge the test PR

Select **Cart: boundary tests** in the App sidebar and ask:

```copilot
Fetch origin and merge the latest origin/main into this test
worker branch. Keep the PR base main and its head this worker branch.
Do not reset main or this branch, discard either worker's changes
or force-push. Show any proposed conflict resolution for approval.
Run ./mvnw test; stop if tests fail or any acceptance case is skipped.
Show the updated diff and ask before pushing this branch to update its PR.
Do not enable Agent Merge or merge the PR yet.
```

Review the updated test PR and **fresh CI for its new revision**. Use the same
repair-only Agent Merge steps as for the UI PR, this time in **Cart: boundary
tests**, with corrections limited to its test scope. Preserve the accepted UI.
Review any repairs with **Merge pull request** still off. Then explicitly ask:

```copilot
Merge this reviewed boundary-test PR into main in my repository
once the tests job and all required checks and approvals pass.
Preserve both workers' contributions, all earlier reviewed tests and
the boundary tests. Do not bypass protections or change the PR base.
Ask before any correction outside the test worker's scope.
```

Enable **Merge pull request** and confirm the App's authorization prompt.
**Done when:** this second PR is also **Merged**.

## Verify the combined application

Stay in **Cart: boundary tests**. Both PRs are merged, so use this same
session to check the code now on `main`, rather than the old worker version.
Ask Copilot:

```copilot
Confirm both worker PRs are Merged in my own repository. Fetch origin.
Confirm this session's working tree is clean; stop if it has uncommitted work.
Preserve the worker branches and their commits. In this session's own worktree,
check out the exact latest origin/main commit for verification, without moving
the main branch or changing another session's checkout. Do not create a new
session or branch, reset anything or push.
Confirm the checked-out commit equals origin/main and contains both PRs'
actual merged results, including squash merges.
Run ./mvnw test and report the executed counts and any failures or skips.
```

The full suite should now contain **all earlier reviewed tests plus the new boundary
cases**, all executed with no failures/errors/skips. Check the reports for every
acceptance class and `CartBoundaryTest`; a successful command that ran no tests
does not verify the change.

Stop the old shop with **Ctrl+C in the terminal that started it**. In the
**Cart: boundary tests** session's directory, start the checked-out main version:

```sh
./mvnw spring-boot:run
```

Confirm repeated adds, removal and the empty-cart catalogue link still work,
including keyboard navigation and a narrow viewport. An individual PR passing
tests does not establish that the merged result works.

The combined result is now on **`main`**. Continue to the independent review
and checkout implementation in the same **Cart: boundary tests** session.
Without an additional production correction, there are three PRs:
the three-ticket preparation PR, the UI PR and the boundary-test PR.
Keep their links, CI results and
combined checks on the [worksheet](/workshops/copilot-app/worksheet/).

<details markdown="1" id="local-recovery">
<summary>Recovery: GitHub, CI or Agent Merge is unavailable</summary>

Preserve the worker branches and any open PRs. Record the blocker and which
PRs, if any, actually merged. Disable Agent Merge in each worker session with
an open PR before integrating locally, so it cannot merge in the background.
Do not bypass protections,
invent CI results or report a local merge as Agent Merge completion.

Stay in **Cart: boundary tests** and give Copilot both reviewed handoffs.
This worker already has the boundary tests; it only needs any missing accepted
UI changes. Ask:

```copilot
Confirm the working tree is clean and this is the reviewed boundary-test
worker branch with its accepted tests. If not, stop and ask before switching.
Preserve both worker branches, their commits and any unfinished work.
If the preparation PR merged and GitHub is reachable, fetch origin and merge
origin/main into this test worker branch, keeping its boundary tests.
If preparation used local recovery, keep the accepted local starting point;
do not replace it with starter main. If remote status is unavailable, mark
it unknown and use only the recorded reviewed local results.
Check whether the accepted UI result is already included, accounting for
squash merges. Merge the reviewed UI handoff commit only if its changes
are missing. Do not merge the test branch into itself or apply changes twice.
If boundary tests needed a separate production correction, include its
reviewed handoff only if missing; do not implement a new fix in this test worker.
Ask before resolving a conflict, or if a reviewed handoff cannot be found.
Run ./mvnw test and report all counts, failures and skips.
Do not push, merge remote PRs or enable Agent Merge.
```

Perform the same combined tests and preview described above. If a conflict
occurs, review both contributions rather than automatically choosing one side.
Continue in **Cart: boundary tests** using this checked local result, not a
remote `main` that may still be incomplete. Skip the normal-path checkout of
`origin/main`: it could discard the recovered result from your preview.
Mark **Agent Merge not completed: local recovery used** and record whether
remote `main` actually contains the work.

</details>

Record whether the result is ready, needs correction or remains unfinished.
Then [get a second opinion](/workshops/copilot-app/rubber-duck/) on this
checked result before building the next feature on its own branch.

## What you have learned

- Use **Changes** and each session's handoff to check its scope, committed code and reported results.
- Target updated `main`, authorize Agent Merge for one worker PR at a time and confirm each PR actually merged.
- Verify the merged application, rather than assuming that two individually passing branches will work together.
