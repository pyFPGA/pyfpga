"""Support examples."""

import argparse
import sys

from pyfpga.factory import Factory, TOOLS


parser = argparse.ArgumentParser()
parser.add_argument(
    '--tool', default='openflow',
    choices=list(TOOLS.keys())
)
args = parser.parse_args()

print(f'INFO: the Tool Under Test is {args.tool}')

print('INFO: checking basic Verilog Support')
prj = Factory(args.tool)
prj.add_vlog('../examples/sources/vlog/blink.v')
prj.set_top('Blink')
prj.make(last='syn')

print('INFO: checking advanced Verilog Support')
prj = Factory(args.tool)
prj.add_vlog('../examples/sources/vlog/*.v')
prj.set_top('Top')
prj.add_include('../examples/sources/vlog/include1')
prj.add_include('../examples/sources/vlog/include2')
prj.add_define('DEFINE1', '1')
prj.add_define('DEFINE2', '1')
prj.add_param('FREQ', '1')
prj.add_param('SECS', '1')
prj.make(last='syn')

try:
    print('INFO: checking Verilog Includes Support')
    prj = Factory(args.tool)
    prj.add_vlog('../examples/sources/vlog/*.v')
    prj.set_top('Top')
    prj.add_define('DEFINE1', '1')
    prj.add_define('DEFINE2', '1')
    prj.add_param('FREQ', '1')
    prj.add_param('SECS', '1')
    prj.make(last='syn')
    sys.exit('ERROR: something does not work as expected')
except SystemExit:
    raise
except Exception:
    pass

try:
    print('INFO: checking Verilog Defines Support')
    prj = Factory(args.tool)
    prj.add_vlog('../examples/sources/vlog/*.v')
    prj.set_top('Top')
    prj.add_include('../examples/sources/vlog/include1')
    prj.add_include('../examples/sources/vlog/include2')
    prj.add_param('FREQ', '1')
    prj.add_param('SECS', '1')
    prj.make(last='syn')
    sys.exit('ERROR: something does not work as expected')
except SystemExit:
    raise
except Exception:
    pass

try:
    print('INFO: checking Verilog Parameters Support')
    prj = Factory(args.tool)
    prj.add_vlog('../examples/sources/vlog/*.v')
    prj.set_top('Top')
    prj.add_include('../examples/sources/vlog/include1')
    prj.add_include('../examples/sources/vlog/include2')
    prj.add_define('DEFINE1', '1')
    prj.add_define('DEFINE2', '1')
    prj.make(last='syn')
    sys.exit('ERROR: something does not work as expected')
except SystemExit:
    raise
except Exception:
    pass

if args.tool not in ['ise']:
    print('INFO: checking basic System Verilog Support')
    prj = Factory(args.tool)
    prj.add_slog('../examples/sources/slog/blink.sv')
    prj.set_top('Blink')
    prj.make(last='syn')

    print('INFO: checking advanced System Verilog Support')
    prj = Factory(args.tool)
    prj.add_slog('../examples/sources/slog/*.sv')
    prj.set_top('Top')
    prj.add_include('../examples/sources/slog/include1')
    prj.add_include('../examples/sources/slog/include2')
    prj.add_define('DEFINE1', '1')
    prj.add_define('DEFINE2', '1')
    prj.add_param('FREQ', '1')
    prj.add_param('SECS', '1')
    prj.make(last='syn')

if args.tool not in ['openflow']:
    print('* INFO: checking basic VHDL Support')
    prj = Factory(args.tool)
    prj.add_vhdl('../examples/sources/vhdl/blink.vhdl')
    prj.set_top('Blink')
    prj.make(last='syn')

    print('* INFO: checking advanced VHDL Support')
    prj = Factory(args.tool)
    prj.add_vhdl('../examples/sources/vhdl/*.vhdl', 'blink_lib')
    prj.add_vhdl('../examples/sources/vhdl/top.vhdl')
    prj.set_top('Top')
    prj.add_param('FREQ', '1')
    prj.add_param('SECS', '1')
    prj.make(last='syn')

    try:
        print('INFO: checking VHDL Generics')
        prj = Factory(args.tool)
        prj.add_vhdl('../examples/sources/vhdl/*.vhdl', 'blink_lib')
        prj.add_vhdl('../examples/sources/vhdl/top.vhdl')
        prj.set_top('Top')
        prj.make(last='syn')
        sys.exit('ERROR: something does not work as expected')
    except SystemExit:
        raise
    except Exception:
        pass

print(f'INFO: {args.tool} support works as expected')
