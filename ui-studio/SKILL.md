---
name: ui-studio
description: Designs and builds web pages and app screens that look professionally designed and work on day one, for non-technical people. Use when asked to design, build or improve a website or interface.
---

# UI Studio

The person asking may never have written code. Hand them a finished page they can open, judge with their own eyes, publish, and keep up to date, without running a command or learning a design term. You do the design thinking, the building and the checking. They supply what only they know: the facts, the photos, the taste.

## Rules that never bend

1. **Never invent a fact.** No made-up prices, reviews, testimonials, customer counts, awards, logos, people, addresses, hours or deadlines. Public facts about places or things they named (a park's street address, a venue's map location) may be looked up from an official source if you can browse; name the source in the hand-off. Anything else missing is shown as clearly labelled sample content and listed in the hand-off.
2. **The person's words win.** A colour, font, style or layout they name is used, even if it's on the avoid list.
3. **Look before you hand back.** Render the page and use it at phone and desktop width before saying it's done. If you can't render, say so plainly.
4. **No homework.** Never ask them to install, run or configure anything. Account sign-ups and approvals that only they can do are named in the hand-off, in plain words.
5. **Honest status.** Never show visitors a disabled main button, a "coming soon" notice, or a success message for something that wasn't actually sent.
6. **Editing is not redesigning.** On an existing page, keep its look, words and structure unless they asked for a redesign.

## Step 1: Understand (one message)

Use what is already on hand first: attached files, an existing site or project, a brand guide, photos, earlier conversation. If core facts are still missing, ask once, in one short message:

> Before I design this, a few quick things (answer any, or say **go ahead** and I'll make sensible choices and tell you what I picked):
> 1. **What should a visitor do?** (call, book, order, sign up, check a schedule, read…)
> 2. **Who are they?** (e.g. "parents on their phones at the field", "finance managers at mid-size firms")
> 3. **What real material do you have?** Photos, logo, prices, hours, a real customer quote with their name, and where orders or messages should go (an email, a number for texts, or a tool like Square or Calendly).
> 4. **How should it feel?** A word or two (warm, bold, calm, premium, playful, serious…) and any colour you love or hate.

If they skip or say "go ahead", infer and state your guesses in one line at the top of your reply. Ask one focused follow-up only if a missing answer would make the result unusable or misleading (e.g. an order page with nowhere for orders to go); otherwise make a reversible assumption and say so.

## Step 2: Decide what it's for and what it must do

Write, briefly:
- **Everything the request explicitly asks for**, as a checklist (e.g. "this Saturday's games, field addresses, rain cancellations"). Every item must be on the finished page, findable in seconds.
- **The visitor's top three jobs** (e.g. "see if Saturday's game is on", "find the field", "know who to contact").
- **What must stay current** and how often (hours, prices, schedules, menus, cancellations). Only promise what the owner will really keep up: prefer stable facts (which days, which areas, opening hours) over figures that change daily, such as "2 slots left", unless they asked for them.
- **What must actually work** (order, book, register, contact) and where it goes (see `references/actions.md`).
- **The delivery level:** *information site* (content and links), *interactive page* (works in the browser, no shared data), or *connected app* (logins, stored records, payments, bookings). A static page is never presented as a connected app. Payments, accounts and children's personal data go through an established service, never an improvised form; say what that service would be and what it costs.
- **The mode**, which sets how bold to be: **Persuade** (landing pages, small-business sites, pricing: earn attention, then action), **Operate** (dashboards, tools, schedules, forms: get the task done fast with familiar patterns; the identity lives in one bold element such as the status board, the club's colours or the type, never in a stack of generic cards), **Read** (articles, docs, guides: comfortable reading), **Show** (portfolios, galleries: the work leads).

Build the sections from the jobs. `references/page-anatomy.md` shows how real sites in common categories are organised; use it as a starting point, not a template.

## Step 3: Plan the design (show it in a compact block)

- **Directions:** sketch three genuinely different directions in one line each (different composition, type, colour posture), then pick the one that best fits the jobs and the subject. Say why in a sentence.
- **Feel:** two or three words and the idea behind them.
- **Colour:** 4–6 named colours with hex values, from one anchor colour taken from the subject's world. See `references/type-and-colour.md`.
- **Type:** one or two typefaces chosen for this subject, naming the real-world object their shapes echo (a shop sign, a ticket, a jersey, a label).
- **Layout:** the order of sections, how the first screen is composed, and how it changes on a phone.
- **Signature:** the one element a visitor will remember and couldn't see on a competitor's site, taken from the subject's own world (its products set large, its menu board, its fixture list, its map). It must help recognition or the main task, never just decorate.
- **Pictures:** where each image comes from (theirs, a screenshot of their real product, or a labelled placeholder). The design must look finished with or without the photos.

**Before building, two quick tests.** *Neighbour:* would a similar business get almost this plan from you? If so, change the weakest decision. *Squint:* with the words blurred, does it still say what kind of business this is and that it's *this* one? Tasteful-but-anonymous fails. Then check the plan against `references/avoid.md`.

Show the plan (they can redirect), then build without waiting unless the job is large.

## Step 4: Build

- **One self-contained `index.html`** (CSS and script inside) unless they already have a project in a framework; then work inside it and its conventions.
- **Design the filled-in page, not the empty one.** Every feature appears as it will in real use: when the owner hasn't supplied the content yet, fill it with clearly labelled sample content (one visible "Sample: replace with yours" note per section, and the samples listed in the hand-off) rather than hiding the feature. Anything time-sensitive (a status, a cancellation, today's specials) shows when it was last updated and by whom.
- **Show what the customer gets, not just what you do.** For a service, put one concrete example of the result on the page: a sample of the report, plan, schedule or finished work the client receives, with the timing ("by the 10th of each month"), so a visitor can picture it. A list of activities is not enough. Label it as a sample if the owner hasn't supplied the real one.
- **Ask once, clearly.** One main button in the hero and one at the end; elsewhere, plain links. Repeating the same invitation in every section reads as a template.
- **Nothing the owner didn't ask for.** Don't add features, required choices or promises that create work for them (live availability, booking-style forms, review sections, maps to embed). The main action should be the simplest thing that gets the owner a useful message: a few optional taps that prefill it beat a form.
- **Content the owner can edit.** Anything that changes (hours, prices, products, schedules, dates, cancellations, contact details) lives in one clearly labelled block at the top of the file, in plain words or a simple list, and the page is built from it. A routine update must never mean touching CSS or layout code.
- **Tokens first.** Every colour, font, spacing step and radius is a CSS custom property; use only those below.
- **Real words.** Plain language from the visitor's side. Buttons say exactly what happens ("Email my pre-order", not "Get started"). Headlines short and specific. No buzzwords.
- **The main action works on day one.** Use their existing tool, or the email or text hand-off in `references/actions.md`, with structured choices (items, quantities, days, times) and a live summary instead of free-text boxes. Tell the visitor exactly what happens next.
- **Phones first.** The most time-sensitive information is the first thing on a phone. Wide tables become stacked rows. Phone numbers, addresses and actions are tappable. Nothing depends on hover.
- **Findable.** A real `<title>` and meta description, Open Graph tags, and for local businesses `LocalBusiness` structured data using only facts they gave.
- **Quality floor, built in:** read `references/floor.md` once before building.

## Step 5: Look, use, fix

1. **Run the checker** if you can run code: `python3 <skill-dir>/scripts/check.py <file.html> --mode <persuade|operate|read|show>`. It renders the page at several sizes when a browser is available, saves screenshots, and lists problems in plain language. Fix every **MUST FIX**; decide on each **CONSIDER**.
2. **Do the main task yourself** in the rendered page, on the phone size: find the key information, use the controls, press the main button and confirm what it produces (for an email hand-off, the subject and body are right). Check every nav link lands somewhere.
3. **Look at the screenshots like a design director:**
   - *Composition:* are scale, alignment and white space deliberate?
   - *Hierarchy:* in three seconds, is it clear what this is and what to do?
   - *Specificity:* would it still belong to this business with the name removed? Compare it against the looks in `references/avoid.md`; if it resembles one (the admin-dashboard card kit, the premium-café look, the SaaS landing page), it fails.
   - *Craft:* are crops, type sizes, spacing and the phone layout finished?
   - *Restraint:* does every prominent element earn its place?
   If two fail, revise before going further.
4. **Remove one thing:** the least necessary decoration or sentence. Never essential information.
5. Fix in one batch, look once more, then hand back. Name anything you couldn't fix or test.

If you can't run code or render, walk `references/floor.md` by reading the code, and tell them you couldn't view or use it rendered.

## Step 6: Hand it over

Short, plain English, following `references/handoff.md`:
- **What you made** in a line or two, and the file.
- **What you assumed**, if they said "go ahead".
- **Replace before publishing:** where orders or messages go first, then each placeholder and what belongs there.
- **How to update it:** where the content block is and one worked example ("to cancel a game, change `on` to `cancelled` next to it").
- **How to publish:** the simplest route for them, and any account or cost involved.
- **The one thing that would improve it most** (usually real photos or a real customer quote).

## Changing an existing page

Read it fully; keep its look, words and structure; change only what was asked. For "make it look better": run the checker, fix floor problems, then make the two or three changes with the biggest effect (first-screen hierarchy, spacing, type and colour discipline) and say what you changed. For "redesign it": keep every fact and working feature, and restart from Step 3.
