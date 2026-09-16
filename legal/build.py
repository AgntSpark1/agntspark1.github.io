"""Build the legal pages (/terms, /privacy, /acceptable-use) from the Markdown here.

    python3 legal/build.py

Needs python-markdown. Edit the .md files, rebuild, and commit both.
"""

from __future__ import annotations

import html
import pathlib
import re

import markdown

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGES = {
    "terms": ("terms-of-service.md", "Terms of Service"),
    "privacy": ("privacy-policy.md", "Privacy Policy"),
    "acceptable-use": ("acceptable-use-policy.md", "Acceptable Use Policy"),
}

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — AgntSpark</title>
<meta name="description" content="{title} for AgntSpark, operated by AgntSpark LLC.">
<link rel="canonical" href="https://agntspark.com/{slug}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%23111'/%3E%3Cpath d='M16 5l2.6 8.4L27 16l-8.4 2.6L16 27l-2.6-8.4L5 16l8.4-2.6z' fill='%23FF5A1F'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {{ --bg:#FAF9F6; --bg-2:#F2F0EA; --card:#FFFFFF; --ink:#141412; --ink-2:#3D3C38; --muted:#6B6A64; --rule:#E4E1D9; --spark:#FF5A1F; --spark-ink:#C73D0A;
  --mono:"Geist Mono", ui-monospace, Menlo, monospace; --sans:"Geist", ui-sans-serif, -apple-system, "Segoe UI", sans-serif; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#0E0E0C; --bg-2:#151513; --card:#171715; --ink:#EEECE6; --ink-2:#C9C6BE; --muted:#8F8C84; --rule:#262522; --spark:#FF6B35; --spark-ink:#FF8A5C; }} }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ font-family:var(--sans); background:var(--bg); color:var(--ink); line-height:1.7; -webkit-font-smoothing:antialiased; }}
.wrap {{ max-width:1140px; margin:0 auto; padding:0 24px; }}
.nav {{ border-bottom:1px solid var(--rule); }}
.nav .wrap {{ display:flex; align-items:center; height:64px; gap:24px; }}
.brand {{ display:flex; align-items:center; gap:10px; font-weight:600; font-size:17px; text-decoration:none; color:var(--ink); }}
.brand svg {{ width:26px; height:26px; }}
.nav nav {{ margin-left:auto; display:flex; gap:20px; font-size:14.5px; }}
.nav nav a {{ color:var(--muted); text-decoration:none; }}
.nav nav a:hover, .nav nav a[aria-current] {{ color:var(--ink); }}
article {{ max-width:760px; margin:0 auto; padding:64px 24px 96px; }}
.kicker {{ font:500 12.5px/1 var(--mono); color:var(--spark-ink); text-transform:uppercase; letter-spacing:.08em; }}
article h1 {{ font-size:clamp(34px,4.5vw,48px); line-height:1.08; letter-spacing:-0.03em; font-weight:600; margin:14px 0 10px; }}
article h2 {{ font-size:22px; letter-spacing:-0.015em; font-weight:600; margin:44px 0 12px; padding-top:20px; border-top:1px solid var(--rule); }}
article p, article li {{ color:var(--ink-2); font-size:16px; }}
article p {{ margin:12px 0; }}
article ul {{ margin:10px 0 10px 22px; }}
article li {{ margin:6px 0; }}
article strong {{ color:var(--ink); font-weight:600; }}
article a {{ color:var(--spark-ink); text-underline-offset:3px; }}
article table {{ width:100%; border-collapse:collapse; margin:18px 0; font-size:14.5px; display:block; overflow-x:auto; }}
article th, article td {{ text-align:left; padding:10px 12px; border-bottom:1px solid var(--rule); vertical-align:top; color:var(--ink-2); }}
article th {{ font:500 12px/1.4 var(--mono); text-transform:uppercase; letter-spacing:.05em; color:var(--muted); background:var(--bg-2); }}
footer {{ border-top:1px solid var(--rule); padding:28px 0 36px; font-size:13.5px; color:var(--muted); }}
footer .wrap {{ display:flex; justify-content:space-between; gap:16px; flex-wrap:wrap; }}
footer a {{ color:inherit; text-decoration:none; margin-left:16px; }}
footer a:hover {{ color:var(--ink); }}
</style>
</head>
<body>
<!--email_off-->
<header class="nav">
  <div class="wrap">
    <a class="brand" href="/"><svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="7" fill="currentColor"/><path d="M16 5l2.6 8.4L27 16l-8.4 2.6L16 27l-2.6-8.4L5 16l8.4-2.6z" fill="#FF5A1F"/></svg>AgntSpark</a>
    <nav>{nav}</nav>
  </div>
</header>
<main>
<article>
<span class="kicker">Legal</span>
{body}
</article>
</main>
<footer>
  <div class="wrap">
    <span>© 2026 AgntSpark LLC · 30 N Gould St Ste N, Sheridan, WY 82801, USA · admin@agntspark.com</span>
    <span><a href="/">Home</a><a href="/terms">Terms</a><a href="/privacy">Privacy</a><a href="/acceptable-use">Acceptable use</a></span>
  </div>
</footer>
<!--/email_off-->
</body>
</html>
"""


def link_emails(rendered: str) -> str:
    return re.sub(
        r"(?<![\w@/.:-])(admin@agntspark\.com)(?![\w.-]*</a>)",
        r'<a href="mailto:\1">\1</a>',
        rendered,
    )


def main() -> None:
    here = pathlib.Path(__file__).resolve().parent
    for slug, (source, title) in PAGES.items():
        text = (here / source).read_text()
        body = markdown.markdown(text, extensions=["tables", "sane_lists"])
        body = link_emails(body)
        nav = "".join(
            f'<a href="/{s}"{" aria-current=\"page\"" if s == slug else ""}>{html.escape(t)}</a>'
            for s, (_, t) in PAGES.items()
        )
        out = ROOT / slug / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(TEMPLATE.format(title=html.escape(title), slug=slug, nav=nav, body=body))
        print("built", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
