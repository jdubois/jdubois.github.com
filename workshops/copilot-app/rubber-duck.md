---
layout: default
title: Review with rubber duck
description: "Ask the built-in rubber duck agent to challenge the combined implementation before final handoff."
permalink: /workshops/copilot-app/rubber-duck/
workshop: true
next: subagents
next_title: Coordinate five subagents
---

## What you will learn

Use Copilot App's **rubber duck** agent for an independent critique, assess
its findings and distinguish a review from permission to apply corrections.

## A critic, not another implementer

Traditional rubber ducking means explaining your code to expose mistakes
in your reasoning. Copilot's built-in **rubber duck agent** talks back:
it reviews a plan, implementation or tests and reports meaningful problems.
It does not edit the code itself.

Copilot selects a different critic model when a suitable one is available.
You do not need to open another project session or manually choose the critic model.
A second opinion can catch blind spots, but it is not proof of correctness.
See <a href="https://docs.github.com/en/copilot/concepts/agent-capabilities/choosing-and-delegating-agent-work/getting-a-second-opinion" target="_blank">the rubber duck guide</a>.

## Challenge the combined result
{: #review-prompt}

Stay in **Cart: boundary tests**, on the verified combined result from the
previous chapter. If you used local recovery, keep that recovered checkout;
do not switch back to incomplete remote `main`. Use **Interactive**.

Type **`/rubber-duck` in the App composer**, not a terminal, with this request:
If working in a separate reference checkout, replace `workshop-start` with
`v2-start` in the prompt.

```copilot
/rubber-duck Review the full shopping-cart change from workshop-start
to this checked result, including the quantity fix, removal, Canvas UI
changes, query optimization and both parallel contributions.
Look for concrete behavior regressions, missing edge-case coverage,
incorrect cents/totals and evidence that does not match the code.
Keep the existing acceptance criteria. Do not edit files, run the app,
change branches, commit, push or merge.
Report each meaningful finding with its file/location, impact, supporting
evidence and suggested correction. Mark unverified assumptions explicitly.
Return the actual critic's findings, or explain why it could not run.
```

Inspect the agent activity and returned critique. Do not count a main-agent
summary as an independent review unless the critic actually ran.

## Decide what to do with the findings

Ask the main Copilot agent to explain which findings it accepts, rejects or
needs more evidence for. Check the cited code yourself. Do not add a defect
just to make the demonstration interesting, and do not accept style-only
suggestions as blocking regressions.

If a finding needs correction, authorize that correction separately.
Ask Copilot to prepare a **normal follow-up feature branch from this checked
result before editing**; never commit on the verification checkout or push
directly to `main`. Review the corrected diff, run the full suite and repeat
the affected preview. Any follow-up PR needs its own review and merge approval.
Otherwise record the finding as deferred and continue without changing code.

**Done when:** you have an actual critique, a decision for each actionable
finding and evidence for any correction you accepted.
Record that on the [worksheet](/workshops/copilot-app/worksheet/).

<details markdown="1">
<summary>If the command or critic model is unavailable</summary>

Check the App's `/` picker. You can also ask “Rubber duck this implementation”
in the same composer. If no independent critic can run, use a facilitator's
demonstration or an ordinary review and record the limitation. Do not describe
a single-model reread as a different-model critique or broaden account permissions.

</details>

The next exercise is different: instead of critiquing this implementation,
you will coordinate five specialists to **build mock checkout** on one
feature branch, after approving its shared contract.

## What you have learned

- Request an independent critique through **/rubber-duck**, without opening another session.
- Assess concrete findings against code and acceptance criteria rather than treating the critic as an authority.
- Separate review from editing and merge permission, and verify accepted corrections on a normal feature branch.
