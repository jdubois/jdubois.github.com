# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Developers and peers in the Java / JVM and open-source world, plus the people who decide where Julien shows up next:

- **Java & JVM developers** who arrive from a talk, a GitHub project (JHipster, Dr JSkill, LangChain4j, Spring AI), or a search for his name, and want to know who he is and what he's working on now.
- **Conference organizers & program committees** scanning for credibility, current talk abstracts, and slides before extending an invitation.
- **Community, press, and recruiters/peers** who need a single, authoritative reference point for Julien's bio, projects, and contact details.

They land with a specific intent (read the bio, find a talk, reach the right project) and want to get to the real artifact quickly, in English or French.

## Product Purpose

A central personal hub for Julien Dubois that links everything together — bio, conferences and talks, projects, photos, and contact — and routes visitors confidently to the real artifacts (GitHub, slides, LinkedIn, the book). Success is a visitor who, within seconds, understands who Julien is and reaches the exact thing they came for without friction. The site itself is the credential: calm, well-built, and unmistakably the work of a practitioner.

## Positioning

The single authoritative source on Julien Dubois, maintained by Julien himself: a Java Champion, creator of JHipster, and Principal Manager, Developer Relations at GitHub / Microsoft. It links his bio, current talks with their slide decks, and his projects. No aggregator, event page or social profile brings these together with the same authority.

## Operating Context

- Conference organizers and attendees reach the site from talks: every slide deck ends with a QR code pointing to `julien-dubois.com/conferences`.
- The site is a Jekyll site on GitHub Pages; the slide decks are standalone reveal.js HTML presentations served from `/conferences/<talk>/index-<lang>.html` and projected on stage.
- English and French audiences are both first-class; French pages mirror English ones (`*-fr.html`, `index-fr.html`).

## Capabilities and Constraints

- Pages: home, biography (EN/FR), conferences, projects, book, photos, contact, attic.
- Conference decks: BootUI, 223 Pull Requests in 11 Days (full and light), AI code generation in Java, Winning the Hackathon; English, and French where it exists.
- No build step beyond Jekyll; JavaScript stays minimal. Redirects use `redirect_from` / `redirect_to` front matter.
- Julien's title is "Principal Manager, Developer Relations at GitHub / Microsoft" everywhere.

## Brand Commitments

- Two visual identities, each with its own design doc:
  - **Website:** its own personal identity, recorded in the root `DESIGN.md`.
  - **Conference slide decks:** follow GitHub's brand (https://brand.github.com), recorded in `conferences/DESIGN.md`, because Julien presents as a GitHub employee. The GitHub brand does not extend to the website.
- Brand personality and anti-references below apply to both.

## Brand Personality

**Expert · Precise · Understated.** A senior practitioner's voice, not a marketer's. Concise, professional, and developer-focused; confidence comes from substance (25+ years, 200+ talks, 22,000+ GitHub stars, real Open Source) shown plainly rather than asserted. The "engineering notebook" feel — legible, deliberate, lightly technical (mono labels, code where it earns its place) — is the personality. It should evoke quiet authority and trust, never hype.

## Anti-references

- **Generic AI-generated "SaaS landing" aesthetic** — gradient blobs / mesh backgrounds, identical icon + heading + text card grids, tiny uppercase tracked eyebrows above every section, hero-metric templates, gradient text. This is the primary thing to avoid.
- Flashy, over-animated personal-brand sites that prioritize spectacle over substance.
- Corporate, stock-photo marketing templates.
- Cluttered, dated developer blogs.

## Evidence on Hand

- Track record, stated plainly: 25+ years, 200+ international talks (Devoxx, SpringOne, Microsoft Build…), JHipster with 22,000+ GitHub stars, Java Champion.
- Real artifacts: the slide decks in `conferences/`, the book *Spring par la pratique* (`book.html`), photos in `img/photos/`, and the projects on GitHub (JHipster, Dr JSkill, BootUI, Coffilot, LangChain4j, Spring AI).
- No testimonials, endorsements or third-party quotes exist; do not invent any.

## Product Principles

- **Substance over spectacle.** Credibility is earned by real work shown plainly (talks, projects, contributions), not by marketing flourish. When in doubt, remove decoration.
- **A hub, not a destination.** Every page's job is to orient the visitor and route them confidently to the real artifact (GitHub, slides, LinkedIn, the book). Reduce the steps between landing and leaving for the right place.
- **Practitioner's voice.** Concise, opinionated, developer-to-developer. Show the work (live-coding, code snippets, concrete numbers); don't sell it.
- **Quiet precision.** The engineering-notebook restraint: calm, legible, deliberate. Rhythm and typography carry the design — no hype, no AI-landing scaffolding.
- **Bilingual & accessible by default.** English / French parity and accessibility are first-class, not afterthoughts; every surface works for keyboard, screen-reader, and reduced-motion users.

## Accessibility & Inclusion

Target **WCAG 2.1 AA**. Maintain and uphold the patterns already in place: a visible skip-to-content link, `prefers-reduced-motion` alternatives for every animation, clear `:focus-visible` states, and contrast-tuned color tokens (body text ≥ 4.5:1, large text ≥ 3:1). Preserve English / French parity so both audiences get an equivalent experience. Keep semantic HTML and meaningful `alt` text on imagery.
