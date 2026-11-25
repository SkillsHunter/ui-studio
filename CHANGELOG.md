# Changelog

## 0.5.2 (unreleased)
The skill's instructions are unchanged. This release hardens the checker and the way the skill is shipped.

**Releases**
- Release zips are built by GitHub Actions from `ui-studio/` and published on the Releases page with `SHA256SUMS` and a signed build provenance attestation. The zip is no longer committed to the repository.
- New `ui-studio-single-file.zip`: the skill as one `SKILL.md` with the references inlined as appendices, generated from the same source so the two can't drift apart.
- Builds are reproducible: the same source always gives byte-identical zips.
- Line endings are normalised to LF (`.gitattributes`).

**Checker (`check.py`)**
- While rendering, the page may load only local files and Google Fonts; other requests are blocked and listed. `--allow-network` turns this off.
- Screenshots go to `.ui-studio-check/` next to the page instead of beside it.
- Fixed: tags with no closing tag (`<img>`, `<br>`, `<input>`) broke the arrow and emoji checks for buttons and links.
- Fixed: placeholder names matched inside longer words ("John Smithson", "Acmeville").
- Proper command-line parsing: an unknown `--mode` or a flag with no value now gives a clear error instead of a crash.
- Clear errors (exit code 2) for a missing file, a file that isn't UTF-8, or a file over 5 MB.
- Says when it fell back to your installed Chrome.
- `--json` now uses the same exit codes as the normal output (1 when there is a MUST FIX).

**Project**
- Tests (pytest), linting (ruff), CI on Linux, Windows and macOS, Dependabot, and a security policy.

## 0.5.1 (2026-11-25)
First public version.
- **Only promise what the owner will keep up:** stable facts (days, areas, hours) over figures that change daily, such as "2 slots left".
- **Nothing the owner didn't ask for:** no live availability, booking-style forms, review sections or embedded maps unless requested. The main action is the simplest thing that gets the owner a useful message.
- These two rules came from Gemini and ChatGPT Thinking independently naming the same weakness. They haven't been tested yet.

## 0.5.0 (2026-11-24)
- **Show what the customer gets:** one concrete sample of the result (a report, a groom card, a schedule) with its timing, instead of only a list of tasks.
- **Ask once:** one main button near the top and one at the end, with plain links everywhere else.

## 0.4.0 (2026-11-23)
- A checklist of everything the request asks for, checked against the finished page.
- Public facts, like a park's street address, looked up from official sources.
- The filled-in page designed with labelled sample content instead of hiding features.
- A "last updated" time on anything that changes.
- Operate-mode pages carry their identity in one bold element. The admin-dashboard look added to the avoid list.

## 0.3.0 (2026-11-23)
After an outside review:
- An editable content block for the owner.
- Delivery levels: information site, interactive page, or connected app.
- The visitor's top three jobs decide the sections.
- Phones-first rules.
- A design-director review of the screenshots.
- A plain-English hand-off.
- Checker upgrades: script errors, broken links, placeholder emails.

## 0.2.0 (2026-11-23)
- The main action works with no back end, through an email or text hand-off. Never a disabled button.
- The squint test, and the "premium hospitality" look added to the avoid list.

## 0.1.0 (2026-11-23)
First draft, built from studying Hallmark, Impeccable, UI/UX Pro Max and Anthropic's frontend-design.
