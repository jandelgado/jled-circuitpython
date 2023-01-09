#!/bin/bash
#
# compile JLed to binary .mpy format and copy lib and example files
# to micropython device using mpremote. Depends on:
# - mpremote (https://pypi.org/project/mpremote/
# - mpy-cross (https://pypi.org/project/mpy-cross)
#
# Due to stability problems with mpremote and my ESP32, files are collected
# in a temp directory and then copied with on mpremote cp invocation.
#
# Environment variables:
#   MAIN_SOURCE - path to to file to copy as main.py (e.g. an example script)
#   MPREMOTE - mpremote binary to use
set -eouT pipefail

# example to copy
MAIN_SOURCE=${MAIN_SOURCE:-examples/jled_micropython.py}
MPREMOTE=${MPREMOTE:-mpremote}

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
cd "$SCRIPT_DIR/.."

LIB_SOURCES="jled/__init__.py jled/jled.py jled/hal_pwm_micropython.py jled/hal_time_micropython.py jled/play.py jled/jled_sequence.py"
SOURCES="$LIB_SOURCES $MAIN_SOURCE"

echo $MPREMOTE

echo ">> compiling .py to .mpy..."
for file in $SOURCES; do
    mpy-cross "$file"
done

# prepare local directory which will be uploaded 
SRC=$(mktemp -d)
trap "rm -rf $SRC" EXIT
mkdir $SRC/jled

echo ">> prepare upload folder..."
for file in $LIB_SOURCES; do
    cp ${file%.py}.mpy $SRC/jled
done

# compiled main.mpy is not supported currently
cp $MAIN_SOURCE $SRC/main.py

cd $SRC && ${MPREMOTE} cp -r . :

