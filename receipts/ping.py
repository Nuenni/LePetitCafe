"""
Ping receipt: a message (and optionally a picture) sent in from the web
form, printed on demand rather than triggered by a button.

Deliberately framed with a box of asterisks and set in oversized bold text -
this one has to jump out among the regular play receipts on the kitchen
counter, since a kid is the one who'll spot it and hand it to whoever it's
for.
"""

from datetime import datetime

import config
from . import layout

# Cap on printed image height, so a huge photo doesn't spool out a meter of
# paper - width is already capped by _skaliert() to the printer's dots.
_MAX_BILD_HOEHE_PX = 800


def _skaliert(bild):
    """
    Downscale to the printer's dot width, preserving aspect ratio.
    python-escpos itself doesn't do this - anything wider than the paper
    just gets cut off on the right instead of shrunk to fit.
    """
    breite, hoehe = bild.size
    faktor = min(config.PRINTER_IMAGE_WIDTH_PX / breite, 1.0)
    neue_breite = max(1, round(breite * faktor))
    neue_hoehe = max(1, round(hoehe * faktor))
    if neue_hoehe > _MAX_BILD_HOEHE_PX:
        faktor = _MAX_BILD_HOEHE_PX / neue_hoehe
        neue_breite = max(1, round(neue_breite * faktor))
        neue_hoehe = _MAX_BILD_HOEHE_PX
    return bild.resize((neue_breite, neue_hoehe))


def erstelle_bon(drucker, nachricht: str, von: str = "", bild=None) -> None:
    now = datetime.now()
    breite = layout.width()
    rahmen = "*" * breite

    drucker.set(align="center", bold=True, double_height=True, double_width=True)
    drucker.text("PING\n")
    drucker.set(normal_textsize=True, align="center", bold=False, double_height=False, double_width=False)
    if von:
        drucker.text(f"Von: {von}\n")
    drucker.text(f"{now.strftime('%d.%m.%Y  %H:%M')}\n")
    drucker.text("\n")

    drucker.set(align="left")
    drucker.text(f"{rahmen}\n")
    drucker.text("*\n")
    drucker.set(bold=True, double_height=True, double_width=False)
    drucker.text(layout.wrapped(nachricht))
    drucker.set(normal_textsize=True, bold=False, double_height=False)
    drucker.text("*\n")
    drucker.text(f"{rahmen}\n")

    if bild is not None:
        drucker.text("\n")
        drucker.set(align="center")
        drucker.image(_skaliert(bild))

    drucker.text("\n")
    drucker.set(align="center")
    drucker.cut()
