"""Tischreservierung für das Bistro – der Anfang eines Restaurantbesuchs."""

import random
from datetime import datetime, timedelta

from . import layout
import config

LADEN_NAME = "LE PETIT BISTRO"

# Wochentage fest hinterlegt statt über strftime: Auf dem Raspberry Pi ist
# die deutsche Locale nicht zwingend eingerichtet, dann käme "Sat" statt "Sa".
WOCHENTAGE = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

WUENSCHE = [
    "Am Fenster",
    "Ruhige Ecke",
    "Nähe Spielecke",
    "Draußen auf der Terrasse",
    "Mit Hochstuhl",
    "Nicht am Durchgang",
    "Blick zur Küche",
]

ANLAESSE = [
    None, None, None,          # meistens ohne besonderen Anlass
    "Geburtstag",
    "Familienfeier",
    "Erster Schultag",
    "Einfach so",
]

QR_NACHRICHTEN = [
    "GUTSCHEIN: Du darfst dir den Platz am Tisch aussuchen.",
    "GUTSCHEIN: Heute bestellst du fuer alle.",
    "GUTSCHEIN: Einmal Nachtisch extra, weil reserviert wurde.",
    "Warum kommt der Tisch nie zu spaet? Er ist immer gedeckt.",
    "Was sagt der Stuhl zum Tisch? Nichts, Moebel reden nicht.",
    "Wie nennt man einen reservierten Tisch? Belegt und gluecklich.",
]


def erstelle_bon(drucker):
    now = datetime.now()
    nummer = random.randint(100, 999)
    tisch = random.randint(1, 24)
    personen = random.randint(2, 6)
    platz = random.randint(1, personen)

    # Reservierung liegt zwischen heute und in einer Woche
    wann = now + timedelta(days=random.randint(0, 7))
    uhrzeit = random.choice(["12:00", "12:30", "17:30", "18:00",
                             "18:30", "19:00", "19:30"])
    anlass = random.choice(ANLAESSE)

    drucker.set(align="center", bold=True, double_height=True, double_width=True)
    drucker.text(f"{LADEN_NAME}\n")
    drucker.set(align="center", bold=False, double_height=False,
                double_width=False)
    drucker.text("*  Marktplatz 7  *\n")
    drucker.text(layout.divider())

    drucker.set(align="center", bold=True, double_height=True)
    drucker.text("TISCH RESERVIERT\n")
    drucker.set(align="left", bold=False, double_height=False)
    drucker.text(layout.divider())

    # Die drei Angaben, auf die es ankommt – groß genug zum Vorzeigen
    drucker.set(bold=True, double_height=True)
    drucker.text(layout.row("TISCH", str(tisch)))
    drucker.text(layout.row("PLATZ", str(platz)))
    drucker.set(bold=False, double_height=False)
    drucker.text(layout.row("Personen", str(personen)))
    drucker.text(layout.divider())

    drucker.text(layout.row("Auf den Namen",
                            f"Fam. {random.choice(config.GUEST_NAMES)}"))
    drucker.text(layout.row("Tag", f"{WOCHENTAGE[wann.weekday()]}, "
                                   f"{wann.strftime('%d.%m.%Y')}"))
    drucker.text(layout.row("Uhrzeit", f"{uhrzeit} Uhr"))
    if anlass:
        drucker.text(layout.row("Anlass", anlass))
    drucker.text(layout.divider())

    drucker.text(layout.row("Wunsch", random.choice(WUENSCHE)))
    drucker.text(layout.row("Angenommen von", random.choice(config.STAFF_NAMES)))
    drucker.text(layout.row("Reservierungs-Nr.", f"{nummer}"))
    drucker.text(layout.divider())

    drucker.set(align="center")
    drucker.text(layout.wrapped("Wir freuen uns auf Sie!"))
    drucker.text(layout.wrapped("Bitte 10 Minuten vorher da sein."))
    layout.codes(drucker, random.choice(QR_NACHRICHTEN),
                 f"RES{nummer:05d}", "Scann mich!")
    drucker.cut()
