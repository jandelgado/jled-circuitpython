# SPDX-FileCopyrightText: Copyright (c) 2022 Jan Delgado
# SPDX-License-Identifier: MIT
"""expose JLed classes and set default HALs to use"""

from .jled import JLed
from .jled_sequence import JLedSequence
from .play import play

__all__ = ["JLed", "JLedSequence", "play"]

try:
    # running on CircuitPython?
    from .hal_pwm_circuitpython import CircuitPython_PWMHAL as _PWMHAL
    from .hal_time_circuitpython import CircuitPython_TimeHAL as _TimeHAL
except ImportError:
    try:
        # running on MicroPython?
        import machine
        from .hal_time_micropython import MicroPython_TimeHAL as _TimeHAL
        from .hal_pwm_micropython import MicroPython_PWMHAL as _PWMHAL

    except ImportError:
        from .hal_debug import PythonHAL as _PWMHAL
        from .hal_debug import PythonHAL as _TimeHAL

JLed._DEFAULT_PWM_HAL = _PWMHAL  # pylint: disable=protected-access
JLed._TIME_HAL = _TimeHAL  # pylint: disable=protected-access
