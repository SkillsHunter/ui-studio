# Type and colour

## Choosing type

Choose the face from the subject's world, not from habit. One family can carry a whole page; two must be clearly different (e.g. a characterful display face and a quiet text face). Load from Google Fonts unless the person has brand fonts.

Avoid as the page's voice unless asked: Inter, Roboto, Open Sans, Poppins, Montserrat, Lato, Raleway, Nunito, DM Sans, Arial/Helvetica/system. Use sparingly because every model already reaches for them: Playfair Display, Cormorant Garamond, Fraunces, Instrument Serif, DM Serif Display, Young Serif, Recoleta, Space Grotesk, Bebas Neue.

A good test: the display face should echo something you could photograph in the subject's world (a shop sign, packaging, a ticket, a jersey, a menu board, a book spine). Name the object when you choose it.

Starting points by feeling (display / text). These are examples, not a catalogue: any good face that fits the subject is welcome, and unrelated projects should not end up looking related.

| Feeling | Display | Text |
| --- | --- | --- |
| Warm, handmade, generous (food, shops, makers) | Bagel Fat One, Alfa Slab One, Rammetto One, Gloock | Figtree, Karla, Source Serif 4 |
| Classic, trustworthy, literary | EB Garamond, Cardo, Castoro | Newsreader, Literata, Source Serif 4 |
| Confident, editorial, premium | Libre Bodoni, Besley, Gloock | Hanken Grotesk, Spectral |
| Modern, precise, product | Rethink Sans, Albert Sans, Onest | IBM Plex Sans, Public Sans, Golos Text |
| Bold, loud, sporty, events | Anton, Antonio, Archivo Black, League Spartan | Archivo, Chivo |
| Friendly, playful, kids, community | Bricolage Grotesque, Gochi Hand (accents only), Shantell Sans | Figtree, Lexend |
| Technical, developer | Space Mono or JetBrains Mono for code only; display in Rethink Sans or Archivo | IBM Plex Sans |
| Calm, wellness, care | Marcellus, Cormorant (sparingly), Castoro | Karla, Figtree |
| Dashboards and tools (Operate) | One family: IBM Plex Sans, Public Sans or Golos Text, with tabular numbers | same |

Set a clear scale: body 16–18px; each step up about 1.25–1.5×; display headlines up to about 6rem on desktop and scaled with `clamp()`. Headlines: tight line-height (1.0–1.15), slight negative tracking for big sizes, `text-wrap: balance`. Body: line-height 1.5–1.65, 45–75 characters per line, `text-wrap: pretty`. Use `font-variant-numeric: tabular-nums` for prices and tables. Sentence case for labels and buttons.

## Building colour

1. **Pick one anchor colour from the subject's world** (the crust of the bread, the client's logo, the river by the office, the team's kit). Not from habit.
2. **Make neutrals that lean toward the anchor**: a background, a surface one step off it, body text, muted text, borders. Avoid pure #000/#fff; tint them slightly (OKLCH chroma ~0.005–0.02 toward the anchor hue).
3. **Choose how much colour the page carries** ("posture"): *restrained* (anchor only on actions and a few accents, under ~5% of the screen), *committed* (one or two big fields of the anchor, e.g. a coloured hero band), or *drenched* (the anchor is the background). Pick one on purpose.
4. **Give every coloured surface its own text colour** that passes contrast (`--accent` and `--on-accent`). Never grey text on a coloured surface.
5. Light or dark is decided by where and when the page is used, not by the category.
6. Check contrast on real pairs: 4.5:1 for body text, 3:1 for large text, icons and focus rings.

Write colours as tokens: `--paper`, `--surface`, `--ink`, `--ink-muted`, `--line`, `--accent`, `--on-accent`, plus `--danger`/`--ok` for app UI.
