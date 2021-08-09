#!/usr/bin/python

from __future__ import print_function

import sys
import os

qlroot = os.path.dirname(os.path.realpath(__file__))+"/../.."
sys.path.append(qlroot+"/pysrc/") # python libraries



import qtwrap # import the library with simple wrappers to qt4
get = qtwrap.get  # get the value of a certain variable
getbox = qtwrap.getbox  # get the value of a certain variable
window = qtwrap.main() # this is the main interface



from qh_interface import * # import all the libraries needed




def get_(modify=True):
  """ Create a 0d island"""
  g = geometry.chain()
  g = 





def initialize():
  """ Initialize the calculation"""
  g = get_geometry() # get the geometry
  h = g.get_hamiltonian(has_spin=False)
  h.add_peierls(get("peierls")) # magnetic field
  h.add_zeeman([get("Bx"),get("By"),get("Bz")]) # Zeeman fields
  h.add_sublattice_imbalance(get("mAB"))  # sublattice imbalance
  if abs(get("rashba")) > 0.0: h.add_rashba(get("rashba"))  # Rashba field
  h.add_antiferromagnetism(get("mAF"))  # AF order
  h.shift_fermi(get("fermi")) # shift fermi energy
  if abs(get("kanemele"))>0.0:  h.add_kane_mele(get("kanemele")) # intrinsic SOC
  if abs(get("haldane"))>0.0:  h.add_haldane(get("haldane")) # intrinsic SOC
  if abs(get("antihaldane"))>0.0:  h.add_antihaldane(get("antihaldane")) 
  if abs(get("swave"))>0.0:  h.add_swave(get("swave")) 
#  h.add_peierls(get("peierls")) # shift fermi energy

  return h








def pickup_hamiltonian():
    return initialize()


def get_sequence(n,dn=0):
    """
    Return the sequence
    """
    n0 = int(n) # integer part
    name = getbox("sequence")
    from pyqula import potentials
    if name=="Fibonacci": seq = potentials.fibonacci(n,n0=n0)
    elif name=="Thue-Morse": seq = potentials.thue_morse(n,n0=n0)
    else: raise
    # now do the interpolation
#    elif name=="Harper-Fibonacci":
#        return potentials.aahf1d(n,n0=n0,beta=get("beta"))





def show_displacement():
    """
    Show the spectrum with a displacement
    """





# create signals
signals = dict()
signals["show_displacement"] = show_displacement  # show displacement



#from qh_interface import create_folder # import all the libraries needed

window.connect_clicks(signals)
folder = create_folder()
tmppath = os.getcwd() # get the initial directory
window.run()

