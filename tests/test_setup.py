import pytest


def test_setup(gpiod, gpiodevice, serial, pms5003):
    _ = pms5003.PMS5003()


def test_double_setup(gpiod, gpiodevice, serial, pms5003):
    sensor = pms5003.PMS5003()
    sensor.setup()


def test_read(gpiod, gpiodevice, serial, pms5003):
    sensor = pms5003.PMS5003()
    data = sensor.read()
    data.pm_ug_per_m3(2.5)


def test_read_fail(gpiod, gpiodevice, serial_fail, pms5003):
    sensor = pms5003.PMS5003()
    with pytest.raises(pms5003.ReadTimeoutError):
        _ = sensor.read()
