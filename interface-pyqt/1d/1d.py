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
window = qtwrap.main() # this is the main interface



from interfacetk.ql_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries
common.initialize(qtwrap) # do several common initializations

from interfacetk import interfacetk
modify_geometry = lambda x: interfacetk.modify_geometry(x,qtwrap)
select_atoms_removal = lambda: common.select_atoms_removal(get_geometry)
pickup_hamiltonian = lambda: common.pickup_hamiltonian(qtwrap,initialize,do_scf=True)






def get_geometry(modify=True):
  """ Create a 0d island"""
  lattice_name = getbox("lattice") # get the option
  n = int(get("width")) # thickness of the system
  lattices = {
    "Chain": geometry.chain,
    "Bichain": geometry.bichain,
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
  g = g.supercell(nsuper,store_primal=True)
  if modify: g = modify_geometry(g) # modify the geometry
  return g








def initialize():
  """ Initialize the calculation"""
  g = get_geometry() # get the geometry
  h = g.get_hamiltonian(has_spin=True,tij=qtwrap.get_array("hoppings"))
  h.turn_multicell()
  h.add_zeeman(qtwrap.get_array("exchange"))
  h.add_sublattice_imbalance(get("mAB"))  # sublattice imbalance
  if abs(get("rashba")) > 0.0: h.add_rashba(get("rashba"))  # Rashba field
  h.add_antiferromagnetism(get("mAF"))  # AF order
  h.add_crystal_field(qtwrap.get("crystalfield")) 
  h.shift_fermi(get("fermi")) # shift fermi energy
  h.add_kane_mele(get("kanemele")) # intrinsic SOC
  h.add_haldane(get("haldane")) # intrinsic SOC
  h.add_antihaldane(get("antihaldane")) 
  h.add_anti_kane_mele(get("antikanemele")) 
  h.add_peierls(get("peierls")) # magnetic field
  if get("swave")!=0.: h.add_swave(get("swave")) 
  p = qtwrap.get_array("pwave")
  if np.sum(np.abs(p))>0.0:
      h.add_pairing(d=p,mode="triplet",delta=1.0)
  return h


def show_edge_dos():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_surface_dos(h,qtwrap) # wrapper




def show_magnetism():
  """Show the magnetism of the system"""
  h = pickup_hamiltonian() # get the Hamiltonian
  common.show_exchange(h,qtwrap)


def show_ldos():
  h = pickup_hamiltonian() # get the Hamiltonian
  ew = abs(qtwrap.get("ldos_ewindow"))
  energies = np.linspace(-ew,ew,100)
  delta = qtwrap.get("ldos_delta")
  nk = int(qtwrap.get("ldos_nk"))
  name = qtwrap.getbox("ldos_operator")
  ldos.spatial_energy_profile(h,operator=h.get_operator(name),
          nk=nk,delta=delta,energies=energies)
  execute_script('ql-map2d --input DOSMAP.OUT --xlabel Energy --ylabel "y-position" --zlabel DOS --title "Local DOS"')
  


def show_structure():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
  execute_script("ql-structure-bond --input POSITIONS.OUT")



def show_structure_3d():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
  execute_script("ql-structure3d POSITIONS.OUT")





def solve_scf():
  """Perform a selfconsistent calculation"""
  h = initialize()
  common.solve_scf(h,qtwrap)





def save_results():  save_state(inipath,tmppath,window) # function to save
def load_results():  load_state(inipath,tmppath,window) # function to load


# create signals: STANDARD_HANDLERS covers the plain "pickup_hamiltonian
# + common.get_X" buttons automatically; only the buttons with mode-specific
# behavior need to be listed explicitly here
signals = common.wire_standard_signals(qtwrap,pickup_hamiltonian,extra={
  "show_structure": show_structure,  # show bandstructure
  "show_ldos": show_ldos,  # show DOS
  "show_edge_dos": show_edge_dos,  # show DOS
  "show_structure_3d": show_structure_3d,
  "show_magnetism": show_magnetism,
  "solve_scf": solve_scf,
  "select_atoms_removal": select_atoms_removal,
  "save_results": save_results,
  "load_results": load_results,
})

# set all the formulas
common.set_formulas(qtwrap)



window.connect_clicks(signals)
inipath = os.getcwd() # get the initial directory
folder = create_folder()
tmppath = os.getcwd() # get the initial directory
window.run()

