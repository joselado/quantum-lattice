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
from interfacetk import hamiltoniantype
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
    on_new_part=lambda form: latticeterms.apply_term_restrictions(
        form,form.lattice.currentText(),hamiltoniantype.get_type(form)))


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
  has_spin = hamiltoniantype.wants_spin(qtwrap)
  if check("strain"): # custom function
    dfun = fint("strain") # get function
    def fun(r1,r2): # function to compute distance
      dr = r1-r2
      dr2 = dr.dot(dr) # distance
      if 0.9<dr2<1.1:
        if 0.9<abs(dr[2])<1.1: return 1.0 + dfun(r1,r2) # first neighbor
        return 1.0
      else: return 0.0
    h = g.get_hamiltonian(tij=fun,has_spin=has_spin) # get the Hamiltonian
  else:
    h = g.get_hamiltonian(has_spin=has_spin)
  if has_spin: # see hamiltoniantype.py's docstring - these unconditionally
    # call turn_spinful() themselves, so they must be skipped outright for
    # "Spinless" rather than called with a zero-ish value
    h.add_zeeman(hybridparts.part_array_interpolator(qtwrap.get_array,"exchange",nparts,2,region_of)) # Zeeman fields
    if check("rashba"): h.add_rashba(fint("rashba"))  # Rashba field
    h.add_antiferromagnetism(fint("mAF"))  # AF order
    if check("kanemele"):  h.add_kane_mele(fint("kanemele")) # intrinsic SOC
  h.add_sublattice_imbalance(fint("mAB"))  # sublattice imbalance
  h.shift_fermi(fint("fermi")) # shift fermi energy
  if check("haldane"):  h.add_haldane(fint("haldane")) # intrinsic SOC
  if check("antihaldane"):  h.add_antihaldane(fint("antihaldane"))
  if hamiltoniantype.wants_nambu(qtwrap):
      h.setup_nambu_spinor() # establish the BdG structure even if swave is left at zero
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
    dos.dos0d(h,es=np.linspace(-3.1,3.1,500),delta=get("dos_delta"))
  elif h.dimensionality==1:
    # dos.dos1d() hits a numba typing error inside pyqula's
    # calculate_dos_hkgen (int dtype k-point); use the same dos.dos()
    # dispatcher the other modes' "show_dos" already relies on instead
    dos.dos(h,delta=get("dos_delta"),energies=np.linspace(-3.1,3.1,500))
  elif h.dimensionality==2:
    # dos.dos2d() hits a numba typing error inside pyqula's
    # calculate_dos_hkgen (int dtype k-point); use the same dos.dos()
    # dispatcher the other modes' "show_dos" already relies on instead
    dos.dos(h,delta=get("dos_delta"),energies=np.linspace(-3.1,3.1,500))
  else: raise
  execute_script("ql-dos  ")


pickup_hamiltonian = lambda: common.pickup_hamiltonian(qtwrap,initialize,do_scf=True,solve=solve_scf)


def solve_scf():
  """Perform a selfconsistent calculation"""
  h = initialize()
  common.solve_scf(h,qtwrap)


def show_structure():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  common.write_unit_cell(g) # primitive cell, before the --nsuper repetition
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
  g.write_profile(np.sign(g.z),name="PROFILE.OUT",normal_order=True,nrep=1)
  execute_script("ql-structure --input PROFILE.OUT --color True")
#  execute_script("ql-structure  ")


def show_structure_3d():
  """Show the lattice of the system"""
  common.show_structure_3d(qtwrap,get_geometry,script="ql-structure-tbg POSITIONS.OUT")



# create signals: STANDARD_HANDLERS covers the plain "pickup_hamiltonian
# + common.get_X" buttons automatically; only the buttons with mode-specific
# behavior need to be listed explicitly here (save_results/load_results are
# wired automatically by common.finalize_page())
signals = common.wire_standard_signals(qtwrap,pickup_hamiltonian,extra={
  "show_structure": show_structure,  # show bandstructure
  "show_structure_3d": show_structure_3d,  # show bandstructure
  "show_dos": show_dos,  # custom dimensionality-dependent DOS
  "show_ldos": show_ldos,  # show DOS
  "solve_scf": solve_scf,
})

inipath = os.getcwd() # get the initial directory, before common.finalize_page()'s create_folder() chdirs away
common.finalize_page(qtwrap,window,signals,inipath)

if __name__ == "__main__":
    window.run() # show this page as its own standalone window and block

