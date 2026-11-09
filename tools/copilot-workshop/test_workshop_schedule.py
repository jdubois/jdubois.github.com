"""Keep one workshop without duration labels, chapter timings or alternate routes."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
HANDBOOK = ROOT / "workshops/copilot-app"
SEQUENCE = ["", "setup", "ticket", "modes", "skills", "verify", "generate",
            "canvas", "tools", "parallel", "integrate", "rubber-duck",
            "subagents", "tokens", "finish"]
EXERCISES = {"ticket", "modes", "skills", "verify", "generate",
             "canvas", "tools", "parallel", "integrate", "rubber-duck",
             "subagents", "tokens", "finish"}


def chapter(slug):
    return (HANDBOOK / (slug or "index")).with_suffix(".md").read_text()


class WorkshopScheduleTests(unittest.TestCase):
    def test_quantity_regressions_are_generated_before_production_edits(self):
        skills = re.sub(r"\s+", " ", chapter("skills"))
        prompt = skills.split("## Generate the regression tests", 1)[1].split(
            "```copilot ", 1)[1].split("```", 1)[0]
        for text in ["Generate src/test/java/com/juliendubois/workshop/CartContractTest.java",
                     "acceptance criteria and test approach we just reviewed",
                     "existing JUnit and HTTP test fixtures",
                     "quantity limits and unchanged state after rejected input",
                     "Assert server-calculated totals",
                     "rather than copying teaching/CartContractTest.java",
                     "Do not change production code",
                     "wait for my review before running or committing"]:
            self.assertIn(text, prompt)
        self.assertIn("must fail on the unfixed application", skills)
        self.assertIn("do not expect a fixed count", skills)
        self.assertNotIn("Expect **3 tests, 2 failures**", skills)
        self.assertIn("4 baseline tests and all generated cart tests", chapter("verify"))
        for slug in ["generate", "tools", "parallel", "integrate", "subagents", "finish"]:
            with self.subTest(chapter=slug):
                self.assertNotRegex(chapter(slug), r"\b12 (?:supplied )?tests\b")

    def test_learner_maven_commands_keep_test_output_visible(self):
        for path in HANDBOOK.glob("*.md"):
            with self.subTest(chapter=path.name):
                self.assertNotRegex(path.read_text(),
                                    r"(?:\./mvnw|\.\\mvnw\.cmd)[^\n]*\s-q\b")

    def test_modes_explain_same_session_and_test_first_handoff(self):
        modes = re.sub(r"\s+", " ", chapter("modes"))
        steps = ["## Match autonomy to the task", "## Choose effort deliberately",
                 "## Plan the quantity fix",
                 "Switch to **Plan** in this same session",
                 "## Review the plan, then prepare to write tests",
                 "return to **Interactive**"]
        positions = [modes.index(text) for text in steps]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn("## Check permissions", modes)
        for text in ["**No new session or worktree is needed.**",
                     "| **Plan** |", "| **Interactive** |", "| **Autopilot** |",
                     "**do not start the whole implementation yet**",
                     "without implementing the plan",
                     "Production code stays unchanged"]:
            self.assertIn(text, modes)
        self.assertIn("in **Interactive** mode", chapter("skills"))
        self.assertIn("Now authorize the production-fix", chapter("verify"))

    def test_setup_explains_repository_instructions_before_running_commands(self):
        setup = re.sub(r"\s+", " ", chapter("setup"))
        steps = ["review `AGENTS.md`", "## Understand AGENTS.md",
                 "## Check the starter", "## Start the application"]
        positions = [setup.index(text) for text in steps]
        self.assertEqual(positions, sorted(positions))
        for text in ["Copilot loads applicable instructions automatically",
                     "does not run commands or grant tool permissions",
                     "run all currently activated tests",
                     "exact, working build, run and test commands",
                     "tests that need activation",
                     "Stay short and current",
                     "you don't need to edit them"]:
            self.assertIn(text, setup)

    def test_fix_requirements_are_introduced_when_planning(self):
        investigation = chapter("ticket")
        self.assertNotIn("## What the fix must achieve", investigation)
        self.assertIn("## Check the investigation", investigation)
        self.assertIn("No code should have changed yet.", investigation)
        modes = chapter("modes")
        steps = ["### Acceptance criteria",
                 "Switch to **Plan** in this same session", "```copilot"]
        positions = [modes.index(text) for text in steps]
        self.assertEqual(positions, sorted(positions))
        for text in ["quantity 2, total €20", "quantity 3 produces quantity 5",
                     "Quantities remain 1–99", "rejected input leaves state unchanged",
                     "Prices and totals come from the server",
                     "no checkout, stock management, accounts, new dependencies"]:
            self.assertIn(text, modes)
        self.assertIn("/workshops/copilot-app/modes/#acceptance-criteria",
                      chapter("skills"))
        self.assertIn("permalink: /workshops/copilot-app/modes/", modes)
        self.assertNotIn("/workshops/copilot-app/fusion/", modes)
        self.assertIn("Do not edit files yet; wait for my review.", modes)

    def test_workshop_amounts_use_euros_not_cent_amounts(self):
        for path in HANDBOOK.glob("*.md"):
            with self.subTest(chapter=path.name):
                text = path.read_text()
                self.assertNotRegex(text, r"\b\d+\s+cents\b")
                self.assertNotRegex(text, r"\$\d|\bUSD\b")
        for slug in ["ticket", "prompts", "skills", "subagents", "facilitator"]:
            with self.subTest(euro_examples=slug):
                self.assertIn("€20", chapter(slug))

    def test_chronicle_availability_is_checked_in_its_own_chapter(self):
        self.assertNotIn("/chronicle", chapter("setup"))
        tokens = chapter("tokens")
        steps = ["## Decide before analyzing history",
                 "## Open Chronicle if you opted in", "/chronicle",
                 "Check that the picker appears."]
        positions = [tokens.index(text) for text in steps]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("Chronicle not available.", tokens)

    def test_mcp_connection_is_deferred_to_runtime_exercise(self):
        setup = chapter("setup")
        self.assertNotIn("## Connect runtime tools", setup)
        self.assertNotIn("get_live_activity", setup)
        self.assertIn("MCP setup comes later", setup)
        tools = chapter("tools")
        steps = ["## Start the reviewed shop", "./mvnw spring-boot:run",
                 "## Connect runtime tools", "**Customize → MCP**",
                 '`query: "/api/cart"` and `limit: 1`',
                 "## Reproduce the same workload", "## Ask Copilot for evidence"]
        positions = [tools.index(text) for text in steps]
        self.assertEqual(positions, sorted(positions))
        self.assertIn('"url": "http://127.0.0.1:18765/bootui/api/mcp"', tools)
        self.assertIn('"tools": ["get_live_activity", "get_request_profile"]', tools)

    def test_setup_starts_session_before_naming_and_opening_files(self):
        setup = re.sub(r"\s+", " ", chapter("setup"))
        prompt = setup.split("```copilot ", 1)[1].split("```", 1)[0]
        for text in ["Analyze this project's tech stack",
                     "backend, frontend, database and test tooling",
                     "Do not edit files, install dependencies, start the application or call MCP tools."]:
            self.assertIn(text, prompt)
        steps = [
            "**model picker below the prompt box**",
            "Send this first prompt to start the session:",
            "Once the session has started, name the session **Cart: quantity bug**.",
            "**Open in...** menu at the **top right**",
            "review `AGENTS.md`",
        ]
        positions = [setup.index(text) for text in steps]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("open the session's working directory in your editor", setup)
        self.assertIn("under `.github/skills/` and `.github/mcp.json`", setup)

    def test_quantity_reproduction_waits_for_completed_requests(self):
        ticket = re.sub(r"\s+", " ", chapter("ticket"))
        for text in ["click **Reset cart**. Click", "button to re-enable",
                     "waiting for each request to finish"]:
            self.assertIn(text, ticket)
        self.assertIn("waiting for each response", chapter("prompts"))

    def test_instruction_permissions_are_staged_before_collaboration(self):
        canvas = re.sub(r"\s+", " ", chapter("canvas"))
        prompt = canvas.split("```copilot ", 1)[1].split("```", 1)[0]
        for text in ["only when its chapter is reached and approved",
                     "two isolated worktree tasks", "read-only independent critic",
                     "five bounded checkout subagents", "separate approval",
                     "publishing and merging", "wait for my approval"]:
            self.assertIn(text, prompt)
        self.assertIn("This amendment does not start those tasks", canvas)

    def test_boundary_regressions_have_separate_production_fix_ownership(self):
        parallel = re.sub(r"\s+", " ", chapter("parallel"))
        worker = parallel.split("### Cart: boundary tests", 1)[1].split(
            "```copilot ", 1)[1].split("```", 1)[0]
        for text in ['numeric 1.5 and string "one"', "HTTP 400",
                     "GET /api/cart and persisted state are unchanged",
                     "Only add CartBoundaryTest.java", "Do not fix application code"]:
            self.assertIn(text, worker)
        correction = parallel.split('id="boundary-fix"', 1)[1].split(
            "</details>", 1)[0]
        for text in ["existing **Cart: query investigation**",
                     "separate production-fix feature branch",
                     "outside `CartBoundaryTest.java`", "preserve all earlier reviewed tests",
                     "Do not include either worker's commit",
                     "own review, checks and merge approval",
                     "updated `origin/main`", "Do not proceed while",
                     "separately reviewed correction handoff"]:
            self.assertIn(text, correction)
        recovery = re.sub(r"\s+", " ", chapter("integrate").split(
            '<summary>Recovery:', 1)[1])
        self.assertIn("reviewed handoff only if missing", recovery)
        self.assertIn("do not implement a new fix in this test worker", recovery)

    def test_prompt_cards_follow_chapter_order_and_reference_bases_are_conditional(self):
        cards = chapter("prompts")
        self.assertEqual(re.findall(r"^## (.+)$", cards, re.MULTILINE), [
            "Investigate without editing", "Use the test skill", "Generate a feature",
            "Canvas and UI feedback", "Investigate through MCP", "Parallel worker cards",
            "Integrate with Agent Merge", "Rubber duck and subagent implementation",
            "Deliver checkout to main", "Improve usage", "Review the diff"])
        for slug in ["prompts", "rubber-duck", "finish"]:
            text = chapter(slug)
            self.assertIn("v2-start", text)
            for prompt in re.findall(r"```copilot\n(.*?)```", text, re.DOTALL):
                self.assertNotIn("v2-start", prompt)

    def test_cache_recovery_does_not_discard_design_records(self):
        canvas = re.sub(r"\s+", " ", chapter("canvas"))
        for text in ["untracked `.impeccable/hook.cache.json`",
                     "local Git exclude", "review it before approval",
                     "delete the whole directory or ignore all `.impeccable/`",
                     "Keep intentional design records"]:
            self.assertIn(text, canvas)

    def test_agent_evidence_and_empty_checkout_do_not_require_invented_activity(self):
        agents = re.sub(r"\s+", " ", chapter("subagents"))
        for text in ["concurrency limit", "during follow-ups as well as launches",
                     "receiving specialists check the actual upstream interface",
                     "**none exchanged**", "Do not manufacture dialogue",
                     "verify the required **409** through HTTP tests",
                     "do not enable it just for this demonstration"]:
            self.assertIn(text, agents)
        worksheet = chapter("worksheet")
        self.assertIn("none exchanged", worksheet)
        self.assertIn("**unknown** for concurrency", worksheet)
        self.assertIn("not the merged preparation PR", chapter("integrate"))

    def test_facilitator_keeps_visible_guidance_short_and_recovery_safe(self):
        facilitator = chapter("facilitator")
        body = facilitator.split("---", 2)[2]
        visible = re.sub(r"<details\b.*?</details>", "", body, flags=re.DOTALL)
        self.assertLess(len(re.findall(r"\b[\w'-]+\b", visible)), 900)
        self.assertEqual(body.count("<details"), 3)
        for text in ["## Before participants arrive",
                     "**before running Chronicle**",
                     "**three PRs targeting `main`**",
                     "**Cart: boundary tests**",
                     "checkout PR merged into `main`",
                     "## Recovery", "disable Agent Merge on open PRs",
                     "do not switch back to incomplete remote `main`",
                     "do not prove their generated checkout works"]:
            with self.subTest(visible_requirement=text):
                self.assertIn(text, visible)
        for text in ["restore the accepted Canvas instruction/UI changes",
                     "all 12 supplied tests pass before parallel work",
                     "participant's **own `main`**",
                     "changing\nthe remote alone does not make reference commits mergeable",
                     "Record that a reference solution was used",
                     "**not through the App**",
                     "{: #executable-checkpoints}",
                     "{: #recover-without-losing-work}"]:
            with self.subTest(recovery_requirement=text):
                self.assertIn(text, facilitator)

    def test_investigation_continues_setup_session_without_creating_an_issue(self):
        investigation = chapter("ticket")
        self.assertIn("name the session **Cart: quantity bug**", chapter("setup"))
        for text in ["## Continue in your existing session",
                     "**Copilot App project session** named **Cart: quantity bug**",
                     "/workshops/copilot-app/setup/#open-it-in-copilot-app",
                     "**No new session or GitHub issue is needed.**",
                     "that session's composer"]:
            with self.subTest(session_guidance=text):
                self.assertIn(text, investigation)
        prompt = investigation.split("```copilot\n", 1)[1].split("```", 1)[0]
        for text in ["After resetting the cart", "quantity 1 and total €10",
                     "quantity 2\nand total €20", "Do not edit files yet"]:
            with self.subTest(investigation_prompt=text):
                self.assertIn(text, prompt)
        self.assertIn("exercise briefs, not GitHub issues", chapter(""))
        self.assertNotIn("## Give Copilot a useful ticket", investigation)

    def test_learning_focused_titles_match_menu_pages_and_next_links(self):
        navigation = (ROOT / "_data/copilot_workshop.yml").read_text()
        names = re.findall(r"^- title: (.+)$", navigation, re.MULTILINE)
        slugs = [value.strip('"').rstrip("/") for value in
                 re.findall(r"^  slug: (.*)$", navigation, re.MULTILINE)]
        titles = dict(zip(slugs, names))
        expected = {
            "setup": "Set up your App workspace",
            "ticket": "Investigate with Copilot",
            "modes": "Modes and effort",
            "skills": "Install and use skills",
            "verify": "Review and verify changes",
            "generate": "Generate and iterate",
            "canvas": "Canvas and Pick & polish",
            "tools": "Investigate runtime with MCP",
            "integrate": "Merge PRs with Agent Merge",
            "rubber-duck": "Review with rubber duck",
            "subagents": "Coordinate five subagents",
        }
        for slug, title in expected.items():
            with self.subTest(chapter=slug):
                self.assertEqual(titles[slug], title)
                metadata = chapter(slug).split("---", 2)[1]
                heading = re.search(r"^title: (.+)$", metadata, re.MULTILINE)
                self.assertEqual(heading.group(1), title)
        for index, slug in enumerate(SEQUENCE[:-1]):
            with self.subTest(next_link=slug or "index"):
                metadata = chapter(slug).split("---", 2)[1]
                following = re.search(r"^next_title: (.+)$", metadata, re.MULTILINE)
                self.assertEqual(following.group(1), titles[SEQUENCE[index + 1]])

    def test_skill_installation_is_visible_and_usage_has_a_copyable_prompt(self):
        skills = chapter("skills")
        self.assertIn("## What is a skill?", skills)
        self.assertIn("## Install skills in another project", skills)
        self.assertLess(skills.index("## Install skills in another project"),
                        skills.index("<details"))
        for text in ["No installation is needed for this workshop",
                     "Installation makes the skill available",
                     "Neither grants new tool permissions",
                     "keep its existing pinned copies unchanged",
                     "**Cart: quantity bug**", "```copilot\n/java-junit",
                     ".github/skills/java-junit/SKILL.md",
                     "report which guidance you loaded",
                     "gh skills install github/awesome-copilot java-junit --pin",
                     "{: #skills-are-already-installed}"]:
            with self.subTest(skills_requirement=text):
                self.assertIn(text, skills)
        for text in ["you don't need to paste them again",
                     "requirements to test assertions",
                     "propose regression",
                     "which assertions would check each requirement",
                     "Do not edit files or implement the fix yet."]:
            self.assertIn(text, skills)
        self.assertIn("```copilot\n/java-junit", chapter("prompts"))

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

    def test_overview_and_listing_cover_the_expanded_workshop(self):
        landing = chapter("")
        metadata = landing.split("---", 2)[1]
        listing = (ROOT / "conferences.html").read_text().split(
            "<h3>GitHub Copilot App</h3>", 1)[1].split("</article>", 1)[0]
        for text in ["Canvas", "rubber duck", "five subagents", "mock checkout"]:
            with self.subTest(summary_concept=text):
                self.assertIn(text, metadata)
                self.assertIn(text, listing)
        self.assertIn("One shop, four tickets", landing)
        self.assertIn("Mock means no real payments", landing)
        flow = landing.split("## Workshop flow", 1)[1].split("\n## ", 1)[0]
        links = re.findall(r"\]\(/workshops/copilot-app/([^)]*)\)", flow)
        slugs = [link.split("#", 1)[0].rstrip("/") for link in links]
        self.assertEqual(slugs, SEQUENCE[1:])

    def test_worksheet_records_follow_workshop_order(self):
        headings = re.findall(r"^## (.+)$", chapter("worksheet"), re.MULTILINE)
        self.assertEqual(headings, [
            "A small record for each ticket", "Canvas: one observed improvement",
            "MCP before and after", "Parallel handoff",
            "Agent Merge and integration", "Rubber duck: critique and decision",
            "Five subagents: mock-checkout implementation", "Chronicle: one better habit"])
        finish = chapter("finish")
        self.assertIn("startup instructions, Canvas UI changes", finish)
        self.assertIn("independent critique and checkout branch/commit", finish)

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
        for slug in ["setup", "verify", "generate", "canvas", "tools"]:
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
                ("canvas", "workshop-feature")]:
            with self.subTest(handoff=branch):
                self.assertIn(f"Create a branch {branch}", chapter(slug))
                self.assertIn("Do not replace an existing branch", chapter(slug))

    def test_canvas_preserves_startup_permissions_and_next_session_handoff(self):
        canvas = re.sub(r"\s+", " ", chapter("canvas"))
        for text in [
                "**Cart: remove item**", "Update AGENTS.md only",
                "human owns the one persistent server", "No payments or authentication",
                'blanket "no agents" restriction', "Only change src/main/resources/static/",
                "bundled impeccable skill", "**Pick & polish**",
                "If the selected interaction already works well",
                "Create a branch workshop-feature",
                "includes the quantity fix, removal feature and accepted Canvas changes",
                "Do not silently overwrite it"]:
            with self.subTest(requirement=text):
                self.assertIn(text, canvas)
        self.assertNotIn("Create a branch workshop-feature", chapter("generate"))
        self.assertIn("contains all those accepted changes", chapter("tools"))
        self.assertIn("plus the reviewed Canvas AGENTS.md", chapter("parallel"))
        self.assertIn("canvas-recovery", chapter("canvas"))

    def test_rubber_duck_is_read_only_and_corrections_need_a_branch(self):
        duck = re.sub(r"\s+", " ", chapter("rubber-duck"))
        for text in [
                "**Cart: boundary tests**", "/rubber-duck Review",
                "Do not edit files", "suggested correction",
                "actual critic", "normal follow-up feature branch",
                "before editing", "Any follow-up PR needs its own review and merge approval"]:
            with self.subTest(requirement=text):
                self.assertIn(text, duck)
        self.assertIn("not a completed five-agent run", chapter("subagents"))
        self.assertIn("do not commit", chapter("finish"))

    def test_subagents_implement_checkout_on_one_branch_with_owned_files(self):
        agents = re.sub(r"\s+", " ", chapter("subagents"))
        for text in [
                "**Mock means no real payment processing**", "**Cart: boundary tests**",
                "exactly five subagents", "Order model", "Checkout service",
                "REST API", "UI", "Acceptance tests",
                "/fleet Implement the approved", "Read AGENTS.md",
                "Create and switch to a new branch workshop-checkout",
                "Do not replace an existing branch",
                "Workers edit only assigned files", "Workers must not run Maven",
                "further nested agents", "otherwise relay",
                "five actual contributions", "Wait for my review before committing",
                "failure leaves it intact", "Concurrent submissions",
                "No payments, authentication", "**example exchange**",
                "scheduled in smaller batches"]:
            with self.subTest(requirement=text):
                self.assertIn(text, agents)
        for slug in ["worksheet", "finish"]:
            with self.subTest(handoff_page=slug):
                self.assertNotIn("planned, not implemented", chapter(slug))
                self.assertIn("checkout feature branch", chapter(slug))
        self.assertLess(agents.index("Prepare one feature branch"),
                        agents.index("/fleet Implement"))
        self.assertLess(agents.index("Show the plan and wait for my approval"),
                        agents.index("/fleet Implement"))
        self.assertLess(SEQUENCE.index("parallel"), SEQUENCE.index("rubber-duck"))
        self.assertLess(SEQUENCE.index("rubber-duck"), SEQUENCE.index("subagents"))

    def test_checkout_contract_verification_and_recovery_are_explicit(self):
        agents = re.sub(r"\s+", " ", chapter("subagents"))
        prompt = agents.split("/fleet Implement", 1)[1].split("```", 1)[0]
        for text in ["POST /api/orders", "UUID requestId", "201", "200",
                     "400", "409", "orderId, requestId, items, itemCount, totalCents",
                     "productId, name, priceCents, quantity, lineTotalCents",
                     "clear the cart atomically", "failure leaves it intact",
                     "Concurrent or later retries", "CheckoutContractTest",
                     "Validate requestId first", "return a stored order before",
                     "one-SELECT GET /api/cart budget"]:
            with self.subTest(copyable_contract=text):
                self.assertIn(text, prompt)
        for text in ["rollback", "snapshots", "concurrent duplicate",
                     "**€20**", "Then squash-merge this checkout PR into main",
                     "published reference checkpoints do not include checkout",
                     "record checkout as unfinished"]:
            with self.subTest(verification=text):
                self.assertIn(text, agents)
        for path in HANDBOOK.glob("*.md"):
            with self.subTest(page=path.name):
                self.assertNotIn("planning-only exercise", path.read_text())

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

    def test_parallel_prompts_are_inline_and_assigned_to_named_sessions(self):
        parallel = chapter("parallel")
        self.assertNotIn("/workshops/copilot-app/prompts/#parallel", parallel)
        self.assertIn("**Cart: query investigation**", parallel)
        self.assertIn("Both prompts are below", parallel)
        self.assertIn("These tasks touch different files", parallel)
        for heading, prompt in [
                ("### Cart: empty-state UX", "Only change src/main/resources/static/."),
                ("### Cart: boundary tests", "Only add CartBoundaryTest.java")]:
            section = parallel.split(heading, 1)[1].split("\n##", 1)[0]
            with self.subTest(session=heading):
                self.assertIn("session's composer" if "UX" in heading
                              else "its composer", section)
                self.assertIn(prompt, section)
                self.assertIn("shared updated origin/main", section)
                self.assertIn("Stop if it does not match", section)
                self.assertIn("Do not open or merge a PR yet", section)
        self.assertIn("Do not fix application code or weaken an assertion", parallel)
        cards = chapter("prompts")
        for anchor in ["ui-worker", "test-worker"]:
            self.assertIn(f"/workshops/copilot-app/parallel/#{anchor}", cards)

    def test_main_is_reviewed_and_updated_before_parallel_workers(self):
        parallel = chapter("parallel")
        prose = re.sub(r"\s+", " ", parallel)
        for text in [
                "**three completed tickets into `main` through one reviewed PR**",
                "open one PR targeting main",
                "Do not push directly to main or merge the PR yet",
                "**Do not start the workers until the PR is Merged.**",
                "**`main` as the base branch** for both",
                "**do not have both edit `main` directly**",
                "main not updated: local recovery used"]:
            with self.subTest(requirement=text):
                self.assertIn(text, prose)
        self.assertLess(parallel.index("## Bring the reviewed work into main"),
                        parallel.index("## Start two tasks from updated main"))
        self.assertLess(parallel.index("Confirm GitHub reports the PR as Merged"),
                        parallel.index("### Cart: empty-state UX"))
        for path in HANDBOOK.glob("*.md"):
            with self.subTest(page=path.name):
                self.assertNotIn("workshop-complete", path.read_text())

    def test_integration_uses_sequential_agent_merge_with_correct_target(self):
        integration = chapter("integrate")
        prose = re.sub(r"\s+", " ", integration)
        for text in [
                "**Both worker PRs target `main`.**",
                "## Open the two worker PRs",
                "## Merge the UI PR first",
                "## Check the UI merge",
                "## Update and merge the test PR",
                "## Verify the combined application",
                "Leave the test PR's Agent Merge off.",
                "**Done when:** the UI PR's status is **Merged**",
                "**all earlier reviewed tests plus the new boundary",
                "all required checks and approvals pass",
                "Do not reset main or this branch"]:
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
                "Stay in **Cart: boundary tests**.",
                "**Base** means the branch receiving the changes",
                "**Head** means the worker branch supplying the changes",
                "branch tip equals its reviewed handoff commit",
                "leave **Merge pull request** unchecked",
                "check out the exact latest origin/main commit for verification",
                "Confirm the checked-out commit equals origin/main",
                "actual merged results, including squash merges",
                "fresh CI for its new revision",
                "may make further permitted repairs and merge without another review pause",
                "A denied permission",
                "If remote status is unavailable, mark it unknown"]:
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

    def test_verification_and_recovery_reuse_the_test_worker_session(self):
        for path in HANDBOOK.glob("*.md"):
            with self.subTest(page=path.name):
                self.assertNotIn("Cart: integration", path.read_text())
        integration = chapter("integrate")
        self.assertNotIn("## Open a session", integration)
        recovery = re.sub(r"\s+", " ", integration.split(
            '<summary>Recovery:', 1)[1])
        for text in [
                "Stay in **Cart: boundary tests**",
                "merge origin/main into this test worker branch",
                "keeping its boundary tests",
                "do not replace it with starter main",
                "mark it unknown",
                "accounting for squash merges",
                "Do not merge the test branch into itself",
                "Skip the normal-path checkout of `origin/main`"]:
            with self.subTest(requirement=text):
                self.assertIn(text, recovery)

    def test_agent_merge_prerequisites_recovery_and_handoff_are_consistent(self):
        setup = chapter("setup")
        for text in ["GitHub Actions", "PRs", "Agent Merge",
                     "default settings", "ask the facilitator"]:
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
        self.assertIn("**three PRs targeting `main`**", chapter("facilitator"))
        finish = chapter("finish")
        self.assertIn("all three earlier PR links", finish)
        self.assertIn("both worker PRs landed on **`main`**", finish)
        self.assertNotIn("## Optional GitHub delivery", finish)
        self.assertNotIn("No remote PR is required", finish)

    def test_checkout_delivery_belongs_to_orchestrator_under_scoped_approval(self):
        agents = re.sub(r"\s+", " ", chapter("subagents"))
        delivery = agents.split("## Deliver checkout into main", 1)[1].split(
            "## Verify the merged application", 1)[0]
        for text in [
                "one checkout PR", "not five specialist PRs or another App session",
                "I approve this reviewed checkout result",
                "the five workers must not publish or merge",
                "all five workers have finished and none can still modify this worktree",
                "preparation and both worker PRs are merged",
                "base main and head this branch",
                "repository, head and base match",
                "not the earlier merged boundary-test PR",
                "Do not reopen or retarget earlier PRs or create duplicate PRs",
                "current PR head", "Missing, skipped, queued or failed checks",
                "Then squash-merge this checkout PR into main under this approval",
                "Do not push directly to main, bypass protections",
                "stop and report unavailable required approval"]:
            with self.subTest(delivery_requirement=text):
                self.assertIn(text, delivery)
        self.assertLess(agents.index("Wait for my review before committing"),
                        agents.index("I approve this reviewed checkout result"))
        for slug in ["index", "finish", "worksheet", "facilitator", "prompts"]:
            with self.subTest(surface=slug):
                self.assertIn("checkout PR", chapter(slug))
                self.assertNotIn("checkout PR is optional", chapter(slug))
        canvas = re.sub(r"\s+", " ", chapter("canvas"))
        self.assertIn("only the orchestrator may publish and merge", canvas)
        self.assertIn("after separate explicit approval", canvas)

    def test_checkout_verification_uses_merged_main_and_correct_running_copy(self):
        agents = re.sub(r"\s+", " ", chapter("subagents"))
        verification = agents.split("## Verify the merged application", 1)[1]
        for text in [
                "checkout PR is Merged", "exact merged revision on main",
                "latest origin/main commit", "accounting for squash merges",
                "stop without overwriting unfinished work",
                "detached verification checkout",
                "Do not move another worktree, reset branches, delete refs or edit",
                "checked-out commit equals origin/main",
                "If main has advanced", "passing checks for this revision too",
                "all earlier reviewed tests, boundary tests and new checkout tests",
                "absolute directory and shop URL",
                "Ctrl+C in its owning terminal", "Opening a canvas",
                "does not replace a running server",
                "app running from the verified main revision demonstrates checkout"]:
            with self.subTest(verification_requirement=text):
                self.assertIn(text, verification)
        self.assertLess(verification.index("stop without overwriting unfinished work"),
                        verification.index("Check out the exact latest origin/main"))
        self.assertIn("/subagents/#verify-merged-checkout", chapter("prompts"))

    def test_checkout_blockers_and_postdelivery_edits_are_not_silent_success(self):
        for slug in ["subagents", "finish", "worksheet", "facilitator"]:
            text = re.sub(r"\s+", " ", chapter(slug))
            for state in ["verified locally; delivery blocked",
                          "merged; post-merge verification blocked"]:
                with self.subTest(surface=slug, state=state):
                    self.assertIn(state, text)
        agents = re.sub(r"\s+", " ", chapter("subagents"))
        self.assertIn("Do not publish a recovered combined branch", agents)
        self.assertIn("Do not substitute a direct push or local merge", agents)
        tokens = re.sub(r"\s+", " ", chapter("tokens"))
        for text in ["Record it as a suggestion", "do not edit the verified main checkout",
                     "new follow-up feature branch",
                     "own review, publishing/merge approval, PR and verification"]:
            self.assertIn(text, tokens)
        finish = re.sub(r"\s+", " ", chapter("finish"))
        self.assertIn("new follow-up feature branch", finish)
        self.assertIn("reuse the merged checkout PR", finish)
        self.assertIn("do not create another commit just to finish", finish)

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
