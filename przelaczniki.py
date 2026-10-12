"""Wszystkie 32 kombinacje modułów prototypu (hero, oferta, opinie, pokaz, czat, kreator
to 6 sekcji; hero jest zawsze, więc przełączamy pozostałe pięć: 2^5 = 32).
Każda kombinacja musi się złożyć, załadować bez błędów JS i bez przewijania w poziomie,
a sekcja bez danych musi zniknąć.

Użycie: python przelaczniki.py [firma]
"""
import itertools
import re
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

import zloz

ROOT = Path(__file__).resolve().parent
MODULY = ["oferta", "opinie", "pokaz", "czat", "kreator"]


def dane_bez(dane_js: str, wylaczone) -> str:
    """Dopisuje na końcu pliku usunięcie wybranych kluczy z DANE (bez parsowania JS)."""
    return dane_js + "\n" + "".join(f"delete window.DANE.{m};\n" for m in wylaczone)


def main():
    firma = sys.argv[1] if len(sys.argv) > 1 else "piekarnia-przykladowa"
    bazowe = (ROOT / "firmy" / firma / "dane.js").read_text(encoding="utf-8")
    kombinacje = [c for n in range(len(MODULY) + 1) for c in itertools.combinations(MODULY, n)]
    assert len(kombinacje) == 32
    zle = 0
    with tempfile.TemporaryDirectory() as tmp, sync_playwright() as pw:
        b = pw.chromium.launch()
        for i, wylaczone in enumerate(kombinacje):
            p = Path(tmp) / f"k{i}.html"
            p.write_text(zloz.zloz(firma, dane_bez(bazowe, wylaczone)), encoding="utf-8")
            page = b.new_page(viewport={"width": 412, "height": 860})
            bledy = []
            page.on("pageerror", lambda e: bledy.append(str(e)))
            page.goto(p.as_uri())
            sekcje = page.evaluate("window.__sekcje")
            szer = page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            for m in MODULY:
                obecna = page.locator(f'[data-sekcja="{m}"]').count() > 0
                if obecna == (m in wylaczone):
                    bledy.append(f"sekcja {m}: obecna={obecna}, wyłączona={m in wylaczone}")
            if bledy or not szer:
                zle += 1
                print("KOMBINACJA", wylaczone, "błędy:", bledy, "poziomy scroll:", not szer)
            page.close()
        b.close()
    print(f"{firma}: {len(kombinacje)} kombinacji, z błędem {zle}, błędy JS {zle} -> {'OK' if not zle else 'BŁĄD'}")
    sys.exit(1 if zle else 0)


if __name__ == "__main__":
    main()
