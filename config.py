# Anpassen: IP-Adresse des WLAN-Druckers und GPIO-Pins der Knöpfe
PRINTER_IP   = "192.168.1.100"   # IP-Adresse des Thermodruckers im Heimnetz
PRINTER_PORT = 9100               # Standard ESC/POS-Netzwerkport

# GPIO-Pinnummern (BCM-Nummerierung) der drei Arcade-Knöpfe
GPIO_SUPERMARKT  = 17
GPIO_EISCAFE     = 27
GPIO_RESTAURANT  = 22

# Mindestpause zwischen zwei Drucken (Sekunden), damit kein Endlosrollen entsteht
DEBOUNCE_SECONDS = 3
