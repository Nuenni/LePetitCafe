# ─── Drucker ──────────────────────────────────────────────────────────────
# "usb"     = Drucker hängt per USB-Kabel am Pi  (empfohlen, braucht kein WLAN)
# "network" = Drucker hängt per WLAN/LAN im Heimnetz
PRINTER_MODE = "usb"

# Nur bei PRINTER_MODE = "usb":
# Gerätedatei des Druckers. Nach dem Einstecken prüfen mit:  ls /dev/usb/
PRINTER_DEVICE = "/dev/usb/lp0"

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
