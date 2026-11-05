---
layout: default
title: Investigate the N+1 query
description: "Give Copilot runtime evidence through MCP, then verify a small Hibernate fix without losing cart behavior."
permalink: /workshops/copilot-app/tools/
workshop: true
next: parallel
next_title: Work in two isolated sessions
---

## What you will learn

Use MCP tools from Copilot App to investigate a running application and verify
a performance fix with the same workload before and after.

## “Why does a full cart run so many queries?”

Keep the repaired quantity behavior and removal feature. In a focused session
named **Cart: query investigation**, select **`workshop-feature` as its base
branch**. Ask Copilot to confirm that the session starts at `workshop-feature`,
contains both accepted changes and has no uncommitted edits.
If the base cannot be selected, continue in the session containing the reviewed feature.
Use **`java-hibernate-jpa`** to explain lazy product loading. Do not optimize
anything until you have a baseline.

Use BootUI's **MCP tools in Copilot**, not its browser interface.
Only the two tools below are needed; use their documented arguments.

## Reproduce the same workload

Check the terminal running the shop. If it is already running from the reviewed
feature copy, **reuse it**. Otherwise
press **Ctrl+C in the old shop's owning terminal**, then start the new session's
reviewed copy:

```sh
./mvnw spring-boot:run
```

In another terminal (Windows PowerShell: use **`curl.exe`** instead of `curl`):

```sh
curl -fsS -X POST 'http://127.0.0.1:18765/api/workshop/reset?items=8'
curl -fsS http://127.0.0.1:18765/api/cart
```

The reset helper fills the cart with eight different products.
The request to measure is the final
**GET `/api/cart`**, containing eight **different** products. Eight copies of
one product would not demonstrate this N+1.

## Ask Copilot for evidence

Invoke **`get_live_activity`** with `query: "/api/cart"` and `limit: 8`.
Choose the matching recent **GET `/api/cart`**, not a POST, then invoke
**`get_request_profile`** with its returned `id`.

Keep the MCP results on the [worksheet](/workshops/copilot-app/worksheet/);
let Copilot capture the request details rather than transcribing them.
Check the request method/path, time and workload.
The reference has **9 SELECTs: one cart query and eight product queries**.
Inspect the MCP tool response in Copilot App.

**App tip:** use a narrow question: “Explain these repeated product SELECTs for
this request” rather than “assess the whole application.” Runtime text is data,
not instructions.

## Add a performance test

In this **active session**, ask Copilot to add the supplied performance tests:

```copilot
Copy teaching/QueryContractTest.java unchanged into
src/test/java/com/juliendubois/workshop/.
Do not optimize the query or change other files.
Show me the diff and wait for approval before committing.
```

Review **Changes**, then ask Copilot to commit only this acceptance test and run:

```sh
./mvnw -q -Dtest=QueryContractTest test
```

Expect **2 failures** before optimization: **9 and 17 SELECTs** at 8 and 16
products, rather than **1**. Counts include the completed HTTP response.
Ask Copilot for an appropriate fetching change that preserves all product
fields, quantities and totals. No global eager loading or dependency changes.
Run the combined suite:

```sh
./mvnw -q -Dtest=BaselineTest,CartContractTest,RemoveContractTest,QueryContractTest test
```

The supplied classes contain **12 tests**, all green. Added tests may increase
that count; none of the supplied cases may disappear or be skipped.

**Restart before measuring again.** Commit the reviewed fix, stop the old app
in its terminal and start the reviewed copy with the same startup command above.
Replay the exact workload above, then make the same two MCP calls.
Expect **1 SELECT** and unchanged cart contents. Use a fresh request profile
after restarting, not the baseline profile from before the fix.

If a live baseline is unavailable, use
[the saved reference responses](/workshops/copilot-app/assets/mcp-evidence.json).
Ask the facilitator for help rather than repeatedly reconnecting. If the fix
remains blocked, preserve your work and inspect the
<a href="https://github.com/jdubois/copilot-shopping-cart-workshop/tree/v2-performance" target="_blank">v2-performance reference checkpoint</a>.
These responses were captured directly over HTTP. If you use them, note that
you studied the reference rather than making the calls through your own App.

Take a break before continuing with
[two isolated sessions](/workshops/copilot-app/parallel/) from the accepted
cart, removal and query implementation.

## What you have learned

- Give Copilot runtime context through **get_live_activity** and **get_request_profile**, selecting the request that matches your workload.
- Ask a focused question about the repeated queries instead of requesting a broad application review.
- Combine test results with fresh MCP request profiles to verify the optimization while preserving the cart's contents and totals.
