import random, math
from datetime import datetime

from . import layout

STORE_NAME = "THE LITTLE BISTRO"
SLOGAN     = "Bon appétit!"

STARTERS = [
    ("Tomato Soup",         4.90),
    ("Bruschetta",          5.50),
    ("Mixed Salad",         5.90),
    ("Prawn Cocktail",      7.90),
    ("Cheese Soup",         4.50),
    ("Avocado Toast",       6.50),
]
MAINS = [
    ("Spaghetti Bolognese", 9.90),
    ("Margherita Pizza",    8.90),
    ("Salami Pizza",        9.50),
    ("Schnitzel & Fries",  12.90),
    ("Salmon Fillet & Rice",14.90),
    ("Veggie Curry",        9.90),
    ("Classic Burger",     11.50),
    ("Tortellini Panna",   10.90),
    ("Chicken Nuggets",     8.50),
    ("Kids Pasta",          6.90),
]
DESSERTS = [
    ("Chocolate Mousse",    4.50),
    ("Tiramisu",            4.90),
    ("Strawberry Panna Cotta",4.50),
    ("Waffle w. Ice Cream", 5.50),
    ("Crème brûlée",        5.90),
    ("Fruit Salad",         3.90),
]
DRINKS = [
    ("Apple Juice",         2.80),
    ("Orange Juice",        2.80),
    ("Lemonade",            2.50),
    ("Still Water 0.3L",    1.90),
    ("Still Water 0.5L",    2.50),
    ("Hot Cocoa",           3.20),
    ("Kids Mocktail",       3.50),
    ("Milk",                1.80),
]

STAFF = ["Marie", "Luca", "Hannah", "Noah", "Emma", "Paul", "Lea", "Tim"]

def erstelle_bon(printer):
    now     = datetime.now()
    rec_no  = random.randint(1, 99)
    table   = random.randint(1, 12)
    guests  = random.randint(2, 5)
    server  = random.choice(STAFF)

    order = []
    if random.random() > 0.3:
        for _ in range(random.randint(1, min(guests, 3))):
            order.append(random.choice(STARTERS))
    for _ in range(random.randint(guests - 1, guests)):
        order.append(random.choice(MAINS))
    if random.random() > 0.4:
        for _ in range(random.randint(1, min(guests, 3))):
            order.append(random.choice(DESSERTS))
    for _ in range(random.randint(guests, guests + 1)):
        order.append(random.choice(DRINKS))

    total = sum(p for _, p in order)
    tax   = total * 0.07

    printer.set(align="center", bold=True, double_height=True, double_width=True)
    printer.text(f"{STORE_NAME}\n")
    printer.set(align="center", bold=False, double_height=False, double_width=False)
    printer.text(f"*  {SLOGAN}  *\n")
    printer.text(layout.wrapped("7 Market Square · 12345 Pleasantville"))
    printer.text("www.thelittlebistro.com\n")
    printer.text(layout.divider())

    printer.set(align="left")
    printer.text(f"Table:   {table:<3}  Receipt No.: {rec_no:02d}\n")
    printer.text(f"Guests:  {guests}\n")
    printer.text(f"Server:  {server}\n")
    printer.text(f"Date:    {now.strftime('%d/%m/%Y  %H:%M')}\n")
    printer.text(layout.divider())

    _section(printer, order, STARTERS,  "STARTERS")
    _section(printer, order, MAINS,     "MAIN COURSES")
    _section(printer, order, DESSERTS,  "DESSERTS")
    _section(printer, order, DRINKS,    "DRINKS")

    printer.text(layout.divider("═"))
    printer.set(bold=True)
    printer.text(layout.row("TOTAL", layout.money(total)))
    printer.set(bold=False)
    printer.text(layout.row("incl. VAT 7%", layout.money(tax)))
    printer.text(layout.divider())

    paid   = math.ceil(total * 2) / 2
    change = paid - total
    printer.text(layout.row("Cash given", layout.money(paid)))
    printer.set(bold=True, double_height=True)
    printer.text(layout.row("CHANGE", layout.money(change)))
    printer.set(bold=False, double_height=False)
    printer.text(layout.divider())
    printer.set(align="center")
    printer.text("Payment: Cash\n\n")
    printer.text(layout.wrapped("*  Thank you for dining with us!  *"))
    printer.text("We hope to see you again soon!\n")
    printer.text("\n")
    printer.text(f"{STORE_NAME}\n")
    printer.cut()

def _section(printer, order, category, title):
    names = {n for n, _ in category}
    items = [(n, p) for n, p in order if n in names]
    if not items:
        return
    printer.set(bold=True)
    printer.text(f"  {title}\n")
    printer.set(bold=False)
    for name, price in items:
        printer.text(layout.item(name, price, indent=2))
