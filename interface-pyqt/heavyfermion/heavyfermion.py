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



from interfacetk.qlinterface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries

#common.initialize(qtwrap) # do several common initializations

from interfacetk import interfacetk
modify_geometry = lambda x: interfacetk.modify_geometry(x,qtwrap)
select_atoms_removal = lambda: common.select_atoms_removal(get_geometry)
pickup_hamiltonian = lambda: common.pickup_hamiltonian(qtwrap,initialize)


LATTICES = {
  "Honeycomb": geometry.honeycomb_lattice,
  "Honeycomb 4 sites": geometry.honeycomb_lattice_square_cell,
  "Square": geometry.square_lattice,
  "Single square": geometry.single_square_lattice,
  "Kagome": geometry.kagome_lattice,
  "Lieb": geometry.lieb_lattice,
  "Triangular": geometry.triangular_lattice,
  "Triangular tripartite": lambda: geometry.triangular_lattice(n=3),
  "Honeycomb 6 sites": lambda: geometry.honeycomb_lattice(n=3),
}

def get_geometry(modify=True):
  """ Create a 0d island"""
  lattice_name = getbox("lattice") # get the option
  g = LATTICES[lattice_name]() # call the geometry
  nsuper = int(get("nsuper"))
  g = g.supercell(nsuper)
  if modify: g = modify_geometry(g) # modify the geometry
  return g







def initialize():
  """ Initialize the calculation"""
  g = get_geometry() # get the geometry
  return generate_hamiltonian(qtwrap,g=g) # return Hamiltonian



def generate_hamiltonian(window,g=None):
    """Generate the Hamiltonian taking as input the geometry"""
    if g is None: raise
    get = window.get # function
    get_array = window.get_array # function
    h = g.get_hamiltonian(has_spin=True,tij=get_array("hoppings"))
    h.shift_fermi(get("fermi")) # shift fermi energy
    from pyqula.specialhamiltonian import H2HFH
    h = H2HFH(h,JK=get("kondo"),J=get("exchange")) # generate HF Hamiltonian
    h.turn_dense()
    return h




def show_dosbands():
  h = pickup_hamiltonian() # get hamiltonian
  nk = int(get("ne_kbands"))
  op = getbox("operator_kdos")
  ewindow=get("window_kbands")
  ne=int(get("ne_kbands"))
  es = np.linspace(-ewindow,ewindow,ne)
  kdos.kdos_bands(h,scale=get("scale_kbands"),
                   energies = es,
                   delta=get("delta_kbands"),
                   ntries=int(get("nv_kbands")),nk=nk,operator=op)
  execute_script("ql-dosbands --input KDOS_BANDS.OUT ")
#  execute_script("ql-map2d --input KDOS_BANDS.OUT --xlabel k --ylabel E/t --zlabel A --show_cuts False --title 'Spectral function'")




  




  


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



inipath = os.getcwd() # get the initial directory
def save_results():  save_state(inipath,tmppath,window) # function to save
def load_results():  load_state(inipath,tmppath,window) # function to load


# create signals: STANDARD_HANDLERS covers the plain "pickup_hamiltonian
# + common.get_X" buttons automatically; only the buttons with mode-specific
# behavior need to be listed explicitly here
signals = common.wire_standard_signals(qtwrap,pickup_hamiltonian,extra={
  "show_structure": show_structure,  # show bandstructure
  "show_dosbands": show_dosbands,  # custom kbands-specific implementation
  "show_structure_3d": show_structure_3d,
  "select_atoms_removal": select_atoms_removal,
  "save_results": save_results,
  "load_results": load_results,
})



# set all the formulas
common.set_formulas(qtwrap)



window.connect_clicks(signals,robust=False)
folder = create_folder()
tmppath = os.getcwd() # get the initial directory
window.run()

