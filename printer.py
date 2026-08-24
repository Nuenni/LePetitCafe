"""Shared printer connection, used by main.py and ping_app.py."""

from escpos.printer import File, Network, Serial

import config


def connect():
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


def target() -> str:
    """Describes where output is going, for the log."""
    if config.PRINTER_MODE == "network":
        return f"{config.PRINTER_IP}:{config.PRINTER_PORT}"
    if config.PRINTER_MODE == "serial":
        return f"{config.SERIAL_DEVICE} @ {config.SERIAL_BAUDRATE} Baud"
    return config.PRINTER_DEVICE
