"""Skład prototypu: szablon + dane.js firmy -> jeden plik dist/<firma>/index.html, z lintem tekstu.

Użycie: python zloz.py piekarnia-przykladowa
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ZAKAZANE = {"\N{EM DASH}": "myślnik", "\N{EN DASH}": "półpauza"}


def lint(dane_js: str) -> list:
    problemy = [f"zakazany znak: {opis}" for znak, opis in ZAKAZANE.items() if znak in dane_js]
    if re.search(r"\d\s?(zł|zl|pln|PLN)\b", dane_js):
        problemy.append("kwota w danych prototypu (kreator nie podaje ceny)")
    return problemy


def zloz(firma: str, dane_js: str = None) -> str:
    if dane_js is None:
        dane_js = (ROOT / "firmy" / firma / "dane.js").read_text(encoding="utf-8")
    problemy = lint(dane_js)
    if problemy:
        raise ValueError(f"lint odrzucił {firma}: {problemy}")
    html = (ROOT / "template" / "index.html").read_text(encoding="utf-8")
    html = html.replace("/*STYLE*/", (ROOT / "template" / "style.css").read_text(encoding="utf-8"))
    html = html.replace("/*DANE*/", dane_js)
    html = html.replace("/*APP*/", (ROOT / "template" / "app.js").read_text(encoding="utf-8"))
    return html


def main():
    firma = sys.argv[1] if len(sys.argv) > 1 else "piekarnia-przykladowa"
    out = ROOT / "dist" / firma
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(zloz(firma), encoding="utf-8")
    print("zapisano", (out / "index.html").relative_to(ROOT))


if __name__ == "__main__":
    main()
