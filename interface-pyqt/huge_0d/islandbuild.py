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


def get_geometry0d(qtwrap):
  """ Create a 0d island"""
  get,getbox = qtwrap.get,qtwrap.getbox
  getactive = qtwrap.is_checked
  t0 = time.perf_counter() # initial time
  lattice_name = getbox("lattice")
  # first create a raw unit cell
  gbulk = LATTICES_0D[lattice_name]()  # build a 2d unit cell
  # now scuplt the geometry
  nf = 1+get("island_size")   # get the desired size, in float
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
  # clean the island
  g.center() # center the geometry
  print("Total number of atoms =",len(g.r))
  print("Time spent in creating the geometry =",time.perf_counter() - t0)
  if getactive("clean_island"): # if it is cleaned
    g = g.clean(iterative=True)  # remove single bonded atoms
  return g


def edge_atoms(g,nn=3):
  """Get the edge potential"""
  cs = g.get_connections() # get the connections
  v1 = np.array([int(len(c)<nn) for c in cs]) # check if the atom is on the edge or not
  v = v1
  np.savetxt("EDGE.OUT",np.matrix([g.x,g.y,v]).T) # save
  return v # return the array
