---
layout: default
title: Facilitate and recover
description: "Prepare the workshop, check key handoffs and help participants recover without losing work."
permalink: /workshops/copilot-app/facilitator/
workshop: true
---

Copilot App is the subject; the shopping cart is the example.
Follow the [workshop flow](/workshops/copilot-app/#workshop-flow), with a break
before parallel work. Keep one workshop, without chapter deadlines.
Use this page for preparation and troubleshooting, not as another exercise.

## Before participants arrive
{: #rehearse-with-the-app}

Rehearse with the App build and accounts you will use.

| Check | Ready when |
|---|---|
| Environment | The participant's own repository opens in a worktree; the 4 baseline tests pass; one owned shop runs on port 18765 |
| App controls | Plan, Interactive, effort and permissions are understood; Fusion Standard or the [setup alternative](/workshops/copilot-app/setup/#open-it-in-copilot-app) is available |
| Skills and tools | Bundled Java skills load; Browser canvas, Pick & polish, impeccable and the two MCP tools have been tried |
| GitHub delivery | Actions is enabled; **Shopping-cart checks / tests** runs; the participant can create and merge PRs under repository rules |
| History privacy | Participants decide **before running Chronicle** whether its history access is acceptable; [transcript review](/workshops/copilot-app/tokens/#decide-before-analyzing-history) is an equal alternative |

<details markdown="1">
<summary>App rehearsal checklist</summary>

### Skills and Canvas

- The three Java skills are repository-bundled; **impeccable** is App-bundled. Demonstrate loading guidance, not reinstalling the workshop's pinned copies.
- Follow the [Canvas chapter](/workshops/copilot-app/canvas/): review the narrow `AGENTS.md` amendment, startup directory and one human-owned server. Do not remove all project constraints.
- Try Pick & polish on an observed issue. Save `workshop-feature` **after** the accepted Canvas instruction/UI changes, so the query session inherits them.

### Review and five-subagent checkout

- Invoke an actual independent critic for [rubber ducking](/workshops/copilot-app/rubber-duck/), not a main-agent reread. Any correction needs a normal feature branch before editing.
- In the same **Cart: boundary tests** session, create `workshop-checkout` from the checked result before implementing. Never code on the detached verification checkout.
- Approve the [checkout contract and file ownership](/workshops/copilot-app/subagents/#checkout-contract), then use `/fleet`: one orchestrator, five bounded implementation assignments, no extra worktrees or custom agent profiles.
- Give each worker its instructions and relevant code. Stage model/service/API dependencies; relay questions when direct messaging is unavailable. Record actual exchanges, not the chapter's example conversation.
- The orchestrator owns the integrated Maven run. Five assignments can run in smaller batches; do not start five shops, Maven suites or nested fleets.
- Check the original 12 tests, boundary cases and **new checkout tests**. Verify rollback, immutable receipts, concurrent duplicate requests and replay after new cart items. Restart the changed copy and place an order in the Browser canvas.
- After final review and scoped approval, the orchestrator delivers one checkout PR, handles checks/reviews and squash-merges when allowed. Workers never publish or merge. Verify exact merged main and restart the shop from that directory.

### Evidence and privacy

Confirm the `/chronicle` picker and its cost-tips spelling in your build:
App docs show `cost tips`; the CLI reference shows `cost-tips`.
History may span repositories or still be indexing. Never project unrelated
private work, invent missing usage figures or treat a later filter as undoing
earlier access.

Record App actions only when their actual responses are available.
Shop screenshots and saved HTTP captures do not prove an App interaction.
Run newcomer and experienced pilots, including navigation and recovery.

### Interrupted sessions

Read the actual partial handoff first: source directory/revision, unfinished
files, executed outcomes and owned helpers. Confirm cleanup before starting
another preview. A query error with no detailed cause is not proof of an
authentication failure. After a bounded retry following recovery, stop if the
same failure repeats; do not create a retry or replacement-agent loop.

If the participant approves a facilitator or single-agent takeover, record the
execution-method change. Preserve earlier failures and coverage gaps; delivered
code is not proof that the original independent or native App exercise completed.

</details>

## Check the delivery handoffs
{: #one-workshop}

Before checkout, the normal path has **three PRs targeting `main`**:

| Order | Required handoff |
|---|---|
| 1. Preparation PR | Merge the three accepted tickets, supplied tests and reviewed Canvas instruction/UI changes. Confirm updated `origin/main` before starting workers |
| 2. UI worker PR | Both workers start from that same updated `main`. Review UI repairs with Agent Merge's **Merge pull request** off; authorize this PR only, then confirm **Merged** and passing checks on `main` |
| 3. Boundary-test PR | Bring updated `main` into the test worker branch. Review its diff and fresh CI, then separately authorize its merge |

After both worker PRs merge, reuse **Cart: boundary tests** to verify exact
`origin/main` in its own clean worktree. Preserve worker branches and other
checkouts; squash-merged results count even when original commits are not ancestors.
No extra integration session is needed.

Continue in that session: **rubber duck → build and review checkout →
checkout PR merged into `main` → verify merged app → Chronicle → handoff**.
The orchestrator owns the single checkout PR under explicit delivery approval.
Confirm its linked PR is checkout, not the earlier boundary-test PR.
Use actual PR links rather than fixed numbers; a production-correction PR may
also exist. The template's `main` remains the unsolved starter, not a completed demo.

## Recovery
{: #recovery}

Preserve the participant's work first. Record what they actually completed;
a fallback or reference demonstration is not a successful native App exercise.

| Blocker | What to do |
|---|---|
| Setup or skill loading | Help or pair with a working participant. Compilation errors are not the expected regression failures |
| Quantity, removal or query fix | Use a separate pinned copy; see [reference recovery](#reference-recovery) below |
| Browser, Pick & polish or impeccable | Use the [Canvas fallback](/workshops/copilot-app/canvas/#canvas-recovery); record which interaction was unavailable |
| MCP connection or baseline | Use [matched reference evidence](/workshops/copilot-app/assets/mcp-evidence.json), clearly labelled as reference, not the participant's App tool calls |
| Preparation PR blocked | Follow [preparation recovery](/workshops/copilot-app/parallel/#local-recovery) only from an accepted local copy with all 12 supplied tests passing; record `main` as not updated |
| Worker, CI or Agent Merge blocked | Preserve both branches, disable Agent Merge on open PRs and follow [integration recovery](/workshops/copilot-app/integrate/#local-recovery) in **Cart: boundary tests** |
| Boundary test reveals a production bug | Keep the test worker test-only. Use the [separate correction path](/workshops/copilot-app/parallel/#boundary-fix), review its regression and rerun the worker tests before integration |
| Independent critic or five-agent delegation unavailable | Use the relevant chapter's demonstration/review fallback; explicitly record the missing independent critique or five-agent run |
| Checkout coding or tests fail | Keep the checkout branch, mark it unfinished and retain the earlier reviewed result; no checkout reference solution is supplied |
| Checkout publishing or merge blocked | Preserve branch/open PR; mark **verified locally; delivery blocked**. No direct push or substitute local merge into `main` |
| Checkout merged but checks or preview fail | Record **merged; post-merge verification blocked**. Repairs need a new approved feature branch and PR |
| Session query error or interruption | Preserve source, branches and partial evidence; an idle session is not completion. Resume only missing work, not the entire rehearsal |
| Chronicle unavailable or privacy opt-out | Review the workshop transcript without analyzing broader history; mark usage figures unavailable |

**CI:** queued/running means wait; absent, skipped or failed is not a pass.
Check Actions and the current PR revision. Keep the second PR's Agent Merge
off until the UI merge is verified. Never bypass policies, required approvals
or failing checks.

**Local recovery:** remote status may be unknown. Keep the checked recovered
result for preview and handoff; do not switch back to incomplete remote `main`
or report local integration as Agent Merge completion.

<details markdown="1" id="reference-recovery">
<summary>Reference checkpoints and safe Git recovery</summary>

### Expected reference results
{: #executable-checkpoints}

The [pinned revisions](/workshops/copilot-app/assets/references.json) and
[recorded checks](/workshops/copilot-app/assets/checkpoint-checks.json)
cover the three earlier tickets, **not checkout**.
These historical pins also predate current-starter input and keyboard hardening;
their counts and captures describe those exact revisions, not today's `main`.

| Check | Tests | Expected result |
|---|---:|---|
| Start, `BaselineTest` | 4 | Pass; repeated addition is not covered |
| Start, activate `CartContractTest` | 3 | Two failures: quantity 2 vs 1, total €50 vs €20 |
| After bug fix, baseline + cart | 7 | Pass |
| After bug fix, activate `RemoveContractTest` | 3 | Two failures: expected 200, actual 404 |
| After feature, baseline + cart + removal | 10 | Pass |
| After feature, activate `QueryContractTest` | 2 | Two failures: 9/17 SELECTs, expected 1 |
| After performance, all four classes | 12 | Pass |

Future acceptance classes live in `teaching/` until activated in the test
source directory. Review and commit them before implementation; keep their
assertions unchanged. Boundary and checkout tests add cases beyond these 12.

### Recover without losing work
{: #recover-without-losing-work}

Use a **new directory**, never the participant's project. This quantity-fix
example checks out the full pinned commit, not a movable tag:

```sh
git clone --no-checkout https://github.com/jdubois/copilot-shopping-cart-workshop.git cart-reference-bugfix
cd cart-reference-bugfix
git switch -c reference-work 8291261524b5e20ce86c111abe909877d8510776
git rev-parse HEAD
```

Confirm the printed SHA matches. For another checkpoint, use its full SHA
below and a fresh directory name. If the commit is unavailable, stop.

1. Connect a new App session to the reference copy. Check its directory and starting commit; activate any required teaching tests there and run the matching checks.
2. For quantity-fix recovery, create `git branch workshop-quantity HEAD` before the removal session. For feature recovery, complete Canvas before saving `workshop-feature`.
3. For performance recovery, restore the accepted Canvas instruction/UI changes, checking startup paths for this copy, and activate all three teaching classes unchanged. Confirm all 12 supplied tests pass before parallel work.
4. To resume GitHub delivery, apply the reviewed reference changes and any accepted Canvas work in a new worktree based on the participant's **own `main`**. Review the complete diff and rerun tests before the preparation PR. If GitHub is blocked, use the linked local recovery instead.

**Do not push this clone:** its `origin` is the template, not the personal
repository. Template-created repositories have independent history; changing
the remote alone does not make reference commits mergeable. Never merge
unrelated histories, overwrite personal `main` or replace an existing handoff
branch.

Stop the old shop in its owning terminal before starting the reference copy.
Record that a reference solution was used. Reference copies do not include
the participant's Canvas changes, new boundary tests or checkout.

| Git checkpoint | Reference | Pinned commit |
|---|---|---|
| `v2-start` | <a href="https://github.com/jdubois/copilot-shopping-cart-workshop/tree/v2-start" target="_blank">Starter</a> | `326f95840e3d42dcbb83d1bb182091cdda38382e` |
| `v2-bugfix` | <a href="https://github.com/jdubois/copilot-shopping-cart-workshop/tree/v2-bugfix" target="_blank">Quantity fix</a> | `8291261524b5e20ce86c111abe909877d8510776` |
| `v2-feature` | <a href="https://github.com/jdubois/copilot-shopping-cart-workshop/tree/v2-feature" target="_blank">Removal feature</a> | `f1b8d4104a3415c5568ea4f7fb15e1294aa3ad3f` |
| `v2-performance` | <a href="https://github.com/jdubois/copilot-shopping-cart-workshop/tree/v2-performance" target="_blank">Query fix</a> | `0a7d9dd3962929c7909ecfee64f72b2f03f43970` |

These are one reference history in the template repository, not separate
downloads or website source copies. Earlier v1 checkpoints remain unchanged.

</details>

## Evidence and maintenance

Use participants' actual test reports, previews and App responses.
The published reference checks do not prove their generated checkout works.

<details markdown="1">
<summary>Capture provenance and maintainer commands</summary>

The [capture manifest](/workshops/copilot-app/assets/capture-manifest.json)
pins source revisions, image/response hashes, runtime identities and the
capture JVM version, which differs from the Java 21 compilation target.
[Saved MCP responses](/workshops/copilot-app/assets/mcp-evidence.json)
were captured using HTTP JSON-RPC, **not through the App**.

Canonical code, skills and test CI live in
<a href="https://github.com/jdubois/copilot-shopping-cart-workshop" target="_blank">the template repository</a>;
its maintainer gate is `python3 tools/verify-checkpoints.py`.
For this website's handbook and reference captures:

```sh
CAPTURE_CHANNEL=chrome python3 tools/copilot-workshop/capture-all.py --port 18767
rbenv exec bundle exec jekyll build --destination tools/copilot-workshop/.build/site
python3 -m unittest discover -s tools/copilot-workshop -p 'test_*.py'
python3 tools/copilot-workshop/check-site.py --remote
```

The local gate checks matched request IDs/runtime identities, eight distinct
products, €115 totals and the 9-to-1 SELECT change. `--remote` also checks live
annotated tags against the pins; local success does not establish remote state
or a successful website workflow. Checkpoint tags are protected against updates
and deletion.

</details>
