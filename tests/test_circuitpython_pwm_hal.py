import sys
import types

# pylint: disable=protected-access
# pylint: disable=misplaced-comparison-constant
# pylint: disable=invalid-name

# provide mocked mocked version of machine.PWM and machine.Pin to
# be used during the tests
class MockPWMOut:
    def __init__(self, pin, frequency, duty_cycle):
        self._pin = pin
        self._freq = frequency
        self._duty = duty_cycle
        self._val = -1
        self._deinit = False

    @property
    def duty_cycle(self):
        return self._val

    @duty_cycle.setter
    def duty_cycle(self, val):
        self._val = val

    def deinit(self):
        self._deinit = True


module_name = "pwmio"
module = types.ModuleType(module_name)
module.PWMOut = MockPWMOut
sys.modules[module_name] = module

# pylint: disable=wrong-import-position
from jled.hal_pwm_circuitpython import CircuitPythonPWMHAL


def test_circuitpython_hal_initializes_pwmout_corretly():
    hal = CircuitPythonPWMHAL(123, frequency=500)
    assert 500 == hal._led._freq
    assert 123 == hal._pin


def test_circuitpython_hal_reuses_pwmout_on_same_pin():
    hal1 = CircuitPythonPWMHAL(123, frequency=500)
    hal2 = CircuitPythonPWMHAL(123, frequency=500)

    assert id(hal1._led) == id(hal2._led)


def test_circuitpython_hal_writes_scaled_value():
    hal = CircuitPythonPWMHAL(123)

    hal.analog_write(0)
    assert 0 == hal._led._val

    hal.analog_write(255)
    assert 0xFFFF == hal._led._val


def test_circuitpython_hal_deinit_deinitialzes_underlying_hal():
    # given
    hal = CircuitPythonPWMHAL(123)

    # when
    savedled = hal._leds[str(123)]
    hal.deinit()

    # then deinit() was called and _
    assert savedled._deinit
    assert str(123) not in hal._leds
