# Add the root path of the pyqula library
import os ; import sys 
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/../../../src")





from pyqula import geometry
from pyqula import heterostructures
import numpy as np
g = geometry.chain()
h = g.get_hamiltonian(has_spin=False)
nc = 10
hc = [h.copy() for i in range(nc)]
ht = heterostructures.build(h,h,central=hc)
h.get_bands() # get bandstructure
es = np.linspace(-3.,3.,50)
ts = [ht.landauer(e) for e in es]

import matplotlib.pyplot as plt
plt.plot(es,ts)
plt.show()

np.savetxt("TRANSPORT.OUT",np.matrix([es,ts]).T)







