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

Prepare a session in this repository. Choose **This computer**, **New worktree**
and **Interactive**.

In the **model picker below the prompt box**, select **Fusion Standard**,
which automatically chooses a model for each task. If unavailable, choose
**Claude Sonnet 5.5** or **GPT-6.1 Sol** and turn **Copilot Fusion** off if the
switch is shown. Available models depend on your plan and organization settings.
See <a href="https://docs.github.com/en/copilot/concepts/models/copilot-fusion" target="_blank">how Fusion works</a>.

Send this first prompt to start the session:

```copilot
Analyze this project's tech stack from its source and configuration files.
Briefly explain the backend, frontend, database and test tooling.
Do not edit files, install dependencies, start the application or call MCP tools.
```

Once the session has started, name the session **Cart: quantity bug**.
Use the **Open in...** menu at the **top right** to open the session's working
directory in your editor. There, review `AGENTS.md`, the skill instructions
under `.github/skills/` and `.github/mcp.json` before approving repository
configuration or using its skills and MCP tools. The three Java skills are
already installed; no installation is needed.
Their [chapter](/workshops/copilot-app/skills/) covers usage.

If a file read is denied, stop and review the App's repository-trust or
file-access request. MCP approval does not grant filesystem access.

Your own repository should be ready for **GitHub Actions**, PRs and
**Agent Merge** with the default settings. If you run into an access or
approval issue later, ask the facilitator.

## Understand AGENTS.md

`AGENTS.md` is a Markdown file containing project instructions for coding agents.
Copilot loads applicable instructions automatically, so you don't need to repeat
the project's commands and conventions in every prompt. It guides Copilot;
it does not run commands or grant tool permissions.

Open the root `AGENTS.md` in your editor. Find the commands to start the shop,
run the four baseline tests and run all currently activated tests. Notice the
project boundaries too: keep the existing stack, preserve acceptance tests
and let the human manage the running shop.

**For your own projects, a useful AGENTS.md should:**

- Give exact, working build, run and test commands, including required versions
  and any setup steps. Prefer the project's wrapper, such as `./mvnw`.
- Explain non-obvious conventions and constraints, such as HTTP tests using
  random ports and isolated databases.
- Stay short and current. Link to detailed documentation instead of copying
  it, and update commands when the workflow changes.

The template already provides these instructions; you don't need to edit them.
Next, use its baseline-test and startup commands.

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
./mvnw -Dtest=BaselineTest test
```

Expect **4 tests, 0 failures, 0 errors, 0 skipped**. Maven downloads missing
dependencies. These tests do not yet cover adding the same product twice.

## Start the application

Click the **terminal icon at the top right** to open a terminal in the
**current session's worktree**, then run:

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

Stay in **this session and on its current branch** for the quantity fix,
removal feature, Canvas and MCP exercises. You don't need a new session,
a named handoff branch or a switch to `main` between these steps.
Review each result and ask Copilot to commit only the accepted changes;
those commits are your checkpoints.

The [Parallel sessions](/workshops/copilot-app/parallel/) chapter introduces
separate worktrees when you have independent tasks to run together.
Until then, run Maven commands from this same session's working directory.

The shop belongs to a particular terminal and source copy. Before running a new
version after code changes, use **Ctrl+C in the terminal that owns the shop**, then start the
reviewed copy using the startup command above. If you cannot identify the owner,
ask the facilitator; never stop an unknown process to free port 18765.

## Ready check

The shop opens, baseline tests pass, you can reproduce the two-click bug, and
you know the active project/session.
MCP setup comes later, in [Investigate runtime with MCP](/workshops/copilot-app/tools/).

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
