---
layout: default
title: Canvas and Pick & polish
description: "Open the running shop in a shared Browser canvas and target one UI improvement."
permalink: /workshops/copilot-app/canvas/
workshop: true
next: tools
next_title: Investigate runtime with MCP
---

## What you will learn

Use a shared Browser canvas in Copilot App and invoke **`/impeccable`**
with Pick & polish to improve one visible interaction.

## What is a Canvas?

A **Canvas** is an interactive work surface beside the conversation.
You and Copilot can inspect and interact with the same artifact: a web page,
terminal, document or another supported surface.
Here, use the **Browser canvas** to see your running shop and point to a UI
issue without having to describe its location from memory.

The canvas is not the server. It displays a URL; opening it does not build or
start Spring Boot. You do not need to create a canvas extension for this exercise.
See the <a href="https://docs.github.com/en/copilot/how-tos/github-copilot-app/working-with-canvas-extensions" target="_blank">Canvas guide</a>.

<figure>
  <a href="/workshops/copilot-app/assets/illustration-canvas-focus.svg" target="_blank"><img src="/workshops/copilot-app/assets/illustration-canvas-focus.svg" alt="Conceptual Canvas interaction, not App UI: select the cart's Remove button, inspect an observed issue, approve a bounded correction, then check keyboard and narrow-screen usability while preserving behavior." width="1440" height="800" loading="lazy"></a>
  <figcaption>Point to one interaction and keep the correction focused. This schematic is not an App screenshot or evidence of a defect.</figcaption>
</figure>

## Open the running shop
{: #browser-preview}

Stay in **the same workshop session, on its current branch**, with the accepted
quantity fix and removal feature. Use **Interactive**. Reuse the human-owned
server already running from this session's directory. If needed, use the
[startup guidance](/workshops/copilot-app/setup/#start-the-application).
Keep its terminal open. Give Copilot this prompt in the **same session**:

```copilot
Confirm which source directory owns the running shop.
Check that http://127.0.0.1:18765 responds, then open that URL in the
Browser canvas beside this conversation. Do not start a second server,
create a canvas extension or change files.
```

Confirm the shop appears in the App's side panel. Add products, remove one,
then reload; you are using the application, not a screenshot.

## Pick one interaction to improve
{: #pick-and-polish}

Use the Browser canvas's **Pick & polish** control to select the **Remove**
button on a cart line. In the feedback associated with that selection,
invoke **`/impeccable`** with a specific styling request that reuses the shop's
existing theme:

```copilot
/impeccable
Make this Remove button more compact and use the existing secondary theme color,
not Add to cart's primary styling. Keep its label, accessibility and whole-line
DELETE behavior, with visible keyboard focus and a usable click/tap target.
Only change src/main/resources/static/. No backend, dependencies or test changes.
Propose the change and wait for my approval.
After approval, apply it and run ./mvnw compile in this session's directory.
Reload this existing Browser canvas and verify the result. Keep the shop running;
report compilation or refresh failures. If it already meets these criteria,
say no change is needed.
```

Approve the change, then review **Changes** and let Copilot
**reload the same Browser canvas automatically**.

Compare **Remove** with **Add to cart**: Remove should be compact and secondary,
while Add to cart stays primary. Keep the label unchanged and check keyboard focus
remains fully visible, including in a scrolling cart, at desktop and narrow widths.
Confirm removal still deletes the whole product line, including all its units,
while other products, quantities and totals remain correct. Run:

```sh
./mvnw -Dtest=BaselineTest,CartContractTest,RemoveContractTest test
```

All tests must pass without weakening assertions. Record the before/after result
on the [worksheet](/workshops/copilot-app/worksheet/).

<details markdown="1" id="canvas-recovery">
<summary>If the canvas, picker or skill is unavailable</summary>

Check the shop URL first. If Browser or Pick & polish is unavailable, use your
normal browser and send a screenshot or specific observation.
If `/impeccable` is unavailable, use explicit UI criteria instead.
Record the fallback; do not claim a tool or skill ran when it did not.

</details>

## Save your progress

After reviewing and verifying any UI changes, ask Copilot:

```copilot
Commit only the reviewed UI changes, if any and not yet committed.
Confirm the working tree is clean and the saved result includes the
quantity fix, removal feature and accepted Canvas changes.
Keep this session and its current branch; do not create or switch branches.
```

Continue to [Investigate runtime with MCP](/workshops/copilot-app/tools/) in
**this same session, on the same branch**.

## What you have learned

- Distinguish the running server from the Browser canvas that displays it.
- Invoke **`/impeccable`** with Pick & polish; have Copilot refresh the same canvas after approved edits, then verify behavior.
- Commit any accepted UI changes before continuing in the same session.
