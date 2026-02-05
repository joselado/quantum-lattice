#!/usr/bin/python

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

qtwrap.set_combobox("bands_color",operators.operator_list)


def get_geometry():
    """Return the geometry"""
    return initialize().geometry


def initialize():
  """ Initialize the calculation"""
  from pyqula import specialhamiltonian
  h = specialhamiltonian.NbSe2(soc=get("ising_SOC"),cdw=get("cdw"))
  h.add_zeeman([get("Bx"),get("By"),get("Bz")]) # Zeeman fields
  h.add_rashba(get("rashba"))  # Rashba field
  h.set_filling(0.5,nk=10) # half filling
  h.shift_fermi(get("fermi")) # shift fermi energy
  if abs(get("swave"))>0.0: h.add_swave(get("swave"))
  return h





def show_bands():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_bands(h,qtwrap) # get the band structure



def show_dosbands():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_kdos_bands(h,qtwrap) # compute DOS



def show_dos(silent=False):
  h = pickup_hamiltonian() # get hamiltonian
  common.get_dos(h,qtwrap,silent=silent)


def pickup_hamiltonian():
  if qtwrap.is_checked("do_scf"):
    return hamiltonians.load() # load the Hamiltonian
  else: # generate from scratch
    return initialize()



  




  


def show_structure():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
  execute_script("ql-structure-bond --input POSITIONS.OUT")


def show_kdos():
  h = pickup_hamiltonian()  # get the hamiltonian
  common.get_kdos(h,qtwrap) # get the KDOS




def show_berry1d():
  h = pickup_hamiltonian()  # get the hamiltonian
  common.get_berry1d(h,qtwrap) # compute Berry 1D


def show_z2():
  h = pickup_hamiltonian()  # get the hamiltonian
  common.get_z2(h,qtwrap) # compute Berry 1D


def show_berry2d():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_berry2d(h,qtwrap)


def show_chern():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_chern(h,qtwrap)

def show_fermi_surface():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_fermi_surface(h,qtwrap)


def show_qpi():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_qpi(h,qtwrap)



def show_magnetism_3d():
  """Show the magnetism of the system"""
  h = pickup_hamiltonian() # get the Hamiltonian
  h.write_magnetization(nrep=int(get("magnetization_nrep"))) 
  execute_script("ql-moments",mayavi=True)


def show_magnetism():
  """Show the magnetism of the system"""
  h = pickup_hamiltonian() # get the Hamiltonian
  h.write_magnetization(nrep=int(get("magnetization_nrep"))) 
  execute_script("ql-quiver")


def show_structure_3d():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
  execute_script("ql-structure3d POSITIONS.OUT")



def show_multildos():
  h = pickup_hamiltonian()  # get the hamiltonian
  common.get_multildos(h,qtwrap)



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
    







save_results = lambda x: save_outputs(inipath,tmppath) # function to save


# create signals
signals = dict()
signals["show_bands"] = show_bands  # show bandstructure
signals["show_structure"] = show_structure  # show bandstructure
signals["show_dos"] = show_dos  # show DOS
signals["show_berry2d"] = show_berry2d  # show DOS
signals["show_chern"] = show_chern  # show the chern number
signals["show_berry1d"] = show_berry1d  # show DOS
signals["show_kdos"] = show_kdos  # show DOS
signals["show_fermi_surface"] = show_fermi_surface
signals["show_dosbands"] = show_dosbands  # show DOS
signals["show_z2"] = show_z2  # show DOS
signals["show_structure_3d"] = show_structure_3d
signals["show_multildos"] = show_multildos






window.connect_clicks(signals,robust=False)
folder = create_folder()
tmppath = os.getcwd() # get the initial directory
window.run()

