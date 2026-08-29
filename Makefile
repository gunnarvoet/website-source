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

# The layout of the rendered list (year headings, truncated author lists,
# titles as DOI links) is assembled by build_biblio.py; pandoc + citeproc only
# supply the formatted fields, through static/files/bibliography-fields.csl.
biblio: bib
	uv run scripts/build_biblio.py static/files/gv.bib static/files/bibliography.md

.PHONY: serve bib biblio
