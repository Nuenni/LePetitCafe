#!/usr/bin/env python3
"""
LePetitCafe – Kassenbon-Drucker für Kinder.
Drei Knöpfe → drei Spielszenarien → Thermodrucker.
"""

import time
import logging
import sys

import RPi.GPIO as GPIO
from escpos.printer import Network

import config
from receipts import supermarkt, eiscafe, restaurant

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)

SCHALTFLÄCHEN = {
    config.GPIO_SUPERMARKT:  ("Supermarkt",  supermarkt.erstelle_bon),
    config.GPIO_EISCAFE:     ("Eiscafé",     eiscafe.erstelle_bon),
    config.GPIO_RESTAURANT:  ("Restaurant",  restaurant.erstelle_bon),
}

_letzter_druck: dict[int, float] = {}


def _drucker_verbinden() -> Network:
    return Network(config.PRINTER_IP, port=config.PRINTER_PORT, timeout=5)


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

    log.info(
        "LePetitCafe gestartet – Drucker: %s:%d",
        config.PRINTER_IP,
        config.PRINTER_PORT,
    )
    log.info(
        "Pins: Supermarkt=GPIO%d  Eiscafé=GPIO%d  Restaurant=GPIO%d",
        config.GPIO_SUPERMARKT,
        config.GPIO_EISCAFE,
        config.GPIO_RESTAURANT,
    )

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
