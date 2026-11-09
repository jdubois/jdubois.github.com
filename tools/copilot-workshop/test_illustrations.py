"""Keep conceptual workshop illustrations accessible and separate from captures."""
from html.parser import HTMLParser
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
WORKSHOP = ROOT / "workshops/copilot-app"
SVG = "{http://www.w3.org/2000/svg}"
ILLUSTRATIONS = {
    "index": (
        ("learning-with-a-real-project", 1440, 820, "eager"),
        ("shop-to-checkout", 1440, 760, "lazy"),
    ),
    "ticket": (("quantity-bug", 1440, 800, "lazy"),),
    "skills": (("skills-and-tests", 1440, 800, "lazy"),),
    "canvas": (("canvas-focus", 1440, 800, "lazy"),),
    "tools": (("mcp-query", 1440, 820, "lazy"),),
    "parallel": (("parallel-worktrees", 1440, 820, "lazy"),),
    "rubber-duck": (("rubber-duck-review", 1440, 800, "lazy"),),
    "subagents": (("five-specialists", 1440, 1080, "lazy"),),
    "tokens": (("chronicle-history-insights", 1440, 880, "lazy"),),
}


class IllustrationImages(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.images = []
        self.links = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "img" and "/illustration-" in attrs.get("src", ""):
            self.images.append(attrs)
        if tag == "a":
            self.links.append(attrs)


class WorkshopIllustrationsTest(unittest.TestCase):
    def test_selected_artwork_is_linked_from_the_matching_chapter(self):
        for chapter, illustrations in ILLUSTRATIONS.items():
            with self.subTest(chapter=chapter):
                page = IllustrationImages((WORKSHOP / f"{chapter}.md").read_text())
                self.assertEqual(len(page.images), len(illustrations))
                for image, (name, width, height, loading) in zip(page.images, illustrations):
                    with self.subTest(illustration=name):
                        path = f"/workshops/copilot-app/assets/illustration-{name}.svg"
                        self.assertEqual(image["src"], path)
                        self.assertTrue(image.get("alt", "").strip())
                        self.assertEqual(image.get("width"), str(width))
                        self.assertEqual(image.get("height"), str(height))
                        self.assertEqual(image.get("loading"), loading)
                        self.assertTrue(any(link.get("href") == path
                                            and link.get("target") == "_blank"
                                            for link in page.links))

    def test_overview_introduction_precedes_the_scenario(self):
        source = (WORKSHOP / "index.md").read_text()
        self.assertLess(source.index("illustration-learning-with-a-real-project.svg"),
                        source.index("## The scenario"))
        images = IllustrationImages(source).images
        self.assertEqual(images[0].get("fetchpriority"), "high")

    def test_svg_artwork_is_accessible_and_self_contained(self):
        for name, width, height, _ in (
                illustration for chapter in ILLUSTRATIONS.values() for illustration in chapter):
            with self.subTest(illustration=name):
                root = ET.parse(WORKSHOP / "assets" / f"illustration-{name}.svg").getroot()
                self.assertEqual(root.tag, SVG + "svg")
                self.assertEqual(root.get("viewBox"), f"0 0 {width} {height}")
                self.assertEqual(root.get("role"), "img")
                elements = {element.get("id"): element for element in root.iter()
                            if element.get("id")}
                labels = root.get("aria-labelledby", "").split()
                self.assertEqual(len(labels), 2)
                self.assertEqual([elements[label].tag for label in labels],
                                 [SVG + "title", SVG + "desc"])
                self.assertTrue(all("".join(elements[label].itertext()).strip()
                                    for label in labels))
                for element in root.iter():
                    self.assertNotIn(element.tag, (SVG + "script", SVG + "foreignObject"))
                    for attr, value in element.attrib.items():
                        self.assertFalse(attr.lower().startswith("on"))
                        if attr.split("}")[-1] == "href":
                            self.assertTrue(value.startswith("#"), value)
                            self.assertIn(value[1:], elements)

    def test_parallel_diagram_allows_overlapping_files(self):
        root = ET.parse(
            WORKSHOP / "assets/illustration-parallel-worktrees.svg").getroot()
        description = root.find(SVG + "desc").text
        self.assertIn("may edit the same files", description)
        self.assertIn("Agent Merge reconciles updated main and any conflicts", description)
        self.assertNotIn("owns", description)
        labels = " ".join(element.text or "" for element in root.iter(SVG + "text"))
        self.assertIn("overlapping files are allowed", labels)
        self.assertNotIn("Independent files", labels)

    def test_only_the_selected_illustrations_are_published(self):
        expected = {f"illustration-{name}.svg"
                    for chapter in ILLUSTRATIONS.values()
                    for name, _, _, _ in chapter}
        actual = {path.name for path in (WORKSHOP / "assets").glob("illustration-*")}
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
