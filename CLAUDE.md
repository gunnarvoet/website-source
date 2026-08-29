# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Source for the personal academic website at https://gunnarvoet.net. Hugo static site built on a fork of the
Hugo Academic theme (v4.8.0), vendored as a git submodule at `themes/hugo-academic-theme` (branch `gunnarvoet`).
Theme docs still live at https://sourcethemes.com/academic/docs/.

## Commands

```
make serve     # hugo server -D (includes drafts), opens http://localhost:1313/
make biblio    # regenerate static/files/bibliography.md from static/files/gv.bib via pandoc + CSL
```

`make biblio` must run from the repo root; `static/files/pandoc-bib-template.md` references `static/files/style.csl`
by a root-relative path. It needs pandoc with `--citeproc`.

`static/files/generate_thumbnail.sh` regenerates `cv_thumbnail.png` from `cv.pdf` with ghostscript; run it from
inside `static/files/`.

## Build and deploy

`.github/workflows/` builds on every push: Hugo **0.164.0 extended** (pinned; local Hugo may be newer),
`hugo --gc --minify --cleanDestinationDir`, then copies `CNAME` into `public/` and pushes `public/` to the
`main` branch of the separate repo `gunnarvoet/gunnarvoet.github.io` using `secrets.TOKEN`. There is no
deploy step to run locally.

`public/` is gitignored and holds stale local build output. It is also still listed in `.gitmodules` from an older
deploy scheme and is not initialized. Do not commit it or try to init that submodule.

## Configuration layout

`config.toml` at the root is an inert compatibility stub. The real config is `config/_default/`:

- `config.toml` — baseurl, outputs (home also emits JSON for built-in search, and a WebAppManifest), markup, taxonomies
- `params.toml` — theme name, contact details, search/map/comments engines, publication and project view styles
- `menus.toml` — nav bar; a URL of `#foo` targets the homepage widget file `content/home/foo.md`
- `languages.toml` — single English language block

Site colors come from `data/themes/minimal_gunnar.toml`, selected by `theme = "minimal_gunnar"` in `params.toml`.
Root-level `layouts/`, `assets/`, `data/`, and `static/` override the theme submodule; keep edits there rather than
in `themes/`. Current overrides are `layouts/partials/custom_head.html` and `layouts/shortcodes/include.html`.

## Homepage structure

The homepage is a widget page: `content/home/index.md` is an empty `type = "widget_page"`, and each other
`content/home/*.md` is one section. Front matter drives everything:

- `widget = "..."` picks a theme partial from `themes/hugo-academic-theme/layouts/partials/widgets/`
- `active = true/false` shows or hides the section
- `weight` sets the order (must stay consistent with the weights in `menus.toml`)

`widget = "blank"` sections (`software.md`, `data.md`, `publicationlist.md`) render their markdown body directly and
are where most hand-written homepage content lives.

## Publication list

The publication list is not the Academic publication widget. `content/home/publicationlist.md` is a `blank` widget
whose body is `{{% include file="static/files/bibliography.md" %}}`, using the local `include` shortcode
(`layouts/shortcodes/include.html`) which reads the file raw and strips a leading `---` front matter block if present.

Both `static/files/gv.bib` and `static/files/bibliography.md` are generated. Never hand-edit either one.
The chain is:

    $HOME/Projects/gvzbib/gv_zotero.bib   (full Zotero library, auto-exported by Better BibTeX)
      -> scripts/filter_bib.py            (select own publications, strip fields, apply fixups)
      -> static/files/gv.bib
      -> pandoc --citeproc + style.csl
      -> static/files/bibliography.md

To add or change a paper: fix it in Zotero, let the export refresh `gv_zotero.bib`, run `make biblio`, and commit
both generated files. Override the source with `make biblio ZOTERO_BIB=/path/to/export.bib`.

Do not point a Zotero auto-export at `static/files/gv.bib`. The raw export carries `file` fields holding absolute
paths under `$HOME`, and that file is served publicly at `/files/gv.bib`.

`scripts/filter_bib.py` keeps `@article`/`@incollection`/`@inproceedings`/`@book`/`@phdthesis` entries with Voet as
an author, and drops entries with no four-digit year (which catches `in preparation`), articles with no journal, and
`@misc`/`@unpublished` (datasets, software releases, unpublished manuscripts). It prints what it excluded on every
run. `scripts/bib_fixups.json` substitutes journal abbreviations where Zotero has no `journalAbbreviation` value
(only 28 of 59 own-publication items carry one). Its `names` map is empty: the compound surnames it used to repair
were fixed at the source with `scripts/fix_zotero_names.js`. Keys are the export's exact form, so add to the
`journals` map only when a full title shows up in the rendered list.

`gv_prior.bib` holds older entries and is not part of the generated list. Citation formatting is
`static/files/style.csl` (Elsevier Harvard, locally adjusted).

Pages under `content/publication/journal-article/<slug>/index.md` are separate standalone publication pages with
Academic front matter (`publication_types`, `doi`, `url_pdf`, abstract, `tags`). They are independent of the
bibliography list, so a new paper needs a `.bib` entry, a detail page, or both depending on intent.

## Content conventions

Content types: `content/post/`, `content/project/`, `content/publication/journal-article/`, `content/talk/`,
`content/authors/gunnar/`. Most entries are page bundles (a directory with `index.md` plus assets); a
`featured.jpg`/`featured.png` in the bundle becomes the card and header image. `archetypes/post/index.md` is the
template for new posts.

Projects and content are linked through `tags` (for example `tags: [samoan-passage]` on both a project and its
publications), and cross-page links use `{{< ref "/project/samoan-passage" >}}`. Inline icons use
`{{< icon name="github" pack="fab" ... >}}`.

`ignoreFiles` in `config/_default/config.toml` excludes `.ipynb`, `.Rmd`, and their checkpoint/cache directories,
so notebooks can sit inside content bundles without being rendered.

The CV is a committed binary at `static/files/cv.pdf`, linked from the nav bar; it is produced outside this repo.
