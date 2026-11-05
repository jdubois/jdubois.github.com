"""Regression checks for published reference and MCP evidence gates."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("check_site", Path(__file__).with_name("check-site.py"))
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.assets = Path(self.directory.name)
        self.references = {
            "repository": "https://github.com/jdubois/copilot-shopping-cart-workshop",
            "verification": "checkpoint-checks.json", "checkpoints": {}
        }
        self.checks = {"revisions": {}}
        self.captures = {"javaRuntime": {"version": "21", "vendor": "Test", "vm": "Test VM"}, "stages": {}}
        self.evidence = {"stages": {}}
        for index, (stage, image) in enumerate(CHECK.STAGES.items(), 1):
            tag, commit = "v2-" + stage.removeprefix("after-"), str(index) * 40
            self.references["checkpoints"][stage] = {"tag": tag, "commit": commit}
            self.checks["revisions"][tag] = commit
            identity = {"application": "shopping-cart", "revision": commit, "processId": index}
            image_bytes = image.encode()
            (self.assets / image).write_bytes(image_bytes)
            self.captures["stages"][stage] = {
                "identity": copy.deepcopy(identity), "sourceRepository": self.references["repository"],
                "sourceTag": tag, "sourceCommit": commit,
                "images": {image: hashlib.sha256(image_bytes).hexdigest()}
            }
            count, request_id = (1 if stage == "after-performance" else 9), f"request-{index}"
            prices = [1000] * 7 + [4500]
            self.evidence["stages"][stage] = {
                "identity": identity,
                "workload": {"method": "GET", "path": "/api/cart", "distinctProducts": 8},
                "cart": {
                    "items": [{"productId": i, "name": f"Product {i}", "quantity": 1,
                               "priceCents": price, "lineTotalCents": price}
                              for i, price in enumerate(prices, 1)],
                    "itemCount": 8, "totalCents": 11500
                },
                "activity": {
                    "tool": "get_live_activity", "arguments": {"query": "/api/cart", "limit": 8},
                    "originalResponseBytes": 100,
                    "matchedRequest": {"id": request_id, "method": "GET", "path": "/api/cart", "status": 200}
                },
                "profile": {
                    "tool": "get_request_profile", "arguments": {"id": request_id},
                    "originalResponseBytes": 200, "requestId": request_id,
                    "route": "GET /api/cart", "status": 200, "sqlEventCount": count,
                    "timeline": [{"source": "sql", "label": "select * from product"} for _ in range(count)]
                }
            }
        self.write_fixtures()

    def write_fixtures(self):
        self.write_json("references.json", self.references)
        self.write_json("checkpoint-checks.json", self.checks)
        self.write_json("mcp-evidence.json", self.evidence)
        self.captures["mcpEvidenceSha256"] = hashlib.sha256(
            (self.assets / "mcp-evidence.json").read_bytes()).hexdigest()
        self.write_json("capture-manifest.json", self.captures)

    def write_json(self, name, data):
        (self.assets / name).write_text(json.dumps(data))

    def test_valid_receipts(self):
        self.assertEqual(self.references, CHECK.check_evidence(self.assets))

    def test_rejects_mismatched_receipt_hash(self):
        self.evidence["stages"]["start"]["cart"]["totalCents"] = 1
        self.write_json("mcp-evidence.json", self.evidence)
        with self.assertRaisesRegex(AssertionError, "receipt hash"):
            CHECK.check_evidence(self.assets)

    def test_rejects_invalid_evidence_even_with_updated_hash(self):
        original = copy.deepcopy(self.evidence)
        mutations = [
            ("wrong total", lambda receipt: receipt["cart"].update(totalCents=1)),
            ("wrong count", lambda receipt: receipt["cart"].update(itemCount=7)),
            ("duplicate products", lambda receipt: receipt["cart"]["items"][1].update(productId=1)),
            ("changed price", lambda receipt: receipt["cart"]["items"][0].update(priceCents=999)),
            ("wrong SQL count", lambda receipt: receipt["profile"].update(sqlEventCount=1)),
            ("non-SELECT SQL", lambda receipt: receipt["profile"]["timeline"][0].update(label="delete from product")),
            ("wrong profile", lambda receipt: receipt["profile"].update(requestId="other")),
            ("wrong tool argument", lambda receipt: receipt["profile"]["arguments"].update(id="other")),
            ("wrong method", lambda receipt: receipt["activity"]["matchedRequest"].update(method="POST")),
            ("wrong runtime", lambda receipt: receipt["identity"].update(revision="f" * 40)),
            ("wrong workload", lambda receipt: receipt["workload"].update(distinctProducts=1)),
        ]
        for name, mutate in mutations:
            with self.subTest(name=name):
                self.evidence = copy.deepcopy(original)
                mutate(self.evidence["stages"]["start"])
                self.write_fixtures()
                with self.assertRaises(AssertionError):
                    CHECK.check_evidence(self.assets)

    def test_rejects_missing_stage(self):
        del self.evidence["stages"]["after-performance"]
        self.write_fixtures()
        with self.assertRaisesRegex(AssertionError, "stages"):
            CHECK.check_evidence(self.assets)

    def test_rejects_reused_pid(self):
        self.evidence["stages"]["after-bugfix"]["identity"]["processId"] = 1
        self.captures["stages"]["after-bugfix"]["identity"]["processId"] = 1
        self.write_fixtures()
        with self.assertRaisesRegex(AssertionError, "PID"):
            CHECK.check_evidence(self.assets)

    def test_rejects_changed_cart_with_valid_arithmetic(self):
        self.evidence["stages"]["after-performance"]["cart"]["items"][0]["name"] = "Different product"
        self.write_fixtures()
        with self.assertRaisesRegex(AssertionError, "cart contents"):
            CHECK.check_evidence(self.assets)

    def test_rejects_mismatched_image(self):
        (self.assets / "cart-bug.png").write_bytes(b"edited")
        with self.assertRaisesRegex(AssertionError, "cart-bug.png"):
            CHECK.check_evidence(self.assets)

    def test_rejects_missing_jvm_metadata(self):
        self.captures["javaRuntime"]["version"] = ""
        self.write_fixtures()
        with self.assertRaisesRegex(AssertionError, "JVM"):
            CHECK.check_evidence(self.assets)

    def remote_output(self, moved=False, peeled=True):
        lines = []
        for checkpoint in self.references["checkpoints"].values():
            ref = f"refs/tags/{checkpoint['tag']}"
            lines.append(f"{'f' * 40}\t{ref}")
            if peeled:
                commit = "0" * 40 if moved else checkpoint["commit"]
                lines.append(f"{commit}\t{ref}^{{}}")
        return "\n".join(lines)

    @patch.object(CHECK.subprocess, "run")
    def test_remote_annotated_tags_match(self, run):
        run.return_value.stdout = self.remote_output()
        CHECK.check_remote_references(self.references)
        self.assertEqual(run.call_args.kwargs["timeout"], 60)

    @patch.object(CHECK.subprocess, "run")
    def test_rejects_missing_moved_or_lightweight_remote_tags(self, run):
        for output in ("", self.remote_output(moved=True), self.remote_output(peeled=False)):
            with self.subTest(output=output):
                run.return_value.stdout = output
                with self.assertRaisesRegex(AssertionError, "tag"):
                    CHECK.check_remote_references(self.references)

    @patch.object(CHECK.subprocess, "run", side_effect=subprocess.CalledProcessError(1, ["git"]))
    def test_remote_transport_failure_is_not_a_pass(self, run):
        with self.assertRaises(subprocess.CalledProcessError):
            CHECK.check_remote_references(self.references)


if __name__ == "__main__":
    unittest.main()
