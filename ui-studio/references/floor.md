# The quality floor

Build every page to this without announcing it. These are pass/fail; the checker tests the starred (*) ones.

## Works on every screen
- * No sideways scrolling at any width from 320px to 1920px. Put `overflow-x: clip` on `html` and `body`; never `width: 100vw`.
- * Persuade pages: the headline, the supporting sentence and the main action are visible without scrolling on a 1280×800 laptop and a 390×844 phone. Other modes: the first screen shows the most important content or task (today's schedule, the form, the article), never a decorative hero.
- Content width is capped (about 1200–1440px) and centred on big screens; reading text stays 45–75 characters per line.
- Tap targets at least 44×44px on phones, with space between them. Body text at least 16px.
- The phone is a first-class layout, not a squeezed desktop: time-sensitive information first, wide tables become stacked rows, phone numbers and addresses are tappable links, nothing relies on hover, the whole main task can be done one-handed.
- Grids that hold images use `minmax(0, 1fr)`; long headings can wrap (`overflow-wrap: break-word`).
- Heroes sized with `svh`/`dvh`, never `vh`, so phone browser bars don't hide content.

## Everyone can use it
- * Text contrast at least 4.5:1 (3:1 for large text and icons) against what's actually behind it.
- * Every link, button and field shows a clear focus ring (`:focus-visible`) for keyboard users; never remove outlines without a replacement.
- * Images have `alt` text (empty `alt=""` for pure decoration); decorative SVGs get `aria-hidden="true"`.
- * One `<h1>`, headings in order, real `<button>` and `<a>` elements, labels on every form field (not just placeholders), `lang` on `<html>`.
- * Every animation has a `prefers-reduced-motion: reduce` fallback, and the page is fully visible if scripts fail (never hide content with `opacity: 0` waiting for JavaScript).

## Feels finished
- Every control has its states: hover, focus, active, disabled; forms have error and success states that are honest about whether anything is connected.
- Space has rhythm: tighter inside groups, more between them, more space above a heading than below it.
- One primary button style. One container width. One radius per level of nesting.
- Theme the small browser surfaces: text-selection colour, focus ring, link underline offset, scrollbar on dark pages.
- Fonts load only the weights used, with `display=swap` and a `preconnect`.
- Motion: at most one deliberate moment (a page-load reveal or a reaction to the visitor's action), using `transform`/`opacity`, ease-out, 150–400ms.

## Honest
- * No invented numbers, quotes, logos or reviews; placeholders are visibly placeholders.
- * The main action works today (email/text hand-off, phone link, or their existing tool), is never disabled for visitors, and never fakes success. See `actions.md`.
- Photo placeholders say what photo belongs there.
