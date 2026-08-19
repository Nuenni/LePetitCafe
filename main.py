#!/usr/bin/env python3
"""
LePetitCafe – Kassenbon-Drucker für Kinder.
Drei Knöpfe → drei Spielszenarien → Thermodrucker.
"""

import time
import logging
import sys
from datetime import datetime

import RPi.GPIO as GPIO
from escpos.printer import File, Network, Serial

import config
from receipts import layout

# Welche Bon-Sprache gedruckt wird, steht in config.LANGUAGE. Die Generatoren
# haben in beiden Sprachen dieselbe Schnittstelle, deshalb reicht es, hier das
# passende Trio auszuwählen.
if config.LANGUAGE == "de":
    from receipts import supermarkt as welt_markt
    from receipts import eiscafe as welt_eis
    from receipts import restaurant as welt_bistro
    from receipts import bus as welt_bus
    from receipts import kino as welt_kino
    from receipts import reservierung as welt_reservierung
else:
    from receipts import supermarket as welt_markt
    from receipts import icecream as welt_eis
    from receipts import bistro as welt_bistro
    from receipts import transit as welt_bus
    from receipts import cinema as welt_kino
    from receipts import reservation as welt_reservierung

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)

SCHALTFLÄCHEN = {
    config.GPIO_SUPERMARKT:    ("Supermarkt",    welt_markt.erstelle_bon),
    config.GPIO_EISCAFE:       ("Eiscafé",       welt_eis.erstelle_bon),
    config.GPIO_RESTAURANT:    ("Restaurant",    welt_bistro.erstelle_bon),
    config.GPIO_BUS:           ("Bus/Taxi",      welt_bus.erstelle_bon),
    config.GPIO_KINO:          ("KinderKino",    welt_kino.erstelle_bon),
    config.GPIO_RESERVIERUNG:  ("Reservierung",  welt_reservierung.erstelle_bon),
}

_letzter_druck: dict[int, float] = {}


def _drucker_verbinden():
    """Verbindung zum Drucker – per USB, RS232 oder über das Heimnetz."""
    if config.PRINTER_MODE == "network":
        return Network(config.PRINTER_IP, port=config.PRINTER_PORT, timeout=5)
    if config.PRINTER_MODE == "serial":
        return Serial(
            devfile=config.SERIAL_DEVICE,
            baudrate=config.SERIAL_BAUDRATE,
            dsrdtr=config.SERIAL_DSRDTR,
            timeout=5,
        )
    return File(config.PRINTER_DEVICE)


def _druckerziel() -> str:
    """Beschreibt fürs Log, wohin gedruckt wird."""
    if config.PRINTER_MODE == "network":
        return f"{config.PRINTER_IP}:{config.PRINTER_PORT}"
    if config.PRINTER_MODE == "serial":
        return f"{config.SERIAL_DEVICE} @ {config.SERIAL_BAUDRATE} Baud"
    return config.PRINTER_DEVICE


def _auf_drucker_warten(versuche: int = 10, pause: float = 3.0) -> bool:
    """
    Beim Systemstart ist der USB-Drucker oft noch nicht fertig erkannt.
    Deshalb ein paar Mal in Ruhe nachfassen, statt sofort aufzugeben.
    """
    for versuch in range(1, versuche + 1):
        try:
            _drucker_verbinden().close()
            return True
        except Exception as exc:
            log.warning(
                "Drucker noch nicht bereit (%d/%d): %s", versuch, versuche, exc
            )
            time.sleep(pause)
    return False


def _bereit_bon(drucker) -> None:
    """
    Kleiner Startbon. Ersetzt eine Bereitschafts-LED: Sobald Papier
    rauskommt, weiß das Kind, dass die Knöpfe jetzt reagieren.
    """
    drucker.set(align="center", bold=True, double_height=True, double_width=True)
    drucker.text("LE PETIT CAFÉ\n")
    drucker.set(align="center", bold=False, double_height=False, double_width=False)
    drucker.text(layout.divider())
    drucker.text("BEREIT – auf geht's!\n")
    drucker.text(f"{datetime.now().strftime('%d.%m.%Y  %H:%M')}\n")
    drucker.text(layout.divider())
    drucker.text("\n")
    drucker.text("Drück einen Knopf:\n\n")
    drucker.text("ROT     Supermarkt\n")
    drucker.text("BLAU    Eiscafé\n")
    drucker.text("GRUEN   Restaurant\n")
    drucker.text("GELB    Bus/Taxi\n")
    drucker.text("SCHWARZ KinderKino\n")
    drucker.text("WEISS   Reservierung\n")
    drucker.cut()


def _knopf_gedrueckt(pin: int) -> None:
    jetzt = time.monotonic()
    if jetzt - _letzter_druck.get(pin, 0) < config.DEBOUNCE_SECONDS:
        return
    _letzter_druck[pin] = jetzt

    name, bon_fn = SCHALTFLÄCHEN[pin]
    log.info("Knopf gedrückt: %s", name)

    try:
        drucker = _drucker_verbinden()
        bon_fn(drucker)
        drucker.close()
        log.info("Bon gedruckt: %s", name)
    except Exception as exc:
        log.error("Druckfehler (%s): %s", name, exc)


def main() -> None:
    GPIO.setmode(GPIO.BCM)

    for pin in SCHALTFLÄCHEN:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(
            pin,
            GPIO.FALLING,
            callback=_knopf_gedrueckt,
            bouncetime=300,
        )

    log.info("LePetitCafe gestartet – Drucker: %s (%d Zeichen breit)",
             _druckerziel(), config.PRINTER_WIDTH)
    log.info(
        "Pins: Supermarkt=GPIO%d  Eiscafé=GPIO%d  Restaurant=GPIO%d  "
        "Bus/Taxi=GPIO%d  KinderKino=GPIO%d  Reservierung=GPIO%d",
        config.GPIO_SUPERMARKT,
        config.GPIO_EISCAFE,
        config.GPIO_RESTAURANT,
        config.GPIO_BUS,
        config.GPIO_KINO,
        config.GPIO_RESERVIERUNG,
    )

    if config.PRINT_READY_RECEIPT:
        if _auf_drucker_warten():
            try:
                drucker = _drucker_verbinden()
                _bereit_bon(drucker)
                drucker.close()
            except Exception as exc:
                log.error("Startbon fehlgeschlagen: %s", exc)
        else:
            log.error("Drucker nicht erreichbar – Knöpfe funktionieren trotzdem, "
                      "sobald der Drucker da ist.")

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
        log.info("LePetitCafe beendet.")


if __name__ == "__main__":
    main()
