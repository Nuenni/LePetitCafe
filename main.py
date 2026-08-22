#!/usr/bin/env python3
"""
LePetitCafe - receipt printer for kids.
Six buttons -> six play scenarios -> thermal printer.
"""

import random
import time
import logging
import sys
from datetime import datetime

import RPi.GPIO as GPIO
from escpos.printer import File, Network, Serial

import config
from receipts import kaffeepause, layout, rezeptideen

# Which receipt language gets printed is set in config.LANGUAGE. The
# generators have the same interface in both languages, so it's enough to
# pick the matching set here.
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

# Every secret button combo: which two pins, what to log it as, and which
# receipt function to call when it triggers.
KOMBIS = (
    (config.COFFEE_COMBO, "Coffee break (combo)", kaffeepause.erstelle_bon),
    (config.RECIPE_COMBO, "Recipe idea (combo)", rezeptideen.erstelle_bon),
)
# Reverse lookup: pin -> the combo tuple it belongs to (if any).
_KOMBI_PIN_ZU_PAAR = {
    pin: paar for paar, _, _ in KOMBIS for pin in paar
}


def _drucker_verbinden():
    """Connect to the printer - over USB, RS232, or the home network."""
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
    """Describes where output is going, for the log."""
    if config.PRINTER_MODE == "network":
        return f"{config.PRINTER_IP}:{config.PRINTER_PORT}"
    if config.PRINTER_MODE == "serial":
        return f"{config.SERIAL_DEVICE} @ {config.SERIAL_BAUDRATE} Baud"
    return config.PRINTER_DEVICE


def _auf_drucker_warten(versuche: int = 10, pause: float = 3.0) -> bool:
    """
    At boot, the USB printer is often not enumerated yet. So retry a few
    times instead of giving up right away.
    """
    for versuch in range(1, versuche + 1):
        try:
            _drucker_verbinden().close()
            return True
        except Exception as exc:
            log.warning(
                "Printer not ready yet (%d/%d): %s", versuch, versuche, exc
            )
            time.sleep(pause)
    return False


def _bereit_bon(drucker) -> None:
    """
    Small startup receipt. Stands in for a ready LED: once paper comes out,
    the kid knows the buttons are live.
    """
    drucker.set(align="center", bold=True, double_height=True, double_width=True)
    drucker.text("LE PETIT CAFÉ\n")
    drucker.set(normal_textsize=True, align="center", bold=False, double_height=False, double_width=False)
    drucker.text(layout.divider())
    drucker.set(align="center", bold=True, double_height=True)
    drucker.text("BEREIT – auf geht's!\n")
    drucker.set(normal_textsize=True, align="center", bold=False, double_height=False)
    drucker.text("\n")
    drucker.text(f"{datetime.now().strftime('%d.%m.%Y  %H:%M')}\n")
    drucker.text(layout.divider())
    drucker.text("\n")
    drucker.set(bold=True)
    drucker.text("Drück einen Knopf:\n\n")
    drucker.set(align="left", double_height=True)
    for farbe, welt in (
        ("ROT",     "Supermarkt"),
        ("BLAU",    "Eiscafé"),
        ("GRUEN",   "Restaurant"),
        ("GELB",    "Bus/Taxi"),
        ("SCHWARZ", "KinderKino"),
        ("WEISS",   "Reservierung"),
    ):
        drucker.text(f"{farbe:<8}{welt}\n")
    drucker.set(normal_textsize=True, align="center", bold=False, double_height=False)
    drucker.cut()


def _drucken(name: str, bon_fn) -> None:
    log.info("Printing receipt: %s", name)
    try:
        drucker = _drucker_verbinden()
        bon_fn(drucker)
        drucker.close()
        log.info("Receipt printed: %s", name)
    except Exception as exc:
        log.error("Print error (%s): %s", name, exc)


def _knopf_gedrueckt(pin: int) -> None:
    jetzt = time.monotonic()
    if jetzt - _letzter_druck.get(pin, 0) < config.DEBOUNCE_SECONDS:
        return
    _letzter_druck[pin] = jetzt

    name, bon_fn = SCHALTFLÄCHEN[pin]

    if (config.COFFEE_RANDOM_EVERY
            and random.random() < 1 / config.COFFEE_RANDOM_EVERY):
        _drucken("Coffee break (random)", kaffeepause.erstelle_bon)
        return

    _drucken(name, bon_fn)


def main() -> None:
    """
    Polls all six buttons in a tight loop instead of using RPi.GPIO's
    interrupt-based edge detection (GPIO.add_event_detect). On some newer
    kernels that relies on a sysfs interface that no longer works reliably
    and raises "Failed to add edge detection" - plain GPIO.input() polling
    uses a different, more fundamental mechanism and keeps working there.
    """
    GPIO.setmode(GPIO.BCM)
    for pin in SCHALTFLÄCHEN:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    log.info("LePetitCafe started - printer: %s (%d columns wide)",
             _druckerziel(), config.PRINTER_WIDTH)
    log.info(
        "Pins: Supermarkt=GPIO%d  Eiscafe=GPIO%d  Restaurant=GPIO%d  "
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
                log.error("Startup receipt failed: %s", exc)
        else:
            log.error("Printer unreachable - buttons will still work once "
                      "the printer is available.")

    # Last known level per pin, to detect press (HIGH->LOW) and release
    # (LOW->HIGH) transitions while polling.
    letzter_pegel = {pin: GPIO.HIGH for pin in SCHALTFLÄCHEN}
    # Timestamp a combo button went down, and which combo pair already fired
    # (so releasing the second button of a triggered pair doesn't double-print).
    combo_gehalten_seit: dict[int, float] = {}
    combo_ausgeloest: dict[tuple, bool] = {}

    try:
        while True:
            jetzt = time.monotonic()
            for pin in SCHALTFLÄCHEN:
                pegel = GPIO.input(pin)
                war = letzter_pegel[pin]
                letzter_pegel[pin] = pegel

                if pegel == war:
                    continue

                paar = _KOMBI_PIN_ZU_PAAR.get(pin)
                if paar is None:
                    if pegel == GPIO.LOW:
                        _knopf_gedrueckt(pin)
                    continue

                # One of this combo's two buttons changed state.
                # RPi.GPIO's classic PUD_UP wiring means LOW = pressed.
                if pegel == GPIO.LOW:
                    combo_gehalten_seit[pin] = jetzt
                    continue

                # Released.
                start = combo_gehalten_seit.pop(pin, jetzt)
                dauer = jetzt - start
                andere_pin = next(p for p in paar if p != pin)
                andere_noch_gehalten = andere_pin in combo_gehalten_seit

                if combo_ausgeloest.get(paar):
                    # This combo already fired when the first button was
                    # released - this second release still belongs to it,
                    # but no longer triggers anything itself.
                    combo_ausgeloest[paar] = False
                    continue

                if dauer >= config.COMBO_HOLD_SECONDS and andere_noch_gehalten:
                    combo_ausgeloest[paar] = True
                    if jetzt - _letzter_druck.get(pin, 0) >= config.DEBOUNCE_SECONDS:
                        _letzter_druck[pin] = jetzt
                        _, label, bon_fn = next(k for k in KOMBIS if k[0] == paar)
                        _drucken(label, bon_fn)
                    continue

                # Not a long joint hold, just a normal short press on one of
                # this combo's two buttons.
                _knopf_gedrueckt(pin)

            time.sleep(0.02)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
        log.info("LePetitCafe stopped.")


if __name__ == "__main__":
    main()
