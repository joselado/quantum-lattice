from __future__ import print_function,division
import numpy as np
from .ldos import spatial_dos as spatial_density
from scipy.sparse import csc_matrix
import scipy.sparse.linalg as slg
import scipy.linalg as lg
from . import geometry
from . import timing
from . import klist

arpack_tol = 1e-06
arpack_maxiter = 10000


def diagonalize(intra,n=20,e=0.0,mode="arpack"):
  if mode=="arpack":
    eig,eigvec = slg.eigsh(csc_matrix(intra),k=n,which="LM",sigma=e,
                                  tol=arpack_tol,maxiter=arpack_maxiter)
  else:
    eig,eigvec = lg.eigh(csc_matrix(intra).todense())
  return eig,np.transpose(eigvec) # return


def restricted_density(intra,n=20,e=0.0,window=0.1,mode="arpack",
          window_mode="around"):
  (es,ws) = diagonalize(intra,n=n,e=e,mode=mode) # get energies and waves
  d = np.zeros(len(ws[0])) # initialize
  for (ie,iw) in zip(es,ws): # loop
    if window_mode=="around":
      if -window<(ie-e)<window: d = d + np.abs(iw)*np.abs(iw) # add
    elif window_mode=="below":
      if -window<(ie-e)<0.0: d = d + np.abs(iw)*np.abs(iw) # add
    elif window_mode=="above":
      if 0.0<(ie-e)<window: d = d + np.abs(iw)*np.abs(iw) # add
    elif window_mode=="filled":
      if ie<e: d = d + np.abs(iw)*np.abs(iw) # add
    else: raise
  return d # return contribution







def density(h,e=0.0,nk=20,mode="arpack",random=True,num_wf=20,
                window=0.1,nrep=3,name="DENSITY.OUT",
                window_mode="around",kpoints=None):
  """ Calculate the electronic density"""
  if h.intra.shape[0]<100: mode="full"
  if h.dimensionality==0: nk = 1 # single kpoint
  hkgen = h.get_hk_gen() # get generator
  d = np.zeros(h.intra.shape[0]) # initialize
  tr = timing.Testimator("DENSITY")
  from . import klist
  kpoints = klist.kmesh(h.dimensionality,nk=nk)
#  if kpoints is None: 
#    kpoints = [np.random.random(3) for ik in range(nk)]
  nk = len(kpoints) # given at input
  for ik in range(len(kpoints)):
    tr.remaining(ik,nk)
    k = kpoints[ik] # random k-point
    hk = csc_matrix(hkgen(k)) # get Hamiltonian
    d = d + restricted_density(hk,n=num_wf,e=e,window=window,
                   mode=mode,window_mode=window_mode) 
  d /= nk # normalize
  d = spatial_density(h,d) # sum if necessary
  geometry.write_profile(h.geometry,d,name=name,nrep=nrep)
  return d # return density









