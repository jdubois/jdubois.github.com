---
layout: default
title: Facilitate and recover
description: "Help participants use Copilot App and distinguish their own results from reference examples."
permalink: /workshops/copilot-app/facilitator/
workshop: true
---

## What this workshop teaches

Copilot App is the subject; the shopping cart is the example application.
Participants review a plan, load skills, generate and debug code, inspect diffs
and inspect their usage with Chronicle. BootUI is only the MCP server behind the
N+1 exercise. Do not turn the session into a dashboard tour.

## Rehearse with the App

Before presenting the workshop, rehearse with the App version and accounts you
will use:
project/worktree creation, base selection, Plan/Interactive/Autopilot controls,
Fusion availability, visible skill invocation, tool trust and MCP tool calls.
Rehearse publishing `workshop-complete` to the participant's own repository,
creating both worker PRs against it, and using Agent Merge sequentially with
repairs first and **Merge pull request** off until the learner has reviewed
the result. Confirm GitHub Actions is enabled, the template's
**Shopping-cart checks / tests** job runs on this non-default PR target, and
the participant can merge under the repository's rules. Do not weaken rules
to make the exercise proceed.
Use one named **Cart: integration** session for combined checks. Rehearse
fetching the latest remote integration branch and fast-forwarding that
session's branch without touching another worktree. Include squash merges:
the PR's merged result, not worker-commit ancestry alone, identifies what landed.
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
Every participant proceeds through the cart bug, removal, MCP investigation,
parallel sessions, integration, Chronicle, and final handoff.
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
| Feature blocked | Preserve work; use after-feature to continue with the MCP investigation |
| MCP baseline unavailable | Use matched reference evidence and ask for help connecting |
| Optimization blocked | Inspect after-performance before preparing parallel work |
| Worker unfinished | Keep its branch; integrate only accepted results |
| Integration unfinished | Preserve the state and record missing evidence |
| Chronicle unavailable/indexing | Review the workshop transcript; record that usage analysis was unavailable |
| Work remains at handoff | Record limitations; do not claim complete delivery |
| GitHub, CI or Agent Merge unavailable | Use the integration chapter's local recovery; record Agent Merge as not completed |
| Integration tests fail or CI is pending | Keep the second PR's Agent Merge off; record unfinished work and do not force a merge or skip checks |

Distinguish queued/running CI from absent or failed runs. If no **tests** job
appears, check Actions is enabled and arrange checks for the current PR revision.
A policy denial or missing required approver is a blocker; repeated prompts
or broader permissions are not a remedy.

The main integration path uses two worker PRs targeting `workshop-complete`,
not the starter on `main`. Merge the UI PR, check its combined result, then
update and merge the test PR. Review any agent-authored corrections and verify
the final checkout includes both merged contributions. The workshop finishes
on the integration branch; no third PR is required. If recovery is needed
after a partial merge, disable Agent Merge on open PRs and preserve both
remote and local work before continuing locally.

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
removal session. For feature recovery, create `git branch workshop-feature HEAD`
before the query session. These are local handoff branches, not permission to
push to the template.
Its `origin` points to the template, **not your personal repository**: do not
push to it. To continue with personal GitHub delivery, configure your own remote
deliberately after checking the participant's repository URL.
For after-performance recovery, activate all three teaching test classes
unchanged and confirm all 12 supplied tests pass before starting parallel work.
Then follow the parallel chapter to create `workshop-complete` and both worker
sessions from this accepted reference-based version. Never overwrite the
participant's `main` or an existing handoff branch to connect the recovered work.
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
