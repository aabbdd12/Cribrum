# Pipeline

How a weekly issue goes from research to publication.

## Weekly workflow

1. **Draft.** The editor (Claude) researches the past seven days, following [CHARTER.md](../CHARTER.md) and [SOURCES.md](../SOURCES.md), and writes the issue: four stories, the editor's note, and the French and Spanish translations.
2. **Independent check.** A second agent checks every claim against its link.
3. **Private review page.** The complete issue, with its three PDFs, is shown to the publisher on a private page. Nothing is pushed to this repository at this stage.
4. **Consent.** The publisher approves or asks for changes. Without an explicit "OK", the issue is not published.
5. **Publish.** After approval, the editor commits the issue:
   - `docs/issues/YYYY-MM-DD/index.html`, the trilingual page;
   - the three PDFs next to it, built with `build_pdfs.py`;
   - the redirect in `docs/index.html`, the list in `docs/archive.html` and the feed in `docs/feed.xml`, updated to the new issue.

## Issue page format

One HTML file holds the three editions. Each edition sits between `<!-- edition:xx -->` and `<!-- /edition -->` markers (`en`, `fr`, `es`); English is shown first and a switcher at the top changes language. A link ending in `#fr` or `#es` opens that edition directly.

## Building the PDFs

```
pip install playwright
playwright install chromium
python pipeline/build_pdfs.py docs/issues/YYYY-MM-DD/index.html
```

The script downloads the typefaces (Bodoni Moda, Source Serif 4, Libre Franklin, all under the SIL Open Font License) into `pipeline/.fonts/` on first run, then writes `Cribrum_YYYY-MM-DD_EN.pdf`, `_FR.pdf` and `_ES.pdf` next to the page.
