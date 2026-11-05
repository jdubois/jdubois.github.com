---
layout: default
title: Use a skill and add a regression test
description: "Load relevant Java guidance and add a regression test before changing the implementation."
permalink: /workshops/copilot-app/skills/
workshop: true
next: verify
next_title: Fix, review and verify
---

## What you will learn

Load a relevant skill in Copilot App and use it to establish a failing regression
test before implementation.

## Skills are already installed

**No installation is needed for this workshop.** Your repository created from
the template already includes complete, pinned skills in `.github/skills/`.

| Skill | When it helps |
|---|---|
| `java-junit` | Reproduce the cart bug and review assertions |
| `spring-boot-testing` | Generate and review HTTP tests for item removal |
| `java-hibernate-jpa` | Diagnose the N+1 query during the MCP exercise |

<details markdown="1">
<summary>Install these skills in another project</summary>

Follow the
<a href="https://github.com/github/awesome-copilot/blob/main/docs/README.skills.md#how-to-use-agent-skills" target="_blank">official Awesome Copilot instructions</a>.
With **GitHub CLI 2.90.0+**, from your other project's root:

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

## Load the skill, not just its name

Ask Copilot to **use `java-junit`** to identify the assertions for the repeated-add
regression, without editing. Check which skill files it reads and ask it to
identify one rule that applies to this test.

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

- Ask Copilot to use a specific installed skill and explain how its guidance applies to the current task.
- Keep the workshop's stack and dependency limits even when a general-purpose skill suggests other tools.
- Review a supplied test in **Changes**, commit it before implementation and distinguish an expected assertion failure from a setup problem.
