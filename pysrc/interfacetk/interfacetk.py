import numpy as np


def modify_geometry(g,qtwrap):
  """Modify the geometry according to the interface,
  qtwrap is the specific interface"""
  if qtwrap.is_checked("remove_selected"): # remove some atoms
      try:
        inds = np.array(np.genfromtxt("REMOVE_ATOMS.INFO",dtype=np.int_))
        if inds.shape==(): inds = [inds]
        # a plain list of ints, not the numpy array genfromtxt returns:
        # Geometry.remove() dispatches on type(i)==list, and would wrap
        # an array as a single element instead of iterating it
        inds = [int(i) for i in inds]
      except: inds = [] # Nothing
      print(inds)
      g = g.remove(inds) # remove those atoms
  if qtwrap.is_checked("remove_single_bonded"): # remove single bonds
      g = g.clean(iterative=True)
  return g # return geometry

