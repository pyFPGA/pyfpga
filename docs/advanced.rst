Advanced usage
==============

The flow implemented by PyFPGA should be sufficient for most cases, but further customizations are possible and discussed in this section.

Hooks
-----

Hooks allow you to insert custom code at specific stages of the project lifecycle. The available hooks are:

+---------+---------------------------------------------------------------------------------------------+
| Stage   | Description                                                                                 |
+=========+=============================================================================================+
| precfg  | Code inserted after project creation and before files inclusion (e.g., specify HDL version) |
+---------+---------------------------------------------------------------------------------------------+
| postcfg | Code inserted after files inclusion (e.g., additional project configurations)               |
+---------+---------------------------------------------------------------------------------------------+
| presyn  | Code inserted before synthesis (e.g., synthesis-specific options)                           |
+---------+---------------------------------------------------------------------------------------------+
| postsyn | Code inserted after synthesis (e.g., report generation)                                     |
+---------+---------------------------------------------------------------------------------------------+
| prepar  | Code inserted before place and route (e.g., place-and-route-specific options)               |
+---------+---------------------------------------------------------------------------------------------+
| postpar | Code inserted after place and route (e.g., report generation)                               |
+---------+---------------------------------------------------------------------------------------------+
| prebit  | Code inserted before bitstream generation (e.g., bitstream-specific options)                |
+---------+---------------------------------------------------------------------------------------------+
| postbit | Code inserted after bitstream generation (e.g., report generation)                          |
+---------+---------------------------------------------------------------------------------------------+

You can specify hooks for a specific stage either line-by-line:

.. code-block:: python

   prj.add_hook('presyn', 'COMMAND1')
   prj.add_hook('presyn', 'COMMAND2')
   prj.add_hook('presyn', 'COMMAND3')

Or in a multi-line format:

.. code-block:: python

   prj.add_hook('presyn', """
   COMMAND1
   COMMAND2
   COMMAND3
   """)

Options
-------

Options allow you to specify additional settings to fine-tune certain commands. The available options are:

.. ATTENTION::

   This feature is WIP.
