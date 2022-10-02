# SPDX-FileCopyrightText: Copyright (c) 2022 Jan Delgado
# SPDX-License-Identifier: MIT
"""
JLead breathe example
"""

import board
from jled import JLed

led = JLed(board.LED).breathe(1000).delay_after(500).forever()

while True:
    led.update()
