from __future__ import print_function
import subprocess
import os
import sys
import shlex
import shutil
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
from pyqula import latticegas

from . import qtwrap

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


def _looks_like_prior_save(path):
  """Whether `path` is a folder that itself looks like a save_state()
  result (i.e. it holds an interface.json) - used both to list candidates
  for ask_load_name()'s picker and, in save_state(), to tell "the user is
  re-saving under a name they already used" (fine to silently overwrite,
  matching the old fixed-"QL_save" behavior) apart from "this name
  collides with something else entirely" (needs confirmation first)."""
  return os.path.isfile(os.path.join(path,"interface.json"))


def save_state(inipath,tmppath,window):
  """Save the interface parameters together with the results computed
  since those parameters were last changed, into a folder the user names
  via a prompt (qtwrap.ask_save_name(), defaulting to "QL_save") - rather
  than always overwriting one fixed "QL_save" folder, so two results can
  be kept side by side without the user having to rename it by hand
  in between saves. A chosen name that collides with something that isn't
  itself a prior save is confirmed first (qtwrap.confirm_overwrite()),
  since fs.rmdir() below deletes whatever is already there before writing
  the new save - unlike the old fixed name, an arbitrary user-typed name
  can easily collide with an unrelated file/folder."""
  save_name = qtwrap.ask_save_name(window)
  if save_name is None:
      qtwrap.notify_cancelled(window,"Save cancelled")
      return
  savepath = inipath+"/"+save_name # name of the folder where to save
  if os.path.exists(savepath):
      if not os.path.isdir(savepath):
          raise ValueError('"%s" already exists here and is not a folder - '
              'pick a different name'%save_name)
      if not _looks_like_prior_save(savepath) and not qtwrap.confirm_overwrite(window,save_name):
          qtwrap.notify_cancelled(window,"Save cancelled")
          return
  print("Saving state in",savepath)
  fs.rmdir(savepath) # remove the folder
  fs.mkdir(savepath) # create a fresh folder
  window.save_interface(output=savepath+"/interface.json") # save parameters
  cutoff = window.params_dirty_time() # results older than this are stale
  for name in os.listdir(tmppath): # loop over the scratch folder
    full = os.path.join(tmppath,name)
    if os.path.isfile(full) and os.path.getmtime(full)>=cutoff:
        shutil.copy(full,savepath) # only results under current parameters
  qtwrap.notify_success(window,"Saved",f"Results saved to {save_name}/")


def _list_save_folders(inipath):
  """Names of subfolders directly under `inipath` that look like a
  save_state() result (see _looks_like_prior_save()), for
  ask_load_name()'s picker - sorted most-recently-modified first so the
  save the user probably wants defaults to the top of the list. Entries
  that vanish or become unreadable between the listdir() and the mtime
  sort (another process, or just bad luck) are treated as oldest rather
  than raising, so the picker still shows whatever else is there."""
  try: names = os.listdir(inipath)
  except OSError: return []
  out = [n for n in names if _looks_like_prior_save(os.path.join(inipath,n))]
  def _mtime(n):
    try: return os.path.getmtime(os.path.join(inipath,n))
    except OSError: return 0
  out.sort(key=_mtime,reverse=True)
  return out


def load_state(inipath,tmppath,window):
  """Restore the parameters and results saved by save_state(), from a
  folder the user picks among those found under `inipath`
  (qtwrap.ask_load_name())."""
  options = _list_save_folders(inipath)
  save_name = qtwrap.ask_load_name(window,options)
  if save_name is None:
      if options: qtwrap.notify_cancelled(window,"Load cancelled")
      return # cancelled, or nothing to load (ask_load_name already warned)
  savepath = inipath+"/"+save_name # name of the folder to load from
  infile = savepath+"/interface.json"
  if not os.path.isfile(infile):
      print("No saved state found in",savepath)
      return
  window.load_interface(infile) # restore the parameters
  window.reset_dirty() # the restored results are valid for these parameters
  for name in os.listdir(savepath): # loop over the saved files
    if name=="interface.json": continue # not a result file
    full = os.path.join(savepath,name)
    if os.path.isfile(full): shutil.copy(full,tmppath) # bring result back
  qtwrap.notify_success(window,"Loaded",f"Restored results from {save_name}/")



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




