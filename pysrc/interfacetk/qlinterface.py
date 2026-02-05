from __future__ import print_function
import subprocess
import os
import sys
import numpy as np
# import the different libraries for quantum lattice
from pyqula import hamiltonians
from pyqula import klist
from pyqula import geometry
from pyqula import sculpt
from pyqula import multilayers
from pyqula import dos
from pyqula import ldos
from pyqula import films
from pyqula import kpm
from pyqula import current
from pyqula import spectrum
from pyqula import topology
#from pyqula import heterostructures
from pyqula import inout
from pyqula import operators
from pyqula import bandstructure
from pyqula import islands
from pyqula import ribbon
from pyqula import hybrid
from pyqula import kdos
from pyqula import potentials
from pyqula import supercell
from pyqula import scftypes
from pyqula import indexing
from pyqula import meanfield
from pyqula import specialgeometry
from pyqula import specialhopping
from pyqula import timeevolution
from pyqula import embedding
from pyqula import filesystem as fs

import platform


dirname = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dirname+"/../interpreter") # add this path
from interpreter import pycommand


def get_python():
  return pycommand.get_python()

get_anaconda_command = get_python







def get_qlroot():
  """Gets the root path of quantum lattice"""
  return os.path.dirname(os.path.realpath(__file__))+"/../../"



def create_folder():
  """Creates a temporal folder and goes to that one"""
  os.chdir("/tmp")
  # get the name of the folder
  i = 0
  forig = "ql-tmp-"
  folders = os.listdir(os.getcwd()) # list all the folders 
  while True:
    folder = forig + str(i)
    if not folder in folders:
      break # stop if folder doesn't exist
    i += 1 # increase the number
  fs.mkdir(folder)  # create the temporal folder
  fs.chdir(folder)  # go to the temporal folder
  return folder  # return the name of the folder






def save_outputs(inipath,tmppath):
  """Save all the results in the original folder"""
  savepath = inipath+"/QL_save" # name of the fodler where ot save
  print("Saving results in",savepath)
  fs.rmdir(savepath) # remove the folder
  fs.cpdir(tmppath,savepath) # copy folder



def execute_script(name,background=True,mayavi=False):
  """Executes a certain script from the folder utilities"""
  try: qlpath = get_qlroot() # get the main path
  except: qlpath = "" 
#  print("Root path",qlpath)
  scriptpath = qlpath+"utilities/"+name # name of the script
  try:
    python = get_anaconda_command("python") # get the anaconda python
  except:
    python = get_python() # get the correct interpreter
  python = pycommand.get_python()
  if background: os.system(python+" "+scriptpath+" &") # execute the script
  else: os.system(python+" "+scriptpath) # execute the script



def computing():
    """Return an object that shows up a window saying computing"""
    qlpath = get_qlroot()
    python = get_python()
    name = qlpath + "interface-pyqt/timer/timer.py"
    subp = subprocess.Popen([python,name]) # execute the command
    return subp


def running(original):
    """Wrapper to use a timer on a fucntion"""
    def wrapper(*args,**kwargs):
        comp = computing()
        out = original(*args,**kwargs)
        comp.kill()
        return out
    return wrapper



