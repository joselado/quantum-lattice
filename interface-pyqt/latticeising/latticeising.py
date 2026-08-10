#!/usr/bin/env python3

from __future__ import print_function

import sys
import os

qlroot = os.path.dirname(os.path.realpath(__file__))+"/../../"
sys.path.append(qlroot+"/pysrc/") # python libraries


from interfacetk import qtwrap # import the library with simple wrappaers to qt4
get = qtwrap.get  # get the value of a certain variable
getbox = qtwrap.getbox  # get the value of a certain variable
window = qtwrap.new_page(os.path.dirname(os.path.realpath(__file__))) # this mode's page

from interfacetk.ql_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries


# This mode is classical statistical mechanics (spin-based Ising model,
# pyqula.latticeising.LatticeIsing), not a quantum tight-binding model -
# there is no Hamiltonian here, so none of common.py's
# pickup_hamiltonian/STANDARD_HANDLERS/wire_standard_signals machinery
# applies. It mirrors the latticegas mode (pyqula.latticegas.LatticeGas)
# very closely - see that mode's own docstrings and INTERFACE_GUIDE.md's
# "Adding a mode" section for the shared pattern - but with two physics
# differences that show up throughout this file: LatticeIsing's spins
# s in {-1,+1} use the OPPOSITE add_interaction() sign convention from
# LatticeGas's occupations (positive Jij is *ferromagnetic* here, not
# repulsive - see pyqula.latticeising's own module docstring), and the
# dynamics used below (li.optimize_energy(), single-spin-flip Metropolis)
# does NOT conserve magnetization - unlike LatticeGas's swap-based
# optimize_energy() (fixed filling), so a uniform external field
# genuinely matters here instead of being a no-op. Also note: since
# self.pairs lists both directions of every bond (see LatticeIsing's own
# module docstring), get_energy() runs twice the usual sum-over-bonds
# convention, so temperature scales here are ~2x literature values (e.g.
# the 2D square-lattice ferromagnet's Tc sits near 2x2.269=4.54, not
# 2.269) - interface.ui's default Temperature (3.0) is picked with that
# in mind, well above latticegas's 0.5 default, so a first click doesn't
# land deep in the fully-ordered regime.


LATTICES = {
  "Chain": geometry.chain,
  "Square": geometry.single_square_lattice,
  "Triangular": geometry.triangular_lattice,
  "Honeycomb": geometry.honeycomb_lattice,
  "Kagome": geometry.kagome_lattice,
  "Lieb": geometry.lieb_lattice,
}


def get_geometry():
  """Build a large finite (open-boundary) patch of the chosen lattice to
  host the classical Ising model - mirrors latticegas.get_geometry(): a
  big periodic patch, then dimensionality forced to 0 so
  add_interaction()'s neighbor-matrix trick and get_correlator() both see
  a plain finite cluster with open boundaries."""
  lattice_name = getbox("lattice") # get the option
  g = LATTICES[lattice_name]() # call the geometry
  if g.dimensionality==2: # turn_orthorhombic only supports 2d geometries
    g = supercell.turn_orthorhombic(g)
  n = int(get("supercell_size"))
  g = g.get_supercell(n)
  g.dimensionality = 0 # open boundary conditions for the interactions
  return g


def get_field_array(g):
  """External (Zeeman-like) field per site - a plain number (uniform,
  broadcast to every site) or a position-dependent expression (evaluated
  per site), the same "lambda r: ..." fallback qtwrap.get() already
  supports for fields like crystalfield/strain profiles elsewhere in the
  interface. Unlike latticegas's mu_profile, a uniform field here is NOT
  a no-op: the single-spin-flip dynamics used by run_anneal() below does
  not conserve magnetization, so a constant field genuinely biases which
  configuration is favored (see get_local_field() in pyqula.latticeising)."""
  field_fun = get("field_profile")
  if callable(field_fun):
    return np.array([field_fun(r) for r in g.r])
  else:
    return np.full(len(g.r),field_fun)


_anneal_state = {} # stashes the objects (not just files) from the last
    # successful anneal - g, li, frames, is_2d, plus a
    # correlator_computed flag - so show_spin_correlator_relaxation() can
    # compute the per-snapshot correlator/structure factor lazily, only
    # when that button is actually pressed (once per anneal, cached
    # across repeat clicks via the flag), instead of run_anneal() always
    # paying for it - mirrors latticegas._anneal_state, see its own
    # docstring for why that cost matters.

_anneal_dirty_time = None # window.params_dirty_time() as of the last
    # successful run_anneal() - mirrors latticegas._anneal_dirty_time.


def run_anneal():
  """Build a fresh random spin configuration at the requested initial
  magnetization and relax it with pyqula's single-spin-flip Metropolis
  optimizer (li.optimize_energy() - the standard Ising Monte Carlo move
  set, in which magnetization is not conserved but fluctuates under the
  field). Writes every output file the Show */Show * buttons below read.
  Not wired to a button of its own - mirrors latticegas.run_anneal(),
  including the auto-run-on-Show-click / checkpoint pattern; see that
  function's docstring."""
  global _anneal_dirty_time
  m0 = get("magnetization")
  if not -1.0<=m0<=1.0:
    raise ValueError("Initial magnetization must be between -1 and 1 (got %r)" % m0)
  _anneal_state.clear() # so a failed anneal (below) leaves _ensure_annealed()
      # correctly retrying next time instead of serving stale results from
      # whatever anneal last succeeded
  is_2d = getbox("lattice")!="Chain" # every LATTICES entry but Chain is a 2D Bravais lattice
  g = get_geometry()
  li = latticeising.LatticeIsing(g,m=m0)
  li.add_field(get_field_array(g))
  li.add_interaction(Jij=qtwrap.get_array("Jij_ising"))
  ntries = int(get("ntries"))
  n_snapshots = int(get("n_snapshots"))
  checkpoint_steps = sorted(set(np.linspace(1,ntries,n_snapshots).astype(int)))
  initial_s = li.s.copy() # before any trial move, for the first frame
  es,ms = li.optimize_energy(temp=get("temp"),ntries=ntries,
      checkpoint_at=checkpoint_steps)
  g.write_profile(li.s,name="SPIN.OUT") # spin map
  np.savetxt("ENERGY.OUT",np.array([np.arange(len(es)),es]).T)
  np.savetxt("MAGNETIZATION.OUT",np.array([np.arange(len(ms)),ms]).T)
  frames = _checkpoint_frames(li,initial_s,checkpoint_steps)
  _write_configuration_frames(g,frames)
  _anneal_state.update(g=g,li=li,frames=frames,is_2d=is_2d,
      correlator_computed=False)
  _anneal_dirty_time = window.params_dirty_time()


def _needs_live_anneal():
  """Whether this process's own last live run_anneal() call (if any)
  still matches the current parameters - mirrors
  latticegas._needs_live_anneal()."""
  return _anneal_dirty_time is None or window.params_dirty_time()>_anneal_dirty_time


def _ensure_annealed():
  """Run the anneal automatically if this process doesn't already have a
  result matching the current parameters, or a fresh-enough SPIN.OUT was
  just restored by Load Results - mirrors latticegas._ensure_annealed(),
  see its docstring for the two-layer freshness check."""
  if not _needs_live_anneal(): return
  if os.path.isfile("SPIN.OUT") and os.path.getmtime("SPIN.OUT")>=window.params_dirty_time():
    return
  run_anneal()


def _checkpoint_frames(li,initial_s,checkpoint_steps):
  """(step,s) pairs for every spin snapshot recorded during the last
  anneal - mirrors latticegas._checkpoint_frames()."""
  frames = [(0,initial_s)]
  frames += [(s,li.checkpoints[s]) for s in checkpoint_steps if s in li.checkpoints]
  return frames


def _write_configuration_frames(g,frames):
  """Write every spin snapshot to LATTICEISING_FRAMES/, the indexed
  folder + index-file convention shared with latticegas's
  LATTICEGAS_FRAMES/ - see _write_configuration_frames() there."""
  fs.rmdir("LATTICEISING_FRAMES")
  fs.mkdir("LATTICEISING_FRAMES")
  index = open("LATTICEISING_FRAMES/LATTICEISING_FRAMES.TXT","w")
  for step,s in frames:
    name = "LATTICEISING_STEP_%d_.OUT"%step
    g.write_profile(s,name="LATTICEISING_FRAMES/"+name)
    index.write(name+"\n")
  index.close()


def _write_correlator_frames(g,li,frames,is_2d):
  """Write, at every spin snapshot in `frames`, whichever correlator is
  actually shown by show_spin_correlator_relaxation()'s right panel -
  mirrors latticegas._write_correlator_frames() exactly, swapping
  LatticeGas.get_correlator()/get_structure_factor() (density-density)
  for LatticeIsing's spin-spin equivalents. Only called from
  show_spin_correlator_relaxation(), not from run_anneal() - see that
  mode's docstring for why this expensive part is deferred."""
  final_s = li.s.copy()
  if is_2d:
    fs.rmdir("LATTICEISING_STRUCTURE_FRAMES")
    fs.mkdir("LATTICEISING_STRUCTURE_FRAMES")
    sindex = open("LATTICEISING_STRUCTURE_FRAMES/LATTICEISING_STRUCTURE_FRAMES.TXT","w")
  else:
    fs.rmdir("LATTICEISING_CORRELATOR_FRAMES")
    fs.mkdir("LATTICEISING_CORRELATOR_FRAMES")
    cindex = open("LATTICEISING_CORRELATOR_FRAMES/LATTICEISING_CORRELATOR_FRAMES.TXT","w")
  for step,s in frames:
    li.s = s
    if is_2d:
      qpath,sq = li.get_structure_factor()
      sname = "LATTICEISING_SQ_STEP_%d_.OUT"%step
      np.savetxt("LATTICEISING_STRUCTURE_FRAMES/"+sname,
          np.array([qpath[:,0],qpath[:,1],sq]).T)
      sindex.write(sname+"\n")
    else:
      # capped at n=8 shells, same rationale as latticegas: a quick
      # slider scrub doesn't need 20 shells' worth of resolution
      x,y = li.get_correlator(n=8)
      cname = "LATTICEISING_CORR_STEP_%d_.OUT"%step
      np.savetxt("LATTICEISING_CORRELATOR_FRAMES/"+cname,np.array([x,y]).T)
      cindex.write(cname+"\n")
  if is_2d: sindex.close()
  else: cindex.close()
  li.s = final_s


def show_spin_configuration():
  """Show the last annealed spin (+-1) map, running the anneal
  automatically first if needed (see _ensure_annealed)"""
  _ensure_annealed()
  execute_script("ql-potential --input SPIN.OUT")


def show_spin_relaxation():
  """Step through the spin snapshots recorded at each stage of the last
  anneal, from the initial random configuration to the final one,
  running the anneal automatically first if needed"""
  _ensure_annealed()
  execute_script("ql-latticeising-relaxation")


def show_spin_correlator_relaxation():
  """Run the anneal automatically first if needed, then compute (only
  the first time this is clicked for a given anneal) and step through
  the neighbor-shell spin correlator - and, for 2D lattices, the
  reciprocal-space structure factor - at each stage of the last anneal.
  Mirrors latticegas.show_correlator_relaxation() - see its docstring
  for why this checks _needs_live_anneal() directly instead of going
  through _ensure_annealed()."""
  if _needs_live_anneal():
    run_anneal()
  if not _anneal_state["correlator_computed"]:
    _write_correlator_frames(_anneal_state["g"],_anneal_state["li"],
        _anneal_state["frames"],_anneal_state["is_2d"])
    _anneal_state["correlator_computed"] = True
  execute_script("ql-latticeising-correlator-relaxation")


def show_structure():
  """Show the lattice of the system"""
  common.show_structure(qtwrap,get_geometry)


def show_structure_3d():
  """Show the lattice of the system in 3D"""
  common.show_structure_3d(qtwrap,get_geometry)


signals = {
  "show_spin_configuration": show_spin_configuration,
  "show_spin_correlator_relaxation": show_spin_correlator_relaxation,
  "show_spin_relaxation": show_spin_relaxation,
  "show_structure": show_structure,
  "show_structure_3d": show_structure_3d,
}

inipath = os.getcwd() # get the initial directory, before finalize_page()'s create_folder() chdirs away

common.finalize_page(qtwrap,window,signals,inipath)

if __name__ == "__main__":
    window.run() # show this page as its own standalone window and block
