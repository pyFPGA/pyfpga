#!/bin/bash

set -e

HDIR=../../pyfpga/helpers

python3 $HDIR/hdl2bit.py -t vivado -o results/vivado-vlog -p xc7z010-1-clg400 \
    -i ../sources/vlog/include1 -i ../sources/vlog/include2 \
    -f ../sources/vlog/blink.v -f ../sources/vlog/top.v \
    -f ../sources/cons/ZYBO/timing.xdc -f ../sources/cons/ZYBO/clk.xdc -f ../sources/cons/ZYBO/led.xdc \
    --define DEFINE1 1 --define DEFINE2 1 --param FREQ 125000000 --param SECS 1 Top

python3 $HDIR/hdl2bit.py -t vivado -o results/vivado-vhdl -p xc7z010-1-clg400 --project example \
    -f ../sources/vhdl/blink.vhdl,blink_lib -f ../sources/vhdl/blink_pkg.vhdl,blink_lib -f ../sources/vhdl/top.vhdl \
    -f ../sources/cons/ZYBO/timing.xdc -f ../sources/cons/ZYBO/clk.xdc -f ../sources/cons/ZYBO/led.xdc \
    --param FREQ 125000000 --param SECS 1 --last cfg Top

python3 $HDIR/prj2bit.py results/vivado-vhdl/example.xpr
