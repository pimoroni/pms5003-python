1.0.1
-----

* Remove platform detection and default to Pi-compatible pins
* Support passing in LineRequest and offset for custom pins (supported in gpiodevice>=0.0.4)

1.0.0
-----

* Repackage to hatch/pyproject.toml
* Port to gpiod/gpiodevice (away from RPi.GPIO)

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
