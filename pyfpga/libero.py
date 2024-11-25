#
# Copyright (C) 2019-2024 PyFPGA Project
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for Libero.
"""

import re

from pyfpga.project import Project


class Libero(Project):
    """Class to support Libero projects."""

    def _configure(self):
        tool = 'libero'
        self.conf['tool'] = tool
        self.conf['make_cmd'] = f'{tool} SCRIPT:{tool}.tcl'
        self.conf['make_ext'] = 'tcl'
        self.conf['prog_bit'] = ['ppd', 'stp', 'bit', 'jed']
        self.conf['prog_cmd'] = f'FPExpress SCRIPT:{tool}-prog.tcl'
        self.conf['prog_ext'] = 'tcl'

    def _make_custom(self):
        info = get_info(self.data.get('part', 'mpf100t-1-fcg484'))
        self.data['family'] = info['family']
        self.data['device'] = info['device']
        self.data['speed'] = info['speed']
        self.data['package'] = info['package']
        self.data['prange'] = info['prange']


# pylint: disable=duplicate-code

def get_info(part):
    """Get info about the FPGA part.

    :param part: the FPGA part as specified by the tool
    :returns: a dict with the keys family, device, speed, package and prange
    """
    part = part.lower().replace(' ', '')
    # Looking for the family
    family = None
    families = {
        r'm2s': 'SmartFusion2',
        r'm2gl': 'IGLOO2',
        r'rt4g': 'RTG4',
        r'mpfs': 'PolarFireSoC',
        r'mpf': 'PolarFire',
        r'a2f': 'SmartFusion',
        r'afs': 'Fusion',
        r'aglp': 'IGLOO+',
        r'agle': 'IGLOOE',
        r'agl': 'IGLOO',
        r'a3p\d+l': 'ProAsic3L',
        r'a3pe': 'ProAsic3E',
        r'a3p': 'ProAsic3'
    }
    for key, value in families.items():
        if re.match(key, part):
            family = value
            break
    # Looking for the other values
    device = None
    speed = None
    package = None
    prange = None
    aux = part.split('-')
    if len(aux) == 2:
        device = aux[0]
        package = aux[1]
        if package[0].isdigit():
            speed = f'-{package[0]}'
            package = package[1:]
        else:
            speed = 'STD'
    elif len(aux) == 3:
        device = aux[0]
        if len(aux[1]) < len(aux[2]):
            speed = f'-{aux[1]}'
            package = aux[2]
        else:
            speed = f'-{aux[2]}'
            package = aux[1]
    else:
        valid = 'DEVICE-[SPEED][-]PACKAGE[PRANGE][-SPEED]'
        raise ValueError(f'Invalid PART format ({valid})')
    pranges = {
        'c': 'COM',
        'e': 'EXT',
        'i': 'IND',
        'm': 'MIL',
        't1': 'TGrade1',
        't2': 'TGrade2'
    }
    prange = 'COM'
    for suffix, name in pranges.items():
        if package.endswith(suffix):
            package = package[:-len(suffix)]
            prange = name
            break
    # Finish
    return {
        'family': family,
        'device': device,
        'speed': speed,
        'package': package,
        'prange': prange
    }
