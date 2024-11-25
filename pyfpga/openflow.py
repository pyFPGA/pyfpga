#
# Copyright (C) 2020-2024 PyFPGA Project
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for an Open Source development flow.
"""

from pyfpga.project import Project


class Openflow(Project):
    """Class to support Open Source tools."""

    def _configure(self):
        tool = 'openflow'
        self.conf['tool'] = tool
        self.conf['make_cmd'] = f'bash {tool}.sh'
        self.conf['make_ext'] = 'sh'
        self.conf['prog_bit'] = ['svf', 'bit']
        self.conf['prog_cmd'] = f'bash {tool}-prog.sh'
        self.conf['prog_ext'] = 'sh'

    def _make_custom(self):
        info = get_info(self.data.get('part', 'hx8k-ct256'))
        self.data['family'] = info['family']
        self.data['device'] = info['device']
        self.data['package'] = info['package']

    def _prog_custom(self):
        info = get_info(self.data.get('part', 'hx8k-ct256'))
        self.data['family'] = info['family']


def get_info(part):
    """Get info about the FPGA part.

    :param part: the FPGA part as specified by the tool
    :returns: a dict with the keys family, device and package
    """
    part = part.lower().replace(' ', '')
    # Looking for the family
    family = None
    families = [
        # From <YOSYS>/techlibs/xilinx/synth_xilinx.cc
        'xcup', 'xcu', 'xc7', 'xc6s', 'xc6v', 'xc5v', 'xc4v', 'xc3sda',
        'xc3sa', 'xc3se', 'xc3s', 'xc2vp', 'xc2v', 'xcve', 'xcv'
    ]
    for item in families:
        if part.startswith(item):
            family = item
            break
    families = [
        # From <nextpnr>/ice40/main.cc
        'lp384', 'lp1k', 'lp4k', 'lp8k', 'hx1k', 'hx4k', 'hx8k',
        'up3k', 'up5k', 'u1k', 'u2k', 'u4k'
    ]
    if part.startswith(tuple(families)):
        family = 'ice40'
    families = [
        # From <nextpnr>/ecp5/main.cc
        '12k', '25k', '45k', '85k', 'um-25k', 'um-45k', 'um-85k',
        'um5g-25k', 'um5g-45k', 'um5g-85k'
    ]
    if part.startswith(tuple(families)):
        family = 'ecp5'
    # Looking for the other values
    device = None
    package = None
    aux = part.split('-')
    if len(aux) == 2:
        device = aux[0]
        package = aux[1]
    elif len(aux) == 3:
        device = f'{aux[0]}-{aux[1]}'
        package = aux[2]
    else:
        valid = 'DEVICE-PACKAGE'
        raise ValueError(f'Invalid PART format ({valid})')
    if family in ['lp4k', 'hx4k']:  # See http://www.clifford.at/icestorm
        device = device.replace('4', '8')
        package += ":4k"
    if family == 'ecp5':
        package = package.upper()
    # Finish
    return {
        'family': family,
        'device': device,
        'package': package
    }
