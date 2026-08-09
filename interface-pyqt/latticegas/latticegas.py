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


# This mode is classical statistical mechanics (occupation-based lattice
# gas, pyqula.latticegas.LatticeGas), not a quantum tight-binding model -
# there is no Hamiltonian here, so none of common.py's
# pickup_hamiltonian/STANDARD_HANDLERS/wire_standard_signals machinery
# applies. See INTERFACE_GUIDE.md's "Adding a mode" section for how this
# mode differs from the rest.


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
  host the classical lattice-gas model - mirrors pyqula's own latticegas
  usage example (see pysrc/pyqula_user_guide.md's "Lattice gas models"
  section): a big periodic patch, then dimensionality forced to 0 so
  add_interaction()'s neighbor-matrix trick and get_correlator() both see
  a plain finite cluster with open boundaries, rather than an island
  shaped by pyqula.islands the way the quantum modes (0d, huge_0d, ...)
  build theirs."""
  lattice_name = getbox("lattice") # get the option
  g = LATTICES[lattice_name]() # call the geometry
  if g.dimensionality==2: # turn_orthorhombic only supports 2d geometries
    g = supercell.turn_orthorhombic(g)
  n = int(get("supercell_size"))
  g = g.get_supercell(n)
  g.dimensionality = 0 # open boundary conditions for the interactions
  return g


def get_mu_array(g):
  """Chemical potential per site - a plain number (uniform, broadcast to
  every site) or a position-dependent expression (evaluated per site),
  the same "lambda r: ..." fallback qtwrap.get() already supports for
  fields like crystalfield/strain profiles elsewhere in the interface.
  Note a uniform mu has no effect on the annealed ground state itself
  (optimize_energy only performs fixed-filling swaps, under which a
  constant offset cannot change which configuration is favored) - it
  only matters when it varies from site to site."""
  mu_fun = get("mu_profile")
  if callable(mu_fun):
    return np.array([mu_fun(r) for r in g.r])
  else:
    return np.full(len(g.r),mu_fun)


_anneal_state = {} # stashes the objects (not just files) from the last
    # successful anneal - g, lg, frames, is_2d, plus a
    # correlator_computed flag - so show_correlator_relaxation() can
    # compute the per-snapshot correlator/structure factor lazily, only
    # when that button is actually pressed (once per anneal, cached
    # across repeat clicks via the flag), instead of run_anneal() always
    # paying for it - see show_correlator_relaxation()'s docstring for
    # why that cost matters. Safe to keep as a plain module global: this
    # module is imported once for the app's lifetime, and qtwrap's
    # app-wide busy lock means only one handler ever runs at a time, so
    # there's no concurrent access.

_anneal_dirty_time = None # window.params_dirty_time() as of the last
    # successful run_anneal() - None means "never run yet, in this
    # process". Compared against the live params_dirty_time() by
    # _needs_live_anneal()/_ensure_annealed() below to decide whether a
    # Show button needs a fresh anneal first - same "rebuild only if
    # something changed" pattern as huge_0d.py's
    # initialize()/_ensure_initialized().


def run_anneal():
  """Build a fresh random configuration at the requested filling and
  anneal it with pyqula's Metropolis swap optimizer. Writes every output
  file the Show */Show * buttons below read. Not wired to a button of its
  own - every Show button calls _ensure_annealed() first, which calls
  this automatically only when needed (see _anneal_dirty_time)."""
  global _anneal_dirty_time
  filling = get("filling")
  if not 0.0<filling<1.0:
    raise ValueError("Filling must be strictly between 0 and 1 (got %r) - "
        "optimize_energy() needs both an occupied and an empty site to swap" % filling)
  _anneal_state.clear() # so a failed anneal (below) leaves _ensure_annealed()
      # correctly retrying next time instead of serving stale results from
      # whatever anneal last succeeded
  is_2d = getbox("lattice")!="Chain" # every LATTICES entry but Chain is a 2D Bravais lattice
  g = get_geometry()
  lg = latticegas.LatticeGas(g,filling=filling)
  lg.mu = get_mu_array(g)
  lg.add_interaction(Jij=qtwrap.get_array("Jij"))
  ntries = int(get("ntries"))
  n_snapshots = int(get("n_snapshots"))
  checkpoint_steps = sorted(set(np.linspace(1,ntries,n_snapshots).astype(int)))
  initial_den = lg.den.copy() # before any trial move, for the first frame
  es = lg.optimize_energy(temp=get("temp"),ntries=ntries,
      checkpoint_at=checkpoint_steps)
  g.write_profile(lg.den,name="PROFILE.OUT") # occupation map
  x,y = lg.get_correlator()
  np.savetxt("CORRELATOR.OUT",np.array([x,y]).T)
  np.savetxt("ENERGY.OUT",np.array([np.arange(len(es)),es]).T)
  frames = _checkpoint_frames(lg,initial_den,checkpoint_steps)
  _write_configuration_frames(g,frames)
  _anneal_state.update(g=g,lg=lg,frames=frames,is_2d=is_2d,
      correlator_computed=False)
  _anneal_dirty_time = window.params_dirty_time()


def _needs_live_anneal():
  """Whether this process's own last live run_anneal() call (if any)
  still matches the current parameters - i.e. whether _anneal_state's
  Python objects (g, lg, frames) can be trusted. Unlike
  _ensure_annealed()'s file-freshness check below, this ignores disk
  state entirely: _anneal_state only ever comes from an actual
  run_anneal() call in this process, never from a Load Results file
  restore, so params_dirty_time() alone (not PROFILE.OUT's mtime) is
  what tells us whether it's still current."""
  return _anneal_dirty_time is None or window.params_dirty_time()>_anneal_dirty_time


def _ensure_annealed():
  """Run the anneal automatically if this process doesn't already have
  a result matching the current parameters - so every Show button below
  works standalone, with no separate explicit Run step. Two things
  count as "already matching": this process's own last live anneal, if
  no parameter has changed since (_needs_live_anneal() False); or - since
  Load Results' reset_dirty() bumps params_dirty_time() forward exactly
  the way a live field edit would - a PROFILE.OUT already on disk that's
  at least as new as the current parameters, covering "the user just
  loaded a saved anneal and hasn't touched anything since" without this
  silently discarding what they loaded and replacing it with a fresh,
  differently-random anneal."""
  if not _needs_live_anneal(): return
  if os.path.isfile("PROFILE.OUT") and os.path.getmtime("PROFILE.OUT")>=window.params_dirty_time():
    return
  run_anneal()


def _checkpoint_frames(lg,initial_den,checkpoint_steps):
  """(step,den) pairs for every occupation snapshot recorded during the
  last anneal - the pre-anneal random configuration (step 0) plus every
  checkpoint optimize_energy's checkpoint_at captured into
  lg.checkpoints. Shared by every "across snapshots" writer below, so
  they all index the same sequence of steps and their Step sliders stay
  in lockstep with each other."""
  frames = [(0,initial_den)]
  frames += [(s,lg.checkpoints[s]) for s in checkpoint_steps if s in lg.checkpoints]
  return frames


def _write_configuration_frames(g,frames):
  """Write every occupation snapshot to LATTICEGAS_FRAMES/, the indexed
  folder + index-file convention ql-multildos/ql-multitimeevolution use
  for their own multi-frame outputs (see
  pyqula.timeevolution.evolve_local_state's MULTITIMEEVOLUTION/ folder).
  Lets show_relaxation() step through the whole relaxation instead of
  only ever seeing the single final PROFILE.OUT."""
  fs.rmdir("LATTICEGAS_FRAMES")
  fs.mkdir("LATTICEGAS_FRAMES")
  index = open("LATTICEGAS_FRAMES/LATTICEGAS_FRAMES.TXT","w")
  for step,den in frames:
    name = "LATTICEGAS_STEP_%d_.OUT"%step
    g.write_profile(den,name="LATTICEGAS_FRAMES/"+name)
    index.write(name+"\n")
  index.close()


def _write_correlator_frames(g,lg,frames,is_2d):
  """Write, at every occupation snapshot in `frames`, whichever
  correlator is actually shown by show_correlator_relaxation()'s right
  panel - for a genuinely 2D lattice (is_2d - everything in LATTICES but
  Chain), the reciprocal-space structure factor S(q)
  (LatticeGas.get_structure_factor(), the 2D companion to the
  neighbor-shell correlator G(r): G(r) gives the ordering length scale,
  S(q) gives its wavevector) to LATTICEGAS_STRUCTURE_FRAMES/; otherwise
  (Chain, which has no meaningful S(q)) G(r) itself
  (LatticeGas.get_correlator()) to LATTICEGAS_CORRELATOR_FRAMES/ - same
  indexed-folder convention as _write_configuration_frames. Only one of
  the two is written since the other is never plotted (G(r) for the
  final snapshot is still always available via CORRELATOR.OUT/
  show_correlator(), independent of this function). Only called from
  show_correlator_relaxation() itself (see _anneal_state), not from
  run_anneal(), since this is the expensive part of the two (see below)
  and most anneals never get this button clicked. Temporarily overwrites
  lg.den per frame since get_correlator()/get_structure_factor() read
  it, restoring the final configuration afterwards."""
  final_den = lg.den.copy()
  if is_2d:
    fs.rmdir("LATTICEGAS_STRUCTURE_FRAMES")
    fs.mkdir("LATTICEGAS_STRUCTURE_FRAMES")
    sindex = open("LATTICEGAS_STRUCTURE_FRAMES/LATTICEGAS_STRUCTURE_FRAMES.TXT","w")
  else:
    fs.rmdir("LATTICEGAS_CORRELATOR_FRAMES")
    fs.mkdir("LATTICEGAS_CORRELATOR_FRAMES")
    cindex = open("LATTICEGAS_CORRELATOR_FRAMES/LATTICEGAS_CORRELATOR_FRAMES.TXT","w")
  for step,den in frames:
    lg.den = den
    if is_2d:
      qpath,sq = lg.get_structure_factor()
      sname = "LATTICEGAS_SQ_STEP_%d_.OUT"%step
      np.savetxt("LATTICEGAS_STRUCTURE_FRAMES/"+sname,
          np.array([qpath[:,0],qpath[:,1],sq]).T)
      sindex.write(sname+"\n")
    else:
      # get_nnc's per-shell loop is O(nsites^2), so at the full default
      # of n=20 shells this dominates the wall time of this function
      # once multiplied across every frame - capped lower here since a
      # quick slider scrub doesn't need 20 shells' worth of resolution
      # to show the ordering trend. The final snapshot's own
      # CORRELATOR.OUT (in run_anneal()) and show_correlator() keep the
      # uncapped default.
      x,y = lg.get_correlator(n=8)
      cname = "LATTICEGAS_CORR_STEP_%d_.OUT"%step
      np.savetxt("LATTICEGAS_CORRELATOR_FRAMES/"+cname,np.array([x,y]).T)
      cindex.write(cname+"\n")
  if is_2d: sindex.close()
  else: cindex.close()
  lg.den = final_den


def show_configuration():
  """Show the last annealed occupation (0/1) map, running the anneal
  automatically first if needed (see _ensure_annealed)"""
  _ensure_annealed()
  execute_script("ql-potential --input PROFILE.OUT --cmap binary --colorbar false")


def show_correlator():
  """Show the neighbor-shell density-density correlator of the last
  anneal, running the anneal automatically first if needed"""
  _ensure_annealed()
  execute_script("ql-latticegas-correlator")


def show_relaxation():
  """Step through the occupation snapshots recorded at each stage of the
  last anneal, from the initial random configuration to the final one,
  running the anneal automatically first if needed"""
  _ensure_annealed()
  execute_script("ql-latticegas-relaxation")


def show_correlator_relaxation():
  """Run the anneal automatically first if needed, then compute (only
  the first time this is clicked for a given anneal, so every other
  button stays unaffected by this one's cost - see _anneal_state) and
  step through the neighbor-shell correlator - and, for 2D lattices, the
  reciprocal-space structure factor - at each stage of the last anneal.
  A later click just replots the same frames, same as every other Show
  button here.

  Unlike the other Show buttons, this doesn't go through
  _ensure_annealed(): that function's file-freshness bypass (letting a
  freshly Load Results-restored PROFILE.OUT count as "up to date") isn't
  enough here, since this button needs the actual LatticeGas object
  (_anneal_state), not just flat files - Load Results doesn't restore
  that (or the LATTICEGAS_*_FRAMES/ folders this button reads/writes),
  so a live anneal is required whenever _needs_live_anneal() is True."""
  if _needs_live_anneal():
    run_anneal()
  if not _anneal_state["correlator_computed"]:
    _write_correlator_frames(_anneal_state["g"],_anneal_state["lg"],
        _anneal_state["frames"],_anneal_state["is_2d"])
    _anneal_state["correlator_computed"] = True
  execute_script("ql-latticegas-correlator-relaxation")


def show_structure():
  """Show the lattice of the system"""
  common.show_structure(qtwrap,get_geometry)


def show_structure_3d():
  """Show the lattice of the system in 3D"""
  common.show_structure_3d(qtwrap,get_geometry)


signals = {
  "show_configuration": show_configuration,
  "show_correlator": show_correlator,
  "show_correlator_relaxation": show_correlator_relaxation,
  "show_relaxation": show_relaxation,
  "show_structure": show_structure,
  "show_structure_3d": show_structure_3d,
}

inipath = os.getcwd() # get the initial directory, before finalize_page()'s create_folder() chdirs away

common.finalize_page(qtwrap,window,signals,inipath)

if __name__ == "__main__":
    window.run() # show this page as its own standalone window and block
