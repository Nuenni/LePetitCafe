"""
Scanner-driven checkout: a barcode scan doesn't look anything up (no lookup
table, no internet) - it just prints one more random item from the chosen
world's regular catalog onto a receipt that's already in progress. The fun
is the physical action - scan, paper moves - not matching the real product.

Deliberately generic (name/slogan/catalog passed in, not imported here) so
it works with either language's receipt modules - main.py already resolves
those per config.LANGUAGE for the six buttons and hands the matching one in.

Printing happens in three separate steps instead of all at once, since a kid
should see the receipt grow with each scan:
  kopf()      - printed once, when the first scan starts a session
  artikel()   - printed once per scan
  abschluss() - printed once, when the session ends (timeout or any button)
"""

import random
from datetime import datetime

import config
from . import layout


def kopf(drucker, name: str, slogan: str) -> int:
    """Prints the receipt header. Returns the receipt number for later reference."""
    bon_nr = random.randint(1000, 9999)

    drucker.set(align="center", bold=True, double_height=True, double_width=True)
    drucker.text(f"{name}\n")
    drucker.set(normal_textsize=True, align="center", bold=False, double_height=False, double_width=False)
    drucker.text(f"{slogan}\n")
    drucker.text(layout.divider())

    drucker.set(align="left")
    drucker.text(f"{'Bon-Nr.' if config.LANGUAGE == 'de' else 'Receipt #'}: {bon_nr}\n")
    drucker.text(f"{datetime.now().strftime('%d.%m.%Y  %H:%M')}\n")
    drucker.text(layout.divider())
    return bon_nr


def artikel(drucker, katalog: list[tuple[str, float]]) -> tuple[str, float]:
    """
    Prints one random item line, bold and oversized - each scan should feed
    a visibly bigger chunk of paper, not one thin line a kid can barely see
    move. Returns (name, price) for the running total.
    """
    name, preis = random.choice(katalog)
    drucker.set(bold=True, double_height=True, double_width=False)
    drucker.text(layout.item(name, preis))
    drucker.set(normal_textsize=True, bold=False, double_height=False)
    return name, preis


def abschluss(drucker, positionen: list[tuple[str, float]], bon_nr: int) -> None:
    """Prints the total and cuts - same closing style as the regular receipts."""
    summe = sum(preis for _, preis in positionen)

    drucker.text(layout.divider("═"))
    drucker.set(bold=True, double_height=True)
    drucker.text(layout.row("SUMME" if config.LANGUAGE == "de" else "TOTAL", layout.money(summe)))
    drucker.set(normal_textsize=True, bold=False, double_height=False)
    drucker.text(layout.divider())

    drucker.set(align="center")
    drucker.text("Vielen Dank für Ihren Einkauf!\n" if config.LANGUAGE == "de"
                 else "Thanks for stopping by!\n")
    drucker.text("* * *\n")
    layout.codes(drucker, layout.voucher_url(config.LANGUAGE), f"LPC{bon_nr:05d}",
                 "Scann mich!" if config.LANGUAGE == "de" else "Scan me!")
    drucker.cut()
