"""Generate the AgntSpark brand files: SVG marks and logos, PNG sizes,
favicon.ico, the web app manifest icons and the social preview image.

    python3 brand/build.py          (needs fonttools; rsvg-convert and ImageMagick on PATH)

The wordmark and all text in the social image are converted to outlines from
Geist (SIL Open Font License), so none of the files depend on installed fonts.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import urllib.request

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent
PNG = HERE / "png"
FONTS = HERE / ".fonts"  # downloaded on demand, not committed

INK = "#141412"
PAPER = "#EEECE6"
SPARK = "#FF5A1F"
CREAM = "#FAF9F6"

FONT_URLS = {
    600: "https://fonts.gstatic.com/s/geist/v5/gyBhhwUxId8gMGYQMKR3pzfaWI_RQuQ4nQ.ttf",
    400: None,  # filled from the Google Fonts CSS API below
}

# ── The mark: an A whose crossbar is a spark, on a 32-unit grid ──────────────
A_PATH = "M5.5 27.5 L16 5 L26.5 27.5"
SPARK_PATH = "M16 13.8 Q16.7 19.3 22.2 20 Q16.7 20.7 16 26.2 Q15.3 20.7 9.8 20 Q15.3 19.3 16 13.8Z"


def mark_group(a_color: str) -> str:
    return (
        f'<path d="{A_PATH}" fill="none" stroke="{a_color}" stroke-width="4" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="{SPARK_PATH}" fill="{SPARK}"/>'
    )


def svg(width: float, height: float, body: str, view: str | None = None) -> str:
    view = view or f"0 0 {width:g} {height:g}"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:g}" height="{height:g}" '
        f'viewBox="{view}">{body}</svg>\n'
    )


# ── Fonts ────────────────────────────────────────────────────────────────────
def font(weight: int) -> TTFont:
    FONTS.mkdir(exist_ok=True)
    path = FONTS / f"Geist-{weight}.ttf"
    if not path.exists():
        url = FONT_URLS.get(weight)
        if url is None:
            css = urllib.request.urlopen(
                f"https://fonts.googleapis.com/css2?family=Geist:wght@{weight}"
            ).read().decode()
            url = css.split("url(")[1].split(")")[0]
        path.write_bytes(urllib.request.urlopen(url).read())
    return TTFont(path)


def text_path(fnt: TTFont, text: str, size: float, x: float, baseline: float, tracking_em: float) -> tuple[str, float]:
    """SVG path data for `text` set at `size` px from (x, baseline); returns (d, advance)."""
    glyphs = fnt.getGlyphSet()
    cmap = fnt.getBestCmap()
    hmtx = fnt["hmtx"]
    scale = size / fnt["head"].unitsPerEm
    pen = SVGPathPen(glyphs)
    cursor = x
    for i, ch in enumerate(text):
        name = cmap[ord(ch)]
        tpen = TransformPen(pen, (scale, 0, 0, -scale, cursor, baseline))
        glyphs[name].draw(tpen)
        cursor += hmtx[name][0] * scale
        if i < len(text) - 1:
            cursor += tracking_em * size
    return pen.getCommands(), cursor - x


def cap_height(fnt: TTFont, size: float) -> float:
    return fnt["OS/2"].sCapHeight * size / fnt["head"].unitsPerEm


# ── Builders ─────────────────────────────────────────────────────────────────
def build_marks() -> dict[str, str]:
    files = {
        "agntspark-mark.svg": svg(32, 32, mark_group(INK)),
        "agntspark-mark-light.svg": svg(32, 32, mark_group(PAPER)),
        "agntspark-icon.svg": svg(32, 32, f'<rect width="32" height="32" rx="7.5" fill="{INK}"/>' + mark_group(PAPER)),
        # Full-bleed square for places that apply their own mask (social avatars, app stores).
        "agntspark-icon-square.svg": svg(32, 32, f'<rect width="32" height="32" fill="{INK}"/>'
                                         f'<g transform="translate(3.2 3.2) scale(.8)">{mark_group(PAPER)}</g>'),
    }
    for name, content in files.items():
        (HERE / name).write_text(content)
    return files


def build_logos(bold: TTFont) -> None:
    mark_h = 64.0
    size = 56.0
    gap = 15.0
    baseline = mark_h / 2 + cap_height(bold, size) / 2
    d, advance = text_path(bold, "AgntSpark", size, mark_h + gap, baseline, -0.03)
    width = round(mark_h + gap + advance + 2)
    scale = mark_h / 32
    for name, a_color, text_color in (
        ("agntspark-logo.svg", INK, INK),
        ("agntspark-logo-light.svg", PAPER, PAPER),
    ):
        body = f'<g transform="scale({scale:g})">{mark_group(a_color)}</g><path d="{d}" fill="{text_color}"/>'
        (HERE / name).write_text(svg(width, mark_h, body))


def build_social(bold: TTFont, regular: TTFont) -> None:
    w, h = 1200, 630
    parts = [f'<rect width="{w}" height="{h}" fill="{CREAM}"/>']
    # faint grid, echoing the site's technical feel
    for gx in range(0, w + 1, 60):
        parts.append(f'<path d="M{gx} 0V{h}" stroke="#E9E6DF" stroke-width="1"/>')
    for gy in range(0, h + 1, 60):
        parts.append(f'<path d="M0 {gy}H{w}" stroke="#E9E6DF" stroke-width="1"/>')
    # icon + wordmark
    parts.append(f'<g transform="translate(96 108) scale(3.25)"><rect width="32" height="32" rx="7.5" fill="{INK}"/>{mark_group(PAPER)}</g>')
    d, _ = text_path(bold, "AgntSpark", 64, 234, 108 + 52 + cap_height(bold, 64) / 2, -0.03)
    parts.append(f'<path d="{d}" fill="{INK}"/>')
    # headline
    d1, _ = text_path(bold, "Put an AI agent on the internet.", 70, 96, 368, -0.035)
    d2, _ = text_path(bold, "Keep it private.", 70, 96, 456, -0.035)
    parts.append(f'<path d="{d1}" fill="{INK}"/><path d="{d2}" fill="{SPARK}"/>')
    # footer line
    d3, _ = text_path(regular, "Hosting for AI agents  ·  agntspark.com", 30, 96, 546, -0.01)
    parts.append(f'<path d="{d3}" fill="#6B6A64"/>')
    (HERE / "agntspark-social.svg").write_text(svg(w, h, "".join(parts)))


def build_x_header(bold: TTFont, regular: TTFont) -> None:
    """1500x500 profile header (X/Twitter, LinkedIn cover). The avatar covers
    the bottom-left, so the content sits on the right."""
    w, h = 1500, 500
    parts = [f'<rect width="{w}" height="{h}" fill="{INK}"/>']
    for gx in range(0, w + 1, 50):
        parts.append(f'<path d="M{gx} 0V{h}" stroke="#1D1D1B" stroke-width="1"/>')
    for gy in range(0, h + 1, 50):
        parts.append(f'<path d="M0 {gy}H{w}" stroke="#1D1D1B" stroke-width="1"/>')
    right = w - 110
    d1, a1 = text_path(bold, "Put an AI agent on the internet.", 58, 0, 0, -0.035)
    d2, a2 = text_path(bold, "Keep it private.", 58, 0, 0, -0.035)
    d3, a3 = text_path(regular, "Hosting for AI agents  ·  agntspark.com", 26, 0, 0, -0.01)
    for d, adv, y, color in ((d1, a1, 222, PAPER), (d2, a2, 296, SPARK), (d3, a3, 368, "#8F8C84")):
        parts.append(f'<g transform="translate({right - adv:.1f} {y})"><path d="{d}" fill="{color}"/></g>')
    parts.append(f'<g transform="translate({right - 64} 72) scale(2)">{mark_group(PAPER)}</g>')
    (HERE / "agntspark-header-1500x500.svg").write_text(svg(w, h, "".join(parts)))


def rsvg(src: pathlib.Path, dst: pathlib.Path, width: int, height: int | None = None) -> None:
    args = ["rsvg-convert", "-w", str(width)]
    if height:
        args += ["-h", str(height)]
    subprocess.run(args + [str(src), "-o", str(dst)], check=True)


def build_pngs() -> None:
    PNG.mkdir(exist_ok=True)
    for size in (16, 32, 48, 64, 128, 180, 192, 256, 512, 1024):
        rsvg(HERE / "agntspark-icon.svg", PNG / f"agntspark-icon-{size}.png", size, size)
    for size in (400, 1024):
        rsvg(HERE / "agntspark-icon-square.svg", PNG / f"agntspark-icon-square-{size}.png", size, size)
    for variant in ("mark", "mark-light"):
        for size in (256, 1024):
            rsvg(HERE / f"agntspark-{variant}.svg", PNG / f"agntspark-{variant}-{size}.png", size, size)
    for variant in ("logo", "logo-light"):
        for width in (600, 1200, 2400):
            rsvg(HERE / f"agntspark-{variant}.svg", PNG / f"agntspark-{variant}-{width}w.png", width)
    rsvg(HERE / "agntspark-social.svg", PNG / "agntspark-social-1200x630.png", 1200, 630)
    rsvg(HERE / "agntspark-header-1500x500.svg", PNG / "agntspark-header-1500x500.png", 1500, 500)


def build_site_icons() -> None:
    (SITE / "favicon.svg").write_text((HERE / "agntspark-icon.svg").read_text())
    subprocess.run(
        ["magick", str(PNG / "agntspark-icon-16.png"), str(PNG / "agntspark-icon-32.png"),
         str(PNG / "agntspark-icon-48.png"), str(SITE / "favicon.ico")],
        check=True,
    )
    for src, dst in (
        ("agntspark-icon-180.png", "apple-touch-icon.png"),
        ("agntspark-icon-192.png", "icon-192.png"),
        ("agntspark-icon-512.png", "icon-512.png"),
        ("agntspark-social-1200x630.png", "og-image.png"),
    ):
        (SITE / dst).write_bytes((PNG / src).read_bytes())
    manifest = {
        "name": "AgntSpark",
        "short_name": "AgntSpark",
        "description": "Hosting for AI agents — each with its own HTTPS endpoint, private by default.",
        "start_url": "/",
        "display": "browser",
        "background_color": CREAM,
        "theme_color": INK,
        "icons": [
            {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }
    (SITE / "site.webmanifest").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    bold, regular = font(600), font(400)
    build_marks()
    build_logos(bold)
    build_social(bold, regular)
    build_x_header(bold, regular)
    build_pngs()
    build_site_icons()
    print("brand files written to", HERE.relative_to(SITE), "and site root")


if __name__ == "__main__":
    main()
