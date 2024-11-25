"""Vivado elaboration example."""

from pyfpga.vivado import Vivado


prj = Vivado()

prj.set_part('xc7z010-1-clg400')

prj.add_param('FREQ', '125000000')
prj.add_param('SECS', '1')
prj.add_define('DEFINE1', '1')
prj.add_define('DEFINE2', '1')

prj.add_include('../sources/slog/include1')
prj.add_include('../sources/slog/include2')
prj.add_slog('../sources/slog/*.sv')

prj.set_top('Top')

prj.add_hook('presyn', 'synth_design -rtl -rtl_skip_mlo; exit 0')

prj.make()
