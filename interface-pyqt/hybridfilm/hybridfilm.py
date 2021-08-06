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
#  lattice_name = builder.get_object("lattice").get_active_text()
  if lattice_name=="Honeycomb":
    geometry_builder = geometry.honeycomb_lattice
  elif lattice_name=="Square":
    geometry_builder = geometry.square_lattice
  elif lattice_name=="Kagome":
    geometry_builder = geometry.kagome_lattice
  elif lattice_name=="Lieb":
    geometry_builder = geometry.lieb_lattice
  elif lattice_name=="Triangular":
    geometry_builder = geometry.triangular_lattice
  g = geometry_builder() # call the geometry
  nsuper = int(get("nsuper"))
  g = g.supercell(nsuper)
  return g



def get_geometry_film():
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
  return g

get_geometry = get_geometry_film



def get_interpolator(p1,p2):
  """Return the interpolator between the two parameters"""
  def fun(r1,r2=None): # function of the position
    if r2 is not None: r = (r1 + r2)/2.
    else: r = r1
    if r[2]<0.0: return p1
    else: return p2
  return fun # return function




def initialize():
  """ Initialize the calculation"""
  def check(name):
    if abs(get(name))>0.0 or abs(get(name+"_2"))>0.0: return True
    else: return False
  def fint(name): return get_interpolator(get(name),get(name+"_2")) # function
  g = get_geometry() # get the geometry
  if check("strain"): # custom function
    dfun = fint("strain") # get function
    def fun(r1,r2): # function to compute distance
      dr = r1-r2
      dr2 = dr.dot(dr) # distance
      if 0.9<dr2<1.1: 
        if 0.9<abs(dr[2])<1.1: return 1.0 + dfun(r1,r2) # first neighbor
        return 1.0
      else: return 0.0
    h = g.get_hamiltonian(fun) # get the Hamiltonian
  else:
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
  execute_script('qh-map2d --input DOSMAP.OUT --xlabel Energy --ylabel "z-position" --zlabel DOS --title "Local DOS"')






def show_dosbands():
  h = pickup_hamiltonian() # get hamiltonian
  kdos.kdos_bands(h,scale=get("scale_kbands"),ewindow=get("window_kbands"),
                   ne=int(get("ne_kbands")),delta=get("delta_kbands"),
                   ntries=int(get("nv_kbands")))
  execute_script("qh-dosbands  KDOS_BANDS.OUT ")



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
  g.write_profile(np.sign(g.z),name="PROFILE.OUT",normal_order=True,nrep=1)
  execute_script("qh-structure --input PROFILE.OUT --color True")
#  execute_script("qh-structure  ")


def show_structure_3d():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
  execute_script("qh-structure-tbg POSITIONS.OUT")



def show_kdos():
  h = pickup_hamiltonian()  # get the hamiltonian
  common.get_kdos(h,qtwrap) # get the KDOS



def show_berry1d():
  h = pickup_hamiltonian()  # get the hamiltonian
  common.get_berry1d(h,qtwrap)



def show_z2():
  h = pickup_hamiltonian()  # get the hamiltonian
  common.get_z2(h,qtwrap)




save_results = lambda x: save_outputs(inipath,tmppath) # function to save


# create signals
signals = dict()
#signals["initialize"] = initialize  # initialize and run
signals["show_bands"] = show_bands  # show bandstructure
signals["show_structure"] = show_structure  # show bandstructure
signals["show_structure_3d"] = show_structure_3d  # show bandstructure
signals["show_dos"] = show_dos  # show DOS
signals["show_berry2d"] = show_berry2d  # show DOS
signals["show_berry1d"] = show_berry1d  # show DOS
signals["show_kdos"] = show_kdos  # show DOS
signals["show_dosbands"] = show_dosbands  # show DOS
signals["show_z2"] = show_z2  # show DOS
signals["show_ldos"] = show_ldos  # show DOS
#signals["show_stm"] = show_stm  # show STM
#signals["show_magnetism"] = show_magnetism  # show magnetism
#signals["show_lattice"] = show_lattice  # show magnetism
#signals["save_results"] = save_results  # save the results






window.connect_clicks(signals)
folder = create_folder()
tmppath = os.getcwd() # get the initial directory
window.run()

