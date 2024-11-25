#!/bin/bash

set -e

HDIR=../../pyfpga/helpers

python3 $HDIR/hdl2bit.py -t libero -o results/libero-vlog -p m2s010-1-tq144 \
    -i ../sources/vlog/include1 -i ../sources/vlog/include2 \
    -f ../sources/vlog/blink.v -f ../sources/vlog/top.v \
    -f ../sources/cons/maker/timing.sdc -f ../sources/cons/maker/clk.pdc -f ../sources/cons/maker/led.pdc \
    --define DEFINE1 1 --define DEFINE2 1 --param FREQ 125000000 --param SECS 1 Top

python3 $HDIR/hdl2bit.py -t libero -o results/libero-vhdl -p m2s010-1-tq144 --project example \
    -f ../sources/vhdl/blink.vhdl,blink_lib -f ../sources/vhdl/blink_pkg.vhdl,blink_lib -f ../sources/vhdl/top.vhdl \
    -f ../sources/cons/maker/timing.sdc -f ../sources/cons/maker/clk.pdc -f ../sources/cons/maker/led.pdc \
    --param FREQ 125000000 --param SECS 1 --last cfg Top

python3 $HDIR/prj2bit.py results/libero-vhdl/libero/example.prjx
