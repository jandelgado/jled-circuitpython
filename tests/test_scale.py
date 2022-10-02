# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Jan Delgado
#
# SPDX-License-Identifier: MIT

# pylint: disable=protected-access
# pylint: disable=misplaced-comparison-constant
# pylint: disable=invalid-name

import pytest
from jled.jled import scale8


@pytest.mark.parametrize(
    "a,factor,,expected",
    [
        (0, 0, 0),
        (255, 0, 0),
        (0, 255, 0),
        (255, 255, 255),
        (128, 255, 128),
        (255, 128, 128),
    ],
)
def test_scale8_scale_byte_by_byte(a, factor, expected):
    assert scale8(a, factor) == expected
