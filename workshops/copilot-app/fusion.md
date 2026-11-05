---
layout: default
title: Plan with Copilot
description: "Use Plan mode, set task boundaries and review the approach before code changes."
permalink: /workshops/copilot-app/fusion/
workshop: true
next: skills
next_title: Use a skill and add a regression test
---

## What you will learn

Use Copilot App's Plan and Interactive modes, choose an effort level and review
tool permissions before implementation.

## Agree before implementing

Use **Plan** mode for the proposed fix. Ask for the smallest change that satisfies
the [acceptance criteria](/workshops/copilot-app/ticket/). If the plan includes a
database redesign, pricing changes or fixing the later N+1 ticket, narrow it now.

```copilot
Plan the smallest fix for the repeated-add bug. Preserve validation,
server-calculated totals and all other cart items. Use the existing
stack. First reproduce the regression; do not change production code
until the plan and failing test are reviewed.
```

**App tip:** an early, specific correction is cheaper than a large unwanted
diff. “Keep the repository query unchanged; that is the next ticket” gives the
agent a clearer boundary than “make it simpler.”

## Match autonomy to the task

Use **Interactive** while learning and steering the bug fix. Use **Autopilot**
later for a clearly scoped feature after approving its plan and permissions,
if your account permits it. Autopilot still needs boundaries: do not authorize
pushes, merges, restarts or dependency changes unless they are part of the task.

Check the current directory and branch before accepting edits. A chat for
brainstorming is not the same as a project session that changes a repository.

## Choose effort deliberately

Start with **Fusion Standard**, or keep the coding model you selected in
[setup](/workshops/copilot-app/setup/#open-it-in-copilot-app).
With Fusion, High is optional for a difficult investigation; Max is not required.
Higher effort can mean longer waits and more usage;
it does not guarantee a fixed number of reviewers. Fusion's model selection
is separate from running sessions in different worktrees.

Before implementation, find the **mode, model/effort and tool-permission
controls** in your App build. Confirm Interactive and the intended effort;
check which terminal and file actions require approval. Do not broaden
permissions just to dismiss a prompt. After one response, look for model-routing
or usage details. Record what the App shows; if details are missing, mark them
"not exposed" rather than guessing which model produced the answer.
Labels and available details may vary with the App version.

Keep the model/effort stable unless the task needs a change. Later,
[Chronicle](/workshops/copilot-app/tokens/) will help you reflect on the actual
workflow rather than assume that “more effort” always means “better.”

**Review every changed file.** Copilot's summary may not mention every edit,
including edits from an approach it later discarded.

## What you have learned

- Use **Plan** mode to agree on a small fix and correct its scope before implementation.
- Use **Interactive** to guide the work, and decide when a clearly scoped Autopilot task is appropriate.
- Choose **Fusion Standard** or a strong coding model, inspect the details the App provides and avoid assuming that higher effort always produces a better result.
- Check tool permissions and review changed files rather than relying only on the final summary.
