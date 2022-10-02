# SPDX-FileCopyrightText: Copyright (c) 2022 Jan Delgado
# SPDX-License-Identifier: MIT
"""
JLead pulse effect example
"""

import board
from jled import JLed

led1 = JLed(board.GP2).breathe(2000).min_brightness(20).delay_after(1000).forever()
led2 = (
    JLed(board.GP3)
    .breathe(2000)
    .delay_before(1000)
    .min_brightness(20)
    .delay_after(1000)
    .forever()
)
led3 = (
    JLed(board.GP4)
    .breathe(2000)
    .delay_before(2000)
    .min_brightness(20)
    .delay_after(1000)
    .forever()
)

while True:
    led1.update()
    led2.update()
    led3.update()
