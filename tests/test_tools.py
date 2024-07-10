from pyfpga.ise import Ise
from pyfpga.libero import Libero
from pyfpga.openflow import Openflow
from pyfpga.quartus import Quartus
from pyfpga.vivado import Vivado


tools = {
    'ise': Ise,
    'libero': Libero,
    'openflow': Openflow,
    'quartus': Quartus,
    'vivado': Vivado
}


def test_ise():
    generate('ise')


def test_libero():
    generate('libero')


def test_openflow():
    generate('openflow')


def test_quartus():
    generate('quartus')


def test_vivado():
    generate('vivado')


def generate(tool):
    prj = tools[tool](odir=f'results/{tool}')
    prj.set_part('PARTNAME')
    prj.set_top('TOPNAME')
    prj.add_include('fakedata/dir1')
    prj.add_include('fakedata/dir2')
    if tool != 'ise':
        prj.add_slog('fakedata/**/*.sv')
    prj.add_vhdl('fakedata/**/*.vhdl', 'LIB')
    prj.add_vlog('fakedata/**/*.v')
    prj.add_cons('fakedata/cons/all.xdc')
    prj.add_cons('fakedata/cons/syn.xdc', 'syn')
    prj.add_cons('fakedata/cons/par.xdc', 'par')
    prj.add_param('PAR1', 'VAL1')
    prj.add_param('PAR2', 'VAL2')
    prj.add_define('DEF1', 'VAL1')
    prj.add_define('DEF2', 'VAL2')
    prj.add_hook('precfg', 'HOOK01')
    prj.add_hook('precfg', 'HOOK02')
    prj.add_hook('postcfg', 'HOOK03')
    prj.add_hook('postcfg', 'HOOK04')
    prj.add_hook('presyn', 'HOOK05')
    prj.add_hook('presyn', 'HOOK06')
    prj.add_hook('postsyn', 'HOOK07')
    prj.add_hook('postsyn', 'HOOK08')
    prj.add_hook('prepar', 'HOOK09')
    prj.add_hook('prepar', 'HOOK10')
    prj.add_hook('postpar', 'HOOK11')
    prj.add_hook('postpar', 'HOOK12')
    prj.add_hook('prebit', 'HOOK13')
    prj.add_hook('prebit', 'HOOK14')
    prj.add_hook('postbit', 'HOOK15')
    prj.add_hook('postbit', 'HOOK16')
    try:
        prj.make()
    except Exception:
        pass
    try:
        prj.prog()
    except Exception:
        pass
