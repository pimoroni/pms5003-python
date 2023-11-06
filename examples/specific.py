#!/usr/bin/env python

from pms5003 import PMS5003

print(
    """specific.py - Continuously print a specific data value.

Press Ctrl+C to exit!

"""
)

# Configure the PMS5003 for Enviro+
# PIN15 and PIN13 are enable and reset for Raspberry Pi 5
pms5003 = PMS5003(device="/dev/ttyAMA0", baudrate=9600, pin_enable="PIN15", pin_reset="PIN13")

try:
    while True:
        data = pms5003.read()
        print("PM2.5 ug/m3 (combustion particles, organic compounds, metals): {}".format(data.pm_ug_per_m3(2.5)))

except KeyboardInterrupt:
    pass
