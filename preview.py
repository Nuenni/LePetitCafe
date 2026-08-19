#!/usr/bin/env python3
"""
Generates the receipt preview as a standalone HTML file.

    python3 preview.py

Writes simulator.html (German) and simulator_en.html (English).

The preview is character-accurate: it renders in real monospace font at
config.PRINTER_WIDTH characters per line, and checks every character against
the real printer's code-page profile. Whatever the printer can't display
gets highlighted in red - so problems show up here instead of on paper.
"""

import argparse
import html
import json
import random
import sys

import config
from receipts import (supermarkt, eiscafe, restaurant, bus, kino, reservierung,
                      supermarket, icecream, bistro, transit, cinema, reservation)

BONS_PRO_WELT = 8

WELTEN_DE = [
    ("supermarkt",   "Supermarkt",   "PETIT MARCHÉ",     "rot",     supermarkt),
    ("eiscafe",      "Eiscafé",      "LE PETIT CAFÉ",    "blau",    eiscafe),
    ("restaurant",   "Restaurant",   "LE PETIT BISTRO",  "gruen",   restaurant),
    ("bus",          "Bus/Taxi",     "LE PETIT EXPRESS", "gelb",    bus),
    ("kino",         "KinderKino",   "KINDERKINO",       "schwarz", kino),
    ("reservierung", "Reservierung", "LE PETIT BISTRO",  "weiss",   reservierung),
]
WELTEN_EN = [
    ("supermarket", "Supermarket",  "THE LITTLE MARKET", "rot",     supermarket),
    ("icecream",    "Ice Cream",    "THE LITTLE CAFÉ",   "blau",    icecream),
    ("bistro",      "Restaurant",   "THE LITTLE BISTRO", "gruen",   bistro),
    ("transit",     "Bus/Taxi",     "LE PETIT EXPRESS",  "gelb",    transit),
    ("cinema",      "Cinema",       "CINÉMA PETIT",      "schwarz", cinema),
    ("reservation", "Reservation",  "THE LITTLE BISTRO", "weiss",   reservation),
]

TEXTE = {
    "de": dict(
        titel="Bon-Vorschau",
        untertitel="So kommt es aus dem Drucker",
        hinweis="Knopf drücken für einen neuen Bon",
        breite="Zeichen pro Zeile",
        pruefung="Zeichenprüfung",
        alles_ok="Alle Zeichen druckbar",
        problem="nicht druckbar",
        andere="Andere Sprache",
        andere_link="simulator_en.html",
        andere_text="English",
    ),
    "en": dict(
        titel="Receipt Preview",
        untertitel="Exactly what the printer puts out",
        hinweis="Press a button for a new receipt",
        breite="characters per line",
        pruefung="Character check",
        alles_ok="All characters printable",
        problem="not printable",
        andere="Other language",
        andere_link="simulator.html",
        andere_text="Deutsch",
    ),
}


# ── Character check against the real printer profile ──────────────────────

def _pruefer():
    """
    Returns a function that says whether the printer can display a character.

    Uses the real code-page profile from python-escpos. If the library isn't
    installed (e.g. on a machine with no printer connection), we skip the
    check and treat everything as printable.
    """
    try:
        from escpos.magicencode import Encoder
        from escpos.capabilities import get_profile
        codepages = get_profile("TM-T20II").codePages
        encoder = Encoder({name: slot for slot, name in codepages.items()})
    except Exception as exc:                                  # pragma: no cover
        print(f"  Note: no character check ({exc})", file=sys.stderr)
        return lambda ch: True

    zwischenspeicher: dict[str, bool] = {}

    def druckbar(ch: str) -> bool:
        if ch not in zwischenspeicher:
            zwischenspeicher[ch] = bool(encoder.find_suitable_encoding(ch))
        return zwischenspeicher[ch]

    return druckbar


# ── Mock printer ────────────────────────────────────────────────────────────

class VorschauDrucker:
    """Collects the output instead of printing it, including font attributes."""

    def __init__(self):
        self.zeilen: list[dict] = []
        self._fett = False
        self._hoch = False
        self._breit = False
        self._ausrichtung = "left"

    def set(self, bold=None, double_height=None, double_width=None,
            align=None, **_):
        if bold is not None:          self._fett  = bold
        if double_height is not None: self._hoch  = double_height
        if double_width is not None:  self._breit = double_width
        if align is not None:         self._ausrichtung = align

    def text(self, txt: str):
        teile = txt.split("\n")
        # A trailing \n ends the line, it's not an empty line.
        if teile and teile[-1] == "":
            teile.pop()
        for zeile in teile:
            self.zeilen.append({
                "text": zeile, "fett": self._fett, "hoch": self._hoch,
                "breit": self._breit, "mitte": self._ausrichtung == "center",
            })

    def cut(self):
        pass

    def close(self):
        pass

    def qr(self, content, **_):
        self.zeilen.append({"grafik": qr_bild(content), "art": "qr",
                            "titel": content})

    def barcode(self, code, bc, **_):
        self.zeilen.append({"grafik": barcode_bild(code), "art": "bc",
                            "titel": code})


# ── Codes as real, scannable images ────────────────────────────────────────
#
# Deliberately PNG instead of SVG: a QR code is a dot matrix. As SVG it needs
# several thousand <rect> elements and around 15 KB; as PNG with one pixel
# per module, just a few hundred bytes. Scaled up via CSS with
# image-rendering: pixelated, which keeps the edges sharp.

def _als_png(pixel: list[list[int]], breite: int, hoehe: int) -> str:
    """Builds a data: URI with one pixel per module from a 0/1 matrix."""
    try:
        from PIL import Image
    except ImportError:                                       # pragma: no cover
        return ""
    import base64, io

    bild = Image.new("1", (breite, hoehe), 1)          # 1 = white
    bild.putdata([0 if p else 1 for reihe in pixel for p in reihe])
    puffer = io.BytesIO()
    bild.save(puffer, format="PNG", optimize=True)
    roh = base64.b64encode(puffer.getvalue()).decode("ascii")
    return f"data:image/png;base64,{roh}"


def qr_bild(text: str) -> str:
    """
    Generates a real QR code. In the preview it's actually scannable with a
    phone - so you can check before the first print whether the content is
    right and reads cleanly.
    """
    try:
        import qrcode
    except ImportError:                                       # pragma: no cover
        return ""

    q = qrcode.QRCode(border=2, box_size=1,
                      error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(text)
    q.make(fit=True)
    matrix = [[1 if m else 0 for m in reihe] for reihe in q.get_matrix()]
    return _als_png(matrix, len(matrix), len(matrix))


def barcode_bild(code: str) -> str:
    """Generates a real CODE39 barcode, same encoding as on the printer."""
    try:
        from barcode import Code39
    except ImportError:                                       # pragma: no cover
        return ""

    # add_checksum=False matches python-escpos, which also doesn't append
    # a check digit.
    bits = Code39(code, add_checksum=False).build()[0]
    return _als_png([[1 if b == "1" else 0 for b in bits]], len(bits), 1)


# ── HTML generation ─────────────────────────────────────────────────────────

def zeile_zu_html(zeile: dict, druckbar) -> str:
    if "grafik" in zeile:
        beschriftung = html.escape(zeile["titel"])
        return (f'<div class="{zeile["art"]}block">'
                f'<img class="{zeile["art"]}" src="{zeile["grafik"]}" '
                f'alt="{beschriftung}" title="{beschriftung}"></div>')

    stuecke = []
    for ch in zeile["text"]:
        sicher = html.escape(ch)
        if ch != " " and not druckbar(ch):
            stuecke.append(f'<b class="bad" title="U+{ord(ch):04X}">{sicher}</b>')
        else:
            stuecke.append(sicher)
    inhalt = "".join(stuecke) or "&nbsp;"

    klassen = []
    if zeile["fett"]:  klassen.append("b")
    if zeile["breit"]: klassen.append("dw")     # doppelt hoch UND breit
    elif zeile["hoch"]: klassen.append("dh")    # nur doppelt hoch
    if zeile["mitte"]: klassen.append("c")

    attr = f' class="{" ".join(klassen)}"' if klassen else ""
    return f"<div{attr}>{inhalt}</div>"


def bon_erzeugen(modul, druckbar) -> tuple[str, int]:
    p = VorschauDrucker()
    modul.erstelle_bon(p)
    html_zeilen = [zeile_zu_html(z, druckbar) for z in p.zeilen]
    fehler = sum(
        1 for z in p.zeilen if "text" in z for ch in z["text"]
        if ch != " " and not druckbar(ch)
    )
    return "\n".join(html_zeilen), fehler


def seite_bauen(sprache: str, welten, nur_inhalt: bool = False) -> tuple[str, int]:
    druckbar = _pruefer()
    t = TEXTE[sprache]

    daten, fehler_gesamt = {}, 0
    for schluessel, _label, _laden, _farbe, modul in welten:
        bons = []
        for _ in range(BONS_PRO_WELT):
            markup, fehler = bon_erzeugen(modul, druckbar)
            bons.append(markup)
            fehler_gesamt += fehler
        daten[schluessel] = bons

    knoepfe = "\n".join(
        f'      <button class="knopf {farbe}" data-welt="{schluessel}">'
        f'<span class="kappe"></span><span class="beschriftung">{html.escape(label)}</span>'
        f'</button>'
        for schluessel, label, _laden, farbe, _modul in welten
    )

    if fehler_gesamt:
        status = (f'<span class="warnung">{fehler_gesamt}× {t["problem"]}</span>')
    else:
        status = f'<span class="gut">{t["alles_ok"]}</span>'

    inhalt = f"""<div class="buehne">
  <header class="kopf">
    <p class="augenbraue">Le Petit Café</p>
    <h1>{t['titel']}</h1>
    <p class="unter">{t['untertitel']}</p>
  </header>

  <div class="pult">
{knoepfe}
  </div>
  <p class="tipp">{t['hinweis']}</p>

  <div class="papierhalter">
    <div class="papier" id="papier"><div class="bon" id="bon"></div></div>
  </div>

  <footer class="fuss">
    <div class="fakt"><dt>{t['breite']}</dt><dd>{config.PRINTER_WIDTH}</dd></div>
    <div class="fakt"><dt>{t['pruefung']}</dt><dd>{status}</dd></div>
    <div class="fakt"><dt>{t['andere']}</dt><dd><a href="{t['andere_link']}">{t['andere_text']}</a></dd></div>
  </footer>
</div>

<script>
const BONS = {json.dumps(daten, ensure_ascii=False)};
const zaehler = {{}};
const bon = document.getElementById('bon');
const papier = document.getElementById('papier');

function zeigen(welt) {{
  const liste = BONS[welt];
  zaehler[welt] = (zaehler[welt] ?? -1) + 1;
  bon.innerHTML = liste[zaehler[welt] % liste.length];
  papier.classList.remove('raus');
  void papier.offsetWidth;
  papier.classList.add('raus');
}}

document.querySelectorAll('.knopf').forEach(b => {{
  b.addEventListener('click', () => {{
    document.querySelectorAll('.knopf').forEach(x => x.classList.remove('aktiv'));
    b.classList.add('aktiv');
    zeigen(b.dataset.welt);
  }});
}});

document.querySelector('.knopf').click();
</script>"""

    if nur_inhalt:
        return CSS + "\n" + inhalt, fehler_gesamt

    lang = "de" if sprache == "de" else "en"
    voll = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['titel']} · Le Petit Café</title>
{CSS}
</head>
<body>
{inhalt}
</body>
</html>"""
    return voll, fehler_gesamt


CSS = """<style>
:root {
  --grund:    #15171c;
  --pult:     #1d2027;
  --kante:    #2b2f39;
  --papier:   #f6f4ef;
  --tinte:    #302c28;
  --text:     #e8eaee;
  --gedaempft:#8b91a0;
  --rot:      #d0432f;
  --blau:     #2f86c5;
  --gruen:    #3f9e5c;
  --gelb:     #d9a92c;
  --schwarz:  #3a3d46;
  --weiss:    #d8dbe2;
  --gut:      #4ca97a;
  --warn:     #e0654a;
  --mono: ui-monospace, "SF Mono", "Cascadia Mono", "Roboto Mono", Menlo, Consolas, monospace;
  --ui: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--grund);
  color: var(--text);
  font-family: var(--ui);
  min-height: 100dvh;
  padding: clamp(20px, 4vw, 48px) 16px 64px;
}
.buehne { max-width: 640px; margin: 0 auto; display: flex; flex-direction: column; gap: 28px; }

.kopf { text-align: center; display: flex; flex-direction: column; gap: 6px; }
.augenbraue {
  font-size: .68rem; letter-spacing: .22em; text-transform: uppercase;
  color: var(--gedaempft);
}
.kopf h1 {
  font-size: clamp(1.5rem, 5vw, 2rem); font-weight: 800;
  letter-spacing: -.02em; text-wrap: balance;
}
.unter { color: var(--gedaempft); font-size: .9rem; }

/* Control panel with the six arcade buttons. Grid instead of flex, so it
   wraps cleanly into two rows of three on narrow phone screens. */
.pult {
  display: grid; grid-template-columns: repeat(3, 1fr);
  justify-items: center; gap: 20px clamp(12px, 4vw, 28px);
  background: var(--pult); border: 1px solid var(--kante);
  border-radius: 18px; padding: 24px 16px;
}
.knopf {
  background: none; border: 0; cursor: pointer; padding: 0;
  display: flex; flex-direction: column; align-items: center; gap: 10px;
  font-family: inherit;
}
.kappe {
  width: clamp(48px, 13vw, 76px); aspect-ratio: 1; border-radius: 50%;
  display: block; transition: transform .08s ease, box-shadow .15s ease;
  border: 3px solid rgba(0,0,0,.35);
}
.rot     .kappe { background: radial-gradient(circle at 34% 30%, #f07a63, var(--rot));     box-shadow: 0 6px 0 #7e2416; }
.blau    .kappe { background: radial-gradient(circle at 34% 30%, #6fbdf0, var(--blau));    box-shadow: 0 6px 0 #1a5179; }
.gruen   .kappe { background: radial-gradient(circle at 34% 30%, #7cd399, var(--gruen));   box-shadow: 0 6px 0 #1f5c34; }
.gelb    .kappe { background: radial-gradient(circle at 34% 30%, #f0cf70, var(--gelb));    box-shadow: 0 6px 0 #7a5e13; }
.schwarz .kappe { background: radial-gradient(circle at 34% 30%, #6a6e7a, var(--schwarz)); box-shadow: 0 6px 0 #17181c; }
.weiss   .kappe { background: radial-gradient(circle at 34% 30%, #ffffff, var(--weiss));   box-shadow: 0 6px 0 #9195a0; border-color: rgba(0,0,0,.2); }
.knopf:active .kappe { transform: translateY(5px); box-shadow: 0 1px 0 rgba(0,0,0,.5); }
.knopf:focus-visible .kappe { outline: 3px solid var(--text); outline-offset: 4px; }
.beschriftung {
  font-size: .7rem; letter-spacing: .12em; text-transform: uppercase;
  color: var(--gedaempft); transition: color .15s ease;
}
.knopf.aktiv .beschriftung { color: var(--text); }
.tipp { text-align: center; font-size: .78rem; color: var(--gedaempft); margin-top: -14px; }

/* Thermal paper */
.papierhalter { display: flex; justify-content: center; }
.papier {
  background: var(--papier); color: var(--tinte);
  padding: 26px 18px 30px; max-width: 100%; overflow-x: auto;
  box-shadow: 0 18px 40px rgba(0,0,0,.5);
  clip-path: polygon(0 6px, 3% 0, 6% 6px, 9% 0, 12% 6px, 15% 0, 18% 6px, 21% 0,
    24% 6px, 27% 0, 30% 6px, 33% 0, 36% 6px, 39% 0, 42% 6px, 45% 0, 48% 6px,
    51% 0, 54% 6px, 57% 0, 60% 6px, 63% 0, 66% 6px, 69% 0, 72% 6px, 75% 0,
    78% 6px, 81% 0, 84% 6px, 87% 0, 90% 6px, 93% 0, 96% 6px, 100% 0,
    100% calc(100% - 6px), 96% 100%, 93% calc(100% - 6px), 90% 100%,
    87% calc(100% - 6px), 84% 100%, 81% calc(100% - 6px), 78% 100%,
    75% calc(100% - 6px), 72% 100%, 69% calc(100% - 6px), 66% 100%,
    63% calc(100% - 6px), 60% 100%, 57% calc(100% - 6px), 54% 100%,
    51% calc(100% - 6px), 48% 100%, 45% calc(100% - 6px), 42% 100%,
    39% calc(100% - 6px), 36% 100%, 33% calc(100% - 6px), 30% 100%,
    27% calc(100% - 6px), 24% 100%, 21% calc(100% - 6px), 18% 100%,
    15% calc(100% - 6px), 12% 100%, 9% calc(100% - 6px), 6% 100%,
    3% calc(100% - 6px), 0 100%);
}
.papier.raus { animation: raus .45s cubic-bezier(.2,.8,.3,1); }
@keyframes raus { from { transform: translateY(-14px); opacity: 0 } to { transform: none; opacity: 1 } }
@media (prefers-reduced-motion: reduce) { .papier.raus { animation: none } }

/* The receipt itself: real monospace, exactly as wide as the paper */
.bon {
  font-family: var(--mono);
  font-size: clamp(9.5px, 2.6vw, 13px);
  line-height: 1.32;
  white-space: pre;
  font-variant-numeric: tabular-nums;
  width: 42ch;
  max-width: 100%;
}
.bon .b  { font-weight: 700; }
.bon .c  { text-align: center; }
.bon .dh, .bon .dw { display: inline-block; font-size: 2em; line-height: .68; }
.bon .dh { transform: scaleX(.5); transform-origin: left center; width: 200%; }
.bon .dw { font-weight: 700; }
.bon .c.dh, .bon .c.dw { display: block; }
.bon .bad {
  background: var(--warn); color: var(--papier);
  font-weight: 700; border-radius: 2px;
}
/* QR code and barcode: real, scannable codes. One pixel per module, scaled
   up via CSS - pixelated keeps the edges sharp instead of blurring them. */
.qrblock, .bcblock { display: flex; justify-content: center; }
.qrblock { margin: 8px 0 2px; }
.bcblock { margin: 6px 0 2px; }
.qr, .bc { image-rendering: pixelated; }
.qr { width: 26ch; height: auto; }
.bc { width: 34ch; height: 32px; }

.fuss {
  display: flex; flex-wrap: wrap; justify-content: center;
  gap: 10px clamp(18px, 6vw, 40px);
  border-top: 1px solid var(--kante); padding-top: 20px;
}
.fakt { text-align: center; display: flex; flex-direction: column; gap: 3px; }
.fakt dt {
  font-size: .62rem; letter-spacing: .16em; text-transform: uppercase;
  color: var(--gedaempft);
}
.fakt dd { font-size: .92rem; font-weight: 600; font-variant-numeric: tabular-nums; }
.fakt a { color: var(--blau); text-decoration: none; border-bottom: 1px solid currentColor; }
.gut  { color: var(--gut); }
.warnung { color: var(--warn); }
</style>"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int,
                        help="random seed, so the output is reproducible")
    parser.add_argument("--artifact", metavar="PATH",
                        help="also write a version without the <html> wrapper")
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    gesamt = 0
    for sprache, welten, datei in (("de", WELTEN_DE, "simulator.html"),
                                   ("en", WELTEN_EN, "simulator_en.html")):
        markup, fehler = seite_bauen(sprache, welten)
        with open(datei, "w", encoding="utf-8") as f:
            f.write(markup)
        gesamt += fehler
        print(f"  {datei:<20} {BONS_PRO_WELT * len(welten)} receipts, "
              f"{len(markup) // 1024} KB, {fehler} unprintable character(s)")

    if args.artifact:
        markup, _ = seite_bauen("de", WELTEN_DE, nur_inhalt=True)
        with open(args.artifact, "w", encoding="utf-8") as f:
            f.write(markup)
        print(f"  {args.artifact:<20} (artifact version)")

    if gesamt:
        print(f"\n  ⚠ {gesamt} character(s) the printer can't display "
              f"(highlighted in red on the receipt).")
    else:
        print("\n  ✓ All characters are displayable on the printer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
