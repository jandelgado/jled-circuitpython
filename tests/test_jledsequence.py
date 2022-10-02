# run tests with pytest --cov=jled tests/

# pylint: disable=protected-access
# pylint: disable=misplaced-comparison-constant
# pylint: disable=invalid-name

import pytest
from jled.jled import JLed
from jled.jled_sequence import JLedSequence
from .mocks import MockPWMHAL, MockTimeHAL, MockEffect

JLed._DEFAULT_PWM_HAL = MockPWMHAL
JLed._TIME_HAL = MockTimeHAL


def test_jled_sequence_updates_leds_parallel():
    t = JLed._TIME_HAL.reset()
    fx1 = MockEffect([10, 20])
    led1 = JLed(1).user_func(fx1)
    fx2 = MockEffect([30, 40])
    led2 = JLed(2).user_func(fx2)
    seq = JLedSequence.parallel([led1, led2])

    assert seq.update()
    assert 10 == led1._hal.val
    assert 30 == led2._hal.val

    t.tick()
    assert not seq.update()
    assert 20 == led1._hal.val
    assert 40 == led2._hal.val


def test_jled_sequence_updates_leds_sequentially():
    t = JLed._TIME_HAL.reset()
    fx1 = MockEffect([10, 20])
    led1 = JLed(1).user_func(fx1)
    fx2 = MockEffect([30, 40])
    led2 = JLed(2).user_func(fx2)
    seq = JLedSequence.sequential([led1, led2])

    assert seq.update()
    assert 10 == led1._hal.val
    assert -1 == led2._hal.val

    t.tick()
    assert seq.update()
    assert 20 == led1._hal.val
    assert -1 == led2._hal.val

    t.tick()
    assert seq.update()
    assert 20 == led1._hal.val
    assert 30 == led2._hal.val

    t.tick()
    assert not seq.update()
    assert 20 == led1._hal.val
    assert 40 == led2._hal.val


def test_jledsequence_reset_resets_all_leds_and_the_sequence():
    fx = MockEffect([255])
    led = JLed(1).user_func(fx)
    seq = JLedSequence.parallel([led])

    assert not seq.update()
    assert not seq.is_running
    assert not led.is_running

    seq.reset()
    assert seq.is_running
    assert led.is_running


def test_jledsequence_update_resets_all_leds_after_each_iteration():
    t = JLed._TIME_HAL.reset()
    fx = MockEffect([255])
    led = JLed(1).user_func(fx)
    seq = JLedSequence.parallel([led]).repeat(2)

    assert seq.update()
    assert seq.is_running
    assert led.is_running

    t.tick()

    assert not seq.update()
    assert not seq.is_running
    assert not led.is_running


@pytest.mark.parametrize("seqinit", [JLedSequence.parallel, JLedSequence.sequential])
def test_jledsequence_is_running_returns_true_only_when_effect_is_running(seqinit):
    fx = MockEffect([255])
    led = JLed(1).user_func(fx)
    seq = seqinit([led])

    assert seq.is_running
    seq.update()
    assert not seq.is_running


def test_jledsequence_accepts_recursive_sequence():
    t = JLed._TIME_HAL.reset()
    fx = MockEffect([255])
    led = JLed(1).user_func(fx)
    seq1 = JLedSequence.parallel([led])
    seq2 = JLedSequence.parallel([seq1]).repeat(2)

    seq2.update()
    assert led.is_running
    assert seq1.is_running
    assert seq2.is_running

    _ = t.tick
    seq2.update()
    assert not led.is_running
    assert not seq1.is_running
    assert not seq2.is_running


def test_jledsequence_stop_stops_all_leds():
    fx = MockEffect([255, 255])
    led = JLed(1).user_func(fx)
    seq = JLedSequence.parallel([led])

    seq.update()
    assert 255 == led._hal.val

    seq.stop()
    assert 0 == led._hal.val
    seq.update()
    assert not seq.is_running
