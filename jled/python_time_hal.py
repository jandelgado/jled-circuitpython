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


class PythonTimeHAL:
    """a JLed Time HAL for Pyhton"""

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
        return PythonTimeHAL.ticks_diff(ticks1, ticks2) < 0
