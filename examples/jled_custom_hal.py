# SPDX-FileCopyrightText: Copyright (c) 2022 Jan Delgado
# SPDX-License-Identifier: MIT
"""
JLed custom HAL example. This example drives a LED with a PCA9685 using the
https://pypi.org/project/adafruit-circuitpython-pca9685/ library.
"""

from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from jled import JLed

#  i2c_bus = busio.I2C(SCL, SDA)
#  pca = PCA9685(i2c_bus)
#  pca.frequency = 60


class PCA9685HAL:
    PCA = PCA9685(busio.I2C(SCL, SDA))
    PCA.frequency = 100

    def __init__(self, pin):
        self._pin = pin

    def analog_write(self, duty):
        # scale JLed 8bit accuracy to 12bit, preserving min/max
        PCA9685HAL.PCA.channels[self._pin] = 0 if duty == 0 else (duty << 4) | 15

    def deinit(self):
        pass


# pylint: disable=too-few-public-methods
class JLedPCA9685(JLed):
    DEFAULT_PWM_HAL = PCA9685HAL


# set the default JLed to use when creating new JLed objects
# JLed.DEFAULT_PWM_HAL = PCA9685HAL

# led1 is connected to the PCA9685, led2 is controlled by a MCU connected PWM
led1 = JLedPCA9685(2).breathe(1000).delay_after(500).forever()
led2 = JLed(2).fade_on(1000).forever()

while True:
    led1.update()
    led2.update()
