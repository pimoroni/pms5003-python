import RPi.GPIO as GPIO
import serial
import struct
import time


__version__ = '0.0.5'


PMS5003_SOF = bytearray(b'\x42\x4d')


class ChecksumMismatchError(RuntimeError):
    pass


class ReadTimeoutError(RuntimeError):
    pass


class SerialTimeoutError(RuntimeError):
    pass


class PMS5003Data():
    def __init__(self, raw_data, timestamp=None):
        """
        Object to store the output of the PMS5003 sensor
        :param raw_data: raw data from the serial output
        :param timestamp: float, seconds since epoch in UTC; timestamp of when data was collected
        """
        self.raw_data = raw_data
        self.data = struct.unpack(">HHHHHHHHHHHHHH", raw_data)
        self.checksum = self.data[13]
        if timestamp is None:
            timestamp = time.time()
        self.timestamp = timestamp  # The timestamp in ns

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

    def get_all_pm(self):
        """
        Returns all PM measurements as a list of dicts with keys 'size', 'environment', and 'val' which are the
        particulate matter size recorded by the measurement, the conditions this was calculated under (atmospheric or
        standard) and the actual value of the PM measurement in ug/m^3

        :return: list of dicts of measurements
        """
        vals = [{'size': x, 'environment': y} for y in ['std', 'atm'] for x in [1.0, 2.5, 10.0]]
        return [{k: v for d in (x, {'val': y}) for (k, v) in d.items()} for x, y in zip(vals, self.data)]

    def get_all_counts(self):
        """
        Returns dict mapping size (float) to number (int) of particles beyond that size in 0.1 L of air.
        :return: dict: size -> particle count
        """
        sizes = [0.3, 0.5, 1.0, 2.5, 5.0, 10.0]
        return {s: v for s, v in zip(sizes, self.data[6:])}

    def as_influxdb_line_proto(self, meas_name='pms5003', timestamp=True):
        """
        Get the data in the form of influxDB line protocol

        :param meas_name: str, the name of the measurement as will show up in influxdb
        :param timestamp: bool, include timestamp in the output or not
        :return: str: the formatted data
        """
        ret = ["{name},size={size},environment={environment} pm={val}u".format(name=meas_name, **x) for x in
               self.get_all_pm()]
        ret.extend(["{},size={} count={}u".format(meas_name, s, c) for s, c in self.get_all_counts().items()])
        if timestamp:
            ret = ["{} {}".format(x, int(1e9 * self.timestamp)) for x in ret]
        return '\n'.join(ret)

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

    def __iter__(self):
        """
        Iterator allows conversion of data object into dict for direct access. IE call d = dict(data)
        :return:
        """
        for x in self.get_all_pm():
            yield "pm{:.1f}_{:s}".format(x['size'], x['environment']), x['val']
        for size, count in self.get_all_counts().items():
            yield "count_{:.1f}".format(size), count


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

        sof_index = 0

        while True:
            elapsed = time.time() - start
            if elapsed > 5:
                raise ReadTimeoutError("PMS5003 Read Timeout: Could not find start of frame")

            sof = self._serial.read(1)
            if len(sof) == 0:
                raise SerialTimeoutError("PMS5003 Read Timeout: Failed to read start of frame byte")
            sof = ord(sof) if type(sof) is bytes else sof

            if sof == PMS5003_SOF[sof_index]:
                if sof_index == 0:
                    sof_index = 1
                elif sof_index == 1:
                    break
            else:
                sof_index = 0

        checksum = sum(PMS5003_SOF)

        data = bytearray(self._serial.read(2))  # Get frame length packet
        if len(data) != 2:
            raise SerialTimeoutError("PMS5003 Read Timeout: Could not find length packet")
        checksum += sum(data)
        frame_length = struct.unpack(">H", data)[0]

        raw_data = bytearray(self._serial.read(frame_length))
        if len(raw_data) != frame_length:
            raise SerialTimeoutError("PMS5003 Read Timeout: Invalid frame length. Got {} bytes, expected {}.".format(len(raw_data), frame_length))

        data = PMS5003Data(raw_data)
        # Don't include the checksum bytes in the checksum calculation
        checksum += sum(raw_data[:-2])

        if checksum != data.checksum:
            raise ChecksumMismatchError("PMS5003 Checksum Mismatch {} != {}".format(checksum, data.checksum))

        return data
