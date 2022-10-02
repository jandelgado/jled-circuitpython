# SPDX-FileCopyrightText: Copyright (c) 2022 Jan Delgado
# SPDX-License-Identifier: MIT
"""
`jled`
================================================================================

Non-blocking LED controlling library

A pure python port of https://github.com/jandelgado/jled

* Author(s): Jan Delgado

"""

import time


class PythonHAL:
    """a JLed PWM and Time HAL for CPyhton for debugging and testing"""

    def __init__(self, pin):
        self._pin = pin

    def analog_write(self, duty):
        """the debug HAL prints the duty that would be written to stdout"""
        print("led on", self._pin, " => ", duty)

    @staticmethod
    def millis():
        """return current time in millis"""
        return time.monotonic_ns() // 1_000_000

    @staticmethod
    def ticks_add(ticks, delta):
        return ticks + delta

    @staticmethod
    def ticks_diff(ticks1, ticks2):
        return ticks1 - ticks2

    @staticmethod
    def ticks_less(ticks1, ticks2):
        return PythonHAL.ticks_diff(ticks1, ticks2) < 0

    def deinit(self):
        pass
