"""Build the résumé PDF linked from /about.

    python tools/build_resume.py

Reads the career data in build_pages.py (EXPERIENCE, EDUCATION, SKILLS, SUMMARY), so the PDF and the
/about page never disagree. Renders a plain A4 HTML résumé and prints it to PDF with headless
Microsoft Edge or Chrome (set BROWSER to override the path). The PDF keeps real text, so applicant
tracking systems can read it.

Writes agha-muhammad-rayyan-khan-resume.pdf at the site root; tools/resume.html is the printable
source and is overwritten each run.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from html import escape as e
from pathlib import Path

import build_pages as bp

ROOT = bp.ROOT
OUT_HTML = ROOT / "tools" / "resume.html"
OUT_PDF = ROOT / bp.RESUME_PDF.lstrip("/")
# Flagship projects on the résumé, in this order.
RESUME_CASES = ["call-stream", "jennifer", "al-munir", "sebastian"]
BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium", "microsoft-edge",
]

CSS = """
@page{size:A4;margin:14mm 15mm}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',Inter,Arial,sans-serif;font-size:9.6pt;line-height:1.42;color:#0B0F19}
a{color:inherit;text-decoration:none}
header{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;padding-bottom:9px;border-bottom:1.4pt solid #0B0F19}
h1{font-size:20pt;letter-spacing:-.02em;line-height:1.1}
.role{font-size:10.5pt;color:#434A5A;margin-top:3px}
.contact{text-align:right;font-size:8.6pt;color:#434A5A;line-height:1.55}
.summary{margin-top:10px;color:#2A303C}
h2{font-size:8.4pt;letter-spacing:.12em;text-transform:uppercase;color:#434A5A;margin:14px 0 6px;padding-bottom:3px;border-bottom:.6pt solid #C9CED8}
.job{margin-bottom:8px;break-inside:avoid}
.job-top{display:flex;justify-content:space-between;gap:12px}
.job-top b{font-size:10pt}
.when{font-size:8.6pt;color:#5C6370;white-space:nowrap}
.co{color:#434A5A;font-size:9pt}
ul{margin:3px 0 0 14px}
li{margin-top:1.5px}
.skills div{margin-bottom:2.5px}
.skills b{display:inline-block;min-width:92px}
.proj{margin-bottom:6px;break-inside:avoid}
.proj b{font-size:9.8pt}
.stack{color:#5C6370;font-size:8.6pt}
"""


def render() -> str:
    jobs = "".join(f"""<div class="job"><div class="job-top"><b>{e(t)}</b><span class="when">{e(d)}</span></div>
<div class="co">{e(co)} · {e(place)}</div><ul>{''.join(f'<li>{e(b)}</li>' for b in bullets)}</ul></div>"""
                   for d, t, co, place, bullets, _ in bp.EXPERIENCE)
    projs = "".join(f"""<div class="proj"><b>{e(bp.CASE_BY[s]['name'])}</b> · <a href="{bp.SITE}/work/{s}">rayyankhan.dev/work/{s}</a>
<div>{e(bp.CASE_BY[s]['description'])}</div><div class="stack">{e(' · '.join(bp.CASE_BY[s]['chips']))}</div></div>"""
                    for s in RESUME_CASES)
    skills = "".join(f"<div><b>{e(g)}</b>{e(', '.join(items))}</div>" for g, items in bp.SKILLS)
    edu = "".join(f"""<div class="job"><div class="job-top"><b>{e(t)}</b><span class="when">{e(d)}</span></div>
<div class="co">{e(w)}</div>{f'<div>{e(n)}</div>' if n else ''}</div>""" for d, t, w, n in bp.EDUCATION)
    phone = bp.PHONE
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>{e(bp.NAME)} résumé</title><style>{CSS}</style></head><body>
<header><div><h1>{e(bp.NAME)}</h1><div class="role">{e(bp.ROLE)} · Lahore, Pakistan · open to remote</div></div>
<div class="contact"><a href="mailto:{bp.EMAIL}">{bp.EMAIL}</a> · {phone}<br><a href="{bp.SITE}">rayyankhan.dev</a> · <a href="https://www.linkedin.com/in/rayyan45/">linkedin.com/in/rayyan45</a><br><a href="https://github.com/rayyanse">github.com/rayyanse</a></div></header>
<p class="summary">{e(bp.SUMMARY)}</p>
<h2>Experience</h2>{jobs}
<h2>Selected projects</h2>{projs}
<p class="stack">{len(bp.PROJECTS)} systems in total, most with a walkthrough film: rayyankhan.dev/projects</p>
<h2>Skills</h2><div class="skills">{skills}</div>
<h2>Education</h2>{edu}
</body></html>"""


def find_browser() -> str:
    for b in [os.environ.get("BROWSER", "")] + BROWSERS:
        if b and (Path(b).is_file() or shutil.which(b)):
            return b
    sys.exit("No Edge or Chrome found. Set BROWSER to the browser's path and run again.")


def main() -> None:
    OUT_HTML.write_text(render(), encoding="utf-8")
    browser = find_browser()
    cmd = [browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
           f"--print-to-pdf={OUT_PDF}", OUT_HTML.resolve().as_uri()]
    before = OUT_PDF.stat().st_mtime if OUT_PDF.exists() else 0
    run = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if run.returncode != 0 or not OUT_PDF.exists() or OUT_PDF.stat().st_mtime == before:
        sys.exit(f"PDF print failed (exit {run.returncode}): {run.stderr.strip()[:500]}")
    print(f"wrote {OUT_PDF.name} ({OUT_PDF.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
