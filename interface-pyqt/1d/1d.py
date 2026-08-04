#!/usr/bin/env python3

from __future__ import print_function

import sys
import os

# main path
qlroot = os.path.dirname(os.path.realpath(__file__))+"/../.."
sys.path.append(qlroot+"/pysrc/") # python libraries
moddir = os.path.dirname(os.path.realpath(__file__)) # this mode's own
    # directory, for run_calculation_subprocess() to find its calc.py


from interfacetk import qtwrap # import the library with simple wrappaers to qt4
get = qtwrap.get  # get the value of a certain variable
getbox = qtwrap.getbox  # get the value of a certain variable
window = qtwrap.new_page(os.path.dirname(os.path.realpath(__file__))) # this mode's page

from interfacetk import scfterms
scfterms.build(qtwrap) # build the Density-density/Spin-spin mean field tabs

from interfacetk import codeview

from interfacetk.ql_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries
common.initialize(qtwrap) # do several common initializations
qtwrap.set_combobox("dos_operator",operators.operator_list)

from interfacetk import interfacetk
modify_geometry = lambda x: interfacetk.modify_geometry(x,qtwrap)

import calc # this mode's own geometry/Hamiltonian-building code, kept
            # importable on its own (no page/QApplication side effects) so
            # run_calculation.py's child process can reuse it - see calc.py
get_geometry = calc.get_geometry
initialize = calc.initialize

select_atoms_removal = lambda: common.select_atoms_removal(get_geometry)
pickup_hamiltonian = lambda: common.pickup_hamiltonian(qtwrap,initialize,do_scf=True,solve=solve_scf)

from interfacetk import hamiltoniantype
from interfacetk import latticeterms
latticeterms.connect(qtwrap,lambda: getbox("lattice")) # hide honeycomb-only
                                                         # terms (Haldane,
                                                         # Kane-Mele, valley)
                                                         # for other lattices








_LATTICE_CALLS = {
  "Chain": "geometry.chain()",
  "Bichain": "geometry.bichain()",
  "Honeycomb": "geometry.honeycomb_lattice()",
  "Square": "geometry.square_lattice()",
  "Kagome": "geometry.kagome_lattice()",
  "Lieb": "geometry.lieb_lattice()",
  "Triangular": "geometry.triangular_lattice_tripartite()",
  "Honeycomb zigzag": "geometry.honeycomb_zigzag_ribbon(%s)",
  "Honeycomb armchair": "geometry.honeycomb_armchair_ribbon(%s)",
}
# lattice names whose constructor builds a 2D bulk geometry that
# get_geometry() then cuts into a ribbon (g.dimensionality==2 check) -
# hardcoded here since it only depends on lattice_name, not on any UI
# value, so it can be decided at code-generation time the same way
# get_geometry()'s runtime check would resolve for that same name
_NEEDS_RIBBON = {"Honeycomb","Square","Kagome","Lieb","Triangular"}


def get_pyqula_code():
  """Return the pyqula script that reproduces the Hamiltonian this page's
  form fields currently describe (mirrors get_geometry()/initialize()
  above) - only non-default (active) terms are included, see
  codeview.is_active(). Atoms removed manually in the "Modify geometry"
  tab are not reproduced, since that depends on a saved selection file
  rather than a term value."""
  fv = lambda name: codeview.format_value(qtwrap,name)
  fa = lambda name: codeview.format_array(qtwrap,name)
  active = lambda name: codeview.is_active(qtwrap,name)

  lattice_name = getbox("lattice")
  width = str(int(get("ribbon_width"))) # matches get_geometry()'s own int(get("ribbon_width"))
  nsuper = str(int(get("nsuper"))) # matches get_geometry()'s int(get("nsuper"))
  lattice_call = _LATTICE_CALLS[lattice_name]
  if "%s" in lattice_call: lattice_call = lattice_call % width
  has_spin = hamiltoniantype.wants_spin(qtwrap)

  lines = [
    "from pyqula import geometry, ribbon",
    "",
    "g = %s" % lattice_call,
  ]
  if lattice_name in _NEEDS_RIBBON:
    lines.append("g = ribbon.bulk2ribbon(g, n=%s)" % width)
  lines.append("g = g.supercell(%s, store_primal=True)" % nsuper)
  lines += codeview.geometry_removal_code(qtwrap)
  lines.append("")
  lines.append("h = g.get_hamiltonian(has_spin=%r, tij=%s)" % (has_spin,fa("hoppings")))
  lines.append("h.turn_multicell()")
  if active("exchange"): lines.append("h.add_zeeman(%s)" % fa("exchange"))
  if active("mAB"): lines.append("h.add_sublattice_imbalance(%s)" % fv("mAB"))
  if active("rashba"): lines.append("h.add_rashba(%s)" % fv("rashba"))
  if active("mAF"): lines.append("h.add_antiferromagnetism(%s)" % fv("mAF"))
  if active("crystalfield"): lines.append("h.add_crystal_field(%s)" % fv("crystalfield"))
  if active("fermi"): lines.append("h.shift_fermi(%s)" % fv("fermi"))
  if active("kanemele"): lines.append("h.add_kane_mele(%s)" % fv("kanemele"))
  if active("haldane"): lines.append("h.add_haldane(%s)" % fv("haldane"))
  if active("antihaldane"): lines.append("h.add_antihaldane(%s)" % fv("antihaldane"))
  if active("antikanemele"): lines.append("h.add_anti_kane_mele(%s)" % fv("antikanemele"))
  if active("peierls"): lines.append("h.add_peierls(%s)" % fv("peierls"))
  if hamiltoniantype.wants_nambu(qtwrap): lines.append("h.setup_nambu_spinor()")
  if active("swave"): lines.append("h.add_swave(%s)" % fv("swave"))
  if active("pwave"): lines.append("h.add_pairing(d=%s, mode=\"triplet\", delta=1.0)" % fa("pwave"))

  if qtwrap.is_checked("do_scf"):
    lines += common.pyqula_code_scf_block(qtwrap,richer=False)

  return "\n".join(lines)


def show_edge_dos():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_surface_dos(h,qtwrap) # wrapper


def show_band_ldos():
  """Open the interactive Band LDOS view: a band structure subplot on
  the left (click a point) and the spatial density of that eigenstate
  on the right, recomputed on every click - see utilities/ql-band-ldos.
  The Hamiltonian has to be handed off (pickled) rather than a
  precomputed BANDS.OUT, since the eigenstate itself is only computed
  in response to the pick_event in that subprocess."""
  h = pickup_hamiltonian() # get the Hamiltonian
  hfile = "BAND_LDOS_HAMILTONIAN.pkl" # not hamiltonian.pkl - see get_site_dos
  h.save(hfile)
  nk = max([int(qtwrap.get("band_ldos_nk")),1])
  execute_script("ql-band-ldos --hamiltonian "+hfile+" --nk "+str(nk))




def show_magnetism():
  """Show the magnetism of the system"""
  h = pickup_hamiltonian() # get the Hamiltonian
  common.show_exchange(h,qtwrap)


def show_ldos():
  h = pickup_hamiltonian() # get the Hamiltonian
  ew = abs(qtwrap.get("ldos_ewindow"))
  energies = np.linspace(-ew,ew,100)
  delta = qtwrap.get("ldos_delta")
  nk = int(qtwrap.get("ldos_nk"))
  name = qtwrap.getbox("ldos_operator")
  ldos.spatial_energy_profile(h,operator=h.get_operator(name),
          nk=nk,delta=delta,energies=energies)
  execute_script('ql-map2d --input DOSMAP.OUT --xlabel Energy --ylabel "y-position" --zlabel DOS --title "Local DOS"')
  


def show_structure():
  """Show the lattice of the system"""
  common.show_structure(qtwrap,get_geometry)



def show_structure_3d():
  """Show the lattice of the system"""
  common.show_structure_3d(qtwrap,get_geometry)





def solve_scf():
  """Perform a selfconsistent calculation - runs in a child process (see
  calc.py/run_calculation.py) instead of calling initialize()/
  common.solve_scf() directly here, so a slow/diverging solve can be
  hard-cancelled via the shell's Cancel control instead of only ever
  finishing or hanging until the app is restarted."""
  qtwrap.run_calculation_subprocess(moddir,"solve_scf",window.scratch_dir)
  window._scf_dirty = False # mirrors common.mark_scf_solved(), which the
                             # subprocess's own DictForm accessor can't
                             # reach (see calc.compute_solve_scf)


codeview.build(qtwrap,get_pyqula_code) # "pyqula code" sub-tab



# create signals: STANDARD_HANDLERS covers the plain "pickup_hamiltonian
# + common.get_X" buttons automatically; only the buttons with mode-specific
# behavior need to be listed explicitly here (save_results/load_results are
# wired automatically by common.finalize_page())
signals = common.wire_standard_signals(qtwrap,pickup_hamiltonian,extra={
  "show_structure": show_structure,  # show bandstructure
  "show_ldos": show_ldos,  # show DOS
  "show_edge_dos": show_edge_dos,  # show DOS
  "show_band_ldos": show_band_ldos,  # interactive LDOS of a picked band-structure point
  "show_structure_3d": show_structure_3d,
  "show_magnetism": show_magnetism,
  "solve_scf": solve_scf,
  "select_atoms_removal": select_atoms_removal,
})

inipath = os.getcwd() # get the initial directory, before common.finalize_page()'s create_folder() chdirs away
common.finalize_page(qtwrap,window,signals,inipath)

if __name__ == "__main__":
    window.run() # show this page as its own standalone window and block

