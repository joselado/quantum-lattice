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
window = qtwrap.main() # this is the main interface


from interfacetk.qh_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries




def get_geometry():
  lattice_name = getbox("lattice") # get the option
  n = int(get("width")) # thickness of the system
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
  return g











def initialize():
  """ Initialize the calculation"""
  g = get_geometry() # get the geometry
  fun = multilayers.multilayer_hopping(ti=get("ti"))
  h = g.get_hamiltonian(fun=fun)
  h.add_peierls(get("peierls")) # magnetic field
  h.add_zeeman([get("Bx"),get("By"),get("Bz")]) # Zeeman fields
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
  h.get_bands(operator=op)
  execute_script("ql-bands1d  ")



def show_dosbands():
  h = pickup_hamiltonian() # get hamiltonian
  kdos.kdos_bands(h,scale=get("scale_kbands"),ewindow=get("window_kbands"),
                   ne=int(get("ne_kbands")),delta=get("delta_kbands"),
                   ntries=int(get("nv_kbands")))
  execute_script("ql-dosbands1d --input KDOS_BANDS.OUT ")




def show_interactive_ldos():
  h = pickup_hamiltonian()  # get the hamiltonian
  ewin = get("window_ldos")
  nrep = int(get("nsuper_ldos"))
  nk = int(get("nk_ldos"))
  ne = int(get("ne_ldos"))
  delta = get("delta_ldos")
  ldos.multi_ldos(h,es=np.linspace(-ewin,ewin,ne),nk=nk,delta=delta,nrep=nrep)
  execute_script("ql-multildos ")






def show_dos():
  h = pickup_hamiltonian() # get hamiltonian
#  mode = getbox("mode_dos") # mode for the DOS
  if h.dimensionality==0:
    dos.dos0d(h,es=np.linspace(-3.1,3.1,500),delta=get("DOS_smearing"))
  elif h.dimensionality==1:
#    dos.dos1d(h,ndos=400,delta=get("DOS_smearing"))
    dos.dos1d(h,ndos=400)
  elif h.dimensionality==2:
    dos.dos2d(h,ndos=500,delta=get("DOS_smearing"))
  else: raise
  execute_script("ql-dos  ")


pickup_hamiltonian = lambda: common.pickup_hamiltonian(qtwrap,initialize)

  



def show_structure():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
  execute_script("ql-structure-bond --input POSITIONS.OUT")


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
  f = open("HOFSTADER.OUT","w")
  for b in bs:
    modify("peierls",str(round(b,4)))
    h = pickup_hamiltonian() # pick the Hamiltonian
    npol = 10*int(get("nume_hofs"))
    (es,ds)=dos.dos1d(h,ewindow=get("ewindow_hofs"),ndos=int(get("nume_hofs")),
               use_kpm=True,nk=int(get("nk_hofs")),npol=npol,
               ntries=int(get("nite_hofs")),frand=fun)
    for (e,d) in zip(es,ds):
      f.write(str(b)+"   ")
      f.write(str(e)+"   ")
      f.write(str(d)+"\n")
    f.flush()
  f.close()
  execute_script("ql-map2d --input HOFSTADER.OUT --xlabel 'Magnetic field' --ylabel Energy --zlabel DOS --title 'Hofstadter spectra'")




def save_results():  save_state(inipath,tmppath,window) # function to save
def load_results():  load_state(inipath,tmppath,window) # function to load


# create signals
signals = dict()
#signals["initialize"] = initialize  # initialize and run
signals["show_bands"] = show_bands  # show bandstructure
signals["show_structure"] = show_structure  # show bandstructure
signals["show_dos"] = show_dos  # show DOS
signals["show_dosbands"] = show_dosbands  # show DOS
signals["show_hofstader"] = show_hofstader  # show DOS
signals["show_interactive_ldos"] = show_interactive_ldos  # show DOS
signals["save_results"] = save_results
signals["load_results"] = load_results






window.connect_clicks(signals,robust=False)
inipath = os.getcwd() # get the initial directory
folder = create_folder()
tmppath = os.getcwd() # get the initial directory
window.run()

