Tools
=====

.. list-table:: Default PyFPGA's parts per tool
   :header-rows: 1

   * - Tool
     - Vendor
     - Default device
     - Name format
   * - Diamond
     - Lattice
     - LFXP2-5E-5TN144C
     - device-speed-package
   * - ISE
     - Xilinx
     - XC7K160T-3-FBG484
     - device-speed-package
   * - Libero
     - Microchip/Microsemi
     - MPF100T-1-FCG484
     - device-speed-package
   * - Openflow
     - FLOSS
     - HX8K-CT256
     - device-package
   * - Quartus
     - Intel/Altera
     - 10M50SCE144I7G
     - part
   * - Vivado
     - AMD/Xilinx
     - XC7K160T-3-FBG484
     - device-speed-package

Diamond
-------

`Diamond downloads <https://www.latticesemi.com/latticediamond>`_

Diamond is the previous generation EDA tool from Lattice.

Example:

.. code::

   from pyfpga.diamond import Diamond

   prj = Diamond()

ISE
---

`ISE downloads <https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vivado-design-tools/archive-ise.html>`_

ISE (*Integrated Software Environment*) is the previous Xilinx's EDA, superseded by Vivado.
The last version is ISE 14.7, launched in October 2013.
It supports devices starting from Spartan 3/Virtex 4 until some of the first members of the 7 series (all the 7 series and above are supported by Vivado).
Previous Spartan/Virtex devices were supported until version 10.

.. attention::

   ISE supports Verilog 2001 and VHDL 1993, but not SystemVerilog.

Example:

.. code::

   from pyfpga.ise import Ise

   prj = Ise()

Valid PART formats:

.. code::

   <DEVICE>-<SPEED>-<PACKAGE>
   <DEVICE>-<PACKAGE>-<SPEED>

Libero
------

`Libero downloads <https://www.microchip.com/en-us/products/fpgas-and-plds/fpga-and-soc-design-tools/fpga/libero-software-later-versions>`_

Libero-SoC (Microsemi, acquired by Microchip in 2018) is the evolution of Libero-IDE (Actel, acquired by Microsemi in 2010).
PyFPGA supports Libero-SoC starting from 12.0, which supports most modern families.
For other devices, Libero-SoC 11.9 or Libero-IDE v9.2 are needed, but these versions are not supported by PyFPGA.

Example:

.. code::

   from pyfpga.libero import Libero

   prj = Libero()

Valid PART formats:

.. code::

   <DEVICE>-<PACKAGE>
   <DEVICE>-<SPEED><PACKAGE>
   <DEVICE>-<SPEED>-<PACKAGE>
   <DEVICE>-<PACKAGE>-<SPEED>
   <DEVICE>-<PACKAGE><RANGE>
   <DEVICE>-<SPEED><PACKAGE><RANGE>
   <DEVICE>-<SPEED>-<PACKAGE><RANGE>
   <DEVICE>-<PACKAGE><RANGE>-<SPEED>

Openflow
--------

`Docker downloads <https://docs.docker.com/engine/install/>`_

Openflow is the combination of different Free/Libre and Open Source (FLOSS) tools:

.. image:: images/openflow.svg
   :width: 70%
   :align: center

* Yosys for synthesis, with ghdl-yosys-plugin for VHDL support.
* nextpnr in its ice40 and ecp5 versions.
* Projects icestorm and Trellis.

It relies on Docker and fine-grain containers.

.. attention::

   It is currently the only flow not solved using Tcl (it uses docker in a bash script instead).

Example:

.. code::

   from pyfpga.openflow import Openflow

   prj = Openflow()

Valid PART formats:

.. code::

   <DEVICE>-<PACKAGE>

Quartus
-------

`Quartus downloads <https://www.intel.com/content/www/us/en/products/details/fpga/development-tools/quartus-prime/resource.html>`_

Quartus Prime (Intel) is the continuation of Quartus II (Altera) and is divided into the Pro, Standard, and Lite editions, each supporting different families.

Example:

.. code::

   from pyfpga.quartus import Quartus

   prj = Quartus()

Vivado
------

`Vivado downloads <https://www.xilinx.com/support/download.html>`_

Vivado is the current EDA tool from Xilinx, which has superseded ISE and supports the 7 series and above.
It is included with Vitis, the SDK for embedded applications.

Example:

.. code::

   from pyfpga.vivado import Vivado

   prj = Vivado()
