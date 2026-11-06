# Conference deck instructions

These instructions supplement the repository's root `AGENTS.md`.

## Design and speaker bio

- Read `conferences/DESIGN.md` before changing deck visuals. Load
  `../github-theme/github-slides.css` last in each deck's head.
- Each deck keeps its speaker bio and its bio CSS directly in its HTML file so
  decks can be copied and edited independently. Do not extract shared bio code.
- For a new deck, copy the `speaker-bio` section and its styles from an existing
  deck in the same language.
- Keep English and French bios equivalent. Use the official title in English in
  both: "Principal Manager, Developer Relations at GitHub / Microsoft".

## Analytics and consent

- Use the shared implementation in `_includes/analytics-consent.html` and
  `js/analytics.js`; do not add per-deck tracking handlers or another GA property.
- For a new deck, add YAML front matter with `layout: null` and `lang: en` or `fr`,
  link `/css/consent.css` before the shared GitHub theme, and include
  `{% include analytics-consent.html deck=true %}` just before `</body>`.
- Load analytics and emit slide events only after consent. Honor the existing
  same-origin consent choice, including changes in other tabs and revocation.
- Hide the deck's cookie settings after acceptance, but preserve revocation
  through the main website's footer. Hide consent controls for print/PDF.
- Count the initial visible slide and slide navigation, not fragment reveals.
  Exclude pre-consent and hidden-tab time from engagement measurements.
- Preview through `./serve.sh` so Jekyll renders the include; opening source HTML
  directly does not render consent controls.
- Run `node --test tools/test-analytics.mjs` after changing tracking or consent.
  When verifying in a browser, block Google requests to avoid test traffic in GA.

Event definitions and GA4 reporting setup are in `docs/analytics.md` at the
repository root. These instructions and the reporting guide must remain
excluded from the Jekyll build.
