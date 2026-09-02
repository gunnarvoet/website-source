# The live site. config/_default/config.toml selects the editorial theme with
# Academic behind it as the fallback, so no --theme flag is needed here.
serve:
	open http://localhost:1313/
	# note: the -D option lets hugo include posts that are marked as draft
	hugo server -D

# The old Academic look, for comparison. Overriding the config's theme list
# with a single theme drops editorial out of the lookup entirely. Runs on its
# own port so it can sit beside `make serve`.
serve-academic:
	open http://localhost:1414/
	hugo server -D --port 1414 --theme hugo-academic-theme

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

.PHONY: serve serve-academic bib biblio
