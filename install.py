#!/usr/bin/env python3

import sys

from pysrc.interpreter import pycommand

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--python",default="",
        help='Python interpreter to install with (defaults to the one running this script)')

args = parser.parse_args() # get the arguments

python = args.python if args.python!="" else sys.executable

pycommand.install_requirements(python=python) # PyQt5/numpy/scipy/numba/matplotlib (+ best-effort pyvista/Fortran)
pycommand.install_editable(python=python)      # registers the `quantum-lattice` console script with pip
pycommand.create_icon()                        # Linux .desktop entry / Windows .bat launcher

print()
print("Install complete. Run the application with: quantum-lattice")
