from setuptools import setup, find_packages

import pyfpga

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='pyfpga',
    version=pyfpga.__version__,
    description='A Python package to use FPGA development tools programmatically',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Rodrigo A. Melo',
    author_email='rodrigomelo9@gmail.com',
    license='GPLv3',
    url='https://github.com/PyFPGA/pyfpga',
    package_data={'': ['templates/*.jinja', 'helpers/*']},
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fpga-hdl2bit = pyfpga.helpers.hdl2bit:main',
            'fpga-prj2bit = pyfpga.helpers.prj2bit:main',
            'fpga-bitprog = pyfpga.helpers.bitprog:main'
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Utilities',
        'Topic :: Software Development :: Build Tools',
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)"
    ],
    install_requires=['jinja2']
)
