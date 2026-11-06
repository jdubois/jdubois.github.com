---
layout: default
title: Facilitate and recover
description: "Help participants use Copilot App and distinguish their own results from reference examples."
permalink: /workshops/copilot-app/facilitator/
workshop: true
---

## What this workshop teaches

Copilot App is the subject; the shopping cart is the example application.
Participants plan, load skills, generate and debug code, and use a shared
Canvas with **impeccable** to improve the UI. They investigate with MCP,
coordinate isolated worktree sessions and integrate reviewed PRs with Agent Merge.
Then they request an independent rubber duck critique, coordinate five
subagents to implement mock checkout and inspect their usage with Chronicle.
BootUI is only the MCP server behind the N+1 exercise, not a dashboard tour.

Keep the three kinds of collaboration distinct: **Canvas** grounds UI feedback
in a shared surface; **rubber duck** challenges an existing solution;
**subagents** coordinate dependent implementations of one checkout feature.
The first three tickets and reviewed UI/test improvements precede a fourth
ticket: working mock checkout, with no payments or authentication.

## Rehearse with the App

Before presenting the workshop, rehearse with the App version and accounts you
will use:
project/worktree creation, base selection, Plan/Interactive/Autopilot controls,
Fusion availability, visible skill invocation, tool trust and MCP tool calls.
Show the difference between an installed skill and guidance loaded for a task.
Use the visible installation section for other projects; do not require
participants to reinstall or replace the workshop's pinned skill copies.
Rehearse the Browser canvas, **Pick & polish** and bundled **impeccable**
with a real, observed UI issue. Confirm the reviewed `AGENTS.md` startup note
matches the active directory and one human-owned server. The starter excludes
agents and checkout: rehearse the Canvas chapter's narrow instruction update,
not a blanket removal of project constraints. Save `workshop-feature` after
that chapter so the query session inherits the accepted UI and instruction changes.
Rehearse merging the three accepted tickets into the participant's **`main`**
through one reviewed preparation PR before starting the workers.
Create both worker sessions from that updated `main`, then rehearse their PRs
targeting `main` and using Agent Merge sequentially with
repairs first and **Merge pull request** off until the learner has reviewed
the result. Confirm GitHub Actions is enabled, the template's
**Shopping-cart checks / tests** job runs on all three PRs, and
the participant can merge under the repository's rules. Do not weaken rules
to make the exercise proceed.
Do not create a third session for verification. After both PRs merge, reuse
**Cart: boundary tests** to fetch and check out the exact `origin/main` commit
in its own clean worktree, preserving its worker branch. Copilot can use a
detached checkout for verification; it must not move a `main` branch that is
checked out elsewhere or alter another worktree. Include squash merges:
the PR's merged result, not worker-commit ancestry alone, identifies what landed.
Any subsequent code correction needs a reviewed feature branch, not a commit
on this verification checkout.
Rehearse **`/rubber-duck`** on the full combined result and record an actual
critic invocation rather than a main-agent reread.
Then rehearse creating **`workshop-checkout`** from the checked result in this
same worktree, without moving `main` or earlier worker refs. This normal
feature branch is required before any checkout edits; do not implement on
the detached verification checkout.
Use **`/fleet`** after approving the contract and exact file ownership:
one existing-session orchestrator and five implementation subagents, with no
additional worktree sessions or agent-profile authoring.
Check each agent receives the constraints and relevant code; do not assume
custom subagents inherit repository instructions or the main conversation.
Verify actual questions/answers about snapshots, cart clearing and retries.
Stage model/service/API dependencies; let UI and HTTP tests use the agreed
contract. The orchestrator owns the one integrated Maven run, not five workers.
Check **CheckoutContractTest** adds cases alongside the original 12 and
boundary tests, including transaction rollback, immutable snapshots,
concurrent duplicate requests and replay after new items enter the cart.
Restart the changed copy and rehearse placing an order in the Browser canvas.
The receipt must show the server's quantities/totals and the cart must clear.
Where direct messaging is unavailable, the orchestrator must relay the exchange
or record the limitation, not fabricate a conversation.
Five assignments may run in smaller batches if machine load or permissions
limit concurrency. Do not run five shops, Maven suites or nested fleets.
Confirm the `/chronicle` picker and its cost-tips spelling in that build.
App docs show `cost tips`; the CLI reference shows `cost-tips`.

If Fusion is unavailable, help participants choose a strong coding model using
the alternatives in [setup](/workshops/copilot-app/setup/#open-it-in-copilot-app).

Use only opt-in workshop sessions for a Chronicle demonstration. History can
span repositories and may be incomplete while sessions are still indexing.
Make the privacy choice **before** selecting cost tips; a follow-up filter
does not undo earlier history access. Offer local transcript review instead
without penalizing participants who opt out.
Do not project private work or estimate missing usage figures. Record an App
tool call as completed only when you have its response. Capture App screenshots
during an authorized rehearsal; shop screenshots and direct HTTP captures do
not demonstrate an App interaction.

Run newcomer and experienced pilots. Check setup, navigation and recovery.
Help participants work through each exercise without completion deadlines.

## One workshop

Use the [workshop flow](/workshops/copilot-app/#workshop-flow), with a break
before the parallel work. Help participants prepare their environment first.
Every participant proceeds through the cart bug, removal, Canvas, MCP investigation,
parallel sessions, integration, rubber ducking, mock-checkout implementation with
subagents, Chronicle, and final handoff.
Do not introduce a separate demonstration-only or extended path, or assign
chapter deadlines. Participants who get stuck can work with a partner or
continue from a reference checkpoint.

## Executable checkpoints

The [reference revisions](/workshops/copilot-app/assets/references.json) pin the
template's four Git checkpoints. The
[test results](/workshops/copilot-app/assets/checkpoint-checks.json)
record the reference checks:

| Check | Tests | Expected result |
|---|---:|---|
| Start, `BaselineTest` | 4 | Pass; repeated addition is not covered |
| Start, activate `CartContractTest` | 3 | Two failures: quantity 2 vs 1, total 5000 vs 2000 |
| After bug fix, baseline + cart | 7 | Pass |
| After bug fix, activate `RemoveContractTest` | 3 | Two failures: expected 200, actual 404 |
| After feature, baseline + cart + removal | 10 | Pass |
| After feature, activate `QueryContractTest` | 2 | Two failures: 9/17 SELECTs, expected 1 |
| After performance, all four classes | 12 | Pass |

Future acceptance tests live in `teaching/` and are intentionally not discovered
by Maven until copied. Review and commit these tests before implementation so
their expected results are clear and their assertions remain unchanged.

## Recovery
{: #recovery}

| If blocked | Recovery |
|---|---|
| Setup fails | Work with a partner or ask for help; compilation errors are not the expected test failures |
| Skill/test setup blocked | Use a working partner's setup or the facilitator's example; note which steps the participant ran |
| Bug fix blocked | Preserve the branch; use a separate after-bugfix copy |
| Feature blocked | Preserve work; use after-feature to continue with the Canvas exercise |
| Browser, Pick & polish or impeccable unavailable | Use the Canvas chapter's browser/observation fallback and record what actually ran |
| Rubber duck or independent critic unavailable | Use a demonstration or ordinary review, explicitly marking the missing independent critique |
| Five-subagent delegation unavailable | Demonstrate or explicitly approve one-agent implementation; record that five-agent delegation was not completed |
| Checkout coding or tests fail | Preserve the feature branch; record checkout as unfinished and retain the earlier reviewed result |
| MCP baseline unavailable | Use matched reference evidence and ask for help connecting |
| Optimization blocked | Inspect after-performance before preparing parallel work |
| Worker unfinished | Keep its branch; integrate only accepted results |
| Integration unfinished | Preserve the state and record missing evidence |
| Chronicle unavailable/indexing | Review the workshop transcript; record that usage analysis was unavailable |
| Work remains at handoff | Record limitations; do not claim complete delivery |
| Preparation PR blocked by GitHub, CI or approvals | Use the parallel chapter's local recovery only if the accepted local copy passes all 12 tests; record main as not updated |
| GitHub, CI or Agent Merge unavailable during integration | Use the integration chapter's local recovery; record Agent Merge as not completed |
| Integration tests fail or CI is pending | Keep the second PR's Agent Merge off; record unfinished work and do not force a merge or skip checks |

Distinguish queued/running CI from absent or failed runs. If no **tests** job
appears, check Actions is enabled and arrange checks for the current PR revision.
A policy denial or missing required approver is a blocker; repeated prompts
or broader permissions are not a remedy.

Before checkout, the workflow uses **three PRs targeting `main`**: one for the three
completed tickets before parallel work, then the UI and boundary-test PRs.
Do not start workers from starter `main`; fetch and verify the preparation
PR's merged result first. Merge the UI PR, check its combined result, then
update and merge the test PR. Review any agent-authored corrections and verify
the final checkout includes both merged contributions. The later checkout feature
is committed on one new branch in the same session; it is not automatically
on `main`. A separate checkout PR is optional and needs its own review and
merge authorization. No extra integration session is needed.
If recovery is needed
after a partial merge, disable Agent Merge on open PRs and preserve both
remote and local work before continuing on **Cart: boundary tests**.
Merge available remote `main` into that worker branch, rather than trying
to fast-forward it over the worker's unmerged tests. If the preparation PR
never merged, retain the accepted local base instead of pulling in starter
`main`. Offline recovery can use reviewed local handoffs, but remote PR status
remains unknown. Keep the recovered checkout for preview and final review;
do not replace it with incomplete remote `main`.
The existing reference checkpoints stop before checkout. Do not present them
as checkout solutions or evidence that generated checkout tests passed.

### Recover without losing work

Clone the required checkpoint into a **new directory**, never over a participant's
project. Use the **full pinned commit** so recovery always uses the expected
version, even if a tag changes. For the quantity-fix reference:

```sh
git clone --no-checkout https://github.com/jdubois/copilot-shopping-cart-workshop.git cart-reference-bugfix
cd cart-reference-bugfix
git switch -c reference-work 8291261524b5e20ce86c111abe909877d8510776
git rev-parse HEAD
```

Git checks out exactly that commit or fails if it is unavailable; it cannot
silently substitute a moved tag. Confirm the printed SHA matches. For another
checkpoint, use its full SHA from the table below and a fresh directory name.
Run Maven checks and ask Copilot to add the required teaching tests in that new
clone, not the participant's old terminal. Connect a new App session to the
clone and check its directory and starting commit.
For quantity-fix recovery, create `git branch workshop-quantity HEAD` before the
removal session. For feature recovery, follow the Canvas chapter before creating
`workshop-feature`, so its handoff includes the reviewed instruction and UI
changes. These are local handoff branches, not permission to
push to the template.
Its `origin` points to the template, **not your personal repository**: do not
push to it. A template-created personal repository has independent history:
merely repointing this clone's remote does not make its commits mergeable
into the participant's `main`. To resume the normal GitHub workflow, apply
the reviewed reference changes to a new worktree based on the participant's
own `main`, review the complete diff and rerun the acceptance tests before
opening the preparation PR. Do not merge unrelated histories or overwrite
the participant's `main`.
For after-performance recovery, activate all three teaching test classes
unchanged and confirm all 12 supplied tests pass before starting parallel work.
Then follow the parallel chapter: merge the preparation PR before starting
workers from updated `main`, or use its explicit local recovery from the
accepted reference-based branch. Record which route was actually completed.
Never overwrite an existing handoff branch to connect the recovered work.
Stop the previous workshop app in its own terminal before starting
this reference. Record that the participant continued from a reference solution.

| Git checkpoint | Reference | Pinned commit |
|---|---|---|
| `v2-start` | <a href="https://github.com/jdubois/copilot-shopping-cart-workshop/tree/v2-start" target="_blank">Starter</a> | `326f95840e3d42dcbb83d1bb182091cdda38382e` |
| `v2-bugfix` | <a href="https://github.com/jdubois/copilot-shopping-cart-workshop/tree/v2-bugfix" target="_blank">Quantity fix</a> | `8291261524b5e20ce86c111abe909877d8510776` |
| `v2-feature` | <a href="https://github.com/jdubois/copilot-shopping-cart-workshop/tree/v2-feature" target="_blank">Removal feature</a> | `f1b8d4104a3415c5568ea4f7fb15e1294aa3ad3f` |
| `v2-performance` | <a href="https://github.com/jdubois/copilot-shopping-cart-workshop/tree/v2-performance" target="_blank">Query fix</a> | `0a7d9dd3962929c7909ecfee64f72b2f03f43970` |

These are commits in one reference history, maintained alongside the starter in
the template repository. There are no separate source downloads or website copies.
The earlier v1 checkpoints remain unchanged; v2 strengthens removal assertions.

## Evidence and maintenance

The shop screenshots were captured from these exact Git revisions.
The [saved MCP responses](/workshops/copilot-app/assets/mcp-evidence.json) were
captured using HTTP JSON-RPC, not through the App.
The [capture manifest](/workshops/copilot-app/assets/capture-manifest.json)
records source commits, image/MCP response hashes, runtime identities and the
actual capture JVM version, distinct from the Java 21 compilation target.
No BootUI browser screenshot is needed.

Canonical sample code, skill maintenance and test CI live only in
<a href="https://github.com/jdubois/copilot-shopping-cart-workshop" target="_blank">the template repository</a>.
Its maintainer command is `python3 tools/verify-checkpoints.py`.
This website keeps only the handbook, reference receipts and capture tooling:

```sh
CAPTURE_CHANNEL=chrome python3 tools/copilot-workshop/capture-all.py --port 18767
rbenv exec bundle exec jekyll build --destination tools/copilot-workshop/.build/site
python3 -m unittest discover -s tools/copilot-workshop -p 'test_*.py'
python3 tools/copilot-workshop/check-site.py --remote
```

The local gate checks matched request IDs, runtime identities, eight distinct
products, €115 totals and the 9-to-1 SELECT change. `--remote` additionally
compares live annotated tags with the published commit pins; a local-only run
does not establish remote state. GitHub protects checkpoint tags against updates
and deletion. The website workflow runs these gates when this change is published;
local success alone is not a remote workflow result.
