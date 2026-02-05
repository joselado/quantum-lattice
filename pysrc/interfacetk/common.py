from .qlinterface import execute_script
import numpy as np
from pyqula import klist
from .qh_interface import *
from pyqula import parallel

def get_operator(h,opname,projector=False):
    """Return an operator"""
    if opname=="None": op = None # no operators
    elif opname=="Sx": op = h.get_operator("sx") # off plane case
    elif opname=="Berry": op = h.get_operator("berry") # off plane case
    elif opname=="Sy": op = h.get_operator("sy")# off plane case
    elif opname=="Sz": op = h.get_operator("sz")# off plane case
    elif opname=="Valley": op = h.get_operator("valley",projector=projector)
    elif opname=="IPR": op = h.get_operator("ipr")
    elif opname=="y-position": op = h.get_operator("yposition")
    elif opname=="x-position": op = h.get_operator("xposition")
    elif opname=="z-position": op = h.get_operator("zposition")
    elif opname=="Interface": op = h.get_operator("interface")
    elif opname=="Surface": op = h.get_operator("surface")
    elif opname=="Layer": op = h.get_operator("zposition")
    else: op = h.get_operator(opname)
    return op



def get_bands(h,window):
    """Compute the bandstructure of the system"""
    opname = window.getbox("bands_color")
    op = get_operator(h,opname) # get operator
    kpath = klist.default(h.geometry,nk=int(window.get("nk_bands")))
    num_bands = int(window.get("nbands"))
    if num_bands<1: num_bands = None # all the eigenvalues
    check_parallel(window) # check if use parallelization
    if op is None: h = h.reduce() # reduce dimensionality if possible
    h.get_bands(operator=op,kpath=kpath,num_bands=num_bands)
    command = "ql-bands --dim "+str(h.dimensionality) 
    if op is not None: command += " --cblabel "+opname
    execute_script(command) # execute the command




def get_kdos(h,window):
    """Show the KDOS"""
    ew = window.get("kdos_ewindow")
    new = int(window.get("kdos_mesh")) # scale as kpoints
    energies = np.linspace(-ew,ew,new) # number of ene
    kpath = [[i,0.,0.] for i in np.linspace(0.,1.,new)]
    h = h.reduce() # reduce dimensionality if possible
    kdos.surface(h,energies=energies,delta=4*ew/new,kpath=kpath)
    command = "ql-kdos-both --input KDOS.OUT"
    execute_script(command) # execute the script




def get_surface_dos(h,window):
    """Show the KDOS"""
    ew = window.get("sdos_ewindow")
    delta = window.get("sdos_delta")
    new = int(4*ew/delta) # scale as kpoints
    energies = np.linspace(-ew,ew,new) # number of ene
    kpath = [[i,0.,0.] for i in np.linspace(0.,1.,new)]
    h = h.reduce() # reduce dimensionality if possible
    kdos.surface(h,energies=energies,delta=delta)
    command = "ql-sdos --input KDOS.OUT"
    execute_script(command) # execute the script



def show_exchange(h,window):
    """Show the exchange field"""
    nrep = max([int(window.get("magnetization_nrep")),1]) # replicas
    h.write_magnetization(nrep=nrep) # write the magnetism
    execute_script("ql-moments",mayavi=True)


def get_dos(h,window,silent=False):
    nk = max([int(window.get("dos_nk")),1])
    delta = window.get("dos_delta")
    ewindow = abs(window.get("dos_ewindow"))
    energies = np.linspace(-ewindow,ewindow,int(ewindow/delta*5)) # get the energies
    h = h.reduce() # reduce dimensionality of possible
    if window.getbox("dos_mode")=="Green":
      dos.dos(h,delta=delta,nk=nk,energies=energies,mode="Green") # compute DOS
    else:
      dos.dos(h,delta=delta,nk=nk,energies=energies) # compute DOS
    if not silent: execute_script("ql-dos --input DOS.OUT")



def get_berry1d(h,window):
    """Get the one dimensional Berry curvature"""
    ks = klist.default(h.geometry,
            nk=int(window.get("topology_nk")))  # write klist
    opname = window.getbox("topology_operator")
    op = get_operator(h,opname,projector=True) # get operator
    topology.write_berry(h,ks,operator=op)
    command = "ql-berry1d  --label True " 
    if opname!="None": command += " --mode "+opname
    execute_script(command)





def get_berry2d(h,window):
    """Get the Berry curvature"""
    nk = int(np.sqrt(window.get("topology_nk")))
    opname = window.getbox("topology_operator")
    op = get_operator(h,opname,projector=True) # get operator
    topology.berry_map(h,nk=nk,operator=op)
    execute_script("ql-map2d --input BERRY_MAP.OUT --xlabel px --ylabel py --zlabel \Omega --show_cuts False --title 'Berry curvature map'")


def get_kdos_bands(h,window):
    """Get the kdos of the bands"""
    get = window.get
    energies = np.linspace(-get("window_kbands"),get("window_kbands"),int(get("ne_kbands")))
    nk = int(get("ne_ldos"))
    if nk==0: nk = 100 # workaround
    op = window.getbox("operator_kdos") # get the operator
    kdos.kdos_bands(h,scale=get("scale_kbands"),
                 operator=op,
                energies=energies,delta=get("delta_kbands"),
                   ntries=int(get("nv_kbands")),nk=nk)
    if h.dimensionality==2:
        execute_script("ql-dosbands --input KDOS_BANDS.OUT ")
    if h.dimensionality==1:
        execute_script("ql-dosbands1d --input KDOS_BANDS.OUT ")



def get_chern(h,window):
    """Get the Chern number"""
    nk = int(np.sqrt(window.get("topology_nk")))
    opname = window.getbox("topology_operator")
    op = get_operator(h,opname,projector=True) # get operator
    topology.chern(h,nk=nk,operator=op)
    execute_script("ql-chern BERRY_CURVATURE.OUT")

def get_fermi_surface(h,window):
    check_parallel(window) # check if use parallelization
    e = window.get("fs_ewindow")
    energies = np.linspace(-e,e,100)
    nk = int(window.get("fs_nk")) # number of kpoints
    numw = int(window.get("fs_numw")) # number of waves for sparse
    delta = window.get("fs_delta")
    operator = window.getbox("fs_operator")
    h = h.reduce() # reduce dimensionality if possible
    spectrum.multi_fermi_surface(h,nk=nk,energies=energies,
        delta=delta,nsuper=1,numw=numw,operator=operator)
    execute_script("ql-multifermisurface")



def get_qpi(h,window):
    check_parallel(window) # check if use parallelization
    e = window.get("qpi_ewindow")
    energies = np.linspace(-e,e,100)
    nk = int(window.get("qpi_nk")) # number of kpoints
    numw = int(window.get("qpi_numw")) # number of waves for sparse
    delta = window.get("qpi_delta")
    h = h.reduce() # reduce dimensionality if possible
    h.get_qpi(nk=nk,energies=energies,delta=delta) # compute the QPI
    execute_script("ql-multiqpi")









def solve_scf(h,window):
  """Perform a selfconsistent calculation"""
  get = window.get # redefine
#  comp = computing() # create the computing window
  scfin = window.getbox("scf_initialization")
  mf = scftypes.guess(h,mode=scfin)
  nk = int(get("nk_scf"))
  U = get("U")
  V1 = get("V1")
  V2 = get("V2")
  filling = get("filling_scf")
  filling = filling%1. # filling
  extrae = get("extra_electron")
  filling += extrae/h.intra.shape[0] # extra electron
  scf = meanfield.Vinteraction(h,nk=nk,filling=filling,U=U,V1=V1,V2=V2,
                mf=mf,load_mf=False,#T=get("smearing_scf"),
                mix = get("mix_scf"),
                verbose=1
                )
  scf.hamiltonian.save() # save in a file



def add_strain(h,window):
    """Add strain to a Hamiltonian"""
    get = window.get
    if get("strain_strength")!=0.0:
        stype = window.getbox("strain_type")
        if stype=="Radial scalar": # radial scalar
            f0 = potentials.radial_decay
            smode="scalar" # mode of the strain
        elif stype=="Radial vector": # radial scalar
            from pyqula.potentialtk.vectorprofile import radial_vector_decay
            f0 = radial_vector_decay
            smode="non_uniform" # mode of the strain
        else: raise
        fs = f0(v0=1.+get("strain_strength"),
                   voo=1.0,rl=get("strain_decay"))
        h.add_strain(fs,mode=smode)




def get_z2(h,window):
    nk = int(np.sqrt(window.get("topology_nk")))
    topology.z2_vanderbilt(h,nk=nk,nt=nk//2) # calculate z2 invariant
    execute_script("ql-wannier-center  ") # plot the result



def get_multildos(h,window):
    check_parallel(window) # check if use parallelization
    ewin = window.get("multildos_ewindow")
    nrep = int(max([1,window.get("multildos_nrep")]))
    nk = int(max([1,window.get("multildos_nk")]))
    numw = int(window.get("multildos_numw"))
    ne = 100 # 100 points
    delta = window.get("multildos_delta")
    proj = window.getbox("basis_ldos")
    if proj=="Real space atomic orbitals":  projection = "atomic"
    else: projection = "TB" # default one
    h = h.reduce() # reduce dimensionality if possible
    ldos.multi_ldos(h,es=np.linspace(-ewin,ewin,ne),
            nk=nk,delta=delta,nrep=nrep,numw=numw,
            projection=projection,ratomic=window.get("ratomic_ldos"))
    if projection=="TB": execute_script("ql-multildos ")
    else: execute_script("ql-multildos --grid True")



def get_nk(h,delta=1e-2,fac=1.0):
    """Return the number of k-points to be used"""
    n = h.intra.shape[0] # dimension of the Hamiltonian
    d = h.dimensionality # dimensionality
    nk = 1./(delta*n) # number of kpoints
    if d==0: return 0
    elif d==1: return int(nk*fac)
    elif d==2: return int(np.sqrt(nk)*fac)
    elif d==3: return int(nk**(1./3.)*fac)






def check_parallel(qtwrap):
  """Check if there is parallelization"""
  if qtwrap.getbox("use_parallelization") =="Yes":
      parallel.cores = parallel.maxcpu
  else: parallel.cores = 1 # single core



def set_colormaps(form,name,cs=[]):
    """Add the different colormaps to a combox"""
    try: cb = getattr(form,name)
    except: 
     #   print("Combobox",name,"not found")
        return
    cb.clear() # clear the items
    cb.addItems(cs)


def generate_hamiltonian(window,g=None):
    """Generate the Hamiltonian taking as input the geometry"""
    if g is None: raise
    get = window.get # function
    get_array = window.get_array # function
    h = g.get_hamiltonian(has_spin=True,tij=get_array("hoppings"))
    ts = get_array("hoppings")
    h.add_exchange(get_array("exchange")) # Zeeman fields
    h.add_sublattice_imbalance(get("mAB"))  # sublattice imbalance
    h.add_rashba(get("rashba"))  # Rashba field
    h.add_antiferromagnetism(get("mAF"))  # AF order
    h.shift_fermi(get("fermi")) # shift fermi energy
    h.add_kane_mele(get("kanemele")) # intrinsic SOC
    h.add_haldane(get("haldane")) # intrinsic SOC
    h.add_antihaldane(get("antihaldane"))
    h.add_anti_kane_mele(get("antikanemele"))
    if np.abs(get("swave"))>0.0: h.add_swave(get("swave")) # add term
    p = get_array("pwave")
    if np.sum(np.abs(p))>0.0: 
        h.add_pairing(d=get_array("pwave"),mode="triplet",delta=1.0)
    h.turn_dense()
    return h





def initialize(window):
    """Do various initializations"""
    cs = ["RGB","hot","inferno","plasma","bwr","rainbow","gnuplot"]
    set_colormaps(window.form,"bands_colormap",cs=cs) # set the bands
    window.set_combobox("scf_initialization",meanfield.spinful_guesses)
    window.set_combobox("bands_color",operators.operator_list)
#    window.set_combobox("fs_operator",operators.operator_list)
    window.set_combobox("operator_kdos",operators.operator_list)



