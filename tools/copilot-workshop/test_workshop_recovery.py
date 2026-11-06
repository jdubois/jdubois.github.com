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

    def prepare_boundary_correction(self):
        self.git("switch", "--quiet", "-c", "production-correction", "main")
        self.write("app/quantity-validation.txt", "reject fractional quantities\n")
        self.write("tests/quantity-validation.txt", "400, unchanged cart\n")
        self.commit("Reviewed production correction and focused regression")
        correction = self.head()
        self.git("switch", "--quiet", "main")
        self.assertEqual(self.git(
            "diff", "--name-only", "main", correction).stdout.splitlines(), [
                "app/quantity-validation.txt", "tests/quantity-validation.txt"])
        return correction

    def test_separate_production_pr_keeps_both_workers_and_their_scopes(self):
        self.prepare()
        correction = self.prepare_boundary_correction()
        self.git("merge", "--squash", correction)
        self.commit("Squash production correction PR")
        self.git("push", "--quiet", "origin", "main")
        self.recover()
        for path in ["app/quantity-validation.txt", "tests/quantity-validation.txt"]:
            self.assertEqual((self.tests / path).read_text(),
                             (self.repo / path).read_text())
        self.assertEqual(self.head(self.ui), self.ui_commit)
        self.assertEqual(self.git(
            "show", f"HEAD:tests/boundary.txt", cwd=self.tests).stdout,
            self.git("show", f"{self.test_commit}:tests/boundary.txt").stdout)
        recovered = self.head(self.tests)
        self.recover()
        self.assertEqual(self.head(self.tests), recovered)

    def test_offline_correction_uses_reviewed_handoff_without_moving_main(self):
        self.prepare()
        correction = self.prepare_boundary_correction()
        self.git("merge", "--no-edit", correction, cwd=self.tests)
        self.recover(online=False)
        self.assertEqual(self.head(ref="main"), self.main_start)
        self.assertEqual(self.head(ref="origin/main"), self.main_start)
        self.assertEqual(
            (self.tests / "app/quantity-validation.txt").read_text(),
            "reject fractional quantities\n")
        self.assertEqual(self.head(ref="production-correction"), correction)

    def test_recovery_stops_without_overwriting_uncommitted_work(self):
        self.prepare()
        self.write("tests/boundary.txt", "unfinished worker changes\n", cwd=self.tests)
        with self.assertRaises(AssertionError):
            self.recover()
        self.assertEqual(self.head(self.tests), self.test_commit)
        self.assertEqual((self.tests / "tests/boundary.txt").read_text(),
                         "unfinished worker changes\n")
        self.assertEqual(self.head(ref="main"), self.main_start)

    def prepare_checkout(self):
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
        self.checkout_tip = self.head(self.tests)
        self.combined_main = merged_main
        self.worker_tip = worker_tip

    def verify_merged_main(self):
        self.assertEqual(self.git("status", "--porcelain", cwd=self.tests).stdout, "")
        self.git("fetch", "--quiet", "origin", cwd=self.tests)
        main = self.head(self.tests, ref="origin/main")
        self.git("checkout", "--quiet", "--detach", main, cwd=self.tests)
        self.assertEqual(self.head(self.tests), main)
        self.assertEqual(
            self.git("branch", "--show-current", cwd=self.tests).stdout.strip(), "")
        return main

    def assert_checkout_refs_preserved(self):
        self.assertEqual(self.head(ref="test-worker"), self.worker_tip)
        self.assertEqual(self.head(self.ui), self.ui_commit)
        self.assertEqual(self.head(ref="workshop-checkout"), self.checkout_tip)

    def squash_checkout_pr(self):
        self.git("push", "--quiet", "origin", "workshop-checkout", cwd=self.tests)
        self.git("merge", "--squash", "workshop-checkout")
        self.commit("Squash approved checkout PR")
        self.git("push", "--quiet", "origin", "main")
        merged = self.head()
        self.git("update-ref", "refs/remotes/origin/main", self.combined_main)
        return merged

    def test_checkout_preparation_does_not_move_main_or_worker_branches(self):
        self.prepare_checkout()
        self.assert_checkout_refs_preserved()
        self.assertEqual(self.head(ref="main"), self.combined_main)
        self.assertEqual(self.head(ref="origin/main"), self.combined_main)
        self.assertEqual(
            self.git("branch", "--show-current", cwd=self.tests).stdout.strip(),
            "workshop-checkout")
        self.assertEqual(
            self.git("branch", "--show-current").stdout.strip(), "main")

    def test_checkout_publication_alone_does_not_count_as_merged_main(self):
        self.prepare_checkout()
        self.git("push", "--quiet", "origin", "workshop-checkout", cwd=self.tests)
        self.assertEqual(self.head(ref="origin/workshop-checkout"), self.checkout_tip)
        self.assertEqual(self.head(ref="main"), self.combined_main)
        self.assertEqual(self.head(ref="origin/main"), self.combined_main)
        self.assertNotEqual(self.checkout_tip, self.combined_main)
        self.assert_checkout_refs_preserved()

    def test_squashed_checkout_verifies_merged_main_without_moving_other_worktrees(self):
        self.prepare_checkout()
        merged = self.squash_checkout_pr()
        self.assertNotEqual(merged, self.checkout_tip)
        self.assertEqual(self.git(
            "merge-base", "--is-ancestor", self.checkout_tip, merged,
            check=False).returncode, 1)
        self.assertEqual(self.verify_merged_main(), merged)
        self.assertEqual(
            self.git("diff", "--exit-code", self.checkout_tip, merged).stdout, "")
        self.assertEqual((self.tests / "app/order.txt").read_text(),
                         "checkout fixture\n")
        self.assert_combined()
        self.assert_checkout_refs_preserved()
        self.assertEqual(
            self.git("branch", "--show-current").stdout.strip(), "main")

    def test_checkout_verification_fetches_later_main_not_stale_feature_or_merge(self):
        self.prepare_checkout()
        merged = self.squash_checkout_pr()
        self.write("docs/other-work.txt", "later accepted main change\n")
        self.commit("Subsequent accepted change")
        self.git("push", "--quiet", "origin", "main")
        latest = self.head()
        self.git("update-ref", "refs/remotes/origin/main", self.combined_main)
        self.assertNotEqual(latest, merged)
        self.assertEqual(self.verify_merged_main(), latest)
        self.assertEqual((self.tests / "app/order.txt").read_text(),
                         "checkout fixture\n")
        self.assertEqual((self.tests / "docs/other-work.txt").read_text(),
                         "later accepted main change\n")
        self.assert_checkout_refs_preserved()

    def test_checkout_verification_stops_without_overwriting_dirty_work(self):
        self.prepare_checkout()
        self.squash_checkout_pr()
        self.write("app/order.txt", "unreviewed follow-up\n", cwd=self.tests)
        with self.assertRaises(AssertionError):
            self.verify_merged_main()
        self.assertEqual(self.head(self.tests), self.checkout_tip)
        self.assertEqual((self.tests / "app/order.txt").read_text(),
                         "unreviewed follow-up\n")
        self.assert_checkout_refs_preserved()

    def test_blocked_checkout_publication_preserves_local_work_and_main(self):
        self.prepare_checkout()
        self.git("remote", "set-url", "--push", "origin",
                 str(self.root / "unavailable.git"))
        pushed = self.git("push", "origin", "workshop-checkout",
                          cwd=self.tests, check=False)
        self.assertNotEqual(pushed.returncode, 0)
        self.assertEqual(self.head(ref="main"), self.combined_main)
        self.assertEqual(self.head(ref="origin/main"), self.combined_main)
        self.assertEqual(self.head(self.tests), self.checkout_tip)
        self.assert_checkout_refs_preserved()

    def test_offline_checkout_verification_does_not_report_cached_main_as_current(self):
        self.prepare_checkout()
        self.git("remote", "set-url", "origin", str(self.root / "unavailable.git"))
        with self.assertRaises(subprocess.CalledProcessError):
            self.verify_merged_main()
        self.assertEqual(self.head(self.tests), self.checkout_tip)
        self.assertEqual(self.head(ref="origin/main"), self.combined_main)
        self.assert_checkout_refs_preserved()


if __name__ == "__main__":
    unittest.main()
