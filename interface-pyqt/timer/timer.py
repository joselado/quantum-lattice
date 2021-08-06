#!/usr/bin/python

from __future__ import print_function

import sys
import os

qhroot = os.path.dirname(os.path.realpath(__file__))+"/../.."
sys.path.append(qhroot+"/interface-pyqt/qtwrap")
sys.path.append(qhroot+"/pysrc/") # python libraries


import qtwrap # import the library with simple wrappaers to qt4
get = qtwrap.get  # get the value of a certain variable
getbox = qtwrap.getbox  # get the value of a certain variable
window = qtwrap.main() # this is the main interface



#from qh_interface import * # import all the libraries needed

window.run()

