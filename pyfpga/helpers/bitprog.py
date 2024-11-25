#!/usr/bin/env python3
#
# Copyright (C) 2020-2024 PyFPGA Project
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
A CLI helper utility to transfer a bitstream to a supported device.
"""

import argparse
import sys

from pathlib import Path
from pyfpga import __version__ as version
from pyfpga.factory import Factory, TOOLS
from pyfpga.project import STEPS

tools = list(TOOLS.keys())
devs = ['fpga', 'spi', 'bpi']
positions = range(1, 10)
widths = [2**i for i in range(6)]

EPILOGUE = f"""
Supported values of arguments with choices:
* TOOL = {'|'.join(tools)}
* TYPE = {'|'.join(devs)}
* POSITION = {'|'.join(map(str, positions))}
* WIDTH = {'|'.join(map(str, widths))}
"""


def main():
    """Solves the main functionality of this helper."""

    # Parsing the command-line.

    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=EPILOGUE,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'v{version}'
    )

    parser.add_argument(
        '-t', '--tool',
        metavar='TOOL',
        default='vivado',
        choices=tools,
        help='backend tool to be used [vivado]'
    )

    parser.add_argument(
        '-o', '--odir',
        metavar='PATH',
        default='results',
        help='where to generate files [results]'
    )

    parser.add_argument(
        '-d', '--device',
        metavar='TYPE',
        choices=devs,
        default=devs[0],
        help=f'the target device type [{devs[0]}]'
    )

    parser.add_argument(
        '-p', '--position',
        metavar='POSITION',
        choices=positions,
        type=int,
        default=1,
        help='the device position into the JTAG chain [1]'
    )

    parser.add_argument(
        '-m', '--memname',
        metavar='NAME',
        help='memory name for SPI or BPI devices [None]'
    )

    parser.add_argument(
        '-w', '--width',
        metavar='WIDTH',
        choices=widths,
        type=int,
        default=1,
        help='memory width for SPI or BPI devices [1]'
    )

    parser.add_argument(
        'bit',
        metavar='BITFILE',
        help='a bitstream file'
    )

    args = parser.parse_args()

    # -------------------------------------------------------------------------
    # Solving with PyFPGA
    # -------------------------------------------------------------------------

    prj = Factory(args.tool, odir=args.odir)

    try:
        if args.device == 'fpga':
            prj.prog(args.bit, args.position)
        if args.device == 'spi':
            prj.prog_spi(args.bit, args.position, args.width, args.memname)
        if args.device == 'bpi':
            prj.prog_bpi(args.bit, args.position, args.width, args.memname)
    except Exception as e:
        sys.exit('{} ({})'.format(type(e).__name__, e))


if __name__ == "__main__":
    main()
