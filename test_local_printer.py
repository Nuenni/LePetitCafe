#!/usr/bin/env python3
"""
Local print test over USB - for your own computer (Mac/Linux), not the Pi.

    python3 test_local_printer.py

Simulates the six buttons as a text menu and prints over the USB printer
connected directly to your computer. Uses the same receipt generators as
main.py on the Pi - only the connection to the printer differs
(escpos.printer.Usb instead of File('/dev/usb/lp0'), because there's no
/dev/usb/lp0 on a Mac).

Setup:
    pip3 install python-escpos pyusb
    brew install libusb        # macOS only

If the printer isn't found even though it's plugged in: most likely macOS
auto-registered it as a system printer and is holding it busy. Fix: System
Settings -> Printers & Scanners -> remove the printer there, then try this
script again.
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

# Epson TM-T20II. Other Epson models usually share the same idVendor but a
# different idProduct - if in doubt, check on the Mac with:
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
    print("Connecting to the printer …")
    try:
        drucker = _drucker_verbinden()
    except Exception as exc:
        print(f"\n✗ Printer unreachable: {exc}\n")
        print("Check:")
        print("  - Is the printer switched on and connected via USB?")
        print("  - pip3 install python-escpos pyusb   (+ brew install libusb on the Mac)")
        print("  - macOS: System Settings -> Printers & Scanners -> remove the printer there,")
        print("    if it got auto-registered as a system printer.")
        return 1

    print(f"✓ Connected (idVendor=0x{ID_VENDOR:04X}, idProduct=0x{ID_PRODUCT:04X})\n")

    while True:
        print("Which button?")
        for taste, name, _ in WELTEN:
            print(f"  {taste}) {name}")
        print("  q) Quit")

        wahl = input("> ").strip().lower()
        if wahl in ("q", "quit", "exit"):
            break

        treffer = next((w for w in WELTEN if w[0] == wahl), None)
        if not treffer:
            print("Invalid input.\n")
            continue

        _, name, bon_fn = treffer
        print(f"Printing: {name} …")
        try:
            bon_fn(drucker)
            print("✓ printed\n")
        except Exception as exc:
            print(f"✗ Print error: {exc}\n")

    drucker.close()
    print("See you!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
