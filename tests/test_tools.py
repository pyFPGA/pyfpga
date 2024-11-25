from pathlib import Path
from pyfpga.factory import Factory

tdir = Path(__file__).parent.resolve()


def test_diamond():
    tool = 'diamond'
    generate(tool, 'PARTNAME')
    base = f'results/{tool}/{tool}'
    assert Path(f'{base}.tcl').exists(), 'file not found'
    assert Path(f'{base}-prog.sh').exists(), 'file not found'


def test_ise():
    tool = 'ise'
    generate(tool, 'DEVICE-PACKAGE-SPEED')
    base = f'results/{tool}/{tool}'
    assert Path(f'{base}.tcl').exists(), 'file not found'
    assert Path(f'{base}-prog.tcl').exists(), 'file not found'


def test_libero():
    tool = 'libero'
    generate(tool, 'DEVICE-PACKAGE-SPEED')
    base = f'results/{tool}/{tool}'
    assert Path(f'{base}.tcl').exists(), 'file not found'
    assert Path(f'{base}-prog.tcl').exists(), 'file not found'


def test_openflow():
    tool = 'openflow'
    generate(tool, 'DEVICE-PACKAGE')
    base = f'results/{tool}/{tool}'
    assert Path(f'{base}.sh').exists(), 'file not found'
    assert Path(f'{base}-prog.sh').exists(), 'file not found'


def test_quartus():
    tool = 'quartus'
    generate(tool, 'PARTNAME')
    base = f'results/{tool}/{tool}'
    assert Path(f'{base}.tcl').exists(), 'file not found'
    assert Path(f'{base}-prog.tcl').exists(), 'file not found'


def test_vivado():
    tool = 'vivado'
    generate(tool, 'PARTNAME')
    base = f'results/{tool}/{tool}'
    assert Path(f'{base}.tcl').exists(), 'file not found'
    assert Path(f'{base}-prog.tcl').exists(), 'file not found'


def generate(tool, part):
    prj = Factory(tool, odir=f'results/{tool}')
    prj.set_part(part)
    prj.set_top('TOPNAME')
    prj.add_include(str(tdir / 'fakedata/dir1'))
    prj.add_include(str(tdir / 'fakedata/dir2'))
    if tool != 'ise':
        prj.add_slog(str(tdir / 'fakedata/**/*.sv'))
    prj.add_vhdl(str(tdir / 'fakedata/**/*.vhdl'), 'LIB')
    prj.add_vlog(str(tdir / 'fakedata/**/*.v'))
    prj.add_cons(str(tdir / 'fakedata/cons/all.xdc'))
    prj.add_cons(str(tdir / 'fakedata/cons/syn.xdc'))
    prj.add_cons(str(tdir / 'fakedata/cons/par.xdc'))
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
    except RuntimeError:
        pass
    if tool == 'libero':
        open(f'results/{tool}/{tool}.ppd', 'w').close()
    elif tool == 'quartus':
        open(f'results/{tool}/{tool}.sof', 'w').close()
    else:
        open(f'results/{tool}/{tool}.bit', 'w').close()
    try:
        prj.prog()
    except RuntimeError:
        pass
