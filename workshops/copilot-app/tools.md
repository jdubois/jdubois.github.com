---
layout: default
title: Investigate runtime with MCP
description: "Give Copilot runtime evidence through MCP, then verify a small Hibernate fix without losing cart behavior."
permalink: /workshops/copilot-app/tools/
workshop: true
next: parallel
next_title: Parallel sessions
---

## What you will learn

Use MCP tools from Copilot App to investigate a running application and verify
a performance fix with the same workload before and after.

## “Why does a full cart run so many queries?”

Continue in **the same workshop session, on its current branch**.
Ask Copilot to confirm that it contains all those accepted changes—the quantity
fix, removal feature and reviewed Canvas changes—and has no uncommitted edits.
Do not create another session or change branches.
Use **`java-hibernate-jpa`** to explain lazy product loading. Do not optimize
anything until you have a baseline.

Use BootUI's **MCP tools in Copilot**, not its browser interface.
Only the two tools below are needed; use their documented arguments.

## Start the reviewed shop

Check the terminal running the shop. If it is already running from the reviewed
feature code in this session's directory, **reuse it**; **DevTools** picks up
compiled changes. If it is running from another worktree, press **Ctrl+C in the
shop's owning terminal** first. Only if the server is not running from this
session's directory, start it here:

```sh
./mvnw spring-boot:run
```

## Connect runtime tools

<a href="https://www.julien-dubois.com/boot-ui/" target="_blank">BootUI</a>
is preinstalled. Its MCP configuration is included in `.github/mcp.json`:

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

With your shop running, ask Copilot to call **`get_live_activity`** with
`query: "/api/cart"` and `limit: 1`. A tool response, even an empty list, confirms
the connection works. If it fails, check trust and reload settings before
continuing. If MCP remains unavailable, ask the facilitator to demonstrate
the exercise using [the saved reference responses](/workshops/copilot-app/assets/mcp-evidence.json).

## Reproduce the same workload

In another terminal (Windows PowerShell: use **`curl.exe`** instead of `curl`):

```sh
curl -fsS -X POST 'http://127.0.0.1:18765/api/workshop/reset?items=8'
curl -fsS http://127.0.0.1:18765/api/cart
```

The reset helper fills the cart with eight different products.
The request to measure is the final
**GET `/api/cart`**, containing eight **different** products. Eight copies of
one product would not demonstrate this N+1.

<figure>
  <a href="/workshops/copilot-app/assets/illustration-mcp-query.svg" target="_blank"><img src="/workshops/copilot-app/assets/illustration-mcp-query.svg" alt="Reference query pattern for GET /api/cart with eight different products: 1 cart query plus 8 product queries before optimization, and 1 SELECT afterward with unchanged cart contents and totals." width="1440" height="820" loading="lazy"></a>
  <figcaption>The reference workload, illustrated. Use your own matching MCP request profiles to establish before-and-after evidence.</figcaption>
</figure>

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

## Generate the query-budget tests

Stay in this session. Use **`/spring-boot-testing`** to turn the measured problem
into tests that require the correct query budget, not the current inefficient
behavior:

```copilot
/spring-boot-testing
Generate src/test/java/com/juliendubois/workshop/QueryContractTest.java
using the existing HTTP test fixtures and Hibernate statistics.
For carts with 8 and 16 distinct products, require exactly 1 SELECT for
the completed HTTP GET /api/cart response.
Seed each cart first, then clear the statistics before the GET.
Record the statement count immediately after the completed response,
before any verification queries, so setup and verification SQL are excluded.
Also assert product IDs, names, prices, quantities, line totals, item count
and total against the seeded data, so a faster but incomplete cart cannot pass.
Use real HTTP requests and database access, not mocked repositories or counts.
Generate tests from these criteria; do not retrieve reference tests or solutions.
Do not optimize production code, change earlier tests or add dependencies.
Explain the measurement and show the assertions for my review before running
or committing.
```

Review **Changes**, especially where measurement starts and ends.
After reviewing, run:

```sh
./mvnw -Dtest=QueryContractTest test
```

The query-budget assertions should fail before optimization: the reference
workloads perform **9 and 17 SELECTs** at 8 and 16 products, rather than **1**.
The generated test count may vary. Check the observed statement counts;
setup errors or zero executed tests do not demonstrate the N+1.
Commit only the reviewed tests once they demonstrate the problem.

Then ask Copilot to apply a scoped fetching fix:

```copilot
/java-hibernate-jpa
Use our MCP evidence and failing query-budget tests to fix the N+1.
Preserve all cart fields, quantities, totals and reviewed test assertions.
No global eager loading, dependency changes or unrelated refactors.
Run the combined baseline, cart, removal and query test suite.
Show me the implementation diff and actual test results before committing.
```

Run the combined suite:

```sh
./mvnw -Dtest=BaselineTest,CartContractTest,RemoveContractTest,QueryContractTest test
```

The **4 baseline tests and all generated cart, removal and query tests**
must pass. Report the actual count; no earlier case
may disappear, be skipped or have its reviewed assertions weakened.

**Wait for DevTools before measuring again.** The combined test run compiled
the fix; wait for the automatic restart to finish in the shop's terminal.
Commit the reviewed fix. Recreate the exact workload above after the data reset,
then make the same two MCP calls.
Expect **1 SELECT** and unchanged cart contents. Use a fresh request profile
from the updated app, not the baseline profile from before the fix.

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
- Generate query-budget tests that measure the completed HTTP response without counting setup or verification queries.
- Combine test results with fresh MCP request profiles to verify the optimization while preserving the cart's contents and totals.
