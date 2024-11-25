Internals
=========

Underlying steps
----------------

.. code-block::

   project creation [options]
   project configuration
   part
   precfg hook
   params
   defines
   includes
   files [options]
   top
   postcfg hook
   project close

   project open
   presyn hook
   synthesis [options]
   postsyn hook
   prepar hook
   place_and_route [options]
   postpar hook
   prebit hook
   bitstream [options]
   postbit hook
   project close

Internal data structure
-----------------------

.. code-block::

   data = {
       'part': 'PARTNAME',
       'includes': ['DIR1', 'DIR2', 'DIR3'],
       'files': {
           'FILE1': {'hdl': 'vhdl', 'lib': 'LIB1', 'opt': 'OPTS'},
           'FILE2': {'hdl': 'vlog', 'opt': 'OPTS'},
           'FILE3': {'hdl': 'slog', 'opt': 'OPTS'}
       },
       'top': 'TOPNAME',
       'constraints': {
           'FILE1': {'opt': 'OPTS'},
           'FILE2': {'opt': 'OPTS'},
           'FILE3': {'opt': 'OPTS'}
       },
       'params': {
           'PAR1': 'VAL1',
           'PAR2': 'VAL2',
           'PAR3': 'VAL3'
       },
       'defines': {
           'DEF1': 'VAL1',
           'DEF2': 'VAL2',
           'DEF3': 'VAL3'
       },
       'hooks': {
           'precfg': ['CMD1', 'CMD2'],
           'postcfg': ['CMD1', 'CMD2'],
           'presyn': ['CMD1', 'CMD2'],
           'postsyn': ['CMD1', 'CMD2'],
           'prepar': ['CMD1', 'CMD2'],
           'postpar': ['CMD1', 'CMD2'],
           'prebit': ['CMD1', 'CMD2'],
           'postbit': ['CMD1', 'CMD2']
       },
       'options': {
           'prj': 'OPTS',
           'syn': 'OPTS',
           'pre': 'OPTS',
           'pre': 'OPTS'
       }
   }
