# Where the rules come from

UI Studio was written from scratch. Some rules come from studying four open design skills, and the rest come from losses in blind tests (see [`TESTING.md`](TESTING.md)). The ideas below are credited to their source. No code or text was copied.

## From the four skills studied

| Source | Idea used in UI Studio |
|---|---|
| [Anthropic frontend-design](https://github.com/anthropics/skills) | Ground the look in the subject's own world. Write a short plan, then review it against the brief before building. Spend boldness in one place. Name the common AI-made defaults so they can be avoided. Take one thing away before you finish. |
| [Hallmark](https://github.com/nutlope/hallmark) (MIT) | Never invent facts. Build to a mechanical quality floor. Choose sections by what the visitor needs to do. Check the page with a lint script before handing it back. |
| [Impeccable](https://github.com/pbakaus/impeccable) (Apache-2.0) | Set the boldness by mode: Persuade, Operate, Read or Show. Treat the first screen as the page's argument. Use clearly labelled demonstration data instead of hiding a feature. Craft-floor checks. |
| [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) (MIT) | A pre-delivery checklist covering contrast, focus, reduced motion and responsive sizes. Name the colours, type and layout decisions before building. |

## From losses in blind tests

| Loss | Rule it produced |
|---|---|
| v1 showed an honest but disabled "ordering not switched on yet" button and lost. | The main action works on day one, through a tool the owner already uses or an email or text hand-off. Never a disabled button or a "coming soon" notice. |
| v1 looked tasteful but anonymous. | The neighbour and squint tests, and the "premium hospitality" look added to the avoid list. |
| An outside review by ChatGPT found the owner had no easy way to update the page. | One editable content block. Delivery levels (information, interactive, connected). A phones-first rule. A design-director review of the screenshots. A plain-English hand-off. |
| v3 left out field addresses, hid a feature that had no content yet, and looked like an admin portal. | A checklist of everything the request asks for. Public facts looked up from official sources. Design the filled-in page with labelled samples. The admin-dashboard look added to the avoid list. |
| v4 listed a bookkeeper's monthly tasks but never showed what the client receives, and repeated "book a call" in every section. | Show one sample of what the customer gets. Ask once. |
| v5 promised "2 slots left" counts and a booking-style form that the owner would have to maintain. | Only promise what the owner will keep up. Add nothing the owner didn't ask for. |

## Not verified
- Whether any rule improves real business results. The tests measured AI judges' opinions of screenshots, not orders or calls.
