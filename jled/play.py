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
from .jled_sequence import JLedSequence


def play(*leds, seq=False):
    """play puts the given list of objects in a
    :class:`~jled.jled_sequence.JLedSequence` and runs the effects, until the last
    effect finished. This function is intended to be used when interactively
    exploring JLed in the Python REPL.

    Example::

        from jled import JLed, play

        led1 = JLed(board.LED).blink(500, 250).repeat(5)
        led2 = JLed(board.GP2).breathe(1000).repeat(5)

        play(led1, led2)

    :param leds: list of effects to "play"
    :param seq: set to True to play effects sequentially. When False (default),
                effects will be played in parallel.
    """
    seq = JLedSequence.sequential(leds) if seq else JLedSequence.parallel(leds)
    while seq.update():
        pass
