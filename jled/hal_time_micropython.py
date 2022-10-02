# SPDX-FileCopyrightText: Copyright (c) 2022 Jan Delgado
# SPDX-License-Identifier: MIT
"""
`jled`
================================================================================

Non-blocking LED controlling library

A pure python port of https://github.com/jandelgado/jled

* Author(s): Jan Delgado

HAL example for MicoPython and the ESP32

"""

# pylint: disable=no-member
import time


class MicroPythonTimeHAL:
    """a JLed Time HAL for CircuitPyhton"""

    @staticmethod
    def millis():
        """return current time in milliseconds"""
        return time.ticks_ms()

    @staticmethod
    def ticks_add(ticks, delta):
        return time.ticks_add(ticks, delta)

    @staticmethod
    def ticks_diff(ticks1, ticks2):
        return time.ticks_diff(ticks1, ticks2)

    @staticmethod
    def ticks_less(ticks1, ticks2):
        "Return true iff ticks1 is less than ticks2, assuming that they are within 2**28 ticks"
        return time.ticks_diff(ticks1, ticks2) < 0
