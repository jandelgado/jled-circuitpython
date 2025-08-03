# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Jan Delgado
#
# SPDX-License-Identifier: MIT


import pytest
from jled.jled import FULL_BRIGHTNESS, fadeon_func


@pytest.mark.parametrize(
    "t,expected",
    [
        (0, 0),
        (500, 3474),
        (1000, 17545),
        (1500, 46081),
        (1999, FULL_BRIGHTNESS),
        (2000, FULL_BRIGHTNESS),
        (10000, FULL_BRIGHTNESS),
    ],
)
def test_fadeon_func_calculates_expected_curve_for_period_2000(t, expected):
    assert fadeon_func(t, 2000) == expected
