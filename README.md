# Le Petit Café 🧾

**A receipt printer for kids** — three big buttons, three play worlds, real thermal prints. No PC, no screen, no app needed.

Press a button → a unique, randomly generated receipt comes rattling out of the printer. Perfect for playing supermarket, ice cream café, or restaurant.

![Receipt preview](docs/preview.png)

---

## 🌐 Live Demo

**Try it in your browser — no hardware needed:**

👉 **[nuenni.github.io/LePetitCafe](https://nuenni.github.io/LePetitCafe/)**

Available in 🇩🇪 German and 🇬🇧 English.

---

## How it works

```
Child presses button
        │
        ▼
Raspberry Pi Zero 2 W  (runs 24/7, no screen needed)
        │  WiFi
        ▼
Thermal printer
        │
        ▼
Receipt comes out 🎉
```

Every receipt is unique — random items, prices, names, table numbers, timestamps. No two receipts are ever the same.

---

## Three Play Worlds, Three Buttons

| Button | Store | Receipt includes |
|--------|-------|-----------------|
| 🔴 Red | **PETIT MARCHÉ** (Supermarket) | Groceries, cashier name, change calculation |
| 🟣 Purple | **LE PETIT CAFÉ** (Ice Cream Café) | Ice cream flavours, table number, optional tip |
| 🔵 Blue | **LE PETIT BISTRO** (Restaurant) | Starter / main / dessert / drinks, server, VAT |

Receipts are available in **German** (default) and **English** — see `receipts/` folder.

---

## Hardware

### What you need

| Part | Recommendation | Price |
|------|---------------|-------|
| [WiFi Thermal Printer](#printer) | MUNBYN ITPP047 (80mm, WiFi) | ~70 € |
| Single-board computer | Raspberry Pi Zero 2 W | ~30 € |
| microSD card | 16 GB Class 10 | ~10 € |
| Arcade buttons | BerryBase 60mm LED, 3 colours | ~12 € |
| Power supply | 5V / 2.5A Micro-USB | ~12 € |
| Enclosure | Wooden box, lunchbox or 3D print | – |

**Total: ~135 €**

---

### Printer

The code uses the **ESC/POS** protocol, supported by virtually all affordable thermal printers. The printer must be reachable via **WiFi on the same home network** as the Raspberry Pi (TCP port 9100).

**MUNBYN ITPP047** *(recommended, ~70 €)*
- 80mm paper, 230mm/s, auto-cutter
- WiFi + Ethernet + USB, ESC/POS compatible
- Well documented for Raspberry Pi projects
- Search Amazon: `MUNBYN ITPP047 thermal receipt printer`

**Xprinter XP-Q80I / XP-N160II** *(alternative, ~50–75 €)*
- 80mm, WiFi variant available, popular in the maker community

**NETUM NT-5890K** *(budget option, ~40–55 €)*
- 58mm paper (slightly narrower receipts), compact and cheap

> **Paper rolls:** Standard 80mm × 80mm thermal rolls, ~10 € for a 10-pack.

---

### Raspberry Pi Zero 2 W

| | Pi Zero 2 W *(recommended)* | Pi Zero W *(budget)* |
|--|--|--|
| Price | ~28–35 € | ~15–20 € |
| CPU | Quad-core 1GHz | Single-core 1GHz |
| RAM | 512MB | 512MB |
| WiFi | ✓ | ✓ |

**Where to buy (Germany/EU):**
- [Berrybase.de](https://www.berrybase.de) — usually best prices, ships from Germany
- Amazon.de — search: `Raspberry Pi Zero 2 W`
- Reichelt.de / Farnell

---

### Arcade Buttons

**60mm LED-illuminated arcade buttons** — big enough for small hands, sturdy and colourful.

- **BerryBase** `Large Arcade Button 60mm beleuchtet LED 12V DC` — ~4 € each, red/blue/yellow/green available, ships from Germany
- **Amazon** — search: `60mm arcade button LED` (brands: EG STARTS, uxcell, BQLZR)

> **LED note:** The LED runs on 12V DC. The button switch itself connects directly to GPIO at 3.3V — no 12V supply needed just for the button function.

---

## Wiring

```
Raspberry Pi Zero 2 W — GPIO (BCM numbering)

  Button RED    (Supermarket) → GPIO 17 + GND
  Button PURPLE (Ice Cream)   → GPIO 27 + GND
  Button BLUE   (Restaurant)  → GPIO 22 + GND
```

Internal pull-up resistors are enabled. Each button simply connects its GPIO pin to GND when pressed — no external resistors needed.

```
                3V3  [1]  [2]  5V
              GPIO2  [3]  [4]  5V
              GPIO3  [5]  [6]  GND ←── all 3 buttons share GND here
              GPIO4  [7]  [8]  GPIO14
                GND  [9] [10]  GPIO15
  RED   → GPIO17 [11] [12]  GPIO18
  PURPLE→ GPIO27 [13] [14]  GND
  BLUE  → GPIO22 [15] [16]  GPIO23
```

---

## Setup

### Step 1 — Flash the Raspberry Pi

1. Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Flash **Raspberry Pi OS Lite (64-bit)**
3. In the Imager settings (⚙️): set WiFi credentials, enable SSH, set username `pi`
4. Insert SD card, power on, wait ~30 seconds

### Step 2 — Connect via SSH

```bash
ssh pi@raspberrypi.local
```

### Step 3 — Clone & configure

```bash
git clone https://github.com/nuenni/lepetitcafe.git
cd lepetitcafe
nano config.py
```

Set your printer's IP address and GPIO pins:

```python
PRINTER_IP  = "192.168.1.xxx"  # find in your router's device list
PRINTER_PORT = 9100

GPIO_SUPERMARKT  = 17
GPIO_EISCAFE     = 27
GPIO_RESTAURANT  = 22
```

### Step 4 — Run setup

```bash
chmod +x setup.sh
./setup.sh
```

Installs dependencies and registers the systemd autostart service.

### Step 5 — Start

```bash
sudo systemctl start lepetitcafe
```

**Press a button → receipt comes out!** 🎉

Le Petit Café now starts automatically every time the Pi is powered on.

---

## Project structure

```
LePetitCafe/
├── main.py                  # GPIO listener, print dispatcher
├── config.py                # ← Set printer IP and GPIO pins here
├── requirements.txt         # python-escpos, RPi.GPIO
├── setup.sh                 # One-time setup script
├── lepetitcafe.service      # systemd unit for autostart
├── simulate_web.py          # Local web simulator (no hardware needed)
├── simulator.html           # Standalone demo — German
├── simulator_en.html        # Standalone demo — English
├── docs/
│   └── preview.png
└── receipts/
    ├── supermarkt.py        # 🇩🇪 PETIT MARCHÉ
    ├── eiscafe.py           # 🇩🇪 LE PETIT CAFÉ
    ├── restaurant.py        # 🇩🇪 LE PETIT BISTRO
    ├── supermarket.py       # 🇬🇧 THE LITTLE MARKET
    ├── icecream.py          # 🇬🇧 THE LITTLE CAFÉ
    └── bistro.py            # 🇬🇧 THE LITTLE BISTRO
```

---

## Troubleshooting

```bash
# Live service log
journalctl -u lepetitcafe -f

# Restart service
sudo systemctl restart lepetitcafe

# Test printer manually
python3 -c "
from escpos.printer import Network
p = Network('192.168.1.xxx')
p.text('Hello from Le Petit Café!\n')
p.cut()
p.close()
print('Success!')
"
```

| Problem | Solution |
|---------|----------|
| Printer unreachable | Check IP in `config.py`; printer and Pi on same WiFi? |
| Button not responding | Check GPIO pin number; check wiring |
| Service won't start | `journalctl -u lepetitcafe` for details |
| Receipt cuts off | Increase `DEBOUNCE_SECONDS` in `config.py` |

---

## Enclosure ideas

- **Wooden box** from a hardware store — hole for printer on top, three button holes on front
- **IKEA MOPPE** mini drawer unit — drawers as shopping basket, buttons on top
- **3D print** — enclosure designs welcome as PRs!
- **Metal lunchbox** — sturdy, cheap, hinged lid as a cash drawer

---

## Contributing

PRs welcome! Ideas:

- 🌍 More languages (French, Spanish, Italian...)
- 🏪 New play worlds (bakery, pharmacy, petrol station...)
- 🛠️ USB printer support
- 📦 3D-printable enclosure (STL files)
- 🧪 Unit tests for receipt generators

---

## License

MIT — free to use, modify and share. Have fun building it!

---

*Inspired by [claude-receipts](https://github.com/chrishutchinson/claude-receipts) by Chris Hutchinson.*
