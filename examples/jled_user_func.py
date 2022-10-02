# SPDX-FileCopyrightText: Copyright (c) 2022 Jan Delgado
# SPDX-License-Identifier: MIT
"""
JLed User defined effect example
"""

import board
from jled import JLed


class UserEffect:
    def __init__(self, period):
        self._period = period

    def eval(self, t):
        """this function returns changes between 0 and 255 and
        vice versa every period/2 ms"""
        return 255 * ((t // (self._period >> 1)) & 1)

    def period(self):
        return self._period


led = JLed(board.LED).user_func(UserEffect(1000)).forever()

while True:
    led.update()
