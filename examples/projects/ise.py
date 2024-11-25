"""ISE examples."""

import argparse

from pyfpga.ise import Ise


parser = argparse.ArgumentParser()
parser.add_argument(
    '--board', choices=['s6micro', 'nexys3'], default='s6micro'
)
parser.add_argument(
    '--source', choices=['vlog', 'vhdl'], default='vlog'
)
parser.add_argument(
    '--action', choices=['make', 'prog', 'all'], default='make'
)
parser.add_argument(
    '--notool', action='store_true'
)
args = parser.parse_args()

prj = Ise(odir=f'results/ise/{args.source}/{args.board}')

if args.board == 's6micro':
    prj.set_part('xc6slx9-2-csg324')
    prj.add_param('FREQ', '125000000')
    prj.add_cons('../sources/cons/s6micro/timing.xcf')
    prj.add_cons('../sources/cons/s6micro/clk.ucf')
    prj.add_cons('../sources/cons/s6micro/led.ucf')
if args.board == 'nexys3':
    prj.set_part('xc6slx16-3-csg32')
    prj.add_param('FREQ', '100000000')
    prj.add_cons('../sources/cons/nexys3/timing.xcf')
    prj.add_cons('../sources/cons/nexys3/clk.ucf')
    prj.add_cons('../sources/cons/nexys3/led.ucf')
prj.add_param('SECS', '1')

if args.source == 'vhdl':
    prj.add_vhdl('../sources/vhdl/*.vhdl', 'blink_lib')
    prj.add_vhdl('../sources/vhdl/top.vhdl')
if args.source == 'vlog':
    prj.add_include('../sources/vlog/include1')
    prj.add_include('../sources/vlog/include2')
    prj.add_vlog('../sources/vlog/*.v')
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
