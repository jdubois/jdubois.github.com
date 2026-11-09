---
layout: default
title: Modes and effort
description: "Use Plan mode, set task boundaries and review the approach before code changes."
permalink: /workshops/copilot-app/modes/
workshop: true
next: skills
next_title: Use a skill to fix the bug
---

## What you will learn

Use Copilot App's Plan and Interactive modes, choose an effort level and review
the plan before implementation.

## Match autonomy to the task

Stay in **Cart: quantity bug**, the session you used to investigate.
**No new session or worktree is needed.** Change modes using the mode control
beside the composer; the conversation and working directory stay the same.

| Mode | When to use it |
|---|---|
| **Plan** | Ask Copilot to investigate and propose an approach, then review it before implementation. Use it now to plan the quantity fix. |
| **Interactive** | Work with Copilot step by step, giving feedback and reviewing actions. Use it for the next chapter's tests and fix. |
| **Autopilot** | Let Copilot carry out a clearly scoped task with fewer pauses. Try it later, after agreeing on the feature, permissions and completion criteria. |

Mode and permissions are separate. Autopilot does not mean you have authorized
pushes, merges, application restarts or dependency changes.

## Choose effort deliberately

Keep **Fusion Standard**, or the coding model you selected in
[setup](/workshops/copilot-app/setup/#open-it-in-copilot-app).
Higher effort can help with a difficult investigation, but may take longer and
use more resources. It is not needed just to plan this small fix.
Keep the model/effort stable unless the task needs a change.

## Plan the quantity fix

The investigation explained the bug. Now agree on what a correct fix must do
before changing code.

### Acceptance criteria

- Adding 1 Notebook twice produces one line, quantity 2, total €20.
- Adding 2 more units to an existing quantity 3 produces quantity 5.
- Adding a new product still works. Quantities remain 1–99, including
  the accumulated quantity; rejected input leaves state unchanged.
- Prices and totals come from the server. Do not patch only the UI.

Keep the scope small: no checkout, stock management, accounts, new dependencies
or query optimization yet. The later performance ticket is a separate task.

Switch to **Plan** in this same session, then send:

```copilot
Plan the smallest fix for the repeated-add bug:
- Adding one €10 Notebook twice must produce quantity 2 and total €20.
- Adding 2 units to an existing quantity 3 must produce quantity 5.
- Adding a new product must still work. Quantities must remain 1–99,
  including the accumulated quantity; rejected input must leave state unchanged.
- Preserve server-calculated prices/totals and all other cart items.
Keep the existing stack. No checkout, stock management, accounts,
new dependencies or query optimization.
Plan a failing regression test before the production fix.
Do not edit files yet; wait for my review.
```

## Review the plan, then prepare to write tests

When Copilot creates the plan, it should open a **plan canvas on the right**.
Read the plan in that canvas alongside the conversation.

Check that the plan establishes a failing regression test first, then fixes
quantity accumulation and verifies the result. If it includes a database
redesign, pricing changes or the later N+1 ticket, ask Copilot to revise it.

Once the plan is clear, **do not start the whole implementation yet**.
Leave planning without launching implementation and return to **Interactive**
in this same session. If the App presents a plan-approval screen, choose the
option that returns to the session without implementing the plan.

Continue to [Use a skill to fix the bug](/workshops/copilot-app/skills/).
Production code stays unchanged until the generated tests show the bug;
then implement, review and verify the fix in that same chapter.

## What you have learned

- Use **Plan** mode to agree on a small fix and correct its scope before implementation.
- Use **Interactive** to guide the work, and decide when a clearly scoped Autopilot task is appropriate.
- Keep a suitable model and effort level rather than increasing effort automatically.
- Review the plan before moving to tests and implementation in the same session.
