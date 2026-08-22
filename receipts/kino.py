"""Kinokarte mit Sitzplatz und Snacks."""

import random
from datetime import datetime, timedelta

from . import layout
import config

# Erfundene Titel – klingt nach Kinderkino, ohne echte Filme zu bemühen.
FILME = [
    ("Die Abenteuer der mutigen Maus",  84),
    ("Rennmaus in der Rakete",          91),
    ("Das Geheimnis der blauen Tür",    97),
    ("Pinguine im Dschungel",           78),
    ("Mein Freund der Roboter",        102),
    ("Die Piratenprinzessin",           88),
    ("Wo die Wolken wohnen",            75),
    ("Ein Elefant zu viel",             81),
    ("Der Zauberwald",                  94),
]

TICKETS = [
    ("Kinderticket",   6.50),
    ("Ticket",         9.50),
    ("Ticket ermäßigt", 7.50),
]

SNACKS = [
    ("Popcorn klein",     3.50),
    ("Popcorn groß",      4.50),
    ("Nachos mit Käse",   5.20),
    ("Gummibärchen",      2.20),
    ("Salzbrezel",        2.50),
    ("Limonade",          2.80),
    ("Eis am Stiel",      2.50),
    ("Slush-Eis",         3.20),
]

WITZE = [
    "Warum ging der Keks ins Kino? Er wollte einen Kruemel-Film sehen.",
    "Was macht ein Popcorn im Kino? Es platzt vor Spannung!",
    "Warum sind Filme nie muede? Sie haben immer eine Rolle zu spielen.",
]


def erstelle_bon(drucker):
    now = datetime.now()
    nummer = random.randint(1000, 9999)
    film, dauer = random.choice(FILME)
    saal = random.randint(1, 6)
    reihe = random.randint(3, 14)
    anzahl = random.randint(1, 4)
    erster_platz = random.randint(1, 18)
    plaetze = list(range(erster_platz, erster_platz + anzahl))

    beginn = now + timedelta(minutes=random.choice([15, 30, 45, 60]))
    ende = beginn + timedelta(minutes=dauer)

    ticket_art, ticket_preis = random.choice(TICKETS)
    snacks = random.sample(SNACKS, k=random.randint(0, 2))

    summe = ticket_preis * anzahl + sum(p for _, p in snacks)

    drucker.set(align="center", bold=True, double_height=True, double_width=True)
    drucker.text("LE PETIT CINÉMA\n")
    drucker.set(normal_textsize=True, align="center", bold=False, double_height=False,
                double_width=False)
    drucker.text("KinderKino\n")
    drucker.text(layout.divider())

    # Filmtitel groß – das ist die Information, die zählt
    drucker.set(align="center", bold=False, double_height=False)
    drucker.text("Heute läuft:\n")
    drucker.set(align="center", bold=True, double_height=True)
    drucker.text(layout.wrapped(film.upper()))
    drucker.set(normal_textsize=True, align="left", bold=False, double_height=False)
    drucker.text(layout.divider())

    drucker.text(layout.row("Saal", str(saal)))
    drucker.text(layout.row("Reihe", str(reihe)))
    if anzahl == 1:
        drucker.text(layout.row("Platz", str(plaetze[0])))
    else:
        drucker.text(layout.row("Plätze",
                                f"{plaetze[0]}–{plaetze[-1]} ({anzahl} Personen)"))
    drucker.text(layout.divider())
    drucker.text(layout.row("Beginn", beginn.strftime("%H:%M Uhr")))
    drucker.text(layout.row("Ende (ca.)", ende.strftime("%H:%M Uhr")))
    drucker.text(layout.row("Dauer", f"{dauer} Minuten"))
    drucker.text(layout.row("Freigegeben", "ab 0 Jahren"))
    drucker.text(layout.divider("═"))

    if anzahl == 1:
        drucker.text(layout.item(ticket_art, ticket_preis))
    else:
        drucker.text(layout.item(f"{anzahl}x {ticket_art}",
                                 ticket_preis * anzahl))
    for name, preis in snacks:
        drucker.text(layout.item(name, preis))

    drucker.text(layout.divider())
    drucker.set(bold=True, double_height=True)
    drucker.text(layout.row("GESAMT", layout.money(summe)))
    drucker.set(normal_textsize=True, bold=False, double_height=False)

    drucker.set(align="center")
    drucker.text("\n")
    drucker.text(layout.wrapped("Bitte am Eingang vorzeigen"))
    drucker.text(layout.wrapped("Viel Spaß im Kino!"))
    qr_inhalt = (layout.voucher_url("de") if random.random() < 0.5
                 else layout.joke_url("de", random.choice(WITZE)))
    layout.codes(drucker, qr_inhalt, f"KINO{nummer:04d}", "Scann mich!")
    drucker.cut()
