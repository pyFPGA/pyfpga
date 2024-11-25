#
# Copyright (C) 2024 PyFPGA Project
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for Diamond.
"""

import os
from pyfpga.project import Project


class Diamond(Project):
    """Class to support Diamond projects."""

    def _configure(self):
        tool = 'diamond'
        executable = 'pnmainc' if os.name == 'nt' else 'diamondc'
        self.conf['tool'] = tool
        self.conf['make_cmd'] = f'{executable} {tool}.tcl'
        self.conf['make_ext'] = 'tcl'
        self.conf['prog_bit'] = ['bit']
        self.conf['prog_cmd'] = f'sh {tool}-prog.sh'
        self.conf['prog_ext'] = 'sh'

    def _make_custom(self):
        if 'part' not in self.data:
            self.data['part'] = 'LFXP2-5E-5TN144C'
