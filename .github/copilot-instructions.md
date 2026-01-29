# GitHub Copilot Instructions

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
- Every page uses YAML front matter with `layout: default` and `title`.
- Use semantic HTML; CSS is Bootstrap 5–compatible — prefer existing utility patterns and CSS variables in `css/main.css`.
- Avoid inline styles; extend `css/main.css` when necessary.
- Keep JS lightweight; no build step.
- For redirects, use `redirect_from` front matter (jekyll-redirect-from).

## Local development
- Ruby ≥ 3.0 (rbenv recommended).
- Install deps: `bundle install`
- Run locally: `./serve.sh` (runs `bundle exec jekyll serve --livereload`).
- `_config.yml` already excludes `node_modules` and `bower_components`.

## Content & assets
- Images: `img/photos/`.
- External links: `target="_blank"` (CSS adds external-link icon automatically).
- Internationalization: French variants (`*-fr.html`) mirror English pages.

## Copilot checklist
- ❌ Do **not** touch `/_site/`.
- ✅ `jekyll serve` builds cleanly locally.
- ✅ Match site tone: concise, professional, developer-focused.
- ✅ Reuse existing CSS variables and components.
