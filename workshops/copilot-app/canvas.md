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
Style this Remove button as a filled button using the same visual treatment
as Add to cart. Reuse the existing button styles and theme tokens for colors,
typography, spacing, hover, focus and disabled states; do not introduce a new theme.
Keep its Remove label, accessible name, keyboard access and whole-line DELETE
behavior. Preserve visible focus and usability on a narrow screen.
Only change src/main/resources/static/. No backend, dependencies,
test changes or whole-page redesign. Explain the smallest proposed change
before editing; wait for my approval.
After applying an approved correction, run ./mvnw compile in this session's
directory, then reload this existing Browser canvas and verify the change.
Keep the shop running. Report compilation or refresh failures instead of
claiming the preview is updated.
If Remove already matches Add to cart and meets these requirements,
say no change is needed instead of inventing a defect.
```

**`/impeccable`** loads the bundled skill's UI design and accessibility guidance; the canvas
supplies the selected element and visual context. Neither is a test result
or permission to change the rest of the project.

Review the proposal and approve only the useful correction. Copilot should apply
it, compile the resources and **reload the same Browser canvas automatically**.
Inspect **Changes** and the updated preview; you do not need to run a separate
terminal command or click refresh.

`./mvnw compile` copies the changed UI resources; it does not force a server
restart. **DevTools** does not normally restart the app for static resources.
Check the refreshed result with keyboard navigation at narrow
and desktop widths. Recreate sample products only if the app restarted.
Compare **Remove** with **Add to cart**: the filled appearance and interaction
states should use the same theme, while the **Remove** label stays unchanged.
Use **Tab before manually scrolling**: the whole focus outline, including its
offset, must remain visible inside both the viewport and any scrolling list.
A visible button box alone does not prove that its focus ring is unclipped.
Collect observed defects together, approve one focused correction, then confirm
the result rather than starting an edit/rebuild loop for every control.
Confirm removal still deletes the whole product line, including all its units,
while other products, quantities and totals remain correct. Run:

```sh
./mvnw -Dtest=BaselineTest,CartContractTest,RemoveContractTest test
```

Expect all baseline and generated cart/removal tests to pass without
removing cases or weakening reviewed assertions.
Record the selected issue, skill guidance actually used and before/after
observations on the [worksheet](/workshops/copilot-app/worksheet/).

<details markdown="1">
<summary>If generated impeccable files appear in Changes</summary>

Ask Copilot to distinguish generated local state from useful design records.
For an untracked `.impeccable/hook.cache.json`, request a narrowly scoped
local Git exclude and review it before approval. Do not commit the cache,
delete the whole directory or ignore all `.impeccable/` files.
Keep intentional design records; review any proposed source change separately.

</details>

<details markdown="1" id="canvas-recovery">
<summary>If the canvas, picker or skill is unavailable</summary>

Check the running app's URL and owning terminal first; an unreachable server
is not a canvas failure. Control labels and availability can vary by build.
If Browser or Pick & polish is unavailable, preview in your normal browser
and send a screenshot or specific observation in the same session.
If impeccable is absent, use explicit UI acceptance criteria without
claiming that the skill ran. Record the unavailable feature or demonstration.
Do not install an unrelated canvas, expose a public tunnel or expand permissions.

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
