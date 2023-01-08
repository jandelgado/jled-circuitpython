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


class PythonPWMHAL:
    """a JLed PWM HAL for Phyton for debugging and testing"""

    def __init__(self, pin):
        self._pin = pin

    def analog_write(self, duty):
        """the debug HAL prints the duty that would be written to stdout"""
        print("led on", self._pin, " => ", duty)

    def deinit(self):
        pass
