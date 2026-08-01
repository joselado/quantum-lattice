"""Pure (no QApplication/page-construction) geometry/Hamiltonian-building
code for the 1D ribbon mode, importable on its own by
run_calculation.py's child process - unlike 1d.py itself, which builds its
page as a side effect of import (`window = qtwrap.new_page(...)` at module
level, unconditional).

get_geometry()/initialize() are the same functions 1d.py used to define
inline, now taking an explicit `accessor` (defaulting to the live qtwrap
module) so the identical code can run against either the real qtwrap
(the normal in-process GUI path - unchanged) or a dictform.DictForm
wrapping a JSON snapshot (the subprocess path - see compute_solve_scf()
below and qtwrap.run_calculation_subprocess()). This is the "gather inputs
up front, run the same code against them" approach CLAUDE.md's
"a larger follow-up" comment on hard-cancelling a calculation calls for,
applied one handler at a time rather than as one large rewrite - see
INTERFACE_GUIDE.md's cancellation-rollout notes.

Only solve_scf is migrated to the subprocess path so far (see
COMPUTE_HANDLERS below); every other 1d.py handler still runs in-process,
unaffected by anything in this file.
"""
import numpy as np

from interfacetk import qtwrap
# import pyqula only via ql_interface's star-import, in the same order
# 1d.py itself uses (hamiltonians, klist, geometry, sculpt, ... - see
# qlinterface.py) - some environments have a second, editable pyqula
# checkout earlier on sys.path than this repo's vendored pysrc/pyqula/,
# whose own sculpt.py only imports cleanly once pyqula's package-level
# init has already run via that full sequence; importing interfacetk.py's
# lone `from pyqula import sculpt` first (before anything else has primed
# that sequence) can hit a circular-import error that never shows up in
# the normal <mode>.py flow, where ql_interface's star-import always runs
# first.
from interfacetk.ql_interface import * # noqa: F401,F403 - geometry, ribbon, np, ...
from interfacetk import interfacetk
from interfacetk import hamiltoniantype
from interfacetk import common


def get_geometry(accessor=qtwrap,modify=True):
  """Create a 1d ribbon - identical to 1d.py's former inline version,
  parameterized on `accessor` instead of reading the module-level
  qtwrap/getbox/get names directly."""
  lattice_name = accessor.getbox("lattice") # get the option
  n = int(accessor.get("width")) # thickness of the system
  lattices = {
    "Chain": geometry.chain,
    "Bichain": geometry.bichain,
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
  nsuper = int(accessor.get("nsuper"))
  g = g.supercell(nsuper,store_primal=True)
  if modify: g = interfacetk.modify_geometry(g,accessor)
  return g


def initialize(accessor=qtwrap):
  """Build the Hamiltonian - identical to 1d.py's former inline version,
  parameterized on `accessor`."""
  g = get_geometry(accessor)
  has_spin = hamiltoniantype.wants_spin(accessor)
  h = g.get_hamiltonian(has_spin=has_spin,tij=accessor.get_array("hoppings"))
  h.turn_multicell()
  if has_spin: # see hamiltoniantype.py's docstring - these unconditionally
    # call turn_spinful() themselves, so they must be skipped outright for
    # "Spinless" rather than called with a zero-ish value
    h.add_zeeman(accessor.get_array("exchange"))
    if abs(accessor.get("rashba")) > 0.0: h.add_rashba(accessor.get("rashba"))  # Rashba field
    h.add_antiferromagnetism(accessor.get("mAF"))  # AF order
    h.add_kane_mele(accessor.get("kanemele")) # intrinsic SOC
    h.add_anti_kane_mele(accessor.get("antikanemele"))
  h.add_sublattice_imbalance(accessor.get("mAB"))  # sublattice imbalance
  h.add_crystal_field(accessor.get("crystalfield"))
  h.shift_fermi(accessor.get("fermi")) # shift fermi energy
  h.add_haldane(accessor.get("haldane")) # intrinsic SOC
  h.add_antihaldane(accessor.get("antihaldane"))
  h.add_peierls(accessor.get("peierls")) # magnetic field
  if hamiltoniantype.wants_nambu(accessor):
    h.setup_nambu_spinor() # establish the BdG structure even if
                            # swave/pwave are both left at zero
    if accessor.get("swave")!=0.: h.add_swave(accessor.get("swave"))
    p = accessor.get_array("pwave")
    if np.sum(np.abs(p))>0.0:
        h.add_pairing(d=p,mode="triplet",delta=1.0)
  return h


def compute_solve_scf(inputs):
  """Pure, subprocess-safe reimplementation of 1d.py's solve_scf() button:
  builds the Hamiltonian and runs the mean-field solve using only the
  field values captured in `inputs` (a save_interface()-shaped snapshot -
  see dictform.DictForm), with no qtwrap/widget access at all. Runs with
  the scratch dir already as cwd (run_calculation.py chdirs there before
  calling this), so file I/O (hamiltonian.pkl, ...) lands in the same
  place the in-process handler would have written it."""
  from interfacetk.dictform import DictForm
  accessor = DictForm(inputs)
  h = initialize(accessor)
  common.solve_scf(h,accessor)


COMPUTE_HANDLERS = {
    "solve_scf": compute_solve_scf,
}
