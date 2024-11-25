"""Vivado examples."""

import argparse

from pyfpga.vivado import Vivado


parser = argparse.ArgumentParser()
parser.add_argument(
    '--board', choices=['zybo', 'arty'], default='zybo'
)
parser.add_argument(
    '--source', choices=['vlog', 'vhdl', 'slog'], default='vlog'
)
parser.add_argument(
    '--action', choices=['make', 'prog', 'all'], default='make'
)
parser.add_argument(
    '--notool', action='store_true'
)
args = parser.parse_args()

prj = Vivado(odir=f'results/vivado/{args.source}/{args.board}')

if args.board == 'zybo':
    prj.set_part('xc7z010-1-clg400')
    prj.add_param('FREQ', '125000000')
    prj.add_cons('../sources/cons/ZYBO/timing.xdc')
    prj.add_cons('../sources/cons/ZYBO/clk.xdc')
    prj.add_cons('../sources/cons/ZYBO/led.xdc')
if args.board == 'arty':
    prj.set_part('xc7a35ticsg324-1L')
    prj.add_param('FREQ', '100000000')
    prj.add_cons('../sources/cons/arty_a7_35t/timing.xdc')
    prj.add_cons('../sources/cons/arty_a7_35t/clk.xdc')
    prj.add_cons('../sources/cons/arty_a7_35t/led.xdc')
prj.add_param('SECS', '1')

if args.source == 'vhdl':
    prj.add_vhdl('../sources/vhdl/*.vhdl', 'blink_lib')
    prj.add_vhdl('../sources/vhdl/top.vhdl')
if args.source == 'vlog':
    prj.add_include('../sources/vlog/include1')
    prj.add_include('../sources/vlog/include2')
    prj.add_vlog('../sources/vlog/*.v')
if args.source == 'slog':
    prj.add_include('../sources/slog/include1')
    prj.add_include('../sources/slog/include2')
    prj.add_slog('../sources/slog/*.sv')
if args.source in ['vlog', 'slog']:
    prj.add_define('DEFINE1', '1')
    prj.add_define('DEFINE2', '1')

prj.set_top('Top')

try:
    if args.action in ['make', 'all']:
        prj.make()
    if args.action in ['prog', 'all']:
        prj.prog()
except RuntimeError:
    if not args.notool:
        raise
