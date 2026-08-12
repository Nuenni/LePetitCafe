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
# GPIO-Pinnummern (BCM-Nummerierung) der drei Arcade-Knöpfe
GPIO_SUPERMARKT  = 17
GPIO_EISCAFE     = 27
GPIO_RESTAURANT  = 22

# Mindestpause zwischen zwei Drucken (Sekunden), damit kein Endlosrollen entsteht
DEBOUNCE_SECONDS = 3

# Beim Start einen kleinen "Bereit"-Bon drucken.
# Praktisch als Ersatz für eine Bereitschafts-LED: Papier kommt raus = Pi ist
# hochgefahren und die Knöpfe reagieren.
PRINT_READY_RECEIPT = True
