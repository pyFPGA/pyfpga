#
# Copyright (C) 2019-2024 PyFPGA Project
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for ISE.
"""

# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=duplicate-code

import re

from pyfpga.project import Project


class Ise(Project):
    """Class to support ISE projects."""

    def _make_prepare(self, steps):
        info = get_info(self.data.get('part', 'xc7k160t-3-fbg484'))
        context = {
            'project': self.name or 'ise',
            'family': info['family'],
            'device': info['device'],
            'speed': info['speed'],
            'package': info['package']
        }
        context['steps'] = steps
        context['includes'] = self.data.get('includes', None)
        context['files'] = self.data.get('files', None)
        context['constraints'] = self.data.get('constraints', None)
        context['top'] = self.data.get('top', None)
        context['defines'] = self.data.get('defines', None)
        context['params'] = self.data.get('params', None)
        context['hooks'] = self.data.get('hooks', None)
        self._create_file('ise', 'tcl', context)
        return 'xtclsh ise.tcl'

    def _prog_prepare(self, bitstream, position):
        if not bitstream:
            basename = self.name or 'ise'
            bitstream = f'{basename}.bit'
        context = {'bitstream': bitstream, 'position': position}
        self._create_file('vivado-prog', 'tcl', context)
        return 'impact -batch impact-prog'

    def add_slog(self, pathname):
        """Add System Verilog file/s."""
        raise NotImplementedError('ISE does not support SystemVerilog')


def get_info(part):
    """Get info about the FPGA part.

    :param part: the FPGA part as specified by the tool
    :returns: a dictionary with the keys family, device, speed and package
    """
    part = part.lower()
    # Looking for the family
    family = None
    families = {
        r'xc7a\d+l': 'artix7l',
        r'xc7a': 'artix7',
        r'xc7k\d+l': 'kintex7l',
        r'xc7k': 'kintex7',
        r'xc3sd\d+a': 'spartan3adsp',
        r'xc3s\d+a': 'spartan3a',
        r'xc3s\d+e': 'spartan3e',
        r'xc3s': 'spartan3',
        r'xc6s\d+l': 'spartan6l',
        r'xc6s': 'spartan6',
        r'xc4v': 'virtex4',
        r'xc5v': 'virtex5',
        r'xc6v\d+l': 'virtex6l',
        r'xc6v': 'virtex6',
        r'xc7v\d+l': 'virtex7l',
        r'xc7v': 'virtex7',
        r'xc7z': 'zynq'
    }
    for key, value in families.items():
        if re.match(key, part):
            family = value
            break
    # Looking for the device, package and speed
    device = None
    speed = None
    package = None
    aux = part.split('-')
    if len(aux) == 3:
        device = aux[0]
        if len(aux[1]) < len(aux[2]):
            speed = aux[1]
            package = aux[2]
        else:
            speed = aux[2]
            package = aux[1]
    else:
        raise ValueError(
            'Part must be DEVICE-SPEED-PACKAGE or DEVICE-PACKAGE-SPEED'
        )
    # Finish
    return {
        'family': family, 'device': device, 'speed': speed, 'package': package
    }
