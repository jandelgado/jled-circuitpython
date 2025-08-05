import pytest

from jled.jled import lerp16by16


@pytest.mark.parametrize(
    "val,a,b,expected",
    [
        (0, 0, 65535, 0),
        (65535, 0, 0, 0),
        (65535, 0, 65535, 65535),
        (0, 10000, 65535, 10000),
        (0, 10000, 11000, 10000),
        (65535, 10000, 65535, 65535),
        (65535, 10000, 20000, 20000),
    ],
)
def test_lerp8by8_interpolations_a_byte_into_the_given_interval(val, a, b, expected):
    assert expected == lerp16by16(val, a, b)
