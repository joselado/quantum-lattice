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
window = qtwrap.new_page(os.path.dirname(os.path.realpath(__file__))) # this mode's page


from interfacetk.qh_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries
common.initialize(qtwrap) # do several common initializations

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
  """Delegates to the shell-wide serial/parallel switch (see
  common.check_parallel) - superseded by the shell's single nav-panel
  switch, no longer this mode's own "Parallelization" combo box."""
  common.check_parallel(qtwrap)




  

def show_dos():
  h = pickup_hamiltonian()  # get the hamiltonian
  nk = int(round(np.sqrt(get("nk_dos"))))
  ndos = int(get("nume_dos"))
  npol = int(get("numpol_dos"))
  ndos = npol*10
  delta = get("delta_dos") or 1e-3 # avoid a division by zero below
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
  return




def show_structure():
  common.show_structure(qtwrap,get_geometry,
      script="ql-potential --input POSITIONS.OUT --colorbar false --cmap rainbow --zoom 70 --size 30")










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


def show_structure_3d():
  """Show the lattice of the system"""
  common.show_structure_3d(qtwrap,get_geometry,script="ql-structure-tbg ")




# create signals: STANDARD_HANDLERS covers the plain "pickup_hamiltonian
# + common.get_X" buttons automatically; only the buttons with mode-specific
# behavior need to be listed explicitly here (save_results/load_results are
# wired automatically by common.finalize_page())
signals = common.wire_standard_signals(qtwrap,pickup_hamiltonian,extra={
  "show_dos": show_dos,  # custom KPM/Lowest DOS modes
  "show_site_dos": lambda: common.get_site_dos(pickup_hamiltonian(),qtwrap,use_kpm=True), # moire cells are too large for ED
  "show_ldos_single": show_ldos,  # interactive single-energy LDOS map
  "show_structure": show_structure,  # potential-colored structure plot
  "show_structure_3d": show_structure_3d,
  "select_atoms_removal": select_atoms_removal,
})

inipath = os.getcwd() # get the initial directory, before common.finalize_page()'s create_folder() chdirs away
common.finalize_page(qtwrap,window,signals,inipath,robust=False)

if __name__ == "__main__":
    window.run() # show this page as its own standalone window and block

