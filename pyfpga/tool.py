#
# Copyright (C) 2019-2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""fpga.tool

Defines the interface to be inherited to support a tool.
"""


FILETYPES = ['verilog', 'vhdl', 'constraint', 'design']
MEMWIDTHS = [1, 2, 4, 8, 16, 32]
PHASES = ['prefile', 'project', 'preflow', 'postsyn', 'postpar', 'postbit']
TASKS = ['prj', 'syn', 'par', 'bit']

# def tcl_path(path):
#     """Returns a Tcl suitable path."""
#     return path.replace(os.path.sep, "/")

# pylint: disable=too-few-public-methods


class Tool:
    """Tool interface.

    It is the basic interface for tool implementations.
    """

#     # Following variables are set in each inheritance (if employed)
#     _TOOL = None         # tool name
#     _EXTENSION = None    # project file extension
#     _PART = None         # default device part name
#     _GEN_PROGRAM = None  # program used when generate is executed
#     _GEN_COMMAND = None  # command to run when generate is executed
#     _TRF_PROGRAM = None  # program used when transfer is executed
#     _TRF_COMMAND = None  # command to run when transfer is executed
#     _BIT_EXT = []        # Supported BITstream EXTensions
#     _DEVTYPES = []       # Supported DEVice TYPES
#     _CLEAN = []          # Files to be CLEAN

#     def __init__(self, project):
#         """Initializes the attributes of the class."""
#         self.bitstream = None
#         self.cmds = {
#             'prefile': [],
#             'project': [],
#             'preflow': [],
#             'postsyn': [],
#             'postpar': [],
#             'postbit': []
#         }
#         self.files = {
#             'vhdl': [],
#             'verilog': [],
#             'constraint': [],
#             'design': []
#         }
#         self.params = []
#         self.part = {
#             'name': 'UNSET',
#             'family': 'UNSET',
#             'device': 'UNSET',
#             'package': 'UNSET',
#             'speed': 'UNSET'
#         }
#         self.paths = []
#         self.presynth = False
#         self.project = self._TOOL if project is None else project
#         self.set_part(self._PART)
#         self.set_top('UNDEFINED')
#         self._configure()

#     def _configure(self):
#         """Configures the underlying tools."""
#         filename = '.pyfpga.yml'
#         self.configs = {}
#         if os.path.exists(filename):
#             with open(filename, 'r', encoding='utf-8') as file:
#                 data = safe_load(file)
#                 if self._TOOL in data:
#                     self.configs = data[self._TOOL]

#     def _create_gen_script(self, tasks):
#         """Create the script for generate execution."""
#         # Paths and files
#         files = []
#         if self.presynth:
#             files.append(f'    fpga_file {self.project}.edif')
#         else:
#             for path in self.paths:
#                 files.append(f'    fpga_include {tcl_path(path)}')
#             for file in self.files['verilog']:
#                 files.append(f'    fpga_file {tcl_path(file[0])}')
#             for file in self.files['vhdl']:
#                 if file[1] is None:
#                     files.append(f'    fpga_file {tcl_path(file[0])}')
#                 else:
#                     files.append(
#                         f'    fpga_file {tcl_path(file[0])} {file[1]}'
#                     )
#         for file in self.files['design']:
#             files.append(f'    fpga_design {tcl_path(file[0])}')
#         for file in self.files['constraint']:
#             files.append(f'    fpga_file {tcl_path(file[0])}')
#         # Parameters
#         params = []
#         for param in self.params:
#             params.append(f'{{ {param[0]} {param[1]} }}')
#         # Script creation
#         template = os.path.join(os.path.dirname(__file__), 'template.tcl')
#         with open(template, 'r', encoding='utf-8') as file:
#             tcl = file.read()
#         tcl = tcl.replace('#TOOL#', self._TOOL)
#         tcl = tcl.replace('#PRESYNTH#', "True" if self.presynth else "False")
#         tcl = tcl.replace('#PROJECT#', self.project)
#         tcl = tcl.replace('#PART#', self.part['name'])
#         tcl = tcl.replace('#FAMILY#', self.part['family'])
#         tcl = tcl.replace('#DEVICE#', self.part['device'])
#         tcl = tcl.replace('#PACKAGE#', self.part['package'])
#         tcl = tcl.replace('#SPEED#', self.part['speed'])
#         tcl = tcl.replace('#PARAMS#', ' '.join(params))
#         tcl = tcl.replace('#FILES#', '\n'.join(files))
#         tcl = tcl.replace('#TOP#', self.top)
#         tcl = tcl.replace('#TASKS#', tasks)
#         tcl = tcl.replace('#PREFILE_CMDS#', '\n'.join(self.cmds['prefile']))
#         tcl = tcl.replace('#PROJECT_CMDS#', '\n'.join(self.cmds['project']))
#         tcl = tcl.replace('#PREFLOW_CMDS#', '\n'.join(self.cmds['preflow']))
#         tcl = tcl.replace('#POSTSYN_CMDS#', '\n'.join(self.cmds['postsyn']))
#         tcl = tcl.replace('#POSTPAR_CMDS#', '\n'.join(self.cmds['postpar']))
#         tcl = tcl.replace('#POSTBIT_CMDS#', '\n'.join(self.cmds['postbit']))
#         with open(f'{self._TOOL}.tcl', 'w', encoding='utf-8') as file:
#             file.write(tcl)

#     def generate(self, to_task, from_task, capture):
#         """Run the FPGA tool."""
#         check_value(to_task, TASKS)
#         check_value(from_task, TASKS)
#         to_index = TASKS.index(to_task)
#         from_index = TASKS.index(from_task)
#         if from_index > to_index:
#             raise ValueError(
#                 f'initial task "{from_task}" cannot be later than the ' +
#                 f'last task "{to_task}"'
#             )
#         tasks = " ".join(TASKS[from_index:to_index+1])
#         self._create_gen_script(tasks)
#         if not which(self._GEN_PROGRAM):
#             raise RuntimeError(f'program "{self._GEN_PROGRAM}" not found')
#         return run(self._GEN_COMMAND, capture)

#     def transfer(self, devtype, position, part, width, capture):
#         """Transfer a bitstream."""
#         if not which(self._TRF_PROGRAM):
#             raise RuntimeError(f'program "{self._TRF_PROGRAM}" not found')
#         check_value(devtype, self._DEVTYPES)
#         check_value(position, range(10))
#         isinstance(part, str)
#         check_value(width, MEMWIDTHS)
#         isinstance(capture, bool)
#         # Bitstream autodiscovery
#         if not self.bitstream and devtype not in ['detect', 'unlock']:
#             bitstream = []
#             for ext in self._BIT_EXT:
#                 bitstream.extend(glob(f'**/*.{ext}', recursive=True))
#             if len(bitstream) == 0:
#                 raise FileNotFoundError('bitStream not found')
#             self.bitstream = bitstream[0]

#     def clean(self):
#         """Clean the generated project files."""
#         for path in self._CLEAN:
#             elements = glob(path)
#             for element in elements:
#                 if os.path.isfile(element):
#                     os.remove(element)
#                 else:
#                     rmtree(element)
