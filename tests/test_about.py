"""Checks the generated /about page and the résumé against the files on disk.

    python tests/test_about.py      (run after tools/build_pages.py)
"""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import build_pages as bp  # noqa: E402


class AboutPage(unittest.TestCase):
    html = (ROOT / "about.html").read_text(encoding="utf-8")

    def test_every_internal_link_resolves_to_a_file(self):
        for href in set(re.findall(r'href="(/[^"#?]*)"', self.html)):
            if href == "/":
                continue
            p = ROOT / href.lstrip("/")
            self.assertTrue(p.exists() or p.with_suffix(".html").exists(), f"broken link {href}")

    def test_resume_pdf_exists_and_is_linked(self):
        self.assertTrue((ROOT / bp.RESUME_PDF.lstrip("/")).is_file())
        self.assertIn(f'href="{bp.RESUME_PDF}"', self.html)

    def test_every_role_is_on_the_page(self):
        for dates, title, company, *_ in bp.EXPERIENCE:
            self.assertIn(dates, self.html)
            self.assertIn(company.replace("&", "&amp;"), self.html)

    def test_only_the_first_role_is_current(self):
        current = [d for d, *_ in bp.EXPERIENCE if "Present" in d]
        self.assertEqual(current, [bp.EXPERIENCE[0][0]])

    def test_about_is_in_the_sitemap_and_nav(self):
        self.assertIn(f"{bp.SITE}/about<", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
        self.assertIn('href="/about"', (ROOT / "index.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
