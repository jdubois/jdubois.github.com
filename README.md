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
on another page of the same origin. Cookie settings on each deck disappear after
acceptance; visitors can still change their choice from the main website's footer.
The controls are hidden for printing and PDF export.

After consent, Reveal.js decks send `slide_view` on the initial visible slide and
each slide navigation, plus `slide_engagement` with the visible time spent on that
slide. Time is flushed on navigation, tab hiding, and page exit; time before
consent and while the tab is hidden is excluded. Returning to the same slide after
switching tabs resumes timing without counting another view. Fragment reveals
do not count as new slides. Revoking consent stops tracking and discards any
unreported time.

Both events include `deck_path`, `deck_language`, `slide_number` (one-based,
matching Reveal's sequential slide counter), and `slide_title` (the first heading,
limited to 100 characters, or a slide-number fallback).
`slide_engagement` also includes `slide_duration_ms` and GA4's
`engagement_time_msec`. All decks use the shared script; no per-deck handlers
are required.

To compare slides in GA4:

1. In **Admin > Custom definitions**, register event-scoped dimensions for
   `deck_path`, `deck_language`, `slide_number`, and `slide_title`, and an
   event-scoped custom metric for `slide_duration_ms` with unit **Milliseconds**.
2. In **Explore**, filter to a deck path and `slide_view`, use slide number/title
   as rows, and sort **Event count** or **Total users** to find the most viewed
   slides. Use a separate tab filtered to `slide_engagement` and sort the custom
   duration metric to compare total visible reading time. Duration divided by
   slide views gives average visible time per view; an engagement event is a
   time segment, not a whole view.
3. Use **Realtime** (or **DebugView** with GA debug mode enabled) to confirm events
   after accepting cookies. Custom reporting definitions are not retroactive and
   can take 24–48 hours to become available. Opening slides naturally receive more
   views; visible reading time is not proof of attention.

For a new deck, add YAML front matter with `layout: null` and `lang: en` (or
`fr`), link `/css/consent.css` before the shared GitHub theme, and add
`{% include analytics-consent.html deck=true %}` just before `</body>`.
Preview through `./serve.sh` so Jekyll renders the shared include; opening the
source HTML directly does not render the consent controls.

Run the consent regression tests with `node --test tools/test-analytics.mjs`.