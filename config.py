# ─── Printer ──────────────────────────────────────────────────────────────
# "usb"     = printer connects to the Pi via USB cable (recommended, no WiFi needed)
# "serial"  = printer only has RS232, connected via USB null-modem cable
# "network" = printer sits on the home network over WiFi/LAN
PRINTER_MODE = "usb"

# Only for PRINTER_MODE = "usb":
# Device file for the printer. After plugging it in, check with:  ls /dev/usb/
PRINTER_DEVICE = "/dev/usb/lp0"

# Only for PRINTER_MODE = "serial":
# Device file for the USB-to-serial adapter. Check with:  ls /dev/ttyUSB*
SERIAL_DEVICE   = "/dev/ttyUSB0"
# The baud rate MUST match the printer's setting, or you get garbled output.
# To read it off: switch the printer off, hold the FEED button, switch it on -
# it prints a self-test page with its current settings.
SERIAL_BAUDRATE = 38400
# Hardware flow control. Epson receipt printers need this, otherwise longer
# receipts lose lines because the print buffer overflows.
SERIAL_DSRDTR   = True

# Only for PRINTER_MODE = "network":
PRINTER_IP   = "192.168.1.100"
PRINTER_PORT = 9100

# Characters per line in the default font (Font A). Model-dependent - don't
# guess it, look it up with:
#   python3 -c "from escpos.capabilities import get_profile as g; print(g('TM-T20II').fonts)"
#   80 mm paper, Epson TM-T20II          -> 48  (72 mm usable width)
#   58 mm paper (mini/battery printers)  -> 32
# If the divider lines don't reach exactly across the paper, or there's a
# noticeable unprinted strip on the right: adjust this here.
PRINTER_WIDTH = 48

# Printable width in dots, for images (e.g. the Ping receipt). python-escpos
# does not scale images to fit the paper - anything wider just gets cut off
# on the right. 72mm usable width at 203dpi = 72 / 25.4 * 203 ≈ 576 dots.
# 58mm paper (mini/battery printers) -> 384.
PRINTER_IMAGE_WIDTH_PX = 576

# ─── Barcode scanner (optional) ─────────────────────────────────────────────
# A USB handheld scanner shows up to Linux as a generic keyboard - most
# cheap ones report a device name ending in "HID Keyboard" regardless of
# brand. This narrows down which input device is the scanner among all
# others. Check the real name on the Pi with:  cat /proc/bus/input/devices
SCANNER_NAME_HINT = "HID Keyboard"

# How many seconds of no further scan before the in-progress scan receipt
# finishes and cuts on its own.
SCAN_TIMEOUT_SECONDS = 60

# ─── Buttons ──────────────────────────────────────────────────────────────
# GPIO pin numbers (BCM numbering) of the six arcade buttons.
# 23/24/25 are, like 17/27/22, plain GPIO pins with no special function, so
# they don't conflict with any other connector.
GPIO_SUPERMARKT    = 17   # red
GPIO_EISCAFE       = 27   # blue
GPIO_RESTAURANT    = 22   # green
GPIO_BUS           = 23   # yellow
GPIO_KINO          = 24   # black
GPIO_RESERVIERUNG  = 25   # white

# Minimum pause between two prints (seconds), to avoid endless paper rolling
DEBOUNCE_SECONDS = 3

# ─── Coffee break (secret receipt) ─────────────────────────────────────────
# A small extra receipt just for you: a coffee order "for Mama" that either
# shows up rarely and randomly between the kids' receipts, or gets triggered
# deliberately via a button combo. "Mama"/"Papa" are roles, not real names -
# unlike STAFF_NAMES, this doesn't belong in config_local.py.
COFFEE_FOR = "Mama"

# Roughly every how many-th receipt is a random coffee receipt instead of the
# chosen game. None = disables the random share entirely.
COFFEE_RANDOM_EVERY = 13

# Holding these two buttons together for ~COMBO_HOLD_SECONDS deliberately
# triggers the coffee receipt, instead of the two normal play worlds.
# Deliberately two buttons far apart from each other (red + white), so this
# doesn't happen by accident during normal button mashing.
COFFEE_COMBO = (GPIO_SUPERMARKT, GPIO_RESERVIERUNG)

# Same idea, second secret receipt: holding yellow + green together prints a
# quick dinner idea instead of Bus/Taxi or Restaurant - for evenings where
# nobody knows what to cook. Press it again for another suggestion.
RECIPE_COMBO = (GPIO_BUS, GPIO_RESTAURANT)

# Shared hold duration for both combos above.
COMBO_HOLD_SECONDS = 1.2

# Print a small "ready" receipt on startup.
# Stands in for a ready LED: paper comes out = the Pi has booted and the
# buttons are responding.
PRINT_READY_RECEIPT = True

# ─── Language ─────────────────────────────────────────────────────────────
# "de" = German receipts, "en" = English receipts
LANGUAGE = "en"

# ─── Names ────────────────────────────────────────────────────────────────
# Appear as cashier and server on the receipts.
#
# Your own names - like your kids' names - do NOT belong here!
# This file lives in the public repository. Create a config_local.py instead
# (template: config_local.py.example). It's excluded via .gitignore and
# stays on your own device.
STAFF_NAMES = [
    "Anna", "Tom", "Lena", "Felix", "Clara",
    "Ben", "Marie", "Paul", "Mia", "Jonas",
]

# Last name for "the Mueller family" on larger reservations (see
# GUEST_FIRST_NAMES below). Same rule as above: real names belong in
# config_local.py, not here.
GUEST_NAMES = ["Berger", "Hoffmann", "Krüger", "Baumann", "Winter"]

# First names for table reservations. If the randomly rolled party size
# matches (or is smaller than) the number of names here, the receipt lists
# them by name - "For: Mia & Ben" instead of just "For: the Hoffmann family".
# For bigger groups (birthdays, family gatherings) the list isn't enough
# anymore, and the last-name fallback above kicks in automatically. Put your
# own kids here, and small reservations will print their real names.
GUEST_FIRST_NAMES = ["Mia", "Ben", "Lea"]


# ─── Local overrides ──────────────────────────────────────────────────────
# Must stay at the very end, so config_local.py can override everything
# above it. If the file is missing, the defaults above apply.
try:
    from config_local import *          # noqa: F401,F403
except ImportError:
    pass
