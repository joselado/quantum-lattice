#!/usr/bin/python

from __future__ import print_function

import sys
import os

qhroot = os.environ["QHROOT"] # root path
sys.path.append(qhroot+"/pysrc/") # python libraries


from interfacetk import qtwrap
get = qtwrap.get  # get the value of a certain variable
getbox = qtwrap.getbox  # get the value of a certain variable
window = qtwrap.main() # this is the main interface



from interfacetk.qh_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries

common.initialize(qtwrap) # do several common initializations


def get_geometry():
  """ Create geometry"""
  lattice_name = getbox("lattice") # get the option
#  lattice_name = builder.get_object("lattice").get_active_text()
  if lattice_name=="Cubic":
    geometry_builder = geometry.cubic_lattice
  elif lattice_name=="Diamond":
    geometry_builder = geometry.diamond_lattice_minimal
  elif lattice_name=="Pyrochlore":
    geometry_builder = geometry.pyrochlore_lattice
  elif lattice_name=="Hyperhoneycomb":
    geometry_builder = geometry.hyperhoneycomb_lattice
  else: raise
  g = geometry_builder() # call the geometry
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
  if check("strain"): # custom function
    dfun = get("strain") # get function
    def fun(r1,r2): # function to compute distance
      dr = r1-r2
      dr2 = dr.dot(dr) # distance
      if 0.9<dr2<1.1: 
        if 0.9<abs(dr[2])<1.1: return 1.0 + dfun # first neighbor
        return 1.0
      else: return 0.0
    h = g.get_hamiltonian(fun) # get the Hamiltonian
  else:
    h = g.get_hamiltonian(has_spin=True)
  j = np.array([get("Bx"),get("By"),get("Bz")])
  h.add_zeeman(j) # Zeeman field
  h.add_sublattice_imbalance(get("mAB"))  # sublattice imbalance
  if check("rashba"): h.add_rashba(get("rashba"))  # Rashba field
  h.add_antiferromagnetism(get("mAF"))  # AF order
  h.shift_fermi(get("fermi")) # shift fermi energy
  if check("kanemele"):  h.add_kane_mele(get("kanemele")) # intrinsic SOC
  if check("haldane"):  h.add_haldane(get("haldane")) # intrinsic SOC
  if check("antihaldane"):  h.add_antihaldane(get("antihaldane")) 
  if check("swave"):  h.add_swave(get("swave")) 
#  h.add_peierls(get("peierls")) # shift fermi energy
  h.turn_dense()
  return h


def show_bands():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_bands(h,qtwrap) # wrapper



def show_ldos():
  """Return the LDOS"""
  h = pickup_hamiltonian() # get hamiltonian
  ewin = abs(get("window_ldos"))
  energies = np.linspace(-ewin,ewin,int(get("ne_ldos")))
  delta = get("delta_ldos")
  ldos.slabldos(h,energies=energies,delta=delta,nk=int(get("nk_ldos")))
  execute_script("qh-ldos-slab DOSMAP.OUT  ")






def show_dosbands():
  h = pickup_hamiltonian() # get hamiltonian
  kdos.kdos_bands(h,scale=get("scale_kbands"),ewindow=get("window_kbands"),
                   ne=int(get("ne_kbands")),delta=get("delta_kbands"),
                   ntries=int(get("nv_kbands")))
  execute_script("qh-dosbands  KDOS_BANDS.OUT ")



def show_dos():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_dos(h,qtwrap)



def pickup_hamiltonian():
  if qtwrap.is_checked("do_scf"):
    return hamiltonians.load() # load the Hamiltonian
  else: # generate from scratch
    return initialize()











def show_berry2d():
  h = pickup_hamiltonian() # get hamiltonian
  nk = int(get("nk_topology"))
  topology.berry_map(h,nk=nk)
  execute_script("qh-berry2d BERRY_MAP.OUT")

  

def show_magnetism():
  h = pickup_hamiltonian() # get hamiltonian
  h.get_magnetization() # get the magnetization
  execute_script("tb90-magnetism  ")
#  execute_script("qh-magnetism  ")


def show_structure():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
  execute_script("qh-structure --input POSITIONS.OUT")



def show_structure_3d():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
  execute_script("qh-structure3d POSITIONS.OUT")



def show_kdos():
  h = pickup_hamiltonian()  # get the hamiltonian
  common.get_kdos(h,qtwrap) # get the KDOS





def show_berry1d():
  h = pickup_hamiltonian()  # get the hamiltonian
  ks = klist.default(h.geometry,nk=int(get("nk_topology")))  # write klist
  topology.write_berry(h,ks)
  execute_script("qh-berry1d  label  ")


def show_z2():
  h = pickup_hamiltonian()  # get the hamiltonian
  nk = get("nk_topology")
  topology.z2_vanderbilt(h,nk=nk,nt=nk/2) # calculate z2 invariant
  execute_script("qh-wannier-center  ") # plot the result



def solve_scf():
  """Perform a selfconsistent calculation"""
  scfin = getbox("scf_initialization")
  h = initialize() # initialize the Hamiltonian
  mf = scftypes.guess(h,mode=scfin)
  nk = int(get("nk_scf"))
  U = get("hubbard")
  filling = get("filling_scf")
  filling = filling%1.
  scf = scftypes.selfconsistency(h,nkp=nk,filling=filling,g=U,
                mf=mf,mode="U",smearing=get("smearing_scf"),
                mix = get("mix_scf"))
  scf.hamiltonian.save() # save in a file



def show_magnetism():
  """Show the magnetism of the system"""
  h = pickup_hamiltonian() # get the Hamiltonian
  h.write_magnetization() # write the magnetism
  execute_script("qh-moments",mayavi=True)




save_results = lambda x: save_outputs(inipath,tmppath) # function to save


# create signals
signals = dict()
#signals["initialize"] = initialize  # initialize and run
signals["show_bands"] = show_bands  # show bandstructure
signals["show_structure"] = show_structure  # show bandstructure
signals["show_structure_3d"] = show_structure_3d  # show bandstructure
signals["show_dos"] = show_dos  # show DOS
#signals["show_berry2d"] = show_berry2d  # show DOS
#signals["show_berry1d"] = show_berry1d  # show DOS
signals["show_kdos"] = show_kdos  # show DOS
#signals["show_dosbands"] = show_dosbands  # show DOS
#signals["show_z2"] = show_z2  # show DOS
#signals["show_ldos"] = show_ldos  # show DOS
signals["show_magnetism"] = show_magnetism
signals["solve_scf"] = solve_scf 
#signals["show_magnetism"] = show_magnetism  # show magnetism
#signals["show_lattice"] = show_lattice  # show magnetism
#signals["save_results"] = save_results  # save the results





#from qh_interface import create_folder # import all the libraries needed

window.connect_clicks(signals)
folder = create_folder()
tmppath = os.getcwd() # get the initial directory
window.run()

