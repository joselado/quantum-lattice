#!/usr/bin/env python3

from __future__ import print_function

import sys
import os

# main path
qlroot = os.path.dirname(os.path.realpath(__file__))+"/../.."
sys.path.append(qlroot+"/pysrc/") # python libraries


from interfacetk import qtwrap # import the library with simple wrappaers to qt4
get = qtwrap.get  # get the value of a certain variable
getbox = qtwrap.getbox  # get the value of a certain variable
window = qtwrap.new_page(os.path.dirname(os.path.realpath(__file__))) # this mode's page

from interfacetk.qh_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries

import islandbuild
import handlers

from interfacetk import latticeterms
latticeterms.connect(qtwrap,lambda: getbox("lattice")) # hide honeycomb-only
                                                         # terms (Haldane,
                                                         # Kane-Mele, valley)
                                                         # for other lattices

inipath = os.getcwd() # get the initial directory

_initialized = False # whether initialize() has built a Hamiltonian yet
                      # in this page's scratch folder
_init_dirty_time = None # window.params_dirty_time() as of the last initialize()

def initialize():
  global _initialized, _init_dirty_time
  handlers.initialize(qtwrap)
  _initialized = True
  _init_dirty_time = window.params_dirty_time()

def _ensure_initialized():
  """Handlers below that read the saved Hamiltonian (handlers.
  load_hamiltonian(), which just hamiltonians.load()s a file from disk)
  need initialize() to have built one first, and need it rebuilt whenever
  a form parameter has changed since - there used to be an explicit
  "Initialize Hamiltonian" button for this, but forgetting to press it
  after changing a parameter silently ran the next calculation against
  the stale Hamiltonian. window.params_dirty_time() (see qtwrap.py's
  dirty-tracking, also used by save_state()/load_state() to decide which
  result files are still valid) only advances on genuine user edits to a
  form widget, never on a handler's own programmatic writes, so comparing
  it against the value as of the last initialize() tells us exactly
  whether a rebuild is needed - including the very first call, where
  _initialized is still False."""
  if not _initialized or window.params_dirty_time()>_init_dirty_time:
    initialize()

def show_ldos():  _ensure_initialized(); handlers.show_ldos(qtwrap)
def show_full_spectrum():  _ensure_initialized(); handlers.show_full_spectrum()
def show_dos():  _ensure_initialized(); handlers.show_dos(qtwrap)
def show_spatial_dos():  _ensure_initialized(); handlers.show_spatial_dos(qtwrap)
def show_potential():  handlers.show_potential(qtwrap)
def show_lattice():  handlers.show_lattice(qtwrap)
def show_path_dos():  _ensure_initialized(); handlers.show_path_dos(qtwrap)
def show_path():  _ensure_initialized(); handlers.show_path(qtwrap)
def show_eigenvalues():  _ensure_initialized(); handlers.show_eigenvalues(qtwrap)
def clear_removal():  handlers.clear_removal()
def select_atoms():  handlers.select_atoms()
def select_atoms_dos():  handlers.select_atoms_dos()
def select_path():  _ensure_initialized(); handlers.select_path_atoms()
def select_site_dos():  _ensure_initialized(); common.select_site(handlers.load_hamiltonian(),qtwrap)
def show_site_dos():  _ensure_initialized(); common.get_site_dos(handlers.load_hamiltonian(),qtwrap,use_kpm=True) # islands here are too large for ED

def save_results():  save_state(inipath,tmppath,window) # function to save
def load_results():  load_state(inipath,tmppath,window) # function to load


# create signals
signals = dict()
signals["show_ldos"] = show_ldos  # show LDOS
signals["show_dos"] = show_dos  # show DOS
signals["show_spatial_dos"] = show_spatial_dos  # show DOS
signals["show_lattice"] = show_lattice  # show magnetism
#signals["show_full_spectrum"] = show_full_spectrum  # show all the eigenvalues
signals["show_path"] = show_path  # show the path
signals["show_eigenvalues"] = show_eigenvalues  # show the path
signals["show_path_dos"] = show_path_dos  # show the path
signals["show_potential"] = show_potential  # show the potential added
signals["save_results"] = save_results  # save the results
signals["load_results"] = load_results  # load the results
#signals["clear_removal"] = clear_removal  # clear the file
#signals["select_atoms"] = select_atoms  # select_atoms
signals["select_atoms_dos"] = select_atoms_dos  # select_atoms
signals["select_path"] = select_path  # draw a line to pick the initial/final atom
signals["select_site_dos"] = select_site_dos  # pick the site for show_site_dos
signals["show_site_dos"] = show_site_dos  # DOS projected onto the picked site



window.connect_clicks(signals)
folder = create_folder()
window.scratch_dir = folder # so qtwrap.connect_clicks() can restore this page's cwd before each handler runs
tmppath = os.getcwd() # get the initial directory
if __name__ == "__main__":
    window.run() # show this page as its own standalone window and block
