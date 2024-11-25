Introduction
============

PyFPGA is a Python package that provides an abstraction layer for working with FPGA development tools in a vendor-agnostic, programmatic way. It includes:

* A **class** for each supported tool, enabling **project creation**, **synthesis**, **place and route**, **bitstream generation**, and **programming**.
* A set of **command-line** helpers for simple projects or quick evaluations.

With PyFPGA, you can create your own FPGA development workflow tailored to your needs. Some of its key benefits include:

* A unified API across different tools and devices.
* Compatibility with *Version Control Systems* and *Continuous Integration*.
* Ensured reproducibility and repeatability.
* Lower resource consumption compared to GUI-based workflows.

It currently supports vendor tools such as ``Diamond``, ``Ise``, ``Quartus``, ``Libero``, and ``Vivado``, as well as ``Openflow``, a solution based on *Free/Libre and Open Source Software* (**FLOSS**).

.. ATTENTION::

  PyFPGA assumes that the backend tool is ready to run.
  This implies, depending on the operating system, the following:

  * The tool is installed.
  * A valid license, if needed, is configured.
  * The tool is available in the system PATH.
  * On GNU/Linux: required packages are installed, environment variables are set, and permissions are granted for devices (to transfer the bitstream).
