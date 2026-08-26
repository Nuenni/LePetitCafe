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


# Odds a scanned item comes with more than 1 piece, and odds it's "on sale" -
# just for variety on the receipt, not tied to anything real.
_MENGEN = [1, 1, 1, 1, 1, 1, 1, 2, 2, 3]
_ANGEBOT_CHANCE = 0.15
_ANGEBOT_RABATT = 0.3

# Each scanned item gets one of Germany's two VAT rates at random - mostly
# 7% (food, like most of what's in these catalogs), sometimes 19% - purely
# for receipt flavor, not derived from what the item actually is.
_MWST_SAETZE = [7, 7, 7, 19]


def artikel(drucker, katalog: list[tuple[str, float]]) -> tuple[str, float, int]:
    """
    Prints one random item line, bold and oversized - each scan should feed
    a visibly bigger chunk of paper, not one thin line a kid can barely see
    move. Sometimes more than one piece, sometimes "on sale" - just for
    variety, not tied to what was actually scanned. Returns (label, total
    price, VAT rate) for the running total/breakdown.
    """
    name, preis = random.choice(katalog)
    menge = random.choice(_MENGEN)
    im_angebot = random.random() < _ANGEBOT_CHANCE
    mwst_satz = random.choice(_MWST_SAETZE)

    einzelpreis = round(preis * (1 - _ANGEBOT_RABATT), 2) if im_angebot else preis
    gesamt = round(einzelpreis * menge, 2)
    label = f"{menge}x {name}" if menge > 1 else name

    drucker.set(bold=True, double_height=True, double_width=False)
    drucker.text(layout.item(label, gesamt))
    drucker.set(normal_textsize=True, bold=False, double_height=False)

    if im_angebot:
        alt_gesamt = round(preis * menge, 2)
        hinweis = (f"* ANGEBOT, statt {layout.money(alt_gesamt)} *" if config.LANGUAGE == "de"
                   else f"* ON SALE, was {layout.money(alt_gesamt)} *")
        drucker.set(bold=True, double_height=True, double_width=False)
        drucker.text(layout.wrapped(hinweis, indent=1))
        drucker.set(normal_textsize=True, bold=False, double_height=False)

    return label, gesamt, mwst_satz


def abschluss(drucker, positionen: list[tuple[str, float, int]], bon_nr: int) -> None:
    """Prints the VAT breakdown, total, and cuts - same closing style as the regular receipts."""
    summe = sum(preis for _, preis, _ in positionen)

    # Each item's price is gross (VAT already included) - back out the VAT
    # portion per rate for the breakdown, same as the regular receipts do.
    mwst_je_satz: dict[int, float] = {}
    for _, preis, satz in positionen:
        mwst_je_satz[satz] = mwst_je_satz.get(satz, 0.0) + preis - preis / (1 + satz / 100)

    drucker.text(layout.divider("═"))
    for satz in sorted(mwst_je_satz):
        label = f"darin MwSt. {satz}%" if config.LANGUAGE == "de" else f"incl. VAT {satz}%"
        drucker.text(layout.row(label, layout.money(mwst_je_satz[satz])))
    drucker.text(layout.divider())

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
