"""Replay the documented Git recovery steps in isolated local repositories."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

BUILD = Path(__file__).resolve().parent / ".build"


class WorkshopRecoveryTests(unittest.TestCase):
    def setUp(self):
        BUILD.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="recovery-", dir=BUILD)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repository"
        self.remote = self.root / "remote.git"
        self.ui = self.root / "ui-session"
        self.tests = self.root / "test-session"
        self.environment = {
            **os.environ,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_AUTHOR_NAME": "Workshop test",
            "GIT_AUTHOR_EMAIL": "workshop-test@example.invalid",
            "GIT_COMMITTER_NAME": "Workshop test",
            "GIT_COMMITTER_EMAIL": "workshop-test@example.invalid",
        }
        self.repo.mkdir()
        self.git("init", "--quiet", "--bare", str(self.remote), cwd=self.root)
        self.git("init", "--quiet", "--initial-branch=main")
        self.git("remote", "add", "origin", str(self.remote))

    def git(self, *arguments, cwd=None, check=True):
        return subprocess.run(
            ["git", "-c", "commit.gpgsign=false",
             "-c", f"core.hooksPath={os.devnull}", *arguments],
            cwd=cwd or self.repo, env=self.environment,
            check=check, capture_output=True, text=True, timeout=20)

    def commit(self, message, cwd=None):
        self.git("add", ".", cwd=cwd)
        self.git(
            "commit", "--quiet", "-m", message, "-m",
            "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>",
            cwd=cwd)

    def write(self, path, content, cwd=None):
        target = (cwd or self.repo) / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)

    def head(self, cwd=None, ref="HEAD"):
        return self.git("rev-parse", ref, cwd=cwd).stdout.strip()

    def prepare(self, merged=True):
        self.write("app/cart.txt", "starter\n")
        self.commit("Starter")
        self.starter = self.head()
        self.git("switch", "--quiet", "-c", "accepted-tickets")
        self.write("app/cart.txt", "quantity fix\n")
        self.write("app/removal.txt", "remove item\n")
        self.write("app/query.txt", "one SELECT\n")
        self.write("tests/acceptance.txt", "baseline, cart, removal, query\n")
        self.commit("Three accepted tickets")
        self.accepted = self.head()
        self.git("switch", "--quiet", "main")
        if merged:
            self.git("merge", "--squash", "accepted-tickets")
            self.commit("Merge preparation PR")
        self.main_start = self.head()
        self.preparation_merged = merged
        self.git("push", "--quiet", "origin", "main")
        base = "main" if merged else "accepted-tickets"
        self.git("worktree", "add", "--quiet", "-b", "ui-worker", str(self.ui), base)
        self.git("worktree", "add", "--quiet", "-b", "test-worker", str(self.tests), base)
        self.write("app/ui.txt", "empty-cart catalogue link\n", cwd=self.ui)
        self.commit("Reviewed UI worker", cwd=self.ui)
        self.ui_commit = self.head(self.ui)
        self.write("tests/boundary.txt", "missing, non-integer, 99\n", cwd=self.tests)
        self.commit("Reviewed test worker", cwd=self.tests)
        self.test_commit = self.head(self.tests)

    def merge_ui_pr(self, squash=True, repair=False):
        cached_main = self.head(ref="origin/main")
        if repair:
            self.write("app/ui.txt", "reviewed keyboard-accessible link\n", cwd=self.ui)
            self.commit("Reviewed Agent Merge repair", cwd=self.ui)
            self.ui_commit = self.head(self.ui)
        if squash:
            self.git("merge", "--squash", "ui-worker")
            self.commit("Squash UI PR")
        else:
            self.git(
                "merge", "--no-ff", "ui-worker", "-m",
                "Merge UI PR\n\nCo-authored-by: Copilot App "
                "<223556219+Copilot@users.noreply.github.com>")
        self.git("push", "--quiet", "origin", "main")
        # A GitHub-side merge does not refresh a learner's cached remote ref.
        self.git("update-ref", "refs/remotes/origin/main", cached_main)

    def recover(self, online=True):
        self.assertEqual(self.git("status", "--porcelain", cwd=self.tests).stdout, "")
        self.assertEqual(
            self.git("branch", "--show-current", cwd=self.tests).stdout.strip(),
            "test-worker")
        if self.preparation_merged and online:
            self.git("fetch", "--quiet", "origin", cwd=self.tests)
            self.git("merge", "--no-edit", "origin/main", cwd=self.tests)
        ui_missing = self.git(
            "diff", "--quiet", self.ui_commit, "--", "app/ui.txt",
            cwd=self.tests, check=False).returncode
        self.assertIn(ui_missing, (0, 1))
        if ui_missing:
            self.git("merge", "--no-edit", self.ui_commit, cwd=self.tests)
        self.assert_combined()
        self.assertEqual(self.head(ref="test-worker"), self.head(self.tests))

    def assert_combined(self):
        for path in ["app/cart.txt", "app/removal.txt", "app/query.txt",
                     "tests/acceptance.txt", "tests/boundary.txt"]:
            with self.subTest(file=path):
                self.assertEqual((self.tests / path).read_text(),
                                 (self.repo / path).read_text()
                                 if path != "tests/boundary.txt"
                                 and self.preparation_merged
                                 else self.git(
                                     "show", f"{self.test_commit}:{path}",
                                     cwd=self.tests).stdout)
        self.assertEqual((self.tests / "app/ui.txt").read_text(),
                         (self.ui / "app/ui.txt").read_text())
        self.assertEqual(self.head(self.ui), self.ui_commit)

    def test_preparation_blocked_preserves_accepted_local_base(self):
        self.prepare(merged=False)
        self.recover()
        self.assertEqual(self.head(ref="main"), self.starter)
        self.assertEqual(self.head(ref="accepted-tickets"), self.accepted)

    def test_before_ui_merge_combines_workers_without_updating_main(self):
        self.prepare()
        self.recover()
        self.assertEqual(self.head(ref="main"), self.main_start)
        self.assertEqual(self.head(ref="origin/main"), self.main_start)

    def test_squashed_ui_and_reviewed_repair_are_not_applied_twice(self):
        self.prepare()
        self.merge_ui_pr(repair=True)
        self.assertNotEqual(self.head(), self.ui_commit)
        self.assertEqual(self.git(
            "merge-base", "--is-ancestor", self.ui_commit, "main",
            check=False).returncode, 1)
        self.recover()
        recovered = self.head(self.tests)
        self.recover()
        self.assertEqual(self.head(self.tests), recovered)

    def test_regular_ui_merge_preserves_boundary_tests(self):
        self.prepare()
        self.merge_ui_pr(squash=False)
        self.recover()
        self.assertEqual(self.git(
            "merge-base", "--is-ancestor", self.test_commit, "HEAD",
            cwd=self.tests, check=False).returncode, 0)

    def test_offline_partial_merge_uses_reviewed_local_handoff(self):
        self.prepare()
        cached_main = self.head(ref="origin/main")
        self.merge_ui_pr(repair=True)
        self.recover(online=False)
        self.assertEqual(self.head(ref="origin/main"), cached_main)
        self.assertNotEqual(self.head(self.tests), self.head(ref="origin/main"))

    def test_recovery_stops_without_overwriting_uncommitted_work(self):
        self.prepare()
        self.write("tests/boundary.txt", "unfinished worker changes\n", cwd=self.tests)
        with self.assertRaises(AssertionError):
            self.recover()
        self.assertEqual(self.head(self.tests), self.test_commit)
        self.assertEqual((self.tests / "tests/boundary.txt").read_text(),
                         "unfinished worker changes\n")
        self.assertEqual(self.head(ref="main"), self.main_start)

    def test_final_verification_reuses_worktree_without_moving_branches(self):
        self.prepare()
        self.merge_ui_pr()
        self.recover()
        worker_tip = self.head(self.tests)
        self.git("merge", "--squash", "test-worker")
        self.commit("Squash test PR")
        self.git("push", "--quiet", "origin", "main")
        merged_main = self.head()
        self.git("fetch", "--quiet", "origin", cwd=self.tests)
        self.git("checkout", "--quiet", "--detach", "origin/main", cwd=self.tests)
        self.assertEqual(self.head(self.tests), merged_main)
        self.assertEqual(self.head(ref="main"), merged_main)
        self.assertEqual(self.head(ref="test-worker"), worker_tip)
        self.assertEqual(self.head(self.ui), self.ui_commit)
        self.assertEqual(
            self.git("branch", "--show-current", cwd=self.tests).stdout.strip(), "")
        self.assert_combined()
        self.git("switch", "--quiet", "-c", "workshop-checkout", cwd=self.tests)
        self.write("app/order.txt", "checkout fixture\n", cwd=self.tests)
        self.commit("Reviewed checkout feature", cwd=self.tests)
        self.assertEqual(self.head(ref="main"), merged_main)
        self.assertEqual(self.head(ref="origin/main"), merged_main)
        self.assertEqual(self.head(ref="test-worker"), worker_tip)
        self.assertEqual(self.head(self.ui), self.ui_commit)
        self.assertEqual(
            self.git("branch", "--show-current", cwd=self.tests).stdout.strip(),
            "workshop-checkout")
        self.assertEqual(
            self.git("branch", "--show-current").stdout.strip(), "main")


if __name__ == "__main__":
    unittest.main()
