---
layout: default
title: Prepare your workshop
description: "Open the project in Copilot App, check the starter tests and run the shop."
permalink: /workshops/copilot-app/setup/
workshop: true
next: ticket
next_title: Reproduce the cart bug
---

## Open your own shop

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

Open the **model picker below the prompt box** and select **Fusion Standard**.

**Copilot Fusion** automatically chooses which AI model to use for each task,
rather than asking you to pick one yourself. **Standard** balances quality,
response time and cost. At higher effort levels, Fusion can have one model
draft a solution and other models review it before returning a single response.
You still review the code and run the tests yourself. See
<a href="https://docs.github.com/en/copilot/concepts/models/copilot-fusion" target="_blank">how Fusion works</a>.

If Fusion is not available, choose a strong coding model from the same picker,
such as **Claude Sonnet 5.5** or **GPT-6.1 Sol**. Turn **Copilot Fusion** off if
the switch is shown. Available models depend on your plan and organization
settings. You can complete every exercise with a single model.

Review `AGENTS.md`, `.github/skills/` and `.github/mcp.json` before trusting
repository configuration.
You need JDK 21+, Git and a supported App account. No Docker or Node installation.

The three skills are **already installed** in `.github/skills/`.
The [skills chapter](/workshops/copilot-app/skills/) explains how to load them
and install them in another project.

The [integration exercise](/workshops/copilot-app/integrate/) uses **Agent Merge**
with two PRs in your own repository. Enable **GitHub Actions** and confirm you
can push branches, create PRs and merge them under your repository's rules.
Check that your organization allows Agent Merge and that any required
reviewer can approve your PRs. A policy denial or unavailable required
approval is a blocker, not a reason to broaden permissions.
The template includes the **Shopping-cart checks** workflow. Never weaken
organization policies or branch protections for the workshop; ask the
facilitator for help or use the integration chapter's local recovery steps
if GitHub, CI or Agent Merge is unavailable.

Let Copilot check the checkout and preserve your starting point:

```copilot
Confirm this session uses my own cart-workshop repository.
Check the source directory, branch, remote and uncommitted changes.
Before any edits, create an annotated tag workshop-start at the current commit.
Never replace an existing tag; if this is not a clean new starter, ask me first.
Report the source directory, branch and saved starting point. Do not edit files.
```

The tag gives Copilot a stable base for the final review. You do not need to
type Git commands or record commit IDs. If Git asks for a name and email, ask
Copilot to help configure **your own** identity.

In this session's working directory, run the baseline check, or ask Copilot to
run it:

```sh
java -version
./mvnw -q -Dtest=BaselineTest test
```

Expect **4 tests, 0 failures, 0 errors, 0 skipped**. This checks the starter
and downloads any missing Maven dependencies. It does not yet test adding the
same product twice.

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

When you move to a new session, start from your reviewed code, not a fresh
copy of the starter:

1. Review the changes in the App, then ask Copilot to commit only the changes you approve.
2. When a chapter asks for it, have Copilot create a named branch, such as `workshop-quantity`. This saves a starting point for the next session. Do not overwrite an existing branch with the same name.
3. Create the next session with **New worktree** and select that branch as its base. Before editing, ask Copilot to confirm that it starts from the saved commit and has no uncommitted changes.

The **branch name** selects the code to start from; the **session title** is
just a label. If the branch is not available in the picker, continue in the
current session rather than starting from the default branch.

Run Maven commands **in the active session's working directory**. Ask Copilot
to confirm the path if you are unsure.

The shop belongs to a particular terminal and source copy. Before running a new
copy, use **Ctrl+C in the terminal that owns the old shop**, then start the
reviewed copy using the startup command above. If you cannot identify the owner,
ask the facilitator; never stop an unknown process to free port 18765.

## Connect runtime tools

<a href="https://www.julien-dubois.com/boot-ui/" target="_blank">BootUI</a>
helps AI coding agents inspect running Java applications. It is preinstalled so
Copilot can diagnose the shop's N+1 query problem through
[MCP](/workshops/copilot-app/tools/), using these tools:

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
