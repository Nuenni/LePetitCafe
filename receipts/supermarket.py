import random
from datetime import datetime

from . import layout
import config

STORE_NAME = "THE LITTLE MARKET"
SLOGAN     = "Fresh. Tasty. Affordable."

ITEMS = [
    ("Whole Milk 1L",       0.99,  "1 pc."),
    ("Whole Milk 1L",       0.99,  "2 pcs."),
    ("Butter 250g",         1.59,  "1 pc."),
    ("Eggs 6-pack",         1.89,  "1 pk."),
    ("Cheese Slices",       2.29,  "1 pk."),
    ("Strawberry Yogurt",   0.65,  "2 pcs."),
    ("Strawberry Yogurt",   0.65,  "3 pcs."),
    ("Bananas",             0.99,  "1 bunch"),
    ("Elstar Apples",       1.39,  "1 kg"),
    ("Oranges",             0.89,  "3 pcs."),
    ("Carrots",             0.79,  "500 g"),
    ("Tomatoes",            1.19,  "500 g"),
    ("Cucumber",            0.59,  "1 pc."),
    ("Iceberg Lettuce",     0.89,  "1 pc."),
    ("Toast Bread",         1.29,  "1 pk."),
    ("Pretzel",             0.49,  "2 pcs."),
    ("Milk Chocolate",      1.09,  "1 bar"),
    ("Gummy Bears",         0.99,  "1 bag"),
    ("Apple Juice 1L",      1.59,  "1 btl."),
    ("Mineral Water 1L",    0.45,  "2 btls."),
    ("Spaghetti",           0.89,  "500 g"),
    ("Tomato Sauce",        1.09,  "1 jar"),
    ("Cornflakes",          2.59,  "1 pk."),
    ("Fruit Muesli",        3.39,  "1 pk."),
    ("Laundry Detergent",   4.99,  "1 pk."),
    ("Dish Soap",           0.99,  "1 btl."),
    ("Toilet Paper 4-pack", 1.99,  "1 pk."),
    ("Shampoo",             2.59,  "1 btl."),
]


# Goes into the QR code on the receipt. ASCII only, see layout.codes().
QR_MESSAGES = [
    "VOUCHER: You get to pick what's for pudding tonight!",
    "VOUCHER: Push the trolley all by yourself - one time only.",
    "VOUCHER: One extra scoop of ice cream. Ask a grown-up.",
    "Why don't bees need trolleys? They already have baskets!",
    "What do you call a sad strawberry? A blueberry.",
    "Two biscuits meet. One says: you're crumbling! - So are you!",
]

def erstelle_bon(printer):
    now    = datetime.now()
    items  = random.sample(ITEMS, k=random.randint(4, 9))
    total  = sum(i[1] for i in items)
    tax    = total * 0.19
    name   = random.choice(config.STAFF_NAMES)
    rec_no = random.randint(1000, 9999)
    till   = random.randint(1, 4)

    printer.set(align="center", bold=True, double_height=True, double_width=True)
    printer.text(f"{STORE_NAME}\n")
    printer.set(align="center", bold=False, double_height=False, double_width=False)
    printer.text(f"{SLOGAN}\n")
    printer.text("12 Main St · 12345 Pleasantville\n")
    printer.text("Tel: 01234 / 567890\n")
    printer.text(layout.divider())

    printer.set(align="left")
    printer.text(f"Date:    {now.strftime('%d/%m/%Y')}\n")
    printer.text(f"Time:    {now.strftime('%H:%M')}\n")
    printer.text(f"Till:    {till}   Receipt No.: {rec_no}\n")
    printer.text(f"Cashier: {name}\n")
    printer.text(layout.divider())

    for article, price, qty in items:
        printer.text(layout.item(article, price))
        printer.text(f"  ({qty})\n")

    printer.text(layout.divider("═"))
    printer.set(bold=True)
    printer.text(layout.row("TOTAL", layout.money(total)))
    printer.set(bold=False)
    printer.text(layout.row("incl. VAT 19%", layout.money(tax)))
    printer.text(layout.divider())

    paid   = _round_up(total)
    change = paid - total
    printer.text(layout.row("Cash given", layout.money(paid)))
    printer.set(bold=True, double_height=True)
    printer.text(layout.row("CHANGE", layout.money(change)))
    printer.set(bold=False, double_height=False)
    printer.text(layout.divider())
    printer.set(align="center")
    printer.text(f"{random.choice(_phrases())}\n")
    printer.text("Thank you for shopping with us!\n")
    printer.text("See you soon!\n")
    layout.codes(printer, random.choice(QR_MESSAGES),
                 f"LPC{rec_no:05d}", "Scan me!")
    printer.cut()

def _round_up(amount):
    import math
    return math.ceil(amount * 2) / 2

def _phrases():
    return [
        "* Bon appétit! *",
        "* Have a wonderful day! *",
        "* Stay healthy! *",
        "* We hope to see you again! *",
        "* Thanks, little shopper! *",
    ]
