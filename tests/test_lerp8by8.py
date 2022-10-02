import pytest

from jled.jled import lerp8by8

# pylint: disable=protected-access
# pylint: disable=misplaced-comparison-constant
# pylint: disable=invalid-name


@pytest.mark.parametrize(
    "val,a,b,expected",
    [
        (0, 0, 255, 0),
        (255, 0, 0, 0),
        (255, 0, 255, 255),
        (0, 100, 255, 100),
        (0, 100, 110, 100),
        (255, 100, 255, 255),
        (255, 100, 200, 200),
    ],
)
# pylint: disable=invalid-name
def test_lerp8by8_interpolations_a_byte_into_the_given_interval(val, a, b, expected):
    assert expected == lerp8by8(val, a, b)
