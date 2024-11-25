#
# Copyright (C) 2024 PyFPGA Project
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
A factory class to create FPGA projects.
"""

# pylint: disable=too-few-public-methods

from pyfpga.diamond import Diamond
from pyfpga.ise import Ise
from pyfpga.libero import Libero
from pyfpga.openflow import Openflow
from pyfpga.quartus import Quartus
from pyfpga.vivado import Vivado


TOOLS = {
    'diamond': Diamond,
    'ise': Ise,
    'libero': Libero,
    'openflow': Openflow,
    'quartus': Quartus,
    'vivado': Vivado
}


class Factory:
    """A factory class to create FPGA projects."""

    def __init__(self, tool='vivado', project=None, odir='results'):
        """Class constructor."""
        if tool not in TOOLS:
            raise NotImplementedError(f'{tool} is unsupported')
        self._instance = TOOLS[tool](project, odir)

    def __getattr__(self, name):
        """Delegate attribute access to the tool instance."""
        return getattr(self._instance, name)
