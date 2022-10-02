# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Jan Delgado
#
# SPDX-License-Identifier: MIT

# pylint: disable=protected-access
# pylint: disable=misplaced-comparison-constant
# pylint: disable=invalid-name

import pytest
from jled.jled import fadeon_func


@pytest.mark.parametrize(
    "t,expected",
    [
        (0, 0),
        (500, 13),
        (1000, 68),
        (1500, 179),
        (1999, 255),
        (2000, 255),
        (10000, 255),
    ],
)
# pylint: disable=invalid-name
def test_fadeon_func_calculates_expected_curve_for_period_2000(t, expected):
    assert fadeon_func(t, 2000) == expected
