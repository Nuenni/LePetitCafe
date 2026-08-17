import random
from datetime import datetime

from . import layout

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

# Landet im QR-Code auf dem Bon. Ohne Umlaute, siehe layout.codes().
QR_NACHRICHTEN = [
    "GUTSCHEIN: Du darfst heute aussuchen, was es zum Nachtisch gibt!",
    "GUTSCHEIN: Einmal den Einkaufswagen schieben - ganz allein!",
    "GUTSCHEIN: Eine Kugel Eis extra. Einzuloesen bei Mama oder Papa.",
    "Warum nehmen Bienen keinen Einkaufswagen? Sie haben doch Koerbchen!",
    "Was ist orange und wandert durch die Berge? Eine Wanderine!",
    "Treffen sich zwei Kekse. Sagt der eine: Du kruemelst ja!",
]

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
    drucker.text(layout.divider())

    drucker.set(align="left")
    drucker.text(f"Datum:  {now.strftime('%d.%m.%Y')}\n")
    drucker.text(f"Uhrzeit:{now.strftime('%H:%M')} Uhr\n")
    drucker.text(f"Kasse:  {kasse}   Bon-Nr.: {bonNr}\n")
    drucker.text(f"Kassierer/in: {name}\n")
    drucker.text(layout.divider())

    for artikel, preis, menge in items:
        drucker.text(layout.item(artikel, preis))
        drucker.text(f"  ({menge})\n")

    drucker.text(layout.divider("═"))
    drucker.set(bold=True)
    drucker.text(layout.row("SUMME", layout.money(summe)))
    drucker.set(bold=False)
    drucker.text(layout.row("darin MwSt. 19%", layout.money(mwst)))
    drucker.text(layout.divider())

    gezahlt = _runden_auf_50ct(summe)
    rueck   = gezahlt - summe
    drucker.text(layout.row("Gegeben (Bar)", layout.money(gezahlt)))
    drucker.set(bold=True, double_height=True)
    drucker.text(layout.row("RUECKGELD", layout.money(rueck)))
    drucker.set(bold=False, double_height=False)

    drucker.text(layout.divider())
    drucker.set(align="center")
    drucker.text(f"{random.choice(_sprueche())}\n")
    drucker.text("Vielen Dank für Ihren Einkauf!\n")
    drucker.text("Auf Wiedersehen!\n")
    layout.codes(drucker, random.choice(QR_NACHRICHTEN),
                 f"LPC{bonNr:05d}", "Scann mich!")
    drucker.cut()

def _runden_auf_50ct(betrag):
    import math
    return math.ceil(betrag * 2) / 2

def _sprueche():
    return [
        "* Guten Appetit! *",
        "* Schönen Tag noch! *",
        "* Bleiben Sie gesund! *",
        "* Wir freuen uns auf Sie! *",
        "* Danke, kleiner Einkäufer! *",
    ]
