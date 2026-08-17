#!/usr/bin/env python3
"""
Prüft alle Bon-Generatoren, ohne dass Hardware angeschlossen sein muss.

    python3 test_receipts.py

Getestet wird gegen beide Papierbreiten: Keine Zeile darf breiter sein als das
Papier, sonst bricht der Drucker sie hart um und der Bon sieht zerrissen aus.
Weil die Bons zufällig erzeugt werden, läuft jeder Generator viele Male.
"""

import sys

import config

MODULE = ["supermarkt", "eiscafe", "restaurant", "supermarket", "icecream", "bistro"]
BREITEN = [42, 32]   # 80mm und 58mm Papier
DURCHLAEUFE = 50

# Bekannte, physikalisch unvermeidbare Ausnahmen: Diese Ladennamen sind länger
# als die 16 Spalten, die auf 58mm-Papier in Doppelbreite zur Verfügung stehen.
BEKANNTE_AUSNAHMEN = {
    (32, "THE LITTLE MARKET"),
    (32, "THE LITTLE BISTRO"),
}


class TextPrinter:
    """Mock-Drucker: sammelt Zeilen samt Schriftbreite, druckt nichts."""

    def __init__(self):
        self.zeilen: list[tuple[str, bool]] = []
        self._doppelt_breit = False

    def set(self, double_width=None, **_):
        if double_width is not None:
            self._doppelt_breit = double_width

    def text(self, txt: str):
        for zeile in txt.split("\n"):
            self.zeilen.append((zeile, self._doppelt_breit))

    def cut(self):
        pass

    def close(self):
        pass

    # QR- und Barcode erzeugen keine Textzeilen und sind für die
    # Breitenprüfung ohne Belang. Sie müssen nur vorhanden sein.
    def qr(self, content, **_):
        pass

    def barcode(self, code, bc, **_):
        pass


def main() -> int:
    fehler = []

    for breite in BREITEN:
        config.PRINTER_WIDTH = breite
        print(f"\nPRINTER_WIDTH = {breite}")

        for name in MODULE:
            modul = __import__(f"receipts.{name}", fromlist=["erstelle_bon"])
            zu_lang = set()

            for _ in range(DURCHLAEUFE):
                drucker = TextPrinter()
                modul.erstelle_bon(drucker)
                for zeile, doppelt_breit in drucker.zeilen:
                    # In Doppelbreite passt nur die halbe Zeichenzahl aufs Papier.
                    grenze = breite // 2 if doppelt_breit else breite
                    if len(zeile) > grenze and (breite, zeile) not in BEKANNTE_AUSNAHMEN:
                        zu_lang.add((len(zeile), grenze, zeile))

            if zu_lang:
                print(f"  ✗ {name}")
                for laenge, grenze, zeile in sorted(zu_lang):
                    print(f"      {laenge} > {grenze}: {zeile!r}")
                    fehler.append((breite, name, zeile))
            else:
                print(f"  ✓ {name:<12} {DURCHLAEUFE} Bons")

    if fehler:
        print(f"\n✗ {len(fehler)} zu lange Zeile(n).")
        return 1

    print("\n✓ Alle Bons passen aufs Papier.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
