#!/usr/bin/env python

from pms5003 import PMS5003
import time

print("""hourly.py - Run (approximately) hourly.

Press Ctrl+C to exit!

""")

# Configure the PMS5003 for Enviro+
pms5003 = PMS5003(
    device='/dev/ttyAMA0',
    baudrate=9600,
    pin_enable=22,
    pin_reset=27
)

last_read_epoch = 0

try:
    while True:
        # has it been an hour since our last reading?
        now = int(time.time())
        if (now - last_read_epoch) > 3600:
            last_read_epoch = now

            print("waking")
            pms5003.wake()

            # give sensor time to wake up and calibrate
            print("sleeping")
            time.sleep(60)
            print("reading")

            # take several readings, good for a median
            for _ in range(9):
                data = pms5003.read()
                print("PM2.5 ug/m3 (combustion particles, organic compounds, metals): {}".format(data.pm_ug_per_m3(2.5)))

            # done reading, shut down sensor (and its fan)
            print("sleeping")
            pms5003.sleep()
        else:
            time.sleep(10)

except KeyboardInterrupt:
    pass

