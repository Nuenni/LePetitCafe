"""Fahrschein für Bus oder Taxi – der Weg zwischen den Spielwelten."""

import random
from datetime import datetime, timedelta

from . import layout
import config

# Die Haltestellen greifen die Adressen der anderen Bons auf: Hauptstraße ist
# der Supermarkt, Seepromenade das Eiscafé, Marktplatz das Bistro. So führt
# eine Fahrt immer irgendwo hin, wo man danach weiterspielen kann.
HALTESTELLEN = [
    "Hauptstraße",
    "Seepromenade",
    "Marktplatz",
    "Kinoplatz",
    "Bahnhof",
    "Zoo",
    "Schwimmbad",
    "Spielplatz",
]

FAHRKARTEN = [
    ("Kurzstrecke",       1.20,  30),
    ("Einzelfahrkarte",   1.80,  90),
    ("Kinderfahrkarte",   0.90,  90),
    ("Tageskarte",        4.50, 600),
    ("Familienkarte",     7.90, 600),
]

WAGENFARBEN = ["gelb", "creme", "silber", "schwarz"]

WITZE = [
    "Warum sitzt der Bus nie? Er hat schon genug Sitze!",
    "Was ist gelb und faehrt im Kreis? Ein Taxi im Kreisverkehr.",
    "Wie kommt ein Igel in den Bus? Durch die Tuer, wie alle anderen.",
]


def erstelle_bon(drucker):
    if random.random() < 0.6:
        _bus(drucker)
    else:
        _taxi(drucker)


def _strecke() -> tuple[str, str]:
    von, nach = random.sample(HALTESTELLEN, k=2)
    return von, nach


def _kopf(drucker, name: str, slogan: str) -> None:
    drucker.set(align="center", bold=True, double_height=True, double_width=True)
    drucker.text(f"{name}\n")
    drucker.set(normal_textsize=True, align="center", bold=False, double_height=False,
                double_width=False)
    drucker.text(f"*  {slogan}  *\n")
    drucker.text(layout.divider())


def _fuss(drucker, hinweis: str, nummer: str) -> None:
    drucker.set(align="center")
    drucker.text("\n")
    drucker.text(layout.wrapped(hinweis))
    qr_inhalt = (layout.voucher_url("de") if random.random() < 0.5
                 else layout.joke_url("de", random.choice(WITZE)))
    layout.codes(drucker, qr_inhalt, nummer, "Scann mich!")
    drucker.cut()


def _bus(drucker):
    now = datetime.now()
    nummer = random.randint(1000, 9999)
    linie = random.choice([1, 3, 5, 7, 8, 12, 21, 42])
    von, nach = _strecke()
    art, preis, minuten = random.choice(FAHRKARTEN)
    gueltig_bis = now + timedelta(minutes=minuten)

    _kopf(drucker, "LE PETIT EXPRESS", "Einsteigen bitte!")

    drucker.set(align="center", bold=True, double_height=True)
    drucker.text(f"{art.upper()}\n")
    drucker.set(normal_textsize=True, align="left", bold=False, double_height=False)
    drucker.text(layout.divider())

    drucker.text(layout.row("Linie", str(linie)))
    drucker.text(layout.row("Von", von))
    drucker.text(layout.row("Nach", nach))
    drucker.text(layout.divider())
    drucker.text(layout.row("Abfahrt", now.strftime("%H:%M Uhr")))
    drucker.text(layout.row("Gültig bis", gueltig_bis.strftime("%H:%M Uhr")))
    drucker.text(layout.row("Fahrer/in", random.choice(config.STAFF_NAMES)))
    drucker.text(layout.divider("═"))

    drucker.set(bold=True, double_height=True)
    drucker.text(layout.row("ZU ZAHLEN", layout.money(preis)))
    drucker.set(normal_textsize=True, bold=False, double_height=False)

    _fuss(drucker, "Bitte beim Einsteigen vorzeigen", f"BUS{nummer:05d}")


def _taxi(drucker):
    now = datetime.now()
    nummer = random.randint(1000, 9999)
    wagen = random.randint(1, 99)
    von, nach = _strecke()
    km = round(random.uniform(1.2, 9.8), 1)
    minuten = max(3, int(km * random.uniform(2.0, 3.5)))

    grundpreis = 3.90
    pro_km = 2.10
    strecke = round(km * pro_km, 2)
    summe = grundpreis + strecke

    _kopf(drucker, "PETIT TAXI", "Immer für Sie da")

    drucker.set(align="left")
    drucker.text(layout.row("Wagen-Nr.", f"{wagen:02d}"))
    drucker.text(layout.row("Fahrer/in", random.choice(config.STAFF_NAMES)))
    drucker.text(layout.row("Farbe", random.choice(WAGENFARBEN)))
    drucker.text(layout.divider())
    drucker.text(layout.row("Von", von))
    drucker.text(layout.row("Nach", nach))
    drucker.text(layout.row("Strecke", f"{km:.1f} km".replace(".", ",")))
    drucker.text(layout.row("Fahrzeit", f"{minuten} Minuten"))
    drucker.text(layout.row("Ankunft", now.strftime("%H:%M Uhr")))
    drucker.text(layout.divider("═"))

    drucker.text(layout.row("Grundpreis", layout.money(grundpreis)))
    drucker.text(layout.row(f"{km:.1f} km à 2,10€".replace(".", ","),
                            layout.money(strecke)))
    drucker.set(bold=True, double_height=True)
    drucker.text(layout.row("ZU ZAHLEN", layout.money(summe)))
    drucker.set(normal_textsize=True, bold=False, double_height=False)

    _fuss(drucker, "Gute Fahrt und bis zum nächsten Mal!", f"TAXI{nummer:04d}")
