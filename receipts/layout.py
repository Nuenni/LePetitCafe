"""
Layout-Helfer für alle Bon-Generatoren.

Damit dieselben Generatoren auf 58-mm- und 80-mm-Druckern gut aussehen, wird
die Zeilenbreite nicht mehr fest verdrahtet, sondern aus config.PRINTER_WIDTH
gelesen.

Wichtig: In doppelt breiter Schrift (double_width=True) passen nur halb so
viele Zeichen in eine Zeile. Dafür gibt es den Schalter `big=True`.
"""

import json
import pathlib
import random
import textwrap
import urllib.parse

import config

_VOUCHERS_PATH = pathlib.Path(__file__).resolve().parent.parent / "vouchers.json"
_VOUCHERS = json.loads(_VOUCHERS_PATH.read_text(encoding="utf-8"))

_VOUCHER_PAGES = {"de": "gutschein.html", "en": "voucher.html"}
_DEMO_BASE_URL = "https://nuenni.github.io/LePetitCafe"

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


def voucher_url(language: str) -> str:
    """
    Liefert einen Link auf eine zufällige Gutschein-Seite (gutschein.html/
    voucher.html), gespeist aus vouchers.json. Landet im QR-Code statt
    reinem Text, damit das Handy eine schön gestaltete Seite öffnet statt
    (wie bei "GUTSCHEIN: ..."-Text) fälschlich ein URL-Schema zu vermuten
    oder (wie bei reinem Text) eine Google-Suche vorzuschlagen.
    """
    gutschein = random.choice(_VOUCHERS)
    seite = _VOUCHER_PAGES[language]
    return f"{_DEMO_BASE_URL}/{seite}?g={gutschein['id']}"


def joke_url(language: str, witz: str) -> str:
    """
    Liefert einen Link, der denselben Witz-Text schön am Handy anzeigt statt
    ihn als reinen Text in den QR-Code zu schreiben. Der Text reist direkt
    per URL-Parameter mit, braucht also keinen Eintrag in vouchers.json.
    """
    seite = _VOUCHER_PAGES[language]
    return f"{_DEMO_BASE_URL}/{seite}?w={urllib.parse.quote(witz)}"


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

    Wichtig: kein center=True hier. python-escpos wirft bei nativer
    QR-Darstellung (native=True) dafür ein NotImplementedError – die
    Zentrierung übernimmt in diesem Modus ohnehin der Drucker selbst,
    gesteuert über das drucker.set(align="center") direkt darüber.
    """
    drucker.set(align="center", bold=False, double_height=False,
                double_width=False)
    drucker.text("\n")
    try:
        drucker.qr(qr_text, size=6, native=True)
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
