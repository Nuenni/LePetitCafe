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

# Kleine Runden (passen in GUEST_FIRST_NAMES) meist ohne Anlass – das ist der
# normale Restaurantbesuch. Größere Runden fast immer mit, sonst wirkt es
# seltsam, warum plötzlich sechs Leute kommen.
ANLAESSE_KLEIN = [None, None, None, None, "Einfach so"]
ANLAESSE_GROSS = ["Geburtstag", "Geburtstag", "Familienfeier",
                  "Erster Schultag", None]

QR_NACHRICHTEN = [
    "GUTSCHEIN: Du darfst dir den Platz am Tisch aussuchen.",
    "GUTSCHEIN: Heute bestellst du fuer alle.",
    "GUTSCHEIN: Einmal Nachtisch extra, weil reserviert wurde.",
    "Warum kommt der Tisch nie zu spaet? Er ist immer gedeckt.",
    "Was sagt der Stuhl zum Tisch? Nichts, Moebel reden nicht.",
    "Wie nennt man einen reservierten Tisch? Belegt und gluecklich.",
]


def _aufzaehlung(namen: list[str]) -> str:
    """['Mia', 'Ben', 'Lea'] -> 'Mia, Ben & Lea'"""
    if len(namen) == 1:
        return namen[0]
    return ", ".join(namen[:-1]) + f" & {namen[-1]}"


def erstelle_bon(drucker):
    now = datetime.now()
    nummer = random.randint(100, 999)
    tisch = random.randint(1, 24)

    # Gewichtet Richtung klein: die meisten Reservierungen sind die eigene
    # Familie, ein großer Freundeskreis ist die Ausnahme, nicht die Regel.
    personen = random.choices(
        [2, 3, 4, 5, 6], weights=[3, 3, 2, 1, 1], k=1
    )[0]
    platz = random.randint(1, personen)

    # Passt die Personenzahl zu den hinterlegten Vornamen, werden die Gäste
    # namentlich genannt statt nur gezählt – siehe config.GUEST_FIRST_NAMES.
    namen = config.GUEST_FIRST_NAMES
    if personen <= len(namen):
        gaeste = random.sample(namen, k=personen)
        auf_den_namen = _aufzaehlung(gaeste)
        anlass = random.choice(ANLAESSE_KLEIN)
    else:
        auf_den_namen = f"Fam. {random.choice(config.GUEST_NAMES)}"
        anlass = random.choice(ANLAESSE_GROSS)

    # Reservierung liegt zwischen heute und in einer Woche
    wann = now + timedelta(days=random.randint(0, 7))
    uhrzeit = random.choice(["12:00", "12:30", "17:30", "18:00",
                             "18:30", "19:00", "19:30"])

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

    drucker.text(layout.row("Auf den Namen", auf_den_namen))
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
