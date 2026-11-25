import json

import pytest


def must_and_consider(check, html):
    must, consider, _ = check.static_checks(html)
    return " | ".join(must), " | ".join(consider)


def test_good_page_has_nothing_to_fix(check, good_page):
    must, _ = must_and_consider(check, good_page)
    assert must == ""


# --- parser: void elements no longer corrupt the open-element stack ---------------

def test_arrow_in_button_after_void_element_is_found(check, good_page):
    html = good_page.replace(
        '<button type="submit">Email my pre-order</button>',
        '<button type="submit"><img src="i.png" alt=""> Email my pre-order →</button>',
    )
    _, consider = must_and_consider(check, html)
    assert "Arrow glued" in consider


def test_emoji_in_button_after_line_break_is_found(check, good_page):
    html = good_page.replace(
        '<button type="submit">Email my pre-order</button>',
        '<button type="submit">Order<br>now \U0001F35E</button>',
    )
    must, _ = must_and_consider(check, html)
    assert "Emoji used as icons" in must


def test_void_elements_never_stay_open(check):
    p = check.Text()
    p.feed('<p>One<br>two<img src="x" alt=""><input id="a"></p><hr/><div/>')
    p.close()
    assert p._in == []


# --- placeholders match whole names only ------------------------------------------

@pytest.mark.parametrize("text", ["John Smithson runs the shop", "Acmeville Road", "Visit counterexample.com"])
def test_placeholder_check_ignores_longer_words(check, good_page, text):
    must, _ = must_and_consider(check, good_page.replace("Order again", text))
    assert "Placeholder" not in must


@pytest.mark.parametrize("text", ["Jane Doe", "ACME Ltd", "Email orders@example.com", "lorem ipsum dolor"])
def test_placeholder_check_still_catches_placeholders(check, good_page, text):
    must, _ = must_and_consider(check, good_page.replace("Order again", text))
    assert "Placeholder" in must


# --- other static checks keep working ---------------------------------------------

@pytest.mark.parametrize("change, expected", [
    (('<html lang="en">', "<html>"), "Missing lang"),
    (('<h1>', '<h1>A</h1><h1>'), "2 <h1> headings"),
    (('alt=""', ""), "without alt text"),
    (("transition: transform 200ms", "transition: all 200ms"), "transition: all"),
    (('<button type="submit">', '<button type="submit" disabled>'), "ships disabled"),
    (('href="#order"', 'href="#nowhere"'), "#nowhere"),
    (("<title>Rye &amp; Crumb Bakery</title>", "<title></title>"), "Missing page title"),
    (('<label for="qty">Country loaves</label>', ""), "without a visible <label"),
])
def test_static_must_fix(check, good_page, change, expected):
    old, new = change
    assert old in good_page
    must, _ = must_and_consider(check, good_page.replace(old, new, 1))
    assert expected in must


def test_buzzwords_are_flagged(check, good_page):
    _, consider = must_and_consider(check, good_page.replace("Order again", "A seamless, world-class loaf"))
    assert "seamless" in consider and "world-class" in consider


# --- network policy while rendering -----------------------------------------------

@pytest.mark.parametrize("url, allowed", [
    ("file:///C:/site/index.html", True),
    ("data:image/png;base64,AAAA", True),
    ("https://fonts.googleapis.com/css2?family=Karla", True),
    ("https://fonts.gstatic.com/s/karla/v1/a.woff2", True),
    ("http://fonts.gstatic.com/s/karla/v1/a.woff2", False),
    ("https://fonts.gstatic.com.evil.example/x", False),
    ("https://cdn.tailwindcss.com/", False),
    ("https://tracker.example/pixel.gif", False),
])
def test_request_allowed(check, url, allowed):
    assert check.request_allowed(url) is allowed
    assert check.request_allowed(url, allow_network=True) is True


# --- command line -----------------------------------------------------------------

def test_cli_rejects_unknown_mode(check, tmp_path, capsys):
    page = tmp_path / "index.html"
    page.write_text("<html></html>", encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        check.main([str(page), "--mode", "fancy"])
    assert exc.value.code == 2
    assert "invalid choice" in capsys.readouterr().err


def test_cli_rejects_flag_without_value(check, tmp_path):
    page = tmp_path / "index.html"
    page.write_text("<html></html>", encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        check.main([str(page), "--mode"])
    assert exc.value.code == 2


def test_cli_missing_file_exits_2(check, tmp_path, capsys):
    assert check.main([str(tmp_path / "nope.html")]) == 2
    assert "No such file" in capsys.readouterr().err


def test_cli_rejects_non_utf8(check, tmp_path, capsys):
    page = tmp_path / "index.html"
    page.write_bytes(b"<html>\xff\xfe caf\xe9</html>")
    assert check.main([str(page)]) == 2
    assert "not UTF-8" in capsys.readouterr().err


def test_cli_rejects_huge_file(check, tmp_path, monkeypatch, capsys):
    page = tmp_path / "index.html"
    page.write_text("<html>" + "x" * 2000 + "</html>", encoding="utf-8")
    monkeypatch.setattr(check, "MAX_BYTES", 1000)
    assert check.main([str(page)]) == 2
    assert "up to" in capsys.readouterr().err


def test_cli_json_and_exit_codes(check, tmp_path, good_page, monkeypatch, capsys):
    monkeypatch.setattr(check, "render_checks", lambda *a, **k: None)
    page = tmp_path / "index.html"
    page.write_text(good_page, encoding="utf-8")
    assert check.main([str(page), "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["must_fix"] == [] and out["screenshots"] == []

    page.write_text(good_page.replace('<html lang="en">', "<html>"), encoding="utf-8")
    assert check.main([str(page), "--json"]) == 1


def test_screenshots_default_to_dedicated_folder(check, tmp_path, good_page, monkeypatch):
    seen = {}

    def fake_render(path, outdir, mode, allow_network):
        seen.update(outdir=outdir, mode=mode, allow_network=allow_network)
        return [], [], []

    monkeypatch.setattr(check, "render_checks", fake_render)
    page = tmp_path / "index.html"
    page.write_text(good_page, encoding="utf-8")
    check.main([str(page), "--mode", "operate", "--allow-network"])
    assert seen == {"outdir": str(tmp_path / ".ui-studio-check"), "mode": "operate", "allow_network": True}


def test_output_survives_a_legacy_console(check, tmp_path, good_page, monkeypatch):
    # Windows consoles often use cp1252, which has no → or ×; printing used to crash.
    import io
    import sys

    monkeypatch.setattr(check, "render_checks", lambda *a, **k: None)
    buf = io.BytesIO()
    monkeypatch.setattr(sys, "stdout", io.TextIOWrapper(buf, encoding="cp1252"))
    page = tmp_path / "index.html"
    page.write_text(good_page.replace("Order again", "Learn more →"), encoding="utf-8")
    assert check.main([str(page)]) == 0
    sys.stdout.flush()
    assert b"Arrow glued" in buf.getvalue()


# --- real rendering (runs only where Playwright and a Chromium-based browser exist) --

def _chromium_available():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False
    with sync_playwright() as pw:
        for kwargs in ({}, {"channel": "chrome"}):
            try:
                pw.chromium.launch(**kwargs).close()
                return True
            except Exception:
                pass
    return False


@pytest.mark.render
def test_render_blocks_remote_requests(check, tmp_path, good_page):
    if not _chromium_available():
        pytest.skip("Playwright Chromium not installed")
    html = good_page.replace(
        "</main>",
        '<img src="https://tracker.invalid/pixel.gif" alt=""><script src="https://cdn.invalid/x.js"></script></main>',
    )
    page = tmp_path / "index.html"
    page.write_text(html, encoding="utf-8")
    must, consider, shots = check.render_checks(str(page), str(tmp_path / "out"), "persuade")
    joined = " | ".join(consider)
    assert "Blocked requests to 2 other host(s)" in joined
    assert "cdn.invalid" in joined and "tracker.invalid" in joined
    assert not any("failed to load" in m for m in must)
    assert len(shots) == 4 and all((tmp_path / "out").joinpath(s).exists() for s in shots)
