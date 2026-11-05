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
push branches, create PRs and merge them. If these are unavailable, use the
[local recovery steps](#local-recovery) and record that Agent Merge was not run.

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
The workers started from this same version. In the session holding that
reviewed base, ask Copilot:

```copilot
Confirm origin is my own workshop repository, not the template repository.
Check that workshop-complete contains the accepted quantity fix, removal
feature, query optimization and all 12 supplied acceptance tests.
Run ./mvnw -q test. Stop if tests fail or any acceptance case is skipped.
Publish workshop-complete to my repository without force-pushing.
If the remote branch already exists, compare it and ask before changing it.
Do not push main, open a PR or merge anything yet.
```

In each worker session, use its reviewed handoff to ask Copilot to publish
**only that worker's branch** and create a PR with **`workshop-complete` as
the base**. Review the proposed branch and repository before approving a push.
Check the PR's base and head in the App: the UI PR should contain only the UI
contribution, and the test PR only the boundary tests, not the earlier tickets.
Do not start Agent Merge on either PR yet.

## Merge the UI PR first

1. Open the UI PR in the App and inspect its diff, preview evidence and CI
   results. The template's **Shopping-cart checks** workflow runs on PRs to
   this integration branch too. Confirm its **tests** job actually ran;
   missing, failed or skipped tests are not a pass.
2. In the UI worker's session, enable **Agent Merge** using the control at
   the top. Review the allowed actions before authorizing fixes. Leave the
   test PR's Agent Merge off.
3. After reviewing the work, enable **Merge pull request** in the Agent Merge
   options if your App shows that setting, confirm any permission prompt,
   and explicitly authorize this PR:

```copilot
Use Agent Merge for this UI PR only, targeting workshop-complete in my repository.
Merge once the tests job and all required checks and approvals pass.
Preserve the acceptance tests and assigned scope. Do not bypass protections
or change the PR base. Stop and ask if a fix needs changes outside this scope.
Do not start or merge the boundary-test PR yet.
```

Follow progress in the PR view. Review any new commits made to address checks,
feedback or conflicts. If the combined diff is no longer acceptable, turn off
merge permission and ask for a correction. Confirm the PR status is **Merged**;
an enabled Agent Merge control or passing CI alone does not establish that.

## Check the result, then merge the test PR

Open an integration session from the **updated remote `workshop-complete`**
branch. Ask Copilot to confirm that its checkout contains the merged UI PR and
has no uncommitted changes, then run:

```sh
./mvnw -q test
```

Stop and resolve failures before proceeding. Before previewing this checkout,
stop the old shop with **Ctrl+C in its owning terminal**, then start the reviewed
integration copy from its own directory:

```sh
./mvnw spring-boot:run
```

Preview the empty cart's catalogue link with keyboard navigation and a narrow
viewport.

Return to the test worker's PR. Keep **`workshop-complete` as its base**; do
not reset that branch to the original shared starting point. Ask Copilot to
update the test branch with the now-merged UI contribution, without discarding
either worker's changes or force-pushing. Review any conflict resolution and
run the full suite. Check fresh CI for the updated PR before granting merge
permission.

Enable Agent Merge for this second PR and explicitly authorize it to merge
into `workshop-complete` only after the **tests** job and all required checks
and approvals pass. Keep the same scope and protection boundaries as the UI
PR. Confirm this PR is **Merged**, too.

## Verify the combined application

Ask Copilot to update the integration session to the latest remote
`workshop-complete` without overwriting local work. Confirm it contains both
merged PRs and is clean, then run the full suite again:

```sh
./mvnw -q test
```

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
PRs, if any, actually merged. Disable Agent Merge on open PRs before integrating
locally, so it cannot merge them in the background. Do not bypass protections,
invent CI results or report a local merge as Agent Merge completion.

In your integration session based on **`workshop-complete`**, give Copilot the
two reviewed handoffs and ask:

```copilot
Inspect the current integration branch, both handoffs and any PRs already merged.
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
