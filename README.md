# UI Studio

A Claude skill for people who don't write code. Describe the website or app screen you need in plain words. You get back a finished page you can open, check with your own eyes, publish, and keep up to date.

| You say | You get |
|---|---|
| "Make a website for my bakery where people can pre-order for Saturday." | One page with a working order button. It opens the customer's email with the order already written, so it works without a server or an online shop. |
| "I coach a kids' soccer team. Parents need this week's games, the field addresses and rain cancellations." | A schedule page with real field addresses, looked up from official sources, and a status at the top. You update it by changing one word. |
| "I'm a bookkeeper. I want owners to understand what I do and book a call on my Calendly." | A page that shows what a client receives each month, with the booking button going straight to your Calendly. |
| "Make my existing page look better." | The same page and the same words, with the layout, spacing and type fixed. You get a short note on what changed. |

## What makes it different
- **The main button works on the day you publish.** It links to a tool you already use (Calendly, Square, Google Forms). If you don't have one, the button opens the visitor's email or text app with their request already written. Visitors never see a disabled button or a "coming soon" notice.
- **You can keep it up to date yourself.** Hours, menus, schedules and prices sit in one plain block at the top of the file. Changing them never means touching the design.
- **It doesn't invent facts.** No made-up reviews, prices, addresses or customer numbers. Anything missing is shown as clearly labelled sample content, and the hand-off note lists what to replace.
- **It checks your request.** It lists everything you asked for and confirms each item is on the page.
- **It looks like your business, not a template.** Colours and type come from your business's own world: a menu board, a team kit, a delivery van. Common AI-made looks are on an avoid list.
- **It looks before it hands back.** It renders the page at phone and desktop sizes, uses the main button itself, and reviews the screenshots before calling the page done.
- **It hands over in plain English.** You get how to publish, how to update, and how to get found on Google.

## Install

**Claude app or claude.ai**
1. Download [`ui-studio.zip`](https://github.com/SkillsHunter/ui-studio/releases/latest/download/ui-studio.zip) from the latest release. Don't unzip it.
2. Open **Customize → Skills**, click **Add** (or **+**), and choose **Upload skill**.
3. Pick the zip and make sure the skill is switched on.

Skills need code execution and file creation turned on. If Skills is missing or greyed out, check that setting. On Team and Enterprise plans, an admin may need to enable it.

**Claude Code**
Unzip the same release zip into `~/.claude/skills/`. You should end up with `~/.claude/skills/ui-studio/SKILL.md`.

**Check your download (optional)**
Every release is built by GitHub Actions straight from the tagged source, never by hand. Each one comes with a checksum file and a signed record of how it was built:

```
sha256sum -c SHA256SUMS
gh attestation verify ui-studio.zip --repo SkillsHunter/ui-studio
```

The release also includes `ui-studio-single-file.zip`: the same skill as one `SKILL.md`, with the references as appendices and no checker. It's generated from the same source.

## The optional checker
`ui-studio/scripts/check.py` checks a page for problems and lists them in plain language. Some checks work with plain Python 3: placeholder text, buzzwords, missing labels, broken links, a disabled main button. If Playwright and Chromium are installed, it also renders the page at five screen widths and checks overflow, contrast, the first screen, tap-target sizes and script errors, and it saves screenshots to `.ui-studio-check/` next to the page. Claude runs it for you when it can; you never need to run it yourself.

```
python3 ui-studio/scripts/check.py index.html --mode persuade
```

| Option | What it does |
|---|---|
| `--mode persuade\|operate\|read\|show` | What the page is for (default `persuade`) |
| `--out DIR` | Save screenshots somewhere else |
| `--json` | Machine-readable output |
| `--allow-network` | Let the page load anything while rendering. By default only local files and Google Fonts load, so a page you didn't write can't contact other sites. |

Exit codes: `0` nothing to fix, `1` at least one MUST FIX, `2` the check couldn't run (missing file, not UTF-8, larger than 5 MB). To enable rendering: `pip install -r requirements-render.txt` then `python -m playwright install chromium`.

## What it does and doesn't do
- It builds one self-contained `index.html` unless you already have a project. If you do, it works inside your project's conventions.
- It never takes payments or stores personal data on a static page. When you need those, it names an established service and says what it costs.
- It doesn't claim a page is live unless you have published it.
- Its accessibility checks follow common practice, but they aren't a legal certification.

## Known limits (version 0.5.2)
- In blind tests, AI models judged screenshots. No real visitors were involved. One person built every test page by following each skill's instructions, so the comparison may favour this skill.
- Version 0.5.1 added two rules after the last tests, and they haven't been tested yet. Version 0.5.2 changes only the checker and the release process, not the skill's instructions.
- There is no evidence yet that pages built with it bring in more orders or calls. That needs a real business using it.

Test details are in [`TESTING.md`](TESTING.md). Where each rule came from is in [`EVIDENCE.md`](EVIDENCE.md).

## Problems or ideas
Open an issue using the template. Include your prompt, which Claude app you used, and a screenshot of the result if you can. For security problems, see [`SECURITY.md`](SECURITY.md) and report privately.

## Developing
`ui-studio/` is the only source of truth. Release zips are built from it and never committed.

```
pip install -r requirements-dev.txt
ruff check .
python -m pytest                # rendering tests skip unless Playwright and Chromium are installed
python tools/build.py           # validates the source and writes dist/ with checksums
```

To release, add a `## x.y.z` entry at the top of `CHANGELOG.md` and push a matching `vx.y.z` tag. GitHub Actions tests, builds, attests and publishes it.

## Credit
UI Studio was written from scratch after studying four open design skills: [Hallmark](https://github.com/nutlope/hallmark), [Impeccable](https://github.com/pbakaus/impeccable), [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) and Anthropic's frontend-design skill. It borrows ideas from them, not code or text. [`EVIDENCE.md`](EVIDENCE.md) says what came from where.
