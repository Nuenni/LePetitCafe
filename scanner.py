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


def _scanner_devices() -> list:
    """
    Finds every input device whose reported name contains
    config.SCANNER_NAME_HINT - so two identical scanners both get picked up,
    each listened to on its own thread. Find the real name on the Pi with:
        cat /proc/bus/input/devices
    """
    return [
        InputDevice(pfad) for pfad in list_devices()
        if config.SCANNER_NAME_HINT.lower() in InputDevice(pfad).name.lower()
    ]


def _lauschen(geraet, auf_scan) -> None:
    log.info("Scanner connected: %s (%s)", geraet.name, geraet.path)
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


def starten(auf_scan) -> list[threading.Thread]:
    """
    Starts one background thread per connected scanner (there can be more
    than one, e.g. so two kids can scan at once) and returns them all.
    main.py's GPIO polling loop keeps running independently on the main
    thread. All scanners feed the same auf_scan callback - main.py doesn't
    need to know or care which physical scanner a given scan came from.
    """
    geraete = _scanner_devices()
    if not geraete:
        log.warning(
            "No scanner found (looking for a device name containing %r) - "
            "scanning disabled. Check with: cat /proc/bus/input/devices",
            config.SCANNER_NAME_HINT,
        )
        return []

    threads = []
    for geraet in geraete:
        thread = threading.Thread(target=_lauschen, args=(geraet, auf_scan), daemon=True)
        thread.start()
        threads.append(thread)
    return threads
