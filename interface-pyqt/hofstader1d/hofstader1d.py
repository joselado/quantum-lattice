#!/usr/bin/env python3

from __future__ import print_function

import sys
import os

# main path
qlroot = os.path.dirname(os.path.realpath(__file__))+"/../.."
sys.path.append(qlroot+"/pysrc/") # python libraries

from interfacetk import qtwrap
get = qtwrap.get  # get the value of a certain variable
modify = qtwrap.modify  # get the value of a certain variable
getbox = qtwrap.getbox  # get the value of a certain variable
window = qtwrap.new_page(os.path.dirname(os.path.realpath(__file__))) # this mode's page


from interfacetk.qh_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries

from interfacetk import interfacetk
modify_geometry = lambda x: interfacetk.modify_geometry(x,qtwrap)

from interfacetk import latticeterms
latticeterms.connect(qtwrap,lambda: getbox("lattice")) # hide honeycomb-only
                                                         # terms (Haldane,
                                                         # Kane-Mele, valley)
                                                         # for other lattices


def get_geometry(modify=True):
  lattice_name = getbox("lattice") # get the option
  n = int(get("ribbon_width")) # thickness of the system
  lattices = {
    "Chain": geometry.chain,
    "Honeycomb": geometry.honeycomb_lattice,
    "Square": geometry.square_lattice,
    "Kagome": geometry.kagome_lattice,
    "Lieb": geometry.lieb_lattice,
    "Triangular": geometry.triangular_lattice,
    "Honeycomb zigzag": lambda: geometry.honeycomb_zigzag_ribbon(n),
    "Honeycomb armchair": lambda: geometry.honeycomb_armchair_ribbon(n),
    "Graphene": geometry.honeycomb_lattice,
    "Bilayer graphene AB": lambda: multilayers.get_geometry("AB"),
    "Bilayer graphene AA": lambda: multilayers.get_geometry("AA"),
  }
  g = lattices[lattice_name]()
  if g.dimensionality==2: # original is a 2d geometry
    g = ribbon.bulk2ribbon(g,n=n,clean=False)
  nsuper = int(get("nsuper"))
  g = g.supercell(nsuper)
  if modify: g = modify_geometry(g)
  return g











def initialize():
  """ Initialize the calculation"""
  g = get_geometry() # get the geometry
  fun = multilayers.multilayer_hopping(ti=get("ti"))
  h = g.get_hamiltonian(tij=fun)
  h.add_peierls(get("peierls")) # magnetic field
  h.add_zeeman(qtwrap.get_array("exchange")) # Zeeman fields
  h.add_sublattice_imbalance(get("mAB"))  # sublattice imbalance
  h.add_rashba(get("rashba"))  # Rashba field
  h.add_antiferromagnetism(get("mAF"))  # AF order
  h.shift_fermi(get("fermi")) # shift fermi energy
  h.add_kane_mele(get("kanemele")) # intrinsic SOC
  h.add_haldane(get("haldane")) # intrinsic SOC
  h.add_antihaldane(get("antihaldane")) 
#  if abs(get("swave"))>0.0:  h.add_swave(get("swave")) 
#  h.add_peierls(get("peierls")) # shift fermi energy
  h = h.reduce()
  return h


def show_bands():
  h = pickup_hamiltonian() # get hamiltonian
  opname = getbox("bands_color")
  if opname=="None": op = None # no operators
  elif opname=="Sx": op = h.get_operator("sx") # off plane case
  elif opname=="Sy": op = h.get_operator("sy")# off plane case
  elif opname=="Sz": op = h.get_operator("sz")# off plane case
  elif opname=="Valley": op = h.get_operator("valley")
  elif opname=="y-position": op = h.get_operator("yposition")
  else: op =None
  kpath = h.geometry.get_default_kpath(nk=int(get("nk_bands")))
  h.get_bands(operator=op,kpath=kpath)
  execute_script("ql-bands1d  ")



def show_dosbands():
  h = pickup_hamiltonian() # get hamiltonian
  ew = get("window_kbands")
  energies = np.linspace(-ew,ew,int(get("ne_kbands")))
  h.get_kdos_bands(scale=get("scale_kbands"),energies=energies,
                   delta=get("delta_kbands"),
                   ntries=int(get("nv_kbands")))
  execute_script("ql-dosbands1d --input KDOS_BANDS.OUT ")




def show_interactive_ldos():
  h = pickup_hamiltonian()  # get the hamiltonian
  common.get_interactive_ldos(h,qtwrap)






def show_dos():
  h = pickup_hamiltonian() # get hamiltonian
  # h.get_dos() is pyqula's general DOS entry point and handles every
  # dimensionality itself - no per-dimensionality branch needed (the
  # dos.dos0d/dos1d/dos2d calls this used to make were wrong: dos0d takes
  # "energies", not "es", and dos1d/dos2d do not exist at all)
  h.get_dos(delta=get("dos_delta"),energies=np.linspace(-3.1,3.1,500))
  execute_script("ql-dos  ")


pickup_hamiltonian = lambda: common.pickup_hamiltonian(qtwrap,initialize)

  



def show_structure():
  """Show the lattice of the system"""
  common.show_structure(qtwrap,get_geometry)


select_atoms_removal = lambda: common.select_atoms_removal(get_geometry)


def show_hofstader():
  bmin = get("minb_hofs")
  bmax = get("maxb_hofs")
  nb = int(get("numb_hofs"))
  bs = np.linspace(bmin,bmax,nb) # array with bfields
  # funcion for the generation of random vectors
  mode = getbox("hofstader_mode")
  h = pickup_hamiltonian() # pick the Hamiltonian
  if mode=="All":
    fun = None # no function
  elif mode=="Bulk":
    op = h.get_operator("bulk").get_matrix() # get the matrix
    def fun(): 
        return op@(np.random.random(op.shape[0])-0.5)
  elif mode=="Edge":
    op = h.get_operator("bulk").get_matrix() # get the matrix
    def fun(): 
        v = np.random.random(op.shape[0])-0.5
        return v - op@v # return the edge
  else: raise
  ew = get("ewindow_hofs") # energy window of each DOS
  ne = int(get("nume_hofs")) # number of energies of each DOS
  f = open("HOFSTADER.OUT","w")
  for b in bs:
    modify("peierls",str(round(b,4)))
    h = pickup_hamiltonian() # pick the Hamiltonian
    # h.get_dos() is pyqula's general DOS entry point (the old dos.dos1d()
    # call did not exist); use_kpm routes it to the stochastic KPM
    # estimator, which is what accepts frand (the Bulk/Edge random-vector
    # generator above) and ntries. The number of Chebyshev polynomials is
    # set indirectly through delta (npol = scale/delta inside dos_kpm),
    # here the spacing of the energy grid.
    (es,ds) = h.get_dos(energies=np.linspace(-ew,ew,ne),use_kpm=True,
               nk=int(get("nk_hofs")),delta=2.*ew/ne,
               ntries=int(get("nite_hofs")),frand=fun)
    for (e,d) in zip(es,ds):
      f.write(str(b)+"   ")
      f.write(str(e)+"   ")
      f.write(str(d)+"\n")
    f.flush()
  f.close()
  execute_script("ql-map2d --input HOFSTADER.OUT --xlabel 'Magnetic field' --ylabel Energy --zlabel DOS --title 'Hofstadter spectra'")




# create signals (save_results/load_results are wired automatically by
# common.finalize_page())
signals = dict()
#signals["initialize"] = initialize  # initialize and run
signals["show_bands"] = show_bands  # show bandstructure
signals["show_structure"] = show_structure
signals["show_dos"] = show_dos
signals["show_dosbands"] = show_dosbands  # DOS resolved along the band structure
signals["show_hofstader"] = show_hofstader  # Hofstadter butterfly spectrum
signals["show_interactive_ldos"] = show_interactive_ldos
signals["show_site_dos"] = lambda: common.get_site_dos(pickup_hamiltonian(),qtwrap,use_kpm=True) # magnetic-field supercells are too large for ED
signals["select_atoms_removal"] = select_atoms_removal



inipath = os.getcwd() # get the initial directory, before common.finalize_page()'s create_folder() chdirs away
common.finalize_page(qtwrap,window,signals,inipath,robust=False)

if __name__ == "__main__":
    window.run() # show this page as its own standalone window and block

