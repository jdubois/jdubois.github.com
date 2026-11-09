#!/usr/bin/env python3
"""Check rendered handbook, Git references, capture provenance and local anchors."""
from html.parser import HTMLParser
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "tools/copilot-workshop/.build/site"
STAGES = {"start": "cart-bug.png", "after-bugfix": "cart-fixed.png",
          "after-feature": "cart-feature.png", "after-performance": "cart-performance.png"}


def check_remote_references(references):
    refs = [f"refs/tags/{checkpoint['tag']}"
            for checkpoint in references["checkpoints"].values()]
    result = subprocess.run(
        ["git", "ls-remote", "--exit-code", "--tags", references["repository"] + ".git",
         *refs, *(ref + "^{}" for ref in refs)],
        check=True, capture_output=True, text=True, timeout=60)
    remote = dict(line.split()[::-1] for line in result.stdout.splitlines())
    for checkpoint in references["checkpoints"].values():
        ref = f"refs/tags/{checkpoint['tag']}^{{}}"
        assert remote.get(ref) == checkpoint["commit"], (
            f"Missing or moved annotated tag: {checkpoint['tag']}")


def check_evidence(assets):
    references = json.loads((assets / "references.json").read_text())
    assert set(references["checkpoints"]) == set(STAGES), "Wrong reference stages"
    for reference in references["checkpoints"].values():
        assert re.fullmatch(r"[0-9a-f]{40}", reference["commit"]), "Invalid pinned SHA"
        assert re.fullmatch(r"v[0-9]+-[a-z]+", reference["tag"]), "Invalid checkpoint tag"
    checks = json.loads((assets / references["verification"]).read_text())
    captures = json.loads((assets / "capture-manifest.json").read_text())
    evidence_path = assets / "mcp-evidence.json"
    evidence = json.loads(evidence_path.read_text())
    assert set(captures["stages"]) == set(evidence["stages"]) == set(STAGES), "Wrong capture stages"
    assert hashlib.sha256(evidence_path.read_bytes()).hexdigest() == captures["mcpEvidenceSha256"], (
        "MCP receipt hash mismatch")
    runtime = captures["javaRuntime"]
    assert all(isinstance(runtime.get(field), str) and runtime[field].strip()
               for field in ("version", "vendor", "vm")), "Missing capture JVM metadata"
    process_ids, request_ids = set(), set()
    baseline_cart = None
    for stage, image in STAGES.items():
        capture, receipt = captures["stages"][stage], evidence["stages"][stage]
        reference = references["checkpoints"][stage]
        assert capture["sourceRepository"] == references["repository"], stage
        assert capture["sourceTag"] == reference["tag"], stage
        assert capture["sourceCommit"] == reference["commit"] == checks["revisions"][reference["tag"]], stage
        identity = capture["identity"]
        assert identity == receipt["identity"], f"{stage}: mismatched runtime"
        assert identity["application"] == "shopping-cart" and identity["revision"] == reference["commit"], stage
        pid = identity["processId"]
        assert type(pid) is int and pid > 0 and pid not in process_ids, f"{stage}: invalid/reused PID"
        process_ids.add(pid)
        assert set(capture["images"]) == {image}, f"{stage}: missing/wrong screenshot"
        assert hashlib.sha256((assets / image).read_bytes()).hexdigest() == capture["images"][image], image

        assert receipt["workload"] == {"method": "GET", "path": "/api/cart", "distinctProducts": 8}, stage
        cart = receipt["cart"]
        items = cart["items"]
        product_ids = [item["productId"] for item in items]
        assert len(items) == len(set(product_ids)) == 8, f"{stage}: not eight distinct products"
        assert all(type(product_id) is int and product_id > 0 for product_id in product_ids), stage
        for item in items:
            assert isinstance(item["name"], str) and item["name"].strip(), stage
            assert type(item["quantity"]) is int and item["quantity"] == 1, stage
            assert type(item["priceCents"]) is int and item["priceCents"] > 0, stage
            assert type(item["lineTotalCents"]) is int, stage
            assert item["lineTotalCents"] == item["quantity"] * item["priceCents"], stage
        assert cart["itemCount"] == sum(item["quantity"] for item in items) == 8, stage
        assert cart["totalCents"] == sum(item["lineTotalCents"] for item in items) == 11500, stage
        ordered_cart = sorted(items, key=lambda item: item["productId"])
        if baseline_cart is None:
            baseline_cart = ordered_cart
        assert ordered_cart == baseline_cart, f"{stage}: changed cart contents"

        activity, profile = receipt["activity"], receipt["profile"]
        assert activity["tool"] == "get_live_activity", stage
        assert activity["arguments"] == {"query": "/api/cart", "limit": 8}, stage
        request = activity["matchedRequest"]
        request_id = request["id"]
        assert isinstance(request_id, str) and request_id and request_id not in request_ids, stage
        request_ids.add(request_id)
        assert (request["method"], request["path"], request["status"]) == ("GET", "/api/cart", 200), stage
        assert profile["tool"] == "get_request_profile" and profile["arguments"] == {"id": request_id}, stage
        assert (profile["requestId"], profile["route"], profile["status"]) == (request_id, "GET /api/cart", 200), stage
        for tool in (activity, profile):
            assert type(tool["originalResponseBytes"]) is int and tool["originalResponseBytes"] > 0, stage
        sql = [event for event in profile["timeline"] if event["source"] == "sql"]
        expected = 1 if stage == "after-performance" else 9
        assert len(sql) == profile["sqlEventCount"] == expected, f"{stage}: wrong SELECT count"
        assert all(event["label"].lstrip().lower().startswith("select ") for event in sql), stage
    return references


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path, self.links, self.ids = path, [], set()
        self.headings = 0
        self.redirect = False
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                raise AssertionError(f"Duplicate id in {self.path}: {attrs['id']}")
            self.ids.add(attrs["id"])
        if tag == "h1":
            self.headings += 1
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            self.redirect = True
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])
        if tag == "img" and not attrs.get("alt"):
            raise AssertionError(f"Missing image alt: {self.path}")


def resolve(path):
    if path.is_file():
        return path
    for candidate in (path / "index.html", path.with_suffix(".html")):
        if candidate.is_file():
            return candidate
    raise AssertionError(f"Missing local target: {path.relative_to(SITE)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--remote", action="store_true",
                        help="Also fail if a live annotated tag differs from its published SHA")
    args = parser.parse_args()
    pages = [Page(path) for path in (SITE / "workshops/copilot-app").rglob("*.html")]
    content = [page for page in pages if not page.redirect]
    expected_pages = len(list((ROOT / "workshops/copilot-app").glob("*.md")))
    assert len(content) == expected_pages, (
        f"Expected {expected_pages} handbook pages, got {len(content)}")
    cache = {page.path: page for page in pages}
    for page in pages:
        if not page.redirect:
            assert page.headings == 1, f"Expected one h1: {page.path}"
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            path = unquote(url.path)
            target = resolve(SITE / path.lstrip("/") if path.startswith("/")
                             else page.path.parent / path)
            if url.fragment and target.suffix == ".html":
                if target not in cache:
                    cache[target] = Page(target)
                assert unquote(url.fragment) in cache[target].ids, f"Missing anchor {link}"
    for svg in (SITE / "workshops/copilot-app/assets").glob("*.svg"):
        ET.parse(svg)
    assert not (SITE / "training").exists(), "Fixture source leaked into published site"
    assert not (SITE / "tools").exists(), "Maintainer tools leaked into published site"
    assets = ROOT / "workshops/copilot-app/assets"
    references = check_evidence(assets)
    if args.remote:
        check_remote_references(references)
    assert not (SITE / "workshops/copilot-app/downloads").exists(), "Obsolete downloads still published"
    print(f"{len(content)} pages: links, anchors, image alt, source exclusions, capture hashes and MCP receipts OK")
    print("Live annotated tag SHAs verified" if args.remote else "Remote refs not checked; use --remote for the release gate")


if __name__ == "__main__":
    main()
