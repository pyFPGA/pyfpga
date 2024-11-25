from pyfpga.ise import get_info as get_info_ise
from pyfpga.libero import get_info as get_info_libero
from pyfpga.openflow import get_info as get_info_openflow


def test_ise():
    info = {
        'family': 'kintex7',
        'device': 'xc7k160t',
        'speed': '-3',
        'package': 'fbg484'
    }
    assert get_info_ise('xc7k160t-3-fbg484') == info
    assert get_info_ise('xc7k160t-fbg484-3') == info
    info['speed'] = '-3l'
    assert get_info_ise('xc7k160t-3L-fbg484') == info
    assert get_info_ise('xc7k160t-fbg484-3L') == info


def test_libero():
    info = {
        'family': 'SmartFusion2',
        'device': 'm2s025t',
        'speed': 'STD',
        'package': 'fg484',
        'prange': 'COM'
    }
    assert get_info_libero('M2S025T-FG484') == info
    info['prange'] = 'IND'
    assert get_info_libero('M2S025T-FG484I') == info
    info['speed'] = '-1'
    info['prange'] = 'COM'
    assert get_info_libero('M2S025T-1FG484') == info
    assert get_info_libero('M2S025T-1-FG484') == info
    assert get_info_libero('M2S025T-FG484-1') == info
    info['prange'] = 'IND'
    assert get_info_libero('M2S025T-1FG484I') == info
    assert get_info_libero('M2S025T-1-FG484I') == info
    assert get_info_libero('M2S025T-FG484I-1') == info
    info['prange'] = 'MIL'
    assert get_info_libero('M2S025T-1FG484M') == info
    assert get_info_libero('M2S025T-1-FG484M') == info
    assert get_info_libero('M2S025T-FG484M-1') == info
    info = {
        'family': 'IGLOO2',
        'device': 'm2gl025',
        'speed': 'STD',
        'package': 'fg484',
        'prange': 'COM'
    }
    assert get_info_libero('M2GL025-FG484') == info
    info['prange'] = 'IND'
    assert get_info_libero('M2GL025-FG484I') == info
    info['speed'] = '-1'
    info['prange'] = 'COM'
    assert get_info_libero('M2GL025-1FG484') == info
    assert get_info_libero('M2GL025-1-FG484') == info
    assert get_info_libero('M2GL025-FG484-1') == info
    info['prange'] = 'IND'
    assert get_info_libero('M2GL025-1FG484I') == info
    assert get_info_libero('M2GL025-1-FG484I') == info
    assert get_info_libero('M2GL025-FG484I-1') == info
    info['prange'] = 'MIL'
    assert get_info_libero('M2GL025-1FG484M') == info
    assert get_info_libero('M2GL025-1-FG484M') == info
    assert get_info_libero('M2GL025-FG484M-1') == info
    info['prange'] = 'TGrade1'
    assert get_info_libero('M2GL025-1FG484T1') == info
    assert get_info_libero('M2GL025-1-FG484T1') == info
    assert get_info_libero('M2GL025-FG484T1-1') == info
    info = {
        'family': 'PolarFire',
        'device': 'mpf300ts_es',
        'speed': 'STD',
        'package': 'fg484',
        'prange': 'EXT'
    }
    assert get_info_libero('MPF300TS_ES-FG484E') == info
    info['prange'] = 'IND'
    assert get_info_libero('MPF300TS_ES-FG484I') == info
    info['speed'] = '-1'
    info['prange'] = 'EXT'
    assert get_info_libero('MPF300TS_ES-1FG484E') == info
    assert get_info_libero('MPF300TS_ES-1-FG484E') == info
    assert get_info_libero('MPF300TS_ES-FG484E-1') == info
    info['prange'] = 'IND'
    assert get_info_libero('MPF300TS_ES-1FG484I') == info
    assert get_info_libero('MPF300TS_ES-1-FG484I') == info
    assert get_info_libero('MPF300TS_ES-FG484I-1') == info
    info = {
        'family': 'PolarFireSoC',
        'device': 'mpfs025t',
        'speed': 'STD',
        'package': 'fcvg484',
        'prange': 'EXT'
    }
    assert get_info_libero('MPFS025T-FCVG484E') == info
    info['prange'] = 'IND'
    assert get_info_libero('MPFS025T-FCVG484I') == info
    info['speed'] = '-1'
    info['prange'] = 'EXT'
    assert get_info_libero('MPFS025T-1FCVG484E') == info
    assert get_info_libero('MPFS025T-1-FCVG484E') == info
    assert get_info_libero('MPFS025T-FCVG484E-1') == info
    info['prange'] = 'IND'
    assert get_info_libero('MPFS025T-1FCVG484I') == info
    assert get_info_libero('MPFS025T-1-FCVG484I') == info
    assert get_info_libero('MPFS025T-FCVG484I-1') == info


def test_openflow():
    info = {'family': 'xc7', 'device': 'xc7k160t-3', 'package': 'fbg484'}
    assert get_info_openflow('xc7k160t-3-fbg484') == info
    info = {'family': 'ice40', 'device': 'hx1k', 'package': 'tq144'}
    assert get_info_openflow('hx1k-tq144') == info
    info = {'family': 'ecp5', 'device': '25k', 'package': 'CSFBGA285'}
    assert get_info_openflow('25k-CSFBGA285') == info
    info = {'family': 'ecp5', 'device': 'um5g-85k', 'package': 'CABGA381'}
    assert get_info_openflow('um5g-85k-CABGA381') == info
