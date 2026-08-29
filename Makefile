serve:
	open http://localhost:1313/
	# note: the -D option lets hugo include posts that are marked as draft
	hugo server -D

# Full Zotero library auto-export. Override if the export moves:
#   make biblio ZOTERO_BIB=/path/to/export.bib
ZOTERO_BIB ?= $(HOME)/Projects/gvzbib/gv_zotero.bib

# static/files/gv.bib is generated, not hand-edited. Do not point a Zotero
# auto-export at it: the raw export carries `file` fields holding absolute
# paths under $HOME, and this file is served at /files/gv.bib.
gv.bib bib:
	uv run scripts/filter_bib.py $(ZOTERO_BIB) static/files/gv.bib

# pandoc >= 3 wraps brace-protected surnames ({van Haren}, {Le Boyer}) in
# <span class="nocase">. The class is unstyled, so strip it to keep the
# generated markdown clean and future diffs limited to real content changes.
biblio: bib
	pandoc -t markdown_strict \
		--citeproc static/files/pandoc-bib-template.md \
		--bibliography static/files/gv.bib \
		| perl -0777 -pe 's|<span class="nocase">||g; s|</span>||g' \
		> static/files/bibliography.md

.PHONY: serve bib biblio
