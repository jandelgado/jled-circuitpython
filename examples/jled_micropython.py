# SPDX-FileCopyrightText: Copyright (c) 2022 Jan Delgado
# SPDX-License-Identifier: MIT
"""
JLead pulse effect example (micropython)
"""

from jled import JLed

led1 = JLed(18).breathe(1000).min_brightness(20).delay_before(500).forever()
led2 = JLed(23).breathe(1000).min_brightness(20).forever()

while True:
    led1.update()
    led2.update()
