#!/usr/bin/env python

from pms5003 import PMS5003

print("""specific.py - Continously print a specific data value.

Press Ctrl+C to exit!

""")

pms5003 = PMS5003()

try:
    while True:
        data = pms5003.read()
        print("PM2.5 ug/m3 (combustion particles, organic compounds, metals): {}".format(data.pm_ug_per_m3(2.5)))

except KeyboardInterrupt:
    pass
