#!/bin/bash

set -e

HDIR=../../pyfpga/helpers

python3 $HDIR/hdl2bit.py -t quartus -o results/quartus-vlog -p 5CSEBA6U23I7 \
    -i ../sources/vlog/include1 -i ../sources/vlog/include2 \
    -f ../sources/vlog/blink.v -f ../sources/vlog/top.v \
    -f ../sources/cons/de10nano/timing.sdc -f ../sources/cons/de10nano/clk.tcl -f ../sources/cons/de10nano/led.tcl \
    --define DEFINE1 1 --define DEFINE2 1 --param FREQ 125000000 --param SECS 1 Top

python3 $HDIR/hdl2bit.py -t quartus -o results/quartus-vhdl -p 5CSEBA6U23I7 --project example \
    -f ../sources/vhdl/blink.vhdl,blink_lib -f ../sources/vhdl/blink_pkg.vhdl,blink_lib -f ../sources/vhdl/top.vhdl \
    -f ../sources/cons/de10nano/timing.sdc -f ../sources/cons/de10nano/clk.tcl -f ../sources/cons/de10nano/led.tcl \
    --param FREQ 125000000 --param SECS 1 --last cfg Top

python3 $HDIR/prj2bit.py results/quartus-vhdl/example.qpf
