---
layout: default
title: Set up your App workspace
description: "Open the project in Copilot App, check the starter tests and run the shop."
permalink: /workshops/copilot-app/setup/
workshop: true
next: ticket
next_title: Investigate with Copilot
---

## Open your own shop

You need JDK 21+, Git and a supported Copilot App account. No Docker or Node
installation is needed.

Open the
<a href="https://github.com/jdubois/copilot-shopping-cart-workshop" target="_blank">shopping-cart template repository</a>
and choose **Use this template → Create a new repository**. Choose your account
as owner and a name such as **cart-workshop**; private or public both work.
Leave **Include all branches** unchecked so your repository contains only the
starting code, without the solutions.

## Open it in Copilot App

In the App sidebar, click **+** next to **Sessions**, then choose
**Add GitHub repository**. Select **your new `cart-workshop` repository**;
the App clones it for you. Do not select the template owner's repository.

If a private repository is not available in the picker, use the App's
**Clone repository** option with its Git URL and your configured credentials.
Do not paste credentials into prompts. See the
<a href="https://docs.github.com/en/copilot/get-started/quickstart-copilot-app#connecting-a-repository-or-folder" target="_blank">App's repository connection guide</a>.

Start a session in this repository. Choose **This computer**, **New worktree**
and **Interactive**, and name the session **Cart: quantity bug**.

In the **model picker below the prompt box**, select **Fusion Standard**,
which automatically chooses a model for each task. If unavailable, choose
**Claude Sonnet 5.5** or **GPT-6.1 Sol** and turn **Copilot Fusion** off if the
switch is shown. Available models depend on your plan and organization settings.
See <a href="https://docs.github.com/en/copilot/concepts/models/copilot-fusion" target="_blank">how Fusion works</a>.

Review `AGENTS.md`, `.github/skills/` and `.github/mcp.json` before trusting
repository configuration. The three Java skills are already installed; no
installation is needed. Their [chapter](/workshops/copilot-app/skills/) covers usage.

If a file read is denied, stop and review the App's repository-trust or
file-access request. MCP approval does not grant filesystem access.
Do not bypass a denial or broaden permissions.

Enable **GitHub Actions** for the included **Shopping-cart checks** workflow.
Confirm you can push branches, create PRs and merge them, obtain required reviews
and use **Agent Merge** under your repository's rules. Never weaken policies
or branch protections. If access or required approval is unavailable, ask the
facilitator; the [parallel](/workshops/copilot-app/parallel/) and
[integration](/workshops/copilot-app/integrate/) chapters provide local recovery.

## Check the starter

Let Copilot check the checkout and preserve your starting point:

```copilot
Confirm this session uses my own cart-workshop repository.
Check the source directory, branch, remote and uncommitted changes.
Before any edits, create an annotated tag workshop-start at the current commit.
Never replace an existing tag; if this is not a clean new starter, ask me first.
Report the source directory, branch and saved starting point. Do not edit files.
```

The tag saves your starting point for the final review; Copilot handles the Git
bookkeeping. If Git asks for a name and email, ask Copilot to help configure
**your own** identity.

In this session's working directory, run the baseline check, or ask Copilot to
run it:

```sh
java -version
./mvnw -q -Dtest=BaselineTest test
```

Expect **4 tests, 0 failures, 0 errors, 0 skipped**. Maven downloads missing
dependencies. These tests do not yet cover adding the same product twice.
If `-q` hides the summary, ask Copilot for the exit status and executed counts
from `target/surefire-reports/`. Silence is not a pass.

## Start one application

Run this in the **active session's working directory**:

```sh
./mvnw spring-boot:run
```

Keep that terminal open. Open
<a href="http://127.0.0.1:18765" target="_blank">the shop</a>.
Ctrl+C in that terminal stops the app. A restart resets data.

Tests have random ports and isolated H2 databases. Never run two persistent
servers on port 18765 or stop processes by name.

## Work in the right session

Find the composer, mode/model controls and **Changes** view.
Your worktree is a separate copy: run and preview the code from this session,
not the repository's original checkout.

### Session handoffs
{: #session-handoffs}

When a chapter asks for a new session, carry forward your reviewed code:

1. Review the changes in the App, then ask Copilot to commit only the changes you approve.
2. Ask Copilot to create the branch named in that chapter, such as `workshop-quantity`. Do not overwrite an existing branch.
3. Create the next session with **New worktree** and select that branch as its base. Before editing, ask Copilot to confirm that it starts from the saved commit and has no uncommitted changes.

The **branch name** selects the starting code; the **session title** is just a
label. If the branch is missing from the picker, continue in the current
session rather than starting from the default branch. Run Maven commands in
the active session's working directory; ask Copilot to confirm the path if unsure.

The shop belongs to a particular terminal and source copy. Before running a new
copy, use **Ctrl+C in the terminal that owns the old shop**, then start the
reviewed copy using the startup command above. If you cannot identify the owner,
ask the facilitator; never stop an unknown process to free port 18765.

## Connect runtime tools

<a href="https://www.julien-dubois.com/boot-ui/" target="_blank">BootUI</a>
is preinstalled. Connect it through [MCP](/workshops/copilot-app/tools/) so
Copilot can inspect the running shop:

```json
{
  "mcpServers": {
    "shopping-cart": {
      "type": "http",
      "url": "http://127.0.0.1:18765/bootui/api/mcp",
      "tools": ["get_live_activity", "get_request_profile"]
    }
  }
}
```

Use **Customize → MCP** to review and trust the repository's MCP configuration,
then reload it if prompted. If the endpoint is missing, add it there.
No VS Code configuration, public tunnel or extra MCP server is needed.

## Ready check

The shop opens, baseline tests pass, you can reproduce the two-click bug, and
you know the active project/session. Type **`/chronicle` in the App composer**
to check that its picker is available; do not run a history analysis yet.
With your shop running, ask Copilot to call **`get_live_activity`** with
`query: "/api/cart"` and `limit: 1`. A tool response, even an empty list, confirms
the connection works. If it fails, check trust and reload settings before
continuing. If MCP remains unavailable, ask the facilitator to demonstrate
the exercise using the reference results.

<details markdown="1">
<summary>Windows and version details</summary>

Use `.\mvnw.cmd` instead of `./mvnw`.
In Windows PowerShell, use **`curl.exe`**, not its `curl` alias; the `-fsS`
workshop commands require the curl executable.
Spring Boot **4.1.2**, BootUI **2.3.0**, Java release **21**, Maven **3.9.9**.
Skills are pinned to Awesome Copilot revision
`7e408815ddcb64889a3683799a85399331cfd4ef`, with license and hashes.
The template's `main` keeps the starter behavior of the `v2-start` edition. See the
[reference revisions](/workshops/copilot-app/assets/references.json).
Creating from a template starts independent history; your initial commit SHA
will differ from the template's, and its solution tags are not copied.
</details>
