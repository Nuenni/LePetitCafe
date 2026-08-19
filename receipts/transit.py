"""Bus or taxi ticket – the way between the play worlds."""

import random
from datetime import datetime, timedelta

from . import layout
import config

# The stops echo the addresses on the other receipts: Main Street is the
# supermarket, Lake Promenade the ice cream cafe, Market Square the bistro.
# That way a ride always leads somewhere you can carry on playing.
STOPS = [
    "Main Street",
    "Lake Promenade",
    "Market Square",
    "Cinema Square",
    "Central Station",
    "Zoo",
    "Swimming Pool",
    "Playground",
]

TICKETS = [
    ("Short Hop",        1.20,  30),
    ("Single Ticket",    1.80,  90),
    ("Child Ticket",     0.90,  90),
    ("Day Pass",         4.50, 600),
    ("Family Pass",      7.90, 600),
]

CAB_COLOURS = ["yellow", "cream", "silver", "black"]

JOKES = [
    "Why don't buses ever sit down? They have plenty of seats already!",
    "What is yellow and drives in circles? A taxi in a roundabout.",
    "How does a hedgehog get on the bus? Through the door, like everyone.",
]


def erstelle_bon(printer):
    if random.random() < 0.6:
        _bus(printer)
    else:
        _taxi(printer)


def _route() -> tuple[str, str]:
    start, end = random.sample(STOPS, k=2)
    return start, end


def _head(printer, name: str, slogan: str) -> None:
    printer.set(align="center", bold=True, double_height=True, double_width=True)
    printer.text(f"{name}\n")
    printer.set(align="center", bold=False, double_height=False,
                double_width=False)
    printer.text(f"*  {slogan}  *\n")
    printer.text(layout.divider())


def _foot(printer, note: str, number: str) -> None:
    printer.set(align="center")
    printer.text("\n")
    printer.text(layout.wrapped(note))
    qr_content = (layout.voucher_url("en") if random.random() < 0.5
                  else layout.joke_url("en", random.choice(JOKES)))
    layout.codes(printer, qr_content, number, "Scan me!")
    printer.cut()


def _bus(printer):
    now = datetime.now()
    number = random.randint(1000, 9999)
    line = random.choice([1, 3, 5, 7, 8, 12, 21, 42])
    start, end = _route()
    kind, price, minutes = random.choice(TICKETS)
    valid_until = now + timedelta(minutes=minutes)

    _head(printer, "LE PETIT EXPRESS", "All aboard!")

    printer.set(align="center", bold=True, double_height=True)
    printer.text(f"{kind.upper()}\n")
    printer.set(align="left", bold=False, double_height=False)
    printer.text(layout.divider())

    printer.text(layout.row("Line", str(line)))
    printer.text(layout.row("From", start))
    printer.text(layout.row("To", end))
    printer.text(layout.divider())
    printer.text(layout.row("Departure", now.strftime("%H:%M")))
    printer.text(layout.row("Valid until", valid_until.strftime("%H:%M")))
    printer.text(layout.row("Driver", random.choice(config.STAFF_NAMES)))
    printer.text(layout.divider("═"))

    printer.set(bold=True, double_height=True)
    printer.text(layout.row("TO PAY", layout.money(price)))
    printer.set(bold=False, double_height=False)

    _foot(printer, "Please show when boarding", f"BUS{number:05d}")


def _taxi(printer):
    now = datetime.now()
    number = random.randint(1000, 9999)
    cab = random.randint(1, 99)
    start, end = _route()
    km = round(random.uniform(1.2, 9.8), 1)
    minutes = max(3, int(km * random.uniform(2.0, 3.5)))

    base = 3.90
    per_km = 2.10
    distance = round(km * per_km, 2)
    total = base + distance

    _head(printer, "PETIT TAXI", "Always at your service")

    printer.set(align="left")
    printer.text(layout.row("Cab No.", f"{cab:02d}"))
    printer.text(layout.row("Driver", random.choice(config.STAFF_NAMES)))
    printer.text(layout.row("Colour", random.choice(CAB_COLOURS)))
    printer.text(layout.divider())
    printer.text(layout.row("From", start))
    printer.text(layout.row("To", end))
    printer.text(layout.row("Distance", f"{km:.1f} km"))
    printer.text(layout.row("Journey time", f"{minutes} minutes"))
    printer.text(layout.row("Arrival", now.strftime("%H:%M")))
    printer.text(layout.divider("═"))

    printer.text(layout.row("Base fare", layout.money(base)))
    printer.text(layout.row(f"{km:.1f} km at 2.10€", layout.money(distance)))
    printer.set(bold=True, double_height=True)
    printer.text(layout.row("TO PAY", layout.money(total)))
    printer.set(bold=False, double_height=False)

    _foot(printer, "Safe travels, and see you next time!", f"TAXI{number:04d}")
