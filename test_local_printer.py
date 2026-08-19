#!/usr/bin/env python3
"""
Lokaler Drucktest über USB – für den eigenen Rechner (Mac/Linux), nicht den Pi.

    python3 test_local_printer.py

Simuliert die sechs Knöpfe als Text-Menü und druckt über den direkt am Rechner
angeschlossenen USB-Drucker. Nutzt dieselben Bon-Generatoren wie main.py auf
dem Pi – nur die Verbindung zum Drucker ist anders (escpos.printer.Usb statt
File('/dev/usb/lp0'), weil es auf dem Mac kein /dev/usb/lp0 gibt).

Vorbereitung:
    pip3 install python-escpos pyusb
    brew install libusb        # nur macOS

Falls der Drucker nicht gefunden wird, obwohl er eingesteckt ist: sehr
wahrscheinlich hat macOS ihn automatisch als Systemdrucker eingebunden und
hält ihn dadurch belegt. Abhilfe: Systemeinstellungen → Drucker & Scanner →
den Drucker dort entfernen, dann dieses Skript erneut versuchen.
"""

import sys

import config
from receipts import layout

if config.LANGUAGE == "de":
    from receipts import supermarkt as welt_markt
    from receipts import eiscafe as welt_eis
    from receipts import restaurant as welt_bistro
    from receipts import bus as welt_bus
    from receipts import kino as welt_kino
    from receipts import reservierung as welt_reservierung
else:
    from receipts import supermarket as welt_markt
    from receipts import icecream as welt_eis
    from receipts import bistro as welt_bistro
    from receipts import transit as welt_bus
    from receipts import cinema as welt_kino
    from receipts import reservation as welt_reservierung

# Epson TM-T20II. Andere Epson-Modelle haben meist dieselbe idVendor, aber
# eine andere idProduct – im Zweifel auf dem Mac nachsehen mit:
#   system_profiler SPUSBDataType | grep -A 5 -i epson
ID_VENDOR = 0x04B8
ID_PRODUCT = 0x0E15

WELTEN = [
    ("1", "Supermarkt",   welt_markt.erstelle_bon),
    ("2", "Eiscafé",      welt_eis.erstelle_bon),
    ("3", "Restaurant",   welt_bistro.erstelle_bon),
    ("4", "Bus/Taxi",     welt_bus.erstelle_bon),
    ("5", "KinderKino",   welt_kino.erstelle_bon),
    ("6", "Reservierung", welt_reservierung.erstelle_bon),
]


def _drucker_verbinden():
    from escpos.printer import Usb
    return Usb(ID_VENDOR, ID_PRODUCT, profile="TM-T20II", timeout=5000)


def main() -> int:
    print("Verbinde mit dem Drucker …")
    try:
        drucker = _drucker_verbinden()
    except Exception as exc:
        print(f"\n✗ Drucker nicht erreichbar: {exc}\n")
        print("Prüfen:")
        print("  - Drucker eingeschaltet und per USB verbunden?")
        print("  - pip3 install python-escpos pyusb   (+ brew install libusb auf dem Mac)")
        print("  - macOS: Systemeinstellungen → Drucker & Scanner → Drucker dort entfernen,")
        print("    falls er dort automatisch als Systemdrucker eingebunden wurde.")
        return 1

    print(f"✓ Verbunden (idVendor=0x{ID_VENDOR:04X}, idProduct=0x{ID_PRODUCT:04X})\n")

    while True:
        print("Welchen Knopf drücken?")
        for taste, name, _ in WELTEN:
            print(f"  {taste}) {name}")
        print("  q) Beenden")

        wahl = input("> ").strip().lower()
        if wahl in ("q", "quit", "exit"):
            break

        treffer = next((w for w in WELTEN if w[0] == wahl), None)
        if not treffer:
            print("Ungültige Eingabe.\n")
            continue

        _, name, bon_fn = treffer
        print(f"Drucke: {name} …")
        try:
            bon_fn(drucker)
            print("✓ gedruckt\n")
        except Exception as exc:
            print(f"✗ Druckfehler: {exc}\n")

    drucker.close()
    print("Bis dann!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
