#!/usr/bin/env python3
"""Geometry/island construction for the huge_0d mode.

Split out of huge_0d.py so the (large) KPM/DOS computation and button
handlers in handlers.py aren't mixed in the same file as building the
island geometry. Every function takes qtwrap explicitly (the interfacetk
qtwrap module) rather than relying on module-level globals, matching the
convention used by pysrc/interfacetk/common.py.
"""
from pyqula import geometry, islands, sculpt
import numpy as np
import os
import time


LATTICES_0D = {
  "Honeycomb": geometry.honeycomb_lattice,
  "Square": geometry.square_lattice,
  "Kagome": geometry.kagome_lattice,
  "Lieb": geometry.lieb_lattice,
  "Triangular": geometry.triangular_lattice,
}


def getfile(name):
  """Get the name of the file"""
  return builder.get_object(name).get_filename()


def get_vacancies():
  """Get the value of a certain variable"""
  name = "vacancies" # name of the object
  ats = builder.get_object(name).get_text()
  ats = ats.replace(","," ") # substitute comma by space
  ats = ats.split() # separte bu commas
  ats = [int(float(a)) for a in ats] # convert to int
  return ats # return list


def get_geometry0d(qtwrap,second_call=False):
  """ Create a 0d island"""
  get,getbox = qtwrap.get,qtwrap.getbox
  getactive,modify = qtwrap.is_checked,qtwrap.modify
  t0 = time.perf_counter() # initial time
  lattice_name = getbox("lattice")
  # first create a raw unit cell
  gbulk = LATTICES_0D[lattice_name]()  # build a 2d unit cell
  # now scuplt the geometry
  nf = 1+get("size")   # get the desired size, in float
  if getbox("geometry_mode") == "Positions": # generate a perfect island
    os.system("cp "+getfile("positions_file")+" POSITIONS.OUT")
    g = geometry.read()
    g.center()
    return g
  elif getbox("geometry_mode") == "Recipe": # generate a perfect island
    nedges = int(get("nedges")) # number of edges
    angle = get("rotation")*2.*np.pi/360 # angle to rotate
    g = islands.get_geometry(geo=gbulk,n=nf,nedges=nedges,
                               rot=angle,clean=False)
  elif getbox("geometry_mode") == "Image": # generate from an image
    print("Direction",getfile("image_path"))
    g = sculpt.image2island(getfile("image_path"),gbulk,size=int(nf),color="black")
  else: raise
  # if a precise diameter is wanted, only for the first call
  if getactive("target_diameter") and not second_call:
    diameter = get("desired_diameter")
    ratio = diameter/g.get_diameter() # ratio between wanted and obtained
    print("\nChecking that it has the desired size",ratio)
    if not 0.99<ratio<1.01: # if outside the tolerance
      newsize = round(ratio*float(get("size"))) # new size
      modify("size",newsize) # modify the value
      print("Recalling the geometry with size",newsize)
      return get_geometry0d(qtwrap,second_call=True)
  # clean the island
  g.center() # center the geometry
  print("Total number of atoms =",len(g.r))
  print("Time spent in creating the geometry =",time.perf_counter() - t0)
  if getactive("clean_island"): # if it is cleaned
    g = sculpt.remove_unibonded(g,iterative=True)  # remove single bonded atoms
  return g


def modify_geometry(qtwrap,g):
  """Modify the geometry according to the interface"""
  mtype = qtwrap.getbox("modify_geometry")
  print("Modifying geometry according to",mtype)
  if mtype == "None": return g # do nothing
  elif mtype == "Index":
    return sculpt.remove(g,get_vacancies()) # removes several atoms
  elif mtype=="Choose atoms": # special case
    print("Removing as chosen\n")
    try:
      inds = np.genfromtxt("REMOVE_ATOMS.INFO") # selected atoms
      print("Removed indexes",inds)
    except: return g
    try:
      inds = [int(i) for i in inds] # as integer
    except: inds = [int(inds)]
    try: return sculpt.remove(g,inds) # removes several atoms
    except: return g


def edge_atoms(g,nn=3):
  """Get the edge potential"""
  cs = g.get_connections() # get the connections
  v1 = np.array([int(len(c)<nn) for c in cs]) # check if the atom is on the edge or not
  v = v1
  np.savetxt("EDGE.OUT",np.matrix([g.x,g.y,v]).T) # save
  return v # return the array
