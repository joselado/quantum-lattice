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

from interfacetk import latticeterms
latticeterms.connect(qtwrap,lambda: getbox("lattice")) # hide honeycomb-only
                                                         # terms (Haldane,
                                                         # Kane-Mele, valley)
                                                         # for other lattices

# parameters set separately per part (y-slab) of the system, in the same
# order Designer laid out the Upper/Lower (part 1/2) tabs - see
# hybridparts.py. Adding a term here is enough for it to also gain
# per-part fields for part 3+; initialize() below still needs its own
# check()/fint() call to actually use it.
PART_FIELDS = [
  ("fermi","Fermi energy"),
  ("peierls","Magnetic field"),
  ("exchange","Exchange field"),
  ("rashba","Rashba"),
  ("kanemele","Kane-Mele"),
  ("haldane","Haldane"),
  ("antihaldane","Anti-Haldane"),
  ("mAB","Sublattice imbalance"),
  ("mAF","Antiferromagnetism"),
  ("swave","swave pairing"),
]
hybridparts.connect(qtwrap,PART_FIELDS,
    on_new_part=lambda form: latticeterms.apply_term_restrictions(form,form.lattice.currentText()))


def get_geometry():
  """ Create a 0d island"""
  lattice_name = getbox("lattice") # get the option
  n = int(get("width")) # thickness of the system
  lattices = {
    "Chain": geometry.chain,
    "Honeycomb": geometry.honeycomb_lattice,
    "Square": geometry.square_lattice,
    "Kagome": geometry.kagome_lattice,
    "Lieb": geometry.lieb_lattice,
    "Triangular": geometry.triangular_lattice_tripartite,
    "Honeycomb zigzag": lambda: geometry.honeycomb_zigzag_ribbon(n),
    "Honeycomb armchair": lambda: geometry.honeycomb_armchair_ribbon(n),
  }
  g = lattices[lattice_name]()
  if g.dimensionality==2: # original is a 2d geometry
    g = ribbon.bulk2ribbon(g,n=n)
  nsuper = int(get("nsuper"))
  g = g.supercell(nsuper)
  return g





def initialize():
  """ Initialize the calculation"""
  nparts = hybridparts.current_nparts(qtwrap) # how many y-slabs the user picked
  g = get_geometry() # get the geometry
  region_of = hybridparts.region_of_factory(g.y.min(),g.y.max(),nparts) # y -> part index
  def check(name): return hybridparts.part_check(get,name,nparts)
  def fint(name): return hybridparts.part_interpolator(get,name,nparts,1,region_of) # axis 1 = y
  h = g.get_hamiltonian(has_spin=True)
  h.add_zeeman(hybridparts.part_array_interpolator(qtwrap.get_array,"exchange",nparts,1,region_of)) # Zeeman fields
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


def show_ldos():
  """Return the LDOS"""
  h = pickup_hamiltonian() # get hamiltonian
  ewin = abs(get("window_ldos"))
  energies = np.linspace(-ewin,ewin,int(get("ne_ldos")))
  delta = get("delta_ldos")
  ldos.slabldos(h,energies=energies,delta=delta,nk=int(get("nk_ldos")))
  execute_script("ql-ldos-slab DOSMAP.OUT  ")





pickup_hamiltonian = lambda: common.pickup_hamiltonian(qtwrap,initialize,do_scf=True,solve=solve_scf)


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


def show_berry2d():
  h = pickup_hamiltonian() # get hamiltonian
  nk = int(get("nk_topology"))
  topology.berry_map(h,nk=nk)
  execute_script("ql-berry2d BERRY_MAP.OUT")

  

def show_magnetism():
  h = pickup_hamiltonian() # get hamiltonian
  h.get_magnetization() # get the magnetization
  execute_script("ql-magnetism  ")
#  execute_script("ql-magnetism  ")


def show_structure():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  common.write_unit_cell(g) # primitive cell, before the --nsuper repetition
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
#  execute_script("ql-light-structure POSITIONS.OUT")
  execute_script("ql-structure-bond POSITIONS.OUT")
#  execute_script("ql-structure  ")



def show_kdos():
  h = pickup_hamiltonian()  # get the hamiltonian
  ew = get("ewindow_kdos")
  new = int(get("mesh_kdos")) # scale as kpoints
  energies = np.linspace(-ew,ew,new) # number of ene
  klist = np.linspace(0.,1.,new)
  kdos.write_surface_2d(h,energies=energies,delta=ew/new,klist=klist)
  execute_script("ql-kdos-both KDOS.OUT  ")



def show_berry1d():
  h = pickup_hamiltonian()  # get the hamiltonian
  ks = klist.default(h.geometry,nk=int(get("nk_topology")))  # write klist
  topology.write_berry(h,ks)
  execute_script("ql-berry1d  label  ")


def show_z2():
  h = pickup_hamiltonian()  # get the hamiltonian
  nk = get("nk_topology")
  topology.z2_vanderbilt(h,nk=nk,nt=nk/2) # calculate z2 invariant
  execute_script("ql-wannier-center  ") # plot the result


def show_interactive_ldos():
  h = pickup_hamiltonian()  # get the hamiltonian
  ewin = get("window_ldos")
  nrep = int(get("nsuper_ldos"))
  nk = int(get("nk_ldos"))
  ne = int(get("ne_ldos"))
  delta = get("delta_ldos")
  ldos.multi_ldos(h,es=np.linspace(-ewin,ewin,ne),nk=nk,delta=delta,nrep=nrep)
  execute_script("ql-multildos ")




def save_results():  save_state(inipath,tmppath,window) # function to save
def load_results():  load_state(inipath,tmppath,window) # function to load


# create signals
# STANDARD_HANDLERS covers the plain "pickup_hamiltonian + common.get_X"
# buttons automatically; only the buttons with mode-specific behavior
# need to be listed explicitly here
signals = common.wire_standard_signals(qtwrap,pickup_hamiltonian,extra={
  "show_structure": show_structure,  # show bandstructure
  "show_interactive_ldos": show_interactive_ldos,  # show DOS
  "solve_scf": solve_scf,
  "save_results": save_results,
  "load_results": load_results,
})

# set all the formulas
common.set_formulas(qtwrap)


common.initialize(qtwrap) # initialize
qtwrap.set_combobox("dos_operator",operators.operator_list)

window.connect_clicks(signals)
common.set_button_tooltips(qtwrap) # hover tooltips on the calculation buttons
inipath = os.getcwd() # get the initial directory
folder = create_folder()
window.scratch_dir = folder # so qtwrap.connect_clicks() can restore this page's cwd before each handler runs
tmppath = os.getcwd() # get the initial directory
if __name__ == "__main__":
    window.run() # show this page as its own standalone window and block

