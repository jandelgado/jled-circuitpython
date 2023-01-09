# SPDX-FileCopyrightText: Copyright (c) 2022 Jan Delgado
# SPDX-License-Identifier: MIT
"""expose JLed classes and set default HALs to use"""

from .jled import JLed
from .jled_sequence import JLedSequence
from .play import play

try:
    # running on CircuitPython?
    from .hal_pwm_circuitpython import CircuitPythonPWMHAL as _PWMHAL

    try:
        from .hal_time_circuitpython import CircuitPythonTimeHAL as _TimeHAL
    except ImportError:
        # when running circuit python on raspi with adafruit blinka, the
        # supervisor module is not available
        from .python_time_hal import PythonTimeHAL as _TimeHAL

except ImportError:
    try:
        # running on MicroPython?
        import machine
        from .hal_pwm_micropython import MicroPythonPWMHAL as _PWMHAL
        from .hal_time_micropython import MicroPythonTimeHAL as _TimeHAL

    except ImportError:
        from .python_pwm_hal import PythonPWMHAL as _PWMHAL
        from .python_time_hal import PythonTimeHAL as _TimeHAL

JLed._DEFAULT_PWM_HAL = _PWMHAL  # pylint: disable=protected-access
JLed._TIME_HAL = _TimeHAL  # pylint: disable=protected-access
