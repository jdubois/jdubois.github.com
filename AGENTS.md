# Agent instructions

## Repository overview
- Personal website for Julien Dubois.
- Built with Jekyll, deployed via GitHub Pages.
- Markdown via kramdown (GFM); plugin: `jekyll-redirect-from`.

## Source vs generated
- Source pages live at repo root and `_layouts/`.
- Styles in `css/main.css`; JS in `js/main.js` (vanilla ES6, currently minimal).
- `/_site/` and everything under it (including `/assets/`, `/css/`, `/js/`) is generated — **never edit**.
- `Gemfile` managed by `github-pages`; let Bundler resolve versions.

## Conventions
- Website pages use YAML front matter with `layout: default` and `title`. Standalone conference decks use `layout: null`; see `conferences/AGENTS.md`.
- Use semantic HTML; CSS is Bootstrap 5–compatible — prefer existing utility patterns and CSS variables in `css/main.css`.
- Avoid inline styles; extend `css/main.css` when necessary.
- Keep JS lightweight; no build step.
- For redirects, use `redirect_from` front matter (jekyll-redirect-from).

## Local development
- Ruby ≥ 3.0 (rbenv recommended).
- Install deps: `bundle install`
- Run locally: `./serve.sh` (runs `bundle exec jekyll serve --livereload`).
- Run analytics regression tests: `node --test tools/test-analytics.mjs`.
- Keep agent instructions, technical documentation, and design context excluded from the Jekyll build in `_config.yml`.

## Content & assets
- Images: `img/photos/`.
- External links: `target="_blank"` (CSS adds external-link icon automatically).
- Internationalization: French variants (`*-fr.html`) mirror English pages.

## Checklist
- ❌ Do **not** touch `/_site/`.
- ✅ `jekyll serve` builds cleanly locally.
- ✅ Match site tone: concise, professional, developer-focused.
- ✅ Reuse existing CSS variables and components.

## Technical documentation
- Keep `README.md` limited to a short personal website introduction and the published website link.
- Follow `conferences/AGENTS.md` when working on conference decks.
- See `docs/analytics.md` for GA4 event definitions and reporting setup.

## Design Context
- **`PRODUCT.md`** (repo root) — design strategy: register (`brand`), users, purpose, brand personality, anti-references, and design principles. Read it before UX or content decisions.
- **`DESIGN.md`** (repo root) — the visual system in Stitch format ("The Engineering Notebook": cobalt-on-ink palette, Schibsted/Hanken/JetBrains Mono type, flat-at-rest elevation). Read it before any visual or styling change; the tokens mirror `css/main.css` variables.
- Core rule: cobalt (`--primary-color`) is the only accent — use it sparingly for interactive/important elements; ink + neutrals carry the surface. Avoid generic AI "SaaS landing" patterns (gradient blobs, identical card grids, per-section eyebrows, gradient text).
- These files (and `.impeccable/`) are excluded from the Jekyll build and are project context only, never published.
