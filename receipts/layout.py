"""
Layout helpers shared by all receipt generators.

So the same generators look right on both 58mm and 80mm printers, the line
width isn't hardcoded but read from config.PRINTER_WIDTH.

Important: in double-width font (double_width=True), only half as many
characters fit on a line. That's what the `big=True` switch is for.
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

# Minimum gap between text and price. Two spaces, so the HTML simulator can
# reliably recognize price lines as such.
_MIN_GAP = 2


def width(big: bool = False) -> int:
    """Available characters per line."""
    return config.PRINTER_WIDTH // 2 if big else config.PRINTER_WIDTH


def divider(char: str = "─") -> str:
    """Divider line spanning the full paper width."""
    return char * width() + "\n"


def money(betrag: float) -> str:
    return f"{betrag:.2f}€"


def row(label: str, value: str, big: bool = False, indent: int = 0) -> str:
    """
    Line with text on the left and a value right-aligned to the paper edge.

    Values like name lists ("Mia, Ben & Lea") come from config_local.py and
    are therefore unpredictably long. If label+value no longer fit on one
    line, the label gets its own line and the value wraps below it, instead
    of overflowing the paper width.
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
    """Wrap running text to the paper width instead of cutting it off."""
    zeilen = textwrap.wrap(text, width=width() - indent) or [""]
    return "".join(" " * indent + zeile + "\n" for zeile in zeilen)


def voucher_url(language: str) -> str:
    """
    Returns a link to a random voucher page (gutschein.html/voucher.html),
    fed from vouchers.json. Goes into the QR code instead of plain text, so
    the phone opens a nicely styled page instead of (like with "VOUCHER: ..."
    text) mistaking it for a URL scheme, or (like with plain text) suggesting
    a Google search.
    """
    gutschein = random.choice(_VOUCHERS)
    seite = _VOUCHER_PAGES[language]
    return f"{_DEMO_BASE_URL}/{seite}?g={gutschein['id']}"


def joke_url(language: str, witz: str) -> str:
    """
    Returns a link that displays the same joke text nicely on a phone,
    instead of writing it into the QR code as plain text. The text travels
    directly via the URL parameter, so it needs no entry in vouchers.json.
    """
    seite = _VOUCHER_PAGES[language]
    return f"{_DEMO_BASE_URL}/{seite}?w={urllib.parse.quote(witz)}"


def codes(drucker, qr_text: str, bon_nummer: str, hinweis: str) -> None:
    """
    Closes out the receipt with a QR code and barcode.

    qr_text is usually a link from voucher_url()/joke_url() that opens a
    styled page, but can also be plain text - scanning it then shows the
    message right away, even with no internet connection.

    Keep any plain-text content ASCII: the printer generates the QR code
    itself (native=True) and passes the bytes through as given. Plain ASCII
    reads identically on every scanner, while accented characters depend on
    the device.

    Not every ESC/POS printer supports QR codes. If it can't, the receipt
    should still print completely - hence the fallback block.

    Important: no center=True here. python-escpos raises a NotImplementedError
    for that in native QR mode (native=True) - centering in this mode is
    handled by the printer itself anyway, driven by the
    drucker.set(align="center") right above.
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
        # Printer without code support: at least keep the number readable.
        drucker.text(bon_nummer + "\n")


def item(name: str, betrag: float, indent: int = 0) -> str:
    """Item line. Names that are too long get truncated to the paper width."""
    wert = money(betrag)
    platz_fuer_namen = width() - indent - len(wert) - _MIN_GAP
    return row(name[:platz_fuer_namen], wert, indent=indent)
