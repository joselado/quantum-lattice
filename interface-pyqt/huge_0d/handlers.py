#!/usr/bin/env python3
"""Hamiltonian building and button handlers for the huge_0d mode.

Split out of huge_0d.py; see islandbuild.py for the geometry/island
construction half. Every function takes qtwrap explicitly rather than
relying on module-level globals, matching pysrc/interfacetk/common.py.
"""
from pyqula import hamiltonians, kpm, dos, ldos, sculpt
from interfacetk.qlinterface import execute_script
import numpy as np
import os
import time

import islandbuild


def load_hamiltonian():
  h = hamiltonians.load() # load the Hamiltonian
  return h


def get_numbers(qtwrap,name):
  """Get the values of a certain variable"""
  ats = qtwrap.get(name,string=True)
  ats = ats.replace(","," ") # substitute comma by space
  ats = ats.split() # separte bu commas
  ats = [int(float(a)) for a in ats] # convert to int
  return ats


def initialize(qtwrap):
  """ Initialize the calculation"""
  get = qtwrap.get
  t0 = time.perf_counter()
  os.system("rm SELECTED_ATOMS.INFO") # remove the file for the DOS
  g = islandbuild.get_geometry0d(qtwrap) # get the geometry
  h = hamiltonians.hamiltonian(g) # get the hamiltonian
  h.has_spin = False # spin treatment
  if h.has_spin: # spinful hamiltonian
    print("Spinful hamiltonian, DO NOT USE VERY LARGE ISLANDS!!!")
    h.is_sparse = False
    h.first_neighbors()  # first neighbor hoppin
    h.add_zeeman([get("Bx"),get("By"),get("Bz")]) # Zeeman fields
    if abs(get("rashba")) > 0.0: h.add_rashba(get("rashba"))  # Rashba field
    h.add_antiferromagnetism(get("mAF"))  # AF order
    if abs(get("kanemele"))>0.0:  h.add_kane_mele(get("kanemele")) # intrinsic SOC
    h.shift_fermi(get("fermi")) # shift fermi energy
    h.turn_sparse() # turn it sparse
  else: # spinless treatment
    h.is_sparse = True
    print("Spinless hamiltonian")
    h.first_neighbors()  # first neighbor hopping
  h.add_sublattice_imbalance(get("mAB"))  # sublattice imbalance
  h.add_peierls(get("peierls")) # add magnetic field
  h.add_crystal_field(get("crystalfield")) # add magnetic field
  if get("haldane")!=0.0:
    h.add_haldane(get("haldane")) # add Haldane coupling
  if get("edge_potential")!=0.0: # if there is edge potential
    edgesites = islandbuild.edge_atoms(h.geometry) # get the edge atoms
    h.shift_fermi(get("edge_potential")*edgesites) # add onsites
  print("Time spent in creating the Hamiltonian =",time.perf_counter() - t0)
  h.geometry.write()
  h.save() # save the Hamiltonian


def show_ldos(qtwrap):
  get,modify = qtwrap.get,qtwrap.modify
  h = load_hamiltonian() # get the hmiltonian
  points = int(get("LDOS_polynomials")) # number of polynomials
  x = np.linspace(-.9,.9,int(get("num_ene_ldos"))) # energies
  h.intra = h.intra/6.0 # normalize
  # make the update of the atoms number if SELECTED_ATOMS file exist
  if os.path.isfile("SELECTED_ATOMS.INFO"):
    ind_atoms = open("SELECTED_ATOMS.INFO").read().replace("\n",", ")
    modify("LDOS_num_atom",ind_atoms)
  # now continue in the usual way
  atoms = get_numbers(qtwrap,"LDOS_num_atom")
  ecut = get("energy_cutoff_local_dos")/6.
  os.system("rm LDOS_*") # remove
  for iatom in atoms: # loop over atoms
    if h.has_spin: iatom = iatom*2 # if spinful
    x = np.linspace(-ecut,ecut,int(get("num_ene_ldos")),endpoint=True) # energies
    mus = kpm.local_dos(h.intra,n=points,i=iatom) # calculate moments
    y = kpm.generate_profile(mus,x) # calculate DOS
    x,y = x*6.,y/6. # renormalize
    y = dos.convolve(x,y,delta=get("smearing_local_dos")) # add broadening
    dos.write_dos(x,y) # write dos in file
    fname = "LDOS_"+str(iatom)+".OUT" # name of the file
    os.system("mv DOS.OUT " + fname) # save the file
  execute_script("ql-several-ldos ")


def show_full_spectrum():
  h = load_hamiltonian() # get the hmiltonian
  nmax = 10000
  if h.intra.shape[0]<nmax:
    h.get_bands()
    execute_script("ql-bands0d ")
  else:
    print("Too large Hamiltonian ",nmax)


def show_dos(qtwrap):
  get = qtwrap.get
  h = load_hamiltonian() # get the hmiltonian
  points = int(get("DOS_polynomials")) # number of polynomials
  x = np.linspace(-.9,.9,int(get("num_ene_dos"))) # energies
  h.intra = h.intra/6.0 # normalize
  ntries = int(get("DOS_iterations"))
  t0 = time.perf_counter() # initial time
  mus = kpm.random_trace(h.intra,n=points,ntries=ntries) # calculate moments
  y = kpm.generate_profile(mus,x) # calculate DOS
  x,y = x*6.,y/6. # renormalize
  y = dos.convolve(x,y,delta=get("smearing_dos")) # add broadening
  dos.write_dos(x,y) # write dos in file
  execute_script("ql-dos")
  print("Time spent in Kernel PM DOS calculation =",time.perf_counter() - t0)


def show_spatial_dos(qtwrap):
  get,getbox = qtwrap.get,qtwrap.getbox
  t0 = time.perf_counter()
  h = load_hamiltonian() # get the hamiltonian
  mode_stm = getbox("mode_stm") # get the way the images will be calculated
  delta = get("smearing_spatial_DOS")
  def shot_dos(energy):
    if mode_stm == "Full": # matrix inversion
      ldos.ldos0d(h,e = energy,
                     delta = delta)
    elif mode_stm == "Eigen": # Using Arnoldi
      ldos.ldos0d_wf(h,e = energy,
                     delta = delta,
                     num_wf = int(get("nwaves_dos")),
                     robust=True,tol=delta/1000)
  mode_dosmap = getbox("mode_dosmap") # one shot or video
  if mode_dosmap=="Single shot":
    energy = get("energy_spatial_DOS") # one shot
    shot_dos(energy) # calculate
    print("Time spent in STM calculation =",time.perf_counter() - t0)
    execute_script("ql-fast-ldos LDOS.OUT  ") # using matplotlib
  if mode_dosmap=="Movie": # do a sweep
    energies = np.linspace(get("mine_movie"),get("maxe_movie"),
                               int(get("stepse_movie")))
    fof = open("FRAMES.OUT","w") # file with frames
    for energy in energies:
      print("Calculating",energy)
      shot_dos(energy) # calculate
      name = "ENERGY_"+'{0:.8f}'.format(energy)+"_LDOS.OUT"
      os.system("mv LDOS.OUT "+name) # save the data
      execute_script("ql-silent-ldos "+name) # save the image
      namepng = name+".png" # name of the image
      fof.write(namepng+"\n") # save the name
    fof.close() # close file
    os.system("xdg-open "+namepng) # open the last file


def show_potential(qtwrap):
  g = islandbuild.get_geometry0d(qtwrap) # get the geometry
  islandbuild.edge_atoms(g)
  execute_script("ql-absolute-potential EDGE.OUT  ")


def show_lattice(qtwrap):
  """Show the lattice of the system"""
  g = islandbuild.get_geometry0d(qtwrap) # get the geometry
  g.write()
  print("Structure has been created")
  execute_script("ql-fast-structure  ")


def calculate_path_dos(qtwrap):
  """Calculate all the DOS in a path"""
  get = qtwrap.get
  i0 = int(get("initial_atom"))
  i1 = int(get("final_atom"))
  h = load_hamiltonian() # get the hamiltonian
  r0 = h.geometry.r[i0] # initial point
  r1 = h.geometry.r[i1] # final point
  # now do something dangerous, rotate the geometry to check which
  # atoms to accept
  print("Initial position",r0)
  print("Final position",r1)
  print("Created new rotated geometry")
  gtmp = h.geometry.copy() # copy geometry
  gtmp.shift(r0) # shift the geometry
  gtmp = sculpt.rotate_a2b(gtmp,r1-r0,np.array([1.,0.,0.]))
  # new positions
  r0 = gtmp.r[i0]
  r1 = gtmp.r[i1]
  dr = r1 - r0 # vector between both points
  dy = np.abs(get("width_path")) # width accepted
  dx = np.sqrt(dr.dot(dr))+0.1
  print("Initial ROTATED position",r0)
  print("Final ROTATED position",r1)
  # and every coordinate
  x1,y1 = r0[0],r0[1]
  x2,y2 = r1[0],r1[1]
  ym = (y1+y2)/2. # average y
  def fun(r):
    """Function that decides which atoms to calculate"""
    x0 = r[0]
    y0 = r[1]
    if (x1-dy)<x0<(x2+dy) and np.abs(y0-ym)<dy: return True
    else: return False
  inds = sculpt.intersected_indexes(gtmp,fun) # indexes of the atoms
  fo = open("PATH.OUT","w") # output file
  fo.write("# index of the atom, step in the path, x, y\n")
  ur = dr/np.sqrt(dr.dot(dr)) # unitary vector
  steps = [(gtmp.r[i] - r0).dot(ur) for i in inds] # proyect along that line
  inds = [i for (s,i) in sorted(zip(steps,inds))] # sort by step
  steps = sorted(steps) # sort the steps
  g = h.geometry
  for (i,s) in zip(inds,steps):
    fo.write(str(i)+"    "+str(s)+"   "+str(g.x[i])+"    "+str(g.y[i])+"\n")
  fo.close() # close file


def show_path_dos(qtwrap):
  """Show the the DOS in the path"""
  get = qtwrap.get
  calculate_path_dos(qtwrap) # calculate the path
  h = load_hamiltonian() # get the hmiltonian
  pols = int(get("pols_path")) # number of polynomials
  h.intra = h.intra/6.0 # normalize
  atoms = np.genfromtxt("PATH.OUT").transpose()[0] # indexes
  atoms = [int(a) for a in atoms] # indexes of the atoms
  os.system("rm LDOS_*") # clean all the data
  ecut = np.abs(get("ecut_path")) # maximum energy in path
  if ecut>5.5: ecut = 5.9
  ecut /= 6.0 # to interval 0,1
  for iatom in atoms: # loop over atoms
    print("Calculating DOS in ",iatom)
    if h.has_spin: iatom = iatom*2 # if spinful
    mus = kpm.local_dos(h.intra,n=pols,i=iatom) # calculate moments
    x = np.linspace(-ecut,ecut,int(get("num_ene_path"))) # energies
    y = kpm.generate_profile(mus,x) # calculate DOS
    xout,yout = x*6.,y/6. #renormalize
    yout = dos.convolve(xout,yout,delta=get("smearing_path_dos")) # add broadening
    dos.write_dos(xout,yout) # write dos in file
    fname = "LDOS_"+str(iatom)+".OUT" # name of the file
    os.system("cp DOS.OUT " + fname) # save the file
  execute_script("ql-dos-path  ")


def show_path(qtwrap):
  """Show the path followed in the DOS, when calculating several
  atoms"""
  calculate_path_dos(qtwrap) # calculate the path
  execute_script("ql-path  ")


def show_eigenvalues(qtwrap):
  """Show the eigenvalues"""
  get = qtwrap.get
  h = load_hamiltonian() # get the Hamiltonian
  if h.intra.shape[0]<2000:
    h.get_bands() # get the bandstructure
  else:
    ne = int(get("num_eigenvalues")) # number of eigenvalues
    h.get_bands(num_bands=ne) # get the bandstructure
  execute_script("ql-bands0d")


def clear_removal():
  os.system("rm SELECTED.INFO") # remove the file


def select_atoms():
  execute_script("ql-fast-pick write remove  ") # remove the file


def select_atoms_dos():
  execute_script("ql-fast-pick write  ") # remove the file
