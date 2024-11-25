"""Vivado hooks examples."""

from pathlib import Path
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

prj.add_cons('../sources/cons/ZYBO/timing.xdc')
prj.add_cons('../sources/cons/ZYBO/clk.xdc')
prj.add_cons('../sources/cons/ZYBO/led.xdc')

prj.set_top('Top')

prj.add_hook('precfg', '''
set obj [get_runs synth_1]
set_property strategy "Flow_AreaOptimized_high" $obj
set_property "steps.synth_design.args.directive" "AreaOptimized_high" $obj
set_property "steps.synth_design.args.control_set_opt_threshold" "1" $obj
set obj [get_runs impl_1]
set_property strategy "Area_Explore" $obj
set_property "steps.opt_design.args.directive" "ExploreArea" $obj
''')

place = ['../sources/cons/ZYBO/clk.xdc', '../sources/cons/ZYBO/led.xdc']
prj.add_hook('postcfg', f'''
set_property USED_IN_SYNTHESIS FALSE [get_files {Path(place[0]).resolve()}]
set_property USED_IN_SYNTHESIS FALSE [get_files {Path(place[1]).resolve()}]
''')

prj.make()
