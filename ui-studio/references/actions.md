# Making the main action work without a backend

The person usually has no server, no database and no developer. The page's main action (order, book, enquire, register) must still work the day they publish it.

## Pick the route, in this order
1. **They already use a tool** (Square, Toast, Shopify, Calendly, Eventbrite, Google Forms, OpenTable): link the main button straight to it, or embed it if the tool gives embed code. Ask for the link in Step 1 if it isn't on hand; until it arrives, use route 2.
2. **Email hand-off (default):** the visitor makes structured choices on the page, then the button opens their email app with a message to the business already written. Works everywhere, costs nothing, and the owner gets a readable order in their inbox.
3. **Text or call:** on phone-first businesses (salons, trades, food trucks), an `sms:` link with the message prefilled, plus a tappable `tel:` number.
4. **A form service** (Formspree, Basin, Netlify Forms) when receipt really matters or volume is high: orders arrive even if the visitor has no mail app. It needs a free account only the owner can create, so build the email hand-off now, keep the form ready, and explain the one-line switch in the hand-off.

Payments are never taken on a static page: link to their payment or shop tool (Square, Stripe Payment Links, Shopify).

## Rules
- Say what will happen next to the button: "Opens your email with the order filled in. We reply to confirm."
- Once the real address or number is known, show it as text too, for visitors whose device has no mail app.
- If it isn't known yet, put an obvious placeholder (`orders@yourbakery.com`) in one constant in the code only, keep it off the visible page, and list it first in the hand-off under "Replace before publishing". Never invent a real-looking address.
- Use the right word for what really happened: **started** (their email app opened), **sent** (a service accepted it), **confirmed** (the business replied). The page can only ever claim "started" for an email hand-off.
- Never show success ("Order received!") for something the page didn't actually send.
- Test it: press the button in the rendered page and check the generated email (recipient, subject, every line of the order). After opening the email, say "Your email app should have opened. Press send to place the order."
- Keep the structured choices (items, quantities, day, time) and a live summary; the email body repeats them in plain lines.

## Email hand-off pattern

```html
<form id="order">
  <!-- choices: quantities, day, name ... -->
  <button type="submit">Email my pre-order</button>
  <p class="hint">Opens your email with the order filled in. We reply to confirm.</p>
  <!-- once the real inbox is known, add: Or email <a href="mailto:...">...</a> -->

  <p role="status" id="order-status"></p>
</form>
<script>
{
  const TO = "orders@yourbakery.com"; // REPLACE with the real order inbox
  const f = document.getElementById("order");
  f.addEventListener("submit", (e) => {
    e.preventDefault();
    const lines = [...f.querySelectorAll("[data-item]")]
      .filter((i) => +i.value > 0)
      .map((i) => `${i.value} x ${i.dataset.item}`);
    if (!lines.length) { document.getElementById("order-status").textContent = "Add at least one item first."; return; }
    const day = f.querySelector("[name=day]:checked")?.value || "";
    const name = f.querySelector("[name=name]")?.value || "";
    const body = [`Pre-order for ${day} pickup`, "", ...lines, "", `Name: ${name}`].join("\n");
    location.href = `mailto:${TO}?subject=${encodeURIComponent("Pre-order: " + day)}&body=${encodeURIComponent(body)}`;
    document.getElementById("order-status").textContent = "Your email app should have opened. Press send to place the order.";
  });
}
</script>
```

For `sms:` use `sms:+15555550123?&body=` + the encoded text (the `?&` form works on both iPhone and Android).
