"""Keep conceptual workshop illustrations accessible and separate from captures."""
from html.parser import HTMLParser
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
WORKSHOP = ROOT / "workshops/copilot-app"
SVG = "{http://www.w3.org/2000/svg}"
ILLUSTRATIONS = {
    "index": ("shop-to-checkout", 1440, 760),
    "ticket": ("quantity-bug", 1440, 800),
    "skills": ("skills-and-tests", 1440, 800),
    "canvas": ("canvas-focus", 1440, 800),
    "tools": ("mcp-query", 1440, 820),
    "parallel": ("parallel-worktrees", 1440, 820),
    "rubber-duck": ("rubber-duck-review", 1440, 800),
    "subagents": ("five-specialists", 1440, 1080),
    "tokens": ("chronicle-history-insights", 1440, 880),
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
        for chapter, (name, width, height) in ILLUSTRATIONS.items():
            with self.subTest(chapter=chapter):
                page = IllustrationImages((WORKSHOP / f"{chapter}.md").read_text())
                path = f"/workshops/copilot-app/assets/illustration-{name}.svg"
                self.assertEqual(len(page.images), 1)
                image = page.images[0]
                self.assertEqual(image["src"], path)
                self.assertTrue(image.get("alt", "").strip())
                self.assertEqual(image.get("width"), str(width))
                self.assertEqual(image.get("height"), str(height))
                self.assertEqual(image.get("loading"), "lazy")
                self.assertTrue(any(link.get("href") == path
                                    and link.get("target") == "_blank"
                                    for link in page.links))

    def test_svg_artwork_is_accessible_and_self_contained(self):
        for name, width, height in ILLUSTRATIONS.values():
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

    def test_only_the_selected_illustrations_are_published(self):
        expected = {f"illustration-{name}.svg"
                    for name, _, _ in ILLUSTRATIONS.values()}
        actual = {path.name for path in (WORKSHOP / "assets").glob("illustration-*")}
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
