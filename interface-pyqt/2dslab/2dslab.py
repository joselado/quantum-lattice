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





def select_atoms_removal():
  g = get_geometry(modify=False) # get the unmodified geometry
  g.write() # write geometry
  execute_script("qh-remove-atoms-geometry-3d") # remove the file


#def modify_geometry(g):
#  """Modify the geometry according to the interface"""
#  if qtwrap.is_checked("remove_selected"): # remove some atoms
#      try:
#        inds = np.array(np.genfromtxt("REMOVE_ATOMS.INFO",dtype=np.int))
#        if inds.shape==(): inds = [inds]
#      except: inds = [] # Nothing
#      print(inds)
#      g = sculpt.remove(g,inds) # remove those atoms
#  if qtwrap.is_checked("remove_single_bonded"): # remove single bonds
#      g = sculpt.remove_unibonded(g,iterative=True)
#  return g # return geometry

from interfacetk import interfacetk
modify_geometry = lambda x: interfacetk.modify_geometry(x,qtwrap)


def get_geometry(modify=True):
  """ Create a 0d island"""
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
  g = films.geometry_film(g,int(get("thickness")))
  g = g.supercell(int(get("nsuper")))
  g.real2fractional()
  g.fractional2real()
  g.center()
  if modify: g = modify_geometry(g) # modify the geometry
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
  h.add_rashba(get("rashba"))  # Rashba field
  h.add_antiferromagnetism(get("mAF"))  # AF order
  h.add_crystal_field(qtwrap.get("crystalfield")) 
  h.shift_fermi(get("fermi")) # shift fermi energy
  h.add_kane_mele(get("kanemele")) # intrinsic SOC
  h.add_anti_kane_mele(get("antikanemele")) 
  h.add_haldane(get("haldane")) # intrinsic SOC
  h.add_antihaldane(get("antihaldane")) 
#  h.add_peierls(get("peierls")) # shift fermi energy
  if abs(get("inplaneb"))>0.0:
      h.add_inplane_bfield(b=get("inplaneb"),phi=get("inplaneb_phi"))
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
  h = pickup_hamiltonian() # get hamiltonian
  common.get_bands(h,qtwrap) # wrapper


def show_ldos():
  """Return the LDOS"""
  h = pickup_hamiltonian() # get hamiltonian
  ewin = abs(get("window_ldos"))
  energies = np.linspace(-ewin,ewin,int(get("ne_ldos")))
  delta = get("delta_ldos")
  ldos.slabldos(h,energies=energies,delta=delta,nk=int(get("nk_ldos")))
  execute_script('qh-map2d --input DOSMAP.OUT --xlabel Energy --ylabel "z-position" --zlabel DOS --title "Local DOS"')






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
  common.get_berry2d(h,qtwrap)

  

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
  execute_script("qh-structure")



def show_structure_3d():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
  execute_script("qh-structure3d POSITIONS.OUT")



def show_kdos():
  h = pickup_hamiltonian()  # get the hamiltonian
  ew = get("ewindow_kdos")
  new = int(get("mesh_kdos")) # scale as kpoints
  energies = np.linspace(-ew,ew,new) # number of ene
  kpath = [[i,0.,0.] for i in np.linspace(0.,1.,new)]
  kdos.surface(h,energies=energies,delta=ew/new,kpath=kpath)
  execute_script("qh-kdos-both KDOS.OUT  ")





def show_berry1d():
  h = pickup_hamiltonian()  # get the hamiltonian
  common.get_berry1d(h,qtwrap)


def show_z2():
  h = pickup_hamiltonian()  # get the hamiltonian
  common.get_z2(h,qtwrap)


def show_chern():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_chern(h,qtwrap)





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

def show_fermi_surface():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_fermi_surface(h,qtwrap)





save_results = lambda x: save_outputs(inipath,tmppath) # function to save


# create signals
signals = dict()
#signals["initialize"] = initialize  # initialize and run
signals["show_bands"] = show_bands  # show bandstructure
signals["show_structure"] = show_structure  # show bandstructure
signals["show_structure_3d"] = show_structure_3d  # show bandstructure
signals["show_dos"] = show_dos  # show DOS
signals["show_berry2d"] = show_berry2d  # show DOS
signals["show_chern"] = show_chern  
signals["show_berry1d"] = show_berry1d  # show DOS
signals["show_kdos"] = show_kdos  # show DOS
signals["show_dosbands"] = show_dosbands  # show DOS
signals["show_z2"] = show_z2  # show DOS
signals["show_ldos"] = show_ldos  # show DOS
signals["show_magnetism"] = show_magnetism
signals["solve_scf"] = solve_scf 
signals["select_atoms_removal"] = select_atoms_removal
signals["show_fermi_surface"] = show_fermi_surface

#signals["show_magnetism"] = show_magnetism  # show magnetism
#signals["show_lattice"] = show_lattice  # show magnetism
#signals["save_results"] = save_results  # save the results






window.connect_clicks(signals)
folder = create_folder()
tmppath = os.getcwd() # get the initial directory
window.run()

