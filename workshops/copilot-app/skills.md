---
layout: default
title: Install and use skills
description: "Understand skill installation and loading, then use the bundled Java guidance to establish a failing regression test."
permalink: /workshops/copilot-app/skills/
workshop: true
next: verify
next_title: Review and verify changes
---

## What you will learn

Find and load a relevant skill in Copilot App, understand how to install it
in another project, and use its guidance to establish a failing regression
test before implementation.

## What is a skill?

A **skill** is a folder of reusable instructions and resources for a task,
such as writing Java tests. Its `SKILL.md` explains when and how to use it;
references or scripts may supply additional guidance.
Installation makes the skill available. Loading it brings the relevant
guidance into Copilot's current task. Neither grants new tool permissions.

## Find the installed skills
{: #skills-are-already-installed}

**No installation is needed for this workshop.** Your repository created from
the template already includes complete, pinned skills in `.github/skills/`.

| Skill | When it helps |
|---|---|
| `java-junit` | Reproduce the cart bug and review assertions |
| `spring-boot-testing` | Generate and review HTTP tests for item removal |
| `java-hibernate-jpa` | Diagnose the N+1 query during the MCP exercise |

The later Canvas exercise uses **impeccable**, bundled with the App.
These three Java skills are instead bundled with the **repository**.

## Install skills in another project
{: #install-skills}

For a project without these skills, inspect the source and complete skill
folder before installing it. Use the destination project's root, not this
workshop's checkout; keep its existing pinned copies unchanged.
Follow the
<a href="https://github.com/github/awesome-copilot/blob/main/docs/README.skills.md#how-to-use-agent-skills" target="_blank">official Awesome Copilot instructions</a>.
With **GitHub CLI 2.90.0+**, install into `.github/skills/` at repository scope
using the pinned commands below, or copy complete skill folders manually.

<details markdown="1">
<summary>Pinned installation commands for another project</summary>

```sh
gh skills install github/awesome-copilot java-junit --pin 7e408815ddcb64889a3683799a85399331cfd4ef --dir .github/skills
gh skills install github/awesome-copilot spring-boot-testing --pin 7e408815ddcb64889a3683799a85399331cfd4ef --dir .github/skills
gh skills install github/awesome-copilot java-hibernate-jpa --pin 7e408815ddcb64889a3683799a85399331cfd4ef --dir .github/skills
```

The source revision and destination match this workshop. The CLI adds its own
installation metadata, so installed files may have different hashes from the
bundled copies. You can also copy complete skill folders, including references.
Keep the workshop's existing copies unchanged.
</details>

Confirm the destination contains each `SKILL.md` and its bundled resources.
Then ask Copilot in that project's session to load the skill and identify
the guidance it actually read. If the skill is not discovered, check its
location and name before retrying; do not claim that installation alone ran it.
You can learn the installation process here without changing repositories
or reinstalling the workshop's skills.

## Load the skill, not just its name

Stay in **Cart: quantity bug**. Use the installed skill in the App composer:

```copilot
Use java-junit to review the repeated-add acceptance criteria.
Read .github/skills/java-junit/SKILL.md and any relevant bundled references.
Identify the assertions needed and explain one skill rule that applies.
Report which skill guidance you actually read. Do not edit or implement yet.
```

**App tip:** load the skill needed for the current task, not every installed skill
on every turn. General skill advice does not override this
workshop's **H2, no-Docker, no-new-dependency** boundary. If a skill recommends
Testcontainers or a different database, retain H2 and explain that constraint.

## Add the regression test

Ask the agent to propose a regression first. Then ask it to activate the
supplied acceptance test in the **active session**:

```copilot
Copy teaching/CartContractTest.java unchanged into
src/test/java/com/juliendubois/workshop/.
Do not implement the fix or change other files.
Show me the diff and wait for approval before committing.
```

Review **Changes**, then ask Copilot to commit only this acceptance test and run:

```sh
./mvnw -q -Dtest=CartContractTest test
```

PowerShell: use `.\mvnw.cmd`.
The `teaching/` directory holds tests for later exercises; Maven does not run
them until they are copied into the test source directory.
Copilot may add tests, but must keep the supplied assertions unchanged.

Expect **3 tests, 2 failures**: expected quantity 2, actual 1; expected total
5000 cents, actual 2000.
The maximum-quantity test passes. Check
`target/surefire-reports/com.juliendubois.workshop.CartContractTest.txt`.
These assertion failures are expected. Compilation errors, a missing JDK or
a run with no tests are setup problems to resolve.

If setup or skill loading is blocked, ask the facilitator for help. If you use
a reference example, note which steps you ran yourself.

## What you have learned

- Distinguish installed skills from loaded guidance, and install complete pinned folders in another project without replacing the workshop's copies.
- Ask Copilot to use a specific installed skill and explain how its guidance applies to the current task.
- Keep the workshop's stack and dependency limits even when a general-purpose skill suggests other tools.
- Review a supplied test in **Changes**, commit it before implementation and distinguish an expected assertion failure from a setup problem.
