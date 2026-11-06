---
layout: default
title: Generate and iterate with Copilot
description: "Turn a small customer request into reviewed backend code, a working button and meaningful tests."
permalink: /workshops/copilot-app/generate/
redirect_from:
  - /workshops/copilot-app/review/
workshop: true
next: canvas
next_title: Canvas and Pick & polish
---

## What you will learn

Give Copilot a feature request with clear acceptance criteria, use a testing
skill and iterate on the generated code in the App.

## “Let me remove something from my cart”

Commit the bug fix first. Start a focused project session named
**Cart: remove item**, selecting **`workshop-quantity` as its base branch**.
Ask Copilot to confirm that the session starts at `workshop-quantity`, includes
the accepted bug fix and has no uncommitted changes. If not, stop and correct
the base; do not recreate the bug fix. If branch selection is unavailable,
continue in the session containing the reviewed fix. A new task can benefit
from a focused session, but it should keep the work you have already completed.

Give Copilot these acceptance criteria:

- Add a **Remove** button to each cart line.
- `DELETE /api/cart/items/{productId}` returns **200 with the updated cart**.
- Removing the final line produces an empty cart and zero count/total.
- Other products and quantities stay unchanged.
- A missing line returns **404** without changing the cart, including a product
  that exists in the catalogue but has never been added.
- Keep server prices, integer cents, existing stack and quantity behavior.

## Specify, generate, preview

Ask for a small plan, then invoke **`spring-boot-testing`** for the HTTP regression
coverage. In that **active session**, ask Copilot to activate the supplied tests:

```copilot
Copy teaching/RemoveContractTest.java unchanged into
src/test/java/com/juliendubois/workshop/.
Do not implement removal or change other files.
Show me the diff and wait for approval before committing.
```

Review **Changes**, then ask Copilot to commit only this acceptance test and run:

```sh
./mvnw -q -Dtest=RemoveContractTest test
```

On the repaired shop expect **3 tests, 2 failures**: DELETE still returns 404
for existing lines. Missing-line behavior already passes.

Let Copilot generate the backend and UI changes. Use Interactive to guide the
work, or Autopilot after approving the task's scope and permissions. Review all file
changes, not only the Java endpoint.

```sh
./mvnw -q -Dtest=BaselineTest,CartContractTest,RemoveContractTest test
```

The supplied classes contain **10 tests**, all green; additional tests may
increase the count without replacing the supplied cases. Review the feature,
then ask Copilot:

```copilot
Commit only the reviewed removal feature and its test changes, if not yet committed.
Confirm the working tree is clean and includes both the quantity fix and
removal feature. Do not create the next handoff branch yet; the Canvas
chapter will save it after the reviewed instruction and UI changes.
```

Stop the old shop with **Ctrl+C in its owning terminal**, then restart from this
reviewed session's directory:

```sh
./mvnw spring-boot:run
```

Preview: add two products, remove one, then remove the last. Confirm the empty state.

<figure>
  <img src="/workshops/copilot-app/assets/cart-feature.png" alt="The generated remove-item reference implementation leaves the Coffee mug in the cart after removing the Notebook." width="1600" height="1000" loading="lazy">
  <figcaption>A complete feature includes the customer interaction, not just an endpoint.</figcaption>
</figure>

**App tip:** describe what you observe: “The item disappears, but the
total is stale after removal” is better than “make the UI work.”

If the implementation is blocked, preserve your work and use
[a reference checkpoint](/workshops/copilot-app/facilitator/#recovery).
Continue to the Canvas exercise with a working feature, noting whether you
implemented it yourself or continued from the reference.

## What you have learned

- Start a focused App session from the reviewed branch rather than losing earlier work.
- Use acceptance criteria and **spring-boot-testing** to guide generation of both backend behavior and the UI.
- Review the full diff, test edge cases and use specific preview feedback to correct the generated feature.
