#!/usr/bin/python

from __future__ import print_function

import sys
import os

qhroot = os.environ["QHROOT"] # root path
sys.path.append(qhroot+"/pysrc/") # python libraries

from interfacetk import qtwrap
get = qtwrap.get  # get the value of a certain variable
modify = qtwrap.modify  # get the value of a certain variable
getbox = qtwrap.getbox  # get the value of a certain variable
window = qtwrap.main() # this is the main interface


from interfacetk.qh_interface import * # import all the libraries needed




def get_geometry():
  lattice_name = getbox("lattice") # get the option
  n = int(get("width")) # thickness of the system
#  lattice_name = builder.get_object("lattice").get_active_text()
  if lattice_name=="Chain":
    g = geometry.chain()
  if lattice_name=="Honeycomb":
    g = geometry.honeycomb_lattice()
  elif lattice_name=="Square":
    g = geometry.square_lattice()
  elif lattice_name=="Kagome":
    g = geometry.kagome_lattice()
  elif lattice_name=="Lieb":
    g = geometry.lieb_lattice()
  elif lattice_name=="Triangular":
    g = geometry.triangular_lattice()
  elif lattice_name=="Honeycomb zigzag":
    g = geometry.honeycomb_zigzag_ribbon(n)
  elif lattice_name=="Honeycomb armchair":
    g = geometry.honeycomb_armchair_ribbon(n)
  ##################
  elif lattice_name=="Graphene":
    g = geometry.honeycomb_lattice()
  elif lattice_name=="Bilayer graphene AB":
    g = multilayers.get_geometry("AB")
  elif lattice_name=="Bilayer graphene AA":
    g = multilayers.get_geometry("AA")
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
  execute_script("qh-bands1d  ")



def show_dosbands():
  h = pickup_hamiltonian() # get hamiltonian
  kdos.kdos_bands(h,scale=get("scale_kbands"),ewindow=get("window_kbands"),
                   ne=int(get("ne_kbands")),delta=get("delta_kbands"),
                   ntries=int(get("nv_kbands")))
  execute_script("qh-dosbands1d  KDOS_BANDS.OUT ")




def show_interactive_ldos():
  h = pickup_hamiltonian()  # get the hamiltonian
  ewin = get("window_ldos")
  nrep = int(get("nsuper_ldos"))
  nk = int(get("nk_ldos"))
  ne = int(get("ne_ldos"))
  delta = get("delta_ldos")
  ldos.multi_ldos(h,es=np.linspace(-ewin,ewin,ne),nk=nk,delta=delta,nrep=nrep)
  execute_script("qh-multildos ")






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
  execute_script("tb90-dos  ")


def pickup_hamiltonian():
  return initialize()
  if builder.get_object("activate_scf").get_active():
    return read_hamiltonian()
  else: # generate from scratch
    return initialize()

  



def show_structure():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
  execute_script("qh-structure-bond --input POSITIONS.OUT")


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
  execute_script("qh-hofstader  HOFSTADER.OUT")




save_results = lambda x: save_outputs(inipath,tmppath) # function to save


# create signals
signals = dict()
#signals["initialize"] = initialize  # initialize and run
signals["show_bands"] = show_bands  # show bandstructure
signals["show_structure"] = show_structure  # show bandstructure
signals["show_dos"] = show_dos  # show DOS
signals["show_dosbands"] = show_dosbands  # show DOS
signals["show_hofstader"] = show_hofstader  # show DOS
signals["show_interactive_ldos"] = show_interactive_ldos  # show DOS






window.connect_clicks(signals,robust=False)
folder = create_folder()
tmppath = os.getcwd() # get the initial directory
window.run()

