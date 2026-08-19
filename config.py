# ─── Drucker ──────────────────────────────────────────────────────────────
# "usb"     = Drucker hängt per USB-Kabel am Pi  (empfohlen, braucht kein WLAN)
# "serial"  = Drucker hat nur RS232, per USB-Nullmodem-Kabel angeschlossen
# "network" = Drucker hängt per WLAN/LAN im Heimnetz
PRINTER_MODE = "usb"

# Nur bei PRINTER_MODE = "usb":
# Gerätedatei des Druckers. Nach dem Einstecken prüfen mit:  ls /dev/usb/
PRINTER_DEVICE = "/dev/usb/lp0"

# Nur bei PRINTER_MODE = "serial":
# Gerätedatei des USB-Seriell-Adapters. Prüfen mit:  ls /dev/ttyUSB*
SERIAL_DEVICE   = "/dev/ttyUSB0"
# Die Baudrate MUSS zur Einstellung im Drucker passen, sonst kommt Kauderwelsch.
# Auslesen: Drucker ausschalten, FEED-Taste gedrückt halten, einschalten –
# er druckt einen Selbsttest mit seinen aktuellen Einstellungen aus.
SERIAL_BAUDRATE = 38400
# Hardware-Flusskontrolle. Epson-Bondrucker brauchen das, sonst gehen bei
# längeren Bons Zeilen verloren, weil der Druckpuffer überläuft.
SERIAL_DSRDTR   = True

# Nur bei PRINTER_MODE = "network":
PRINTER_IP   = "192.168.1.100"
PRINTER_PORT = 9100

# Zeichen pro Zeile in der Standardschrift (Font A).
#   80 mm Papier (z. B. Epson TM-T20)  → 42
#   58 mm Papier (Mini-/Akku-Drucker)  → 32
# Falls die Trennlinien nicht exakt über die Papierbreite gehen: hier korrigieren.
PRINTER_WIDTH = 42

# ─── Knöpfe ───────────────────────────────────────────────────────────────
# GPIO-Pinnummern (BCM-Nummerierung) der sechs Arcade-Knöpfe.
# 23/24/25 sind wie 17/27/22 reine GPIO-Pins ohne Sonderfunktion, sie kommen
# also keinem anderen Anschluss in die Quere.
GPIO_SUPERMARKT    = 17   # rot
GPIO_EISCAFE       = 27   # blau
GPIO_RESTAURANT    = 22   # grün
GPIO_BUS           = 23   # gelb
GPIO_KINO          = 24   # schwarz
GPIO_RESERVIERUNG  = 25   # weiß

# Mindestpause zwischen zwei Drucken (Sekunden), damit kein Endlosrollen entsteht
DEBOUNCE_SECONDS = 3

# Beim Start einen kleinen "Bereit"-Bon drucken.
# Praktisch als Ersatz für eine Bereitschafts-LED: Papier kommt raus = Pi ist
# hochgefahren und die Knöpfe reagieren.
PRINT_READY_RECEIPT = True

# ─── Sprache ──────────────────────────────────────────────────────────────
# "de" = deutsche Bons, "en" = englische Bons
LANGUAGE = "en"

# ─── Namen ────────────────────────────────────────────────────────────────
# Erscheinen als Kassierer/in und Bedienung auf den Bons.
#
# Eigene Namen – etwa die der eigenen Kinder – gehören NICHT hierher!
# Diese Datei liegt im öffentlichen Repository. Lege stattdessen eine
# config_local.py an (Vorlage: config_local.py.example). Die ist per
# .gitignore ausgeschlossen und bleibt auf deinem Gerät.
STAFF_NAMES = [
    "Anna", "Tom", "Lena", "Felix", "Clara",
    "Ben", "Marie", "Paul", "Mia", "Jonas",
]

# Nachname für "Familie Müller" auf größeren Reservierungen (siehe
# GUEST_FIRST_NAMES unten). Gleiche Regel wie oben: echte Namen gehören in
# config_local.py, nicht hierher.
GUEST_NAMES = ["Berger", "Hoffmann", "Krüger", "Baumann", "Winter"]

# Vornamen für Tischreservierungen. Passt die gewürfelte Personenzahl genau
# zur Anzahl dieser Namen (oder ist kleiner), listet der Bon sie namentlich
# auf – "Für: Mia & Ben" statt nur "Für: Familie Hoffmann". Bei größeren
# Runden (Geburtstag, Familienfeier) reicht die Liste nicht mehr, dann greift
# automatisch der Nachname-Fallback oben. Trag hier die eigenen Kinder ein,
# dann drucken kleine Reservierungen ihre echten Namen.
GUEST_FIRST_NAMES = ["Mia", "Ben", "Lea"]


# ─── Lokale Anpassungen ───────────────────────────────────────────────────
# Muss ganz am Ende stehen, damit config_local.py alles hierüber überschreiben
# kann. Fehlt die Datei, bleibt es bei den Vorgaben oben.
try:
    from config_local import *          # noqa: F401,F403
except ImportError:
    pass
