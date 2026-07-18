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
window = qtwrap.main() # this is the main interface


from interfacetk.qh_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries





from interfacetk import interfacetk
modify_geometry = lambda x: interfacetk.modify_geometry(x,qtwrap)
select_atoms_removal = lambda: common.select_atoms_removal(get_geometry,script="ql-remove-atoms-geometry-3d")
pickup_hamiltonian = lambda: common.pickup_hamiltonian(qtwrap,initialize,do_scf=True)

qtwrap.set_combobox("dos_operator",operators.operator_list)


LATTICES = {
  "Cubic": geometry.cubic_lattice,
  "Diamond": geometry.diamond_lattice_minimal,
  "Pyrochlore": geometry.pyrochlore_lattice,
  "Hyperhoneycomb": geometry.hyperhoneycomb_lattice,
}

def get_geometry(modify=True):
  """ Create a 0d island"""
  lattice_name = getbox("lattice") # get the option
  g = LATTICES[lattice_name]() # call the geometry
  g = films.geometry_film(g,int(get("thickness")))
  g = g.supercell(int(get("nsuper")))
  g.real2fractional()
  g.fractional2real()
  g.center()
  if modify: g = modify_geometry(g) # modify the geometry
  return g






def initialize():
  """ Initialize the calculation"""
  def check(name):
    if abs(get(name))>0.0: return True
    else: return False
  g = get_geometry() # get the geometry
  if check("strain"): # custom function
    dfun = get("strain") # get function
    def fun(r1,r2): # function to compute distance
      dr = r1-r2
      dr2 = dr.dot(dr) # distance
      if 0.9<dr2<1.1: 
        if 0.9<abs(dr[2])<1.1: return 1.0 + dfun # first neighbor
        return 1.0
      else: return 0.0
    h = g.get_hamiltonian(fun=fun) # get the Hamiltonian
  else:
    h = g.get_hamiltonian(has_spin=True)
  h.add_zeeman(qtwrap.get_array("exchange")) # Zeeman field
  h.add_sublattice_imbalance(get("mAB"))  # sublattice imbalance
  h.add_rashba(get("rashba"))  # Rashba field
  h.add_antiferromagnetism(get("mAF"))  # AF order
  h.add_crystal_field(qtwrap.get("crystalfield")) 
  h.shift_fermi(get("fermi")) # shift fermi energy
  h.add_kane_mele(get("kanemele")) # intrinsic SOC
  h.add_anti_kane_mele(get("antikanemele")) 
  h.add_haldane(get("haldane")) # intrinsic SOC
  h.add_antihaldane(get("antihaldane")) 
#  h.add_peierls(get("peierls")) # shift fermi energy
  if abs(get("inplaneb"))>0.0:
      h.add_inplane_bfield(b=get("inplaneb"),phi=get("inplaneb_phi"))
  if abs(get("swave"))>0.0: 
      h.add_swave(get("swave")) # s-wave SC
  return h





def special_pairing(h):
    """Create a special pairing function"""
    delta = get("swave") # value
    deltatype = getbox("pairing_type") # type of pairing
    if deltatype=="Uniform":
        h.add_pairing(delta,mode="swave")
    elif deltatype=="One sublattice": # only in one sublattice
        h.add_pairing(delta,mode="swaveA")
    elif deltatype=="sigma_z": # only in one sublattice
        h.add_pairing(delta,mode="swavez")
    elif deltatype=="Haldane": # only in one sublattice
        h.add_pairing(delta,mode="haldane")
    elif deltatype=="AntiHaldane": # only in one sublattice
        h.add_pairing(delta,mode="antihaldane")
    else: raise # not implemented









def show_ldos():
  """Return the LDOS"""
  h = pickup_hamiltonian() # get hamiltonian
  ewin = abs(get("window_ldos"))
  energies = np.linspace(-ewin,ewin,int(get("ne_ldos")))
  delta = get("delta_ldos")
  ldos.slabldos(h,energies=energies,delta=delta,nk=int(get("nk_ldos")))
  execute_script('ql-map2d --input DOSMAP.OUT --xlabel Energy --ylabel "z-position" --zlabel DOS --title "Local DOS"')








def show_structure():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
  execute_script("ql-structure")



def show_structure_3d():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
  execute_script("ql-structure3d POSITIONS.OUT")



def show_kdos():
  h = pickup_hamiltonian()  # get the hamiltonian
  ew = get("ewindow_kdos")
  new = int(get("mesh_kdos")) # scale as kpoints
  energies = np.linspace(-ew,ew,new) # number of ene
  kpath = [[i,0.,0.] for i in np.linspace(0.,1.,new)]
  kdos.surface(h,energies=energies,delta=ew/new,kpath=kpath)
  execute_script("ql-kdos-both KDOS.OUT  ")






def solve_scf():
  """Perform a selfconsistent calculation"""
  scfin = getbox("scf_initialization")
  h = initialize() # initialize the Hamiltonian
  mf = scftypes.guess(h,mode=scfin)
  nk = int(get("nk_scf"))
  U = get("hubbard")
  filling = get("filling_scf")
  filling = filling%1.
  scf = scftypes.selfconsistency(h,nkp=nk,filling=filling,g=U,
                mf=mf,mode="U",smearing=get("smearing_scf"),
                mix = get("mix_scf"))
  scf.hamiltonian.save() # save in a file



def show_magnetism():
  """Show the magnetism of the system"""
  h = pickup_hamiltonian() # get the Hamiltonian
  h.write_magnetization() # write the magnetism
  execute_script("ql-moments")


def save_results():  save_state(inipath,tmppath,window) # function to save
def load_results():  load_state(inipath,tmppath,window) # function to load


# create signals: STANDARD_HANDLERS covers the plain "pickup_hamiltonian
# + common.get_X" buttons automatically; only the buttons with mode-specific
# behavior need to be listed explicitly here
signals = common.wire_standard_signals(qtwrap,pickup_hamiltonian,extra={
  "show_structure": show_structure,  # show bandstructure
  "show_structure_3d": show_structure_3d,  # show bandstructure
  "show_kdos": show_kdos,  # custom mesh_kdos/ewindow_kdos fields
  "show_ldos": show_ldos,  # show DOS
  "show_magnetism": show_magnetism,
  "solve_scf": solve_scf,
  "select_atoms_removal": select_atoms_removal,
  "save_results": save_results,
  "load_results": load_results,
})






window.connect_clicks(signals)
inipath = os.getcwd() # get the initial directory
folder = create_folder()
tmppath = os.getcwd() # get the initial directory
window.run()

