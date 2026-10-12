"""Zrzuty minimalnego przykładu (demo/piekarnia-przykladowa.html) i wyniku testów."""
import html
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
demo = (ROOT / "demo" / "piekarnia-przykladowa.html").as_uri()
out = ROOT / "screenshots"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 412, "height": 860}, is_mobile=True, has_touch=True)
    pg.goto(demo)
    pg.click("#czat-pod button >> nth=1")
    pg.screenshot(path=str(out / "minimalny-telefon.png"))
    pg.click("#b-kreator")
    pg.click("#k-opcje button >> nth=0")
    pg.screenshot(path=str(out / "minimalny-kreator.png"))
    pg = b.new_page(viewport={"width": 1280, "height": 800})
    pg.goto(demo)
    pg.screenshot(path=str(out / "minimalny-komputer.png"))
    wynik = ""
    for cmd in (["test.py"], ["przelaczniki.py"]):
        r = subprocess.run([sys.executable, "-X", "utf8"] + cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        wynik += f"$ python {cmd[0]}\n{r.stdout}\n"
    pg = b.new_page(viewport={"width": 900, "height": 260})
    pg.set_content(f"<body style='margin:0;background:#021836;color:#bfe9f7;font:15px/1.6 Consolas,monospace;padding:20px'><pre>{html.escape(wynik)}</pre>")
    pg.screenshot(path=str(out / "testy.png"), full_page=True)
    b.close()
