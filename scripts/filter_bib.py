# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Build the site publication bibliography from the full Zotero export.

Selects Gunnar's own publications out of the library-wide auto-export and drops
fields that either leak local paths or add nothing to the rendered list.

Usage: filter_bib.py <source.bib> <dest.bib>
"""

import json
import re
import sys
from pathlib import Path

AUTHOR = "Voet"

# Entry types that belong on the publication list. Datasets and software
# releases (@misc) and unpublished manuscripts (@unpublished) are excluded.
KEEP_TYPES = {"article", "incollection", "inproceedings", "book", "phdthesis"}

# `file` carries absolute paths under $HOME and this file is served publicly.
# The rest are Zotero bookkeeping that the CSL never renders.
DROP_FIELDS = {"file", "abstract", "copyright", "langid", "keywords", "urldate",
               "chapter", "date-added", "date-modified"}

FIELD_RE = re.compile(r"^\s*([\w-]+)\s*=\s*", re.M)

# Zotero stores several compound surnames split across its first/last name
# fields ("Boyer, Arnaud Le"), and holds full journal titles where the list
# wants abbreviations. bib_fixups.json maps the export's form to the correct
# one. Keys are full "Last, First" strings so unrelated people who share a
# surname (Tim Boyer, I. P. Castro) are left alone. Fixing the records in
# Zotero would make these entries redundant.
FIXUPS = json.loads((Path(__file__).parent / "bib_fixups.json").read_text(encoding="utf-8"))
NAME_FIXES = FIXUPS["names"]
JOURNAL_FIXES = FIXUPS["journals"]


def repair(body):
    """Apply the Zotero-export corrections to author, editor and journal."""
    def fix_names(m):
        head, names = m.group(1), m.group(2)
        parts = [NAME_FIXES.get(a.strip(), a.strip()) for a in re.split(r"\s+and\s+", names)]
        return "%s{%s}," % (head, " and ".join(parts))

    body = re.sub(r"^(\s*(?:author|editor)\s*=\s*)\{(.*)\},\s*$",
                  fix_names, body, flags=re.M)

    def fix_journal(m):
        title = m.group(2)
        return "%s{%s}%s" % (m.group(1), JOURNAL_FIXES.get(title, title), m.group(3))

    return re.sub(r"^(\s*journal\s*=\s*)\{(.*)\}(,?)\s*$",
                  fix_journal, body, flags=re.M)


def parse(text):
    """Split a .bib into (key, type, body) triples, keyed by citekey."""
    entries = {}
    key = etype = None
    buf = []
    for line in text.splitlines(True):
        if line.startswith("@"):
            if key:
                entries[key] = (etype, "".join(buf))
            m = re.match(r"@(\w+)\s*\{\s*([^,]+),", line)
            key, etype = (m.group(2).strip(), m.group(1).lower()) if m else (None, None)
            buf = [line]
        elif key:
            buf.append(line)
    if key:
        entries[key] = (etype, "".join(buf))
    return entries


def field(body, name):
    m = re.search(r"^\s*%s\s*=\s*(.*)$" % re.escape(name), body, re.M)
    return m.group(1).strip().rstrip(",") if m else ""


def strip_fields(body):
    """Remove DROP_FIELDS, handling values that wrap across lines."""
    out = []
    skipping = False
    for line in body.rstrip().splitlines():
        m = FIELD_RE.match(line)
        if m:
            skipping = m.group(1).lower() in DROP_FIELDS
        elif line.startswith(("}", "@")):
            # closing brace (or a malformed run-on) always ends a skip
            skipping = False
        if not skipping:
            out.append(line)
    # the last field may now carry a trailing comma before the closing brace
    while len(out) > 1 and out[-1].strip() == "}":
        if out[-2].rstrip().endswith(","):
            out[-2] = out[-2].rstrip()[:-1]
        break
    return "\n".join(out).rstrip() + "\n"


def keep(key, etype, body):
    """Curation rules. Returns (bool, reason-if-dropped)."""
    if AUTHOR not in field(body, "author") and AUTHOR not in field(body, "editor"):
        return False, "not an author"
    if etype not in KEEP_TYPES:
        return False, "type @%s" % etype
    year = field(body, "year")
    if not re.search(r"\d{4}", year):
        # catches `in preparation`, `submitted`, and missing years
        return False, "no published year (%s)" % (year or "absent")
    if etype == "article" and not field(body, "journal"):
        return False, "no journal"
    return True, ""


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: filter_bib.py <source.bib> <dest.bib>")
    src, dest = Path(sys.argv[1]), Path(sys.argv[2])
    if not src.exists():
        sys.exit("source bibliography not found: %s" % src)

    entries = parse(src.read_text(encoding="utf-8", errors="replace"))
    kept, dropped = {}, []
    for key, (etype, body) in entries.items():
        ok, why = keep(key, etype, body)
        if ok:
            kept[key] = strip_fields(repair(body))
        elif AUTHOR in field(body, "author") or AUTHOR in field(body, "editor"):
            dropped.append((key, why))

    dest.write_text("\n".join(kept[k] for k in sorted(kept)), encoding="utf-8")

    print("%s: %d entries from %d in %s" % (dest, len(kept), len(entries), src.name))
    if dropped:
        print("excluded %d of your entries:" % len(dropped))
        for key, why in sorted(dropped):
            print("  %-24s %s" % (key, why))


if __name__ == "__main__":
    main()
