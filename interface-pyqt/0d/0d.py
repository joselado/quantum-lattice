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

from interfacetk import scfterms
scfterms.build(qtwrap) # build the Density-density/Spin-spin mean field tabs

from interfacetk import codeview

from interfacetk.ql_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries
common.initialize(qtwrap) # several initilizations
qtwrap.set_combobox("dos_operator",operators.operator_list)

from interfacetk import interfacetk
select_atoms_removal = lambda: common.select_atoms_removal(get_geometry)
pickup_hamiltonian = lambda: common.pickup_hamiltonian(qtwrap,initialize,do_scf=True,solve=solve_scf)

from interfacetk import latticeterms
latticeterms.connect(qtwrap,lambda: getbox("lattice")) # hide honeycomb-only
                                                         # terms (Haldane,
                                                         # Kane-Mele, valley)
                                                         # for other lattices


def get_geometry(modify=True):
  """ Create a 0d island"""
  lattice_name = getbox("lattice") # get the option
  n = float(get("width")) # thickness of the system
  lattices = {
    "Chain": geometry.chain,
    "Honeycomb": geometry.honeycomb_lattice,
    "Square": geometry.single_square_lattice,
    "Kagome": geometry.kagome_lattice,
    "Lieb": geometry.lieb_lattice,
    "Triangular": geometry.triangular_lattice_tripartite,
    "Honeycomb zigzag": lambda: geometry.honeycomb_zigzag_ribbon(n),
    "Honeycomb armchair": lambda: geometry.honeycomb_armchair_ribbon(n),
  }
  g = lattices[lattice_name]()
  rot = get("rotation")*np.pi/180.
  g = islands.get_geometry(n=n,nedges=int(get("nsides")),rot=rot,geo=g)
  if modify: g = modify_geometry(g) # modify the geometry
  return g


def select_atom_time_evolution():
  """Select a single atom"""
  g = get_geometry() # get the unmodified geometry
  g.write()
  execute_script("ql-pick-single-atom") # pick a single atom


def show_time_evolution():
  h = pickup_hamiltonian() # get hamiltonian
  try: i = open("SELECTED_SINGLE_ATOM.INFO").read()
  except: i = 0
  if i=="": i=0
  else: i = int(i)
  if h.has_spin: 
      i = i*2
      if qtwrap.getbox("channel_time_evolution")=="Down": i += 1
#  print(i) ; return
  if h.has_eh: i = i*4
  tmax = qtwrap.get("tmax_time_evolution") # maximum time
  timeevolution.evolve_local_state(h,i=i,ts=np.linspace(0.,tmax,100),
        mode="green")
  execute_script("ql-multitimeevolution") # plot the result






def modify_geometry(g):
  """Modify the geometry according to the interface"""
  g = interfacetk.modify_geometry(g,qtwrap)
  g.center()
  return g # return geometry
  


     






def initialize():
    """ Initialize the calculation"""
    g = get_geometry() # get the geometry
    h = g.get_hamiltonian(has_spin=True,tij=qtwrap.get_array("hoppings"))
    h.add_zeeman(qtwrap.get_array("exchange"))
    h.add_sublattice_imbalance(get("mAB"))  # sublattice imbalance
    h.add_rashba(get("rashba"))  # Rashba field
    h.add_antiferromagnetism(get("mAF"))  # AF order
    h.add_crystal_field(qtwrap.get("crystalfield")) # add magnetic field
    h.shift_fermi(get("fermi")) # shift fermi energy
    h.add_kane_mele(get("kanemele")) # intrinsic SOC
    h.add_haldane(get("haldane")) # intrinsic SOC
    h.add_antihaldane(get("antihaldane")) 
    h.add_peierls(get("peierls")) # magnetic field
    common.add_strain(h,window) # add strain
    if get("swave")!=0.0: h.add_swave(get("swave")) 
    p = qtwrap.get_array("pwave")
    if np.sum(np.abs(p))>0.0:
        h.add_pairing(d=p,mode="triplet",delta=1.0)
    return h


_LATTICE_CALLS = {
  "Chain": "geometry.chain()",
  "Honeycomb": "geometry.honeycomb_lattice()",
  "Square": "geometry.single_square_lattice()",
  "Kagome": "geometry.kagome_lattice()",
  "Lieb": "geometry.lieb_lattice()",
  "Triangular": "geometry.triangular_lattice_tripartite()",
  "Honeycomb zigzag": "geometry.honeycomb_zigzag_ribbon(%s)",
  "Honeycomb armchair": "geometry.honeycomb_armchair_ribbon(%s)",
}


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
  width = fv("width") # matches get_geometry()'s own float(get("width"))
  nsides = str(int(get("nsides"))) # matches get_geometry()'s int(get("nsides"))
  lattice_call = _LATTICE_CALLS[lattice_name]
  if "%s" in lattice_call: lattice_call = lattice_call % width

  lines = [
    "from pyqula import geometry, islands",
    "import numpy as np",
    "",
    "g = %s" % lattice_call,
    "g = islands.get_geometry(n=%s, nedges=%s, rot=%s*np.pi/180., geo=g)"
        % (width,nsides,fv("rotation")),
  ]
  lines += codeview.geometry_removal_code(qtwrap,center=True)
  lines += [
    "",
    "h = g.get_hamiltonian(has_spin=True, tij=%s)" % fa("hoppings"),
  ]
  if active("exchange"): lines.append("h.add_zeeman(%s)" % fa("exchange"))
  if active("mAB"): lines.append("h.add_sublattice_imbalance(%s)" % fv("mAB"))
  if active("rashba"): lines.append("h.add_rashba(%s)" % fv("rashba"))
  if active("mAF"): lines.append("h.add_antiferromagnetism(%s)" % fv("mAF"))
  if active("crystalfield"): lines.append("h.add_crystal_field(%s)" % fv("crystalfield"))
  if active("fermi"): lines.append("h.shift_fermi(%s)" % fv("fermi"))
  if active("kanemele"): lines.append("h.add_kane_mele(%s)" % fv("kanemele"))
  if active("haldane"): lines.append("h.add_haldane(%s)" % fv("haldane"))
  if active("antihaldane"): lines.append("h.add_antihaldane(%s)" % fv("antihaldane"))
  if active("peierls"): lines.append("h.add_peierls(%s)" % fv("peierls"))
  if active("strain_strength"):
    v0 = repr(1.0+get("strain_strength"))
    rl = repr(get("strain_decay"))
    stype = getbox("strain_type")
    if stype=="Radial scalar":
      lines.append("from pyqula import potentials")
      lines.append("fs = potentials.radial_decay(v0=%s, voo=1.0, rl=%s)" % (v0,rl))
      lines.append("h.add_strain(fs, mode=\"scalar\")")
    elif stype=="Radial vector":
      lines.append("from pyqula.potentialtk.vectorprofile import radial_vector_decay")
      lines.append("fs = radial_vector_decay(v0=%s, voo=1.0, rl=%s)" % (v0,rl))
      lines.append("h.add_strain(fs, mode=\"non_uniform\")")
  if active("swave"): lines.append("h.add_swave(%s)" % fv("swave"))
  if active("pwave"): lines.append("h.add_pairing(d=%s, mode=\"triplet\", delta=1.0)" % fa("pwave"))

  if qtwrap.is_checked("do_scf"):
    lines += common.pyqula_code_scf_block(qtwrap,richer=False)

  return "\n".join(lines)


def show_interactive_ldos():
  h = pickup_hamiltonian()  # get the hamiltonian
  common.get_multildos(h,qtwrap) # compute




def show_structure():
  """Show the lattice of the system"""
  common.show_structure(qtwrap,get_geometry)




def show_structure_3d():
  """Show the lattice of the system"""
  common.show_structure_3d(qtwrap,get_geometry)



def solve_scf():
  """Perform a selfconsistent calculation"""
  h = initialize()
  common.solve_scf(h,qtwrap)







def show_magnetism():
  """Show the magnetism of the system"""
  h = pickup_hamiltonian() # get the Hamiltonian
  h.write_magnetization() # write the magnetism
  if getbox("magnetization_plot_mode")=="2D":
      execute_script("ql-magnetism2d")
  else: # 3D mode
      execute_script("ql-moments")


def show_hoppings():
  """Show the lattice of the system"""
  h = pickup_hamiltonian() # get the Hamiltonian
  h.write_hopping()
  execute_script("ql-network --input HOPPING.OUT")


def show_local_chern():
  h = pickup_hamiltonian() # get hamiltonian
  op = getbox("operator_chern")
  op = h.get_operator(op)
  topology.real_space_chern(h,operator=op)
  execute_script("ql-potential --input REAL_SPACE_CHERN.OUT --cmap rainbow")



codeview.build(qtwrap,get_pyqula_code) # "pyqula code" sub-tab

inipath = os.getcwd() # get the initial directory, before common.finalize_page()'s create_folder() chdirs away

# create signals: STANDARD_HANDLERS covers the plain "pickup_hamiltonian
# + common.get_X" buttons automatically; only the buttons with mode-specific
# behavior need to be listed explicitly here (save_results/load_results are
# wired automatically by common.finalize_page())
signals = common.wire_standard_signals(qtwrap,pickup_hamiltonian,extra={
  "solve_scf": solve_scf,
  "show_structure": show_structure,  # show bandstructure
  "show_hoppings": show_hoppings,  # show DOS
  "show_structure_3d": show_structure_3d,
  "show_interactive_ldos": show_interactive_ldos,  # show DOS
  "show_magnetism": show_magnetism,
  "select_atoms_removal": select_atoms_removal,
  "select_atom_time_evolution": select_atom_time_evolution,
  "show_time_evolution": show_time_evolution,
  "show_local_chern": show_local_chern,
})

common.finalize_page(qtwrap,window,signals,inipath)

if __name__ == "__main__":
    window.run() # show this page as its own standalone window and block

