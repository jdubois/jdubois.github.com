# Conference analytics

All decks use the website's Google Analytics property and shared consent
choice through `_includes/analytics-consent.html` and `js/analytics.js`.
Analytics loads only after acceptance, including consent already given on
another page of the same origin.

## Events

- `slide_view`: the initial visible slide and each slide navigation.
- `slide_engagement`: visible time spent on a slide, flushed on navigation,
  tab hiding, and page exit.

Both events include `deck_path`, `deck_language`, `slide_number` (one-based,
matching Reveal's sequential slide counter), and `slide_title` (the first heading,
limited to 100 characters, or a slide-number fallback).
`slide_engagement` also includes `slide_duration_ms` and GA4's
`engagement_time_msec`.

Time before consent and while the tab is hidden is excluded. Returning to the
same slide after switching tabs resumes timing without another view. Fragment
reveals do not count as new slides. Revoking consent stops tracking and discards
unreported time. Cookie settings disappear from decks after acceptance; visitors
can revoke consent through the main website's footer.

## GA4 reporting setup

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
   can take 24-48 hours to become available.

Opening slides naturally receive more views; visible reading time is not proof
of attention. Keep automated browser verification traffic out of the property
by blocking Google Analytics requests.

Run regression tests with `node --test tools/test-analytics.mjs`.
