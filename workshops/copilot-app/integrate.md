---
layout: default
title: Integrate the branches
description: "Review each session's change, then verify the combined application."
permalink: /workshops/copilot-app/integrate/
workshop: true
next: tokens
next_title: Improve usage with Chronicle
---

## What you will learn

Review contributions from parallel Copilot App sessions and integrate them one
at a time, checking the combined result after each merge.

## Inspect both results

Use the session view and **Changes** to inspect each worker's committed change
and handoff. Keep its branch and commit in the handoff; let Copilot use them
directly rather than copying commit IDs into commands.
Do not guess branch names from session titles.

Check that both began at `workshop-complete`, changed only their assigned files
and preserved the existing 12 acceptance tests. Inspect the UI worker's preview
and the test worker's test output.

## Integrate one at a time

In your integration session based on **`workshop-complete`**, give Copilot the
two reviewed handoffs and ask:

```copilot
Merge the accepted UI worker commit from its handoff using --no-ff.
Run ./mvnw -q test and stop if it fails.
Then merge the accepted test worker commit using --no-ff.
Run ./mvnw -q test again.
Use the actual reviewed commits, not inferred branch names or newer changes.
If a handoff or commit is unavailable, ask before merging.
```

The full suite should now contain the original **12 tests plus the new boundary
cases**, all executed with no failures/errors/skips. Check the reports for every
acceptance class; a successful command that ran no tests does not verify the change.

If Git reports a conflict, review what each change was intended to do. Resolve
it without discarding either contribution, then rerun the tests. Do not
automatically choose "ours" or "theirs."

Restart only the final reviewed copy if needed for preview. Confirm the empty
cart's catalogue link with keyboard navigation and a narrow viewport.
An individual branch passing tests does not establish that the merged result works.

Record whether the result is ready, needs correction or remains unfinished. Then use
[Chronicle](/workshops/copilot-app/tokens/) to reflect on the workshop's actual
sessions, including the parallel work and integration.

## What you have learned

- Use **Changes** and each session's handoff to check its scope, committed code and reported results.
- Ask Copilot to merge the reviewed commits one at a time and stop if a test fails or a conflict needs review.
- Verify the merged application, rather than assuming that two individually passing branches will work together.
