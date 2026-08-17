import random
from datetime import datetime

from . import layout

STORE_NAME = "THE LITTLE CAFÉ"
SLOGAN     = "Ice Cream · Waffles · Dreams"

FLAVOURS = [
    "Vanilla", "Chocolate", "Strawberry", "Hazelnut",
    "Pistachio", "Lemon", "Yogurt", "Caramel",
    "Bubblegum", "Stracciatella", "Mango", "Raspberry",
    "Coconut", "Mint Choc Chip", "Tiramisu",
]

# (Name, price, scoops)
# scoops = number of freely chosen flavours listed on the receipt.
#   0 = ready-made creation or something on a stick. A Black Forest sundae or a
#       Magnum already says what it is — a random flavour list would be nonsense.
MENU = [
    # Scoops and cones
    ("Single Scoop",           1.20, 1),
    ("Waffle Cone (2 scoops)", 2.40, 2),
    ("Waffle Cone (3 scoops)", 3.40, 3),
    ("Hot Waffle w. Ice",      4.50, 2),

    # Build-your-own cups
    ("Small Ice Cream Cup",    3.50, 2),
    ("Large Ice Cream Cup",    5.50, 3),

    # Classic sundaes
    ("Spaghetti Ice Cream",    5.90, 0),
    ("Praline Crunch Sundae",  5.90, 0),
    ("After Eight Sundae",     6.20, 0),
    ("Black Forest Sundae",    6.50, 0),
    ("Banana Split",           6.20, 0),

    # For the little ones
    ("Kids Ice Cream Cup",     3.20, 1),
    ("Pinocchio Sundae",       4.50, 0),
    ("Maya the Bee Sundae",    4.50, 0),

    # Ice lollies
    ("Magnum Classic",         2.50, 0),
    ("Magnum White",           2.50, 0),
    ("Solero",                 2.20, 0),
    ("Calippo",                1.80, 0),
    ("Twister",                1.80, 0),

    # Drinks and treats
    ("Hot Chocolate",          3.80, 0),
    ("Strawberry Milkshake",   4.20, 0),
    ("Vanilla Milkshake",      4.20, 0),
    ("Affogato",               3.90, 0),
    ("Lemonade",               2.50, 0),
    ("Still Water",            1.80, 0),
    ("Hot Cocoa",              2.80, 0),
]

STAFF = ["Anna", "Tom", "Lena", "Felix", "Clara", "Ben"]

def erstelle_bon(printer):
    now     = datetime.now()
    rec_no  = random.randint(100, 999)
    table   = random.randint(1, 8)
    server  = random.choice(STAFF)
    count   = random.randint(3, 7)

    selection = random.sample(MENU, k=min(count, len(MENU)))
    positions = [
        (name, price, scoops, random.randint(1, 2))
        for name, price, scoops in selection
    ]

    subtotal  = sum(price * qty for _, price, _, qty in positions)
    tip_pct   = random.choice([0, 5, 10])
    tip       = round(subtotal * tip_pct / 100, 2)
    total     = subtotal + tip

    printer.set(align="center", bold=True, double_height=True, double_width=True)
    printer.text(f"{STORE_NAME}\n")
    printer.set(align="center", bold=False, double_height=False, double_width=False)
    printer.text(layout.wrapped("✿  " + SLOGAN + "  ✿"))
    printer.text(layout.wrapped("3 Lake Promenade · 12345 Sunnyville"))
    printer.text(layout.divider())

    printer.set(align="left")
    printer.text(f"Table:   {table:<4}  Receipt No.: {rec_no}\n")
    printer.text(f"Server:  {server}\n")
    printer.text(f"Time:    {now.strftime('%H:%M')}\n")
    printer.text(layout.divider())

    for name, price, scoops, qty in positions:
        total_pos = price * qty
        printer.text(layout.wrapped(f"{qty}x {name}"))
        printer.text(f"   {qty} x {price:.2f}€ = {total_pos:.2f}€\n")
        if scoops:
            chosen = random.sample(FLAVOURS, k=min(scoops * qty, len(FLAVOURS)))
            printer.text(layout.wrapped(f"({', '.join(chosen)})", indent=3))

    printer.text(layout.divider("═"))
    printer.set(bold=True)
    printer.text(layout.row("Subtotal", layout.money(subtotal)))
    printer.set(bold=False)
    if tip_pct > 0:
        printer.text(layout.row(f"Tip {tip_pct}%", layout.money(tip)))
    printer.set(bold=True, double_height=True)
    printer.text(layout.row("TOTAL", layout.money(total)))
    printer.set(bold=False, double_height=False)
    printer.text(layout.divider())
    printer.set(align="center")
    printer.text("Payment: Cash\n")
    printer.text(f"{now.strftime('%d/%m/%Y')}\n")
    printer.text("\n")
    printer.text("★  Thank you for your visit!  ★\n")
    printer.text("We wish you a\n")
    printer.text("wonderful day!\n")
    printer.text("✿ ✿ ✿\n")
    printer.cut()
