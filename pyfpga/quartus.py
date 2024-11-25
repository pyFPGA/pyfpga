#
# Copyright (C) 2019-2024 PyFPGA Project
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for Quartus.
"""

from pyfpga.project import Project


class Quartus(Project):
    """Class to support Quartus projects."""

    def _configure(self):
        tool = 'quartus'
        self.conf['tool'] = tool
        self.conf['make_cmd'] = f'quartus_sh --script {tool}.tcl'
        self.conf['make_ext'] = 'tcl'
        self.conf['prog_bit'] = ['sof', 'pof']
        self.conf['prog_cmd'] = f'bash {tool}-prog.tcl'
        self.conf['prog_ext'] = 'tcl'

    def _make_custom(self):
        if 'part' not in self.data:
            self.data['part'] = '10M50SCE144I7G'
