PMS5003 Particulate Sensor
==========================

`Build Status <https://travis-ci.com/pimoroni/pms5003-python>`__
`Coverage
Status <https://coveralls.io/github/pimoroni/pms5003-python?branch=master>`__
`PyPi Package <https://pypi.python.org/pypi/pms5003>`__ `Python
Versions <https://pypi.python.org/pypi/pms5003>`__

Installing
==========

Stable library from PyPi:

-  Just run ``sudo pip install pms5003``

Latest/development library from GitHub:

-  ``git clone https://github.com/pimoroni/pms5003-python``
-  ``cd pms5003-python``
-  ``sudo ./install.sh``

Requirements
============

The serial port on your Raspberry Pi must be enabled:

::

   # Disable serial terminal over /dev/ttyAMA0
   sudo raspi-config nonint do_serial 1

   # Enable serial port
   raspi-config nonint set_config_var enable_uart 1 /boot/config.txt

And additionally be using a full UART (versus the default miniUART):

Add the line ``dtoverlay=pi3-miniuart-bt`` to your ``/boot/config.txt``

This will switch Bluetooth over to miniUART, see
https://www.raspberrypi.org/documentation/configuration/uart.md for more
details.

0.0.4
-----

* Packaging improvements/bugfix from boilerplate

0.0.3
-----

* Added pyserial dependency

0.0.2
-----

* Added reset function

0.0.1
-----

* Initial Release
