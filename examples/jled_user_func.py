# SPDX-FileCopyrightText: Copyright (c) 2022 Jan Delgado
# SPDX-License-Identifier: MIT
"""
JLed User defined effect example
"""

import board
from jled import JLed
from jled.jled import FULL_BRIGHTNESS


class UserEffect:
    def __init__(self, period):
        self._period = period

    def eval(self, t):
        """this function changes between 0 and FULL_BRIGHTNESS and
        vice versa every period/2 ms"""
        return FULL_BRIGHTNESS * ((t // (self._period >> 1)) & 1)

    def period(self):
        return self._period


led = JLed(board.LED).user_func(UserEffect(1000)).forever()

while True:
    led.update()
