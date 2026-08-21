"""
Geheimer Extra-Bon: eine Kaffeebestellung an config.COFFEE_FOR.

"Von" wird zufällig aus config.STAFF_NAMES gewählt (auf dem eigenen Gerät
also die echten Kindernamen aus config_local.py) - ansonsten stehen hier
bewusst keine echten Namen, nur Rollen ("Mama"), siehe config.py.
"""

import random
from datetime import datetime

import config
from . import layout

# ASCII-Art-Herz statt eines echten Herz-Zeichens: Unicode-Herzen (♥, ❤, ♡)
# liegen auf keiner Codepage dieses Druckers, auch das klassische DOS/CP437-
# Herz an Bytewert 0x03 kennt Pythons eigener cp437-Codec nicht mehr.
HERZ = [
    "  **   **  ",
    " ******** ",
    "  ******  ",
    "   ****   ",
    "    **    ",
]


def erstelle_bon(drucker):
    now = datetime.now()
    fuer = config.COFFEE_FOR
    von = random.choice(config.STAFF_NAMES)

    drucker.set(align="center", bold=True, double_height=True, double_width=True)
    drucker.text("LE PETIT CAFÉ\n")
    drucker.set(normal_textsize=True, align="center", bold=True, double_height=True, double_width=False)
    drucker.text("*  Sonderbestellung  *\n")
    drucker.set(normal_textsize=True, align="center", bold=False, double_height=False)
    drucker.text(layout.divider())

    drucker.set(align="left")
    drucker.text(f"Für:      {fuer}\n")
    drucker.text(f"Von:      {von}\n")
    drucker.text(f"Uhrzeit:  {now.strftime('%H:%M')} Uhr\n")
    drucker.text(layout.divider())

    drucker.text(layout.wrapped("1x Kaffee, so wie Papa ihn mag"))
    drucker.text(layout.wrapped("Bitte mit extra viel Liebe zubereitet", indent=3))

    drucker.text(layout.divider("═"))
    drucker.set(align="center")
    drucker.text(layout.wrapped("Bezahlung: Ein Kuss + Dankeschön"))
    drucker.text(layout.divider())
    drucker.text(layout.wrapped("Einzulösen: sofort, ohne Wartezeit"))
    drucker.text("\n")
    drucker.text(layout.wrapped("*  Danke, dass du das machst!  *"))
    drucker.text("\n")
    drucker.set(bold=True)
    for zeile in HERZ:
        drucker.text(zeile + "\n")
    drucker.set(normal_textsize=True, bold=False)
    drucker.cut()
