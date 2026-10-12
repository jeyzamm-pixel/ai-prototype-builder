"""Test prototypu na telefonie (412 px) i komputerze (1440 px): brak przewijania w poziomie,
brak błędów JS, czat odpowiada ze słów kluczowych, kreator kończy się zgłoszeniem bez ceny.

Użycie: python test.py [firma]   (wymaga: playwright install chromium)
"""
import re
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

import zloz

PROFILE = {"telefon": {"width": 412, "height": 860, "is_mobile": True, "has_touch": True},
           "komputer": {"width": 1440, "height": 900}}


def otworz(browser, html_path, profil):
    ctx = browser.new_context(viewport={k: v for k, v in profil.items() if k in ("width", "height")},
                              is_mobile=profil.get("is_mobile", False), has_touch=profil.get("has_touch", False))
    page = ctx.new_page()
    bledy = []
    page.on("pageerror", lambda e: bledy.append(str(e)))
    page.on("console", lambda m: bledy.append(m.text) if m.type == "error" else None)
    page.goto(Path(html_path).as_uri())
    return page, bledy


def sprawdz(browser, html_path, nazwa, profil):
    page, bledy = otworz(browser, html_path, profil)
    szer = page.evaluate("({iw: innerWidth, sw: document.documentElement.scrollWidth})")
    assert szer["sw"] <= szer["iw"], f"{nazwa}: przewijanie w poziomie {szer}"
    # czat: słowa kluczowe
    page.fill("#czat-in", "do której otwarte?")
    page.press("#czat-in", "Enter")
    ostatnia = page.locator("#czat-log .m.b").last.inner_text()
    assert "czynni" in ostatnia, f"{nazwa}: czat odpowiedział: {ostatnia}"
    page.fill("#czat-in", "coś zupełnie innego")
    page.press("#czat-in", "Enter")
    assert "oddzwonimy" in page.locator("#czat-log .m.b").last.inner_text()
    # kreator
    page.click("#b-kreator")
    page.click("#k-opcje button >> nth=0")
    page.click("#k-opcje button >> nth=0")
    wynik = page.inner_text("#k-wynik")
    assert "Cenę poda człowiek" in wynik and not re.search(r"\d\s?(zł|PLN)", wynik), f"{nazwa}: {wynik}"
    assert page.evaluate("window.__zgloszenie.odpowiedzi.length") == 2
    assert not bledy, f"{nazwa}: błędy JS {bledy}"
    page.context.close()
    return szer


def main():
    firma = sys.argv[1] if len(sys.argv) > 1 else "piekarnia-przykladowa"
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "index.html"
        p.write_text(zloz.zloz(firma), encoding="utf-8")
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            for nazwa, profil in PROFILE.items():
                szer = sprawdz(b, p, nazwa, profil)
                print(f"{nazwa:<9} OK  szer={szer} czat=True kreator=True bledy=[]")
            b.close()


if __name__ == "__main__":
    main()
