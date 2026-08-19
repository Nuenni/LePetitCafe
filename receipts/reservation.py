"""Table reservation for the bistro – the start of a restaurant visit."""

import random
from datetime import datetime, timedelta

from . import layout
import config

STORE_NAME = "THE LITTLE BISTRO"

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

WISHES = [
    "By the window",
    "Quiet corner",
    "Near the play area",
    "Outside on the terrace",
    "With a high chair",
    "Away from the walkway",
    "Facing the kitchen",
]

# Small groups (fit inside GUEST_FIRST_NAMES) usually have no occasion –
# that's just an ordinary meal out. Bigger groups almost always do, otherwise
# it's odd why six people suddenly showed up.
OCCASIONS_SMALL = [None, None, None, None, "Just because"]
OCCASIONS_LARGE = ["Birthday", "Birthday", "Family celebration",
                   "First day at school", None]

QR_MESSAGES = [
    "VOUCHER: You choose your seat at the table.",
    "VOUCHER: You order for everyone today.",
    "VOUCHER: Extra pudding, because you booked ahead.",
    "Why is the table never late? It is always laid on time.",
    "What does the chair say to the table? Nothing, furniture cannot talk.",
    "What do you call a booked table? Taken and happy.",
]


def _list_names(names: list[str]) -> str:
    """['Mia', 'Ben', 'Lea'] -> 'Mia, Ben & Lea'"""
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + f" & {names[-1]}"


def erstelle_bon(printer):
    now = datetime.now()
    number = random.randint(100, 999)
    table = random.randint(1, 24)

    # Weighted towards small: most reservations are the family itself, a big
    # group of friends is the exception, not the rule.
    people = random.choices([2, 3, 4, 5, 6], weights=[3, 3, 2, 1, 1], k=1)[0]
    seat = random.randint(1, people)

    # If the head count matches the configured first names, name the guests
    # instead of just counting them – see config.GUEST_FIRST_NAMES.
    names = config.GUEST_FIRST_NAMES
    if people <= len(names):
        guests = random.sample(names, k=people)
        booked_for = _list_names(guests)
        occasion = random.choice(OCCASIONS_SMALL)
    else:
        booked_for = f"The {random.choice(config.GUEST_NAMES)}s"
        occasion = random.choice(OCCASIONS_LARGE)

    # Reservation falls between today and a week from now
    when = now + timedelta(days=random.randint(0, 7))
    time_slot = random.choice(["12:00", "12:30", "17:30", "18:00",
                               "18:30", "19:00", "19:30"])

    printer.set(align="center", bold=True, double_height=True, double_width=True)
    printer.text(f"{STORE_NAME}\n")
    printer.set(align="center", bold=False, double_height=False,
                double_width=False)
    printer.text("*  7 Market Square  *\n")
    printer.text(layout.divider())

    printer.set(align="center", bold=True, double_height=True)
    printer.text("TABLE RESERVED\n")
    printer.set(align="left", bold=False, double_height=False)
    printer.text(layout.divider())

    # The three details that matter – large enough to show at the door
    printer.set(bold=True, double_height=True)
    printer.text(layout.row("TABLE", str(table)))
    printer.text(layout.row("SEAT", str(seat)))
    printer.set(bold=False, double_height=False)
    printer.text(layout.row("People", str(people)))
    printer.text(layout.divider())

    printer.text(layout.row("Booked for",
                            f"The {random.choice(config.GUEST_NAMES)}s"))
    printer.text(layout.row("Day", f"{WEEKDAYS[when.weekday()]}, "
                                   f"{when.strftime('%d/%m/%Y')}"))
    printer.text(layout.row("Time", time_slot))
    if occasion:
        printer.text(layout.row("Occasion", occasion))
    printer.text(layout.divider())

    printer.text(layout.row("Request", random.choice(WISHES)))
    printer.text(layout.row("Taken by", random.choice(config.STAFF_NAMES)))
    printer.text(layout.row("Booking No.", f"{number}"))
    printer.text(layout.divider())

    printer.set(align="center")
    printer.text(layout.wrapped("We look forward to seeing you!"))
    printer.text(layout.wrapped("Please arrive 10 minutes early."))
    layout.codes(printer, random.choice(QR_MESSAGES),
                 f"RES{number:05d}", "Scan me!")
    printer.cut()
