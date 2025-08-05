# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Jan Delgado
#
# SPDX-License-Identifier: MIT


import pytest
from jled.jled import scale16


@pytest.mark.parametrize(
    "a,factor,,expected",
    [
        (0, 0, 0),
        (65535, 0, 0),
        (0, 65535, 0),
        (65535, 65535, 65535),
        (32768, 65535, 32768),
        (65535, 32768, 32768),
    ],
)
def test_scale16_scale_word_by_word(a, factor, expected):
    assert scale16(a, factor) == expected
