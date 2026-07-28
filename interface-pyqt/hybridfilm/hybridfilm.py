#!/usr/bin/env python3

from __future__ import print_function

import sys
import os

# main path
qlroot = os.path.dirname(os.path.realpath(__file__))+"/../.."
sys.path.append(qlroot+"/pysrc/") # python libraries


from interfacetk import qtwrap # import the library with simple wrappaers to qt4
get = qtwrap.get  # get the value of a certain variable
getbox = qtwrap.getbox  # get the value of a certain variable
window = qtwrap.new_page(os.path.dirname(os.path.realpath(__file__))) # this mode's page

from interfacetk import scfterms
# grid= differs from the default "gridLayout_10" because that name is
# already taken by an unrelated layout in this mode's interface.ui - see
# INTERFACE_GUIDE.md's "Adding a mode" checklist
scfterms.build(qtwrap,grid="gridLayout_scf_10") # build the Density-density/Spin-spin mean field tabs



from interfacetk.qh_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries
from interfacetk import hybridparts # per-part (Upper/Lower/...) parameter widgets





LATTICES = {
  "Cubic": geometry.cubic_lattice,
  "Diamond": geometry.diamond_lattice_minimal,
  "Pyrochlore": geometry.pyrochlore_lattice,
  "Hyperhoneycomb": geometry.hyperhoneycomb_lattice,
}

from interfacetk import latticeterms
latticeterms.connect(qtwrap,lambda: getbox("lattice")) # hide honeycomb-only
                                                         # terms (Haldane,
                                                         # Kane-Mele, valley)
                                                         # for other lattices

# parameters set separately per part (z-slab) of the system, in the same
# order Designer laid out the Upper/Lower (part 1/2) tabs - see
# hybridparts.py. Adding a term here is enough for it to also gain
# per-part fields for part 3+; initialize() below still needs its own
# check()/fint() call to actually use it.
PART_FIELDS = [
  ("strain","Strain"),
  ("fermi","Fermi energy"),
  ("Bx","Zeeman Jx"),
  ("By","Zeeman Jy"),
  ("Bz","Zeeman Jz"),
  ("rashba","Rashba"),
  ("kanemele","Kane-Mele"),
  ("haldane","Haldane"),
  ("antihaldane","Anti-Haldane"),
  ("mAB","Sublattice imbalance"),
  ("mAF","Antiferromagnetism"),
  ("swave","swave pairing"),
]
hybridparts.connect(qtwrap,PART_FIELDS,
    on_new_part=lambda: latticeterms.apply_term_restrictions(qtwrap.form,getbox("lattice")))


def get_geometry():
  """ Create a 0d island"""
  lattice_name = getbox("lattice") # get the option
  g = LATTICES[lattice_name]() # call the geometry
  g = films.geometry_film(g,int(get("thickness")))
  g = g.supercell(int(get("nsuper")))
  g.real2fractional()
  g.fractional2real()
  g.center()
  return g



def initialize():
  """ Initialize the calculation"""
  nparts = hybridparts.current_nparts(qtwrap) # how many z-slabs the user picked
  g = get_geometry() # get the geometry
  region_of = hybridparts.region_of_factory(g.z.min(),g.z.max(),nparts) # z -> part index
  def check(name): return hybridparts.part_check(get,name,nparts)
  def fint(name): return hybridparts.part_interpolator(get,name,nparts,2,region_of) # axis 2 = z
  if check("strain"): # custom function
    dfun = fint("strain") # get function
    def fun(r1,r2): # function to compute distance
      dr = r1-r2
      dr2 = dr.dot(dr) # distance
      if 0.9<dr2<1.1:
        if 0.9<abs(dr[2])<1.1: return 1.0 + dfun(r1,r2) # first neighbor
        return 1.0
      else: return 0.0
    h = g.get_hamiltonian(fun=fun) # get the Hamiltonian
  else:
    h = g.get_hamiltonian(has_spin=True)
  h.add_zeeman(hybridparts.part_vector_interpolator(get,["Bx","By","Bz"],nparts,2,region_of)) # Zeeman fields
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


def show_ldos():
  """Return the LDOS"""
  h = pickup_hamiltonian() # get hamiltonian
  ewin = abs(get("window_ldos"))
  energies = np.linspace(-ewin,ewin,int(get("ne_ldos")))
  delta = get("delta_ldos")
  ldos.slabldos(h,energies=energies,delta=delta,nk=int(get("nk_ldos")))
  execute_script('ql-map2d --input DOSMAP.OUT --xlabel Energy --ylabel "z-position" --zlabel DOS --title "Local DOS"')




def show_dos():
  h = pickup_hamiltonian() # get hamiltonian
#  mode = getbox("mode_dos") # mode for the DOS
  if h.dimensionality==0:
    dos.dos0d(h,es=np.linspace(-3.1,3.1,500),delta=get("DOS_smearing"))
  elif h.dimensionality==1:
#    dos.dos1d(h,ndos=400,delta=get("DOS_smearing"))
    dos.dos1d(h,ndos=400)
  elif h.dimensionality==2:
    # dos.dos2d() hits a numba typing error inside pyqula's
    # calculate_dos_hkgen (int dtype k-point); use the same dos.dos()
    # dispatcher the other modes' "show_dos" already relies on instead
    dos.dos(h,delta=get("DOS_smearing"),energies=np.linspace(-3.1,3.1,500))
  else: raise
  execute_script("ql-dos  ")


pickup_hamiltonian = lambda: common.pickup_hamiltonian(qtwrap,initialize,do_scf=True)


def solve_scf():
  """Perform a selfconsistent calculation"""
  h = initialize()
  common.solve_scf(h,qtwrap)










def show_stm():
  h = pickup_hamiltonian() # get hamiltonian
#  ldos.multi_ldos()
  ewin = abs(get("window_ldos")) # energy window
  ne = int(get("num_ldos")) # number of LDOS
  delta = ewin/ne # delta
  ldos.multi_ldos(h,es=np.linspace(-ewin,ewin,ne),nk=1,delta=delta)
  execute_script("ql-multildos ")
#  hamiltonians.ldos(h,e=get("stm_bias"),delta=get("DOS_smearing")) # calculate the stm spectra
#  print("Using semaring",get("DOS_smearing"))
#  execute_script("ql-ldos  LDOS.OUT")
  return


def show_magnetism():
  h = pickup_hamiltonian() # get hamiltonian
  h.get_magnetization() # get the magnetization
  execute_script("ql-magnetism  ")
#  execute_script("ql-magnetism  ")


def show_structure():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
  g.write_profile(np.sign(g.z),name="PROFILE.OUT",normal_order=True,nrep=1)
  execute_script("ql-structure --input PROFILE.OUT --color True")
#  execute_script("ql-structure  ")


def show_structure_3d():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
  execute_script("ql-structure-tbg POSITIONS.OUT")



def save_results():  save_state(inipath,tmppath,window) # function to save
def load_results():  load_state(inipath,tmppath,window) # function to load


# create signals: STANDARD_HANDLERS covers the plain "pickup_hamiltonian
# + common.get_X" buttons automatically; only the buttons with mode-specific
# behavior need to be listed explicitly here
signals = common.wire_standard_signals(qtwrap,pickup_hamiltonian,extra={
  "show_structure": show_structure,  # show bandstructure
  "show_structure_3d": show_structure_3d,  # show bandstructure
  "show_dos": show_dos,  # custom dimensionality-dependent DOS
  "show_ldos": show_ldos,  # show DOS
  "solve_scf": solve_scf,
  "save_results": save_results,
  "load_results": load_results,
})

# set all the formulas
common.set_formulas(qtwrap)



window.connect_clicks(signals)
inipath = os.getcwd() # get the initial directory
folder = create_folder()
window.scratch_dir = folder # so qtwrap.connect_clicks() can restore this page's cwd before each handler runs
tmppath = os.getcwd() # get the initial directory
if __name__ == "__main__":
    window.run() # show this page as its own standalone window and block

