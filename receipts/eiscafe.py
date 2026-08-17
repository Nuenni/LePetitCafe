import random
from datetime import datetime

from . import layout

LADEN_NAME = "LE PETIT CAFÉ"
SLOGAN     = "Eis · Waffeln · Träume"

EISSORTEN = [
    "Vanille", "Schokolade", "Erdbeere", "Haselnuss",
    "Pistazie", "Zitrone", "Joghurt", "Karamell",
    "Bubblegum", "Stracciatella", "Mango", "Himbeere",
    "Kokos", "Mint Choc Chip", "Tiramisu",
]

# (Name, Preis, Kugeln)
# Kugeln = Anzahl frei wählbarer Eissorten, die auf dem Bon aufgelistet werden.
#   0 = fertige Kreation oder Verpacktes am Stiel. Bei einem Krokantbecher oder
#       einem Magnum steht die Sorte ja schon im Namen – da wäre eine zufällige
#       Sortenliste Unfug.
KARTE = [
    # Kugeln und Waffeln
    ("Eiskugel",              1.20, 1),
    ("Waffeleis (2 Kugeln)",  2.40, 2),
    ("Waffeleis (3 Kugeln)",  3.40, 3),
    ("Heiße Waffel m. Eis",   4.50, 2),

    # Becher zum Selbstzusammenstellen
    ("Eisbecher klein",       3.50, 2),
    ("Eisbecher groß",        5.50, 3),

    # Eisbecher-Klassiker
    ("Spaghettieis",          5.90, 0),
    ("Krokantbecher",         5.90, 0),
    ("After Eight Becher",    6.20, 0),
    ("Schwarzwald Becher",    6.50, 0),
    ("Bananasplit",           6.20, 0),

    # Für die Kleinen
    ("Kindereisbecher",       3.20, 1),
    ("Pinocchio Becher",      4.50, 0),
    ("Biene Maja Becher",     4.50, 0),

    # Eis am Stiel
    ("Magnum Schokolade",     2.50, 0),
    ("Magnum White",          2.50, 0),
    ("Solero",                2.20, 0),
    ("Calippo",               1.80, 0),
    ("Twister",               1.80, 0),

    # Getränke und Süßes
    ("Eisschokolade",         3.80, 0),
    ("Milchshake Erdbeere",   4.20, 0),
    ("Milchshake Vanille",    4.20, 0),
    ("Affogato",              3.90, 0),
    ("Limonade",              2.50, 0),
    ("Wasser still",          1.80, 0),
    ("Kakao",                 2.80, 0),
]

KELLNER = ["Anna", "Tom", "Lena", "Felix", "Clara", "Ben"]

def erstelle_bon(drucker):
    now      = datetime.now()
    bonNr    = random.randint(100, 999)
    tisch    = random.randint(1, 8)
    kellner  = random.choice(KELLNER)
    anzahl   = random.randint(3, 7)

    auswahl  = random.sample(KARTE, k=min(anzahl, len(KARTE)))
    positionen = [
        (name, preis, kugeln, random.randint(1, 2))
        for name, preis, kugeln in auswahl
    ]

    summe    = sum(preis * menge for _, preis, _, menge in positionen)
    trinkgeld_pct = random.choice([0, 5, 10])
    trinkgeld = round(summe * trinkgeld_pct / 100, 2)
    gesamt   = summe + trinkgeld

    drucker.set(align="center", bold=True, double_height=True, double_width=True)
    drucker.text(f"{LADEN_NAME}\n")
    drucker.set(align="center", bold=False, double_height=False, double_width=False)
    drucker.text("✿  " + SLOGAN + "  ✿\n")
    drucker.text(layout.wrapped("Seepromenade 3 · 12345 Sonnenstadt"))
    drucker.text(layout.divider())

    drucker.set(align="left")
    drucker.text(f"Tisch:    {tisch:<4}  Bon-Nr.: {bonNr}\n")
    drucker.text(f"Bedienung: {kellner}\n")
    drucker.text(f"Uhrzeit:  {now.strftime('%H:%M')} Uhr\n")
    drucker.text(layout.divider())

    for name, preis, kugeln, menge in positionen:
        gesamt_pos = preis * menge
        drucker.text(layout.wrapped(f"{menge}x {name}"))
        drucker.text(f"   {menge} x {preis:.2f}€ = {gesamt_pos:.2f}€\n")
        if kugeln:
            sorten = random.sample(EISSORTEN, k=min(kugeln * menge, len(EISSORTEN)))
            drucker.text(layout.wrapped(f"({', '.join(sorten)})", indent=3))

    drucker.text(layout.divider("═"))
    drucker.set(bold=True)
    drucker.text(layout.row("Zwischensumme", layout.money(summe)))
    drucker.set(bold=False)
    if trinkgeld_pct > 0:
        drucker.text(layout.row(f"Trinkgeld {trinkgeld_pct}%", layout.money(trinkgeld)))
    drucker.set(bold=True, double_height=True)
    drucker.text(layout.row("GESAMT", layout.money(gesamt)))
    drucker.set(bold=False, double_height=False)

    drucker.text(layout.divider())
    drucker.set(align="center")
    drucker.text("Zahlung: Bar\n")
    drucker.text(f"{now.strftime('%d.%m.%Y')}\n")
    drucker.text("\n")
    drucker.text("★  Danke für Ihren Besuch!  ★\n")
    drucker.text("Wir wünschen einen\n")
    drucker.text("wunderschönen Tag!\n")
    drucker.text("✿ ✿ ✿\n")
    drucker.cut()
