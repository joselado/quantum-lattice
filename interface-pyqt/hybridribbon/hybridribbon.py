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

from interfacetk import scfterms
# grid= differs from the default "gridLayout_10" because that name is
# already taken by an unrelated layout in this mode's interface.ui - see
# INTERFACE_GUIDE.md's "Adding a mode" checklist
scfterms.build(qtwrap,grid="gridLayout_scf_10") # build the Density-density/Spin-spin mean field tabs



from interfacetk.qh_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries
from interfacetk import hybridparts # per-part (Upper/Lower/...) parameter widgets
from interfacetk import interfacetk
modify_geometry = lambda x: interfacetk.modify_geometry(x,qtwrap)
select_atoms_removal = lambda: common.select_atoms_removal(get_geometry,script="ql-remove-atoms-geometry-3d")

from interfacetk import latticeterms
from interfacetk import hamiltoniantype
latticeterms.connect(qtwrap,lambda: getbox("lattice")) # hide honeycomb-only
                                                         # terms (Haldane,
                                                         # Kane-Mele, valley)
                                                         # for other lattices

# parameters set separately per part (y-slab) of the system, in the same
# order Designer laid out the Upper/Lower (part 1/2) tabs - see
# hybridparts.py. Adding a term here is enough for it to also gain
# per-part fields for part 3+; initialize() below still needs its own
# check()/fint() call to actually use it.
PART_FIELDS = [
  ("fermi","Fermi energy"),
  ("peierls","Magnetic field"),
  ("exchange","Exchange field"),
  ("rashba","Rashba"),
  ("kanemele","Kane-Mele"),
  ("haldane","Haldane"),
  ("antihaldane","Anti-Haldane"),
  ("mAB","Sublattice imbalance"),
  ("mAF","Antiferromagnetism"),
  ("swave","swave pairing"),
]
hybridparts.connect(qtwrap,PART_FIELDS,
    on_new_part=lambda form: latticeterms.apply_term_restrictions(
        form,form.lattice.currentText(),hamiltoniantype.get_type(form)))


def get_geometry(modify=True):
  """ Create a 0d island"""
  lattice_name = getbox("lattice") # get the option
  n = int(get("ribbon_width")) # thickness of the system
  lattices = {
    "Chain": geometry.chain,
    "Honeycomb": geometry.honeycomb_lattice,
    "Square": geometry.square_lattice,
    "Kagome": geometry.kagome_lattice,
    "Lieb": geometry.lieb_lattice,
    "Triangular": geometry.triangular_lattice_tripartite,
    "Honeycomb zigzag": lambda: geometry.honeycomb_zigzag_ribbon(n),
    "Honeycomb armchair": lambda: geometry.honeycomb_armchair_ribbon(n),
  }
  g = lattices[lattice_name]()
  if g.dimensionality==2: # original is a 2d geometry
    g = ribbon.bulk2ribbon(g,n=n)
  nsuper = int(get("nsuper"))
  g = g.supercell(nsuper)
  if modify: g = modify_geometry(g)
  return g





def initialize():
  """ Initialize the calculation"""
  nparts = hybridparts.current_nparts(qtwrap) # how many y-slabs the user picked
  g = get_geometry() # get the geometry
  region_of = hybridparts.region_of_factory(g.y.min(),g.y.max(),nparts) # y -> part index
  def check(name): return hybridparts.part_check(get,name,nparts)
  def fint(name): return hybridparts.part_interpolator(get,name,nparts,1,region_of) # axis 1 = y
  has_spin = hamiltoniantype.wants_spin(qtwrap)
  h = g.get_hamiltonian(has_spin=has_spin)
  if has_spin: # see hamiltoniantype.py's docstring - these unconditionally
    # call turn_spinful() themselves, so they must be skipped outright for
    # "Spinless" rather than called with a zero-ish value
    h.add_zeeman(hybridparts.part_array_interpolator(qtwrap.get_array,"exchange",nparts,1,region_of)) # Zeeman fields
    if check("rashba"): h.add_rashba(fint("rashba"))  # Rashba field
    h.add_antiferromagnetism(fint("mAF"))  # AF order
    if check("kanemele"):  h.add_kane_mele(fint("kanemele")) # intrinsic SOC
  h.add_sublattice_imbalance(fint("mAB"))  # sublattice imbalance
  h.shift_fermi(fint("fermi")) # shift fermi energy
  if check("haldane"):  h.add_haldane(fint("haldane")) # intrinsic SOC
  if check("antihaldane"):  h.add_antihaldane(fint("antihaldane"))
  if check("peierls"):  h.add_peierls(fint("peierls"))
  if hamiltoniantype.wants_nambu(qtwrap):
      h.setup_nambu_spinor() # establish the BdG structure even if swave is left at zero
      if check("swave"):  h.add_swave(fint("swave"))
#  h.add_peierls(get("peierls")) # shift fermi energy
  return h


pickup_hamiltonian = lambda: common.pickup_hamiltonian(qtwrap,initialize,do_scf=True,solve=solve_scf)


def solve_scf():
  """Perform a selfconsistent calculation"""
  h = initialize()
  common.solve_scf(h,qtwrap)


def show_structure():
  """Show the lattice of the system"""
  common.show_structure(qtwrap,get_geometry,script="ql-structure-bond POSITIONS.OUT")


def show_structure_3d():
  """Show the lattice of the system"""
  common.show_structure_3d(qtwrap,get_geometry,script="ql-structure-tbg POSITIONS.OUT")


def show_magnetism():
  """Show the magnetism of the system"""
  h = pickup_hamiltonian() # get the Hamiltonian
  common.show_exchange(h,qtwrap)


def show_interactive_ldos():
  h = pickup_hamiltonian()  # get the hamiltonian
  common.get_interactive_ldos(h,qtwrap)




# create signals
# STANDARD_HANDLERS covers the plain "pickup_hamiltonian + common.get_X"
# buttons automatically; only the buttons with mode-specific behavior
# need to be listed explicitly here (save_results/load_results are wired
# automatically by common.finalize_page())
signals = common.wire_standard_signals(qtwrap,pickup_hamiltonian,extra={
  "show_structure": show_structure,
  "show_structure_3d": show_structure_3d,
  "show_interactive_ldos": show_interactive_ldos,
  "solve_scf": solve_scf,
  "show_magnetism": show_magnetism,
  "select_atoms_removal": select_atoms_removal,
})

common.initialize(qtwrap) # initialize
qtwrap.set_combobox("dos_operator",operators.operator_list)

inipath = os.getcwd() # get the initial directory, before common.finalize_page()'s create_folder() chdirs away
common.finalize_page(qtwrap,window,signals,inipath)

if __name__ == "__main__":
    window.run() # show this page as its own standalone window and block

