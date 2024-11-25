#
# Copyright (C) 2019-2024 PyFPGA Project
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Base class that implements agnostic methods to deal with FPGA projects.
"""

import glob
import logging
import os
import subprocess

from pathlib import Path
from time import time
from jinja2 import Environment, FileSystemLoader


STEPS = {
    'cfg': 'Project Creation',
    'syn': 'Synthesis',
    'par': 'Place and Route',
    'bit': 'Bitstream generation'
}


class Project:
    """Base class to manage an FPGA project.

    :param project: project name (tool name when nothing specified)
    :type project: str, optional
    :param odir: output directory
    :type odir: str, optional
    """

    def __init__(self, project=None, odir='results'):
        """Class constructor."""
        self.conf = {}
        self.data = {}
        self._configure()
        self.data['project'] = project or self.conf['tool']
        self.odir = odir
        # logging config
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def set_part(self, name):
        """Set the FPGA part name.

        :param name: FPGA part name
        :type name: str
        """
        self.logger.debug('Executing set_part: %s', name)
        self.data['part'] = name

    def add_include(self, path):
        """Add an Include path.

        Specify where to search for Included Verilog Files, IP repos, etc.

        :param path: path of a directory
        :type name: str
        :raises NotADirectoryError: if path is not a directory
        """
        self.logger.debug('Executing add_include: %s', path)
        path = Path(path).resolve()
        if not path.is_dir():
            raise NotADirectoryError(path)
        self.data.setdefault('includes', []).append(path.as_posix())

    def _add_file(self, pathname, hdl=None, lib=None):
        files = glob.glob(pathname, recursive=True)
        if len(files) == 0:
            raise FileNotFoundError(pathname)
        for file in files:
            path = Path(file).resolve().as_posix()
            attr = {}
            if hdl:
                attr['hdl'] = hdl
            if lib:
                attr['lib'] = lib
            if path in self.data.get('files', {}):
                del self.data['files'][path]
            self.data.setdefault('files', {})[path] = attr

    def add_slog(self, pathname):
        """Add System Verilog file/s.

        :param pathname: path to a SV file (glob compliant)
        :type pathname: str
        :raises FileNotFoundError: when pathname is not found
        """
        self.logger.debug('Executing add_slog: %s', pathname)
        self._add_file(pathname, 'slog')

    def add_vhdl(self, pathname, lib=None):
        """Add VHDL file/s.

        :param pathname: path to a SV file (glob compliant)
        :type pathname: str
        :param lib: VHDL library name
        :type lib: str, optional
        :raises FileNotFoundError: when pathname is not found
        """
        lib_str = 'default library' if lib is None else lib
        self.logger.debug('Executing add_vhdl: %s : %s', lib_str, pathname)
        self._add_file(pathname, 'vhdl', lib)

    def add_vlog(self, pathname):
        """Add Verilog file/s.

        :param pathname: path to a SV file (glob compliant)
        :type pathname: str
        :raises FileNotFoundError: when pathname is not found
        """
        self.logger.debug('Executing add_vlog: %s', pathname)
        self._add_file(pathname, 'vlog')

    def add_cons(self, path):
        """Add a constraint file.

        :param pathname: path of a file
        :type pathname: str
        :raises FileNotFoundError: if path is not found
        """
        self.logger.debug('Executing add_cons: %s', path)
        path = Path(path).resolve()
        if not path.is_file():
            raise FileNotFoundError(path)
        attr = {}
        self.data.setdefault('constraints', {})[path.as_posix()] = attr

    def add_param(self, name, value):
        """Add a Parameter/Generic Value.

        :param name: parameter/generic name
        :type name: str
        :param value: parameter/generic value
        :type name: str
        """
        self.logger.debug('Executing add_param: %s : %s', name, value)
        self.data.setdefault('params', {})[name] = value

    def add_define(self, name, value):
        """Add a Verilog Defile Value.

        :param name: define name
        :type name: str
        :param value: define value
        :type name: str
        """
        self.logger.debug('Executing add_define: %s : %s', name, value)
        self.data.setdefault('defines', {})[name] = value

    def add_fileset(self, pathname):
        """Add fileset file/s.

        :param pathname: path to a fileset file
        :type pathname: str
        :raises FileNotFoundError: when pathname is not found
        """
        self.logger.debug('Executing add_fileset: %s', pathname)
        if not os.path.exists(pathname):
            raise FileNotFoundError(pathname)
        raise NotImplementedError()

    def set_top(self, name):
        """Set the name of the top level component.

        :param name: top-level name
        :type name: str
        """
        self.logger.debug('Executing set_top: %s', name)
        self.data['top'] = name

    def add_hook(self, stage, hook):
        """Add a hook in the specific stage.

        A hook is a place that allows you to insert customized code.

        :param stage: where to insert the hook
        :type stage: str
        :param hook: a tool-specific command
        :type hook: str
        :raises ValueError: when stage is invalid
        """
        self.logger.debug('Executing add_hook: %s : %s', stage, hook)
        stages = [
            'precfg', 'postcfg', 'presyn', 'postsyn',
            'prepar', 'postpar', 'prebit', 'postbit'
        ]
        if stage not in stages:
            raise ValueError('Invalid stage.')
        self.data.setdefault('hooks', {}).setdefault(stage, []).append(hook)

    def set_debug(self):
        """Enables debug messages."""
        self.logger.setLevel(logging.DEBUG)

    def make(self, first='cfg', last='bit'):
        """Run the underlying tool.

        :param first: first step
        :type first: str, optional
        :param last: last step
        :type last: str, optional
        :raises ValueError: for missing or wrong values
        :raises RuntimeError: error running the needed underlying tool

        .. note:: valid steps are ``cfg``, ``syn``, ``par`` and ``bit``.
        """
        self.logger.debug('Executing make')
        if last not in STEPS:
            raise ValueError('Invalid last step.')
        if first not in STEPS:
            raise ValueError('Invalid first step.')
        keys = list(STEPS.keys())
        index = [keys.index(first), keys.index(last)]
        if index[0] > index[1]:
            raise ValueError('Invalid steps combination.')
        message = f'from {STEPS[first]} to {STEPS[last]}'
        if first == last:
            message = STEPS[first]
        self.logger.info('Running %s', message)
        self.data['steps'] = keys[index[0]:index[1]+1]
        self._make_custom()
        self._create_file(self.conf['tool'], self.conf['make_ext'])
        self._run(self.conf['make_cmd'], 'make.log')

    def prog(self, bitstream=None, position=1):
        """Program the FPGA

        :param bitstream: bitstream to be programmed
        :type bitstream: str, optional
        :param position: position of the device in the JTAG chain
        :type position: str, optional
        :raises ValueError: for missing or wrong values
        :raises FileNotFoundError: when bitstream is not found
        :raises RuntimeError: error running the needed underlying tool
        """
        self.logger.debug('Executing prog')
        if position not in range(1, 9):
            raise ValueError('Invalid position.')
        self.logger.info('Programming')
        if not bitstream:
            for ext in self.conf['prog_bit']:
                candidate = Path(self.odir) / f'{self.data["project"]}.{ext}'
                if candidate.exists():
                    bitstream = candidate.resolve()
                    break
        else:
            bitstream = Path(bitstream).resolve()
        if not bitstream or not bitstream.exists():
            raise FileNotFoundError(bitstream)
        self.data['bitstream'] = bitstream
        self._prog_custom()
        self._create_file(f'{self.conf["tool"]}-prog', self.conf['prog_ext'])
        self._run(self.conf['prog_cmd'], 'prog.log')

    def _configure(self):
        raise NotImplementedError('Tool-dependent')

    def _make_custom(self):
        pass

    def _prog_custom(self):
        pass

    def _create_file(self, basename, extension):
        tempdir = Path(__file__).parent.joinpath('templates')
        jinja_file_loader = FileSystemLoader(str(tempdir))
        jinja_env = Environment(loader=jinja_file_loader)
        jinja_template = jinja_env.get_template(f'{basename}.jinja')
        content = jinja_template.render(self.data)
        directory = Path(self.odir)
        directory.mkdir(parents=True, exist_ok=True)
        filename = f'{basename}.{extension}'
        with open(directory / filename, 'w', encoding='utf-8') as file:
            file.write(content)

    def _run(self, command, logname):
        num = 20
        error = 0
        old_dir = Path.cwd()
        new_dir = Path(self.odir)
        start = time()
        try:
            os.chdir(new_dir)
            with open(logname, 'w', encoding='utf-8') as file:
                subprocess.run(
                    command, shell=True, check=True, text=True,
                    stdout=file, stderr=subprocess.STDOUT
                )
        except subprocess.CalledProcessError:
            with open(logname, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                last_lines = lines[-num:] if len(lines) >= num else lines
                for line in last_lines:
                    message = line.strip()
                    if len(message):
                        print(f'>> {message}')
            error = 1
        finally:
            os.chdir(old_dir)
            end = time()
            elapsed = end - start
            self.logger.info(
                'Elapsed time %dh %dm %.2fs',
                int(elapsed // 3600),
                int((elapsed % 3600) // 60),
                elapsed % 60
            )
            if error:
                raise RuntimeError('Problem with the underlying tool')
