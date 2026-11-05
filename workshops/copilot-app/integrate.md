---
layout: default
title: Integrate the branches
description: "Review two pull requests, use Agent Merge one at a time, and verify the combined application."
permalink: /workshops/copilot-app/integrate/
workshop: true
next: tokens
next_title: Improve usage with Chronicle
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
| **Cart: boundary tests** session | Update, review and merge the test PR second |
| **Cart: integration** session, created below | Test and preview the merged application |

Use the [worksheet](/workshops/copilot-app/worksheet/#agent-merge-and-integration)
to record each completed step.

## Inspect both results

Use the session view and **Changes** to inspect each worker's committed change
and handoff. Keep its branch and commit in the handoff; let Copilot use them
directly rather than copying commit IDs into commands.
Do not guess branch names from session titles.

Check that both began at `workshop-complete`, changed only their assigned files
and preserved the existing 12 acceptance tests. Inspect the UI worker's preview
and the test worker's test output.

## Prepare the integration branch

Use **`workshop-complete` as the integration branch**, not `main`: it already
contains the accepted quantity fix, removal feature and query optimization.
The workers started from this same version.
Create one project session named **Cart: integration**, choosing **New worktree**
and **`workshop-complete` as the base branch**. Keep this session for the rest
of the chapter. If that base is unavailable, ask the facilitator rather than
choosing `main`.

In **Cart: integration**, ask Copilot:

```copilot
Confirm origin is my own workshop repository, not the template repository.
Check that workshop-complete contains the accepted quantity fix, removal
feature, query optimization and all 12 supplied acceptance tests.
Run ./mvnw -q test. Stop if tests fail or any acceptance case is skipped.
Publish workshop-complete to my repository without force-pushing.
If the remote branch already exists, compare it and ask before changing it.
Do not push main, open a PR or merge anything yet.
```

## Open the two worker PRs

**Base** means the branch receiving the changes: `workshop-complete`.
**Head** means the worker branch supplying the changes.

Paste this once in **Cart: empty-state UX**, then once in **Cart: boundary tests**:

```copilot
Confirm this session's branch tip equals its reviewed handoff commit and the
working tree is clean. If not, stop for renewed review.
Show my repository, this worker's branch and proposed PR target before pushing.
After I approve, publish only this worker branch without force-pushing,
then create a PR with base workshop-complete and head this worker branch.
The diff must contain only this worker's contribution, not the earlier tickets.
Do not enable Agent Merge or merge anything.
```

In each PR's overview, check the repository and branch names:
**`base: workshop-complete` ← `head: your worker branch`**.
Stop if the base shows `main` or the diff includes the earlier tickets.

## Merge the UI PR first

Open the UI PR in the App. Inspect its diff and CI results; use the UI worker's
session for its preview evidence. The template's **Shopping-cart checks**
workflow runs on this target branch too. Its **tests** job must actually pass.

Return to **Cart: empty-state UX**. Open the dropdown beside **Create PR**
(or **Agent Merge**, if already selected), choose **Agent Merge**, and inspect
its options **before starting it**. First allow repairs only:
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
Merge this reviewed UI PR into workshop-complete in my repository once the
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

Return to **Cart: integration** and ask:

```copilot
Fetch origin in my own workshop repository. Use the latest remote
origin/workshop-complete, not the possibly stale local workshop-complete.
Fast-forward only this integration session's clean branch to that revision.
If it has edits or cannot fast-forward, stop and ask; do not reset anything
or change another session's checkout.
Confirm it contains the UI PR's actual merged result, including a squash merge,
not just whether the original worker commit is an ancestor.
Run ./mvnw -q test and report the executed counts and any failures or skips.
```

Stop if verification fails. Before previewing, stop the old shop with
**Ctrl+C in the terminal that started it**. In the **Cart: integration**
session's directory, start the reviewed copy:

```sh
./mvnw spring-boot:run
```

**Done when:** this checkout contains the UI merge, the original 12 tests pass
without skips, and the empty-cart catalogue link works with a keyboard and
a narrow viewport.

## Update and merge the test PR

Return to **Cart: boundary tests**, not the integration session. Ask:

```copilot
Fetch origin and merge the latest origin/workshop-complete into this test
worker branch. Keep the PR base workshop-complete and its head this worker branch.
Do not reset workshop-complete or this branch, discard either worker's changes
or force-push. Show any proposed conflict resolution for approval.
Run ./mvnw -q test; stop if tests fail or any acceptance case is skipped.
Show the updated diff and ask before pushing this branch to update its PR.
Do not enable Agent Merge or merge the PR yet.
```

Review the updated test PR and **fresh CI for its new revision**. Use the same
repair-only Agent Merge steps as for the UI PR, this time in **Cart: boundary
tests**, with corrections limited to its test scope. Preserve the accepted UI.
Review any repairs with **Merge pull request** still off. Then explicitly ask:

```copilot
Merge this reviewed boundary-test PR into workshop-complete in my repository
once the tests job and all required checks and approvals pass.
Preserve both workers' contributions, the 12 supplied acceptance tests and
the boundary tests. Do not bypass protections or change the PR base.
Ask before any correction outside the test worker's scope.
```

Enable **Merge pull request** and confirm the App's authorization prompt.
**Done when:** this second PR is also **Merged**.

## Verify the combined application

Return to **Cart: integration**. Repeat the
[synchronization and test prompt](#check-ui-merge), this time asking Copilot to
confirm **both PRs' merged results** are included. Do not use a worker checkout
or assume the local branch has updated itself.

The full suite should now contain the original **12 tests plus the new boundary
cases**, all executed with no failures/errors/skips. Check the reports for every
acceptance class and `CartBoundaryTest`; a successful command that ran no tests
does not verify the change.

Stop the previous shop in its owning terminal and restart the final reviewed
copy with the same startup command before previewing it. Confirm repeated adds,
removal and the empty-cart link still work. An individual PR passing tests does
not establish that the merged result works.

The combined result is on **`workshop-complete`**, not `main`. Continue to
Chronicle and the final review from this integration session. No additional PR
to `main` is required for this exercise. Keep the two PR links, CI results and
combined checks on the [worksheet](/workshops/copilot-app/worksheet/).

<details markdown="1" id="local-recovery">
<summary>Recovery: GitHub, CI or Agent Merge is unavailable</summary>

Preserve the worker branches and any open PRs. Record the blocker and which
PRs, if any, actually merged. Disable Agent Merge in each worker session with
an open PR before integrating locally, so it cannot merge in the background.
Do not bypass protections,
invent CI results or report a local merge as Agent Merge completion.

Use **Cart: integration**. If it does not exist yet, create it with
**New worktree**, based on local **`workshop-complete`**.
Give Copilot both reviewed handoffs and ask:

```copilot
Inspect the current integration branch, both handoffs and any PRs already merged.
If GitHub is reachable, fetch origin and fast-forward this clean session
to origin/workshop-complete first; ask if that would discard or conflict with work.
Use actual PR merge results to recognize squash merges, not just worker ancestry.
If remote status cannot be checked, record it as unknown.
Preserve existing work; do not reset branches or merge a contribution twice.
Merge the accepted UI contribution if it is not already included.
Run ./mvnw -q test and stop if it fails.
Then merge the accepted boundary-test contribution if not already included.
Run ./mvnw -q test again.
Use the actual reviewed commits, not inferred branch names or newer changes.
Ask before resolving a conflict or using an unavailable handoff.
Do not push, merge remote PRs or enable Agent Merge.
```

Perform the same combined tests and preview described above. If a conflict
occurs, review both contributions rather than automatically choosing one side.
Continue from this local integration session, not a remote branch that may
still be incomplete. Mark **Agent Merge not completed: local recovery used**.

</details>

Record whether the result is ready, needs correction or remains unfinished. Then use
[Chronicle](/workshops/copilot-app/tokens/) to reflect on the workshop's actual
sessions, including the parallel work and integration.

## What you have learned

- Use **Changes** and each session's handoff to check its scope, committed code and reported results.
- Target the reviewed integration branch, authorize Agent Merge for one PR at a time and confirm each PR actually merged.
- Verify the merged application, rather than assuming that two individually passing branches will work together.
