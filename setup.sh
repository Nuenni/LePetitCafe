#!/bin/bash
# Einmalige Einrichtung auf dem Raspberry Pi
set -e

echo "=== LePetitCafe Setup ==="

# Paketlisten aktualisieren
sudo apt-get update -q

# Python-Abhängigkeiten
sudo apt-get install -y python3-pip python3-rpi.gpio

# Python-Bibliotheken
pip3 install --break-system-packages -r requirements.txt

# USB-Drucker: /dev/usb/lp0 gehört root:lp, der Benutzer muss in die lp-Gruppe
sudo usermod -a -G lp "$USER"

# Systemd-Service installieren
sudo cp lepetitcafe.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable lepetitcafe.service

echo ""
echo "✓ Fertig!"
echo ""

# Angeschlossenen USB-Drucker suchen und melden
if ls /dev/usb/lp* >/dev/null 2>&1; then
    echo "Gefundener USB-Drucker: $(ls /dev/usb/lp*)"
    echo "→ Diesen Pfad in config.py als PRINTER_DEVICE eintragen."
else
    echo "⚠ Kein USB-Drucker gefunden (/dev/usb/lp*)."
    echo "  Drucker einschalten, USB-Kabel prüfen, dann:  ls /dev/usb/"
fi

echo ""
echo "Noch in config.py prüfen:"
echo "  - PRINTER_MODE   = \"usb\" oder \"network\""
echo "  - PRINTER_WIDTH  = 42 (80mm-Papier) oder 32 (58mm-Papier)"
echo "  - GPIO_*         = GPIO-Pins der drei Knöpfe"
echo ""
echo "Danach starten mit:"
echo "  sudo systemctl start lepetitcafe"
echo ""
echo "Status prüfen:"
echo "  sudo systemctl status lepetitcafe"
echo "  journalctl -u lepetitcafe -f"
