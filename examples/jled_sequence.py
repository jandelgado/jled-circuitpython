# SPDX-FileCopyrightText: Copyright (c) 2022 Jan Delgado
# SPDX-License-Identifier: MIT
"""
drive multiple LEDs using different effects with a JLedSequence
"""

import board
from jled import JLed, JLedSequence

led0 = JLed(board.LED).breathe(750).delay_after(250).forever()
led1 = JLed(board.GP2).blink(500, 250).delay_after(250).forever()
led2 = JLed(board.GP3).fade_off(1000).delay_after(500).forever()
led3 = JLed(board.GP4).fade_on(1500).forever()

seq = JLedSequence.parallel([led0, led1, led2, led3])

while True:
    seq.update()
