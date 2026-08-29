serve:
	open http://localhost:1313/
	# note: the -D option lets hugo include posts that are marked as draft
	hugo server -D

# pandoc >= 3 wraps brace-protected surnames ({van Haren}, {Le Boyer}) in
# <span class="nocase">. The class is unstyled, so strip it to keep the
# generated markdown clean and future diffs limited to real content changes.
biblio:
	pandoc -t markdown_strict \
		--citeproc static/files/pandoc-bib-template.md \
		--bibliography static/files/gv.bib \
		| perl -0777 -pe 's|<span class="nocase">||g; s|</span>||g' \
		> static/files/bibliography.md
