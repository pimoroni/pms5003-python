#!/usr/bin/env python

from pms5003 import PMS5003

print(
    """all.py - Continuously print all data values.

Press Ctrl+C to exit!

"""
)


# Configure the PMS5003 for Enviro+
# PIN15 and PIN13 are enable and reset for Raspberry Pi 5
pms5003 = PMS5003(device="/dev/ttyAMA0", baudrate=9600, pin_enable="PIN15", pin_reset="PIN13")

try:
    while True:
        data = pms5003.read()
        print(data)

except KeyboardInterrupt:
    pass
