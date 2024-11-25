Extending
=========

.. note::

   All <TOOL> classes inherit from ``Project`` (``project.py``).

This is a guide on how to add support for a new TOOL.

Add support for the new tool
----------------------------

.. code-block:: bash

   pyfpga/templates/<NEWTOOL>.jinja
   pyfpga/templates/<NEWTOOL>-prog.jinja
   pyfpga/<NEWTOOL>.py
   pyfpga/factory.py # UPDATE
   pyfpga/helpers/prj2bit.py # UPDATE

Add tests and a tool mock-up
----------------------------

.. code-block:: bash

   tests/test_tools.py # UPDATE
   tests/support.py # UPDATE if exceptions are needed
   tests/mocks/<NEWCOMMAND>

Add examples
------------

.. code-block:: bash

   examples/sources/cons/<NEWBOARD>/timing.<EXT>
   examples/sources/cons/<NEWBOARD>/clk.<EXT>
   examples/sources/cons/<NEWBOARD>/led.<EXT>
   examples/projects/<NEWTOOL>.py
   examples/projects/regress.sh # UPDATE
   examples/helpers/<NEWTOOL>.sh
   examples/hooks/<NEWTOOL>.py # OPTIONAL

Verify the code
---------------

Run it at the root of the repo.

.. code-block:: bash

   make docs
   make lint
   make test

.. tip::

   You can simply run ``make`` to perform all the operations.
   Running ``make clean`` will remove all the generated files.

Verify the functionality
------------------------

.. code-block:: bash

   cd examples/projects/
   bash regress.sh <NEWTOOL>
   cd ../../tests/
   python3 support.py --tool <NEWTOOL>

Updated the documentation
-------------------------

.. code-block:: bash

   README.md
   docs/intro.rst
   docs/tools.rst
