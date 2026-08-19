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
Raspberry Pi Zero 2 W  (no screen, no network needed)
        │  USB
        ▼
Thermal printer
        │
        ▼
Receipt comes out 🎉
```

Everything lives in one box with a single power cable, so the kids can carry it into another room and just plug it in.

Every receipt is unique — random items, prices, names, table numbers, timestamps. No two receipts are ever the same.

---

## Three Play Worlds, Three Buttons

| Button | Store | Receipt includes |
|--------|-------|-----------------|
| 🔴 Red | **PETIT MARCHÉ** (Supermarket) | Groceries, cashier name, change calculation |
| 🟣 Purple | **LE PETIT CAFÉ** (Ice Cream Café) | Sundaes, ice lollies, chosen flavours |
| 🔵 Blue | **LE PETIT BISTRO** (Restaurant) | Starter / main / dessert / drinks, VAT, sometimes a tip |

All three end with a barcode and a **scannable QR code** containing a joke or a voucher — see below.

Receipts are available in **German** (default) and **English** — see `receipts/` folder.

### The QR code

Every receipt ends with a barcode and a QR code. The QR doesn't point at a website — **the message is encoded in the code itself**, so scanning it with any phone camera shows the text instantly, with no internet connection and nothing to host or keep running.

Each play world has its own pool of jokes and vouchers:

> *VOUCHER: You're head chef today. What are we having?*
> *Waiter, there's a fly in my soup! — Don't worry, the spider is coming.*

Edit `QR_MESSAGES` in any receipt file to add your own. Keep them ASCII — the printer generates the QR in hardware and passes the bytes through as given, so plain ASCII reads identically on every scanner while accented characters depend on the device.

---

## Hardware

### What you need

Everything below plugs together — **no soldering required**.

| Part | Recommendation | Price |
|------|---------------|-------|
| [Thermal printer](#printer) | Epson TM-T20II/III **USB**, bought used | 35–50 € |
| Printer power supply | Epson PS-180 (24V) — ⚠️ often missing, see below | 0–20 € |
| Single-board computer | Raspberry Pi Zero 2 **WH** *(header pre-soldered)* | ~25 € |
| microSD card | 16 GB Class 10 | ~8 € |
| Pi power supply | 5V / 2.5A Micro-USB | ~10 € |
| USB adapter | Micro-USB **OTG** → USB-A *(the Pi Zero has no USB-A port)* | ~5 € |
| Arcade buttons | 60mm with 6.3mm spade terminals, 3 colours | ~12 € |
| Button cables | 6.3mm spade → Dupont socket, 6 pieces | ~8 € |
| Power strip | Short 3-outlet strip, so only **one** cable leaves the box | ~8 € |
| Enclosure | Wooden box, toolbox or 3D print | ~15 € |

**Total: ~135 €** — around 90 € if you find a printer with its power supply cheap.

> ⚠️ **The one mistake to avoid when buying used:** many listings ship *without* the PS-180 power supply (24V, 3-pin) — restaurants tend to keep them. Buying one separately costs 17–25 €. Always check the listing says "with power supply". Also make sure you get the **USB** variant — the TM-T20 also exists with serial and Ethernet interfaces.

---

### Printer

The code uses the **ESC/POS** protocol, supported by virtually all thermal receipt printers. Three connection modes are supported, set via `PRINTER_MODE` in `config.py`:

- **`"usb"`** *(recommended)* — printer plugs straight into the Pi. Works with no router and no WiFi, so the whole box can be carried anywhere there's a power socket.
- **`"serial"`** — for older printers that only have RS232. See [Serial printers](#serial-printers-rs232) below.
- **`"network"`** — printer sits on the home network (TCP port 9100).

**Epson TM-T20II / TM-T20III, bought used** *(recommended, 35–50 €)*
- 80mm paper, auto-cutter, very fast and quiet
- Built for restaurant use — these things are indestructible
- Widely available second-hand from restaurant closures
- Search Kleinanzeigen / eBay: `Epson TM-T20 Bondrucker USB`

**Star TSP100 (futurePRNT), bought used** *(alternative, ~35 €)*
- 80mm, auto-cutter, equally solid, also common second-hand

**Any 58mm ESC/POS printer** *(budget option, ~40 €)*
- Narrower receipts — set `PRINTER_WIDTH = 32` in `config.py`

> **Paper rolls:** Standard 80mm × 80mm thermal rolls, ~10 € for a 10-pack.

> **Receipt width:** `PRINTER_WIDTH` in `config.py` controls how many characters fit per line — **42** for 80mm paper, **32** for 58mm. If your dividers don't reach the edge of the paper, this is the setting to adjust.

---

### Serial printers (RS232)

Plenty of cheap second-hand printers only have RS232. They work fine — you just need the right cable and the right baud rate.

**The cable.** Epson printers use a **DB25 socket** and need a **null-modem** (crossover) cable, not a straight-through one. Buy it as a single part rather than stacking adapters — search for `FTDI USB RS232 DB25 null modem cable Epson TM` (~15–20 €). It shows up on the Pi as `/dev/ttyUSB0`.

**The baud rate.** This is the one thing that has to match, or you get garbled output. To find out what the printer is set to: **switch it off, hold the FEED button, switch it on** — it prints a self-test page listing its current serial settings. Put that value into `config.py`:

```python
PRINTER_MODE    = "serial"
SERIAL_DEVICE   = "/dev/ttyUSB0"
SERIAL_BAUDRATE = 38400      # whatever the self-test says
SERIAL_DSRDTR   = True       # keep this on
```

> Leave `SERIAL_DSRDTR = True`. Epson printers rely on hardware flow control; without it, longer receipts lose lines when the print buffer fills up.

---

### Raspberry Pi Zero 2 W

Get the **WH** variant — the "H" means the GPIO header is already soldered on, which is the difference between a plug-together build and one that needs a soldering iron.

| | Pi Zero 2 WH *(recommended)* | Pi Zero WH *(also fine)* |
|--|--|--|
| Price | ~25–30 € | ~20–35 € |
| CPU | Quad-core 1GHz | Single-core 1GHz |
| RAM | 512MB | 512MB |
| WiFi | ✓ | ✓ |

**The older Pi Zero WH works perfectly well here.** The workload is a handful of string operations per button press, and the program runs continuously — so nothing is started when a button is pressed, and response time is identical on both. The faster chip only shows up in boot time (~30s vs ~45s), which the startup receipt already covers. Buy whichever you can actually get; the Zero 2 WH is frequently out of stock.

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
2. Flash **Raspberry Pi OS Lite** — pick the bitness that matches your board:
   - **Pi Zero W / Zero WH** (single-core, ARMv6) → **32-bit**. This board cannot boot a 64-bit image at all — the Imager won't stop you from picking the wrong one, so double-check.
   - **Pi Zero 2 W / Zero 2 WH** (quad-core, ARMv8) → 64-bit works, but 32-bit runs fine too.
3. In the Imager settings (⚙️): set WiFi credentials, enable SSH, set username `pi`
4. Insert SD card, power on — first boot takes ~30s on a Zero 2, ~45s on the original Zero

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

Set how the printer is connected and how wide the paper is:

```python
PRINTER_MODE   = "usb"            # "usb", "serial" or "network"
PRINTER_DEVICE = "/dev/usb/lp0"   # check with: ls /dev/usb/
PRINTER_WIDTH  = 42               # 42 for 80mm paper, 32 for 58mm
LANGUAGE       = "en"             # "de" or "en"

GPIO_SUPERMARKT  = 17
GPIO_EISCAFE     = 27
GPIO_RESTAURANT  = 22
```

### Step 3b — Your own names (optional)

The receipts name a cashier and a server. Out of the box those are generic placeholders — because `config.py` is in a public repository and **real names, especially children's names, don't belong there.**

For anything personal, create a `config_local.py` instead. It's listed in `.gitignore`, so it stays on your device and can never be committed by accident:

```bash
cp config_local.py.example config_local.py
nano config_local.py
```

```python
STAFF_NAMES = ["Anna", "Ben", "Charlie"]   # your kids
LANGUAGE    = "de"                          # German receipts
```

Anything you put there overrides `config.py`; anything you leave out keeps its default. The same file is the right place for your printer's IP address or any other detail that's nobody else's business.

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

A short **"READY"** receipt prints as soon as the Pi has booted — that's your cue that the buttons are live. (It works as a poor man's status LED; turn it off with `PRINT_READY_RECEIPT = False`.)

**Press a button → receipt comes out!** 🎉

Le Petit Café now starts automatically every time the Pi is powered on.

> 💡 **If the box gets carried around and unplugged a lot**, enable the read-only filesystem: `sudo raspi-config` → *Performance Options* → *Overlay File System*. Pulling the plug then can't corrupt the SD card.

---

## Project structure

```
LePetitCafe/
├── main.py                  # GPIO listener, print dispatcher
├── config.py                # ← Printer, GPIO pins, language
├── config_local.py.example  # ← Template for personal settings (gitignored)
├── requirements.txt         # python-escpos, RPi.GPIO
├── setup.sh                 # One-time setup script
├── lepetitcafe.service      # systemd unit for autostart
├── test_receipts.py         # Checks every receipt fits the paper width
├── preview.py               # Regenerates the two demos below
├── simulator.html           # Standalone demo — German
├── simulator_en.html        # Standalone demo — English
├── docs/
│   └── preview.png
└── receipts/
    ├── layout.py            # Width-aware line layout (58mm / 80mm)
    ├── supermarkt.py        # 🇩🇪 PETIT MARCHÉ
    ├── eiscafe.py           # 🇩🇪 LE PETIT CAFÉ
    ├── restaurant.py        # 🇩🇪 LE PETIT BISTRO
    ├── supermarket.py       # 🇬🇧 THE LITTLE MARKET
    ├── icecream.py          # 🇬🇧 THE LITTLE CAFÉ
    └── bistro.py            # 🇬🇧 THE LITTLE BISTRO
```

---

## Preview without hardware

```bash
python3 preview.py
```

Regenerates `simulator.html` and `simulator_en.html` — standalone pages with 24 sample receipts, three arcade buttons to cycle through them, and no server needed. Open the file in any browser.

The preview is **character-accurate**: it renders in real monospace at exactly `PRINTER_WIDTH` columns, so what you see is what the printer puts out. It also checks every character against the printer's actual code-page profile via `python-escpos` and highlights anything the printer can't represent in red.

That check is worth running after editing any receipt text. Thermal printers don't do Unicode — they switch between 8-bit code pages. Box-drawing characters (`─ ═`), umlauts, `é` and even `€` all work, but decorative symbols like `★ ✿ ✦` have no code page and would silently print as `?`.

---

## Troubleshooting

```bash
# Live service log
journalctl -u lepetitcafe -f

# Restart service
sudo systemctl restart lepetitcafe

# Is the USB printer detected?
ls /dev/usb/          # expect lp0
lsusb                 # expect e.g. "Seiko Epson Corp. Receipt Printer"

# Test printer manually (USB)
python3 -c "
from escpos.printer import File
p = File('/dev/usb/lp0')
p.text('Hello from Le Petit Café!\n')
p.cut()
p.close()
print('Success!')
"
```

| Problem | Solution |
|---------|----------|
| `/dev/usb/lp0` missing | Printer switched on? Using the **OTG** adapter on the Pi Zero? Check `lsusb` |
| Permission denied on `/dev/usb/lp0` | `sudo usermod -a -G lp,dialout $USER`, then reboot |
| Serial: garbled characters | Wrong `SERIAL_BAUDRATE` — read the real value off the FEED-button self-test |
| Serial: lines missing on long receipts | `SERIAL_DSRDTR = True` (flow control) |
| Serial: nothing happens at all | Straight-through cable instead of **null-modem**? Check `ls /dev/ttyUSB*` |
| Printer unreachable (network mode) | Check IP in `config.py`; printer and Pi on same WiFi? |
| Dividers don't span the paper | Wrong `PRINTER_WIDTH` — use 42 for 80mm, 32 for 58mm |
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
- 📦 3D-printable enclosure (STL files)
- 🔋 Battery-powered variant (58mm printer module + power bank)

---

## Disclaimer

This is a non-commercial hobby project, built for fun and for making kids happy at home — nothing here is sold or offered as a service. Some receipts mention real brand and character names (Magnum, Calippo, Solero, Twister, After Eight, Biene Maja, Pinocchio...) purely because kids recognize them and it makes the pretend-play more fun. This project has no affiliation with, endorsement from, or connection to any of those trademark holders — all trademarks and copyrights belong to their respective owners. If you're one of them and this bothers you: it's a printer in someone's playroom, not a business. Open an issue and it'll get sorted out.

## License

MIT — free to use, modify and share. Have fun building it!

---

*Inspired by [claude-receipts](https://github.com/chrishutchinson/claude-receipts) by Chris Hutchinson.*
