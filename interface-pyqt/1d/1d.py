#!/usr/bin/python

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






def get_geometry(modify=True):
  """ Create a 0d island"""
  lattice_name = getbox("lattice") # get the option
  n = int(get("width")) # thickness of the system
#  lattice_name = builder.get_object("lattice").get_active_text()
  if lattice_name=="Chain":
    g = geometry.chain()
    print(g.r)
  elif lattice_name=="Bichain":
    g = geometry.bichain()
  elif lattice_name=="Honeycomb":
    g = geometry.honeycomb_lattice()
  elif lattice_name=="Square":
    g = geometry.square_lattice()
  elif lattice_name=="Kagome":
    g = geometry.kagome_lattice()
  elif lattice_name=="Lieb":
    g = geometry.lieb_lattice()
  elif lattice_name=="Triangular":
    g = geometry.triangular_lattice_tripartite()
  elif lattice_name=="Honeycomb zigzag":
    g = geometry.honeycomb_zigzag_ribbon(n)
  elif lattice_name=="Honeycomb armchair":
    g = geometry.honeycomb_armchair_ribbon(n)
  if g.dimensionality==2: # original is a 2d geometry
    g = ribbon.bulk2ribbon(g,n=n)
  nsuper = int(get("nsuper"))
  g = g.supercell(nsuper)
  if modify: g = modify_geometry(g) # modify the geometry
  return g




def select_atoms_removal():
  g = get_geometry(modify=False) # get the unmodified geometry
  g.write() # write geometry
  execute_script("ql-remove-atoms-geometry") # remove the file


def modify_geometry(g):
  """Modify the geometry according to the interface"""
  if qtwrap.is_checked("remove_selected"): # remove some atoms
      try:
        inds = np.array(np.genfromtxt("REMOVE_ATOMS.INFO",dtype=np.int_))
        if inds.shape==(): inds = [inds]
      except: inds = [] # Nothing
      g = sculpt.remove(g,inds) # remove those atoms
  if qtwrap.is_checked("remove_single_bonded"): # remove single bonds
      g = sculpt.remove_unibonded(g,iterative=True)
  return g # return geometry








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


def show_bands():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_bands(h,qtwrap) # wrapper



def show_edge_dos():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_surface_dos(h,qtwrap) # wrapper



def show_dosbands():
  h = pickup_hamiltonian() # get hamiltonian
  kdos.kdos_bands(h,scale=get("scale_kbands"),ewindow=get("window_kbands"),
                   ne=int(get("ne_kbands")),delta=get("delta_kbands"),
                   ntries=int(get("nv_kbands")))
  execute_script("ql-dosbands1d --input KDOS_BANDS.OUT ")




def show_multildos():
  h = pickup_hamiltonian()  # get the hamiltonian
  common.get_multildos(h,qtwrap)






def show_dos():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_dos(h,qtwrap) # compute DOS



def pickup_hamiltonian():
  if qtwrap.is_checked("do_scf"):
    return hamiltonians.load() # load the Hamiltonian
  else: # generate from scratch
    return initialize()



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





save_results = lambda x: save_outputs(inipath,tmppath) # function to save


# create signals
signals = dict()
#signals["initialize"] = initialize  # initialize and run
signals["show_bands"] = show_bands  # show bandstructure
signals["show_structure"] = show_structure  # show bandstructure
signals["show_dos"] = show_dos  # show DOS
signals["show_dosbands"] = show_dosbands  # show DOS
signals["show_multildos"] = show_multildos  # show DOS
signals["show_ldos"] = show_ldos  # show DOS
signals["show_edge_dos"] = show_edge_dos  # show DOS
signals["show_structure_3d"] = show_structure_3d
signals["show_magnetism"] = show_magnetism 
signals["solve_scf"] = solve_scf
signals["select_atoms_removal"] = select_atoms_removal




window.connect_clicks(signals)
folder = create_folder()
tmppath = os.getcwd() # get the initial directory
window.run()

