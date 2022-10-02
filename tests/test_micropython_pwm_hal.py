import sys
import types

# pylint: disable=protected-access
# pylint: disable=misplaced-comparison-constant
# pylint: disable=invalid-name

# provide mocked mocked version of machine.PWM and machine.Pin to
# be used during the tests
# pylint: disable=too-few-public-methods
class MockPin:
    def __init__(self, num):
        self._num = num


class MockPWM:
    def __init__(self, pin, freq, duty):
        self._pin = pin
        self._freq = freq
        self._duty = duty
        self._val = -1
        self._deinit = False

    def duty_u16(self, val):
        self._val = val

    def deinit(self):
        self._deinit = True


module_name = "machine"
module = types.ModuleType(module_name)
module.PWM = MockPWM
module.Pin = MockPin
sys.modules[module_name] = module

# pylint: disable=wrong-import-position
from jled.hal_pwm_micropython import MicroPythonPWMHAL, _scale8to16


def test_scale8to16_preserves_min_max_relationships():
    assert 0 == _scale8to16(0)
    assert 0xFFFF == _scale8to16(0xFF)


def test_scale8to16_scales():
    assert 0x10FF == _scale8to16(0x10)


def test_micropython_hal_initializes_corretly():
    hal = MicroPythonPWMHAL(123, frequency=500)
    assert 500 == hal._pwm._freq
    assert 0 == hal._pwm._duty


def test_micropython_hal_hal_initializes_right_pin():
    hal = MicroPythonPWMHAL(123)
    assert 123 == hal._pwm._pin._num


def test_micropython_hal_writes_scaled_value():
    hal = MicroPythonPWMHAL(123)

    hal.analog_write(0)
    assert 0 == hal._pwm._val

    hal.analog_write(255)
    assert 0xFFFF == hal._pwm._val


def test_micropython_hal_deinit_deinitialzes_underlying_hal():
    # given
    hal = MicroPythonPWMHAL(123)

    # when
    savedled = hal._pwm
    hal.deinit()

    # then deinit() was called and _pwm is unset
    assert savedled._deinit
    assert None is hal._pwm
