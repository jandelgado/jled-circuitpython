# SPDX-FileCopyrightText: Copyright (c) 2022 Jan Delgado
# SPDX-License-Identifier: MIT
"""
`jled`
================================================================================

Non-blocking LED controlling library

A pure python port of https://github.com/jandelgado/jled

* Author(s): Jan Delgado

"""

from supervisor import ticks_ms

# see https://docs.circuitpython.org/en/latest/docs/design_guide.html#use-of-micropython-const
from micropython import const

# don't change values
# pylint: disable=undefined-variable
_TICKS_PERIOD = const(1 << 29)  # must be power of 2
_TICKS_MAX = const(_TICKS_PERIOD - 1)
_TICKS_HALFPERIOD = const(_TICKS_PERIOD // 2)


class CircuitPythonTimeHAL:
    """a JLed Time HAL for CircuitPyhton"""

    @staticmethod
    def millis():
        # pylint: disable=line-too-long
        """return current time in milliseconds

        see  https://docs.circuitpython.org/en/latest/shared-bindings/supervisor/index.html#supervisor.ticks_ms:

         "Return the time in milliseconds since an unspecified reference
          point, wrapping after 2**29ms."

         for the different time functions available in CirctuitPython, see
         see https://docs.circuitpython.org/en/latest/shared-bindings/time"""
        return ticks_ms()

    @staticmethod
    def ticks_add(ticks, delta):
        """Add a delta to a base number of ticks, performing wraparound at
        2**29ms.  Note that for any a = (2^n)-1, (b%a == b&a), which spares
        us the modulo operation."""
        return (ticks + delta) & _TICKS_MAX

    @staticmethod
    def ticks_diff(ticks1, ticks2):
        """Compute the signed difference between two ticks values, assuming
        that they are within 2**28 ticks"""
        diff = (ticks1 - ticks2) & _TICKS_MAX
        diff = ((diff + _TICKS_HALFPERIOD) & _TICKS_MAX) - _TICKS_HALFPERIOD
        return diff

    @staticmethod
    def ticks_less(ticks1, ticks2):
        """Return true iff ticks1 is less than ticks2, assuming that they are within 2**28 ticks"""
        return CircuitPythonTimeHAL.ticks_diff(ticks1, ticks2) < 0
