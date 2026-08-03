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

MENU = {
    "Single Scoop":          1.20,
    "Small Ice Cream Cup":   3.50,
    "Large Ice Cream Cup":   5.50,
    "Waffle Cone (2 scoops)":2.40,
    "Waffle Cone (3 scoops)":3.40,
    "Hot Chocolate":         3.80,
    "Strawberry Milkshake":  4.20,
    "Vanilla Milkshake":     4.20,
    "Spaghetti Ice Cream":   5.90,
    "Hot Waffle w. Ice":     4.50,
    "Affogato":              3.90,
    "Kids Ice Cream Cup":    3.20,
    "Lemonade":              2.50,
    "Still Water":           1.80,
    "Hot Cocoa":             2.80,
}

STAFF = ["Anna", "Tom", "Lena", "Felix", "Clara", "Ben"]

def erstelle_bon(printer):
    now     = datetime.now()
    rec_no  = random.randint(100, 999)
    table   = random.randint(1, 8)
    server  = random.choice(STAFF)
    count   = random.randint(2, 6)

    selection = random.sample(list(MENU.items()), k=min(count, len(MENU)))
    qtys      = [random.randint(1, 2) for _ in selection]
    positions = [(name, price, qty) for (name, price), qty in zip(selection, qtys)]

    subtotal  = sum(p * q for _, p, q in positions)
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

    for name, price, qty in positions:
        total_pos = price * qty
        printer.text(layout.wrapped(f"{qty}x {name}"))
        printer.text(f"   {qty} x {price:.2f}€ = {total_pos:.2f}€\n")
        if "scoop" in name.lower() or "waffle" in name.lower() or "cup" in name.lower():
            scoops = random.sample(FLAVOURS, k=min(3, qty * 2))
            printer.text(layout.wrapped(f"({', '.join(scoops)})", indent=3))

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
