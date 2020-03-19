PMS5003 Particulate Sensor
==========================

|Build Status| |Coverage Status| |PyPi Package| |Python Versions|

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

.. |Build Status| image:: https://travis-ci.com/pimoroni/pms5003-python.svg?branch=master
   :target: https://travis-ci.com/pimoroni/pms5003-python
.. |Coverage Status| image:: https://coveralls.io/repos/github/pimoroni/pms5003-python/badge.svg?branch=master
   :target: https://coveralls.io/github/pimoroni/pms5003-python?branch=master
.. |PyPi Package| image:: https://img.shields.io/pypi/v/pms5003.svg
   :target: https://pypi.python.org/pypi/pms5003
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/pms5003.svg
   :target: https://pypi.python.org/pypi/pms5003

0.0.5
-----

* BugFix: Read start-of-frame a byte at a time to avoid misalignment issues, potential fix for #2, #3 and #4
* Enhancement: Clarified error message when length packet cannot be read
* Enhancement: Clarified error message when start of frame cannot be read
* Enhancement: Added new error message where raw data length is less than expected (frame length)

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
