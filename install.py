#!/usr/bin/python

import os
import sys

from pysrc.interpreter import pycommand

pycommand.install_python() # install the correct python dist
pycommand.install_dependencies() # install the dependencies
pycommand.add_to_path() # install the correct python dist
pycommand.create_icon() # create the icon
pycommand.set_utility_interpreter() # install the correct python dist
