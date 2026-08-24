"""
Ping receipt: a message (and optionally a picture) sent in from the web
form, printed on demand rather than triggered by a button.

Deliberately framed with a box of asterisks and set in oversized bold text -
this one has to jump out among the regular play receipts on the kitchen
counter, since a kid is the one who'll spot it and hand it to whoever it's
for.
"""

from datetime import datetime

from . import layout


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
        drucker.image(bild)

    drucker.text("\n")
    drucker.set(align="center")
    drucker.cut()
