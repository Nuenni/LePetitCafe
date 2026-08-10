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

# Geräterechte: /dev/usb/lp0 gehört root:lp, /dev/ttyUSB0 gehört root:dialout
sudo usermod -a -G lp,dialout "$USER"

# Systemd-Service installieren
sudo cp lepetitcafe.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable lepetitcafe.service

echo ""
echo "✓ Fertig!"
echo ""

# Angeschlossenen Drucker suchen und melden
if ls /dev/usb/lp* >/dev/null 2>&1; then
    echo "Gefundener USB-Drucker: $(ls /dev/usb/lp*)"
    echo "→ PRINTER_MODE = \"usb\", PRINTER_DEVICE = obiger Pfad."
elif ls /dev/ttyUSB* >/dev/null 2>&1; then
    echo "Gefundener USB-Seriell-Adapter: $(ls /dev/ttyUSB*)"
    echo "→ PRINTER_MODE = \"serial\", SERIAL_DEVICE = obiger Pfad."
    echo "  Baudrate auslesen: Drucker aus, FEED gedrückt halten, einschalten."
else
    echo "⚠ Kein Drucker gefunden (/dev/usb/lp* und /dev/ttyUSB*)."
    echo "  Drucker einschalten, Kabel prüfen, dann:  ls /dev/usb/ /dev/ttyUSB*"
fi

echo ""
echo "Noch in config.py prüfen:"
echo "  - PRINTER_MODE   = \"usb\", \"serial\" oder \"network\""
echo "  - PRINTER_WIDTH  = 42 (80mm-Papier) oder 32 (58mm-Papier)"
echo "  - GPIO_*         = GPIO-Pins der drei Knöpfe"
echo ""
echo "Danach starten mit:"
echo "  sudo systemctl start lepetitcafe"
echo ""
echo "Status prüfen:"
echo "  sudo systemctl status lepetitcafe"
echo "  journalctl -u lepetitcafe -f"
