#!/usr/bin/env python
"""
Call this script from telegraf by adding the following lines to telegraf.conf

[[inputs.exec]]
  commands = ["python <script location>/telegraf_influxdb.py"]
  timeout = "2s"
  data_format = "influx"
"""

from pms5003 import PMS5003


# Configure the PMS5003 for Enviro+
pms5003 = PMS5003(
    device='/dev/ttyAMA0',
    baudrate=9600,
    pin_enable=22,
    pin_reset=27
)

print(pms5003.read().as_influxdb_line_proto())
