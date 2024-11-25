#
# Copyright (C) 2019-2024 PyFPGA Project
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for Vivado.
"""

from pyfpga.project import Project


class Vivado(Project):
    """Class to support Vivado projects."""

    def _configure(self):
        tool = 'vivado'
        command = 'vivado -mode batch -notrace -quiet -source'
        self.conf['tool'] = tool
        self.conf['make_cmd'] = f'{command} {tool}.tcl'
        self.conf['make_ext'] = 'tcl'
        self.conf['prog_bit'] = ['bit']
        self.conf['prog_cmd'] = f'{command} {tool}-prog.tcl'
        self.conf['prog_ext'] = 'tcl'

    def _make_custom(self):
        if 'part' not in self.data:
            self.data['part'] = 'xc7k160t-3-fbg484'
