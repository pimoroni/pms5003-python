import RPi.GPIO as GPIO
import serial
import struct
import time


__version__ = '0.0.4'


PMS5003_SOF = bytearray(b'\x42\x4d')


class ChecksumMismatchError(RuntimeError):
    pass


class ReadTimeoutError(RuntimeError):
    pass


class SerialTimeoutError(RuntimeError):
    pass


class PMS5003Data():
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.data = struct.unpack(">HHHHHHHHHHHHHH", raw_data)
        self.checksum = self.data[13]

    def pm_ug_per_m3(self, size, atmospheric_environment=False):
        if atmospheric_environment:
            if size == 1.0:
                return self.data[3]
            if size == 2.5:
                return self.data[4]
            if size is None:
                return self.data[5]

        else:
            if size == 1.0:
                return self.data[0]
            if size == 2.5:
                return self.data[1]
            if size == 10:
                return self.data[2]

        raise ValueError("Particle size {} measurement not available.".format(size))

    def pm_per_1l_air(self, size):
        if size == 0.3:
            return self.data[6]
        if size == 0.5:
            return self.data[7]
        if size == 1.0:
            return self.data[8]
        if size == 2.5:
            return self.data[9]
        if size == 5:
            return self.data[10]
        if size == 10:
            return self.data[11]

        raise ValueError("Particle size {} measurement not available.".format(size))

    def __repr__(self):
        return """
PM1.0 ug/m3 (ultrafine particles):                             {}
PM2.5 ug/m3 (combustion particles, organic compounds, metals): {}
PM10 ug/m3  (dust, pollen, mould spores):                      {}
PM1.0 ug/m3 (atmos env):                                       {}
PM2.5 ug/m3 (atmos env):                                       {}
PM10 ug/m3 (atmos env):                                        {}
>0.3um in 0.1L air:                                            {}
>0.5um in 0.1L air:                                            {}
>1.0um in 0.1L air:                                            {}
>2.5um in 0.1L air:                                            {}
>5.0um in 0.1L air:                                            {}
>10um in 0.1L air:                                             {}
""".format(*self.data[:-2], checksum=self.checksum)

    def __str__(self):
        return self.__repr__()


class PMS5003():
    def __init__(self, device='/dev/ttyAMA0', baudrate=9600, pin_enable=22, pin_reset=27):
        self._serial = None
        self._device = device
        self._baudrate = baudrate
        self._pin_enable = pin_enable
        self._pin_reset = pin_reset
        self.setup()

    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin_enable, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self._pin_reset, GPIO.OUT, initial=GPIO.HIGH)

        if self._serial is not None:
            self._serial.close()

        self._serial = serial.Serial(self._device, baudrate=self._baudrate, timeout=4)

        self.reset()

    def reset(self):
        time.sleep(0.1)
        GPIO.output(self._pin_reset, GPIO.LOW)
        self._serial.flushInput()
        time.sleep(0.1)
        GPIO.output(self._pin_reset, GPIO.HIGH)

    def read(self):
        start = time.time()

        while True:
            elapsed = time.time() - start
            if elapsed > 5:
                raise ReadTimeoutError("PMS5003 Read Timeout")

            sof = bytearray(self._serial.read(2))
            if sof == PMS5003_SOF:
                break

        checksum = sum(PMS5003_SOF)

        data = bytearray(self._serial.read(2))  # Get frame length packet
        if len(data) != 2:
            raise SerialTimeoutError("PMS5003 Serial Timeout")
        checksum += sum(data)
        frame_length = struct.unpack(">H", data)[0]

        raw_data = bytearray(self._serial.read(frame_length))
        data = PMS5003Data(raw_data)
        # Don't include the checksum bytes in the checksum calculation
        checksum += sum(raw_data[:-2])

        if checksum != data.checksum:
            raise ChecksumMismatchError("PMS5003 Checksum Mismatch {} != {}".format(checksum, data.checksum))

        return data
