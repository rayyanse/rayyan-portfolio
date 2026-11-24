"""Checks the homepage Person schema and llms.txt against the build data.

    python tests/test_seo_files.py      (run after tools/build_pages.py)
"""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import build_pages as bp  # noqa: E402


def json_ld(html: str) -> list:
    return [json.loads(m) for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]


def person(blocks: list) -> dict:
    for b in blocks:
        for node in b.get("@graph", [b]):
            if node.get("@type") == "Person":
                return node
            if node.get("mainEntity", {}).get("@type") == "Person":
                return node["mainEntity"]
    raise AssertionError("no Person node")


class PersonSchema(unittest.TestCase):
    def test_homepage_and_about_share_the_same_profiles(self):
        for page in ("index.html", "about.html"):
            p = person(json_ld((ROOT / page).read_text(encoding="utf-8")))
            self.assertEqual(p["sameAs"], bp.SAME_AS, page)

    def test_profiles_are_https_and_unique(self):
        self.assertEqual(len(bp.SAME_AS), len(set(bp.SAME_AS)))
        for u in bp.SAME_AS:
            self.assertTrue(u.startswith("https://"), u)

    def test_homepage_names_the_voice_agent_niche(self):
        p = person(json_ld((ROOT / "index.html").read_text(encoding="utf-8")))
        self.assertIn("Urdu voice agents", p["knowsAbout"])
        self.assertIn("Urdu", p["description"])


class LlmsTxt(unittest.TestCase):
    text = (ROOT / "llms.txt").read_text(encoding="utf-8")

    def test_matches_the_build(self):
        self.assertEqual(self.text, bp.llms_txt())

    def test_starts_with_the_name_heading(self):
        self.assertTrue(self.text.startswith(f"# {bp.NAME}\n"))

    def test_every_linked_page_exists(self):
        for url in re.findall(r"\]\((https://rayyankhan\.dev[^)]*)\)", self.text):
            path = url.removeprefix(bp.SITE).lstrip("/") or "index"
            self.assertTrue((ROOT / f"{path}.html").exists(), url)

    def test_lists_every_service_and_case(self):
        for s in bp.SERVICES:
            self.assertIn(f"{bp.SITE}/{s['slug']})", self.text)
        for c in bp.CASES:
            self.assertIn(f"{bp.SITE}/work/{c['slug']})", self.text)


if __name__ == "__main__":
    unittest.main()
