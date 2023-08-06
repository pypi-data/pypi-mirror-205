import asyncio
import glob
import sys
import logging

import serial

logger = logging.getLogger(__name__)

LINUX = "linux"
DARWIN = "darwin"


def get_system_name() -> str:
    if sys.platform.startswith(LINUX):
        return LINUX
    elif sys.platform.startswith(DARWIN):
        return DARWIN
    else:
        raise OSError(f"Unsupported system for serial reading: {sys.platform}")


SYSTEM_TO_SERIAL_PORT_GLOB = {LINUX: "/dev/ttyUSB*", DARWIN: "/dev/cu.usbserial*"}  # "/dev/tty.usbserial*"}


def get_serial_port() -> str:
    """Get the serial port based on the system"""
    system_name = get_system_name()
    serial_port_glob = SYSTEM_TO_SERIAL_PORT_GLOB[system_name]
    serial_ports = sorted(glob.glob(serial_port_glob))

    if not serial_ports:
        raise serial.SerialException("No serial port found. Is your serial cable plugged in?")

    logger.debug(f"Found serial ports {serial_ports} for system {system_name}, using first one.")
    return serial_ports[0]


DEFAULT_BLE_ADDRESS = {LINUX: "D5:73:DB:85:B4:A1", DARWIN: "b171e34e-9454-4d6d-b3d0-8740b703b66e"}[get_system_name()]


def get_or_create_event_loop():
    """Gets the running event loop or creates a new one and returns it

    By default `asyncio` only starts an event loop in the main thread, so when running in another thread we
    need to explicitly create a new event loop for that particular thread.
    """
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            asyncio.set_event_loop(asyncio.new_event_loop())
            return asyncio.get_event_loop()
