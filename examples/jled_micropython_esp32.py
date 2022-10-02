# SPDX-FileCopyrightText: Copyright (c) 2022 Jan Delgado
# SPDX-License-Identifier: MIT
"""
JLed MicroPython example. MicroPython has no board/pin abstraction and
LED pins are simply addressed numerically.
"""

from jled import JLed

led = JLed(2).fade_on(1000).delay_after(500).forever()

while True:
    led.update()
