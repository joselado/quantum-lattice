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

common.initialize(qtwrap) # do several common initializations

from interfacetk import interfacetk
modify_geometry = lambda x: interfacetk.modify_geometry(x,qtwrap)
select_atoms_removal = lambda: common.select_atoms_removal(get_geometry)
pickup_hamiltonian = lambda: common.pickup_hamiltonian(qtwrap,initialize,do_scf=True)

qtwrap.set_combobox("scf_initialization",meanfield.spinful_guesses)
qtwrap.set_combobox("bands_color",operators.operator_list)
qtwrap.set_combobox("fs_operator",operators.operator_list)
qtwrap.set_combobox("operator_kdos",operators.operator_list)
qtwrap.set_combobox("dos_operator",operators.operator_list)


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
  g = g.supercell(nsuper,store_primal=True)
  if modify: g = modify_geometry(g) # modify the geometry
  return g












def initialize():
  """ Initialize the calculation"""
  g = get_geometry() # get the geometry
  return common.generate_hamiltonian(qtwrap,g=g) # return Hamiltonian


def special_pairing(h):
    """Create a special pairing function"""
    delta = get("swave") # value
    deltatype = getbox("pairing_type") # type of pairing
    if deltatype=="Uniform":
        h.add_pairing(delta,mode="swave")
    elif deltatype=="One sublattice": # only in one sublattice
        h.add_pairing(delta,mode="swaveA")
    elif deltatype=="sigma_z": # only in one sublattice
        h.add_pairing(delta,mode="swavez")
    elif deltatype=="Haldane": # only in one sublattice
        h.add_pairing(delta,mode="haldane")
    elif deltatype=="AntiHaldane": # only in one sublattice
        h.add_pairing(delta,mode="antihaldane")
    else: raise # not implemented





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



def show_dos(silent=False):
  h = pickup_hamiltonian() # get hamiltonian
  common.get_dos(h,qtwrap,silent=silent)





  


def show_structure():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
  execute_script("ql-structure-bond --input POSITIONS.OUT")



def solve_scf():
  """Perform a selfconsistent calculation"""
  scfin = window.getbox("scf_initialization")
  h = initialize() # initialize the Hamiltonian
  mf = scftypes.guess(h,mode=scfin)
  nk = int(get("nk_scf"))
  U = get("U")
  V1 = get("V1")
  V2 = get("V2")
  filling = get("filling_scf")
  filling = filling%1.
  # flavor of the mean field
#  compute_dd = window.is_checked("compute_dd",default=True)
#  compute_anomalous = window.is_checked("compute_anomalous",default=False)
#  compute_cross = window.is_checked("compute_cross",default=True)
#  compute_normal = window.is_checked("compute_normal",default=True)
  error = window.get("scf_error",default=1e-5) # error in the mean field
#  if compute_anomalous: h.add_swave(0.)
  scf = meanfield.Vinteraction(h,nk=nk,filling=filling,U=U,V1=V1,V2=V2,
                mf=mf,load_mf=False,
                mix = get("mix_scf"),
                maxerror=error,
                verbose=1,
                )
  mfname = scf.identify_symmetry_breaking(as_string=True)
  window.set("identified_mean_field",mfname)  
  scf.hamiltonian.save() # save in a file




def show_magnetism():
  """Show the magnetism of the system"""
  h = pickup_hamiltonian() # get the Hamiltonian
  common.show_exchange(h,qtwrap)



def show_structure_3d():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
  execute_script("ql-structure3d POSITIONS.OUT")



def sweep_parameter():
    """Perform a sweep in a parameter"""
    pname = getbox("sweep_parameter") # get the parameter
    ps = np.linspace(get("sweep_initial"),get("sweep_final"),
               int(get("sweep_steps"))) # parameters
    def modify(p): # function to change the parameter
        if pname=="Sublattice imbalance": qtwrap.modify("mAB",p)
        elif pname=="Kane-Mele": qtwrap.modify("kanemele",p)
        elif pname=="Jx": qtwrap.modify("Bx",p)
        elif pname=="Jy": qtwrap.modify("By",p)
        elif pname=="Jz": qtwrap.modify("Bz",p)
        elif pname=="Rashba": qtwrap.modify("rashba",p)
        elif pname=="Haldane": qtwrap.modify("haldane",p)
        elif pname=="Anti-Haldane": qtwrap.modify("antihaldane",p)
        elif pname=="s-wave pairing": qtwrap.modify("swave",p)
        elif pname=="Fermi": qtwrap.modify("fermi",p)
        else: raise # not implemented
    cname = getbox("sweep_task") # type of computation
    out = [] # empty list
    for p in ps: # loop over the values
        modify(p) # modify the Hamiltonian
        h = pickup_hamiltonian() # get hamiltonian
        if cname=="DOS": 
            show_dos(silent=True) # compute DOS
            m = np.genfromtxt("DOS.OUT").transpose() # get dos
            es,ds = m[0],m[1]
            for (e,d) in zip(es,ds): # loop over energies
                out.append([p,e,d])
        elif cname=="Indirect gap": # compute the gap
            g = h.get_gap() # compute Gap
            out.append([p,g]) # store result
        elif cname=="Chern number": # compute the gap
            c = topology.chern(h,nk=int(np.sqrt(get("nk_topology"))))
            out.append([p,c]) # store result
        elif cname=="Eigenvalues": # compute the gap
            kpath = [np.random.random(3) for i in range(int(get("nk_bands")))]
            (ks,es) = h.get_bands() # compute eigenvalues
            for e in es: out.append([p,e]) # store
        else: raise
    np.savetxt("SWEEP.OUT",np.matrix(out)) # store result
    if cname=="DOS":
        execute_script("ql-sweep-dos SWEEP.OUT") # remove the file
    elif cname=="Indirect gap":
        execute_script("ql-indirect-gap SWEEP.OUT") # remove the file
    elif cname=="Chern number":
        execute_script("ql-chern-evolution SWEEP.OUT") # remove the file
    else:
        execute_script("ql-indirect-gap SWEEP.OUT") # remove the file
    



inipath = os.getcwd() # get the initial directory
def save_results():  save_state(inipath,tmppath,window) # function to save
def load_results():  load_state(inipath,tmppath,window) # function to load


# create signals: STANDARD_HANDLERS covers the plain "pickup_hamiltonian
# + common.get_X" buttons automatically; only the buttons with mode-specific
# behavior need to be listed explicitly here
signals = common.wire_standard_signals(qtwrap,pickup_hamiltonian,extra={
  "solve_scf": solve_scf,  # initialize and run
  "show_structure": show_structure,  # show bandstructure
  "show_dos": show_dos,  # custom silent= support, also used by sweep_parameter
  "show_dosbands": show_dosbands,  # custom kbands-specific implementation
  "show_magnetism": show_magnetism,  # show magnetism
  "compute_sweep": sweep_parameter,
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

