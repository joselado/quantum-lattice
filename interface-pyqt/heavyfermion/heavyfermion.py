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



from interfacetk.qlinterface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries

#common.initialize(qtwrap) # do several common initializations


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
  execute_script("ql-remove-atoms-geometry") # remove the file


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




def show_bands():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_bands(h,qtwrap) # get the band structure



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


def pickup_hamiltonian():
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



def show_fermi_surface():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_fermi_surface(h,qtwrap)


def show_qpi():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_qpi(h,qtwrap)


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




save_results = lambda x: save_outputs(inipath,tmppath) # function to save


# create signals
signals = dict()
signals["show_bands"] = show_bands  # show bandstructure
signals["show_structure"] = show_structure  # show bandstructure
signals["show_dos"] = show_dos  # show DOS
signals["show_kdos"] = show_kdos  # show DOS
signals["show_fermi_surface"] = show_fermi_surface
signals["show_qpi"] = show_qpi
signals["show_dosbands"] = show_dosbands  # show DOS
signals["show_structure_3d"] = show_structure_3d
signals["select_atoms_removal"] = select_atoms_removal
signals["show_multildos"] = show_multildos






window.connect_clicks(signals,robust=True)
folder = create_folder()
tmppath = os.getcwd() # get the initial directory
window.run()

