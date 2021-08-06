#!/usr/bin/python

from __future__ import print_function

import sys
import os

qhroot = os.environ["QHROOT"] # root path
sys.path.append(qhroot+"/pysrc/") # python libraries


from interfacetk import qtwrap # import the library with simple wrappaers to qt4
get = qtwrap.get  # get the value of a certain variable
getbox = qtwrap.getbox  # get the value of a certain variable
window = qtwrap.main() # this is the main interface



from interfacetk.qh_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries

common.initialize(qtwrap) # do several common initializations

qtwrap.set_combobox("scf_initialization",meanfield.spinful_guesses)
qtwrap.set_combobox("bands_color",operators.operator_list)


def get_geometry(modify=True):
  """ Create a 0d island"""
  lattice_name = getbox("lattice") # get the option
  if lattice_name=="Honeycomb":
    geometry_builder = geometry.honeycomb_lattice
  elif lattice_name=="Honeycomb 4 sites":
    geometry_builder = geometry.honeycomb_lattice_square_cell
  elif lattice_name=="Square":
    geometry_builder = geometry.square_lattice
  elif lattice_name=="Single square":
    geometry_builder = geometry.single_square_lattice
  elif lattice_name=="Kagome":
    geometry_builder = geometry.kagome_lattice
  elif lattice_name=="Lieb":
    geometry_builder = geometry.lieb_lattice
  elif lattice_name=="Triangular":
    geometry_builder = geometry.triangular_lattice
  elif lattice_name=="Triangular tripartite":
    geometry_builder = lambda: geometry.triangular_lattice(n=3)
  elif lattice_name=="Honeycomb 6 sites":
    geometry_builder = lambda: geometry.honeycomb_lattice(n=3)
  else: raise
  g = geometry_builder() # call the geometry
  nsuper = int(get("nsuper"))
  g = g.supercell(nsuper)
  if modify: g = modify_geometry(g) # modify the geometry
  return g





def select_atoms_removal():
  g = get_geometry(modify=False) # get the unmodified geometry
  g.write() # write geometry
  execute_script("qh-remove-atoms-geometry") # remove the file


def modify_geometry(g):
  """Modify the geometry according to the interface"""
  if qtwrap.is_checked("remove_selected"): # remove some atoms
      try:
        inds = np.array(np.genfromtxt("REMOVE_ATOMS.INFO",dtype=np.int))
        if inds.shape==(): inds = [inds]
      except: inds = [] # Nothing
      print(inds)
      g = sculpt.remove(g,inds) # remove those atoms
  if qtwrap.is_checked("remove_single_bonded"): # remove single bonds
      g = sculpt.remove_unibonded(g,iterative=True)
#  g.save()
  return g # return geometry











def initialize():
  """ Initialize the calculation"""
  g = get_geometry() # get the geometry
  h = g.get_hamiltonian(has_spin=True)
  h.add_zeeman([get("Bx"),get("By"),get("Bz")]) # Zeeman fields
  h.add_sublattice_imbalance(get("mAB"))  # sublattice imbalance
  h.add_rashba(get("rashba"))  # Rashba field
  h.add_antiferromagnetism(get("mAF"))  # AF order
  h.shift_fermi(get("fermi")) # shift fermi energy
  h.add_kane_mele(get("kanemele")) # intrinsic SOC
  h.add_haldane(get("haldane")) # intrinsic SOC
  h.add_antihaldane(get("antihaldane")) 
  h.add_anti_kane_mele(get("antikanemele")) 
  if abs(get("swave"))>0.0: 
      h = h.get_multicell()
      special_pairing(h)
  return h



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






def show_bands():
  comp = computing() # create the computing window
  h = pickup_hamiltonian() # get hamiltonian
  common.get_bands(h,qtwrap) # get the band structure
  comp.kill()



def show_dosbands():
  h = pickup_hamiltonian() # get hamiltonian
  kdos.kdos_bands(h,scale=get("scale_kbands"),ewindow=get("window_kbands"),
                   ne=int(get("ne_kbands")),delta=get("delta_kbands"),
                   ntries=int(get("nv_kbands")))
  execute_script("qh-dosbands  KDOS_BANDS.OUT ")



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
#  execute_script("qh-light-structure POSITIONS.OUT")
  execute_script("qh-structure-bond --input POSITIONS.OUT")
#  execute_script("qh-structure  ")



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


def solve_scf():
  """Perform a selfconsistent calculation"""
#  comp = computing() # create the computing window
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
  compute_dd = window.is_checked("compute_dd",default=True)
  compute_anomalous = window.is_checked("compute_anomalous",default=False)
  compute_cross = window.is_checked("compute_cross",default=True)
  compute_normal = window.is_checked("compute_normal",default=True)
  error = window.get("scf_error",default=1e-5) # error in the mean field
  if compute_anomalous: h.add_swave(0.)
  scf = meanfield.Vinteraction(h,nk=nk,filling=filling,U=U,V1=V1,V2=V2,
                mf=mf,load_mf=False,#T=get("smearing_scf"),
                mix = get("mix_scf"),
                compute_dd=compute_dd,
                compute_anomalous=compute_anomalous,
                compute_cross=compute_cross,
                compute_normal=compute_normal,
                maxerror=error
                )
  mfname = scf.identify_symmetry_breaking(as_string=True)
  window.set("identified_mean_field",mfname)  
  scf.hamiltonian.save() # save in a file
#  comp.kill()



def show_magnetism_3d():
  """Show the magnetism of the system"""
  h = pickup_hamiltonian() # get the Hamiltonian
  h.write_magnetization(nrep=int(get("magnetization_nrep"))) 
  execute_script("qh-moments",mayavi=True)


def show_magnetism():
  """Show the magnetism of the system"""
  h = pickup_hamiltonian() # get the Hamiltonian
  h.write_magnetization(nrep=int(get("magnetization_nrep"))) 
  execute_script("qh-quiver")


def show_structure_3d():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
  execute_script("qh-structure3d POSITIONS.OUT")



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
        execute_script("qh-sweep-dos SWEEP.OUT") # remove the file
    elif cname=="Indirect gap":
        execute_script("qh-indirect-gap SWEEP.OUT") # remove the file
    elif cname=="Chern number":
        execute_script("qh-chern-evolution SWEEP.OUT") # remove the file
    else:
        execute_script("qh-indirect-gap SWEEP.OUT") # remove the file
    







save_results = lambda x: save_outputs(inipath,tmppath) # function to save


# create signals
signals = dict()
signals["solve_scf"] = solve_scf  # initialize and run
signals["show_bands"] = show_bands  # show bandstructure
signals["show_structure"] = show_structure  # show bandstructure
signals["show_dos"] = show_dos  # show DOS
signals["show_berry2d"] = show_berry2d  # show DOS
signals["show_chern"] = show_chern  # show the chern number
signals["show_berry1d"] = show_berry1d  # show DOS
signals["show_kdos"] = show_kdos  # show DOS
signals["show_fermi_surface"] = show_fermi_surface
signals["show_qpi"] = show_qpi
signals["show_dosbands"] = show_dosbands  # show DOS
signals["show_z2"] = show_z2  # show DOS
signals["show_magnetism"] = show_magnetism  # show magnetism
signals["show_magnetism_3d"] = show_magnetism_3d  # show magnetism
signals["compute_sweep"] = sweep_parameter  
signals["show_structure_3d"] = show_structure_3d
signals["select_atoms_removal"] = select_atoms_removal
signals["show_multildos"] = show_multildos






window.connect_clicks(signals)
folder = create_folder()
tmppath = os.getcwd() # get the initial directory
window.run()

