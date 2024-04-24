import struct
import sys

import mock
import pytest


class MockSerial:
    def __init__(self, *args, **kwargs):
        self.ptr = 0
        self.sof = b"\x42\x4d"
        self.data = self.sof
        self.data += struct.pack(">H", 28)
        self.data += b"\x00" * 26
        checksum = struct.pack(">H", sum(bytearray(self.data)))
        self.data += checksum

    def read(self, length):
        result = self.data[self.ptr : self.ptr + length]
        self.ptr += length
        if self.ptr >= len(self.data):
            self.ptr = 0
        return result

    def flushInput(self):
        pass

    def close(self):
        pass


class MockSerialFail(MockSerial):
    def __init__(self, *args, **kwargs):
        pass

    def read(self, length):
        return b"\x00" * length


@pytest.fixture(scope='function', autouse=False)
def pms5003():
    import pms5003
    yield pms5003
    del sys.modules['pms5003']


@pytest.fixture(scope='function', autouse=False)
def gpiod():
    sys.modules['gpiod'] = mock.Mock()
    sys.modules['gpiod.line'] = mock.Mock()
    yield sys.modules['gpiod']
    del sys.modules['gpiod.line']
    del sys.modules['gpiod']


@pytest.fixture(scope='function', autouse=False)
def gpiodevice():
    gpiodevice = mock.Mock()
    gpiodevice.get_pins_for_platform.return_value = [(mock.Mock(), 0), (mock.Mock(), 0)]
    gpiodevice.get_pin.return_value = (mock.Mock(), 0)

    sys.modules['gpiodevice'] = gpiodevice
    yield gpiodevice
    del sys.modules['gpiodevice']


@pytest.fixture(scope='function', autouse=False)
def serial():
    sys.modules['serial'] = mock.Mock()
    sys.modules['serial'].Serial = MockSerial
    yield sys.modules['serial']
    del sys.modules['serial']


@pytest.fixture(scope='function', autouse=False)
def serial_fail():
    sys.modules['serial'] = mock.Mock()
    sys.modules['serial'].Serial = MockSerialFail
    yield sys.modules['serial']
    del sys.modules['serial']

