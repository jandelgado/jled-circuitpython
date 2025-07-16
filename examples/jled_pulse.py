# SPDX-FileCopyrightText: Copyright (c) 2025 Jan Delgado
# SPDX-License-Identifier: MIT
"""
JLed pulse example
"""

import board
from jled import JLed

led = JLed(board.LED).breathe(2000).min_brightness(20).max_brightness(200).forever()

while True:
    led.update()