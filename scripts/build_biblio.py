# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Render static/files/bibliography.md from static/files/gv.bib.

pandoc + citeproc do the bibliographic formatting (name initials, journal
abbreviations, page ranges) but not the layout: bibliography-fields.csl emits
each entry as delimiter-separated fields, and this script assembles the HTML
the homepage publication widget includes.

Usage: build_biblio.py <source.bib> <dest.md>
"""

import html
import re
import subprocess
import sys
from pathlib import Path

AUTHOR = "Voet"

# Delimiters emitted by bibliography-fields.csl. Chosen so they cannot occur
# in a title, a journal name or a page range.
FIELD_SEP = "‖"  # between the six fields of an entry
NAME_SEP = "¦"   # between authors

# Author lists up to this length are shown in full. Longer ones collapse to
# the first three names, an ellipsis and Voet, so a 32-author paper still
# reads as one of his.
MAX_AUTHORS = 10
KEEP_FIRST = 3

HERE = Path(__file__).resolve().parent
CSL = HERE.parent / "static" / "files" / "bibliography-fields.csl"

# citeproc marks case-protected spans (`{van Haren}`, `{Yanai Wave}`) with
# <span> and <span class="nocase">. Both are unstyled here, so drop them.
SPAN_RE = re.compile(r'</?span(?: class="nocase")?>')
ENTRY_RE = re.compile(r'<div id="ref-([^"]+)" class="csl-entry"[^>]*>(.*?)\n</div>', re.S)
LINK_RE = re.compile(r'<a\s+href="([^"]+)">.*?</a>', re.S)


def run_pandoc(bib):
    """Return citeproc's HTML for every entry in `bib`."""
    doc = '---\nnocite: "@*"\n---\n'
    cmd = ["pandoc", "-t", "html", "--citeproc",
           "--bibliography", str(bib), "--csl", str(CSL)]
    out = subprocess.run(cmd, input=doc, capture_output=True, text=True)
    if out.returncode:
        sys.exit("pandoc failed:\n" + out.stderr)
    return out.stdout


def authors(field):
    """Format one author list: truncate the long ones, always keep Voet."""
    names = [n.strip() for n in field.split(NAME_SEP) if n.strip()]
    shown = ", ".join(names)
    if len(names) > MAX_AUTHORS:
        head = ", ".join(names[:KEEP_FIRST])
        rest = names[KEEP_FIRST:]
        mine = next((i for i, n in enumerate(rest) if n.startswith(AUTHOR)), None)
        if mine is None:
            shown = head + ", et al."
        else:
            # an ellipsis stands in for the names skipped ahead of Voet, and
            # "et al." for those after him
            gap = " … " if mine else ", "
            tail = ", et al." if mine < len(rest) - 1 else ""
            shown = head + gap + rest[mine] + tail
    return re.sub(r"\b(%s, [A-Z][.\-A-Z]*)" % AUTHOR, r"<strong>\1</strong>", shown, count=1)


def parse(entry):
    """Split one citeproc entry into its six fields."""
    text = SPAN_RE.sub("", entry)
    link = LINK_RE.search(text)
    # DOIs carry LaTeX escapes from the Zotero export (10.1007/...-7\_20).
    url = link.group(1).replace("\\", "") if link else ""
    text = LINK_RE.sub("", text)
    text = re.sub(r"\s+", " ", text).strip()
    fields = text.split(FIELD_SEP)
    if len(fields) != 6:
        sys.exit("unexpected field count (%d) in entry: %.120s" % (len(fields), text))
    year, names, title, venue, locators, _ = (f.strip() for f in fields)
    return year, names, title, venue, locators, url


def render(entries):
    out = ['<div class="pub-list">']
    year = None
    for key, entry in entries:
        y, names, title, venue, locators, url = parse(entry)
        if y != year:
            year = y
            out.append('<h3 class="pub-year">%s</h3>' % html.escape(year))
        title_html = ('<a class="pub-title" href="%s">%s</a>' % (html.escape(url), title)
                      if url else '<span class="pub-title">%s</span>' % title)
        # book chapters emit "pp. 89-103", which needs a comma; a journal
        # volume runs straight on from the abbreviation.
        sep = ", " if locators.startswith("pp.") else " "
        venue = sep.join(v for v in (venue, locators) if v)
        out.append('<div class="pub" id="pub-%s">' % html.escape(key))
        out.append("  " + title_html)
        out.append('  <div class="pub-meta"><span class="pub-authors">%s</span>'
                   '<span class="pub-venue">%s</span></div>' % (authors(names), venue))
        out.append("</div>")
    out.append("</div>")
    return "\n".join(out) + "\n"


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: build_biblio.py <source.bib> <dest.md>")
    src, dest = Path(sys.argv[1]), Path(sys.argv[2])
    if not src.exists():
        sys.exit("bibliography not found: %s" % src)

    entries = ENTRY_RE.findall(run_pandoc(src))
    if not entries:
        sys.exit("citeproc returned no entries; is %s empty?" % src)
    dest.write_text(render(entries), encoding="utf-8")

    long_lists = sum(1 for _, e in entries if e.count(NAME_SEP) >= MAX_AUTHORS)
    print("%s: %d entries, %d author lists truncated" % (dest, len(entries), long_lists))


if __name__ == "__main__":
    main()
