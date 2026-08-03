"""
Layout-Helfer für alle Bon-Generatoren.

Damit dieselben Generatoren auf 58-mm- und 80-mm-Druckern gut aussehen, wird
die Zeilenbreite nicht mehr fest verdrahtet, sondern aus config.PRINTER_WIDTH
gelesen.

Wichtig: In doppelt breiter Schrift (double_width=True) passen nur halb so
viele Zeichen in eine Zeile. Dafür gibt es den Schalter `big=True`.
"""

import textwrap

import config

# Mindestabstand zwischen Text und Preis. Zwei Leerzeichen, damit der
# HTML-Simulator Preiszeilen zuverlässig als solche erkennt.
_MIN_GAP = 2


def width(big: bool = False) -> int:
    """Verfügbare Zeichen pro Zeile."""
    return config.PRINTER_WIDTH // 2 if big else config.PRINTER_WIDTH


def divider(char: str = "─") -> str:
    """Trennlinie über die volle Papierbreite."""
    return char * width() + "\n"


def money(betrag: float) -> str:
    return f"{betrag:.2f}€"


def row(label: str, value: str, big: bool = False, indent: int = 0) -> str:
    """Zeile mit Text links und Wert rechtsbündig am Papierrand."""
    lueckenbreite = width(big) - indent - len(label) - len(value)
    return (
        " " * indent
        + label
        + " " * max(lueckenbreite, _MIN_GAP)
        + value
        + "\n"
    )


def wrapped(text: str, indent: int = 0) -> str:
    """Fließtext auf die Papierbreite umbrechen statt ihn abzuschneiden."""
    zeilen = textwrap.wrap(text, width=width() - indent) or [""]
    return "".join(" " * indent + zeile + "\n" for zeile in zeilen)


def item(name: str, betrag: float, indent: int = 0) -> str:
    """Artikelzeile. Zu lange Namen werden auf die Papierbreite gekürzt."""
    wert = money(betrag)
    platz_fuer_namen = width() - indent - len(wert) - _MIN_GAP
    return row(name[:platz_fuer_namen], wert, indent=indent)
