#!/bin/bash

set -e

HDIR=../../pyfpga/helpers

python3 $HDIR/hdl2bit.py -t ise -o results/ise-vlog -p xc6slx16-3-csg32 \
    -i ../sources/vlog/include1 -i ../sources/vlog/include2 \
    -f ../sources/vlog/blink.v -f ../sources/vlog/top.v \
    -f ../sources/cons/nexys3/timing.xcf -f ../sources/cons/nexys3/clk.ucf -f ../sources/cons/nexys3/led.ucf \
    --define DEFINE1 1 --define DEFINE2 1 --param FREQ 125000000 --param SECS 1 Top

python3 $HDIR/hdl2bit.py -t ise -o results/ise-vhdl -p xc6slx16-3-csg32 --project example \
    -f ../sources/vhdl/blink.vhdl,blink_lib -f ../sources/vhdl/blink_pkg.vhdl,blink_lib -f ../sources/vhdl/top.vhdl \
    -f ../sources/cons/nexys3/timing.xcf -f ../sources/cons/nexys3/clk.ucf -f ../sources/cons/nexys3/led.ucf \
    --param FREQ 125000000 --param SECS 1 --last cfg Top

python3 $HDIR/prj2bit.py results/ise-vhdl/example.xise
