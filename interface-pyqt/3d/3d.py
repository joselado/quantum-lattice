#!/usr/bin/env python3

from __future__ import print_function

import sys
import os

qlroot = os.path.dirname(os.path.realpath(__file__))+"/../.."
sys.path.append(qlroot+"/pysrc/") # python libraries


from interfacetk import qtwrap
get = qtwrap.get  # get the value of a certain variable
getbox = qtwrap.getbox  # get the value of a certain variable
window = qtwrap.new_page(os.path.dirname(os.path.realpath(__file__))) # this mode's page

from interfacetk import scfterms
scfterms.build(qtwrap) # build the Density-density/Spin-spin mean field tabs (with formulas)

from interfacetk.qh_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries

common.initialize(qtwrap) # do several common initializations
qtwrap.set_combobox("dos_operator",operators.operator_list)

pickup_hamiltonian = lambda: common.pickup_hamiltonian(qtwrap,initialize,do_scf=True)


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

def get_geometry():
  """ Create geometry"""
  lattice_name = getbox("lattice") # get the option
  g = LATTICES[lattice_name]() # call the geometry
  nsuper = int(get("nsuper"))
  g = g.supercell(nsuper)
  g.real2fractional()
  g.fractional2real()
  g.center()
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
    h = g.get_hamiltonian(fun) # get the Hamiltonian
  else:
    h = g.get_hamiltonian(has_spin=True)
  j = np.array([get("Bx"),get("By"),get("Bz")])
  h.add_zeeman(j) # Zeeman field
  h.add_sublattice_imbalance(get("mAB"))  # sublattice imbalance
  if check("rashba"): h.add_rashba(get("rashba"))  # Rashba field
  h.add_antiferromagnetism(get("mAF"))  # AF order
  h.shift_fermi(get("fermi")) # shift fermi energy
  if check("kanemele"):  h.add_kane_mele(get("kanemele")) # intrinsic SOC
  if check("haldane"):  h.add_haldane(get("haldane")) # intrinsic SOC
  if check("antihaldane"):  h.add_antihaldane(get("antihaldane")) 
  if check("swave"):  h.add_swave(get("swave")) 
#  h.add_peierls(get("peierls")) # shift fermi energy
  h.turn_dense()
  return h


def show_ldos():
  """Return the LDOS"""
  h = pickup_hamiltonian() # get hamiltonian
  ewin = abs(get("window_ldos"))
  energies = np.linspace(-ewin,ewin,int(get("ne_ldos")))
  delta = get("delta_ldos")
  ldos.slabldos(h,energies=energies,delta=delta,nk=int(get("nk_ldos")))
  execute_script("ql-ldos-slab DOSMAP.OUT  ")






def show_dosbands():
  h = pickup_hamiltonian() # get hamiltonian
  kdos.kdos_bands(h,scale=get("scale_kbands"),ewindow=get("window_kbands"),
                   ne=int(get("ne_kbands")),delta=get("delta_kbands"),
                   ntries=int(get("nv_kbands")))
  execute_script("ql-dosbands --input KDOS_BANDS.OUT ")



def show_dos():
  h = pickup_hamiltonian() # get hamiltonian
  common.get_dos(h,qtwrap)














def show_berry2d():
  h = pickup_hamiltonian() # get hamiltonian
  nk = int(get("nk_topology"))
  topology.berry_map(h,nk=nk)
  execute_script("ql-berry2d BERRY_MAP.OUT")

  
def show_magnetism():
  """Show the magnetism of the system"""
  h = pickup_hamiltonian() # get the Hamiltonian
  h.write_magnetization(nrep=int(get("magnetization_nrep")))
  execute_script("ql-quiver")


def show_structure():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
  execute_script("ql-structure --input POSITIONS.OUT")



def show_structure_3d():
  """Show the lattice of the system"""
  g = get_geometry() # get the geometry
  nsuper = int(get("nsuper_struct"))
  g = g.supercell(nsuper)
  g.write()
  execute_script("ql-structure3d POSITIONS.OUT")




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



def solve_scf():
  """Perform a selfconsistent calculation"""
  scfin = window.getbox("scf_initialization")
  h = initialize() # initialize the Hamiltonian
  mf = scftypes.guess(h,mode=scfin)
  nk = int(get("nk_scf"))
  U = get("U")
  V1 = get("V1")
  V2 = get("V2")
  filling = get("filling_scf")
  filling = filling%1.
  # flavor of the mean field
#  compute_dd = window.is_checked("compute_dd",default=True)
#  compute_anomalous = window.is_checked("compute_anomalous",default=False)
#  compute_cross = window.is_checked("compute_cross",default=True)
#  compute_normal = window.is_checked("compute_normal",default=True)
  error = window.get("scf_error",default=1e-5) # error in the mean field
#  if compute_anomalous: h.add_swave(0.)
  mix = get("mix_scf")
  if h.has_spin: # J1/J2/J3 exchange has no meaning without a spin degree
                 # of freedom - see common.solve_scf, which this mirrors
    J1 = get("J1")
    J2 = get("J2")
    J3 = get("J3")
    scf = meanfield.VJinteraction(h,nk=nk,filling=filling,U=U,V1=V1,V2=V2,
                  J1=J1,J2=J2,J3=J3,
                  mf=mf,mix=mix,maxerror=error,verbose=1,
                  )
  else:
    scf = meanfield.Vinteraction(h,nk=nk,filling=filling,U=U,V1=V1,V2=V2,
                  mf=mf,load_mf=False,
                  mix=mix,maxerror=error,verbose=1,
                  )
  mfname = scf.identify_symmetry_breaking(as_string=True)
  window.set("identified_mean_field",mfname)
  scf.hamiltonian.save() # save in a file







def save_results():  save_state(inipath,tmppath,window) # function to save
def load_results():  load_state(inipath,tmppath,window) # function to load


# create signals: STANDARD_HANDLERS covers the plain "pickup_hamiltonian
# + common.get_X" buttons automatically; only the buttons with mode-specific
# behavior need to be listed explicitly here
signals = common.wire_standard_signals(qtwrap,pickup_hamiltonian,extra={
  "show_structure": show_structure,  # show bandstructure
  "show_structure_3d": show_structure_3d,  # show bandstructure
  "show_magnetism": show_magnetism,
  "solve_scf": solve_scf,
  "save_results": save_results,
  "load_results": load_results,
})





#from qh_interface import create_folder # import all the libraries needed

window.connect_clicks(signals)
common.set_formulas(qtwrap) # Hamiltonian-term formula images + tooltips
common.set_button_tooltips(qtwrap) # hover tooltips on the calculation buttons
inipath = os.getcwd() # get the initial directory
folder = create_folder()
window.scratch_dir = folder # so qtwrap.connect_clicks() can restore this page's cwd before each handler runs
tmppath = os.getcwd() # get the initial directory
if __name__ == "__main__":
    window.run() # show this page as its own standalone window and block

