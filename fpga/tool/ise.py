#
# Copyright (C) 2019 INTI
# Copyright (C) 2019 Rodrigo A. Melo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""fpga.tool.ise

Implements the support of ISE (Xilinx).
"""

from fpga.tool import Tool

_TEMPLATES = {
    'fpga': """\
set impact_fpga "setMode -bs
setCable -port auto
Identify -inferir
assignFile -p #POSITION# -file #BITSTREAM#
Program -p #POSITION#
""",
    'spi': """\
setMode -pff
addConfigDevice -name #NAME# -path .
setSubmode -pffspi
addDesign -version 0 -name 0
addDeviceChain -index 0
addDevice -p 1 -file #BITSTREAM#
generate -generic

setMode -bs
setCable -port auto
Identify
attachflash -position #POSITION# -spi #NAME#
assignfiletoattachedflash -position #POSITION# -file ./#NAME#.mcs
Program -p #POSITION# -dataWidth #WIDTH# -spionly -e -v -loadfpga

quit
""",
    'bpi': """\
setMode -pff
addConfigDevice -name #NAME# -path .
setSubmode -pffbpi
addDesign -version 0 -name 0
addDeviceChain -index 0
setAttribute -configdevice -attr flashDataWidth -value #WIDTH#
addDevice -p 1 -file #BITSTREAM#
generate -generic

setMode -bs
setCable -port auto
Identify
attachflash -position #POSITION# -bpi #NAME#
assignfiletoattachedflash -position #POSITION# -file ./#NAME#.mcs
Program -p #POSITION# -dataWidth #WIDTH# \
-rs1 NONE -rs0 NONE -bpionly -e -v -loadfpga

quit
""",
    'detect': """\
setMode -bs
setCable -port auto
Identify -inferir
""",
    'unlock': 'set impact_unlock "cleancablelock"'
}


class Ise(Tool):
    """Implementation of the class to support ISE."""

    _TOOL = 'ise'
    _EXTENSION = 'xise'
    _PART = 'XC6SLX9-2-CSG324'

    _GEN_COMMAND = 'xtclsh ise.tcl'
    _TRF_COMMAND = 'impact -batch ise-prog.impact'

    _DEVTYPES = ['fpga', 'spi', 'bpi', 'xcf', 'detect', 'unlock']

    def transfer(self, devtype, position, part, width):
        super().transfer(devtype, position, part, width)
        raise NotImplementedError('transfer(ise)')
