#!/bin/bash
#
# compile JLed to binary .mpy format and copy lib and example
# to micropython device using mpremote. Depends on:
# - mpy-cross (https://pypi.org/project/mpy-cross)
# - mpremote (https://pypi.org/project/mpremote/
#
set -eouT pipefail

# example to copy
EXAMPLE_SOURCE="examples/jled_micropython.py"

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
cd "$SCRIPT_DIR/.."

LIB_SOURCES="jled/__init__.py jled/jled.py jled/hal_pwm_micropython.py jled/hal_time_micropython.py"
SOURCES="$LIB_SOURCES $EXAMPLE_SOURCE"

echo ">> compiling .py to .mpy..."
for file in $SOURCES; do
    mpy-cross "$file"
done

echo ">> copy lib files to device..."
mpremote mkdir :jled 2>&1 > /dev/null || true
for file in $LIB_SOURCES; do
    mpremote cp ${file%.py}.mpy :jled/
done

echo ">> copy example $EXAMPLE_SOURCE"
mpremote cp ${EXAMPLE_SOURCE%.py}.mpy :main.mpy
