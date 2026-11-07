"""Build the GitHub Pages site (index.html) and the Canvas paste version from src/body.html.

Usage:  python src/build.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://hilaryhavens.github.io/claude-code-setup-guide/"
body = (ROOT / "src" / "body.html").read_text(encoding="utf-8")

# ---------- GitHub Pages version ----------
CSS = """
:root{--ink:#1f1f1f;--muted:#5b5b5b;--accent:#c25e00;--rule:#e2ddd5;--code-bg:#f4f1ec;--bg:#fffdf9;--panel:#ffffff}
@media (prefers-color-scheme:dark){:root{--ink:#ece9e4;--muted:#b0aaa2;--accent:#ff9b3d;--rule:#3a3632;--code-bg:#26231f;--bg:#181614;--panel:#1f1c19}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.65 Georgia,"Times New Roman",serif}
main{max-width:820px;margin:0 auto;padding:40px 20px 80px}
h1{font-size:2.1rem;line-height:1.2;margin:0 0 .3rem}
h2{font-size:1.45rem;margin:2.6rem 0 .6rem;padding-top:.4rem;border-top:3px solid var(--accent)}
.byline{color:var(--muted);margin-top:0}
a{color:var(--accent)}
code{font:0.88em/1.4 Consolas,Menlo,monospace;background:var(--code-bg);padding:.1em .3em;border-radius:4px}
pre{background:var(--code-bg);padding:12px 14px;border-radius:6px;overflow-x:auto;border-left:4px solid var(--accent)}
pre code{background:none;padding:0;font-size:.9rem}
table{border-collapse:collapse;width:100%;margin:1rem 0;font-size:.95rem;display:block;overflow-x:auto}
th,td{border:1px solid var(--rule);padding:8px 10px;text-align:left;vertical-align:top}
th{background:var(--code-bg)}
figure{margin:1.2rem 0}
figure img{max-width:100%;height:auto;border:1px solid var(--rule);border-radius:6px;display:block}
figcaption{font-style:italic;color:var(--muted);font-size:.92rem;margin-top:.35rem}
blockquote{margin:.8rem 0;padding:10px 14px;background:var(--panel);border:1px solid var(--rule);border-left:4px solid var(--accent);border-radius:4px;font-family:Consolas,Menlo,monospace;font-size:.92rem}
ul.checklist{list-style:none;padding-left:0}
ul.checklist li::before{content:"\\2610  ";font-size:1.1em}
li{margin:.3rem 0}
"""

site = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Claude Code Setup Guide</title>
<meta name="description" content="Student guide to installing Claude Code, sandboxing it to a course folder, connecting GitHub, and publishing a first website.">
<style>{CSS}</style>
</head>
<body>
<main>
{body}
</main>
</body>
</html>
"""
(ROOT / "index.html").write_text(site, encoding="utf-8")

# ---------- Canvas version: inline styles only, absolute image URLs ----------
c = body
c = c.replace('src="images/', f'src="{SITE_URL}images/')
c = c.replace("<figure>", '<div style="margin:16px 0;">').replace("</figure>", "</div>")
c = c.replace("<figcaption>", '<p style="font-style:italic;color:#555;font-size:0.92em;margin-top:4px;">').replace("</figcaption>", "</p>")
c = re.sub(r"<img ", '<img style="max-width:100%;height:auto;border:1px solid #ddd;border-radius:6px;" ', c)
c = c.replace("<pre><code>", '<pre style="background:#f4f1ec;padding:12px 14px;border-left:4px solid #c25e00;border-radius:6px;overflow-x:auto;white-space:pre;"><code style="font-family:Consolas,Menlo,monospace;font-size:0.9em;">')
c = re.sub(r"<code>", '<code style="font-family:Consolas,Menlo,monospace;background:#f4f1ec;padding:1px 4px;border-radius:3px;">', c)
c = c.replace("<table>", '<table style="border-collapse:collapse;width:100%;margin:12px 0;">')
c = c.replace("<th>", '<th style="border:1px solid #ccc;padding:8px;background:#f4f1ec;text-align:left;vertical-align:top;">')
c = c.replace("<td>", '<td style="border:1px solid #ccc;padding:8px;text-align:left;vertical-align:top;">')
c = c.replace("<blockquote>", '<blockquote style="margin:10px 0;padding:10px 14px;border:1px solid #ddd;border-left:4px solid #c25e00;background:#fafafa;font-family:Consolas,Menlo,monospace;font-size:0.92em;">')
c = c.replace("<h2>", '<h2 style="border-top:3px solid #c25e00;padding-top:6px;margin-top:32px;">')
c = c.replace('<ul class="checklist">', '<ul style="list-style:none;padding-left:0;">')
c = re.sub(r'(<ul style="list-style:none;padding-left:0;">)(.*?)(</ul>)',
           lambda m: m.group(1) + m.group(2).replace("<li>", "<li>&#9744; ") + m.group(3), c, flags=re.S)
c = c.replace('<p class="byline">', '<p style="color:#555;">')
# Canvas pages supply their own title; drop the h1 so it is not duplicated.
c = re.sub(r"<h1>.*?</h1>\s*", "", c, flags=re.S)
note = (f'<p style="background:#fff4e8;border:1px solid #f0c9a0;padding:10px 14px;border-radius:6px;">'
        f'This guide is also available as a web page: <a href="{SITE_URL}">{SITE_URL}</a></p>\n')
(ROOT / "canvas-paste.html").write_text(note + c, encoding="utf-8")
print("built index.html and canvas-paste.html")
