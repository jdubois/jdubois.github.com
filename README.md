This is the source of Julien Dubois' personal Web site.
=======

This Web site is rendered with Github pages.

## Conference speaker slide

Each presentation under `conferences/` keeps its own copy of the short speaker
bio and its CSS directly in the HTML file. The decks intentionally do not share
bio code, so they can be copied and edited independently.

For a new deck, copy the `speaker-bio` section and its style block from an
existing deck in the same language. Keep the English and French bios equivalent
when updating all presentations, and use the official title in English in both:
"Principal Manager, Developer Relations at GitHub / Microsoft".

## Conference analytics and consent

Every deck uses the website's Google Analytics property and shared consent
choice through `_includes/analytics-consent.html` and `js/analytics.js`.
Analytics loads only after acceptance, including when consent was already given
on another page of the same origin. Cookie settings on each deck lets visitors
change their choice; the controls are hidden for printing and PDF export.

For a new deck, add YAML front matter with `layout: null` and `lang: en` (or
`fr`), link `/css/consent.css` before the shared GitHub theme, and add
`{% include analytics-consent.html deck=true %}` just before `</body>`.
Preview through `./serve.sh` so Jekyll renders the shared include; opening the
source HTML directly does not render the consent controls.

Run the consent regression tests with `node --test tools/test-analytics.mjs`.