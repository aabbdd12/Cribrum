# Cribrum

**The week in AI, sifted by AI.**

Cribrum is a weekly newspaper about artificial intelligence. Each issue brings four stories from the past seven days, written and checked by an AI editor, with every claim linked to its source. It is published in English, French and Spanish, on the web and as PDF.

Read it at **https://aabbdd12.github.io/Cribrum/**

*Cribrum* is Latin for a sieve.

## How an issue is made

1. **Watch.** The editor scans the sources listed in [SOURCES.md](SOURCES.md) for the past seven days.
2. **Sift.** Stories are deduplicated, and anything whose event falls outside the week is dropped.
3. **Verify.** Facts, figures and dates are checked against primary sources.
4. **Write.** Four stories and an editor's note: what was left out, and why.
5. **Check.** A second AI agent, which did not write the issue, checks every claim against its link.
6. **Translate.** French and Spanish editions are translated from the English reference text.
7. **Review and consent.** The publisher reviews the full issue on a private page. Nothing is published without his explicit approval.
8. **Publish.** The issue is pushed here and appears on the site, with one PDF per language.

The rules behind these steps are in the [editorial charter](CHARTER.md). Errors are listed in [CORRECTIONS.md](CORRECTIONS.md).

## Repository layout

```
CHARTER.md          editorial rules, including the consent rule
SOURCES.md          where the editor looks each week
CORRECTIONS.md      public log of corrections
docs/               the website (served by GitHub Pages)
  index.html          redirects to the latest issue
  archive.html        every issue, in every language
  feed.xml            RSS feed
  issues/YYYY-MM-DD/  one folder per issue: the trilingual page and its PDFs
pipeline/           tools used to produce an issue (PDF builder)
```

## Who is behind it

- **Publisher:** Abdelkrim Araar
- **Editor:** Claude, an AI model made by Anthropic. The paper discloses this whenever a story involves Anthropic.
