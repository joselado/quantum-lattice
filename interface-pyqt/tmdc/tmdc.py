#!/usr/bin/env python3

import sys
import os

# main path
qlroot = os.path.dirname(os.path.realpath(__file__))+"/../.."
sys.path.append(qlroot+"/pysrc/") # python libraries


from interfacetk import qtwrap # import the library with simple wrappaers to qt4
get = qtwrap.get  # get the value of a certain variable
getbox = qtwrap.getbox  # get the value of a certain variable
window = qtwrap.new_page(os.path.dirname(os.path.realpath(__file__))) # this mode's page


from interfacetk.ql_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries

common.initialize(qtwrap) # do several common initializations

pickup_hamiltonian = lambda: common.pickup_hamiltonian(qtwrap,initialize)

qtwrap.set_combobox("bands_color",operators.operator_list)
qtwrap.set_combobox("dos_operator",operators.operator_list)


def get_geometry():
    """Return the geometry"""
    return initialize().geometry


def initialize():
  """ Initialize the calculation"""
  from pyqula import specialhamiltonian
  h = specialhamiltonian.NbSe2(soc=get("ising_SOC"),cdw=get("cdw"))
  h.add_zeeman(qtwrap.get_array("exchange")) # Zeeman fields
  h.add_rashba(get("rashba"))  # Rashba field
  h.set_filling(0.5,nk=10) # half filling
  h.shift_fermi(get("fermi")) # shift fermi energy
  if abs(get("swave"))>0.0: h.add_swave(get("swave"))
  return h





def show_dos():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_dos(h,qtwrap)





  




  


def show_structure():
  """Show the lattice of the system"""
  common.show_structure(qtwrap,get_geometry)


def show_structure_3d():
  """Show the lattice of the system"""
  common.show_structure_3d(qtwrap,get_geometry)


# create signals: STANDARD_HANDLERS covers the plain "pickup_hamiltonian
# + common.get_X" buttons automatically; only the buttons with mode-specific
# behavior need to be listed explicitly here (save_results/load_results are
# wired automatically by common.finalize_page())
signals = common.wire_standard_signals(qtwrap,pickup_hamiltonian,extra={
  "show_structure": show_structure,  # show bandstructure
  "show_dos": show_dos,
  "show_structure_3d": show_structure_3d,
})

inipath = os.getcwd() # get the initial directory, before common.finalize_page()'s create_folder() chdirs away
common.finalize_page(qtwrap,window,signals,inipath,robust=False)

if __name__ == "__main__":
    window.run() # show this page as its own standalone window and block

