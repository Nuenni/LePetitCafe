"""
Reads barcode scans from a USB handheld scanner via evdev.

Cheap USB scanners show up to Linux as a generic HID keyboard: they "type"
the barcode digits followed by Enter. On a headless Pi there's no window to
receive that keystroke text the normal way, so evdev reads it straight off
the input device instead.

The scanned code's actual value is discarded (see receipts/scankasse.py) -
only the fact that a scan just happened is used.
"""

import logging
import threading

from evdev import InputDevice, categorize, ecodes, list_devices

import config

log = logging.getLogger(__name__)

_ENTER_KEYS = {"KEY_ENTER", "KEY_KPENTER"}


def _scanner_device():
    """
    Finds the scanner among all input devices by a substring of its reported
    name (config.SCANNER_NAME_HINT). Find the real name on the Pi with:
        cat /proc/bus/input/devices
    """
    for pfad in list_devices():
        geraet = InputDevice(pfad)
        if config.SCANNER_NAME_HINT.lower() in geraet.name.lower():
            return geraet
    return None


def _lauschen(auf_scan) -> None:
    geraet = _scanner_device()
    if geraet is None:
        log.warning(
            "Scanner not found (looking for a device name containing %r) - "
            "scanning disabled. Check with: cat /proc/bus/input/devices",
            config.SCANNER_NAME_HINT,
        )
        return

    log.info("Scanner connected: %s", geraet.name)
    hat_zeichen = False
    for event in geraet.read_loop():
        if event.type != ecodes.EV_KEY or event.value != 1:  # only "key down"
            continue
        taste = categorize(event)
        code = ecodes.KEY.get(taste.scancode, "") if isinstance(taste.scancode, int) else taste.scancode

        if code in _ENTER_KEYS:
            if hat_zeichen:
                auf_scan()
            hat_zeichen = False
        else:
            hat_zeichen = True


def starten(auf_scan) -> threading.Thread:
    """
    Starts listening in a background thread and returns it. main.py's GPIO
    polling loop keeps running independently on the main thread.
    """
    thread = threading.Thread(target=_lauschen, args=(auf_scan,), daemon=True)
    thread.start()
    return thread
