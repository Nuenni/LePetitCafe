import random
from datetime import datetime

from . import layout
import config

LADEN_NAME = "LE PETIT BISTRO"
SLOGAN     = "Bon appétit!"

VORSPEISEN = [
    ("Tomatensuppe",           4.90),
    ("Bruschetta",             5.50),
    ("Gemischter Salat",       5.90),
    ("Garnelencocktail",       7.90),
    ("Käsesuppe",              4.50),
    ("Avocado Toast",          6.50),
]
HAUPTGERICHTE = [
    ("Spaghetti Bolognese",    9.90),
    ("Pizza Margherita",       8.90),
    ("Pizza Salami",           9.50),
    ("Schnitzel m. Pommes",   12.90),
    ("Lachsfilet m. Reis",    14.90),
    ("Gemüse-Curry",           9.90),
    ("Hamburger Klassisch",   11.50),
    ("Tortellini Panna",       10.90),
    ("Hähnchen-Nuggets",       8.50),
    ("Kinderteller Nudeln",    6.90),
]
DESSERTS = [
    ("Schokoladen-Mousse",     4.50),
    ("Tiramisu",               4.90),
    ("Erdbeer-Panna Cotta",    4.50),
    ("Waffel m. Eis",          5.50),
    ("Crème brûlée",           5.90),
    ("Obstsalat",              3.90),
]
GETRAENKE = [
    ("Apfelsaft",              2.80),
    ("Orangensaft",            2.80),
    ("Limonade",               2.50),
    ("Wasser still 0,3L",      1.90),
    ("Wasser still 0,5L",      2.50),
    ("Kakao",                  3.20),
    ("Kinder-Cocktail",        3.50),
    ("Milch",                  1.80),
]


# Landet im QR-Code auf dem Bon. Ohne Umlaute, siehe layout.codes().
QR_NACHRICHTEN = [
    "GUTSCHEIN: Du bist heute der Chefkoch. Was gibt es?",
    "GUTSCHEIN: Einmal Tisch decken erlassen.",
    "GUTSCHEIN: Heute darfst du den Nachtisch zuerst essen.",
    "Kellner, eine Fliege in der Suppe! - Keine Sorge, die Spinne kommt gleich.",
    "Warum wurde die Tomate rot? Sie hat den Salat beim Umziehen gesehen!",
    "Was macht ein Koch, wenn er wuetend ist? Er brutzelt vor sich hin.",
]

def erstelle_bon(drucker):
    now     = datetime.now()
    bonNr   = random.randint(1, 99)
    tisch   = random.randint(1, 12)
    pers    = random.randint(2, 5)
    kellner = random.choice(config.STAFF_NAMES)

    bestellung = []

    # Vorspeisen (manchmal)
    if random.random() > 0.3:
        for _ in range(random.randint(1, min(pers, 3))):
            bestellung.append(random.choice(VORSPEISEN))

    # Hauptgerichte (fast immer)
    for _ in range(random.randint(pers - 1, pers)):
        bestellung.append(random.choice(HAUPTGERICHTE))

    # Desserts (manchmal)
    if random.random() > 0.4:
        for _ in range(random.randint(1, min(pers, 3))):
            bestellung.append(random.choice(DESSERTS))

    # Getränke
    for _ in range(random.randint(pers, pers + 1)):
        bestellung.append(random.choice(GETRAENKE))

    summe = sum(p for _, p in bestellung)
    mwst  = summe * 0.07  # Restaurant: 7% MwSt auf Speisen

    # Trinkgeld für die Bedienung. Die doppelte 0 sorgt dafür, dass etwa
    # jeder zweite Bon ohne auskommt – sonst wäre es keine nette Geste mehr,
    # sondern Routine.
    trinkgeld_pct = random.choice([0, 0, 5, 10])
    trinkgeld = round(summe * trinkgeld_pct / 100, 2)
    gesamt = summe + trinkgeld

    drucker.set(align="center", bold=True, double_height=True, double_width=True)
    drucker.text(f"{LADEN_NAME}\n")
    drucker.set(align="center", bold=False, double_height=False, double_width=False)
    drucker.text(f"*  {SLOGAN}  *\n")
    drucker.text("Marktplatz 7 · 12345 Genussstadt\n")
    drucker.text("www.lepetitbistro.de\n")
    drucker.text(layout.divider())

    drucker.set(align="left")
    drucker.text(f"Tisch:     {tisch:<3}  Bon-Nr.: {bonNr:02d}\n")
    drucker.text(f"Personen:  {pers}\n")
    drucker.text(f"Kellner/in:{kellner}\n")
    drucker.text(f"Datum:     {now.strftime('%d.%m.%Y  %H:%M')} Uhr\n")
    drucker.text(layout.divider())

    # Kategorien gruppiert ausgeben
    _kategorie_block(drucker, bestellung, VORSPEISEN,   "VORSPEISEN")
    _kategorie_block(drucker, bestellung, HAUPTGERICHTE, "HAUPTGERICHTE")
    _kategorie_block(drucker, bestellung, DESSERTS,      "DESSERTS")
    _kategorie_block(drucker, bestellung, GETRAENKE,     "GETRAENKE")

    drucker.text(layout.divider("═"))
    drucker.set(bold=True)
    drucker.text(layout.row("SUMME", layout.money(summe)))
    drucker.set(bold=False)
    drucker.text(layout.row("darin MwSt. 7%", layout.money(mwst)))
    if trinkgeld_pct:
        drucker.text(layout.row(f"Trinkgeld {trinkgeld_pct}%", layout.money(trinkgeld)))
        drucker.set(bold=True)
        drucker.text(layout.row("GESAMT", layout.money(gesamt)))
        drucker.set(bold=False)
    drucker.text(layout.divider())

    gezahlt = _runden_auf_50ct(gesamt)
    rueck   = gezahlt - gesamt
    drucker.text(layout.row("Gegeben (Bar)", layout.money(gezahlt)))
    drucker.set(bold=True, double_height=True)
    drucker.text(layout.row("RUECKGELD", layout.money(rueck)))
    drucker.set(bold=False, double_height=False)
    drucker.text(layout.divider())
    drucker.set(align="center")
    drucker.text("Zahlung: Bar\n\n")
    drucker.text(layout.wrapped("*  Vielen Dank für Ihren Besuch!  *"))
    drucker.text("Wir freuen uns, Sie\n")
    drucker.text("bald wieder zu sehen!\n")
    drucker.text("\n")
    drucker.text(f"{LADEN_NAME}\n")
    layout.codes(drucker, random.choice(QR_NACHRICHTEN),
                 f"LPB{bonNr:05d}", "Scann mich!")
    drucker.cut()

def _runden_auf_50ct(betrag):
    import math
    return math.ceil(betrag * 2) / 2

def _kategorie_block(drucker, bestellung, kategorie, titel):
    namen = {n for n, _ in kategorie}
    items = [(n, p) for n, p in bestellung if n in namen]
    if not items:
        return
    drucker.set(bold=True)
    drucker.text(f"  {titel}\n")
    drucker.set(bold=False)
    for name, preis in items:
        drucker.text(layout.item(name, preis, indent=2))
