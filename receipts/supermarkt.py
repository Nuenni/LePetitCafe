import random
from datetime import datetime

LADEN_NAME = "PETIT MARCHÉ"
SLOGAN     = "Frisch. Lecker. Günstig."

SORTIMENT = [
    ("Vollmilch 1L",        0.89,  "1 St."),
    ("Vollmilch 1L",        0.89,  "2 St."),
    ("Butter 250g",         1.49,  "1 St."),
    ("Eier 6er Pack",       1.79,  "1 St."),
    ("Käse Scheiben",       2.19,  "1 Pck."),
    ("Joghurt Erdbeere",    0.55,  "2 St."),
    ("Joghurt Erdbeere",    0.55,  "3 St."),
    ("Bananen",             0.99,  "1 Bund"),
    ("Äpfel Elstar",        1.29,  "1 kg"),
    ("Orangen",             0.79,  "3 St."),
    ("Karotten",            0.69,  "500 g"),
    ("Tomaten",             1.09,  "500 g"),
    ("Salatgurke",          0.49,  "1 St."),
    ("Eisbergsalat",        0.79,  "1 St."),
    ("Toastbrot",           1.19,  "1 Pck."),
    ("Brezel",              0.39,  "2 St."),
    ("Schokolade Vollmilch",0.99,  "1 Tfl."),
    ("Gummibärchen",        0.89,  "1 Tüte"),
    ("Apfelsaft 1L",        1.49,  "1 Fl."),
    ("Mineralwasser 1L",    0.35,  "2 Fl."),
    ("Nudeln Spaghetti",    0.79,  "500 g"),
    ("Tomatensauce",        0.99,  "1 Glas"),
    ("Cornflakes",          2.49,  "1 Pck."),
    ("Müsli Früchte",       3.29,  "1 Pck."),
    ("Waschmittel",         4.99,  "1 Pck."),
    ("Spülmittel",          0.95,  "1 Fl."),
    ("Klopapier 4er",       1.99,  "1 Pck."),
    ("Shampoo",             2.49,  "1 Fl."),
]

KASSIERER = ["Emilia", "Max", "Sophie", "Lukas", "Mia", "Jonas"]

def erstelle_bon(drucker):
    now    = datetime.now()
    items  = random.sample(SORTIMENT, k=random.randint(4, 9))
    summe  = sum(i[1] for i in items)
    mwst   = summe * 0.19
    name   = random.choice(KASSIERER)
    bonNr  = random.randint(1000, 9999)
    kasse  = random.randint(1, 4)

    drucker.set(align="center", bold=True, double_height=True, double_width=True)
    drucker.text(f"{LADEN_NAME}\n")
    drucker.set(align="center", bold=False, double_height=False, double_width=False)
    drucker.text(f"{SLOGAN}\n")
    drucker.text("Hauptstr. 12 · 12345 Musterstadt\n")
    drucker.text("Tel: 01234 / 567890\n")
    drucker.text("─" * 32 + "\n")

    drucker.set(align="left")
    drucker.text(f"Datum:  {now.strftime('%d.%m.%Y')}\n")
    drucker.text(f"Uhrzeit:{now.strftime('%H:%M')} Uhr\n")
    drucker.text(f"Kasse:  {kasse}   Bon-Nr.: {bonNr}\n")
    drucker.text(f"Kassierer/in: {name}\n")
    drucker.text("─" * 32 + "\n")

    for artikel, preis, menge in items:
        zeile = f"{artikel[:20]:<20} {preis:>5.2f}€"
        drucker.text(zeile + "\n")
        drucker.text(f"  ({menge})\n")

    drucker.text("═" * 32 + "\n")
    drucker.set(bold=True)
    drucker.text(f"{'SUMME':<20} {summe:>7.2f}€\n")
    drucker.set(bold=False)
    drucker.text(f"{'darin MwSt. 19%':<20} {mwst:>7.2f}€\n")
    drucker.text("─" * 32 + "\n")

    gezahlt = _runden_auf_50ct(summe)
    rueck   = gezahlt - summe
    drucker.text(f"{'Gegeben (Bar)':<20} {gezahlt:>7.2f}€\n")
    drucker.set(bold=True, double_height=True)
    drucker.text(f"{'RUECKGELD':<16} {rueck:>7.2f}€\n")
    drucker.set(bold=False, double_height=False)

    drucker.text("─" * 32 + "\n")
    drucker.set(align="center")
    drucker.text(f"{random.choice(_sprueche())}\n")
    drucker.text("Vielen Dank für Ihren Einkauf!\n")
    drucker.text("Auf Wiedersehen!\n")
    drucker.cut()

def _runden_auf_50ct(betrag):
    import math
    return math.ceil(betrag * 2) / 2

def _sprueche():
    return [
        "★ Guten Appetit! ★",
        "★ Schönen Tag noch! ★",
        "★ Bleiben Sie gesund! ★",
        "★ Wir freuen uns auf Sie! ★",
        "★ Danke, kleiner Einkäufer! ★",
    ]
