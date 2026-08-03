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

MENU = {
    "Eiskugel (1 Kugel)":    1.20,
    "Eisbecher klein":        3.50,
    "Eisbecher groß":         5.50,
    "Waffeleis (2 Kugeln)":   2.40,
    "Waffeleis (3 Kugeln)":   3.40,
    "Eisschokolade":          3.80,
    "Milchshake Erdbeere":    4.20,
    "Milchshake Vanille":     4.20,
    "Spaghettieis":           5.90,
    "Heiße Waffel m. Eis":    4.50,
    "Affogato":               3.90,
    "Kindereisbecher":        3.20,
    "Limonade":               2.50,
    "Wasser still":           1.80,
    "Kakao":                  2.80,
}

KELLNER = ["Anna", "Tom", "Lena", "Felix", "Clara", "Ben"]

def erstelle_bon(drucker):
    now      = datetime.now()
    bonNr    = random.randint(100, 999)
    tisch    = random.randint(1, 8)
    kellner  = random.choice(KELLNER)
    anzahl   = random.randint(2, 6)

    auswahl  = random.sample(list(MENU.items()), k=min(anzahl, len(MENU)))
    mengen   = [random.randint(1, 2) for _ in auswahl]
    positionen = [(name, preis, menge) for (name, preis), menge in zip(auswahl, mengen)]

    summe    = sum(p * m for _, p, m in positionen)
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

    for name, preis, menge in positionen:
        gesamt_pos = preis * menge
        drucker.text(layout.wrapped(f"{menge}x {name}"))
        drucker.text(f"   {menge} x {preis:.2f}€ = {gesamt_pos:.2f}€\n")
        # Eissorten-Hinweis wenn relevant
        if "kugel" in name.lower() or "waffeleis" in name.lower() or "becher" in name.lower():
            kugeln = random.sample(EISSORTEN, k=min(3, menge * 2))
            drucker.text(layout.wrapped(f"({', '.join(kugeln)})", indent=3))

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
