Basic usage
===========

Project Configuration
---------------------

The first steps involve importing the necessary module to support the desired tool and instantiating the corresponding ``class``:

.. code-block:: python

   from pyfpga.vivado import Vivado

   prj = Vivado('PRJNAME', odir='OUTDIR')

In the example, we are using Vivado, specifying the optional parameters
``project name`` (``tool name`` if omitted) and ``output directory``
(``results`` by default).

Next step is to specify the target FPGA device:

.. code-block:: python

   prj.set_part('xc7k160t-3-fbg484')

.. note::

  Default parts are provided for each supported tool.

HDL source files are added using one of the following methods:

.. code-block:: python

   prj.add_vhdl('PATH_TO_FILES_GLOB_COMPATIBLE', 'OPTIONAL_LIBNAME')
   prj.add_vlog('PATH_TO_FILES_GLOB_COMPATIBLE')
   prj.add_slog('PATH_TO_FILES_GLOB_COMPATIBLE')

In these methods, you provide a path to the files. The path can include wildcards (like ``*.vhdl``), allowing you to match multiple files at once.
In case of ``add_vhdl``, you can also optionally specify a library name where the files will be included.

.. note::

   Internally, the methods that specify files use `glob`_ to support wildcards and `Path`_ to obtain absolute paths.

  .. _glob: https://docs.python.org/3/library/glob.html
  .. _Path: https://docs.python.org/3/library/pathlib.html

.. hint::

   Files are processed in the order they are added. If a file is specified more than once,
   it is removed from its previous position and placed at the end of the list.
   This allows you to ensure that a file is processed after others when necessary
   (e.g., placing a top-level at the end) or to customize options
   (e.g., removing a VHDL library specification in case of a top-level)
   when multiple files are added using a wildcard.

Generics/parameters can be specified with:

.. code-block:: python

   prj.add_param('PARAMNAME', 'PARAMVALUE')

For Verilog and SystemVerilog, the following methods are also available:

.. code-block:: python

   prj.add_include('PATH_TO_A_DIRECTORY')
   prj.add_define('DEFNAME', 'DEFVALUE')

Constraint source files are included using the following:

.. code-block:: python

   prj.add_cons('PATH_TO_FILES_GLOB_COMPATIBLE')

Finally, the top-level can be specified as follows:

.. code-block:: python

   prj.set_top('Top')

.. note::

   The order of the methods described in this section is not significant.
   They will be arranged in the required order by the underlying template.

Bitstream generation
--------------------

After configuring the project, you can run the following to generate a bitstream:

.. code-block:: python

   prj.make()

By default, this method performs **project creation**, **synthesis**, **place and route**,
and **bitstream generation**.
However, you can optionally specify both the initial and final stages, as follows:

.. code-block:: python

   prj.make(first='syn', last='par')

.. note::

   Valid values are:

   * ``cfg``: generates the project file
   * ``syn``: performs synthesis
   * ``par``: performs place and route
   * ``bit``: performs bitstream generation

.. note::

   After executing this method, you will find the file ``<TOOL>.tcl``
   (``<TOOL>.sh`` in some cases) in the output directory.
   For debugging purposes, if things do not work as expected, you can review this file.

Bitstream programming
---------------------

The final step is programming the FPGA:

.. code-block:: python

   prj.prog('BITSTREAM', 'POSITION')

Both ``BITSTREAM`` and ``POSITION`` are optional.
If ``BITSTREAM`` is not specified, PyFPGA will attempt to discover it based on project information.
The ``POSITION`` parameter is not always required (depends on the tool being used).

.. note::

   After executing this method, you will find the file ``<TOOL>prog.tcl``
   (``<TOOL>-prog.sh`` in some cases) in the output directory.
   For debugging purposes, if things do not work as expected, you can review this file.

Debugging
---------

Under the hood, `logging`_ is employed. To enable debug messages, you can use:

.. code-block:: python

   prj.set_debug()

.. _logging: https://docs.python.org/3/library/logging.html
