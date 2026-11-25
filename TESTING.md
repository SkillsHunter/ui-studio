# Testing

## Method
Each test used one plain-language brief from a small business owner. One person (Claude) built the page five times, following each skill's instructions as written:

- UI Studio
- Anthropic's frontend-design
- Hallmark
- Impeccable
- UI/UX Pro Max

Each page was rendered at 1440×900 and 390×844 with its fonts loaded. Screenshots of the first screen and the full page went to an AI judge in a temporary chat, labelled only with letters, and the labels were reshuffled for every round. The judge looked through three lenses: the business owner, a senior product designer, and a customer on a phone. It then ranked the five and scored each one out of 10. The judge was told that missing names, photos and prices were placeholders in every version and shouldn't count against any of them.

Briefs A and B were used to develop the skill, so UI Studio was revised after seeing those results. Briefs C and D were held out: nothing in the skill changed until their results were in.

## Results with ChatGPT as the judge (scores out of 10)

| Brief | Round | UI Studio | frontend-design | Hallmark | Impeccable | UI/UX Pro Max |
|---|---|---|---|---|---|---|
| A bakery (development) | v1 | 8.3 | **8.7** | 7.1 | 7.8 | 6.8 |
| A bakery (development) | v2 | **9.0** | 8.5 | 8.7 | 7.6 | 7.0 |
| A bakery (development) | v2, rejudged | **8.8** | 8.6 | 7.8 | 7.2 | 8.0 |
| B soccer schedule (held out for v3) | v3 | 8.0 | 7.6 | 8.5 | **9.0** | 7.1 |
| B soccer schedule (then development) | v4 | **9.0** | 7.7 | 8.4 | 8.0 | not captured |
| B soccer schedule (then development) | v4, rejudged | **8.7** | not captured | 8.1 | 7.9 | not captured |
| C bookkeeper (held out for v4) | v4 | 8.8 | **9.2** | 7.3 | 8.3 | 7.7 |
| C bookkeeper (held out for v4) | v4, relabelled | 8.7 | **9.0** | 7.9 | 8.3 | 7.5 |

## Brief D, judged by three models (v5)
Brief D was a one-woman mobile dog groomer in Arlington, Virginia, who takes bookings by text. Each judge saw the same five pages with a fresh label order every round.

| Judge | Rounds | UI Studio | frontend-design | Impeccable | Hallmark | UI/UX Pro Max |
|---|---|---|---|---|---|---|
| ChatGPT, default model | 3 | 8.50 | **8.53** | 7.40 | 7.53 | 7.93 |
| ChatGPT, Thinking | 2 | 8.60 | **8.85** | 7.85 | 7.65 | 7.65 |
| Gemini, everyday model | 2 | **8.90** | 8.15 | 7.50 | 6.70 | 4.95 |
| **All 7 rounds** | 7 | **8.64** | 8.51 | 7.56 | 7.33 | 7.00 |

UI Studio came first in 4 of the 7 rounds. It beat Hallmark, Impeccable and UI/UX Pro Max in 6 of the 7.

## What the results do and don't show
- **Against Hallmark, Impeccable and UI/UX Pro Max,** UI Studio scored higher in almost every round since v2, on briefs it had and hadn't seen.
- **Against Anthropic's frontend-design,** it's a tie within the judges' noise. Gemini preferred UI Studio, ChatGPT Thinking preferred frontend-design, and ChatGPT's default model was even.
- **The judges are noisy.** One unchanged page scored 7.7, 9.1 and 8.7 across three ChatGPT rounds. Another scored 7.1, 8.7 and 7.8. Single rounds prove little.
- **The comparison may favour UI Studio.** The same person built every page, including the ones for the other skills.
- **Two of the other skills ran with handicaps.** Impeccable ran without its compiled engine, because the download was blocked in the test environment. Hallmark couldn't load its photo library. Hallmark and UI/UX Pro Max did run their own scripts.
- **No real customers were involved.** The judges are AI models looking at screenshots. Nobody has yet measured whether these pages bring in more orders or calls.

## What changed because of the tests
See [`CHANGELOG.md`](CHANGELOG.md). Each version answers a specific loss: a disabled order button, missing field addresses, a list of tasks in place of a sample of the result, and extra features the owner would have had to maintain.

## Not yet tested
- Version 0.5.1 on a new brief
- Real people choosing between versions without labels
- A real business publishing a page and counting enquiries
- `check.py` inside the Claude app's own code environment
- How reliably the skill is picked up automatically, compared with asking for it by name

## How to rerun
Write a short brief in a business owner's words. Build it with each skill in a fresh chat, screenshot each page at laptop and phone sizes, and give the screenshots to a judge model with letter labels only. Reshuffle the labels and run at least two rounds per judge. Please share your results in an issue.
