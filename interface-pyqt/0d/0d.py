#!/usr/bin/python

from __future__ import print_function

import sys
import os

qhroot = os.path.dirname(os.path.realpath(__file__))+"/../../"
sys.path.append(qhroot+"/pysrc/") # python libraries


from interfacetk import qtwrap # import the library with simple wrappaers to qt4
get = qtwrap.get  # get the value of a certain variable
getbox = qtwrap.getbox  # get the value of a certain variable
window = qtwrap.main() # this is the main interface



from interfacetk.qh_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries
common.initialize(qtwrap) # several initilizations



def get_geometry(modify=True):
  """ Create a 0d island"""
  lattice_name = getbox("lattice") # get the option
  n = float(get("width")) # thickness of the system
#  lattice_name = builder.get_object("lattice").get_active_text()
  if lattice_name=="Chain":
    g = geometry.chain()
  if lattice_name=="Honeycomb":
    g = geometry.honeycomb_lattice()
  elif lattice_name=="Square":
    g = geometry.single_square_lattice()
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
  rot = get("rotation")*np.pi/180.
  g = islands.get_geometry(n=n,nedges=int(get("nsides")),rot=rot,geo=g)
  if modify: g = modify_geometry(g) # modify the geometry
  return g


def select_atoms_removal():
  g = get_geometry(modify=False) # get the unmodified geometry
  g.write() # write geometry
  execute_script("qh-remove-atoms-geometry") # remove the file



def select_atom_time_evolution():
  """Select a single atom"""
  g = get_geometry() # get the unmodified geometry
  g.write()
  execute_script("qh-pick-single-atom") # pick a single atom


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
  execute_script("qh-multitimeevolution") # plot the result






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
  g.center()
  return g # return geometry
  


     






def initialize():
  """ Initialize the calculation"""
  g = get_geometry() # get the geometry
  t2,t3 = get("t2"),get("t3") # get hoppings
  if t2!=0.0 or t3!=0.0:
      ts = [1.,t2,t3]
      fm = specialhopping.neighbor_hopping_matrix(g,ts)
      h = g.get_hamiltonian(mgenerator=fm,has_spin=True)
  else:
      h = g.get_hamiltonian(has_spin=True)
  h.add_zeeman([get("Bx"),get("By"),get("Bz")]) # Zeeman fields
  h.add_sublattice_imbalance(get("mAB"))  # sublattice imbalance
  h.add_rashba(get("rashba"))  # Rashba field
  h.add_antiferromagnetism(get("mAF"))  # AF order
  h.add_crystal_field(qtwrap.get("crystalfield")) # add magnetic field
  h.shift_fermi(get("fermi")) # shift fermi energy
  h.add_kane_mele(get("kanemele")) # intrinsic SOC
  h.add_haldane(get("haldane")) # intrinsic SOC
  h.add_antihaldane(get("antihaldane")) 
  h.add_peierls(get("peierls")) # magnetic field
  if get("swave")!=0.0: h.add_swave(get("swave")) 
  return h


def show_bands():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_bands(h,qtwrap) # wrapper


def show_dosbands():
  h = pickup_hamiltonian() # get hamiltonian
  kdos.kdos_bands(h,scale=get("scale_kbands"),ewindow=get("window_kbands"),
                   ne=int(get("ne_kbands")),delta=get("delta_kbands"),
                   ntries=int(get("nv_kbands")))
  execute_script("qh-dosbands1d  KDOS_BANDS.OUT ")




def show_interactive_ldos():
  h = pickup_hamiltonian()  # get the hamiltonian
  common.get_multildos(h,qtwrap) # compute




def show_structure():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
#  execute_script("qh-light-structure POSITIONS.OUT")
  execute_script("qh-structure-bond --input POSITIONS.OUT")
#  execute_script("qh-structure  ")




def show_structure_3d():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
  execute_script("qh-structure3d POSITIONS.OUT")



def solve_scf():
  """Perform a selfconsistent calculation"""
  h = initialize()
  common.solve_scf(h,qtwrap)


def pickup_hamiltonian():
  if qtwrap.is_checked("do_scf"):
    return hamiltonians.load() # load the Hamiltonian
  else: # generate from scratch
    return initialize()





def show_magnetism():
  """Show the magnetism of the system"""
  h = pickup_hamiltonian() # get the Hamiltonian
  h.write_magnetization() # write the magnetism
  execute_script("qh-moments",mayavi=True)



def show_dos():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_dos(h,qtwrap) # compute DOS


def show_local_chern():
  h = pickup_hamiltonian() # get hamiltonian
  op = getbox("operator_chern")
  op = h.get_operator(op)
  topology.real_space_chern(h,operator=op)
  execute_script("qh-potential --input REAL_SPACE_CHERN.OUT --cmap rainbow")



inipath = os.getcwd() # get the initial directory
folder = create_folder() # create a new folder
tmppath = os.getcwd() # get the initial directory
save_results = lambda: save_outputs(inipath,tmppath) # function to save


# create signals
signals = dict()
#signals["initialize"] = initialize  # initialize and run
signals["solve_scf"] = solve_scf
signals["show_bands"] = show_bands  # show bandstructure
signals["show_structure"] = show_structure  # show bandstructure
signals["show_dos"] = show_dos  # show DOS
signals["show_structure_3d"] = show_structure_3d
signals["show_interactive_ldos"] = show_interactive_ldos  # show DOS
signals["show_magnetism"] = show_magnetism
signals["select_atoms_removal"] = select_atoms_removal
signals["select_atom_time_evolution"] = select_atom_time_evolution
signals["show_time_evolution"] = show_time_evolution
signals["show_local_chern"] = show_local_chern
signals["save_results"] = save_results





#from qh_interface import create_folder # import all the libraries needed

window.connect_clicks(signals)
window.run()

