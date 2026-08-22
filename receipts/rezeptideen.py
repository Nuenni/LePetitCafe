"""
Geheimer Extra-Bon: eine zufaellige Feierabend-Rezeptidee.

Bewusst schnelle Alltagsgerichte fuer 4-6 Personen mit Zutaten, die oft
schon im Haushalt sind - kein Spezialeinkauf noetig. Mehrfach druecken
gibt eine neue Idee.
"""

import random
from datetime import datetime

from . import layout

# (Name, Minuten, Zutaten)
REZEPTE = [
    ("Spaghetti Aglio e Olio", 20,
     ["Spaghetti", "Knoblauch", "Olivenoel", "Chiliflocken", "Petersilie", "Parmesan"]),
    ("Tomaten-Nudeln mit Thunfisch", 20,
     ["Nudeln", "Dose Tomaten", "Dose Thunfisch", "Zwiebel", "Knoblauch", "Oliven"]),
    ("Kartoffel-Gemuese-Pfanne", 30,
     ["Kartoffeln", "Zwiebel", "Paprika", "Eier", "Kaese"]),
    ("Ruehrei mit Speck und Toast", 15,
     ["Eier", "Speck", "Toastbrot", "Schnittlauch"]),
    ("Linsensuppe", 35,
     ["Linsen", "Zwiebel", "Karotte", "Kartoffel", "Bruehe", "Essig"]),
    ("Gebratener Reis mit Ei", 20,
     ["Reis (vom Vortag)", "Eier", "TK-Gemuese", "Sojasosse"]),
    ("Kaesespaetzle", 25,
     ["Spaetzle", "Kaese", "Zwiebel"]),
    ("Herzhafte Pfannkuchen", 20,
     ["Mehl", "Milch", "Eier", "Butter", "Fuellung nach Wahl"]),
    ("Kartoffelpueree mit Bratwurst", 30,
     ["Kartoffeln", "Milch", "Butter", "Bratwuerste"]),
    ("Nudelauflauf mit Gemuese", 35,
     ["Nudeln", "TK-Gemuese", "Sahne", "Kaese"]),
    ("Omelett mit Kaese und Kraeutern", 15,
     ["Eier", "Kaese", "Kraeuter", "Milch"]),
    ("Chili sin Carne", 25,
     ["Kidneybohnen (Dose)", "Mais (Dose)", "Tomaten (Dose)", "Zwiebel", "Paprika"]),
    ("Griechischer Nudelsalat", 20,
     ["Nudeln", "Feta", "Gurke", "Tomaten", "Oliven", "Essig und Oel"]),
    ("Ofenkartoffeln mit Kraeuterquark", 40,
     ["Kartoffeln", "Quark", "Kraeuter", "Zwiebel"]),
    ("Tomatensuppe mit Grilled Cheese", 25,
     ["Dosentomaten", "Zwiebel", "Sahne", "Toastbrot", "Kaese"]),
    ("Bratkartoffeln mit Spiegelei", 25,
     ["Kartoffeln", "Zwiebel", "Speck", "Eier"]),
    ("Couscous-Salat mit Gemuese", 15,
     ["Couscous", "Paprika", "Gurke", "Zitrone", "Minze"]),
    ("Zucchini-Puffer", 25,
     ["Zucchini", "Eier", "Mehl", "Zwiebel"]),
    ("Erbsensuppe mit Wuerstchen", 25,
     ["TK-Erbsen", "Kartoffel", "Wuerstchen", "Bruehe"]),
    ("Reispfanne mit Hackfleisch", 30,
     ["Reis", "Hackfleisch", "Zwiebel", "Paprika", "Tomatenmark"]),
    ("Toast Hawaii", 10,
     ["Toastbrot", "Schinken", "Ananas", "Kaese"]),
    ("Kartoffelsuppe", 35,
     ["Kartoffeln", "Karotte", "Lauch", "Wuerstchen", "Bruehe"]),
    ("Gebratene Nudeln mit Gemuese", 20,
     ["Eiernudeln", "TK-Gemuese", "Eier", "Sojasosse"]),
    ("Quesadillas mit Kaese und Bohnen", 15,
     ["Tortillas", "Kaese", "Bohnen (Dose)", "Zwiebel"]),
    ("Bauernfruehstueck", 25,
     ["Kartoffeln", "Speck", "Zwiebel", "Eier"]),
    ("Gemuesepfanne mit Feta", 20,
     ["TK-Gemuesemix", "Feta", "Knoblauch"]),
    ("Tomaten-Mozzarella-Nudeln", 20,
     ["Nudeln", "Kirschtomaten", "Mozzarella", "Basilikum", "Olivenoel"]),
    ("Currywurst mit Pommes", 25,
     ["Wuerstchen", "Currysosse", "TK-Pommes"]),
    ("Kuerbissuppe", 25,
     ["TK-Kuerbis", "Zwiebel", "Kokosmilch", "Bruehe"]),
    ("Flammkuchen", 20,
     ["Flammkuchenteig", "Creme fraiche", "Zwiebel", "Speck"]),
]


def erstelle_bon(drucker):
    now = datetime.now()
    name, minuten, zutaten = random.choice(REZEPTE)

    drucker.set(align="center", bold=True, double_height=True, double_width=True)
    drucker.text("LE PETIT CAFÉ\n")
    drucker.set(normal_textsize=True, align="center", bold=True, double_height=True, double_width=False)
    drucker.text("*  Rezept-Idee  *\n")
    drucker.set(normal_textsize=True, align="center", bold=False, double_height=False)
    drucker.text(layout.divider())

    drucker.set(align="left")
    drucker.text(f"Für:      4-6 Personen\n")
    drucker.text(f"Dauer:    ca. {minuten} Minuten\n")
    drucker.text(f"Uhrzeit:  {now.strftime('%H:%M')} Uhr\n")
    drucker.text(layout.divider())

    drucker.set(bold=True, double_height=True)
    drucker.text(layout.wrapped(name.upper()))
    drucker.set(normal_textsize=True, bold=False, double_height=False)
    drucker.text("\n")
    drucker.text("Zutaten:\n")
    for zutat in zutaten:
        drucker.text(layout.wrapped(f"- {zutat}", indent=1))

    drucker.text(layout.divider("═"))
    drucker.set(align="center")
    drucker.text(layout.wrapped("Nochmal die Kombi drücken für eine andere Idee!"))
    drucker.text("\n")
    drucker.text("* * *\n")
    drucker.cut()
