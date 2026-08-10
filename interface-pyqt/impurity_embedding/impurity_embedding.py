#!/usr/bin/env python3

import sys
import os

qlroot = os.path.dirname(os.path.realpath(__file__))+"/../../"
sys.path.append(qlroot+"/pysrc/") # python libraries


from interfacetk import qtwrap # import the library with simple wrappaers to qt4
getbox = qtwrap.getbox  # get the value of a certain variable
window = qtwrap.new_page(os.path.dirname(os.path.realpath(__file__))) # this mode's page
get = window.get  # get the value of a certain variable



from interfacetk.qh_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries

common.initialize(qtwrap) # do several common initializations

from interfacetk import interfacetk
modify_geometry = lambda x: interfacetk.modify_geometry(x,qtwrap)
select_atoms_removal = lambda: common.select_atoms_removal(get_geometry)
pickup_hamiltonian = lambda: common.pickup_hamiltonian(qtwrap,initialize)

qtwrap.set_combobox("bands_color",operators.operator_list)


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

from interfacetk import latticeterms
latticeterms.connect(qtwrap,lambda: getbox("lattice")) # hide honeycomb-only
                                                         # terms (Haldane,
                                                         # Kane-Mele, valley)
                                                         # for other lattices

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
    h = g.get_hamiltonian(has_spin=True)
    h.add_zeeman(qtwrap.get_array("exchange")) # Zeeman fields
    h.add_sublattice_imbalance(get("mAB"))  # sublattice imbalance
    h.add_rashba(get("rashba"))  # Rashba field
    h.add_antiferromagnetism(get("mAF"))  # AF order
    h.shift_fermi(get("fermi")) # shift fermi energy
    h.add_kane_mele(get("kanemele")) # intrinsic SOC
    h.add_haldane(get("haldane")) # intrinsic SOC
    h.add_antihaldane(get("antihaldane")) 
    h.add_anti_kane_mele(get("antikanemele")) 
    if get("swave")!=0.: h.add_swave(get("swave"))
    p = qtwrap.get_array("pwave")
    if np.sum(np.abs(p))>0.0:
        h.add_pairing(d=p,mode="triplet",delta=1.0)
#    h = h.reduce() # reduce the Hamiltonian
    return h



def show_structure():
  """Show the lattice of the system"""
  common.show_structure(qtwrap,get_geometry)



def show_structure_3d():
    """Show the lattice of the system"""
    common.show_structure_3d(qtwrap,get_geometry)


def show_embedding_ldos():
    common.get_embedding_ldos(pickup_hamiltonian(),window)


def show_embedding_ldos_sweep():
    common.get_embedding_ldos_sweep(pickup_hamiltonian(),window)


def select_impurity_sites():
    common.select_impurity_sites(get_geometry(),window)



inipath = os.getcwd() # get the initial directory, before common.finalize_page()'s create_folder() chdirs away

# create signals (save_results/load_results are wired automatically by
# common.finalize_page())
signals = dict()
signals["show_structure"] = show_structure  # show bandstructure
signals["show_structure_3d"] = show_structure_3d
signals["select_atoms_removal"] = select_atoms_removal
signals["show_embedding_ldos"] = show_embedding_ldos
signals["show_embedding_ldos_sweep"] = show_embedding_ldos_sweep
signals["select_impurity_sites"] = select_impurity_sites

window.set("info_tab","Results will be saved to "+inipath)

common.finalize_page(qtwrap,window,signals,inipath,robust=False)

if __name__ == "__main__":
    window.run() # show this page as its own standalone window and block

