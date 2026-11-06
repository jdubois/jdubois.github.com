# Workshop publishing and capture maintenance

The **only sample-code source** is
[jdubois/copilot-shopping-cart-workshop](https://github.com/jdubois/copilot-shopping-cart-workshop).
The template's `main` contains the starter; `reference/v2` contains the current
solution history, tagged `v2-start`, `v2-bugfix`, `v2-feature`, `v2-performance`.
No fixture copy, ZIP generator or downloadable source archive is maintained here.

The website owns the handbook, reference receipts and screenshot tooling.
`assets/references.json` pins the exact published commits for this edition.
Do not move published tags; use a new edition for fixture changes.
The original v1 references are retained unchanged. GitHub's active checkpoint-tag
ruleset prevents updates and deletion; new edition tags can still be created.

## Validate reference code in its own repository

From a full clone of the template:

```sh
git fetch origin --tags
python3 tools/verify-checkpoints.py
```

The verifier uses temporary Git worktrees, validates pinned skill provenance,
unchanged acceptance tests, exact intended failing assertions and green
checkpoints. Normal Maven CI is also included for participant-created repos.
Skill vendoring is maintained by `tools/vendor-skills.py` in the template only.

Copy its generated `target/checkpoint-checks/manifest.json` to this site's
`workshops/copilot-app/assets/checkpoint-checks.json` after a successful run.
This is a test receipt, not a second implementation.

## Capture and publish the handbook

```sh
CAPTURE_CHANNEL=chrome python3 tools/copilot-workshop/capture-all.py --port 18767
rbenv exec bundle exec jekyll build --destination tools/copilot-workshop/.build/site
python3 -m unittest discover -s tools/copilot-workshop -p 'test_*.py'
python3 tools/copilot-workshop/check-site.py --remote
```

The runner clones the public template at the four pinned Git commits. It rejects
moved tags, builds one revision at a time, verifies its owned JVM's revision/PID,
captures real shop interactions and stops that process in `finally`.
Use an unoccupied `--port`; never stop an unrelated app to free the default port.
Participant instructions still use 18765.

For missing browser tooling:

```sh
npm --prefix tools/copilot-workshop ci
npm --prefix tools/copilot-workshop exec -- playwright install chromium
```

`CAPTURE_CHANNEL=chrome` uses installed Chrome; otherwise use the pinned
Playwright Chromium. Use one browser across the stages. Captures check repeated
adds, removal and the sample workload. BootUI is accessed **only through MCP**.
The same eight-product cart gives 9 SELECTs before optimization and 1 afterward.

The capture manifest records source commits, PNG/MCP-receipt hashes,
browser/channel, Playwright and actual JVM versions. The Java release in
`references.json` is the compiler target, not a claim that the capture JVM was 21.
Receipts measure actual UTF-8 response bytes, not tokens.
`check-site.py` rejects stale source/image/test-receipt combinations, wrong
request/runtime matches, SQL counts, product uniqueness, cart totals and leftover
published downloads. Full synthetic cart lines are retained so totals and
preserved contents are verifiable, rather than asserted by a constant.

`--remote` checks each live annotated tag's peeled SHA against `references.json`
and fails on a missing or moved tag or network error. The website CI uses this
flag; omit it only for explicitly offline local checks. The regression suite
exercises tampered receipts and missing/moved/lightweight tags without network
access. Recovery instructions check out full commit SHAs directly, so they cannot
silently run a different revision behind a moved tag.

The reference PNGs are actual shop UI, **not** native Copilot or Chronicle captures.
Those require an opt-in pilot; never fabricate App screens or usage accounting.
Supplementary `assets/illustration-*.svg` files are editable conceptual
illustrations, not captured evidence. They are separate from the screenshot
and MCP provenance manifests; preserve those receipts when updating artwork.
Generated clones and the preview under `.build/` are ignored, disposable outputs,
not maintained sources.
