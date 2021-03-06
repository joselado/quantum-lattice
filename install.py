#!/usr/bin/python

import os
import sys

from pysrc.interpreter import pycommand

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--full",default="False",help='Perform a full install')
parser.add_argument("--python",default="",help='Python to use in the installation')

args = parser.parse_args() # get the arguments

if args.python=="": # no Python provided
    pycommand.install_python() # install the correct python dist
else: # python provided
    pycommand.write_python_exec(args.python) # write this executable


if args.full=="True": # full install
    pycommand.install_dependencies() # install the dependencies


pycommand.add_to_path() # add to the program to the path
pycommand.create_icon() # create the icon
pycommand.set_utility_interpreter() # set the interpreter
