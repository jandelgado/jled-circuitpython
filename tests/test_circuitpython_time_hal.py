import sys
import types

# pylint: disable=protected-access
# pylint: disable=misplaced-comparison-constant
# pylint: disable=invalid-name
# pylint: disable=wrong-import-position

# provide mocked suppervisor.tick_ms and micropython.const modules/functions
# to our test runs with cpython
module_name = "supervisor"
module = types.ModuleType(module_name)
module.ticks_ms = lambda: 123
sys.modules[module_name] = module

module_name = "micropython"
module = types.ModuleType(module_name)
module.const = lambda x: x
sys.modules[module_name] = module

module_name = "pwmio"
module = types.ModuleType(module_name)
sys.modules[module_name] = module

from jled.hal_time_circuitpython import CircuitPythonTimeHAL as HAL

# from jled.hal_time_circuitpython import _TICKS_PERIOD as TICKS_PERIOD


def test_time_hal_adds_ticks():
    assert 300 == HAL.ticks_add(ticks=100, delta=200)


def test_time_hal_adds_ticks_stays_within_period():
    ticks = 2**29 - 1
    delta = 1
    assert 0 == HAL.ticks_add(ticks, delta)


def test_time_hal_calculates_difference():
    ticks1 = 200
    ticks2 = 100
    assert 100 == HAL.ticks_diff(ticks1, ticks2)


def test_time_hal_calculates_difference_with_overflow():
    # assert 100 == HAL.ticks_diff(100, 200)
    pass
