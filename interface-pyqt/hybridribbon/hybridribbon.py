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





def get_geometry():
  """ Create a 0d island"""
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
    g = geometry.triangular_lattice_tripartite()
  elif lattice_name=="Honeycomb zigzag":
    g = geometry.honeycomb_zigzag_ribbon(n)
  elif lattice_name=="Honeycomb armchair":
    g = geometry.honeycomb_armchair_ribbon(n)
  if g.dimensionality==2: # original is a 2d geometry
    g = ribbon.bulk2ribbon(g,n=n)
  nsuper = int(get("nsuper"))
  g = g.supercell(nsuper)
  return g





def get_interpolator(p1,p2):
  """Return the interpolator between the two parameters"""
  def fun(r1,r2=None): # function of the position
    if r2 is not None: r = (r1 + r2)/2.
    else: r = r1
    if r[1]<0.0: return p1
    else: return p2
  return fun # return function




def initialize():
  """ Initialize the calculation"""
  def check(name):
    if abs(get(name))>0.0 or abs(get(name+"_2"))>0.0: return True
    else: return False
  def fint(name): return get_interpolator(get(name),get(name+"_2")) # function
  g = get_geometry() # get the geometry
  h = g.get_hamiltonian(has_spin=True)
  j1 = np.array([get("Bx"),get("By"),get("Bz")])
  j2 = np.array([get("Bx_2"),get("By_2"),get("Bz_2")])
  h.add_zeeman(get_interpolator(j1,j2)) # Zeeman fields
  h.add_sublattice_imbalance(fint("mAB"))  # sublattice imbalance
  if check("rashba"): h.add_rashba(fint("rashba"))  # Rashba field
  h.add_antiferromagnetism(fint("mAF"))  # AF order
  h.shift_fermi(fint("fermi")) # shift fermi energy
  if check("kanemele"):  h.add_kane_mele(fint("kanemele")) # intrinsic SOC
  if check("haldane"):  h.add_haldane(fint("haldane")) # intrinsic SOC
  if check("antihaldane"):  h.add_antihaldane(fint("antihaldane")) 
  if check("peierls"):  h.add_peierls(fint("peierls")) 
  if check("swave"):  h.add_swave(fint("swave")) 
#  h.add_peierls(get("peierls")) # shift fermi energy
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
  execute_script("qh-dosbands1d  KDOS_BANDS.OUT ")



def show_dos():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_dos(h,qtwrap) # compute DOS


def pickup_hamiltonian():
  return initialize()
  if builder.get_object("activate_scf").get_active():
    return read_hamiltonian()
  else: # generate from scratch
    return initialize()










def show_stm():
  h = pickup_hamiltonian() # get hamiltonian
#  ldos.multi_ldos()
  ewin = abs(get("window_ldos")) # energy window
  ne = int(get("num_ldos")) # number of LDOS
  delta = ewin/ne # delta
  ldos.multi_ldos(h,es=np.linspace(-ewin,ewin,ne),nk=1,delta=delta)
  execute_script("qh-multildos ")
#  hamiltonians.ldos(h,e=get("stm_bias"),delta=get("DOS_smearing")) # calculate the stm spectra
#  print("Using semaring",get("DOS_smearing"))
#  execute_script("qh-ldos  LDOS.OUT")
  return


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
#  execute_script("qh-light-structure POSITIONS.OUT")
  execute_script("qh-structure-bond POSITIONS.OUT")
#  execute_script("qh-structure  ")



def show_kdos():
  h = pickup_hamiltonian()  # get the hamiltonian
  ew = get("ewindow_kdos")
  new = int(get("mesh_kdos")) # scale as kpoints
  energies = np.linspace(-ew,ew,new) # number of ene
  klist = np.linspace(0.,1.,new)
  kdos.write_surface_2d(h,energies=energies,delta=ew/new,klist=klist)
  execute_script("qh-kdos-both KDOS.OUT  ")



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


def show_interactive_ldos():
  h = pickup_hamiltonian()  # get the hamiltonian
  ewin = get("window_ldos")
  nrep = int(get("nsuper_ldos"))
  nk = int(get("nk_ldos"))
  ne = int(get("ne_ldos"))
  delta = get("delta_ldos")
  ldos.multi_ldos(h,es=np.linspace(-ewin,ewin,ne),nk=nk,delta=delta,nrep=nrep)
  execute_script("qh-multildos ")




save_results = lambda x: save_outputs(inipath,tmppath) # function to save


# create signals
signals = dict()
#signals["initialize"] = initialize  # initialize and run
signals["show_bands"] = show_bands  # show bandstructure
signals["show_structure"] = show_structure  # show bandstructure
signals["show_dos"] = show_dos  # show DOS
signals["show_dosbands"] = show_dosbands  # show DOS
signals["show_interactive_ldos"] = show_interactive_ldos  # show DOS




common.initialize(qtwrap) # initialize

window.connect_clicks(signals)
folder = create_folder()
tmppath = os.getcwd() # get the initial directory
window.run()

