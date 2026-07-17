#!/usr/bin/env python3

import sys
import os


# Add path of the wrapper
# main path
qlroot = os.path.dirname(os.path.realpath(__file__))+"/../.."
sys.path.append(qlroot+"/pysrc/") # python libraries

from interfacetk import qtwrap # import the library with simple wrappaers to qt4
get = qtwrap.get  # get the value of a certain variable
is_checked = qtwrap.is_checked  # get the value of a certain variable
window = qtwrap.main() # this is the main interface


from interfacetk.qh_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries
common.initialize(qtwrap) # do several common initializations

from pyqula import parallel

from interfacetk import interfacetk
modify_geometry = lambda x: interfacetk.modify_geometry(x,qtwrap)
select_atoms_removal = lambda: common.select_atoms_removal(get_geometry,script="ql-remove-atoms-geometry-3d")
pickup_hamiltonian = lambda: common.pickup_hamiltonian(qtwrap,initialize)

qtwrap.set_combobox("multilayer_type",
        cs=["Twisted bilayer",
            "Aligned bilayer AA",
            "Aligned bilayer AB",
            "Aligned trilayer ABC",
            "Twisted trilayer 010",
            "Twisted trilayer 001"
            ,"Twisted tetralayer 0101"
            ,"Twisted bi-bilayer AB AB"
            ,"Twisted bi-bilayer AB BA"
            ,"Twisted bi-trilayer ABC"
            ])

def get_geometry(modify=True):
  """ Create a 2d honeycomb lattice"""
  n = int(qtwrap.get("cell_size")) # size of the unit cell
  name = qtwrap.getbox("multilayer_type")
  def _aligned_bilayer_ab():
    gb = specialgeometry.multilayer_graphene(l=[0,1])
    return specialgeometry.twisted_multilayer(n,rot=[0],g=gb,dz=6.0)
  def _aligned_trilayer_abc():
    gb = specialgeometry.multilayer_graphene(l=[0,1,2])
    return specialgeometry.twisted_multilayer(n,rot=[0],g=gb,dz=6.0)
  lattices = {
    "Twisted bilayer": lambda: specialgeometry.twisted_multilayer(n,rot=[0,1]),
    "Aligned bilayer AA": lambda: specialgeometry.twisted_multilayer(n,rot=[0,0]),
    "Aligned bilayer AB": _aligned_bilayer_ab,
    "Aligned trilayer ABC": _aligned_trilayer_abc,
    "Twisted trilayer 010": lambda: specialgeometry.twisted_multilayer(n,rot=[0,1,0]),
    "Twisted tetralayer 0101": lambda: specialgeometry.twisted_multilayer(n,rot=[0,1,0,1]),
    "Twisted trilayer 001": lambda: specialgeometry.twisted_multilayer(n,rot=[0,0,1]),
    "Twisted bi-bilayer AB AB": lambda: specialgeometry.parse_twisted_multimultilayer([["AB","AB"],[0,1]],n=n),
    "Twisted bi-bilayer AB BA": lambda: specialgeometry.parse_twisted_multimultilayer([["AB","BA"],[0,1]],n=n),
    "Twisted bi-trilayer ABC": lambda: specialgeometry.parse_twisted_multimultilayer([["ABC","ABC"],[0,1]],n=n),
  }
  g = lattices[name]()
  if modify: g = modify_geometry(g) # remove atoms if necessary
  return g



def initialize():
  """ Initialize the calculation"""
  g = get_geometry() # get the geometry
  twisted_matrix = specialhopping.twisted_matrix
  has_spin = False
  h = g.get_hamiltonian(is_sparse=True,has_spin=has_spin,is_multicell=True,
     mgenerator=twisted_matrix(ti=get("tinter"),lambi=7.0))
  # workaround to put Fermi energy in zero approx
  h.shift_fermi(-get("tinter")/16.) 
  h.add_crystal_field(qtwrap.get("crystalfield")) 
  if abs(get("inplaneb"))>0.0:
      h.add_inplane_bfield(b=get("inplaneb"),phi=get("inplaneb_phi"))
#  mu,ml = get("mAB_upper"),get("mAB_lower") # get the masses
#  h.add_sublattice_imbalance(lambda r: mu*(r[2]>0.))  # upper mass
#  h.add_sublattice_imbalance(lambda r: ml*(r[2]<0.))  # lower mass
  efield = get("interlayer_bias")
  h.add_onsite(lambda r: r[2]*efield)
  if h.has_spin:
    h.add_zeeman([get("Bx"),get("By"),get("Bz")]) # Zeeman fields
    h.add_rashba(get("rashba"))  # Rashba field
    h.add_antiferromagnetism(get("mAF"))  # AF order
    h.add_kane_mele(get("kanemele")) # intrinsic SOC
  h.shift_fermi(get("fermi")) # shift fermi energy
  if is_checked("set_half_filling"): h.set_filling(.5,nk=2)
  klist.default(g,nk=int(get("nkpoints")))  # write klist
  return h



def check_parallel():
  """Check if there is parallelization"""
  if qtwrap.getbox("use_parallelization") =="Yes":
      parallel.cores = parallel.maxcpu
  else: parallel.cores = 1 # single core




  

def show_dos():
  comp = computing() # create the computing window
  h = pickup_hamiltonian()  # get the hamiltonian
  nk = int(round(np.sqrt(get("nk_dos"))))
  ndos = int(get("nume_dos"))
  npol = int(get("numpol_dos"))
  ndos = npol*10
  delta = get("delta_dos")
  scale = 10.0 # scale for KPM
  check_parallel() # check if there is parallelization
  name = qtwrap.getbox("mode_dos") # mode of the DOS
  if name=="KPM":
    dos.dos(h,use_kpm=True,nk=nk,ntries=1,scale=scale,delta=5*delta,
            energies=np.linspace(-5.0,5.0,int(20./delta)))
  elif name=="Lowest":
    numw = int(get("numw_dos")) # number of waves
    energies = None
    dos.dos2d(h,nk=nk,delta=delta,numw=numw)
  else: raise
  execute_script("ql-dos --input DOS.OUT ")
  comp.kill()
  return




def show_structure():
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct")) 
  g = g.supercell(nsuper) # build a supercell
  g.write()
  execute_script("ql-potential --input POSITIONS.OUT --colorbar false --cmap rainbow --zoom 70 --size 30")










def show_ldos():
  h = pickup_hamiltonian()  # get the hamiltonian
#  if h.intra.shape[0]<2000: h.turn_dense()
  e = get("energy_ldos_single")
  delta = get("delta_ldos_single")
  nk = get("nk_ldos_single")
  nk = int(round(np.sqrt(nk)))
  nsuper = int(get("nsuper_ldos_single"))
  ldos.ldos(h,e=e,delta=delta,nk=nk,mode="arpack",nrep=nsuper)
  execute_script("ql-fast-ldos LDOS.OUT  ")



def show_z2_invariant():
  h = pickup_hamiltonian()  # get the hamiltonian
  nk = get("nkpoints")/4
  topology.z2_vanderbilt(h,nk=nk,nt=nk/2) # calculate z2 invariant
  execute_script("ql-wannier-center  ") # plot the result




def show_kdos():
  h = pickup_hamiltonian()  # get the hamiltonian
  ew = get("e_kdos")
  new = int(get("nkpoints")/10) # scale as kpoints
  energies = np.linspace(-ew,ew,new) # number of ene
  klist = np.linspace(0.,1.,new)
  kdos.write_surface_2d(h,energies=energies,delta=ew/new,klist=klist)
  execute_script("ql-kdos KDOS.OUT  ")


def show_2dband():
  h = pickup_hamiltonian()  # get the hamiltonian
  nk = get("nkpoints")/4
  ns = get_text("num_2dband") # get indexes of the bands
  if "," in ns: ns = [int(n) for n in ns.split(",")] # get the different numbers
  else: ns=[int(ns)] # single one
  if 0 in ns: # in case all eigenvalues wanted
    ns = [i+1 for i in range(h.intra.shape[0]//2)]
    ns += [-i for i in ns]
  spectrum.get_bands(h,nindex=ns,nk=nk,reciprocal=True)
  string = ""
  for n in ns: string += "BANDS2D__"+str(n)+".OUT "
  execute_script("ql-plot3d "+string +"  ")










def show_structure_3d():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
#  execute_script("ql-structure3d POSITIONS.OUT")
#  execute_script("ql-magnetism nomag nobonds POSITIONS.OUT")
  execute_script("ql-structure-tbg ")




def save_results():  save_state(inipath,tmppath,window) # function to save
def load_results():  load_state(inipath,tmppath,window) # function to load

# create signals: STANDARD_HANDLERS covers the plain "pickup_hamiltonian
# + common.get_X" buttons automatically; only the buttons with mode-specific
# behavior need to be listed explicitly here
signals = common.wire_standard_signals(qtwrap,pickup_hamiltonian,extra={
  "show_dos": show_dos,  # custom KPM/Lowest DOS modes
  "show_ldos_single": show_ldos,  # show Berry curvature
  "show_structure": show_structure,  # show magnetism
  "show_structure_3d": show_structure_3d,
  "select_atoms_removal": select_atoms_removal,
  "save_results": save_results,
  "load_results": load_results,
})


window.connect_clicks(signals,robust=False)
inipath = os.getcwd() # get the initial directory
folder = create_folder()
tmppath = os.getcwd() # get the initial directory
window.run()

