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
    """
    Zeile mit Text links und Wert rechtsbündig am Papierrand.

    Werte wie Namenslisten ("Mia, Ben & Lea") kommen aus config_local.py
    und sind damit nicht vorhersehbar lang. Passt label+value nicht mehr in
    eine Zeile, geht das Label auf eine eigene Zeile und der Wert wird
    darunter umgebrochen, statt die Papierbreite zu überschreiten.
    """
    lueckenbreite = width(big) - indent - len(label) - len(value)
    if lueckenbreite < _MIN_GAP:
        return (" " * indent + label + "\n"
               + wrapped(value, indent=indent + 2))
    return (
        " " * indent
        + label
        + " " * lueckenbreite
        + value
        + "\n"
    )


def wrapped(text: str, indent: int = 0) -> str:
    """Fließtext auf die Papierbreite umbrechen statt ihn abzuschneiden."""
    zeilen = textwrap.wrap(text, width=width() - indent) or [""]
    return "".join(" " * indent + zeile + "\n" for zeile in zeilen)


def codes(drucker, qr_text: str, bon_nummer: str, hinweis: str) -> None:
    """
    Schließt den Bon mit QR-Code und Barcode ab.

    Der QR-Code enthält den Text direkt – kein Link, kein Server. Wer ihn mit
    dem Handy scannt, sieht die Nachricht sofort, auch ohne Internet.

    Der Text ist bewusst frei von Umlauten: Der Drucker erzeugt den QR-Code
    selbst (native=True) und übernimmt die Bytes so, wie wir sie schicken.
    Reines ASCII liest jeder Scanner gleich, bei Umlauten hängt das Ergebnis
    vom Gerät ab.

    Nicht jeder ESC/POS-Drucker beherrscht QR-Codes. Kann er es nicht, soll
    der Bon trotzdem komplett rauskommen – deshalb der Auffangblock.
    """
    drucker.set(align="center", bold=False, double_height=False,
                double_width=False)
    drucker.text("\n")
    try:
        drucker.qr(qr_text, size=6, native=True, center=True)
        drucker.text(hinweis + "\n\n")
        drucker.barcode(bon_nummer, "CODE39", height=48, width=2,
                        pos="BELOW", align_ct=True)
    except Exception:
        # Drucker ohne Code-Unterstuetzung: wenigstens die Nummer lesbar.
        drucker.text(bon_nummer + "\n")


def item(name: str, betrag: float, indent: int = 0) -> str:
    """Artikelzeile. Zu lange Namen werden auf die Papierbreite gekürzt."""
    wert = money(betrag)
    platz_fuer_namen = width() - indent - len(wert) - _MIN_GAP
    return row(name[:platz_fuer_namen], wert, indent=indent)
