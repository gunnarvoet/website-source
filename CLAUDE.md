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

`make biblio` must run from the repo root; the Makefile addresses `static/files/` by relative path. It needs
pandoc with `--citeproc`.

`static/files/generate_thumbnail.sh` regenerates `cv_thumbnail.png` from `cv.pdf` with ghostscript; run it from
inside `static/files/`.

## Build and deploy

`.github/workflows/` builds on every push: Hugo **0.164.0 extended** (pinned; local Hugo may be newer),
`hugo --gc --minify --cleanDestinationDir`, then copies `CNAME` into `public/` and pushes `public/` to the
`main` branch of the separate repo `gunnarvoet/gunnarvoet.github.io` using `secrets.TOKEN`. There is no
deploy step to run locally.

`public/` is gitignored and holds stale local build output. It is also still listed in `.gitmodules` from an older
deploy scheme and is not initialized. Do not commit it or try to init that submodule. `resources/` (Hugo's asset
cache) is gitignored too.

The custom domain `gunnarvoet.net` was registered at Cloudflare on 2024-05-29 and `gunnarvoet.github.io` redirects
to it. `CNAME` at the repo root holds the bare domain, and the workflow's copy step is what keeps the custom domain
attached after each deploy, since `--cleanDestinationDir` would otherwise wipe it.

## Theme submodule

`themes/hugo-academic-theme` is a fork (`gunnarvoet/hugo-academic-theme`), branch `gunnarvoet`, based on Academic
v4.8.0 with local tweaks. Pull fork changes with:

    git submodule update --remote --merge

Moving to a newer upstream Academic release breaks a lot and has not been attempted since 4.8.0. Customize through
the root-level `layouts/`, `assets/`, `data/`, and `static/` overrides instead: the theme's own lookup order means a
copy of any theme file at the matching root path wins, color and font themes come from `data/themes/` and
`data/fonts/`, and extra CSS/JS is registered as `plugins_css` / `plugins_js` in `params.toml`.

## Editorial theme (in progress)

`themes/editorial/` is a second look: paper ground, hairline band grid, condensed uppercase Archivo. It is a
plain tracked directory, not a submodule. Run it with:

    make serve-editorial     # hugo server -D --port 1414 --theme editorial,hugo-academic-theme

It is a **theme component, not a replacement**. Hugo resolves the `--theme` list left to right, so editorial
supplies whatever it defines and Academic supplies the rest. Editorial now defines a template for every page
kind the site produces, so the whole editorial build renders in the editorial look; Academic is still the
fallback, and removing a template from `themes/editorial/layouts/` returns that page type to it.

Nothing in `config/` selects it. `config/_default/config.toml` still says `theme = "hugo-academic-theme"`, so
`make serve`, a bare `hugo`, and the GitHub deploy all build the Academic site untouched. Keep it that way
until the theme is finished. After any change, verify both: a bare `hugo` must produce the Academic site with
no editorial markup in it, and `hugo --theme editorial,hugo-academic-theme` must produce the editorial one.

Do **not** develop this theme from the root-level `layouts/` or `assets/`. The project root wins over every
theme in Hugo's lookup order, so a homepage layout placed there is not optional, it is the homepage, and it
would deploy on the next push. That is why these files live under `themes/`.

The `--theme` flag can only swap templates, not configuration. When editorial needs its own `menus.toml` or
different `params.toml` values, move the switch to a config environment (`config/editorial/`, selected with
`hugo --environment editorial`) rather than trying to bend the flag.

### Layout structure

The shell is `partials/shell/open.html` and `partials/shell/close.html`, with `head.html`, `header.html` and
`footer.html` inside them. Page templates are `{{ define "main" }}` blocks.

**There is deliberately no `layouts/_default/baseof.html`.** Hugo resolves base templates across the whole
`--theme` list, so a `_default` one here would be picked for every page, including any that editorial has no
template for; those would pair the editorial shell with an Academic content template that defines no `main`
block and render as an empty frame. Instead each page kind gets its own three-line base template
(`index-baseof.html`, `project/baseof.html`, `post/baseof.html`, and so on) that calls the two shell partials
around a `{{ block "main" }}`. A base template cannot be shared through a partial, because `{{ block }}` is
only recognised in the base template file itself, which is why those three lines are repeated.

Two lookup traps cost time; both are commented in the files:

- `layouts/section/<SECTION>.html` outranks `layouts/<SECTION>/list.html`, and Academic ships
  `section/post.html`, `section/publication.html` and `section/talk.html`. Section lists therefore live in
  `themes/editorial/layouts/section/`.
- A taxonomy index is reached **only** through `layouts/<TAXONOMY>/terms.html`. Neither `layouts/terms.html`
  nor `layouts/_default/terms.html` is ever consulted, so all four configured taxonomies carry their own copy.
  Academic also ships `layouts/authors/list.html`, which outranks `_default/term.html` for the author
  taxonomy, so that name exists here too. All of them are one line over a shared partial.

Shared partials: `plate.html` (a page's featured image as a full-bleed band, honouring Academic's
`image.preview_only`), `pagenav.html` (the neighbouring pages as cells of the projects grid),
`related.html` and `pagegroups.html` (bands built from real links in the content), and under `func/`, partials
that return values rather than markup: `author.html`, `content.html`, `math.html`, `related.html`,
`term-name.html`.

`shortcodes/figure.html` overrides Academic's. Academic's hands the image to lazysizes as `data-src` with
`class="lazyload"` and wraps it in a fancybox trigger, and the editorial shell loads neither script, so every
figure in the cruise posts would render as an empty box.

Math is typeset at build time. Academic pulls MathJax off a CDN; `func/math.html` hands the TeX to Hugo's
built-in KaTeX (`transform.ToMath`) and emits MathML instead, so there is no script and no external request.
The site's goldmark has no passthrough extension and `config/` is off limits to this theme, so the delimiters
are found in the rendered HTML rather than during markdown parsing, and only pages with `math: true` are
scanned.

### Content coupling

Every template reads real site content, so the theme stays in sync on its own: the author bundle (found by
`superuser: true`, not by slug), the `project` section, the `software.md` and `data.md` widget bodies,
`params.toml`, and `static/files/bibliography.md`. Pages are linked to each other through the `tags` and
`projects` front matter that already exists, which is what fills the "Papers", "From the field" and "Project"
bands. Nothing is transcribed by hand.

Archivo and IBM Plex Mono are self-hosted from `themes/editorial/static/fonts/`, so the theme makes no request
to Google Fonts. `themes/editorial/fetch-fonts.sh` refreshes those files from the Google Fonts CSS API, keeping
the latin and latin-ext subsets. The matching `@font-face` rules are hand-maintained at the top of
`editorial.css` and have to be edited alongside it if the axes or weights change. Both families are OFL 1.1;
`static/fonts/OFL.txt` carries the license.

## Configuration layout

`config.toml` at the root is an inert compatibility stub. The real config is `config/_default/`:

- `config.toml` — baseurl, outputs (home also emits JSON for built-in search, and a WebAppManifest), markup, taxonomies
- `params.toml` — theme name, contact details, search/map/comments engines, publication and project view styles
- `menus.toml` — nav bar; a URL of `#foo` targets the homepage widget file `content/home/foo.md`
- `languages.toml` — single English language block

Site colors come from `data/themes/minimal_gunnar.toml`, selected by `theme = "minimal_gunnar"` in `params.toml`.
Root-level `layouts/`, `assets/`, `data/`, and `static/` override the theme submodule; keep edits there rather than
in `themes/`. Current overrides are `layouts/partials/custom_head.html`, `layouts/shortcodes/include.html`, and
`assets/scss/custom.scss`. The last is the theme's own hook for extra styling: `main.scss` ends with
`@import "custom"`, so the root copy is compiled into `academic.css` with the theme's SCSS variables
(`$sta-primary` and friends) in scope. Dark-mode rules take a `.dark` prefix.

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
      -> scripts/build_biblio.py          (runs pandoc --citeproc, then lays out the HTML)
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

`scripts/build_biblio.py` owns the rendered layout. pandoc formats the fields but does not lay them out:
`static/files/bibliography-fields.csl` emits each entry as six fields separated by `‖` (year, authors separated by
`¦`, title, venue, volume/pages, DOI URL) and the script turns them into the HTML the widget includes: an `<h3>`
per year, the title as a link to the DOI, and a muted meta line with the authors and journal. Author lists longer
than ten names collapse to the first three, an ellipsis and Voet (`Cimoli, L., Mashayek, A., Naveira Garabato, A.C.
… **Voet, G.**, et al.`), so the large-collaboration papers stay recognizable as his; `Voet, G.` is bolded in every
entry. Styling lives in `assets/scss/custom.scss` under the `.pub-*` classes.

If the field count ever changes, the script exits rather than writing a mangled list. Both delimiters are chosen so
they cannot appear in bibliographic text.

`gv_prior.bib` holds older entries and is not part of the generated list. `static/files/style.csl` (Elsevier
Harvard, locally adjusted) is no longer in the chain; `bibliography-fields.csl` was derived from it and keeps its
macros, so journal-abbreviation and name handling are unchanged.

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
so notebooks can sit inside content bundles without being rendered. It applies to content only, not to `static/`.

**Put a post's photographs in its own bundle, not in `static/img/`.** Hugo copies `static/` verbatim and cannot
resize anything in it, so a figure written as `{{< figure library="true" src="cruise-x/photo.jpg" >}}` served
the original at whatever the camera produced. Write `{{< figure src="photo.jpg" >}}` against a file in the
bundle instead, and both themes' figure shortcodes put it through `Fit "2000x2000"`.

`content/post/_index.md` cascades `build.publishResources = false` over every post. Hugo otherwise publishes
every bundle resource whether or not a template asks for it, which would put the original next to the resized
copy on the server. With it set, only what a template actually references is published. If you ever link a
bundle file directly rather than through a template, it will 404 until something processes it.

The CV is a committed binary at `static/files/cv.pdf`, linked from the nav bar; it is produced outside this repo.

## Notes outside this repo

Long-form history and the archived theme documentation live in the Obsidian vault:

- `$HOME/Projects/zettelkasten/references/other/Personal Website.md` — domain and hosting, the theme update
  procedure, a per-year change log, and the links collected while building the bibliography pipeline
- `$HOME/Projects/zettelkasten/references/other/hugo academic theme customization.md` — archived Academic
  customization docs (colors, fonts, site icons, permalinks, custom CSS/JS, template overrides, date formats)

After a change worth remembering a year from now, add it to the change log in `Personal Website.md`.
