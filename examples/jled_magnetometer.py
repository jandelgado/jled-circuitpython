# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
# SPDX-License-Identifier: MIT
"""
JLed example using a led to display how close is a magnetometer
"""
import time
import board
import adafruit_lis3mdl
from jled import JLed

### Magnetometer Sensor Setup
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_lis3mdl.LIS3MDL(i2c)
# Limit Values from the Magnetometer sensor in the Z direction
rmin = -60
rmax = -478

# Setup of the JLed Object
led = JLed(board.A1).set(12)

while True:
    _, _, mag_z = sensor.magnetic
    # We correct the sensor value to work with the LED Brightness
    corrected = max(0, int(((mag_z - rmin) / (rmax - rmin)) * 255))
    led.set(corrected)
    led.update()
    time.sleep(0.2)
