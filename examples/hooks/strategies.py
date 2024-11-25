"""PyFPGA Multi Vendor Strategy example.

The main idea of a multi-vendor project is to implements the same HDL code
with different tools, to make comparisons. The project name is not important
and the default devices can be used. In this example, strategies are changed
between area, power and speed.
"""

import logging

from fpga.project import Project

logging.basicConfig()

commands = {
    'ise': {
        'area': """
project set "Optimization Goal" "Area"
""",
        'power': """
project set "Optimization Goal" "Area"
project set "Power Reduction" "true" -process "Synthesize - XST"
project set "Power Reduction" "high" -process "Map"
project set "Power Reduction" "true" -process "Place & Route"
""",
        'speed': """
project set "Optimization Goal" "Speed"
"""
    },
    'libero': {
        'area': """
configure_tool -name {SYNTHESIZE} -params {RAM_OPTIMIZED_FOR_POWER:true}
""",
        'power': """
configure_tool -name {SYNTHESIZE} -params {RAM_OPTIMIZED_FOR_POWER:true}
configure_tool -name {PLACEROUTE} -params {PDPR:true}
""",
        'speed': """
configure_tool -name {SYNTHESIZE} -params {RAM_OPTIMIZED_FOR_POWER:false}
configure_tool -name {PLACEROUTE} -params {EFFORT_LEVEL:true}
"""
    },
    'quartus': {
        'area': """
set_global_assignment -name OPTIMIZATION_MODE "AGGRESSIVE AREA"
set_global_assignment -name OPTIMIZATION_TECHNIQUE AREA
""",
        'power': """
set_global_assignment -name OPTIMIZATION_MODE "AGGRESSIVE POWER"
set_global_assignment -name OPTIMIZE_POWER_DURING_SYNTHESIS "EXTRA EFFORT"
set_global_assignment -name OPTIMIZE_POWER_DURING_FITTING "EXTRA EFFORT"
""",
        'speed': """
set_global_assignment -name OPTIMIZATION_MODE "AGGRESSIVE PERFORMANCE"
set_global_assignment -name OPTIMIZATION_TECHNIQUE SPEED
"""
    },
    'vivado': {
        'area': """
set obj [get_runs synth_1]
set_property strategy "Flow_AreaOptimized_high" $obj
set_property "steps.synth_design.args.directive" "AreaOptimized_high" $obj
set_property "steps.synth_design.args.control_set_opt_threshold" "1" $obj
set obj [get_runs impl_1]
set_property strategy "Area_Explore" $obj
set_property "steps.opt_design.args.directive" "ExploreArea" $obj
""",
        'power': """
#enable power_opt_design and phys_opt_design
set obj [get_runs synth_1]
set_property strategy "Vivado Synthesis Defaults" $obj
set obj [get_runs impl_1]
set_property strategy "Power_DefaultOpt" $obj
set_property "steps.power_opt_design.is_enabled" "1" $obj
set_property "steps.phys_opt_design.is_enabled" "1" $obj
""",
        'speed': """
#enable phys_opt_design
set obj [get_runs synth_1]
set_property strategy "Flow_PerfOptimized_high" $obj
set_property "steps.synth_design.args.fanout_limit" "400" $obj
set_property "steps.synth_design.args.keep_equivalent_registers" "1" $obj
set_property "steps.synth_design.args.resource_sharing" "off" $obj
set_property "steps.synth_design.args.no_lc" "1" $obj
set_property "steps.synth_design.args.shreg_min_size" "5" $obj
set obj [get_runs impl_1]
set_property strategy "Performance_Explore" $obj
set_property "steps.opt_design.args.directive" "Explore" $obj
set_property "steps.place_design.args.directive" "Explore" $obj
set_property "steps.phys_opt_design.is_enabled" "1" $obj
set_property "steps.phys_opt_design.args.directive" "Explore" $obj
set_property "steps.route_design.args.directive" "Explore" $obj
"""
    }
}

for tool in commands:
    for strategy in commands[tool]:
        PRJ = Project(tool)
        PRJ.set_outdir('../../build/hooks/%s-%s' % (tool, strategy))
        PRJ.add_files('../../hdl/blinking.vhdl')
        PRJ.set_top('Blinking')
        PRJ.add_hook(
            'puts "Appling {} optimizations"'.format(strategy),
            'project'
        )
        PRJ.add_hook(commands[tool][strategy], 'project')
        PRJ.generate(to_task='syn')
