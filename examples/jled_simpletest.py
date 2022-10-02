# SPDX-FileCopyrightText: Copyright (c) 2022 Jan Delgado
# SPDX-License-Identifier: MIT
"""
JLed Hello world
"""

import board
from jled import JLed

led = JLed(board.LED).blink(500, 500).forever()

while True:
    led.update()
