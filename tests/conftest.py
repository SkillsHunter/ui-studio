import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def check():
    return _load("ui_studio_check", ROOT / "ui-studio" / "scripts" / "check.py")


@pytest.fixture(scope="session")
def build():
    return _load("ui_studio_build", ROOT / "tools" / "build.py")


GOOD_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rye &amp; Crumb Bakery</title>
<meta name="description" content="Sourdough baked every Saturday in Leeds. Pre-order by email.">
<meta property="og:title" content="Rye &amp; Crumb Bakery">
<style>
  html, body { overflow-x: clip; margin: 0; }
  body { font-family: "Karla", sans-serif; color: #1f1a14; background: #fbf6ee; }
  h1 { font-family: "Alfa Slab One", serif; }
  a:focus-visible, button:focus-visible { outline: 3px solid #8a3b12; }
  button { transition: transform 200ms ease-out; min-height: 48px; padding: 0 24px; }
  @media (prefers-reduced-motion: reduce) { button { transition: none; } }
</style>
</head>
<body>
<main>
  <h1>Saturday sourdough, baked in Leeds</h1>
  <p>Pick your loaves below and we'll have them ready at 9am.</p>
  <form id="order">
    <label for="qty">Country loaves</label>
    <input id="qty" type="number" min="0" value="0">
    <img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="">
    <button type="submit">Email my pre-order</button>
  </form>
  <p><a href="#order">Order again</a></p>
</main>
</body>
</html>
"""


@pytest.fixture
def good_page():
    return GOOD_PAGE
