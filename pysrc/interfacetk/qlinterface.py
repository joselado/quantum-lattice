from __future__ import print_function
import subprocess
import os
import sys
import shlex
import tempfile
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


def get_qlroot():
  """Gets the root path of quantum lattice"""
  return pycommand.get_qh_path() # single source of truth, see pycommand.py



def create_folder():
  """Creates a temporal folder and goes to that one"""
  # tempfile.mkdtemp uses the OS temp dir (respects TMPDIR/TEMP/TMP) and
  # guarantees a unique folder name, so it works the same on Linux, Mac
  # and Windows without a hardcoded "/tmp" or a manual naming loop
  folder = tempfile.mkdtemp(prefix="ql-tmp-")
  fs.chdir(folder)  # go to the temporal folder
  return folder  # return the path of the folder






def save_outputs(inipath,tmppath):
  """Save all the results in the original folder"""
  savepath = inipath+"/QL_save" # name of the fodler where ot save
  print("Saving results in",savepath)
  fs.rmdir(savepath) # remove the folder
  fs.cpdir(tmppath,savepath) # copy folder



def execute_script(name,background=True):
  """Executes a certain script from the folder utilities.
  `name` may be a bare script name or a full command string with
  arguments (e.g. "ql-bands --dim 2"), possibly quoted."""
  qlpath = get_qlroot() # get the main path
  args = shlex.split(name) # split into [script, *arguments], respects quoting
  scriptpath = os.path.join(qlpath,"utilities",args[0]) # portable path, no OS-only "&"
  python = pycommand.get_python() # get the correct interpreter
  cmd = [python,scriptpath]+args[1:]
  # log stdout/stderr instead of discarding them, so a failing script
  # (e.g. missing pyvista) leaves a diagnosable trace instead of vanishing
  logpath = os.path.join(os.getcwd(),args[0]+".log")
  with open(logpath,"w") as logfile:
    proc = subprocess.Popen(cmd,stdout=logfile,stderr=subprocess.STDOUT)
  if not background: proc.wait() # block until the script finishes
  return proc



def computing():
    """Return an object that shows up a window saying computing"""
    qlpath = get_qlroot()
    python = get_python()
    name = os.path.join(qlpath,"interface-pyqt","timer","timer.py")
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



