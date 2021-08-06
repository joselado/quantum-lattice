import numpy as np

def get_dmat():
  """ Create the file DENSITIES.OUT and return densities and magnetization """
  lines = open("hamiltonian.in","r").readlines() # read hamiltonian.in  
  i = 0
  for l in lines:
    i += 1
    if 'DIMENSION_OF_THE_HAMILTONIAN' in l:
      norbitals = int(lines[i]) # get the number of orbitals
  nat = norbitals/2 # number of atoms
  
  nl = len(lines)
  
  # create matrix of the density matrix
  m = np.zeros((norbitals,norbitals),np.complex)
  col = np.genfromtxt("DENSITY_MATRIX.OUT")
  
  # create matrix
  for c in col:
   i = c[0]-1
   j = c[1]-1
   re = c[2]
   im = c[3]
   m[i,j] = re+1j*im
  return m # return the density matrix  
  
  
def create_densities(angle = 0., axis = [1,0,0]):
  """ Creates the spin densities"""
  m = get_dmat() # get the density matrix
  m = rotate_mag(m,angle=angle,axis=axis) # rotate magnetizations
  nat = len(m)/2
  # eigenvactors for the different projections
  mx = np.array([0.0,1.0,1.0,0.0])
  my = np.array([0.0,1j,-1j,0.0])
  mz = np.array([1.0,0.0,0.0,-1.0])
  dd = np.array([1.0,0.0,0.0,1.0])
  
  
  # magnetization of each atom
  mag_ats = []
  den = []
  
  for iat in range(nat):
    ind = iat * 2 
    # vector with the elements of the local field
    mm = np.array([m[ind,ind],m[ind,ind+1],m[ind+1,ind],m[ind+1,ind+1]])
    magx = np.dot(mm,mx).real 
    magy = np.dot(mm,my).real 
    magz = np.dot(mm,mz).real 
    mag_ats += [[magx,magy,magz]]
    den += [np.dot(mm,dd).real] 
  
  
  mag_ats = np.array(mag_ats).transpose()
  inds = [i for i in range(nat)]
   
  # save the magnetization in a file
  fm = open("DENSITIES.OUT","w")
  fm.write("#  Componnents of the magnetization in the different atoms\n")
  fm.write("# index  Den Mx My Mz\n")
  for i in range(nat):
    f = '{0:.8f}'.format
    fm.write(str(i+1)+"  "+f(den[i])+"  "+f(mag_ats[0,i])+"  "+f(mag_ats[1,i])+"  "+f(mag_ats[2,i])+"\n" )
  fm.close()
  return (den,mag_ats)



def rotate_mag(m,angle=0.0,axis=[0,0,1]):
  """ Rotates the magnetization along a particular axis """
  nat = len(m)/2

  #####################
  ## rotate the dmat ##
  #####################
  from scipy.sparse import coo_matrix, bmat
  sx = np.matrix([[0.,1.],[1.,0.]])
  sy = np.matrix([[0.,1j],[-1j,0.]])
  sz = np.matrix([[1.,0.],[0.,-1.]])

  from scipy.linalg import expm
  rmat = expm(1j*np.pi*angle*(axis[0]*sx + axis[1]*sy + axis[2]*sz))
  rmat = coo_matrix(rmat) # to sparse
  rot = [[None for i in range(nat)] for j in range(nat)]
  for i in range(nat):
    rot[i][i] = rmat
  rot = bmat(rot).todense() # rotational matrix

  # rotate the matrix
  m = rot * m * rot.H

  return m 





