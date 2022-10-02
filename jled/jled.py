# SPDX-FileCopyrightText: Copyright (c) 2022 Jan Delgado
# SPDX-License-Identifier: MIT
#
"""
jled
================================================================================

Non-blocking LED controlling library

A pure python port of JLed (https://github.com/jandelgado/jled)

* Author(s): Jan Delgado

"""

import random

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jandelgado/jled-circuitpython.git"

FULL_BRIGHTNESS = 255
ZERO_BRIGHTNESS = 0


def scale8(a, factor):
    """scale a byte by a byte"""
    return (a * (1 + factor)) >> 8


def lerp8by8(val, a, b):
    """interpolate val to the interval defined by [a,b]. Returns a if val==0
    and b if val==255 or a value in [a,b]"""
    if a == 0 and b == 255:
        return val
    return a + scale8(val, b - a)


def fadeon_func(t, period):
    # pylint: disable=line-too-long
    """The fade-on func is an approximation of
    y(x) = exp(sin((t-period/2.) * PI / period)) - 0.36787944) * 108.), using
    pre-computed values and integers only.

    see https://www.wolframalpha.com/input/?i=plot+(exp(sin((x-100%2F2.)*PI%2F100))-0.36787944)*108.0++x%3D0+to+100
    """

    fadeon_table = [0, 3, 13, 33, 68, 118, 179, 232, 255]

    if t + 1 >= period:
        return FULL_BRIGHTNESS
    t = ((t << 8) // period) & 0xFF
    i = t >> 5
    y0 = fadeon_table[i]
    y1 = fadeon_table[i + 1]
    x0 = i << 5
    return (((t - x0) * (y1 - y0)) >> 5) + y0


class _ConstantBrightnessEval:
    def __init__(self, val, duration=1):
        self._val = val
        self._duration = duration

    def period(self):
        return self._duration

    def eval(self, _):
        return self._val


class _BlinkBrightnessEval:
    def __init__(self, duration_on, duration_off):
        self._duration_on = duration_on
        self._duration_off = duration_off

    def period(self):
        return self._duration_on + self._duration_off

    def eval(self, t):
        return FULL_BRIGHTNESS if t < self._duration_on else ZERO_BRIGHTNESS


class _BreatheBrightnessEval:
    def __init__(self, duration_fade_on, duration_on, duration_fade_off):
        self._duration_fade_on = duration_fade_on
        self._duration_on = duration_on
        self._duration_fade_off = duration_fade_off

    def period(self):
        return self._duration_fade_on + self._duration_on + self._duration_fade_off

    def eval(self, t):
        if t < self._duration_fade_on:
            return fadeon_func(t, self._duration_fade_on)
        if t < self._duration_fade_on + self._duration_on:
            return FULL_BRIGHTNESS
        if t < self.period():
            return fadeon_func(self.period() - t, self._duration_fade_off)
        return ZERO_BRIGHTNESS


class _CandleBrightnessEval:
    _CANDLE_TABLE = [5, 10, 20, 30, 50, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 255]

    def __init__(self, speed, jitter, period):
        self._speed = speed
        self._jitter = jitter
        self._period = period
        self._last = 5
        self._last_t = 0

    def period(self):
        return self._period

    def eval(self, t):
        if t >> self._speed == self._last_t:
            return self._last
        self._last_t = t >> self._speed
        rnd = random.randint(0, 255)
        self._last = (
            FULL_BRIGHTNESS
            if rnd >= self._jitter
            else (50 + self._CANDLE_TABLE[rnd & 0xF])
        )
        return self._last


# pylint: disable=too-many-public-methods
class JLed:
    """JLed class"""

    _REPEAT_FOREVER = -1
    _ST_RUNNING = 0
    _ST_INIT = 1
    _ST_STOPPED = 2
    _ST_IN_DELAY_AFTER_PHASE = 3

    # 2 abstractions are used: one to write to PWM pins (configurable per
    # JLed object) and one to handle millisecond time (one per plattform).
    # _DEFAULT_PWM_HAL and _TIME_HAL are set platform specific in __init__.py
    _DEFAULT_PWM_HAL = None
    _TIME_HAL = None

    def __init__(self, pin=None, hal=None):
        """
        construct a new JLed object connected to the given pin, or using
        the provided hal object.

        :param pin: the pin to connect the JLed object to
        :param hal: the HAL object to use

        Either pin or hal must be provided. If pin is provided, a HAL instance
        using ``JLed._DEFAULT_PWM_HAL`` will be created.

        Unless you have special requirements, you will want to initialize
        your ``JLed`` object like ``led = JLed(board.LED).breathe(1000)``, i.e.
        by providing the pin the LED is connected to.
        """
        if not (pin is None) ^ (hal is None):
            raise ValueError("either pin or hal must be set")

        # pylint: disable=not-callable
        self._hal = JLed._DEFAULT_PWM_HAL(pin) if hal is None else hal
        self._last_update_time = 0
        self._time_start = 0
        self._state = JLed._ST_INIT
        self._max_brightness = FULL_BRIGHTNESS
        self._min_brightness = 0
        self._low_active = False
        self._num_repetitions = 1
        self._delay_before = 0
        self._delay_after = 0
        self._brightness_eval = None

    def reset(self):
        """A call to ``reset`` brings the JLed object to its initial state.
        Use it when you want to start-over an effect."""
        self._time_start = 0
        self._last_update_time = 0
        self._state = JLed._ST_INIT
        return self

    def low_active(self, val=True):
        """Use the ``low_active`` method when the connected LED is low active.
        All output will be inverted by JLed (i.e. instead of x, the value of
        255-x will be set)."""
        self._low_active = val
        return self

    # pylint: disable=invalid-name
    def on(self, period=1):
        """Calling ``on`` turns the LED on. To immediately turn a LED on,
        remember to also call :func:`update` like in
        ``JLed(board.LED).on().update()``. The ``period`` is optional and defaults
        to 1ms. ``on`` basically calls :func:`set` with brightness
        set to 255.

        :param period: period of the effect. Period will be relevant when
                       multiple JLed objects are controlled by a JLedSequence

        :return: this JLed instance
        """
        return self.set(FULL_BRIGHTNESS, period)

    def off(self, period=1):
        """The ``off`` method works like :func:`on`, except that it
        turns the LED off, i.e. it sets the brightness to 0.

        :param period: period of the effect. Period will be relevant when
                       multiple JLed objects are controlled by a JLedSequence

        :return: this JLed instance
        """
        return self.set(ZERO_BRIGHTNESS, period)

    def set(self, brightness, period=1):
        """Use the ``set`` method to set the brightness to the given value.

        :param brightness: brightness (0..255) to set
        :param period: period of the effect. Period will be relevant when
                       multiple JLed objects are controlled by a JLedSequence

        :return: this JLed instance
        """
        return self._set_brightness_eval(_ConstantBrightnessEval(brightness, period))

    def fade_on(self, period):
        """In fade_on mode, the LED is smoothly faded on to 100% brightness
        using PWM. The ``fade_on`` method takes the period of the effect as an
        argument.

        The brightness function uses an `approximation of this function (example with
        period 1000
        <https://www.wolframalpha.com/input/?i=plot+(exp(sin((t-1000%2F2.)*PI%2F1000))-0.36787944)*108.0++t%3D0+to+1000>`_.

        :param period: period of the effect

        :return: this JLed instance
        """
        return self._set_brightness_eval(_BreatheBrightnessEval(period, 0, 0))

    def fade_off(self, period):
        """In fade_off mode, the LED is smoothly faded off using PWM. The fade
        starts at 100% brightness. Internally it is implemented as a mirrored
        version of the :func:`fade_on` function, i.e.
        ``fade_off(t) = fade_on(period-t)``.

        :param period: period of the effect

        :return: this JLed instance
        """
        return self._set_brightness_eval(_BreatheBrightnessEval(0, 0, period))

    def fade(self, start, end, period):
        """The fade effect allows to fade from any start value ``start`` to
        any target value ``end`` with the given period. Internally it sets up a
        :func:`fade` or :func:`fade_off` effect and :func:`min_brightness` and
        :func:`max_brightness` values properly.

        :param start: start brightness values
        :param end: end brightness value
        :param period: period of the effect

        :return: this JLed instance
        """
        if start < end:
            return self.fade_on(period).min_brightness(start).max_brightness(end)
        return self.fade_off(period).min_brightness(end).max_brightness(start)

    def breathe(self, duration_fade_on, duration_on=None, duration_fade_off=None):
        """In breathing mode, the LED smoothly changes the brightness using
        PWM. The ``breathe`` method takes the period of the effect as an
        argument, however it is also possible to specify fade-on, on- and
        fade-off durations for the breathing mode to customize the effect.

        :param duration_fade_on: if only this parameter is set, then duration_fade_on
           specifies the time in ms of a full breathe period. If also duration_on
           and duration_off are set, this parameter specifies the fade-on time only.
        :param duration_on: if set, specifies time to keep effect at maximum
        :param duration_off: if set, specifies fade-off time

        :return: this JLed instance
        """

        if duration_on is None:
            hperiod = duration_fade_on >> 1
            return self.breathe(hperiod, 0, hperiod)

        return self._set_brightness_eval(
            _BreatheBrightnessEval(duration_fade_on, duration_on, duration_fade_off)
        )

    def blink(self, duration_on, duration_off):
        """In blink mode, the LED cycles through a given number of on-off
        cycles. On- and Off-cycle durations are specified independently.

        :param duration_on: time in ms to turn the LED on
        :param duration_off: time in ms to turn the LED off

        :return: this JLed instance
        """
        return self._set_brightness_eval(
            _BlinkBrightnessEval(duration_on, duration_off)
        )

    def candle(self, speed=6, jitter=15, period=0xFFFF):
        # pylint: disable=line-too-long
        """In candle mode, the random flickering of a candle or fire is simulated.
        The idea was taken from `here <https://cpldcpu.wordpress.com/2013/12/08/hacking-a-candleflicker-led/>`_

        :param speed:   controls the speed of the effect. 0 for fastest,
                        increasing speed divides into halve per increment.
                        The default value is 6.
        :param jitter: the amount of jittering. 0 none (constant on), 255
                        maximum. Default value is 15.
        :param period: - Period of effect in ms. The default value is 65535 ms.

        The default settings simulate a candle. For a fire effect for
        example use call the method with e.g. ``speed=5`` and ``jitter=100``.

        :return: this JLed instance
        """
        return self._set_brightness_eval(_CandleBrightnessEval(speed, jitter, period))

    def user_func(self, user_eval):
        """It is also possible to provide a user defined brightness evaluator.
        The class must implement two methods:

        ``eval(t)`` - the brightness evaluation function that calculates a
        brightness for the given time ``t``. The brightness must be returned as
        an unsigned byte , where 0 means LED off and 255 means full brightness.
        ``period()`` - returns the period of the effect.

        The unit of time is milliseconds.

        .. literalinclude:: ../examples/jled_user_func.py

        :return: this JLed instance
        """
        return self._set_brightness_eval(user_eval)

    def forever(self):
        """Set effect to run forever.

        :return: this JLed instance
        """
        self.repeat(JLed._REPEAT_FOREVER)
        return self

    @property
    def is_forever(self):
        """
        :return: True if effect is set to run forever, otherwise False.
        """
        return self._num_repetitions == JLed._REPEAT_FOREVER

    def repeat(self, num):
        """Use the ``repeat`` method to specify the number of repetitions. The
        default value is 1 repetition. The :func:`forever` method
        sets to repeat the effect forever. Each repetition includes a full
        period of the effect and the time specified by
        :func:`delay_after` method.

        :param num: number of repetitions

        :return: this JLed instance
        """
        self._num_repetitions = num
        return self

    def delay_before(self, time):
        """Use the ``delay_before`` method to specify a delay before the first
        effect starts.  The default value is 0 ms.

        :param time: delay time in milliseconds

        :return: this JLed instance
        """
        self._delay_before = time
        return self

    def delay_after(self, time):
        """Use the ``delay_after`` method to specify a delay after each
        repetition of an effect. The default value is 0 ms.

        :param time: delay time in milliseconds

        :return: this JLed instance
        """
        self._delay_after = time
        return self

    def stop(self):
        """Call ``stop`` to immediately turn the LED off and stop any running
        effects.  Further calls to :func:`update` will have no
        effect unless the :func:`reset` method is called or a new
        effect is activated.

        :return: this JLed instance
        """
        self._write(ZERO_BRIGHTNESS)
        self._state = JLed._ST_STOPPED
        return self

    @property
    def is_running(self):
        """
        :return: True if the effect is running, otherwise False.
        """
        return self._state != JLed._ST_STOPPED

    def max_brightness(self, level):
        """The ``max_brightness`` method is used to set the maximum brightness
        level of the LED. A level of 255 (the default) is full brightness, while 0
        effectively turns the LED off. In the same way, the ``min_brightness``
        method sets the minimum brightness level. The default minimum level is 0. If
        minimum or maximum brightness levels are set, the output value is scaled to be
        within the interval defined by ``[minimum brightness, maximum brightness]``: a
        value of 0 will be mapped to the minimum brightness level, a value of 255 will
        be mapped to the maximum brightness level.

        :return: this JLed instance"""
        self._max_brightness = level & 0xFF
        return self

    def min_brightness(self, level):
        """See :func:`max_brightness`

        :return: this JLed instance
        """
        self._min_brightness = level & 0xFF
        return self

    def _set_brightness_eval(self, evaluator):
        self._brightness_eval = evaluator
        return self.reset()

    def deinit(self):
        """Call ``deinit`` to free hardware resources used by this object"""
        self._hal.deinit()

    def update(self):
        """
        Call ``update`` periodically to update the LED.

        :return: True if the effect is active, otherwise False, when finished.
        """
        return self._update(self._TIME_HAL.millis())

    def _update(self, now):
        if self._state == JLed._ST_STOPPED or self._brightness_eval is None:
            return False

        if self._state == JLed._ST_INIT:
            self._time_start = self._TIME_HAL.ticks_add(now, self._delay_before)
            self._state = JLed._ST_RUNNING
        else:
            if self._last_update_time == now:
                return True

        self._last_update_time = now

        delta = self._TIME_HAL.ticks_diff(now, self._time_start)
        if delta < 0:  # TODO
            return True

        period = self._brightness_eval.period()
        t = delta % (period + self._delay_after)

        if not self.is_forever:
            time_end = self._TIME_HAL.ticks_add(
                self._time_start,
                (period + self._delay_after) * self._num_repetitions - 1,
            )

            if self._TIME_HAL.ticks_diff(now, time_end) >= 0:
                self._state = JLed._ST_STOPPED
                self._write(self._brightness_eval.eval(period - 1))
                return False

        if t < period:
            self._state = JLed._ST_RUNNING
            self._write(self._brightness_eval.eval(t))
        else:
            if self._state == JLed._ST_RUNNING:
                self._state = JLed._ST_IN_DELAY_AFTER_PHASE
                self._write(self._brightness_eval.eval(period - 1))

        return True

    def _write(self, val):
        val = lerp8by8(val, self._min_brightness, self._max_brightness)
        self._hal.analog_write(FULL_BRIGHTNESS - val if self._low_active else val)
