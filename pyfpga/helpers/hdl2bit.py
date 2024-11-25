#!/usr/bin/env python3
#
# Copyright (C) 2020-2024 PyFPGA Project
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
A CLI helper utility to transform HDL design files into a bitstream.
"""

import argparse
import sys

from pathlib import Path
from pyfpga import __version__ as version
from pyfpga.factory import Factory, TOOLS
from pyfpga.project import STEPS

tools = list(TOOLS.keys())
steps = list(STEPS.keys())

EPILOGUE = f"""
Supported values of arguments with choices:
* TOOL = {'|'.join(tools)}
* STEP = {'|'.join(steps)}

Notes:
* PATH and FILE must be relative to the execution directory.
* The default PART name and how to specify it depends on the selected TOOL.
* More than one '--file', '--include' or '--param' arguments can be specified.
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
        '-p', '--part',
        metavar='PART',
        help='the target device'
    )

    parser.add_argument(
        '-f', '--file',
        metavar='FILE[,LIBRARY]',
        action='append',
        help='add a design file (optionally specifying a VHDL library)'
    )

    parser.add_argument(
        '-i', '--include',
        metavar='PATH',
        action='append',
        help='specify a Verilog Include directory'
    )

    parser.add_argument(
        '--define',
        metavar=('DEFINE', 'VALUE'),
        action='append',
        nargs=2,
        help='define and set the value of a Verilog Define'
    )

    parser.add_argument(
        '--param',
        metavar=('PARAMETER', 'VALUE'),
        action='append',
        nargs=2,
        help='set the value of a Generic/Parameter of the top-level'
    )

    parser.add_argument(
        '--project',
        metavar='PROJECT',
        help='optional PROJECT name'
    )

    parser.add_argument(
        '--last',
        metavar='STEP',
        choices=steps,
        default='bit',
        help=f'last step to perform [{steps[-1]}] ({"|".join(steps)})'
    )

    parser.add_argument(
        'toplevel',
        metavar='TOPLEVEL',
        help='the top-level name'
    )

    args = parser.parse_args()

    # -------------------------------------------------------------------------
    # Solving with PyFPGA
    # -------------------------------------------------------------------------

    project = args.project or args.tool

    prj = Factory(args.tool, project, odir=args.odir)

    if args.part is not None:
        prj.set_part(args.part)

    if args.include is not None:
        for include in args.include:
            prj.add_include(include)

    if args.file is not None:
        for file in args.file:
            aux = file.split(',')
            file = aux[0]
            lib = aux[1] if len(aux) > 1 else None
            ext = Path(file).suffix.lower()
            if ext == '.v':
                print(f'* Adding Verilog file: {file}')
                prj.add_vlog(file)
            elif ext == '.sv':
                print(f'* Adding System Verilog file: {file}')
                prj.add_slog(file)
            elif ext in ['.vhd', '.vhdl']:
                if lib:
                    print(f'* Adding VHDL file: {file} (library={lib})')
                else:
                    print(f'* Adding VHDL file: {file}')
                prj.add_vhdl(file, lib)
            else:
                print(f'* Adding Constraint file: {file}')
                prj.add_cons(file)

    if args.define is not None:
        for define in args.define:
            prj.add_define(define[0], define[1])

    if args.param is not None:
        for param in args.param:
            prj.add_param(param[0], param[1])

    prj.set_top(args.toplevel)

    try:
        prj.make(last=args.last)
    except Exception as e:
        sys.exit('{} ({})'.format(type(e).__name__, e))


if __name__ == "__main__":
    main()
