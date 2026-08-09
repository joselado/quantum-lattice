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


def run_anneal():
  """Build a fresh random configuration at the requested filling and
  anneal it with pyqula's Metropolis swap optimizer. Writes every output
  file the Show */Show * buttons below read, so a later click on one of
  those just re-plots the last anneal without recomputing it."""
  filling = get("filling")
  if not 0.0<filling<1.0:
    raise ValueError("Filling must be strictly between 0 and 1 (got %r) - "
        "optimize_energy() needs both an occupied and an empty site to swap" % filling)
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
  _write_relaxation_frames(g,lg,initial_den,checkpoint_steps)


def _write_relaxation_frames(g,lg,initial_den,checkpoint_steps):
  """Write the occupation snapshots the anneal passed through (the
  initial random configuration plus every step in checkpoint_steps,
  captured into lg.checkpoints via optimize_energy's checkpoint_at
  above) to LATTICEGAS_FRAMES/, following the same indexed-folder +
  index-file convention ql-multildos/ql-multitimeevolution already use
  for their own "step through a sequence of spatial snapshots" sliders
  (see pyqula.timeevolution.evolve_local_state). Lets show_relaxation()
  step through the whole relaxation instead of only ever seeing the
  single final PROFILE.OUT."""
  fs.rmdir("LATTICEGAS_FRAMES")
  fs.mkdir("LATTICEGAS_FRAMES")
  index = open("LATTICEGAS_FRAMES/LATTICEGAS_FRAMES.TXT","w")
  frames = [(0,initial_den)]
  frames += [(s,lg.checkpoints[s]) for s in checkpoint_steps if s in lg.checkpoints]
  for step,den in frames:
    name = "LATTICEGAS_STEP_%d_.OUT"%step
    g.write_profile(den,name="LATTICEGAS_FRAMES/"+name)
    index.write(name+"\n")
  index.close()


def _require_anneal(output_file):
  """Show configuration/correlator/energy trace all read a file run_anneal()
  writes - guard against the silent failure of launching a plotting script
  against a file that was never written (execute_script() runs it as a
  non-blocking background subprocess, so a crash there would otherwise
  never reach an InfoBar)."""
  if not os.path.exists(output_file):
    raise RuntimeError("Run anneal first")


def show_configuration():
  """Show the last annealed occupation (0/1) map"""
  _require_anneal("PROFILE.OUT")
  execute_script("ql-potential --input PROFILE.OUT --cmap binary --colorbar false")


def show_correlator():
  """Show the neighbor-shell density-density correlator of the last anneal"""
  _require_anneal("CORRELATOR.OUT")
  execute_script("ql-latticegas-correlator")


def show_energy_trace():
  """Show the energy trajectory of the last anneal"""
  _require_anneal("ENERGY.OUT")
  execute_script("ql-latticegas-energy")


def show_relaxation():
  """Step through the occupation snapshots recorded at each stage of the
  last anneal, from the initial random configuration to the final one"""
  _require_anneal("LATTICEGAS_FRAMES/LATTICEGAS_FRAMES.TXT")
  execute_script("ql-latticegas-relaxation")


def show_structure():
  """Show the lattice of the system"""
  common.show_structure(qtwrap,get_geometry)


def show_structure_3d():
  """Show the lattice of the system in 3D"""
  common.show_structure_3d(qtwrap,get_geometry)


signals = {
  "run_anneal": run_anneal,
  "show_configuration": show_configuration,
  "show_correlator": show_correlator,
  "show_energy_trace": show_energy_trace,
  "show_relaxation": show_relaxation,
  "show_structure": show_structure,
  "show_structure_3d": show_structure_3d,
}

inipath = os.getcwd() # get the initial directory, before finalize_page()'s create_folder() chdirs away

common.finalize_page(qtwrap,window,signals,inipath)

if __name__ == "__main__":
    window.run() # show this page as its own standalone window and block
