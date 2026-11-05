"""Keep one workshop without duration labels, chapter timings or alternate routes."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
HANDBOOK = ROOT / "workshops/copilot-app"
SEQUENCE = ["", "setup", "ticket", "fusion", "skills", "verify", "generate",
            "tools", "parallel", "integrate", "tokens", "finish"]
EXERCISES = {"ticket", "fusion", "skills", "verify", "generate",
             "tools", "parallel", "integrate", "tokens", "finish"}


def chapter(slug):
    return (HANDBOOK / (slug or "index")).with_suffix(".md").read_text()


class WorkshopScheduleTests(unittest.TestCase):
    def test_exercises_have_app_learning_goals_and_recap(self):
        for path in HANDBOOK.glob("*.md"):
            if path.stem not in EXERCISES:
                continue
            body = path.read_text().split("---", 2)[2].strip()
            with self.subTest(chapter=path.name):
                self.assertTrue(body.startswith("## What you will learn\n"))
                self.assertEqual(body.count("## What you will learn\n"), 1)
                self.assertEqual(body.count("## What you have learned\n"), 1)
                goals = body.split("\n## ", 1)[0]
                self.assertRegex(goals, r"Copilot|Chronicle")
                recap = body.split("## What you have learned\n", 1)[1]
                self.assertNotIn("\n## ", recap)
                self.assertGreaterEqual(
                    len(re.findall(r"^- ", recap, re.MULTILINE)), 3)

    def test_preparation_and_reference_pages_have_no_learning_blocks(self):
        for path in HANDBOOK.glob("*.md"):
            if path.stem in EXERCISES:
                continue
            with self.subTest(page=path.name):
                text = path.read_text()
                self.assertNotIn("## What you will learn", text)
                self.assertNotIn("## What you have learned", text)
        self.assertIn("## The scenario", chapter(""))

    def test_one_workshop_flow_without_a_timetable(self):
        landing = chapter("")
        self.assertIn("hands-on workshop", landing)
        self.assertEqual(landing.count("## Workshop flow"), 1)
        self.assertNotIn("| Minutes |", landing)
        self.assertIn("Take a break before the parallel work", landing)

    def test_chapters_have_no_deadlines_or_timeboxes(self):
        timing = re.compile(r"^timebox:|\bminute \d+|\b\d{2,3}–\d{2,3}\b|\bcutoff\b",
                            re.MULTILINE | re.IGNORECASE)
        for path in HANDBOOK.glob("*.md"):
            with self.subTest(chapter=path.name):
                self.assertIsNone(timing.search(path.read_text()))

    def test_workshop_has_no_duration_labels(self):
        duration = re.compile(r"\b(?:three|3)[- ]hours?\b|\b180[- ]minutes?\b",
                              re.IGNORECASE)
        paths = list(HANDBOOK.glob("*.md")) + [
            ROOT / "_includes/copilot-workshop-nav.html"
        ]
        for path in paths:
            with self.subTest(path=path.name):
                self.assertIsNone(duration.search(path.read_text()))
        listing = (ROOT / "conferences.html").read_text()
        workshop_listing = next(
            line for line in listing.splitlines()
            if 'href="/workshops/copilot-app/"' in line
        )
        self.assertIsNone(duration.search(workshop_listing))

    def test_learner_startup_needs_no_revision_argument(self):
        setup = chapter("setup")
        self.assertIn('annotated tag workshop-start', setup)
        self.assertNotIn("Record that SHA", setup)
        for slug in ["setup", "verify", "generate", "tools"]:
            with self.subTest(startup_chapter=slug):
                self.assertIn("\n./mvnw spring-boot:run\n", chapter(slug))
        for path in HANDBOOK.glob("*.md"):
            text = path.read_text()
            with self.subTest(chapter=path.name):
                self.assertIsNone(re.search(r"\b[A-Z][A-Z_]*_SHA\b", text))
                self.assertNotIn("workshop.revision", text)
                self.assertNotIn("runtime revision", text)
                for command in re.findall(r"^\./mvnw spring-boot:run[^\n]*$",
                                          text, re.MULTILINE):
                    self.assertEqual(command, "./mvnw spring-boot:run")
        self.assertNotIn("`workshop-start` SHA", chapter("worksheet"))

    def test_checkout_and_git_bookkeeping_are_app_driven(self):
        setup = chapter("setup")
        self.assertIn("Add GitHub repository", setup)
        self.assertIn("New worktree", setup)
        self.assertIn("your new `cart-workshop` repository", setup)
        commands = re.compile(
            r"\bgit\s+(?:clone|--version|remote|tag|status|branch|rev-parse|"
            r"add|diff|commit|switch|checkout|merge)\b",
            re.IGNORECASE)
        for path in HANDBOOK.glob("*.md"):
            if path.stem == "facilitator":
                continue
            with self.subTest(chapter=path.name):
                self.assertIsNone(commands.search(path.read_text()))
        for slug, branch in [
                ("verify", "workshop-quantity"),
                ("generate", "workshop-feature"),
                ("parallel", "workshop-complete")]:
            with self.subTest(handoff=branch):
                self.assertIn(f"Create a branch {branch}", chapter(slug))
                self.assertIn("Do not replace an existing branch", chapter(slug))

    def test_next_links_and_navigation_have_one_linear_sequence(self):
        for index, slug in enumerate(SEQUENCE):
            with self.subTest(chapter=slug or "index"):
                metadata = chapter(slug).split("---", 2)[1]
                following = re.search(r"^next: (\S+)$", metadata, re.MULTILINE)
                if index == len(SEQUENCE) - 1:
                    self.assertIsNone(following)
                else:
                    self.assertIsNotNone(following)
                    self.assertEqual(following.group(1), SEQUENCE[index + 1])
                self.assertNotIn("next_anchor:", metadata)
        navigation = (ROOT / "_data/copilot_workshop.yml").read_text()
        slugs = [value.strip('"').rstrip("/") for value in
                 re.findall(r"^  slug: (.*)$", navigation, re.MULTILINE)]
        self.assertEqual(slugs[:len(SEQUENCE)], SEQUENCE)

    def test_integration_uses_sequential_agent_merge_with_correct_target(self):
        integration = chapter("integrate")
        prose = re.sub(r"\s+", " ", integration)
        for text in [
                "**`workshop-complete` as the integration branch**, not `main`",
                "## Open the two worker PRs",
                "## Merge the UI PR first",
                "## Check the UI merge",
                "## Update and merge the test PR",
                "## Verify the combined application",
                "Leave the test PR's Agent Merge off.",
                "**Done when:** the UI PR's status is **Merged**",
                "original **12 tests plus the new boundary",
                "all required checks and approvals pass",
                "Do not reset workshop-complete or this branch"]:
            with self.subTest(requirement=text):
                self.assertIn(text, prose)
        stages = ["## Open the two worker PRs", "## Merge the UI PR first",
                  "## Check the UI merge", "## Update and merge the test PR",
                  "## Verify the combined application"]
        positions = [integration.index(stage) for stage in stages]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn("--no-ff", integration)

    def test_integration_explains_sessions_review_gates_and_remote_state(self):
        prose = re.sub(r"\s+", " ", chapter("integrate"))
        for text in [
                "**Cart: integration**",
                "**Base** means the branch receiving the changes",
                "**Head** means the worker branch supplying the changes",
                "branch tip equals its reviewed handoff commit",
                "leave **Merge pull request** unchecked",
                "origin/workshop-complete, not the possibly stale local workshop-complete",
                "Fast-forward only this integration session's clean branch",
                "including a squash merge",
                "fresh CI for its new revision",
                "may make further permitted repairs and merge without another review pause",
                "A denied permission",
                "If remote status cannot be checked, record it as unknown"]:
            with self.subTest(requirement=text):
                self.assertIn(text, prose)
        ui = prose.split("## Merge the UI PR first", 1)[1].split(
            "## Check the UI merge", 1)[0]
        self.assertLess(ui.index("leave **Merge pull request** unchecked"),
                        ui.index("Merge this reviewed UI PR"))
        self.assertLess(ui.index("Review the UI PR's complete updated diff"),
                        ui.index("Merge this reviewed UI PR"))
        test = prose.split("## Update and merge the test PR", 1)[1].split(
            "## Verify the combined application", 1)[0]
        self.assertLess(test.index("**Merge pull request** still off"),
                        test.index("Merge this reviewed boundary-test PR"))
        self.assertIn("Do not reuse the UI authorization prompt", chapter("prompts"))
        self.assertIn("comparison starting point only", chapter("finish"))

    def test_agent_merge_prerequisites_recovery_and_handoff_are_consistent(self):
        setup = chapter("setup")
        for text in ["GitHub Actions", "create PRs and merge them", "local recovery"]:
            self.assertIn(text, setup)
        self.assertIn("Agent Merge", chapter(""))
        self.assertIn("Do not let the workers open or merge PRs yet", chapter("parallel"))
        self.assertIn("## Integrate with Agent Merge", chapter("prompts"))
        for slug in ["integrate", "worksheet"]:
            with self.subTest(chapter=slug):
                self.assertIn("Agent Merge not completed: local recovery used", chapter(slug))
        recovery = chapter("integrate").split('<summary>Recovery:', 1)[1]
        self.assertIn("Disable Agent Merge in each worker session", recovery)
        self.assertIn("Do not push, merge remote PRs or enable Agent Merge", recovery)
        self.assertIn("two worker PRs targeting `workshop-complete`", chapter("facilitator"))
        finish = chapter("finish")
        self.assertIn("not `main`", finish)
        self.assertNotIn("## Optional GitHub delivery", finish)
        self.assertNotIn("No remote PR is required", finish)

    def test_alternative_route_instructions_are_removed(self):
        paths = list(HANDBOOK.glob("*.md")) + [
            ROOT / "conferences.html", ROOT / "_includes/copilot-workshop-nav.html"
        ]
        obsolete = re.compile(
            r"\b(?:one|two)[- ]hour\b|\b[12]h\b|one-hour-demo|extended-clinic|choose your route",
            re.IGNORECASE)
        for path in paths:
            with self.subTest(path=path.name):
                self.assertIsNone(obsolete.search(path.read_text()))


if __name__ == "__main__":
    unittest.main()
