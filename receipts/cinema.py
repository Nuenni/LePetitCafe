"""Cinema ticket with seat and snacks."""

import random
from datetime import datetime, timedelta

from . import layout
import config

# Made-up titles – sounds like a children's cinema without borrowing real films.
FILMS = [
    ("The Adventures of the Brave Mouse", 84),
    ("Gerbil in a Rocket",                91),
    ("The Secret of the Blue Door",       97),
    ("Penguins in the Jungle",            78),
    ("My Friend the Robot",              102),
    ("The Pirate Princess",               88),
    ("Where the Clouds Live",             75),
    ("One Elephant Too Many",             81),
    ("The Enchanted Forest",              94),
]

TICKETS = [
    ("Child Ticket",     6.50),
    ("Ticket",           9.50),
    ("Ticket concession", 7.50),
]

SNACKS = [
    ("Popcorn small",    3.50),
    ("Popcorn large",    4.50),
    ("Nachos with cheese", 5.20),
    ("Gummy Bears",      2.20),
    ("Salted Pretzel",   2.50),
    ("Lemonade",         2.80),
    ("Ice Lolly",        2.50),
    ("Slushie",          3.20),
]

QR_MESSAGES = [
    "VOUCHER: You pick tonight's film.",
    "VOUCHER: Popcorn, no arguments.",
    "VOUCHER: Ten minutes past bedtime.",
    "Why did the biscuit go to the cinema? For the crumb-edy.",
    "What does popcorn do at the cinema? It bursts with excitement!",
    "Why are films never tired? They always have a role to play.",
]


def erstelle_bon(printer):
    now = datetime.now()
    number = random.randint(1000, 9999)
    film, runtime = random.choice(FILMS)
    screen = random.randint(1, 6)
    row = random.randint(3, 14)
    count = random.randint(1, 4)
    first_seat = random.randint(1, 18)
    seats = list(range(first_seat, first_seat + count))

    start = now + timedelta(minutes=random.choice([15, 30, 45, 60]))
    end = start + timedelta(minutes=runtime)

    ticket_kind, ticket_price = random.choice(TICKETS)
    snacks = random.sample(SNACKS, k=random.randint(0, 2))

    total = ticket_price * count + sum(p for _, p in snacks)

    printer.set(align="center", bold=True, double_height=True, double_width=True)
    printer.text("CINÉMA PETIT\n")
    printer.set(align="center", bold=False, double_height=False,
                double_width=False)
    printer.text("*  Roll film!  *\n")
    printer.text(layout.divider())

    # The film title large – that's the information that matters
    printer.set(align="center", bold=True, double_height=True)
    printer.text(layout.wrapped(film.upper()))
    printer.set(align="left", bold=False, double_height=False)
    printer.text(layout.divider())

    printer.text(layout.row("Screen", str(screen)))
    printer.text(layout.row("Row", str(row)))
    if count == 1:
        printer.text(layout.row("Seat", str(seats[0])))
    else:
        printer.text(layout.row("Seats",
                                f"{seats[0]}–{seats[-1]} ({count} people)"))
    printer.text(layout.divider())
    printer.text(layout.row("Starts", start.strftime("%H:%M")))
    printer.text(layout.row("Ends (approx.)", end.strftime("%H:%M")))
    printer.text(layout.row("Running time", f"{runtime} minutes"))
    printer.text(layout.row("Rating", "U — all ages"))
    printer.text(layout.divider("═"))

    if count == 1:
        printer.text(layout.item(ticket_kind, ticket_price))
    else:
        printer.text(layout.item(f"{count}x {ticket_kind}",
                                 ticket_price * count))
    for name, price in snacks:
        printer.text(layout.item(name, price))

    printer.text(layout.divider())
    printer.set(bold=True, double_height=True)
    printer.text(layout.row("TOTAL", layout.money(total)))
    printer.set(bold=False, double_height=False)

    printer.set(align="center")
    printer.text("\n")
    printer.text(layout.wrapped("Please show at the entrance"))
    printer.text(layout.wrapped("Enjoy the film!"))
    layout.codes(printer, random.choice(QR_MESSAGES),
                 f"KINO{number:04d}", "Scan me!")
    printer.cut()
