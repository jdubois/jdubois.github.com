---
target: conferences page
total_score: 34
p0_count: 0
p1_count: 1
timestamp: 2026-06-24T13-54-19Z
slug: conferences-html
---
# Critique: Conferences page (conferences.html)

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | Chevron + hover-lift signal open/closed clearly |
| 2 | Match System / Real World | 4 | Plain-language section labels |
| 3 | User Control and Freedom | 4 | Native <details>, free expand/collapse |
| 4 | Consistency and Standards | 3 | Talk titles are <h2>, same level as section headers — flattened outline |
| 5 | Error Prevention | 3 | n/a (no forms/destructive actions) |
| 6 | Recognition Rather Than Recall | 4 | Everything visible/labeled |
| 7 | Flexibility and Efficiency | 3 | EN/FR slide links (the real CTA) buried behind collapse; no expand-all |
| 8 | Aesthetic and Minimalist Design | 4 | Clean, brand-consistent, uncluttered |
| 9 | Error Recovery | 3 | n/a |
| 10 | Help and Documentation | 3 | Disclaimer <em> + Contact me section |
| **Total** | | **34/40** | **Strong** |

## Anti-Patterns Verdict
- LLM assessment: Does NOT read as AI slop. Native <details>, full borders (no side-stripes), one accent color, brand-consistent.
- Deterministic scan: detect.mjs on conferences.html returned `[]` (clean).
- Browser evidence: no horizontal overflow at 320/360/375px; live render correct.

## What's Working
1. Native <details>/<summary> collapsibles — correct affordance, no JS, accessible, reduced-motion guarded.
2. Brand-consistent restraint — site tokens reused, full borders, single blue accent.
3. Section IA — Contact me first, then talks, videos, workshops, presentations: logical scan order.

## Priority Issues
- [P1] Heading-level flattening: talk titles are <h2>, siblings of section headers (Contact me, Videos...). Should be <h3> under "Current talks." Breaks document outline / screen-reader heading nav.
- [P2] Primary CTA buried: EN/FR slide links live inside the collapsed body. The decks are the strongest proof for a booking organizer but sit two clicks deep. Surface a "slides" hint or the links in the summary.
- [P3] Muted body color: talk descriptions use --text-secondary (#6b7280, ~4.83:1) — passes AA but light for primary content; consider --text-primary.
- [P3] Desktop right column empty below the hero photo; lower sections feel unbalanced.

## Persona Red Flags
- Event organizer (booking decision): must click to expand AND click again to view slides — strongest asset (polished decks) is two clicks deep.
- Mobile visitor: clean, no overflow, titles wrap to 2 lines acceptably. No red flags.

## Minor Observations
- No textual expand cue / expand-all; chevron is the only signal.
- Two collapsibles is a list, not a card grid — not the banned "identical card grid."
