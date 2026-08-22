"""
Geheimer Extra-Bon: eine zufaellige Feierabend-Rezeptidee.

Bewusst schnelle Alltagsgerichte fuer 4-6 Personen mit Zutaten, die oft
schon im Haushalt sind - kein Spezialeinkauf noetig. Mehrfach druecken
gibt eine neue Idee.
"""

import random
from datetime import datetime

from . import layout

# (Name, Minuten, Zutaten mit Menge, Zubereitungsschritte)
REZEPTE = [
    ("Spaghetti Aglio e Olio", 20,
     ["500g Spaghetti", "6 Zehen Knoblauch", "100ml Olivenoel",
      "1 TL Chiliflocken", "1 Bund Petersilie", "80g Parmesan"],
     ["Spaghetti in Salzwasser kochen.",
      "Knoblauch fein hacken, in Olivenoel sanft anbraten.",
      "Chiliflocken dazugeben, kurz mitbraten.",
      "Nudeln abgiessen, mit dem Oel vermischen.",
      "Mit Petersilie und Parmesan bestreuen."]),
    ("Tomaten-Nudeln mit Thunfisch", 20,
     ["500g Nudeln", "2 Dosen Tomaten", "2 Dosen Thunfisch",
      "1 Zwiebel", "2 Zehen Knoblauch", "50g Oliven"],
     ["Nudeln kochen.",
      "Zwiebel und Knoblauch anbraten.",
      "Tomaten dazugeben, 10 Min koecheln.",
      "Thunfisch und Oliven unterruehren.",
      "Mit den Nudeln vermengen."]),
    ("Kartoffel-Gemüse-Pfanne", 30,
     ["1kg Kartoffeln", "1 Zwiebel", "2 Paprika", "6 Eier", "150g Käse"],
     ["Kartoffeln wuerfeln, in der Pfanne anbraten.",
      "Zwiebel und Paprika dazugeben.",
      "Eier verquirlen, daruebergiessen.",
      "Kaese darueberstreuen, stocken lassen."]),
    ("Rührei mit Speck und Toast", 15,
     ["10 Eier", "200g Speck", "8 Scheiben Toastbrot", "1 Bund Schnittlauch"],
     ["Speck knusprig anbraten.",
      "Eier verquirlen, dazugeben.",
      "Unter Ruehren stocken lassen.",
      "Mit Schnittlauch bestreuen, mit Toast servieren."]),
    ("Linsensuppe", 35,
     ["400g Linsen", "1 Zwiebel", "2 Karotten", "2 Kartoffeln",
      "1l Brühe", "2 EL Essig"],
     ["Zwiebel anbraten.",
      "Gemuese und Linsen dazugeben.",
      "Mit Bruehe auffuellen, 25 Min koecheln.",
      "Mit Essig abschmecken."]),
    ("Gebratener Reis mit Ei", 20,
     ["500g Reis (vom Vortag)", "4 Eier", "300g TK-Gemüse", "4 EL Sojasoße"],
     ["Gemuese in der Pfanne anbraten.",
      "Reis dazugeben, mitbraten.",
      "Verquirlte Eier einruehren.",
      "Mit Sojasosse abschmecken."]),
    ("Käsespätzle", 25,
     ["750g Spätzle", "300g Käse", "2 Zwiebeln"],
     ["Zwiebeln in Ringen goldbraun braten.",
      "Spaetzle erhitzen, Kaese unterheben.",
      "Schichtweise mit Roestzwiebeln servieren."]),
    ("Herzhafte Pfannkuchen", 20,
     ["400g Mehl", "600ml Milch", "4 Eier", "2 EL Butter", "Füllung nach Wahl"],
     ["Mehl, Milch und Eier zu einem Teig verruehren.",
      "Butter in der Pfanne erhitzen.",
      "Portionsweise Pfannkuchen ausbacken.",
      "Nach Wunsch fuellen."]),
    ("Kartoffelpüree mit Bratwurst", 30,
     ["1,5kg Kartoffeln", "200ml Milch", "50g Butter", "6 Bratwürste"],
     ["Kartoffeln kochen, abgiessen.",
      "Mit Milch und Butter zu Puree stampfen.",
      "Bratwuerste braten.",
      "Zusammen servieren."]),
    ("Nudelauflauf mit Gemüse", 35,
     ["500g Nudeln", "400g TK-Gemüse", "200ml Sahne", "200g Käse"],
     ["Nudeln kochen.",
      "Mit Gemuese und Sahne mischen, in eine Form geben.",
      "Kaese darueberstreuen.",
      "20 Min bei 200°C ueberbacken."]),
    ("Omelett mit Käse und Kräutern", 15,
     ["8 Eier", "150g Käse", "1 Bund Kräuter", "100ml Milch"],
     ["Eier mit Milch verquirlen.",
      "In der Pfanne stocken lassen.",
      "Kaese und Kraeuter darueberstreuen, zusammenklappen."]),
    ("Chili sin Carne", 25,
     ["2 Dosen Kidneybohnen", "1 Dose Mais", "2 Dosen Tomaten",
      "1 Zwiebel", "2 Paprika"],
     ["Zwiebel und Paprika anbraten.",
      "Tomaten, Bohnen und Mais dazugeben.",
      "15 Min koecheln lassen, wuerzen."]),
    ("Griechischer Nudelsalat", 20,
     ["500g Nudeln", "200g Feta", "1 Gurke", "4 Tomaten",
      "100g Oliven", "Essig und Öl"],
     ["Nudeln kochen, abkuehlen lassen.",
      "Gemuese und Feta wuerfeln.",
      "Alles mit Essig und Oel vermengen."]),
    ("Ofenkartoffeln mit Kräuterquark", 40,
     ["1,5kg Kartoffeln", "500g Quark", "1 Bund Kräuter", "1 Zwiebel"],
     ["Kartoffeln halbieren, im Ofen backen (200°C, 35 Min).",
      "Quark mit Kraeutern und Zwiebel verruehren.",
      "Zusammen servieren."]),
    ("Tomatensuppe mit Grilled Cheese", 25,
     ["2 Dosen Tomaten", "1 Zwiebel", "200ml Sahne",
      "8 Scheiben Toast", "200g Käse"],
     ["Zwiebel anbraten, Tomaten dazugeben.",
      "Puerieren, mit Sahne verfeinern.",
      "Toast mit Kaese belegen, in der Pfanne goldbraun braten."]),
    ("Bratkartoffeln mit Spiegelei", 25,
     ["1kg Kartoffeln (gekocht)", "1 Zwiebel", "150g Speck", "6 Eier"],
     ["Kartoffeln in Scheiben braten.",
      "Zwiebel und Speck dazugeben.",
      "Spiegeleier separat braten, obenauf servieren."]),
    ("Couscous-Salat mit Gemüse", 15,
     ["400g Couscous", "2 Paprika", "1 Gurke", "1 Zitrone", "1 Bund Minze"],
     ["Couscous mit heissem Wasser uebergiessen, quellen lassen.",
      "Gemuese wuerfeln, untermischen.",
      "Mit Zitrone und Minze abschmecken."]),
    ("Zucchini-Puffer", 25,
     ["3 Zucchini", "4 Eier", "150g Mehl", "1 Zwiebel"],
     ["Zucchini raspeln, ausdruecken.",
      "Mit Eiern, Mehl und Zwiebel vermengen.",
      "Portionsweise in der Pfanne ausbacken."]),
    ("Erbsensuppe mit Würstchen", 25,
     ["500g TK-Erbsen", "2 Kartoffeln", "6 Würstchen", "1l Brühe"],
     ["Kartoffeln in Bruehe weich kochen.",
      "Erbsen dazugeben, puerieren.",
      "Wuerstchen erhitzen, in die Suppe geben."]),
    ("Reispfanne mit Hackfleisch", 30,
     ["400g Reis", "500g Hackfleisch", "1 Zwiebel",
      "2 Paprika", "2 EL Tomatenmark"],
     ["Hackfleisch anbraten.",
      "Zwiebel, Paprika und Tomatenmark dazugeben.",
      "Reis kochen, untermischen."]),
    ("Toast Hawaii", 10,
     ["8 Scheiben Toast", "8 Scheiben Schinken", "1 Dose Ananas", "200g Käse"],
     ["Toast mit Schinken und Ananas belegen.",
      "Mit Kaese bestreuen.",
      "Im Ofen ueberbacken, bis der Kaese schmilzt."]),
    ("Kartoffelsuppe", 35,
     ["1kg Kartoffeln", "2 Karotten", "1 Stange Lauch",
      "6 Würstchen", "1l Brühe"],
     ["Gemuese wuerfeln, in Bruehe weich kochen.",
      "Teilweise puerieren.",
      "Wuerstchen in Scheiben dazugeben."]),
    ("Gebratene Nudeln mit Gemüse", 20,
     ["500g Eiernudeln", "400g TK-Gemüse", "4 Eier", "4 EL Sojasoße"],
     ["Nudeln kochen.",
      "Gemuese anbraten, Nudeln dazugeben.",
      "Eier einruehren, mit Sojasosse abschmecken."]),
    ("Quesadillas mit Käse und Bohnen", 15,
     ["8 Tortillas", "300g Käse", "1 Dose Bohnen", "1 Zwiebel"],
     ["Tortilla mit Kaese, Bohnen und Zwiebel belegen.",
      "Mit einer zweiten Tortilla bedecken.",
      "Beidseitig in der Pfanne goldbraun braten."]),
    ("Bauernfrühstück", 25,
     ["1kg Kartoffeln (gekocht)", "200g Speck", "1 Zwiebel", "8 Eier"],
     ["Kartoffeln in Scheiben braten.",
      "Speck und Zwiebel dazugeben.",
      "Verquirlte Eier daruebergiessen, stocken lassen."]),
    ("Gemüsepfanne mit Feta", 20,
     ["600g TK-Gemüsemix", "200g Feta", "3 Zehen Knoblauch"],
     ["Gemuese in der Pfanne braten.",
      "Knoblauch dazugeben.",
      "Feta darueberbroeseln."]),
    ("Tomaten-Mozzarella-Nudeln", 20,
     ["500g Nudeln", "400g Kirschtomaten", "250g Mozzarella",
      "1 Bund Basilikum", "4 EL Olivenöl"],
     ["Nudeln kochen.",
      "Tomaten halbieren, in Oel anschwitzen.",
      "Mozzarella und Basilikum untermischen."]),
    ("Currywurst mit Pommes", 25,
     ["6 Würstchen", "300ml Currysoße", "1kg TK-Pommes"],
     ["Pommes im Ofen backen.",
      "Wuerstchen erhitzen, in Scheiben schneiden.",
      "Mit Currysosse uebergiessen."]),
    ("Kürbissuppe", 25,
     ["800g TK-Kürbis", "1 Zwiebel", "400ml Kokosmilch", "500ml Brühe"],
     ["Zwiebel anbraten.",
      "Kuerbis und Bruehe dazugeben, 15 Min koecheln.",
      "Puerieren, Kokosmilch einruehren."]),
    ("Flammkuchen", 20,
     ["2 Flammkuchenteige", "200g Crème fraîche", "1 Zwiebel", "150g Speck"],
     ["Teig mit Creme fraiche bestreichen.",
      "Zwiebel und Speck darauf verteilen.",
      "Bei 220°C ca. 12 Min backen."]),
]


def erstelle_bon(drucker):
    now = datetime.now()
    name, minuten, zutaten, schritte = random.choice(REZEPTE)

    drucker.set(align="center", bold=True, double_height=True, double_width=True)
    drucker.text("LE PETIT BISTRO\n")
    drucker.set(normal_textsize=True, align="center", bold=True, double_height=True, double_width=False)
    drucker.text("*  Rezept-Idee  *\n")
    drucker.set(normal_textsize=True, align="center", bold=False, double_height=False)
    drucker.text(layout.divider())

    drucker.set(align="left")
    drucker.text("Für:      4-6 Personen\n")
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

    drucker.text(layout.divider())
    drucker.text("Zubereitung:\n")
    for nummer, schritt in enumerate(schritte, start=1):
        drucker.text(layout.wrapped(f"{nummer}. {schritt}", indent=3))

    drucker.text(layout.divider("═"))
    drucker.set(align="center")
    drucker.text(layout.wrapped("Nochmal die Kombi drücken für eine andere Idee!"))
    drucker.text("\n")
    drucker.text("* * *\n")
    drucker.cut()
