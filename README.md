# LePetitCafe 🧾

Kassenbon-Drucker für Kinder — drei Knöpfe, drei Spielwelten, echter Thermodruck.

Ein Knopfdruck auf **Supermarkt**, **Eiscafé** oder **Restaurant** druckt sofort
einen zufällig generierten, liebevoll gestalteten Kassenbon. Kein PC nötig,
läuft komplett auf einem Raspberry Pi Zero 2 W.

---

## Hardware-Einkaufsliste

| Teil | Empfehlung | Preis ca. |
|------|-----------|-----------|
| Thermodrucker (WLAN) | EPSON TM-T20III oder Xprinter XP-Q200 | 60–120 € |
| Einplatinen-Computer | Raspberry Pi Zero 2 W | 18 € |
| SD-Karte | 16 GB Class 10 | 8 € |
| Arcade-Knöpfe | 60 mm Großknöpfe (rot/gelb/blau) | 3× 3 € |
| Gehäuse | Holzbox oder 3D-Druck | – |
| Netzteil | 5 V / 2,5 A Micro-USB | 8 € |

### Drucker-Kompatibilität

Das Skript nutzt das **ESC/POS**-Protokoll — kompatibel mit fast allen
Thermodruckern. Wichtig: Der Drucker muss über **WLAN im selben Heimnetz**
wie der Raspberry Pi erreichbar sein (manche Drucker öffnen Port 9100).

---

## Verdrahtung (GPIO)

```
Raspberry Pi Zero 2 W (BCM-Nummerierung)

  Knopf SUPERMARKT  → GPIO 17  +  GND
  Knopf EISCAFÉ     → GPIO 27  +  GND
  Knopf RESTAURANT  → GPIO 22  +  GND
```

Interne Pull-up-Widerstände sind aktiviert. Die Knöpfe schließen
einfach den jeweiligen Pin gegen GND.

---

## Installation

1. **Raspberry Pi OS Lite** auf SD-Karte flashen (z. B. mit Raspberry Pi Imager).
   WLAN und SSH beim Flashen gleich konfigurieren.

2. Per SSH einloggen und das Repository klonen:
   ```bash
   git clone https://github.com/nuenni/lepetitcafe.git
   cd lepetitcafe
   ```

3. **`config.py` anpassen** — IP-Adresse des Druckers und GPIO-Pins eintragen.

4. Setup-Skript ausführen:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

5. Drucker einschalten, dann Service starten:
   ```bash
   sudo systemctl start lepetitcafe
   ```

6. Testen — Knopf drücken → Bon kommt raus!

---

## Projektstruktur

```
LePetitCafe/
├── main.py                 # Hauptprogramm, GPIO-Listener
├── config.py               # IP, GPIO-Pins — hier anpassen!
├── requirements.txt        # Python-Pakete
├── setup.sh                # Einrichtungsskript
├── lepetitcafe.service     # Systemd-Unit (Autostart)
└── receipts/
    ├── supermarkt.py       # Bon-Generator: Petit Marché
    ├── eiscafe.py          # Bon-Generator: Le Petit Café
    └── restaurant.py       # Bon-Generator: Le Petit Bistro
```

---

## Bon-Beispiele

### PETIT MARCHÉ (Supermarkt)
Zufällige Lebensmittel, Kassierer-Name, Bon-Nummer, Rückgeld-Berechnung.

### LE PETIT CAFÉ (Eiscafé)
Eiskugeln mit Sorten-Angabe, Tischnummer, Bedienung, optionales Trinkgeld.

### LE PETIT BISTRO (Restaurant)
Vorspeisen / Hauptgerichte / Desserts / Getränke, Tisch, Kellner, MwSt.

---

## Fehlersuche

```bash
# Live-Log anzeigen
journalctl -u lepetitcafe -f

# Service neu starten
sudo systemctl restart lepetitcafe

# Drucker manuell testen (IP anpassen)
python3 -c "
from escpos.printer import Network
p = Network('192.168.1.100')
p.text('Hallo!\n')
p.cut()
p.close()
"
```