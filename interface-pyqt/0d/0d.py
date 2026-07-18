#!/usr/bin/env python3

from __future__ import print_function

import sys
import os

qlroot = os.path.dirname(os.path.realpath(__file__))+"/../../"
sys.path.append(qlroot+"/pysrc/") # python libraries


from interfacetk import qtwrap # import the library with simple wrappaers to qt4
get = qtwrap.get  # get the value of a certain variable
getbox = qtwrap.getbox  # get the value of a certain variable
window = qtwrap.main() # this is the main interface



from interfacetk.ql_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries
common.initialize(qtwrap) # several initilizations
qtwrap.set_combobox("dos_operator",operators.operator_list)

from interfacetk import interfacetk
select_atoms_removal = lambda: common.select_atoms_removal(get_geometry)
pickup_hamiltonian = lambda: common.pickup_hamiltonian(qtwrap,initialize,do_scf=True)



def get_geometry(modify=True):
  """ Create a 0d island"""
  lattice_name = getbox("lattice") # get the option
  n = float(get("width")) # thickness of the system
  lattices = {
    "Chain": geometry.chain,
    "Honeycomb": geometry.honeycomb_lattice,
    "Square": geometry.single_square_lattice,
    "Kagome": geometry.kagome_lattice,
    "Lieb": geometry.lieb_lattice,
    "Triangular": geometry.triangular_lattice_tripartite,
    "Honeycomb zigzag": lambda: geometry.honeycomb_zigzag_ribbon(n),
    "Honeycomb armchair": lambda: geometry.honeycomb_armchair_ribbon(n),
  }
  g = lattices[lattice_name]()
  rot = get("rotation")*np.pi/180.
  g = islands.get_geometry(n=n,nedges=int(get("nsides")),rot=rot,geo=g)
  if modify: g = modify_geometry(g) # modify the geometry
  return g


def select_atom_time_evolution():
  """Select a single atom"""
  g = get_geometry() # get the unmodified geometry
  g.write()
  execute_script("ql-pick-single-atom") # pick a single atom


def show_time_evolution():
  h = pickup_hamiltonian() # get hamiltonian
  try: i = open("SELECTED_SINGLE_ATOM.INFO").read()
  except: i = 0
  if i=="": i=0
  else: i = int(i)
  if h.has_spin: 
      i = i*2
      if qtwrap.getbox("channel_time_evolution")=="Down": i += 1
#  print(i) ; return
  if h.has_eh: i = i*4
  tmax = qtwrap.get("tmax_time_evolution") # maximum time
  timeevolution.evolve_local_state(h,i=i,ts=np.linspace(0.,tmax,100),
        mode="green")
  execute_script("ql-multitimeevolution") # plot the result






def modify_geometry(g):
  """Modify the geometry according to the interface"""
  g = interfacetk.modify_geometry(g,qtwrap)
  g.center()
  return g # return geometry
  


     






def initialize():
    """ Initialize the calculation"""
    g = get_geometry() # get the geometry
    h = g.get_hamiltonian(has_spin=True,tij=qtwrap.get_array("hoppings"))
    h.add_zeeman(qtwrap.get_array("exchange"))
    h.add_sublattice_imbalance(get("mAB"))  # sublattice imbalance
    h.add_rashba(get("rashba"))  # Rashba field
    h.add_antiferromagnetism(get("mAF"))  # AF order
    h.add_crystal_field(qtwrap.get("crystalfield")) # add magnetic field
    h.shift_fermi(get("fermi")) # shift fermi energy
    h.add_kane_mele(get("kanemele")) # intrinsic SOC
    h.add_haldane(get("haldane")) # intrinsic SOC
    h.add_antihaldane(get("antihaldane")) 
    h.add_peierls(get("peierls")) # magnetic field
    common.add_strain(h,window) # add strain
    if get("swave")!=0.0: h.add_swave(get("swave")) 
    p = qtwrap.get_array("pwave")
    if np.sum(np.abs(p))>0.0:
        h.add_pairing(d=p,mode="triplet",delta=1.0)
    return h


def show_interactive_ldos():
  h = pickup_hamiltonian()  # get the hamiltonian
  common.get_multildos(h,qtwrap) # compute




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







def show_magnetism():
  """Show the magnetism of the system"""
  h = pickup_hamiltonian() # get the Hamiltonian
  h.write_magnetization() # write the magnetism
  if getbox("magnetization_plot_mode")=="2D":
      execute_script("ql-magnetism2d")
  else: # 3D mode
      execute_script("ql-moments")


def show_hoppings():
  """Show the lattice of the system"""
  h = pickup_hamiltonian() # get the Hamiltonian
  h.write_hopping()
  execute_script("ql-network --input HOPPING.OUT")


def show_local_chern():
  h = pickup_hamiltonian() # get hamiltonian
  op = getbox("operator_chern")
  op = h.get_operator(op)
  topology.real_space_chern(h,operator=op)
  execute_script("ql-potential --input REAL_SPACE_CHERN.OUT --cmap rainbow")



inipath = os.getcwd() # get the initial directory
folder = create_folder() # create a new folder
tmppath = os.getcwd() # get the initial directory
def save_results():  save_state(inipath,tmppath,window) # function to save
def load_results():  load_state(inipath,tmppath,window) # function to load


# create signals: STANDARD_HANDLERS covers the plain "pickup_hamiltonian
# + common.get_X" buttons automatically; only the buttons with mode-specific
# behavior need to be listed explicitly here
signals = common.wire_standard_signals(qtwrap,pickup_hamiltonian,extra={
  "solve_scf": solve_scf,
  "show_structure": show_structure,  # show bandstructure
  "show_hoppings": show_hoppings,  # show DOS
  "show_structure_3d": show_structure_3d,
  "show_interactive_ldos": show_interactive_ldos,  # show DOS
  "show_magnetism": show_magnetism,
  "select_atoms_removal": select_atoms_removal,
  "select_atom_time_evolution": select_atom_time_evolution,
  "show_time_evolution": show_time_evolution,
  "show_local_chern": show_local_chern,
  "save_results": save_results,
  "load_results": load_results,
})



# set all the formulas
common.set_formulas(qtwrap)


#from qh_interface import create_folder # import all the libraries needed

window.connect_clicks(signals)
window.run()

