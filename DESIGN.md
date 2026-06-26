---
name: Julien Dubois
description: Personal site of Julien Dubois — Java Champion, creator of JHipster, Principal Manager at Microsoft.
colors:
  ink: "#0f1419"
  cobalt: "#1d4ed8"
  cobalt-dark: "#14309c"
  cobalt-tint: "rgba(29, 78, 216, 0.08)"
  accent-bright: "#2f5cf5"
  text-body: "#2a313c"
  text-secondary: "#46505f"
  mono-meta: "#475569"
  bg-white: "#ffffff"
  bg-light: "#f4f6f8"
  border: "#e2e6ea"
  border-strong: "#d2d8df"
typography:
  display:
    fontFamily: "Schibsted Grotesk, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "clamp(2.75rem, 1.9rem + 4vw, 4.5rem)"
    fontWeight: 800
    lineHeight: 1.02
    letterSpacing: "-0.04em"
  headline:
    fontFamily: "Schibsted Grotesk, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "clamp(2.5rem, 1.8rem + 3vw, 3.75rem)"
    fontWeight: 800
    lineHeight: 1.15
    letterSpacing: "-0.035em"
  title:
    fontFamily: "Schibsted Grotesk, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "clamp(1.6rem, 1.3rem + 1.2vw, 2.05rem)"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-0.02em"
  body:
    fontFamily: "Hanken Grotesk, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.7
    letterSpacing: "normal"
  label:
    fontFamily: "JetBrains Mono, ui-monospace, 'SF Mono', Menlo, monospace"
    fontSize: "0.8rem"
    fontWeight: 500
    lineHeight: 1.9
    letterSpacing: "0.005em"
rounded:
  sm: "8px"
  md: "10px"
  lg: "12px"
  xl: "14px"
  xxl: "18px"
spacing:
  xs: "0.5rem"
  sm: "0.75rem"
  md: "1.25rem"
  lg: "1.75rem"
  xl: "3rem"
components:
  button-ink:
    backgroundColor: "{colors.ink}"
    textColor: "#ffffff"
    rounded: "{rounded.md}"
    padding: "0.7rem 1.35rem"
  button-ink-hover:
    backgroundColor: "{colors.cobalt}"
    textColor: "#ffffff"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "0.7rem 1.35rem"
  social-link:
    backgroundColor: "{colors.bg-white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "0.6rem 1rem"
  talk-card:
    backgroundColor: "{colors.bg-white}"
    textColor: "{colors.text-body}"
    rounded: "{rounded.lg}"
    padding: "1.5rem 1.75rem"
  talk-card-open:
    backgroundColor: "{colors.bg-white}"
    textColor: "{colors.text-body}"
    rounded: "{rounded.lg}"
---

# Design System: Julien Dubois

## 1. Overview

**Creative North Star: "The Engineering Notebook"**

This is the personal site of a senior practitioner, and it reads like one: a clean, ruled page where the work speaks and the design gets out of the way. The system pairs near-black ink, a calm off-white field, and a single deliberate cobalt for anything interactive. Typographic confidence — a tight geometric-grotesk display over a humanist body, with a monospace reserved for credentials and metadata — carries the whole composition. Density is generous and unhurried; whitespace is the primary layout tool, not boxes.

The personality is **expert, precise, and understated**. Credibility comes from substance shown plainly (25+ years, 200+ talks, 22,000+ GitHub stars), never from marketing flourish. Every surface's job is to orient a visitor and route them to the real artifact — a talk, a repo, the bio — with as little friction as possible.

It explicitly rejects the **generic AI-generated "SaaS landing" aesthetic**: no gradient blobs or mesh backgrounds, no identical icon-heading-text card grids, no tiny uppercase tracked eyebrows stacked above every section, no hero-metric templates, no gradient text. It is not a flashy over-animated personal-brand site, and it is not a corporate stock-photo template. When in doubt, remove decoration.

**Key Characteristics:**
- Monochrome ink-and-paper spine with one cobalt accent for intent
- Geometric display + humanist body + monospace metadata, used on a strict contrast axis
- Flat at rest, lifting only in response to interaction
- Motion that is purposeful and restrained, fully reduced-motion aware
- Bilingual (EN/FR) and WCAG 2.1 AA by default

## 2. Colors

A monochrome ink-on-paper foundation with a single saturated cobalt that signals "this is interactive or important."

### Primary
- **Cobalt** (`#1d4ed8`): Links, interactive affordances, active-page indicators, the `[open]` state of talk cards, and accent punctuation. The one voice of the system.
- **Cobalt Deep** (`#14309c`): Hover/pressed state for cobalt — links and footer links darken into it.
- **Hero Cobalt** (`#2f5cf5`): A brighter cobalt reserved exclusively for large-scale hero accents and focus outlines. Never used on body-scale text.
- **Cobalt Wash** (`rgba(29,78,216,0.08)`): The active/selected tint behind dropdown items and the mobile active nav link.

### Neutral
- **Ink** (`#0f1419`): Display headings, primary buttons, the dark anchor of the palette. Near-black with a cool cast.
- **Reading Ink** (`#2a313c`): Main body copy (~12:1 on white). The default reading color.
- **Secondary Ink** (`#46505f`): Secondary and meta text, list items, captions (~7.8:1).
- **Mono Slate** (`#475569`): Monospace metadata labels (credentials row, photo captions).
- **Paper** (`#ffffff`): The primary page field and card surface.
- **Cool Paper** (`#f4f6f8`): The footer and mobile dropdown field; a faint cool-gray step down from white.
- **Hairline** (`#e2e6ea`) / **Hairline Strong** (`#d2d8df`): Borders and dividers; the stronger step outlines ghost buttons.

### Named Rules
**The One Voice Rule.** Cobalt is the only chromatic color in the system and appears on ≤10% of any screen. Its job is to mean "interactive / important." If cobalt is everywhere, it means nothing — let ink and the neutral spine carry the surface, and spend cobalt sparingly.

## 3. Typography

**Display Font:** Schibsted Grotesk (with `-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`)
**Body Font:** Hanken Grotesk (with `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`)
**Label/Mono Font:** JetBrains Mono (with `ui-monospace, 'SF Mono', Menlo, monospace`)

**Character:** A confident pairing built on a true contrast axis — a tight, slightly condensed geometric grotesk for display, a warm humanist grotesk for reading, and a precise monospace for metadata. The three never blur together because each lives in its own role.

### Hierarchy
- **Display** (800, `clamp(2.75rem → 4.5rem)`, line-height 1.02, tracking -0.04em): The home hero name only. The single loudest element on the site.
- **Headline** (800, `clamp(2.5rem → 3.75rem)`, line-height 1.15, tracking -0.035em): Page `h1` titles (Biography, Conferences, Projects).
- **Title** (700, `clamp(1.6rem → 2.05rem)`, line-height 1.15, tracking -0.02em): Section `h2` and card `h3` headings.
- **Body** (400, 17px, line-height 1.7): All running prose. Capped at ~54–68ch (`max-width` on `p`) for comfortable measure.
- **Label** (500, 0.8rem, tracking +0.005em): JetBrains Mono metadata — the credentials row, photo captions, the skip link.

### Named Rules
**The Mono-as-Metadata Rule.** JetBrains Mono is for labels, credentials, and captions only — never running text and never headlines. Its monospace texture reads as "data / annotation," reinforcing the engineering-notebook feel. **The No-Cramped-Display Rule.** Display tracking floors at -0.04em and clamp maxes at 4.5rem; never tighter, never larger.

## 4. Elevation

A **layered** system that is **flat at rest**. Surfaces sit on the page with at most a 1px hairline border; depth is introduced only as a response to state. Shadows are low-spread and tinted with the ink hue (`rgba(15,20,25,…)`) rather than pure black, so lifts feel cool and crisp rather than heavy.

### Shadow Vocabulary
- **sm** (`box-shadow: 0 1px 2px 0 rgba(15,20,25,0.06)`): Resting elevation for the navbar and idle talk cards.
- **md** (`box-shadow: 0 6px 16px -6px rgba(15,20,25,0.12)`): Hover/open state for cards, buttons, social links, dropdown menus.
- **lg** (`box-shadow: 0 18px 40px -12px rgba(15,20,25,0.18)`): The profile image and gallery hover.
- **xl** (`box-shadow: 0 24px 48px -12px rgba(15,20,25,0.22)`): The deepest lift — profile image on hover.

### Named Rules
**The Lift-on-Intent Rule.** Surfaces are flat (or sm) at rest. A surface gains a shadow step *and* a `translateY(-2px to -4px)` only in response to hover, focus, or open. Depth is feedback, never decoration.

## 5. Components

### Buttons
- **Shape:** Softly rounded (`10px`, `{rounded.md}`), inline-flex with a 0.5rem gap for optional icons.
- **Primary (`.btn-ink`):** Ink background, white text, 0.7rem×1.35rem padding. On hover it shifts to **cobalt**, lifts `translateY(-2px)`, and gains shadow-md — the brand's signature "ink → cobalt" transition.
- **Ghost (`.btn-ghost`):** Transparent with a `border-strong` hairline and ink text; hover darkens the border to ink and lifts. Used as the secondary action beside the primary.
- **Focus:** Inherits visible focus; hero focus outlines use Hero Cobalt.

### Cards / Containers (the `.talk` disclosure)
- **Corner Style:** `12px` (`{rounded.lg}`).
- **Background:** Paper (`#ffffff`).
- **Shadow Strategy:** sm at rest → md on hover and when `[open]` (see Elevation).
- **Border:** 1px hairline at rest; the border turns **cobalt** when the card is open.
- **Internal Padding:** 1.5rem 1.75rem on the summary; a rotating chevron (45°→-135°) signals open state.

### Navigation
- **Style:** Fixed white Bootstrap 5 navbar with a hairline bottom border and shadow-sm; brand wordmark in ink.
- **States:** Links are ink at 500 weight; hover → cobalt; the active page is marked by a 2px cobalt underline (desktop) or a cobalt-wash background (mobile).
- **Mobile:** Collapses to a paper panel; dropdowns flatten onto Cool Paper and submenus expand inline rather than flying out.

### Signature Component — Social Link Row
A unified monochrome row of pill links (`10px`, paper background, hairline border, inline SVG glyph + label). Hover darkens the border to ink, lifts `translateY(-2px)`, and adds shadow-md. Deliberately *not* colored per-network — the row stays monochrome so it reads as one calm set, not a rainbow of brand badges.

### Links (inline content)
Cobalt, no underline at rest, with an **animated underline** that grows left-to-right on hover (`background-size: 0% → 100% 2px`). External links append a small inline "open" SVG icon automatically.

## 6. Do's and Don'ts

### Do:
- **Do** spend cobalt sparingly — links, the active-nav indicator, the open-card border, hero accents. Let ink + the cool-gray neutrals carry the page (The One Voice Rule).
- **Do** keep JetBrains Mono for metadata only: the credentials row, captions, labels. Never set body copy or headings in mono.
- **Do** keep surfaces flat at rest and lift them only on hover/focus/open with a shadow step plus `translateY(-2px to -4px)`.
- **Do** hold body text at `#2a313c` (Reading Ink) on white/Cool Paper for ≥4.5:1 contrast; bump toward ink before ever lightening for "elegance."
- **Do** preserve the accessibility spine on every new surface: skip link, `:focus-visible` outlines, a `prefers-reduced-motion` alternative for each animation, and meaningful `alt` text.
- **Do** keep English/French parity — every `*-fr` page mirrors its English counterpart.

### Don't:
- **Don't** reach for the generic AI "SaaS landing" kit: no gradient blobs or mesh backgrounds, no identical icon-heading-text card grids, no hero-metric templates.
- **Don't** add a tiny uppercase tracked eyebrow (or `01 / 02 / 03` numbered marker) above every section. They are not part of this system's voice.
- **Don't** use gradient text (`background-clip: text`) or decorative glassmorphism — emphasis comes from weight, size, and ink/cobalt contrast.
- **Don't** use a colored side-stripe border (`border-left`/`border-right` > 1px) on cards or callouts; use the full hairline or the cobalt-on-open border instead.
- **Don't** color the social row per network or introduce a second accent hue — cobalt is the only chromatic voice.
- **Don't** tighten display tracking past -0.04em or push hero type past 4.5rem.
