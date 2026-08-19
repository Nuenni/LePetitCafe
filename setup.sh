#!/bin/bash
# One-time setup on the Raspberry Pi
set -e

echo "=== LePetitCafe Setup ==="

# Update package lists
sudo apt-get update -q

# Python dependencies.
# Pillow, pyserial, and pyusb deliberately come from the package repos
# instead of pip: on the old Pi Zero (ARMv6), pip often has no prebuilt
# packages for these, so it compiles them itself for several minutes. As
# apt packages they're available instantly.
sudo apt-get install -y \
    python3-pip \
    python3-rpi.gpio \
    python3-pil \
    python3-serial \
    python3-usb

# Python libraries (finds the apt packages above already installed)
pip3 install --break-system-packages -r requirements.txt

# Device permissions: /dev/usb/lp0 belongs to root:lp, /dev/ttyUSB0 to root:dialout
sudo usermod -a -G lp,dialout "$USER"

# Install the systemd service
sudo cp lepetitcafe.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable lepetitcafe.service

echo ""
echo "✓ Done!"
echo ""

# Look for a connected printer and report it
if ls /dev/usb/lp* >/dev/null 2>&1; then
    echo "USB printer found: $(ls /dev/usb/lp*)"
    echo "→ PRINTER_MODE = \"usb\", PRINTER_DEVICE = the path above."
elif ls /dev/ttyUSB* >/dev/null 2>&1; then
    echo "USB-to-serial adapter found: $(ls /dev/ttyUSB*)"
    echo "→ PRINTER_MODE = \"serial\", SERIAL_DEVICE = the path above."
    echo "  Read the baud rate: printer off, hold FEED, switch on."
else
    echo "⚠ No printer found (/dev/usb/lp* and /dev/ttyUSB*)."
    echo "  Switch on the printer, check the cable, then:  ls /dev/usb/ /dev/ttyUSB*"
fi

echo ""
echo "Still check in config.py:"
echo "  - PRINTER_MODE   = \"usb\", \"serial\", or \"network\""
echo "  - PRINTER_WIDTH  = 42 (80mm paper) or 32 (58mm paper)"
echo "  - GPIO_*         = GPIO pins of the six buttons"
echo ""
echo "Then start with:"
echo "  sudo systemctl start lepetitcafe"
echo ""
echo "Check status:"
echo "  sudo systemctl status lepetitcafe"
echo "  journalctl -u lepetitcafe -f"
