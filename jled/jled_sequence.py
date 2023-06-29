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

from .jled import JLed


class JLedSequence:
    """The ``JLedSequence`` class allows controlling a group of effects
    either in parallel or sequentially. An effect is either a :class:`~jled.jled.JLed`
    object or a ``JLedSequence``.

    Example::

        from jled import JLed, JLedSequence

        led1 = JLed(board.LED).blink(500, 250).repeat(5)
        led2 = JLed(board.GP2).breathe(1000).repeat(5)

        seq = JLedSequence(JLedSequence.SEQUENTIAL, [led1, led2])

    """

    PARALLEL = 0
    SEQUENTIAL = 1
    _REPEAT_FOREVER = -1

    def __init__(self, mode, leds):
        """Construct a JLedSequence for the given list of effects. An effect
        can be either a ``JLed`` object, or another ``JLedSequence``.

        For convenience, two additional functions are provided:
        :func:`parallel` and :func:`sequential`

        :param mode: one of ``JLedSequence.PARALLEL`` or ``JLedSequence.SEQUENTIAL``
        :param leds: list of effects to control


        """
        self._mode = mode
        self._leds = leds
        self._num_repetitions = 1
        self._cur = 0
        self._iteration = 0
        self._is_running = True

    @staticmethod
    def parallel(leds):
        """Initialize a JLedSequence to play given effects in parallel. This is
        a convenience method for calling ``JLedSequence(JLedSequence.PARALLEL, leds)``.

        :param leds: list of effects to play

        :return: a new JLedSequence object
        """
        return JLedSequence(JLedSequence.PARALLEL, leds)

    @staticmethod
    def sequential(leds):
        """Initialize a JLedSequence to play given effects sequentially. This is
        a convenience method for calling ``JLedSequence(JLedSequence.SEQUENTIAL, leds)``.

        :param leds: list of effects to play

        :return: a new JLedSequence object
        """
        return JLedSequence(JLedSequence.SEQUENTIAL, leds)

    def _reset_leds(self):
        for led in self._leds:
            led.reset()

    def _update_parallel(self, t):
        result = False
        for led in self._leds:
            # pylint: disable=protected-access
            result |= led._update(t)  # considered "friend class"
        return result

    def _update_sequentially(self, t):
        n = len(self._leds)
        if self._cur >= n:
            return False
        # pylint: disable=protected-access
        if not self._leds[self._cur]._update(t):
            self._cur += 1
            return self._cur < n
        return True

    def _update(self, t):
        #  if self._mode == JLedSequence.PARALLEL:
        #      return self._update_parallel(t)
        #  return self._update_sequentially(t)
        running = (
            self._update_parallel(t)
            if self._mode == JLedSequence.PARALLEL
            else self._update_sequentially(t)
        )

        if running:
            return True

        self._cur = 0
        self._iteration += 1
        is_running = self._iteration < self._num_repetitions or self.is_forever

        if is_running:
            # reset all leds after each full iteration as long as the sequence is running
            self._reset_leds()

        self._is_running = is_running
        return is_running

    def update(self):
        """
        Call update periodically to play the effects/LEDs.

        :return: True if the effect is still running, otherwise False
        """
        if not self._is_running:
            return False

        t = JLed._TIME_HAL.millis()  # pylint: disable=protected-access
        return self._update(t)

    def reset(self):
        """Reset all LEDs controlled by this ``JLedSequence`` and the
        JLedSequence itself. Calling update afterwards will start all all LEDs
        over.

        :return: this JLedSequence object
        """
        self._reset_leds()
        self._cur = 0
        self._iteration = 0
        self._is_running = True
        return self

    def stop(self):
        """Turns off all objects controlled by this ``JLedSequence`` and stops
        the sequence. Further calls to :func:`update` will have no effect.

        :return: this JLedSequence object
        """
        self._is_running = False
        for led in self._leds:
            led.stop()
        return self

    def repeat(self, num):
        """Use the ``repeat`` method to specify the number of repetitions. The
        default value is 1 repetition.

        :param num: number of repetitions

        :return: this JLedSequence object
        """
        self._num_repetitions = num
        return self

    def forever(self):
        """Set this ``JLedSequence`` to run forever.

        :return: this JLedSequence object
        """
        """set effect to run forever"""
        return self.repeat(JLedSequence._REPEAT_FOREVER)

    @property
    def is_forever(self):
        """
        :return: True if this ``JLedSequence`` is set to run
                 :func:`forever`, otherwise False
        """
        return self._num_repetitions == JLedSequence._REPEAT_FOREVER

    @property
    def is_running(self):
        """
        :return: True if ``JLedSequence`` is running, otherwise False.
        """
        return self._is_running
