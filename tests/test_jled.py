# run tests with pytest --cov=jled tests/

# pylint: disable=protected-access
# pylint: disable=misplaced-comparison-constant
# pylint: disable=invalid-name

import pytest

from jled.jled import JLed
from jled.jled import _ConstantBrightnessEval
from jled.jled import _BlinkBrightnessEval
from jled.jled import _BreatheBrightnessEval
from jled.jled import _CandleBrightnessEval
from .mocks import MockPWMHAL, MockTimeHAL, MockEffect

JLed._DEFAULT_PWM_HAL = MockPWMHAL
JLed._TIME_HAL = MockTimeHAL


def test_constant_brightness_eval_returns_configured_brightness():
    fx = _ConstantBrightnessEval(10, 20)
    assert 10 == fx.eval(0)
    assert 20 == fx.period()


def test_blink_brightness_eval_blinks_in_given_times():
    fx = _BlinkBrightnessEval(10, 20)

    assert 30 == fx.period()
    assert 255 == fx.eval(0)
    assert 255 == fx.eval(9)
    assert 0 == fx.eval(10)
    assert 0 == fx.eval(19)


def test_breathe_brightness_evalulates_curve():
    fx = _BreatheBrightnessEval(10, 20, 30)

    assert 10 + 20 + 30 == fx.period()
    assert 0 == fx.eval(0)
    assert 0 < fx.eval(9)
    assert 255 == fx.eval(10)
    assert 255 == fx.eval(30)
    assert 0 < fx.eval(31)
    assert 0 == fx.eval(59)
    assert 0 == fx.eval(100)


def test_candle_brightness_evalulater():
    fx = _CandleBrightnessEval(6, 15, 10000)

    assert 10000 == fx.period()
    assert 5 == fx.eval(0)
    # assert 255 == fx.eval(100)    # TODO need injected rand() for that


def test_jled_init_passes_pin_to_hal():
    led = JLed(99)
    assert 99 == led._hal.pin


def test_jled_init_needs_hal_or_pin():
    with pytest.raises(ValueError):
        _ = JLed()

    with pytest.raises(ValueError):
        _ = JLed(hal=None, pin=None)


def test_write_value_to_hal():
    led = JLed(1)
    led._write(123)
    assert 123 == led._hal.val


def test_write_value_to_hal_is_inverted_on_low_active_led():
    led = JLed(1).low_active()
    led._write(0)
    assert 255 == led._hal.val


def test_update_returns_false_if_no_effect_is_set():
    led = JLed(1)
    assert not led.update()


def test_update_has_no_effect_when_called_during_the_same_tick():
    fx = MockEffect([10, 20, 30])
    led = JLed(1).user_func(fx)

    led.update()
    led.update()
    led.update()

    assert 1 == led._hal.count_called
    assert 10 == led._hal.val


def test_update_writes_values_of_effect():
    t = JLed._TIME_HAL.reset()
    fx = MockEffect([1, 2, 3])
    led = JLed(1).user_func(fx)

    led.update()
    assert 1 == led._hal.val
    t.tick()
    led.update()
    assert 2 == led._hal.val
    t.tick()
    led.update()
    assert 3 == led._hal.val


def test_update_returns_true_as_long_as_effect_is_active():
    t = JLed._TIME_HAL.reset()
    fx = MockEffect([255, 0])
    led = JLed(1).user_func(fx)

    assert led.update()
    assert 255 == led._hal.val

    t.tick()
    assert not led.update()
    assert 0 == led._hal.val


def test_delay_before_delays_effect_start():
    t = JLed._TIME_HAL.reset()
    fx = MockEffect([255])
    led = JLed(1).user_func(fx).delay_before(1)

    assert led.update()
    assert -1 == led._hal.val  # -1 = nothing written yet

    t.tick()
    assert not led.update()
    assert 255 == led._hal.val


def test_delay_after_delays_effect_end():
    t = JLed._TIME_HAL.reset()
    fx = MockEffect([255])
    led = JLed(1).user_func(fx).delay_after(1)

    assert led.update()
    assert 255 == led._hal.val

    t.tick()
    assert not led.update()
    assert 255 == led._hal.val


def test_repeat_effect_multiple_times():
    t = JLed._TIME_HAL.reset()
    fx = MockEffect([255, 0])
    led = JLed(1).user_func(fx).repeat(2)

    assert led.update()
    assert 255 == led._hal.val
    t.tick()
    assert led.update()
    assert 0 == led._hal.val
    t.tick()
    assert led.update()
    assert 255 == led._hal.val
    t.tick()
    assert not led.update()
    assert 0 == led._hal.val


def test_forever_runs_effect_multiple_times():
    t = JLed._TIME_HAL.reset()
    fx = MockEffect([255, 0])
    led = JLed(1).user_func(fx).forever()

    for _ in range(100):
        assert led.update()
        assert 255 == led._hal.val
        t.tick()
        assert led.update()
        assert 0 == led._hal.val
        t.tick()


def test_after_stop_is_called_update_returns_false_and_set_brightness_to_zero():
    fx = MockEffect([255, 255, 255])
    led = JLed(1).user_func(fx)

    assert led.update()
    assert 255 == led._hal.val

    led.stop()
    assert not led.update()
    assert 0 == led._hal.val


def test_is_running_returns_true_only_when_effect_is_running():
    fx = MockEffect([255])
    led = JLed(1).user_func(fx)

    assert led.is_running
    led.update()
    assert not led.is_running


def test_reset_starts_led_again():
    t = JLed._TIME_HAL.reset()
    fx = MockEffect([10, 20])
    led = JLed(1).user_func(fx)

    assert led.update()
    assert 10 == led._hal.val
    t.tick()
    assert not led.update()
    assert 20 == led._hal.val
    led.reset()
    t.tick()
    assert led.update()
    assert 10 == led._hal.val
    t.tick()
    assert not led.update()
    assert 20 == led._hal.val


def test_jled_deinit_de_initializes_hal():
    led = JLed(1)
    assert led._hal.pin is not None

    led.deinit()
    assert led._hal.pin is None


def test_on_sets_constant_brightness_eval_to_255():
    led = JLed(1).on(10)
    assert isinstance(led._brightness_eval, _ConstantBrightnessEval)
    assert led._brightness_eval.__dict__ == _ConstantBrightnessEval(255, 10).__dict__


def test_off_sets_constant_brightness_eval_to_0():
    led = JLed(1).off(10)
    assert isinstance(led._brightness_eval, _ConstantBrightnessEval)
    assert led._brightness_eval.__dict__ == _ConstantBrightnessEval(0, 10).__dict__


def test_set_sets_constant_brightness_eval_to_given_value():
    led = JLed(1).set(99, 10)
    assert isinstance(led._brightness_eval, _ConstantBrightnessEval)
    assert led._brightness_eval.__dict__ == _ConstantBrightnessEval(99, 10).__dict__


def test_candle_sets_constant_brightness_eval_to_given_value():
    led = JLed(1).candle(1, 2, 3)
    assert isinstance(led._brightness_eval, _CandleBrightnessEval)
    assert led._brightness_eval.__dict__ == _CandleBrightnessEval(1, 2, 3).__dict__


def test_blink_sets_blink_brightness_eval():
    led = JLed(1).blink(1, 2)
    assert isinstance(led._brightness_eval, _BlinkBrightnessEval)
    assert led._brightness_eval.__dict__ == _BlinkBrightnessEval(1, 2).__dict__


def test_breathe_with_custom_params_sets_breathe_brightness_eval():
    led = JLed(1).breathe(100, 200, 300)
    assert isinstance(led._brightness_eval, _BreatheBrightnessEval)
    assert (
        _BreatheBrightnessEval(100, 200, 300).__dict__ == led._brightness_eval.__dict__
    )


def test_breathe_sets_breathe_brightness_eval():
    led = JLed(1).breathe(100)
    assert isinstance(led._brightness_eval, _BreatheBrightnessEval)
    assert _BreatheBrightnessEval(50, 0, 50).__dict__ == led._brightness_eval.__dict__


def test_fadeon_sets_breathe_brightness_eval():
    led = JLed(1).fade_on(100)
    assert isinstance(led._brightness_eval, _BreatheBrightnessEval)
    assert _BreatheBrightnessEval(100, 0, 0).__dict__ == led._brightness_eval.__dict__


def test_fadeoff_sets_breathe_brightness_eval():
    led = JLed(1).fade_off(100)
    assert isinstance(led._brightness_eval, _BreatheBrightnessEval)
    assert _BreatheBrightnessEval(0, 0, 100).__dict__ == led._brightness_eval.__dict__


def test_fade_from_low_to_high_sets_breathe_brightness_eval_and_brightness():
    led = JLed(1).fade(start=100, end=200, period=300)
    assert isinstance(led._brightness_eval, _BreatheBrightnessEval)
    assert _BreatheBrightnessEval(300, 0, 0).__dict__ == led._brightness_eval.__dict__
    assert 100 == led._min_brightness
    assert 200 == led._max_brightness


def test_fade_from_high_to_low_sets_breathe_brightness_eval_and_brightness():
    led = JLed(1).fade(start=200, end=100, period=300)
    assert isinstance(led._brightness_eval, _BreatheBrightnessEval)
    assert _BreatheBrightnessEval(0, 0, 300).__dict__ == led._brightness_eval.__dict__
    assert 100 == led._min_brightness
    assert 200 == led._max_brightness
