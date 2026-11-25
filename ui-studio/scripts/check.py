#!/usr/bin/env python3
"""UI Studio checker: plain-language quality checks for one HTML page.

Usage: python3 check.py page.html [--mode persuade|operate|read|show] [--out DIR] [--json]

Runs static checks with the standard library. If Playwright and a Chromium
browser are available, it also renders the page at phone and desktop sizes,
checks layout, contrast and the first screen, and saves screenshots.
Nothing is sent over the network except what the page itself loads.
"""
import json
import os
import re
import sys
from html.parser import HTMLParser

BUZZ = ["seamless", "robust", "empower", "supercharge", "elevate", "effortless",
        "unlock", "unleash", "revolutionize", "revolutionise", "cutting-edge",
        "next-generation", "next-gen", "world-class", "best-in-class", "game-changer",
        "game changer", "synergy", "fast-paced world", "take it to the next level",
        "state-of-the-art", "industry-leading", "mission-critical"]
PLACEHOLDER = ["lorem ipsum", "jane doe", "john doe", "john smith", "acme", "example.com",
               "your name here"]
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿\U0001F000-\U0001F2FF]")
DEFAULT_FONTS = ["inter", "roboto", "open sans", "poppins", "montserrat", "lato",
                 "raleway", "nunito", "dm sans"]


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.chunks = []
        self.imgs_no_alt = 0
        self.h1 = 0
        self.html_lang = None
        self.inputs = []
        self.labels_for = set()
        self.button_texts = []
        self._in = []
        self.label_depth = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "noscript"):
            self.skip += 1
        if tag == "html":
            self.html_lang = a.get("lang")
        if tag == "img" and "alt" not in a:
            self.imgs_no_alt += 1
        if tag == "h1":
            self.h1 += 1
        if tag in ("input", "select", "textarea") and a.get("type") not in ("hidden", "submit", "button", "reset"):
            if self.label_depth == 0:
                self.inputs.append(a)
        if tag == "label":
            self.label_depth += 1
        if tag == "label" and a.get("for"):
            self.labels_for.add(a["for"])
        self._in.append(tag)

    def handle_endtag(self, tag):
        if tag == "label" and self.label_depth:
            self.label_depth -= 1
        if tag in ("script", "style", "noscript") and self.skip:
            self.skip -= 1
        if self._in and self._in[-1] == tag:
            self._in.pop()

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.chunks.append(data.strip())
            if self._in and self._in[-1] in ("button", "a"):
                self.button_texts.append(data.strip())


def static_checks(html):
    must, consider = [], []
    p = Text()
    p.feed(html)
    text = " ".join(p.chunks)
    low = text.lower()
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I))
    cssl = css.lower()

    found = sorted({w for w in BUZZ if re.search(r"\b" + re.escape(w) + r"\b", low)})
    if found:
        consider.append(f"Buzzwords in the copy ({', '.join(found)}). Say what it actually does, plainly.")
    ph = sorted({w for w in PLACEHOLDER if w in low})
    if ph:
        must.append(f"Placeholder names or text left in ({', '.join(ph)}). Replace or mark clearly as a placeholder.")
    if re.search(r"\w+ · \w+ · \w+", text):
        consider.append("Meta text joined with middle dots (A · B · C) reads as template; write it as a sentence or separate lines.")
    arrows = [t for t in p.button_texts if re.search(r"[→›»]\s*$|^\s*[←‹«]", t)]
    if arrows:
        consider.append(f"Arrow glued to button/link text ({arrows[0]!r}). Let the label stand alone.")
    emo = [t for t in p.button_texts if EMOJI.search(t)]
    heads = re.findall(r"<h[1-3][^>]*>(.*?)</h[1-3]>", html, re.S | re.I)
    emo += [h for h in heads if EMOJI.search(h)]
    if emo:
        must.append("Emoji used as icons in buttons or headings. Use one real icon set or plain text.")
    if p.h1 != 1:
        must.append(f"The page has {p.h1} <h1> headings; it needs exactly one.")
    if not p.html_lang:
        must.append('Missing lang on <html> (e.g. <html lang="en">) for screen readers.')
    if p.imgs_no_alt:
        must.append(f"{p.imgs_no_alt} image(s) without alt text (use alt=\"\" for decoration).")
    unlabeled = [i for i in p.inputs if i.get("id") not in p.labels_for and not i.get("aria-label") and not i.get("aria-labelledby")]
    if unlabeled:
        must.append(f"{len(unlabeled)} form field(s) without a visible <label for=…>.")
    if "background-clip: text" in cssl or "background-clip:text" in cssl:
        consider.append("Gradient or image-filled text. Emphasis usually reads better from size or weight.")
    if re.search(r"transition\s*:\s*all", cssl):
        must.append("`transition: all` found; list the properties you animate (transform, opacity).")
    if re.search(r"@keyframes[^{]*\{[^@]*?\b(width|height|top|left)\s*:", cssl, re.S):
        consider.append("An animation changes width/height/top/left, which janks; animate transform or opacity.")
    has_motion = "@keyframes" in cssl or "transition" in cssl or "animation" in cssl
    if has_motion and "prefers-reduced-motion" not in cssl:
        must.append("Animations without a prefers-reduced-motion fallback.")
    if ("<a" in html or "<button" in html) and ":focus-visible" not in cssl:
        must.append("No :focus-visible style; keyboard users need a clear focus ring.")
    if "100vw" in cssl:
        consider.append("`100vw` widths cause sideways scroll on many devices; use 100%.")
    if re.search(r"\b\d+(\.\d+)?vh\b", cssl):
        consider.append("Heights in vh get hidden behind phone browser bars; use svh or dvh.")
    fams = set()
    for m in re.findall(r"font-family\s*:\s*([^;}{]+)", css, re.I):
        first = m.split(",")[0].strip().strip("'\"").lower()
        if first and not first.startswith("var(") and first not in ("inherit", "ui-sans-serif", "ui-serif", "system-ui", "sans-serif", "serif", "monospace"):
            fams.add(first)
    for m in re.findall(r"--[\w-]*font[\w-]*\s*:\s*([^;}{]+)", css, re.I):
        fams.add(m.split(",")[0].strip().strip("'\"").lower())
    fams = {f for f in fams if f and not f.startswith("var(")}
    if len(fams) > 3:
        consider.append(f"{len(fams)} typefaces ({', '.join(sorted(fams))}); two is usually plenty.")
    defaults = sorted(f for f in fams if f in DEFAULT_FONTS)
    if defaults:
        consider.append(f"Default AI-typical typeface as a voice ({', '.join(defaults)}). Fine if the brand uses it; otherwise choose for the subject.")
    if re.search(r"(purple|violet|#7c3aed|#8b5cf6|#6366f1|#a855f7)[^;]*(blue|#3b82f6|#2563eb|#06b6d4)|linear-gradient\([^)]*(#6366f1|#8b5cf6|#7c3aed|#a855f7)[^)]*(#3b82f6|#06b6d4|#ec4899)", cssl):
        must.append("Purple/blue/pink gradient: the most recognisable AI-generated look.")
    if re.search(r"not (switched on|connected|available) yet|isn.t (switched on|connected|live) yet|coming soon|ordering (is )?(not|n.t) (available|enabled)", low):
        must.append("The page tells visitors the main action doesn't work yet. Make it work now (email/text hand-off or their existing tool; see references/actions.md) and keep setup notes out of the page.")
    if re.search(r"<button[^>]*type=[\"']submit[\"'][^>]*\bdisabled\b|<button[^>]*\bdisabled\b[^>]*type=[\"']submit", html, re.I):
        must.append("The main submit button ships disabled. Visitors must be able to act; validate on submit instead.")
    if re.search(r"\b(success|thank you|thanks!|you're on the list|we got it|message sent)\b", low) and "<form" in html.lower():
        consider.append("A form shows a success message; make sure it is only shown when something real is sent.")
    ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', html))
    broken = sorted({h for h in re.findall(r'href=["\']#([^"\']+)["\']', html) if h not in ids})
    if broken:
        must.append(f"Links to sections that don't exist: {', '.join('#'+b for b in broken[:5])}.")
    if re.search(r"<title>\s*</title>", html, re.I) or "<title" not in html.lower():
        must.append("Missing page title (<title>), which is what shows in search results and browser tabs.")
    if 'name="description"' not in html and "name='description'" not in html:
        consider.append("No meta description; add one sentence for search results and link previews.")
    if "og:title" not in html:
        consider.append("No Open Graph tags (og:title, og:description); links shared in messages will look bare.")
    if re.search(r"mailto:[^\"'?]*@(yourbakery|yourbusiness|example)\.", html) or re.search(r"[\"']\w+@your\w*\.com[\"']", html):
        consider.append("The order/contact email is still a placeholder. List it first under 'Replace before publishing'.")
    return must, consider, len(text.split())


RENDER_JS = r"""
() => {
  const vw = window.innerWidth, vh = window.innerHeight;
  const out = {overflow: document.documentElement.scrollWidth > vw + 1, lowContrast: [], eyebrows: [], accentWords: [], brokenImgs: 0, fold: {}, tinyText: 0};
  function rgb(s){const m=s.match(/rgba?\(([^)]+)\)/); if(!m) return null; const p=m[1].split(/[ ,/]+/).filter(Boolean).map(Number); return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1};}
  function lum(c){const f=v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)}; return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b);}
  function bgOf(el){let e=el; while(e){const cs=getComputedStyle(e); if(cs.backgroundImage && cs.backgroundImage!=='none') return null; const c=rgb(cs.backgroundColor); if(c && c.a>0.9) return c; e=e.parentElement;} return {r:255,g:255,b:255,a:1};}
  const seen = new Set();
  const all = document.body.querySelectorAll('*');
  for (const el of all) {
    const own = [...el.childNodes].filter(n=>n.nodeType===3 && n.textContent.trim()).map(n=>n.textContent.trim()).join(' ');
    if (!own) continue;
    const cs = getComputedStyle(el); const r = el.getBoundingClientRect();
    if (r.width===0 || cs.visibility==='hidden' || parseFloat(cs.opacity)===0) continue;
    const fs = parseFloat(cs.fontSize);
    if (fs < 12 && own.length > 20) out.tinyText++;
    const fg = rgb(cs.color), bg = bgOf(el);
    if (fg && bg) {
      const L1=lum(fg), L2=lum(bg); const ratio=(Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
      const large = fs>=24 || (fs>=18.66 && parseInt(cs.fontWeight)>=700);
      const need = large?3:4.5;
      if (ratio < need && !seen.has(own.slice(0,40))) { seen.add(own.slice(0,40)); out.lowContrast.push({text: own.slice(0,50), ratio: Math.round(ratio*100)/100, need}); }
    }
    const words = own.split(/\s+/).length;
    const caps = cs.textTransform==='uppercase' || (own === own.toUpperCase() && /[A-Z]{3}/.test(own));
    const tracked = parseFloat(cs.letterSpacing) > 0.04*fs;
    if (words<=6 && fs<=16 && (caps||tracked) && !['A','BUTTON','LABEL','TH','NAV'].includes(el.tagName) && !el.closest('nav,button,a,label,th,footer')) {
      let nx = el.nextElementSibling; if (nx && /^H[1-4]$/.test(nx.tagName)) out.eyebrows.push(own.slice(0,40));
    }
  }
  for (const h of document.querySelectorAll('h1,h2,h3')) {
    const hs = getComputedStyle(h);
    for (const c of h.querySelectorAll('em,i,span,mark,strong')) {
      const cs = getComputedStyle(c);
      if (cs.color!==hs.color || cs.fontStyle!==hs.fontStyle || cs.backgroundImage!=='none') { out.accentWords.push(h.textContent.trim().slice(0,60)); break; }
    }
  }
  for (const img of document.images) if (img.complete && img.naturalWidth===0) out.brokenImgs++;
  const h1 = document.querySelector('h1');
  if (h1) {
    const hb = h1.getBoundingClientRect(); out.fold.h1 = hb.bottom <= vh;
    const ctas = [...document.querySelectorAll('a, button, [type=submit]')].filter(e=>{const b=e.getBoundingClientRect(); const cs=getComputedStyle(e); return b.width>=100 && b.height>=40 && cs.display!=='none' && cs.visibility!=='hidden' && b.top>hb.top-10 && !e.closest('nav');});
    if (ctas.length) { const b = ctas[0].getBoundingClientRect(); out.fold.cta = b.bottom <= vh; out.fold.ctaText = ctas[0].textContent.trim().slice(0,40); }
  }
  const small = [...document.querySelectorAll('a,button,input,select,textarea')].filter(e=>{
    const cs=getComputedStyle(e); if (parseFloat(cs.opacity)===0 || cs.visibility==='hidden') return false;
    if (e.closest('label') && /radio|checkbox/.test(e.type||'')) return false;
    if (e.tagName==='A' && getComputedStyle(e.parentElement).display.includes('inline') === false && e.closest('p,li,td,dd,address')) return false;
    const b=e.getBoundingClientRect(); return b.width>0 && b.height>0 && (b.height<32 || b.width<32);});
  out.smallTargets = small.length; out.smallTargetNames = small.slice(0,4).map(e=>(e.getAttribute('aria-label')||e.textContent||e.id||e.tagName).trim().slice(0,30));
  return out;
}
"""


def render_checks(path, outdir, mode="persuade"):
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return None
    must, consider, shots = [], [], []
    url = "file://" + os.path.abspath(path)
    sizes = [("phone", 390, 844), ("laptop", 1280, 800), ("desktop", 1440, 900), ("wide", 1920, 1080), ("narrow", 320, 640)]
    try:
        with sync_playwright() as pw:
            try:
                browser = pw.chromium.launch()
            except Exception:
                browser = pw.chromium.launch(channel="chrome")
            for name, w, h in sizes:
                page = browser.new_page(viewport={"width": w, "height": h})
                errs = []
                if name == "desktop":
                    page.on("pageerror", lambda e: errs.append(str(e)[:120]))
                    page.on("console", lambda m: errs.append(m.text[:120]) if m.type == "error" and "Failed to load resource" not in m.text else None)
                page.goto(url, wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(600)
                r = page.evaluate(RENDER_JS)
                if r["overflow"]:
                    must.append(f"Sideways scrolling at {w}px wide ({name}).")
                if name in ("phone", "laptop"):
                    if r["fold"].get("h1") is False:
                        must.append(f"The main headline isn't fully visible without scrolling on a {name} ({w}×{h}).")
                    if r["fold"].get("cta") is False and mode == "persuade":
                        must.append(f"The main button ({r['fold'].get('ctaText','')!r}) isn't visible without scrolling on a {name} ({w}×{h}).")
                if name == "desktop" and errs:
                    must.append(f"Script errors in the page: {errs[:2]}")
                if name == "desktop":
                    for c in r["lowContrast"][:8]:
                        must.append(f"Low contrast {c['ratio']}:1 (needs {c['need']}:1): \"{c['text']}\"")
                    if r["eyebrows"]:
                        consider.append(f"Small caps label above a heading (the 'eyebrow' tell): {r['eyebrows'][:3]}. Delete it or make it real content.")
                    if r["accentWords"]:
                        consider.append(f"A word in a heading styled differently (italic/colour/highlight): {r['accentWords'][:2]}. Usually reads as a template tell.")
                    if r["brokenImgs"]:
                        must.append(f"{r['brokenImgs']} image(s) failed to load.")
                    if r["tinyText"]:
                        consider.append(f"{r['tinyText']} block(s) of text under 12px; hard to read.")
                if name == "phone" and r["smallTargets"]:
                    consider.append(f"{r['smallTargets']} tap target(s) smaller than 32px on a phone ({', '.join(r['smallTargetNames'])}); aim for 44px.")
                if name in ("phone", "desktop"):
                    f = os.path.join(outdir, f"shot-{name}.png")
                    page.screenshot(path=f, full_page=True)
                    shots.append(f)
                    f2 = os.path.join(outdir, f"shot-{name}-first-screen.png")
                    page.screenshot(path=f2, full_page=False)
                    shots.append(f2)
                page.close()
            browser.close()
    except Exception as e:
        consider.append(f"Could not render the page ({type(e).__name__}: {str(e)[:120]}). Only static checks ran.")
        return must, consider, shots
    return must, consider, shots


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    path = args[0]
    outdir = os.path.dirname(os.path.abspath(path))
    if "--out" in args:
        outdir = args[args.index("--out") + 1]
        os.makedirs(outdir, exist_ok=True)
    html = open(path, encoding="utf-8").read()
    must, consider, words = static_checks(html)
    mode = args[args.index("--mode") + 1] if "--mode" in args else "persuade"
    rendered = render_checks(path, outdir, mode)
    shots = []
    if rendered is None:
        consider.append("Rendering skipped (Playwright not installed). Look at the page in a browser at phone and desktop width.")
    else:
        must += rendered[0]
        consider += rendered[1]
        shots = rendered[2]
    if "--json" in args:
        print(json.dumps({"must_fix": must, "consider": consider, "screenshots": shots, "words": words}, indent=1))
        return
    print(f"UI Studio check: {os.path.basename(path)} ({words} words of visible text)")
    print(f"\nMUST FIX ({len(must)})")
    for m in must:
        print(" - " + m)
    print(f"\nCONSIDER ({len(consider)})")
    for c in consider:
        print(" - " + c)
    if shots:
        print("\nScreenshots (look at these):")
        for s in shots:
            print(" - " + s)
    sys.exit(1 if must else 0)


if __name__ == "__main__":
    main()
