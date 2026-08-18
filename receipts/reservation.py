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

OCCASIONS = [
    None, None, None,          # usually no special occasion
    "Birthday",
    "Family celebration",
    "First day at school",
    "Just because",
]

QR_MESSAGES = [
    "VOUCHER: You choose your seat at the table.",
    "VOUCHER: You order for everyone today.",
    "VOUCHER: Extra pudding, because you booked ahead.",
    "Why is the table never late? It is always laid on time.",
    "What does the chair say to the table? Nothing, furniture cannot talk.",
    "What do you call a booked table? Taken and happy.",
]


def erstelle_bon(printer):
    now = datetime.now()
    number = random.randint(100, 999)
    table = random.randint(1, 24)
    people = random.randint(2, 6)
    seat = random.randint(1, people)

    # Reservation falls between today and a week from now
    when = now + timedelta(days=random.randint(0, 7))
    time_slot = random.choice(["12:00", "12:30", "17:30", "18:00",
                               "18:30", "19:00", "19:30"])
    occasion = random.choice(OCCASIONS)

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
