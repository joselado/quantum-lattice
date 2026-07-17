#!/usr/bin/env python3

import sys
import os

qlroot = os.path.dirname(os.path.realpath(__file__))+"/../../"
sys.path.append(qlroot+"/pysrc/") # python libraries


from interfacetk import qtwrap # import the library with simple wrappaers to qt4
getbox = qtwrap.getbox  # get the value of a certain variable
window = qtwrap.main() # this is the main interface
get = window.get  # get the value of a certain variable



from interfacetk.qh_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries

common.initialize(qtwrap) # do several common initializations

from interfacetk import interfacetk
modify_geometry = lambda x: interfacetk.modify_geometry(x,qtwrap)
select_atoms_removal = lambda: common.select_atoms_removal(get_geometry)
pickup_hamiltonian = lambda: common.pickup_hamiltonian(qtwrap,initialize)

qtwrap.set_combobox("scf_initialization",meanfield.spinful_guesses)
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
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
#  execute_script("ql-light-structure POSITIONS.OUT")
  execute_script("ql-structure-bond --input POSITIONS.OUT")
#  execute_script("ql-structure  ")





def show_structure_3d():
    """Show the lattice of the system"""
    g = get_geometry() # get the geometry
    nsuper = int(get("nsuper_struct"))
    g = g.supercell(nsuper)
    g.write()
    execute_script("ql-structure3d POSITIONS.OUT")


def show_embedding_ldos():
    h = pickup_hamiltonian()
    vintra = get_impurity_matrix(h)
    ns0 = int(window.get("nsuper_impurity")) # supercell of the impurity
    eb = embedding.Embedding(h,m=vintra,nsuper=ns0)
    e = get("energy_embedding_ldos") # energy
    delta = get("delta_embedding_ldos") # energy
    ns = int(get("ncells_embedding_ldos"))
    nks = get("nk_scaling_embedding_ldos")
    nk = common.get_nk(h,delta=delta,fac=20*nks) # number of kpoints
    (x,y,d) = eb.ldos(nsuper=ns,energy=e,delta=delta,nk=nk)
    np.savetxt("LDOS.OUT",np.array([x,y,d]).T)
    execute_script("ql-ldos --input LDOS.OUT")


def get_impurity_matrix(h0):
    """Get the impurity matrix"""
    n = int(window.get("nsuper_impurity")) # supercell for the impurities
    if n>1: h0 = h0.supercell(n) # create the supercell
    h = h0.copy()*0. # initialize
    v = get("impurity_potential") # (additional) potential in this site
    jv = qtwrap.get_array("impurity_exchange") # (additional) Zeeman field
    from pyqula import potentials
    pot_ons = 0. # initialize
    pot_j = 0. # initialize
    try: # many impurities
        inds = np.genfromtxt("IMPURITY_SITES.OUT") # read the indexes
        if inds.shape==(): inds = [inds] # just one number
        print(inds)
    except: inds = [0] # just the first site
    for i in inds: 
        i = int(i) # to integer
        imp_ons = potentials.impurity(h.geometry.r[i],v=v) # onsite
        imp_j = potentials.impurity(h.geometry.r[i],v=jv) # exchange
        pot_ons = pot_ons + imp_ons # add contribution
        pot_j = pot_j + imp_j # add contribution
    h.add_onsite(pot_ons) # add the onsite
    h.add_exchange(pot_j) # add the exchange
    return h+h0 # return the defective Hamiltonian




def show_embedding_ldos_sweep():
    h = pickup_hamiltonian()
    vintra = get_impurity_matrix(h)
    ns0 = int(window.get("nsuper_impurity")) # supercell of the impurity
    eb = embedding.Embedding(h,m=vintra,nsuper=ns0)
    ewin = get("energy_window_embedding_ldos_sweep") # energy
    ne = int(get("num_energies_embedding_ldos_sweep")) # energy
    es = np.linspace(-ewin,ewin,ne,endpoint=True) # number of energies
    delta = get("delta_embedding_ldos_sweep") # energy
    ns = int(get("ncells_embedding_ldos_sweep"))
    nks = int(get("nk_scaling_embedding_ldos_sweep"))
    nk = common.get_nk(h,delta=delta,fac=20*nks) # number of kpoints
    ds = [] # density of states
    eb.multildos(es=es,delta=delta,nk=nk,nsuper=ns) # compute
    execute_script("ql-multildos ")



def select_impurity_sites():
    g = get_geometry() # get the geometry
    n = int(window.get("nsuper_impurity")) # supercell for the impurities
    g = g.supercell(n) # supercell
    np.savetxt("POSITIONS_PP.OUT",np.array(g.r)) # write in file
    # select the sites
    execute_script("ql-select-atoms-geometry  --input POSITIONS_PP.OUT --output IMPURITY_SITES.OUT --initially_selected \"0\"  --caption \" Sites with impurities\"")



inipath = os.getcwd() # get the initial directory

def save_results():  save_state(inipath,tmppath,window) # function to save
def load_results():  load_state(inipath,tmppath,window) # function to load

# create signals
signals = dict()
signals["show_structure"] = show_structure  # show bandstructure
signals["show_structure_3d"] = show_structure_3d
signals["select_atoms_removal"] = select_atoms_removal
signals["show_embedding_ldos"] = show_embedding_ldos
signals["show_embedding_ldos_sweep"] = show_embedding_ldos_sweep
signals["select_impurity_sites"] = select_impurity_sites
signals["save_results"] = save_results
signals["load_results"] = load_results


# set all the formulas
common.set_formulas(qtwrap)

window.set("info_tab","Results will be saved to "+inipath)


window.connect_clicks(signals,robust=False)
folder = create_folder()
tmppath = os.getcwd() # get the initial directory
window.run()

