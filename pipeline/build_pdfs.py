"""Build one print-formatted PDF per language edition of a Cribrum issue page.

Usage:
    python pipeline/build_pdfs.py docs/issues/YYYY-MM-DD/index.html

The issue page holds the three editions between <!-- edition:xx --> and
<!-- /edition --> markers. The PDFs are written next to the page as
Cribrum_YYYY-MM-DD_EN.pdf, _FR.pdf and _ES.pdf.

Requirements: Python 3 and Playwright with Chromium
(pip install playwright && playwright install chromium).
The typefaces are downloaded once from the Google Fonts repository
into pipeline/.fonts/.
"""
import re
import sys
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

FONT_FILES = {
    "BodoniModa.ttf": "ofl/bodonimoda/BodoniModa%5Bopsz%2Cwght%5D.ttf",
    "SourceSerif4.ttf": "ofl/sourceserif4/SourceSerif4%5Bopsz%2Cwght%5D.ttf",
    "SourceSerif4-Italic.ttf": "ofl/sourceserif4/SourceSerif4-Italic%5Bopsz%2Cwght%5D.ttf",
    "LibreFranklin.ttf": "ofl/librefranklin/LibreFranklin%5Bwght%5D.ttf",
}
FONT_BASE = "https://raw.githubusercontent.com/google/fonts/main/"

PRINT_CSS = """
@page{size:Letter;margin:12mm 13mm 15mm 13mm}
:root,:root[data-theme]{--paper:#FFFFFF;--ink:#141414;--ink-2:#3A3936;--rule:#141414;--hair:#BDB6A6;--photo:#E6E0D2;--accent:#8A1C1C;--link:#6E1A1A;color-scheme:light}
html,body{background:#FFFFFF}
body{margin:0;font-size:9.5pt;line-height:1.45;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{max-width:none;padding:0;margin:0}
.langs,.pdf-link,footer nav{display:none}
.label{font-size:7pt}
.bar{padding-block:4pt}
.masthead{font-size:64pt;margin:8pt 0 0}
.tagline{font-size:11.5pt;margin:2pt 0 8pt}
.front{flex-wrap:nowrap;gap:16pt;margin-top:12pt}
.lead{flex:2.15 1 0}
aside{flex:1 1 0;padding-top:8pt}
.kicker{font-size:7pt}
.lead h2{font-size:24pt;margin:4pt 0 6pt}
.deck{font-size:11.5pt;margin-bottom:6pt}
.byline{margin-bottom:8pt}
figure{margin:0 0 8pt}
figcaption{font-size:8pt;margin-top:4pt}
.cols{column-count:2;column-width:auto;column-gap:14pt;font-size:9.6pt;line-height:1.45}
.cols p{margin:0 0 6pt}
.cols > p:first-child::first-letter{font-size:38pt;padding:3pt 5pt 0 0}
.sub{font-size:7.5pt;margin:8pt 0 4pt}
.sources{font-size:7pt;margin-top:4pt}
aside h2{font-size:16pt}
aside .label{margin-bottom:8pt}
.dropped{gap:7pt}
.dropped p,.note p{font-size:9pt;line-height:1.45}
.note{margin-top:10pt;padding-top:8pt}
.note h3{font-size:7.5pt}
.deck3{grid-template-columns:repeat(3,minmax(0,1fr));gap:14pt;margin-top:14pt;padding-top:10pt}
.deck3 h2{font-size:13.5pt;margin:4pt 0 6pt}
.deck3 p{font-size:9.2pt;margin:0 0 6pt}
.deck3 article{break-inside:avoid}
footer{margin-top:14pt;padding-top:8pt;font-size:7.5pt}
a{text-decoration:none}
"""


def ensure_fonts(folder: Path) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    for name, path in FONT_FILES.items():
        target = folder / name
        if not target.exists():
            urllib.request.urlretrieve(FONT_BASE + path, target)
    return folder


def font_css(folder: Path) -> str:
    def face(family, file, weights, style="normal"):
        return (f"@font-face{{font-family:'{family}';src:url('{(folder / file).as_uri()}') "
                f"format('truetype');font-weight:{weights};font-style:{style}}}")
    return "".join([
        face("Bodoni Moda", "BodoniModa.ttf", "400 900"),
        face("Source Serif 4", "SourceSerif4.ttf", "200 900"),
        face("Source Serif 4", "SourceSerif4-Italic.ttf", "200 900", "italic"),
        face("Libre Franklin", "LibreFranklin.ttf", "100 900"),
    ])


def strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).replace("&nbsp;", " ").strip()


def main(page_path: Path) -> None:
    html = page_path.read_text(encoding="utf-8")
    issue_date = page_path.parent.name
    style = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
    editions = dict(re.findall(r"<!-- edition:(\w+) -->\s*(.*?)\s*<!-- /edition -->", html, re.S))
    fonts = ensure_fonts(Path(__file__).resolve().parent / ".fonts")
    css = font_css(fonts) + style + PRINT_CSS

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for lang, body in editions.items():
            body = body.replace(" hidden>", ">", 1)
            spans = re.findall(r"<span>(.*?)</span>", re.search(r'class="bar top label">(.*?)</div>', body, re.S).group(1), re.S)
            week, edition = strip_tags(spans[1]), strip_tags(spans[2]).split(" · ")[0]
            doc = (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8">'
                   f"<title>Cribrum — {week}</title><style>{css}</style></head>"
                   f'<body><div class="page">{body}</div></body></html>')
            tmp = page_path.parent / f"_print_{lang}.html"
            tmp.write_text(doc, encoding="utf-8")
            try:
                page.goto(tmp.as_uri(), wait_until="load")
                page.emulate_media(media="print", color_scheme="light")
                page.evaluate("document.fonts.ready")
                footer = ('<div style="width:100%;padding:0 13mm;font-family:Georgia,serif;font-size:7.5pt;'
                          'color:#555;display:flex;justify-content:space-between;">'
                          f"<span>Cribrum · {week} · {edition}</span>"
                          '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
                out = page_path.parent / f"Cribrum_{issue_date}_{lang.upper()}.pdf"
                page.pdf(path=str(out), format="Letter", print_background=True,
                         display_header_footer=True, header_template="<div></div>",
                         footer_template=footer,
                         margin={"top": "12mm", "bottom": "15mm", "left": "13mm", "right": "13mm"})
                print(out)
            finally:
                tmp.unlink(missing_ok=True)
        browser.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(Path(sys.argv[1]).resolve())
