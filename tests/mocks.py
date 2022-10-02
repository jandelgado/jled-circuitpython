# run tests with pytest --cov=jled tests/

# pylint: disable=protected-access
# pylint: disable=misplaced-comparison-constant
# pylint: disable=invalid-name


class MockPWMHAL:
    def __init__(self, pin):
        self._pin = pin
        self._val = -1
        self._count = 0

    def analog_write(self, val):
        self._val = val
        self._count += 1

    def deinit(self):
        self._pin = None

    @property
    def pin(self):
        return self._pin

    @property
    def val(self):
        return self._val

    @property
    def count_called(self):
        return self._count


class MockTimeHAL:
    _time = 0

    @staticmethod
    def tick():
        MockTimeHAL._time += 1

    @staticmethod
    def reset():
        MockTimeHAL.set(0)
        return MockTimeHAL

    @staticmethod
    def set(time):
        MockTimeHAL._time = time
        return MockTimeHAL

    @staticmethod
    def millis():
        return MockTimeHAL._time

    @staticmethod
    def ticks_add(ticks, delta):
        return ticks + delta

    @staticmethod
    def ticks_diff(ticks1, ticks2):
        return ticks1 - ticks2

    @staticmethod
    def ticks_less(ticks1, ticks2):
        "Return true iff ticks1 is less than ticks2, assuming that they are within 2**28 ticks"
        return MockTimeHAL.ticks_diff(ticks1, ticks2) < 0


class MockEffect:
    def __init__(self, values):
        self._values = values

    def period(self):
        return len(self._values)

    def eval(self, t):
        return self._values[t]
