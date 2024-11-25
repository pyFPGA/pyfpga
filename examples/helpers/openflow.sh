#!/bin/bash

set -e

HDIR=../../pyfpga/helpers

python3 $HDIR/hdl2bit.py -t openflow -o results/openflow-vlog -p hx1k-tq144 \
    -i ../sources/vlog/include1 -i ../sources/vlog/include2 \
    -f ../sources/vlog/blink.v -f ../sources/vlog/top.v \
    -f ../sources/cons/icestick/clk.pcf -f ../sources/cons/icestick/led.pcf \
    --define DEFINE1 1 --define DEFINE2 1 --param FREQ 100000000 --param SECS 1 Top
