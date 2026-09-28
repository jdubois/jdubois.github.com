---
name: GitHub Conference Slides
description: Conference deck system for Julien Dubois talks, re-skinned through the shared GitHub brand Reveal theme.
colors:
  github-green: "#0FBF3E"
  github-green-light: "#BFFFD1"
  github-green-bright: "#5FED83"
  github-green-dark: "#08872B"
  github-green-ink: "#0A241B"
  copilot-purple: "#8534F3"
  copilot-purple-light: "#B870FF"
  copilot-purple-ink: "#26115F"
  alert-orange: "#C53211"
  alert-orange-light: "#F08A3A"
  white: "#FFFFFF"
  gray-1: "#F2F5F3"
  gray-2: "#E4EBE6"
  gray-3: "#B6BFB8"
  gray-4: "#909692"
  gray-5: "#232925"
  black: "#101411"
  black-terminal: "#0B0E0C"
  text-subtle-light: "#5F6B63"
  text-subtle-dark: "#96A199"
typography:
  display:
    fontFamily: "Mona Sans, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
    fontSize: "2.9em"
    fontWeight: 500
    lineHeight: 1
    letterSpacing: "-0.015em"
    fontFeature: "'liga' 0"
  headline:
    fontFamily: "Mona Sans, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
    fontSize: "1.2em"
    fontWeight: 500
    lineHeight: 1.12
    letterSpacing: "-0.005em"
    fontFeature: "'liga' 0"
  title:
    fontFamily: "Mona Sans, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
    fontSize: "0.7em"
    fontWeight: 600
    lineHeight: 1.35
    letterSpacing: "0"
    fontFeature: "'liga' 0"
  body:
    fontFamily: "Mona Sans, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
    fontSize: "0.7em"
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "normal"
    fontFeature: "'liga' 0"
  label:
    fontFamily: "Mona Sans Mono, ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"
    fontSize: "15px"
    fontWeight: 500
    lineHeight: 1.35
    letterSpacing: "0"
rounded:
  chip: "6px"
  image: "8px"
  card: "12px"
  cell: "14px"
spacing:
  cell-gap: "10px"
  card-gap: "16px"
  rail-width: "184px"
  slide-inset: "48px"
  slide-pad: "56px"
  main-pad-x: "64px"
components:
  content-card:
    backgroundColor: "{colors.white}"
    textColor: "{colors.gray-5}"
    typography: "{typography.body}"
    rounded: "{rounded.card}"
    padding: "0.8em 1em"
  dark-card:
    backgroundColor: "{colors.gray-5}"
    textColor: "#C9D1CB"
    typography: "{typography.body}"
    rounded: "{rounded.card}"
    padding: "0.8em 1em"
  mono-chip:
    backgroundColor: "{colors.gray-1}"
    textColor: "{colors.gray-5}"
    typography: "{typography.label}"
    rounded: "{rounded.chip}"
    padding: "3px 12px"
  copy-button:
    backgroundColor: "{colors.github-green-dark}"
    textColor: "#FFFFFF"
    typography: "{typography.body}"
    rounded: "{rounded.chip}"
    padding: "0.5em 0.9em"
  rail-cover:
    backgroundColor: "{colors.black}"
    textColor: "#FFFFFF"
    typography: "{typography.display}"
    width: "1280px"
    height: "720px"
---

# Design System: GitHub Conference Slides

## Overview

**Creative North Star: "The GitHub Speaker Rail"**

The conference decks read as GitHub talks before they read as individual talk brands: a neutral stage, one GitHub Green hero, a black opening and closing cadence, and the brand's speaker-card rail on the slides that carry ceremony. The system is not a generic AI-keynote skin. It replaces blue/violet gradient washes, glow, gradient text, and per-deck personality chrome with GitHub's presentation grammar: black-and-white contrast, green rules, contribution cells, Mona typography, and quiet 2px structure.

Content slides stay White so the talk remains readable and fast to scan. Covers, section dividers, demo/night slides, conclusions, and closings move to Black (`#101411`) when the deck needs ceremony or terminal focus. Legacy decks still keep their inline `<style>` blocks; the shared theme is loaded last and re-tokenises their old variables (`--blue`, `--violet`, `--amber`, `--primary`, `--accent-*`) into the GitHub palette. That compatibility layer is part of the system, not a migration accident.

Fonts are self-hosted in `conferences/github-theme/fonts/`: Mona Sans v2.0.27 and Mona Sans Mono under the SIL Open Font License. A new deck opts in by linking `../github-theme/github-slides.css` last in `<head>`, then using `gh-full gh-cover`, `gh-full gh-divider`, or `gh-full gh-closing` sections with `data-background-color="#101411"` and the required `.gh-frame > .gh-rail + .gh-main` structure.

**Key Characteristics:**
- White content slides, Black ceremonial/demo slides, and GitHub Green as the single hero color
- Mona Sans everywhere, Mona Sans Mono only for code, handles, labels, slide numbers, and terminal UI
- A 184px left rail, one 2px green rule, and four contribution cells for cover/divider/closing slides
- Flat 2px borders instead of shadows, gradients, glows, or glass
- Copilot Purple appears only when Copilot or AI is the subject

## Colors

The palette follows GitHub brand proportions: mostly neutral, a small gray structure layer, and a rare green hero accent; purple is a topic marker, not a second brand voice.

### Primary
- **GitHub Green**: The hero accent for rails, bullets, progress, strong emphasis on Black, timeline dots, and primary deck chrome.
- **Accessible Green Text**: The dark green role used for links and emphasis on White slides through `--gh-accent-text`; the bright hero green is reserved for large/bold text or dark backgrounds.
- **Contribution Greens**: The light, bright, hero, dark, and ink-green steps draw the four-cell motif, chart fills, green chips, and dark green banners.

### Secondary
- **Copilot Purple**: Used sparingly for Copilot/AI subject matter: the fourth contribution cell on Copilot covers, `.card.t-violet`, `.agent .pill.run`, purple dark banners, and selected terminal/demo moments.
- **Operational Orange**: Used for warnings, contrast categories, solo/no-AI estimates, and amber/rose legacy classes. It supports the story but never replaces green as the brand accent.

### Neutral
- **White Stage**: Default content-slide background and card surface.
- **Soft Gray Stage**: The subtle content field for demoted detail cards, chips, fills, and low-priority panels.
- **Neutral Rules**: Gray-2 and gray-3 are the border system: 2px slide rules, card outlines, screenshot frames, dashed bands, and table separators.
- **Reading Ink**: Gray-6 for headings and primary text on White; gray-5 for body and dark-card surfaces.
- **Black Stage**: Cover, divider, demo, conclusion, and closing background. It is the ceremonial color of the deck.
- **Dark Subtle Text**: The muted text color on Black slides for subtitles, links lists, speaker metadata, and slide numbers.

### Named Rules
**The 80 / 10 / 10 Rule.** A slide should feel roughly 80% neutral, 10% gray structure, and 10% GitHub Green. If green becomes a fill color everywhere, the deck stops feeling like GitHub and starts feeling like a theme pack.

**The Purple Needs a Reason Rule.** Copilot Purple is allowed only when Copilot, AI agents, or an AI workflow is the subject. It is not a decorative alternate accent.

**The Compatibility Remap Rule.** Legacy deck colors are accepted only through the shared theme's root remap. New deck code should use the GitHub roles directly; old `--blue`, `--violet`, `--amber`, and `--primary` values exist so older inline styles land in the brand system.

## Typography

**Display Font:** Mona Sans (with `-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif`)
**Body Font:** Mona Sans (same stack)
**Label/Mono Font:** Mona Sans Mono (with `ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace`)

**Character:** A single-family brand system: Mona Sans carries both title authority and body clarity, while Mona Sans Mono supplies the GitHub engineering voice for code and metadata. The theme disables ligatures and avoids alternate widths, tracking tricks, and multiline uppercase mono.

### Hierarchy
- **Display** (500, `2.9em`, line-height 1): Cover titles inside `.gh-main h1`; maximum width stays narrow so the rail layout has a strong editorial block.
- **Divider Display** (500, `2.4em`, line-height 1): Section divider titles; paired with a green part number or muted part label.
- **Headline** (500, `1.2em`, line-height 1.12): Content-slide `h2`, with a 2px neutral rule underneath.
- **Title** (600, around `0.7em`): Card `h3`, tool row titles, feature names, and compact local headings.
- **Body** (400, around `0.7em`, line-height 1.4): Slide prose and list items; content is short and presentation-first rather than article length.
- **Label** (500, `15px` or deck micro sizes): Mono handles, tags, slide numbers, terminal prompts, table numbers, and URLs.

### Named Rules
**The Sentence-Case Brand Rule.** Headings are sentence case, not all caps. Mona's optical sizing does the work; letter-spacing stays near zero except the slight title/display tightening already in the theme.

**The Mono Is Evidence Rule.** Mona Sans Mono marks code, handles, prompts, counts, and URLs. It does not become a decorative headline style and never appears as multiline uppercase branding.

**The No-Ligature Rule.** Headlines and body disable ligatures so code terms, product names, and command text remain literal and presentation-safe.

## Layout

Reveal decks are rendered at 1280 × 720 with a compact presentation density. Ordinary content slides use the incumbent deck grids (`grid-2`, `grid-3`, `grid-4`) and compact card spacing, but the theme normalizes the stage to White, removes scenic backgrounds, and lets the content blocks carry the structure.

Ceremonial slides use the GitHub rail layout. `.gh-frame` fills the slide and creates a 184px rail plus a flexible main column. `.gh-rail` has a 2px GitHub Green right border, 56px top padding, 48px bottom padding, a 72px Invertocat or part number at the top, and four 72px contribution cells at the bottom. `.gh-main` uses 56px top padding, 64px right padding, 48px bottom padding, and 56px left padding, with the speaker card or tags anchored to the bottom via `.gh-foot`.

Text and visuals are separated by solid GitHub Green lines on ceremonial slides: the rail rule is the page spine, and the speaker card gets its own 2px green top rule. Content slides use 2px neutral rules under headings and around cards. Four contribution cells appear as light branding in the bottom-left chrome on ordinary slides and disappear on `gh-full` slides where the rail owns the brand mark.

## Elevation & Depth

This is a flat system. The shared theme deliberately remaps old shadow variables to `none`, removes card and terminal glows, and replaces gradient depth with tonal layers and 2px borders. Depth comes from field changes (White, Soft Gray, Black), contrast, and rules; not from floating surfaces.

### Named Rules
**The Flat Stage Rule.** A deck surface is either a stage, a card, a terminal, or a rail panel. None of those float by default; if a legacy slide asked for a shadow, the GitHub theme cancels it.

**The Border Reveals Structure Rule.** Use 2px neutral or green borders to reveal hierarchy. Do not use blur, glow, drop shadows, or glassmorphism to separate content.

## Shapes

The form language is GitHub presentation geometry: crisp rectangles softened just enough to feel modern. Cards and terminals use 12px corners; speaker photos and compact images use 8px; chips and buttons use 6px; contribution cells use larger 14px corners so they read as branded tiles. Bullets are small rounded contribution cells, not arrows or dots, and they preserve meaning without relying on color alone.

Borders are structural. The default line is 2px for slides, cards, screenshots, tables, terminal frames, progress elements, and rail rules. One-pixel borders are tolerated inside legacy content where the source already uses them, but new deck patterns should use the 2px vocabulary.

## Components

### Rail Cover / Divider / Closing
- **Shape:** Full-slide Black stage with a fixed 184px left rail and one 2px GitHub Green vertical rule.
- **Cover:** White Mona Sans title, key phrase in GitHub Green, short lede/subtitle, bottom tags, and a speaker card anchored bottom-right under a green rule.
- **Divider:** Green part number in the rail, centered title block, muted subtitle, and bottom part label.
- **Closing:** Black stage with a text-and-QR grid, green URL, white QR card, and the same rail/cell branding.

### Cards / Containers
- **Corner Style:** Gently rounded cards (12px).
- **Background:** White on content slides, Gray-5 on Black slides, Soft Gray for demoted details.
- **Shadow Strategy:** None; cards are separated by 2px borders and top rules.
- **Border:** Neutral 2px by default; top rules use green, purple, orange, or gray roles only when the category matters.
- **Internal Padding:** Compact presentation padding (`0.8em 1em`) with tight grid gaps.

### Chips / Tags / Pills
- **Style:** Mona Sans Mono, 500 weight, 6px radius, subtle filled background, 1px border, and no letter-spacing.
- **Green Variant:** Pale green fill with dark green text for success, GitHub, or running-agent labels.
- **Purple Variant:** Pale purple fill only for Copilot/AI run labels.
- **Amber Variant:** Pale orange fill for warning or no-AI/solo-estimate categories.

### Terminal Cards / Demo Prompts
- **Style:** Black terminal surface (`#0B0E0C`) with a 2px Gray-5 border, Gray-5 header, muted title, and Mona Sans Mono body.
- **Prompt:** GitHub Green prompt marker; command text is light neutral.
- **Copy Button:** Dark green button that turns bright green with Black text on hover or copied state; focus outline is GitHub Green.
- **Motion:** Copy micro-interactions may remain, but decorative float and pulse animations are disabled by the theme.

### Lists / Bullets
- **Style:** No browser bullets. Each item gets a small rounded GitHub Green contribution cell positioned at the text rhythm.
- **Dark Slides:** Text moves to light neutrals; bullets remain Green and must not be the only indicator of correctness or category.

### Deck Chrome
- **Slide Number:** Mona Sans Mono, 14px, bottom-left after the contribution cells, muted on both White and Black stages.
- **Progress:** 4px GitHub Green progress bar.
- **Controls:** Green controls, brighter on Black backgrounds.
- **Brand Cells:** Four contribution cells bottom-left on ordinary slides; hidden on full rail slides.

## Do's and Don'ts

### Do:
- **Do** load `../github-theme/github-slides.css` last in every deck so legacy inline styles are re-tokenised into the GitHub system.
- **Do** use White for ordinary content slides and Black (`#101411`) for cover, dividers, closing, demos, and night/conclusion slides.
- **Do** build new cover/divider/closing slides with `gh-full` plus `.gh-frame > .gh-rail + .gh-main`.
- **Do** use GitHub Green as the hero accent for rails, bullets, progress, and important emphasis, while keeping the slide mostly neutral.
- **Do** keep all text WCAG AA: use the dark green text role on White and bright green only for large/bold text or Black slides.
- **Do** separate text and visuals with solid Green or neutral 2px rules, not background effects.
- **Do** keep all factual talk content intact when re-skinning a legacy deck.

### Don't:
- **Don't** add gradient washes, gradient text, blue/violet keynote backgrounds, glow, glass, or shadow-based depth.
- **Don't** use Copilot Purple as general decoration; reserve it for Copilot/AI subject matter.
- **Don't** use alternate Mona widths, headline ligatures, broad tracking, or multiline uppercase mono treatments.
- **Don't** recolor the Invertocat, add effects to it, or use a low-contrast logo treatment; use white on Black or black on White.
- **Don't** rely on color alone for status, correctness, or category; pair color with labels, icons, text, or position.
- **Don't** edit generated `_site/` output or the root website `DESIGN.md` when changing this deck system.
