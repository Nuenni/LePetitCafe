#!/usr/bin/env python3
"""
LePetitCafe Simulator — Bons im Terminal testen, ohne Hardware.

Steuerung:
  1  →  Supermarkt-Bon drucken
  2  →  Eiscafé-Bon drucken
  3  →  Restaurant-Bon drucken
  q  →  Beenden
  h  →  Letzten Bon als HTML speichern (preview_last.html)
"""

import sys
import os
import random

# ── Mock-Drucker ──────────────────────────────────────────────────────────────

RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RED    = "\033[91m"
PURPLE = "\033[95m"
BLUE   = "\033[94m"

BON_WIDTH = 42  # Zeichen pro Zeile

class MockPrinter:
    """Simuliert einen ESC/POS-Thermodrucker im Terminal."""

    def __init__(self, accent=RED):
        self._bold         = False
        self._double_h     = False
        self._double_w     = False
        self._align        = "left"
        self._accent       = accent
        self._lines: list[str] = []   # für HTML-Export
        self._html_lines: list[dict] = []

    # ── ESC/POS-API (entspricht python-escpos) ────────────────────────────────

    def set(self, bold=None, double_height=None, double_width=None, align=None, **_):
        if bold         is not None: self._bold     = bold
        if double_height is not None: self._double_h = double_height
        if double_width  is not None: self._double_w = double_width
        if align        is not None: self._align    = align

    def text(self, txt: str):
        for line in txt.split("\n"):
            self._render_line(line)

    def cut(self):
        self._render_cut()

    def close(self):
        pass

    # ── Rendering ─────────────────────────────────────────────────────────────

    def _render_line(self, line: str):
        if not line:
            print()
            self._html_lines.append({"text": "", "bold": False, "big": False, "align": "left"})
            return

        w        = BON_WIDTH
        bold     = self._bold or self._double_h
        big      = self._double_h

        # Ausrichten
        if self._align == "center":
            padded = line.center(w)
        elif self._align == "right":
            padded = line.rjust(w)
        else:
            padded = line

        # Terminal-Ausgabe
        fmt = ""
        if bold:   fmt += BOLD
        out = fmt + padded + RESET
        print(out)

        # Für HTML merken
        self._html_lines.append({
            "text": line, "bold": bold, "big": big,
            "align": self._align,
        })

    def _render_cut(self):
        sep = "✂" + "─" * (BON_WIDTH - 1)
        print(DIM + sep + RESET)
        print()
        self._html_lines.append({"cut": True})

    # ── HTML-Export ───────────────────────────────────────────────────────────

    def to_html(self, accent_css: str) -> str:
        rows = []
        for h in self._html_lines:
            if h.get("cut"):
                rows.append('<hr class="cut">')
                continue
            txt   = h["text"].replace("&", "&amp;").replace("<", "&lt;")
            style = []
            if h["bold"]: style.append("font-weight:700")
            if h["big"]:  style.append("font-size:1.3em")
            align = h.get("align", "left")
            style.append(f"text-align:{align}")
            rows.append(f'<div style="{";".join(style)}">{txt or "&nbsp;"}</div>')

        body = "\n".join(rows)
        return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>LePetitCafe — Bon-Vorschau</title>
<style>
  body {{ background:#2b2b2b; display:flex; justify-content:center;
          padding:40px; font-family:'Courier New',monospace; }}
  .receipt {{ background:#faf6ee; width:340px; padding:28px 22px 36px;
              box-shadow:0 8px 32px rgba(0,0,0,.5);
              clip-path:polygon(0% 1%,3% 0%,6% 1%,9% 0%,12% 1%,15% 0%,18% 1%,
                21% 0%,24% 1%,27% 0%,30% 1%,33% 0%,36% 1%,39% 0%,42% 1%,
                45% 0%,48% 1%,51% 0%,54% 1%,57% 0%,60% 1%,63% 0%,66% 1%,
                69% 0%,72% 1%,75% 0%,78% 1%,81% 0%,84% 1%,87% 0%,90% 1%,
                93% 0%,96% 1%,100% 0%,100% 99%,97% 100%,94% 99%,91% 100%,
                88% 99%,85% 100%,82% 99%,79% 100%,76% 99%,73% 100%,70% 99%,
                67% 100%,64% 99%,61% 100%,58% 99%,55% 100%,52% 99%,49% 100%,
                46% 99%,43% 100%,40% 99%,37% 100%,34% 99%,31% 100%,28% 99%,
                25% 100%,22% 99%,19% 100%,16% 99%,13% 100%,10% 99%,7% 100%,
                4% 99%,1% 100%,0% 99%); }}
  div {{ white-space:pre-wrap; font-size:0.78em; line-height:1.6;
         color:#222; min-height:1em; }}
  hr.cut {{ border:none; border-top:1px dashed #aaa; margin:8px 0; }}
</style>
</head>
<body>
<div class="receipt">
{body}
</div>
</body>
</html>"""


# ── Bon-Generatoren laden (ohne RPi.GPIO) ─────────────────────────────────────

sys.path.insert(0, os.path.dirname(__file__))
from receipts import supermarkt, eiscafe, restaurant

WELTEN = {
    "1": ("Supermarkt",  supermarkt.erstelle_bon,  RED),
    "2": ("Eiscafé",     eiscafe.erstelle_bon,     PURPLE),
    "3": ("Restaurant",  restaurant.erstelle_bon,  BLUE),
}

ACCENT_CSS = {
    "1": "#c0392b",
    "2": "#8e44ad",
    "3": "#1a5276",
}

_last_html = ""

def drucke_bon(taste: str):
    global _last_html
    name, fn, accent = WELTEN[taste]

    breite = BON_WIDTH + 2
    print()
    print("┌" + "─" * breite + "┐")
    print("│" + f" {accent}{BOLD}{name}{RESET}".ljust(breite + len(accent) + len(BOLD) + len(RESET) - 1) + "│")
    print("├" + "─" * breite + "┤")

    p = MockPrinter(accent=accent)
    fn(p)

    print("└" + "─" * breite + "┘")
    print(DIM + '  [h] als HTML speichern  [1/2/3] nächster Bon  [q] beenden' + RESET)

    _last_html = p.to_html(ACCENT_CSS[taste])


def speichere_html():
    path = os.path.join(os.path.dirname(__file__), "preview_last.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(_last_html)
    print(f"\n{BOLD}Gespeichert:{RESET} {path}")
    print(DIM + "Im Browser öffnen um den Bon zu sehen." + RESET)


# ── Hauptschleife ──────────────────────────────────────────────────────────────

def main():
    # Versuche, tty-Eingabe ohne Enter zu lesen
    try:
        import tty, termios
        USE_RAW = True
    except ImportError:
        USE_RAW = False

    print(f"\n{BOLD}LePetitCafe Simulator{RESET}")
    print("─" * (BON_WIDTH + 4))
    print(f"  {RED}1{RESET} = Supermarkt   {PURPLE}2{RESET} = Eiscafé   {BLUE}3{RESET} = Restaurant")
    print(f"  h = letzten Bon als HTML speichern   q = beenden")
    print("─" * (BON_WIDTH + 4))
    print(DIM + "Taste drücken..." + RESET)

    if USE_RAW and sys.stdin.isatty():
        fd  = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch in WELTEN:
                    tty.setcbreak(fd)
                    drucke_bon(ch)
                    tty.setraw(fd)
                elif ch == "h" and _last_html:
                    tty.setcbreak(fd)
                    speichere_html()
                    tty.setraw(fd)
                elif ch in ("q", "\x03", "\x1b"):
                    break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    else:
        while True:
            ch = input("\nTaste (1/2/3/h/q): ").strip().lower()
            if ch in WELTEN:
                drucke_bon(ch)
            elif ch == "h" and _last_html:
                speichere_html()
            elif ch == "q":
                break

    print("\nTschüss!")


if __name__ == "__main__":
    main()
