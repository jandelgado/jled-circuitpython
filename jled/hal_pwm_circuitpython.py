# SPDX-FileCopyrightText: Copyright (c) 2022 Jan Delgado
# SPDX-License-Identifier: MIT
"""
`jled`
================================================================================

Non-blocking LED controlling library

A pure python port of https://github.com/jandelgado/jled

* Author(s): Jan Delgado

"""

import pwmio


class CircuitPythonPWMHAL:
    """a JLed PWM HAL for CircuitPyhton"""

    _leds = {}

    def __init__(self, pin, frequency=5000):

        self._pin = pin
        # PWM instances are shared among JLed instances to be able
        # to instanciate multiple JLed objects using the same PWM. We need
        # to use str(pin) as the key because pin might not be hashable
        if not str(pin) in CircuitPythonPWMHAL._leds:
            led = pwmio.PWMOut(pin, frequency=frequency, duty_cycle=0)
            CircuitPythonPWMHAL._leds[str(pin)] = led

    def analog_write(self, duty):
        """write duty (0..255) to PWM port controlled by this HAL"""
        # scale JLed 8bit accuracy to 16bit, preserving min/max
        self._led.duty_cycle = 0 if duty == 0 else (duty << 8) | 0xFF

    @property
    def _led(self):
        return CircuitPythonPWMHAL._leds[str(self._pin)]

    def deinit(self):
        self._led.deinit()
        del CircuitPythonPWMHAL._leds[str(self._pin)]
