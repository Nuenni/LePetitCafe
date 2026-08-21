#!/usr/bin/env python3
"""
Drilling template for the 6 arcade buttons (LePetitCafe), A4, 1:1.

Needs reportlab (not part of requirements.txt - only used to regenerate
this one PDF, not needed on the Pi itself):
    pip install reportlab

Deliberately no printed frame as a reference - the printer can't print
borderless anyway, so the actual paper edge itself serves as the
reference line (top = front edge of the lid, left = left edge).
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

OUT = "docs/drilling-template.pdf"

PAGE_W, PAGE_H = A4  # 210 x 297 mm

LOCH_D = 24 * mm
LOCH_R = LOCH_D / 2

# Hole centers: distance from the LEFT and TOP paper edge.
# Top = front edge of the lid, left = left edge of the lid.
SPALTEN_X = [60 * mm, 110 * mm, 160 * mm]
REIHEN_Y = [70 * mm, 130 * mm]

KNOEPFE = [
    # (column, row, color name, world)
    (0, 0, "ROT",     "Supermarkt"),
    (1, 0, "BLAU",    "Eiscafé"),
    (2, 0, "GRÜN",    "Restaurant"),
    (0, 1, "GELB",    "Bus/Taxi"),
    (1, 1, "SCHWARZ", "KinderKino"),
    (2, 1, "WEISS",   "Reservierung"),
]


def y_von_oben(abstand_oben):
    """Converts PDF y (0 = bottom) to "distance from the top paper edge"."""
    return PAGE_H - abstand_oben


def kreuz(c, x, y, laenge=4 * mm):
    c.setLineWidth(0.3)
    c.line(x - laenge / 2, y, x + laenge / 2, y)
    c.line(x, y - laenge / 2, x, y + laenge / 2)


def build():
    c = canvas.Canvas(OUT, pagesize=A4)

    # ---- Header ----
    c.setFont("Helvetica-Bold", 11)
    c.drawString(15 * mm, PAGE_H - 12 * mm, "LePetitCafe — Bohrschablone Deckel (1:1, A4)")
    c.setFont("Helvetica", 8)
    c.drawString(15 * mm, PAGE_H - 17 * mm,
                 "Blatt an Vorderkante + linke Kante des Deckels ausrichten. Papierkante = Bezugslinie, kein Rand nötig.")
    c.drawString(15 * mm, PAGE_H - 21.5 * mm,
                 "Loch-Ø 24mm ist Richtwert — vor dem Bohren mit der echten Mutter gegenchecken.")

    # ---- 100mm scale-check strip, to measure after printing ----
    ruler_x0 = 15 * mm
    ruler_y = y_von_oben(28 * mm)
    ruler_x1 = ruler_x0 + 100 * mm
    c.setLineWidth(0.6)
    c.line(ruler_x0, ruler_y, ruler_x1, ruler_y)
    for x in (ruler_x0, ruler_x1):
        c.line(x, ruler_y - 1.5 * mm, x, ruler_y + 1.5 * mm)
    for cm in range(1, 10):
        xc = ruler_x0 + cm * 10 * mm
        c.line(xc, ruler_y - 0.8 * mm, xc, ruler_y + 0.8 * mm)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(ruler_x1 + 3 * mm, ruler_y - 2.6 * mm, "= genau 100mm? Sonst Druckskalierung auf 100% stellen.")

    # No drawn corner symbol here - it would sit near, but not exactly on,
    # the real paper edge, which would be misleading. The reference is the
    # actual top-left corner of the sheet itself.
    c.setFont("Helvetica", 6.5)
    c.drawString(15 * mm, y_von_oben(38 * mm),
                 "Die obere linke Ecke des Blatts selbst = Vorderkante + linke Kante des Deckels.")

    # ---- Holes ----
    for spalte, reihe, farbe, welt in KNOEPFE:
        cx = SPALTEN_X[spalte]
        cy = y_von_oben(REIHEN_Y[reihe])

        c.setLineWidth(0.7)
        c.circle(cx, cy, LOCH_R, stroke=1, fill=0)
        kreuz(c, cx, cy)

        c.setFont("Helvetica-Bold", 8)
        label = f"{farbe} · {welt}"
        w = stringWidth(label, "Helvetica-Bold", 8)
        c.drawString(cx - w / 2, cy - LOCH_R - 4.5 * mm, label)

        # Dimension: distance from the left/top edge, printed next to the hole.
        c.setFont("Helvetica", 6.5)
        massangabe = f"{int(SPALTEN_X[spalte] / mm)}mm / {int(REIHEN_Y[reihe] / mm)}mm"
        c.drawCentredString(cx, cy + LOCH_R + 3 * mm, massangabe)

    # ---- Footer: dimension legend ----
    c.setFont("Helvetica", 7)
    c.drawString(15 * mm, 10 * mm,
                 "Zahl über jedem Loch = Abstand Mittelpunkt von linker Kante / oberer Kante des Blatts (mm).")

    c.showPage()
    c.save()


if __name__ == "__main__":
    build()
    print("done ->", OUT)
