#!/usr/bin/env python3
"""
Checks every receipt generator without needing hardware connected.

    python3 test_receipts.py

Tested against both paper widths: no line may be wider than the paper, or
the printer hard-wraps it and the receipt looks broken. Since receipts are
generated randomly, each generator runs many times.
"""

import sys

import config
from receipts import ping as ping_module

MODULE = [
    "supermarkt", "eiscafe", "restaurant", "bus", "kino", "reservierung",
    "supermarket", "icecream", "bistro", "transit", "cinema", "reservation",
    "kaffeepause", "rezeptideen",
]
BREITEN = [48, 42, 32]   # 80mm (TM-T20II), 80mm (other models), 58mm paper
DURCHLAEUFE = 50

# Known, physically unavoidable exceptions: these store names are longer
# than the 16 columns available in double width on 58mm paper.
BEKANNTE_AUSNAHMEN = {
    (32, "THE LITTLE MARKET"),
    (32, "THE LITTLE BISTRO"),
}


class TextPrinter:
    """Mock printer: collects lines along with font width, prints nothing."""

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

    # QR codes and barcodes produce no text lines and are irrelevant to the
    # width check. They just need to exist.
    def qr(self, content, **_):
        pass

    def barcode(self, code, bc, **_):
        pass

    def image(self, img, **_):
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
                    # In double width, only half as many characters fit on the paper.
                    grenze = breite // 2 if doppelt_breit else breite
                    if len(zeile) > grenze and (breite, zeile) not in BEKANNTE_AUSNAHMEN:
                        zu_lang.add((len(zeile), grenze, zeile))

            if zu_lang:
                print(f"  ✗ {name}")
                for laenge, grenze, zeile in sorted(zu_lang):
                    print(f"      {laenge} > {grenze}: {zeile!r}")
                    fehler.append((breite, name, zeile))
            else:
                print(f"  ✓ {name:<12} {DURCHLAEUFE} receipts")

        # ping.erstelle_bon() takes extra arguments, so it doesn't fit the
        # MODULE loop above - checked separately with representative input.
        zu_lang = set()
        for nachricht in (
            "Kurz",
            "Ein etwas laengerer Test-Text fuer den Ping-Bon, der ueber "
            "mehrere Zeilen umbrechen sollte, damit wir den Zeilenumbruch "
            "im Rahmen pruefen koennen.",
        ):
            drucker = TextPrinter()
            ping_module.erstelle_bon(drucker, nachricht, von="Testperson")
            for zeile, doppelt_breit in drucker.zeilen:
                grenze = breite // 2 if doppelt_breit else breite
                if len(zeile) > grenze:
                    zu_lang.add((len(zeile), grenze, zeile))
        if zu_lang:
            print("  ✗ ping")
            for laenge, grenze, zeile in sorted(zu_lang):
                print(f"      {laenge} > {grenze}: {zeile!r}")
                fehler.append((breite, "ping", zeile))
        else:
            print(f"  ✓ {'ping':<12} 2 receipts")

    if fehler:
        print(f"\n✗ {len(fehler)} line(s) too long.")
        return 1

    print("\n✓ All receipts fit the paper.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
