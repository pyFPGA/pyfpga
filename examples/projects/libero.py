"""Libero examples."""

import argparse

from pyfpga.libero import Libero

parser = argparse.ArgumentParser()
parser.add_argument(
    '--board', choices=['mpfs-disco-kit', 'maker'], default='mpfs-disco-kit'
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

prj = Libero(odir=f'results/libero/{args.source}/{args.board}')


if args.board == 'mpfs-disco-kit':
    prj.set_part('MPFS095T-1-FCSG325E')
    prj.add_param('FREQ', '50000000')
    prj.add_cons('../sources/cons/mpfs-disco-kit/timing.sdc')
    prj.add_cons('../sources/cons/mpfs-disco-kit/clk.pdc')
    prj.add_cons('../sources/cons/mpfs-disco-kit/led.pdc')
if args.board == 'maker':
    prj.set_part('m2s010-1-tq144')
    prj.add_param('FREQ', '125000000')
    prj.add_cons('../sources/cons/maker/timing.sdc')
    prj.add_cons('../sources/cons/maker/clk.pdc')
    prj.add_cons('../sources/cons/maker/led.pdc')
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
    prj.add_vlog('../sources/slog/*.sv')
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
