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

def initialize():
  global _initialized
  handlers.initialize(qtwrap)
  _initialized = True

def _ensure_initialized():
  """Handlers below that read the saved Hamiltonian (handlers.
  load_hamiltonian(), which just hamiltonians.load()s a file from disk)
  need initialize() to have run at least once first. It used to run
  unconditionally as soon as this module was imported - on a ~1260-atom
  default island that alone costs a couple of seconds - which, now that
  the shell only imports a mode's <mode>.py on first navigation to it
  (see _LazyPage in bin/versions/quantum-lattice-pyqt), meant just
  opening this page paid that cost even before touching a button. Build
  it lazily instead, on first handler call that actually needs it; an
  explicit click of the "Initialize" button still always rebuilds
  (e.g. after changing parameters), same as before."""
  if not _initialized: initialize()

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

def save_results():  save_state(inipath,tmppath,window) # function to save
def load_results():  load_state(inipath,tmppath,window) # function to load


# create signals
signals = dict()
signals["initialize"] = initialize  # initialize and run
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



window.connect_clicks(signals)
folder = create_folder()
window.scratch_dir = folder # so qtwrap.connect_clicks() can restore this page's cwd before each handler runs
tmppath = os.getcwd() # get the initial directory
if __name__ == "__main__":
    window.run() # show this page as its own standalone window and block
