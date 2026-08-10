#!/usr/bin/env python3

from __future__ import print_function

import sys
import os

qlroot = os.path.dirname(os.path.realpath(__file__))+"/../.."
sys.path.append(qlroot+"/pysrc/") # python libraries


from interfacetk import qtwrap
get = qtwrap.get  # get the value of a certain variable
getbox = qtwrap.getbox  # get the value of a certain variable
window = qtwrap.new_page(os.path.dirname(os.path.realpath(__file__))) # this mode's page

from interfacetk import scfterms
scfterms.build(qtwrap) # build the Density-density/Spin-spin mean field tabs (with formulas)

from interfacetk.qh_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries

common.initialize(qtwrap) # do several common initializations
qtwrap.set_combobox("dos_operator",operators.operator_list)

pickup_hamiltonian = lambda: common.pickup_hamiltonian(qtwrap,initialize,do_scf=True,solve=solve_scf)


LATTICES = {
  "Cubic": geometry.cubic_lattice,
  "Diamond": geometry.diamond_lattice_minimal,
  "Pyrochlore": geometry.pyrochlore_lattice,
  "Hyperhoneycomb": geometry.hyperhoneycomb_lattice,
}

from interfacetk import hamiltoniantype
from interfacetk import latticeterms
latticeterms.connect(qtwrap,lambda: getbox("lattice")) # hide honeycomb-only
                                                         # terms (Haldane,
                                                         # Kane-Mele, valley)
                                                         # for other lattices

def get_geometry():
  """ Create geometry"""
  lattice_name = getbox("lattice") # get the option
  g = LATTICES[lattice_name]() # call the geometry
  nsuper = int(get("nsuper"))
  g = g.supercell(nsuper)
  g.real2fractional()
  g.fractional2real()
  g.center()
  return g




def initialize():
  """ Initialize the calculation"""
  def check(name):
    if abs(get(name))>0.0: return True
    else: return False
  g = get_geometry() # get the geometry
  has_spin = hamiltoniantype.wants_spin(qtwrap)
  if check("strain"): # custom function
    dfun = get("strain") # get function
    def fun(r1,r2): # function to compute distance
      dr = r1-r2
      dr2 = dr.dot(dr) # distance
      if 0.9<dr2<1.1:
        if 0.9<abs(dr[2])<1.1: return 1.0 + dfun # first neighbor
        return 1.0
      else: return 0.0
    h = g.get_hamiltonian(tij=fun,has_spin=has_spin) # get the Hamiltonian
  else:
    h = g.get_hamiltonian(has_spin=has_spin)
  if has_spin: # see hamiltoniantype.py's docstring - these unconditionally
    # call turn_spinful() themselves, so they must be skipped outright for
    # "Spinless" rather than called with a zero-ish value
    h.add_zeeman(qtwrap.get_array("exchange")) # Zeeman field
    if check("rashba"): h.add_rashba(get("rashba"))  # Rashba field
    h.add_antiferromagnetism(get("mAF"))  # AF order
    if check("kanemele"):  h.add_kane_mele(get("kanemele")) # intrinsic SOC
  h.add_sublattice_imbalance(get("mAB"))  # sublattice imbalance
  h.shift_fermi(get("fermi")) # shift fermi energy
  if check("haldane"):  h.add_haldane(get("haldane")) # intrinsic SOC
  if check("antihaldane"):  h.add_antihaldane(get("antihaldane"))
  if hamiltoniantype.wants_nambu(qtwrap):
    h.setup_nambu_spinor() # establish the BdG structure even if swave is left at zero
    if check("swave"):  h.add_swave(get("swave"))
#  h.add_peierls(get("peierls")) # shift fermi energy
  h.turn_dense()
  return h


def show_magnetism():
  """Show the magnetism of the system"""
  h = pickup_hamiltonian() # get the Hamiltonian
  h.write_magnetization(nrep=int(get("magnetization_nrep")))
  execute_script("ql-quiver")


def show_structure():
  """Show the lattice of the system"""
  common.show_structure(qtwrap,get_geometry,script="ql-structure --input POSITIONS.OUT")



def show_structure_3d():
  """Show the lattice of the system"""
  common.show_structure_3d(qtwrap,get_geometry)


def solve_scf():
  """Perform a selfconsistent calculation"""
  h = initialize() # initialize the Hamiltonian
  common.solve_scf_identify_symmetry_breaking(h,qtwrap)







# create signals: STANDARD_HANDLERS covers the plain "pickup_hamiltonian
# + common.get_X" buttons automatically; only the buttons with mode-specific
# behavior need to be listed explicitly here (save_results/load_results are
# wired automatically by common.finalize_page())
signals = common.wire_standard_signals(qtwrap,pickup_hamiltonian,extra={
  "show_structure": show_structure,  # show bandstructure
  "show_structure_3d": show_structure_3d,  # show bandstructure
  "show_magnetism": show_magnetism,
  "solve_scf": solve_scf,
})



inipath = os.getcwd() # get the initial directory, before common.finalize_page()'s create_folder() chdirs away
common.finalize_page(qtwrap,window,signals,inipath)

if __name__ == "__main__":
    window.run() # show this page as its own standalone window and block

