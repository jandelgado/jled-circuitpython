Introduction
============

.. image:: https://github.com/jandelgado/jled-circuitpython/workflows/Build%20CI/badge.svg
    :target: https://github.com/jandelgado/jled-circuitpython/actions
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

An embedded library for Python to control LEDs. It uses a **non-blocking**
approach and can control LEDs in simple (**on**/**off**) and complex
(**blinking**, **breathing** and more) ways in a **time-driven** manner.

This is a pure Python port of my `JLed <https://github.com/jandelgado/jled>`_
C++ library.

.. image:: .images/jled.gif
    :alt: JLed in action

Features
========

* non-blocking
* effects: simple on/off, breathe, blink, candle, fade, user-defined
* supports inverted  polarity of LED
* easy configuration using fluent interface
* can control groups of LEDs sequentially or in parallel
* supports CircuitPython and MicroPython

Usage Example
=============

Test JLed interactively in a CircuitPython REPL:

.. code-block::

  Adafruit CircuitPython 7.3.3 on 2022-08-29; Raspberry Pi Pico with rp2040
  >>> import board
  >>> from jled import JLed
  >>> led=JLed(board.LED).breathe(500).delay_after(250).repeat(5)
  >>> while led.update(): pass

This creates a JLed object connected to the builtin LED (``board.LED``), with a
breathe effect that is repeated 5 times.  Each iteration is followed by a delay
of 250 ms, before starting again.  By calling ``led.update()`` periodically,
the LED gets physically updated. Alternatively ``play(led)`` can be call in the
REPL as a shortcut.  Once finished, call ``led.reset()`` before playing the
effect again.

Cheat Sheet
===========

.. image:: .images/jled_cheat_sheet.jpg

Installation
=============

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/circuitpython-jled/>`_.
To install for current user:

.. code-block:: shell

    pip3 install circuitpython-jled

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install circuitpython-jled

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .env/bin/activate
    pip3 install circuitpython-jled

Installing to a Connected CircuitPython Device with Circup
==========================================================

TODO

Documentation
=============

API documentation for this library can be found on `Read the Docs
<https://circuitpython-jled.readthedocs.io/>`_.

For information on building library documentation, please check out `this guide
<https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Rebuild the documentation with ``sphinx-build -E -W -b html . _build/html``
in the ``docs`` directory. Run ``pip install ".[optional]`` before to install
build-time dependency `Sphinx <https://www.sphinx-doc.org/>`_

Tests
=====

Unit tests (using https://docs.pytest.org) are provided, run the tests with:

.. code-block::

   $ pip install ".[optional]"
   $ pytest

To run the ``pre-commit-hook`` locally, run ``pre-commit run --all-files``

Author & Copyright
==================

Copyright © 2022 by Jan Delgado, License: MIT
