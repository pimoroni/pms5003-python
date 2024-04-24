# PMS5003 Particulate Sensor

[![Build Status](https://img.shields.io/github/actions/workflow/status/pimoroni/pms5003-python/test.yml?branch=main)](https://github.com/pimoroni/pms5003-python/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/pms5003-python/badge.svg?branch=main)](https://coveralls.io/github/pimoroni/pms5003-python?branch=main)
[![PyPi Package](https://img.shields.io/pypi/v/pms5003.svg)](https://pypi.python.org/pypi/pms5003)
[![Python Versions](https://img.shields.io/pypi/pyversions/pms5003.svg)](https://pypi.python.org/pypi/pms5003)

# Installing

**Note** The code in this repository supports both the Enviro+ and Enviro Mini boards. _The Enviro Mini board does not have the Gas sensor or the breakout for the PM sensor._

![Enviro Plus pHAT](https://raw.githubusercontent.com/pimoroni/enviroplus-python/main/Enviro-Plus-pHAT.jpg)
![Enviro Mini pHAT](https://raw.githubusercontent.com/pimoroni/enviroplus-python/main/Enviro-mini-pHAT.jpg)

:warning: This library now supports Python 3 only, Python 2 is EOL - https://www.python.org/doc/sunset-python-2/

## Install and configure dependencies from GitHub:

* `git clone https://github.com/pimoroni/pms5003-python`
* `cd pms5003-python`
* `./install.sh`

**Note** Libraries will be installed in the "pimoroni" virtual environment, you will need to activate it to run examples:

```
source ~/.virtualenvs/pimoroni/bin/activate
```

**Note** Raspbian/Raspberry Pi OS Lite users may first need to install git: `sudo apt install git`

## Or... Install from PyPi and configure manually:

* `python3 -m venv --system-site-packages $HOME/.virtualenvs/pimoroni`
* Run `python3 -m pip install pms5003`

**Note** this will not perform any of the required configuration changes on your Pi, you may additionally need to:

### Bookworm

* Enable serial: `raspi-config nonint do_serial_hw 0`
* Disable serial terminal: `raspi-config nonint do_serial_cons 1`
* Add `dtoverlay=pi3-miniuart-bt` to your `/boot/config.txt`

### Bullseye

* Enable serial: `raspi-config nonint set_config_var enable_uart 1 /boot/config.txt`
* Disable serial terminal: `sudo raspi-config nonint do_serial 1`
* Add `dtoverlay=pi3-miniuart-bt` to your `/boot/config.txt`

In both cases the last line will switch Bluetooth over to miniUART, see https://www.raspberrypi.org/documentation/configuration/uart.md for more details.
