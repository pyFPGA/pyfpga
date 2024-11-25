"""Diamond hooks examples."""

from pyfpga.diamond import Diamond

prj = Diamond()

hooks = {
    "reports": """
prj_run Map -task MapTrace -forceOne
prj_run PAR -task PARTrace -forceOne
prj_run PAR -task IOTiming -forceOne
    """,

    "netlist_simulation": """
prj_run Map -task MapVerilogSimFile
prj_run Map -task MapVHDLSimFile -forceOne
prj_run Export -task TimingSimFileVHD -forceOne
prj_run Export -task TimingSimFileVlg -forceOne
prj_run Export -task IBIS -forceOne
    """,

    "progfile_ecp5u": """
prj_run Export -task Promgen -forceOne
    """,

    "progfile_machxo2": """
prj_run Export -task Jedecgen -forceOne
    """
}

prj.set_part('LFXP2-5E-5TN144C')

prj.add_param('FREQ', '50000000')
prj.add_param('SECS', '1')

prj.add_cons('../sources/cons/brevia2/clk.lpf')
prj.add_cons('../sources/cons/brevia2/led.lpf')

prj.add_include('../sources/vlog/include1')
prj.add_include('../sources/vlog/include2')
prj.add_vlog('../sources/vlog/*.v')

prj.add_define('DEFINE1', '1')
prj.add_define('DEFINE2', '1')

prj.set_top('Top')

for hook_name, hook in hooks.items():
    prj.add_hook('postpar', hook)

prj.make()
