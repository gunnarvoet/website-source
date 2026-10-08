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

# Checkout of the private cv repo (gunnarvoet/cv). Override if it moves:
#   make cv CV_DIR=/path/to/cv
CV_DIR ?= $(HOME)/Projects/cv
CV_NAME ?= cv_gunnar_voet

# static/files/cv.pdf is built from the cv repo, which does not track its PDF.
# The PDF is public, so the checkout has to be clean: what gets served then
# matches a commit over there. `make cv FORCE=1` skips that check.
cv:
ifndef FORCE
	@test -z "$$(git -C $(CV_DIR) status --porcelain)" || { \
		echo "$(CV_DIR) has uncommitted changes; commit them or run 'make cv FORCE=1'"; \
		git -C $(CV_DIR) status --short; \
		exit 1; }
endif
	latexmk -cd $(CV_DIR)/$(CV_NAME).tex
	cp $(CV_DIR)/$(CV_NAME).pdf static/files/cv.pdf
	@echo "cv.pdf <- $(CV_DIR) @ $$(git -C $(CV_DIR) log -1 --format='%h %s')"

.PHONY: serve serve-academic bib biblio cv
