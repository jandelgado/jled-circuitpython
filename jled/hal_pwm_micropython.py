# SPDX-FileCopyrightText: Copyright (c) 2022 Jan Delgado
# SPDX-License-Identifier: MIT
"""
`jled`
================================================================================

Non-blocking LED controlling library

A pure python port of https://github.com/jandelgado/jled

* Author(s): Jan Delgado

HAL for MicoPython
"""

from machine import Pin, PWM


def _scale8to16(val):
    return 0 if val == 0 else (val << 8) | 255


class MicroPythonPWMHAL:
    """a JLed HAL for MicroPyhton"""

    def __init__(self, pin, frequency=1000):
        self._pwm = PWM(Pin(pin), freq=frequency, duty=0)

    def analog_write(self, duty):
        """write duty (0..255) to PWM port controlled by this HAL"""
        # scale JLed 8bit accuracy to 16bit, preserving min/max
        self._pwm.duty_u16(_scale8to16(duty))

    def deinit(self):
        self._pwm.deinit()
        self._pwm = None
