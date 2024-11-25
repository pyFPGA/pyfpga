"""Yosys-Vivado example project."""

import argparse
import logging

from fpga.project import Project

logging.basicConfig()

parser = argparse.ArgumentParser()
parser.add_argument(
    '--action', choices=['generate', 'transfer', 'all'], default='generate',
)
parser.add_argument(
    '--lang', choices=['verilog', 'vhdl'], default='verilog',
)
args = parser.parse_args()

prj = Project('yosys-vivado')
prj.set_outdir('../../build/yosys-vivado-{}'.format(args.lang))
prj.set_part('xc7z010-1-clg400')

if args.lang == 'verilog':
    prj.add_vlog_include('../../hdl/headers1')
    prj.add_vlog_include('../../hdl/headers2')
    prj.add_files('../../hdl/blinking.v')
    prj.add_files('../../hdl/top.v')
else:  # args.lang == 'vhdl'
    prj.add_files('../../hdl/blinking.vhdl', library='examples')
    prj.add_files('../../hdl/examples_pkg.vhdl', library='examples')
    prj.add_files('../../hdl/top.vhdl')

prj.add_files('../vivado/zybo.xdc')
prj.set_top('Top')

if args.action in ['generate', 'all']:
    prj.generate()

if args.action in ['transfer', 'all']:
    prj.transfer()
