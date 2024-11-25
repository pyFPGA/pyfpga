#!/usr/bin/env python3
#
# Copyright (C) 2020-2024 PyFPGA Project
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
A CLI helper utility to deal with a vendor FPGA Project file.
"""

import argparse
import sys

from pathlib import Path
from pyfpga import __version__ as version
from pyfpga.factory import Factory, TOOLS
from pyfpga.project import STEPS

steps = list(STEPS.keys())[1:len(STEPS)]


def main():
    """Solves the main functionality of this helper."""

    # Parsing the command-line.

    parser = argparse.ArgumentParser(
        description=__doc__
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'v{version}'
    )

    parser.add_argument(
        '--last',
        metavar='STEP',
        choices=steps,
        default='bit',
        help=f'last step to perform [{steps[-1]}] ({"|".join(steps)})'
    )

    parser.add_argument(
        'prjfile',
        metavar='PRJFILE',
        help='a vendor Project File'
    )

    args = parser.parse_args()

    # Detecting a Project file

    tool_per_ext = {
        '.xise': 'ise',
        '.prjx': 'libero',
        '.qpf': 'quartus',
        '.xpr': 'vivado'
    }

    prjfile = Path(args.prjfile)

    if not prjfile.exists():
        sys.exit(f'ERROR: {prjfile} file not found.')

    directory = prjfile.parent
    base_name = prjfile.stem
    extension = prjfile.suffix

    tool = ''
    if extension in tool_per_ext:
        tool = tool_per_ext[extension]
        print(f'INFO: {tool} project file found.')
    else:
        sys.exit(f'ERROR: unknown project file extension ({extension})')

    # -------------------------------------------------------------------------
    # Solving with PyFPGA
    # -------------------------------------------------------------------------

    prj = Factory(tool, base_name, directory)

    try:
        prj.make('syn', args.last)
    except Exception as e:
        sys.exit('{} ({})'.format(type(e).__name__, e))


if __name__ == "__main__":
    main()
