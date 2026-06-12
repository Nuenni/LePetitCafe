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

# Systemd-Service installieren
sudo cp lepetitcafe.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable lepetitcafe.service

echo ""
echo "✓ Fertig! Bitte zuerst config.py anpassen:"
echo "  - PRINTER_IP  = IP-Adresse des WLAN-Druckers"
echo "  - GPIO_*      = GPIO-Pins der drei Knöpfe"
echo ""
echo "Danach starten mit:"
echo "  sudo systemctl start lepetitcafe"
echo ""
echo "Status prüfen:"
echo "  sudo systemctl status lepetitcafe"
echo "  journalctl -u lepetitcafe -f"
