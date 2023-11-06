import sys
import mock
import pytest
import struct


class MockSerialFail():
    def __init__(self):
        pass

    def read(self, length):
        return b'\x00' * length


class MockSerial():
    def __init__(self):
        self.ptr = 0
        self.sof = b'\x42\x4d'
        self.data = self.sof
        self.data += struct.pack('>H', 28)
        self.data += b'\x00' * 26
        checksum = struct.pack('>H', sum(bytearray(self.data)))
        self.data += checksum

    def read(self, length):
        result = self.data[self.ptr:self.ptr + length]
        self.ptr += length
        if self.ptr >= len(self.data):
            self.ptr = 0
        return result


def _mock():
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi.GPIO'] = mock.Mock()
    sys.modules['serial'] = mock.Mock()


def test_setup():
    _mock()
    import pms5003
    sensor = pms5003.PMS5003()
    del sensor


def test_double_setup():
    _mock()
    import pms5003
    sensor = pms5003.PMS5003()
    sensor.setup()


def test_read():
    _mock()
    import pms5003
    sensor = pms5003.PMS5003()
    sensor._serial = MockSerial()
    data = sensor.read()
    data.pm_ug_per_m3(2.5)


def test_read_fail():
    _mock()
    import pms5003
    sensor = pms5003.PMS5003()
    sensor._serial = MockSerialFail()
    with pytest.raises(pms5003.ReadTimeoutError):
        data = sensor.read()
        del data
