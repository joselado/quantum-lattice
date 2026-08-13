from .qlinterface import execute_script, create_folder, save_state, load_state
from . import qtwrap
from . import hamiltoniantype
import os
import numpy as np
from pyqula import klist
from .qh_interface import *
from pyqula import parallel
from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from qfluentwidgets import BodyLabel

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
    delta = window.get("sdos_delta") or 1e-3 # avoid a division by zero below
    new = int(4*ew/delta) # scale as kpoints
    energies = np.linspace(-ew,ew,new) # number of ene
    kpath = [[i,0.,0.] for i in np.linspace(0.,1.,new)]
    h = h.reduce() # reduce dimensionality if possible
    kdos.surface(h,energies=energies,delta=delta)
    command = "ql-sdos --input KDOS.OUT"
    execute_script(command) # execute the script




def show_exchange(h,window):
    """Show the exchange field"""
    # default=5 matches hamiltonians.write_magnetization()'s own default
    # (htk/write.py) - modes with no magnetization_nrep field of their own
    # (2dslab/hybridfilm/hybridribbon/multilayergraphene) must fall back to
    # the same value h.write_magnetization() with no args would use
    nrep = max([int(window.get("magnetization_nrep",default=5)),1]) # replicas
    h.write_magnetization(nrep=nrep) # write the magnetism
    if window.getbox("magnetization_plot_mode")=="2D":
        execute_script("ql-magnetism2d")
    else: # 3D mode
        execute_script("ql-moments")


def get_dos(h,window,silent=False):
    nk = max([int(window.get("dos_nk")),1])
    delta = window.get("dos_delta") or 1e-3 # avoid a division by zero below
    ewindow = abs(window.get("dos_ewindow"))
    energies = np.linspace(-ewindow,ewindow,int(ewindow/delta*5)) # get the energies
    h = h.reduce() # reduce dimensionality of possible
    opname = window.getbox("dos_operator") # operator to project the DOS onto
    op = get_operator(h,opname) if opname else None
    mode = window.getbox("dos_mode")
    if mode=="Green":
      dos.dos(h,delta=delta,nk=nk,energies=energies,mode="Green",operator=op) # compute DOS
    elif mode=="KPM":
      dos.dos(h,delta=delta,nk=nk,energies=energies,use_kpm=True,operator=op) # compute DOS
    else:
      dos.dos(h,delta=delta,nk=nk,energies=energies,operator=op) # compute DOS
    if not silent: execute_script("ql-dos --input DOS.OUT")



def get_site_dos(h,window,use_kpm=False):
    """Open the interactive Site DOS view: a geometry subplot on the
    left (click a site, or drag a lasso to select several at once - the
    same LassoSelector engine as the "Select atoms to remove" picker)
    and a DOS subplot on the right, recomputed on every selection change
    - see utilities/ql-site-dos. The DOS itself has to be (re)computed
    inside that subprocess, in response to its own matplotlib
    pick_event/lasso callback, so what's handed off here is the built
    Hamiltonian (pickled) rather than a single precomputed DOS.OUT.
    use_kpm picks the diagonalization method: KPM for the modes whose
    Hamiltonians are too large for exact diagonalization (huge_0d, tbg,
    hofstader1d - wired with use_kpm=True in their own <mode>.py), ED
    (the dos.dos default) for every other mode."""
    # a dedicated filename, not the "hamiltonian.pkl" default: that one is
    # pickup_hamiltonian()'s canonical SCF result (written by
    # scf.hamiltonian.save() above), and this handler runs regardless of
    # whether "do_scf" is checked - saving over the default here would
    # silently clobber the converged SCF Hamiltonian with a fresh one
    hfile = "SITE_DOS_HAMILTONIAN.pkl"
    h.save(hfile) # loaded back by ql-site-dos
    ewindow = abs(window.get("site_dos_ewindow"))
    delta = window.get("site_dos_delta") or 1e-3 # avoid a division by zero below
    nk = max([int(window.get("site_dos_nk")),1])
    command = "ql-site-dos --hamiltonian "+hfile+" --ewindow "+str(ewindow)+" --delta "+str(delta)+" --nk "+str(nk)
    if use_kpm: command += " --kpm True"
    execute_script(command)


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
    nk = int(get("nk_kbands",default=100))
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



def get_iets_qdos(h,window):
    """Get the momentum-resolved inelastic (spin-flip) response, i.e. the
    RPA spin-excitation dispersion along a q-path - the magnetic analog of
    get_kdos_bands. Needs a mean-field Hamiltonian with an onsite H.V
    (converged via "Solve SCF" with do_scf checked) - pyqula raises if H.V
    is missing or has non-onsite (V1/V2/J-neighbor) support."""
    get = window.get
    energies = np.linspace(0.,get("window_iets"),int(get("ne_iets")))
    nq = int(get("nq_iets"))
    qout,es,chimap = h.get_qdos_iets(energies=energies,nq=nq,
                nk=int(get("nk_iets")),delta=get("delta_iets"))
    fo = open("IETS_QDOS.OUT","w") # open file
    for iq in range(len(chimap)): # loop over q-points
      for (ie,ce) in zip(es,chimap[iq]): # loop over energies
        fo.write(str(iq/len(chimap))+"   ")
        fo.write(str(ie)+"   ")
        fo.write(str(ce)+"\n")
      fo.flush()
    fo.close()
    if h.dimensionality==1:
        execute_script("ql-dosbands1d --input IETS_QDOS.OUT --title 'IETS (momentum-resolved)'")
    else:
        execute_script("ql-dosbands --input IETS_QDOS.OUT --zlabel 'Im \\chi' --title 'IETS (momentum-resolved)'")




def get_iets_ldos(h,window):
    """Get the real-space inelastic (spin-flip) response over a range of
    energies, all computed in a single call (h.get_iets_ldos accepts an
    energy array) - the 0d (finite system) analog of get_iets_qdos, since
    a 0d system has no Brillouin zone to scan a q-path over. Mirrors
    get_multildos: reuses ql-multildos's spatial-map-next-to-total-curve
    viewer (with an energy slider) instead of a single-energy snapshot, by
    writing the same MULTILDOS/ folder layout multi_ldos_tb writes (see
    pyqula/ldos.py) by hand - there is no pyqula "multi-energy IETS"
    helper to call, and pysrc/pyqula/ is vendored/black-box so one isn't
    added there. Needs a mean-field Hamiltonian with an onsite H.V, same
    requirement as get_iets_qdos above."""
    get = window.get
    ewin = get("window_iets")
    delta = get("delta_iets")
    ne = 100 # match get_multildos's fixed energy count
    energies = np.linspace(-ewin,ewin,ne)
    r,ds = h.get_iets_ldos(e=energies,delta=delta) # (ne,nsites), all energies at once
    fs.rmdir("MULTILDOS") # remove any previous folder
    fs.mkdir("MULTILDOS") # create folder
    fo = open("MULTILDOS/MULTILDOS.TXT","w") # names of the per-energy files
    for (e,d) in zip(energies,ds): # loop over energies
        name0 = "LDOS_"+str(e)+"_.OUT"
        ldos.write_ldos(r[:,0],r[:,1],d,output_file="MULTILDOS/"+name0)
        fo.write(name0+"\n")
    fo.close()
    total = np.array([np.sum(d) for d in ds]) # total (site-summed) IETS vs energy
    dos.write_dos(energies,total,output_file="MULTILDOS/DOS.OUT")
    execute_script("ql-multildos --title 'Real-space IETS' --zlabel 'Im \\chi' "
                   "--dlabel 'Total IETS' --dtitle 'Total IETS vs energy'")




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









# VJinteraction's use_jax=True path names its solvers "linear_mixing"/
# "error_gradient" (its public, physically-descriptive names - see
# pysrc/pyqula/selfconsistency/spinspin.py's docstring) and passes
# "newton_krylov" straight through unchanged (not one of its renamed pair);
# Vinteraction's own use_jax=True path (densitydensity_jax.py) still uses
# the older internal names "fixed_point"/"lbfgs" for the same two renamed
# algorithms, but likewise accepts "newton_krylov" verbatim - translated
# here rather than in pyqula, since VJinteraction and Vinteraction are two
# different upstream entry points that happen to expose the same solvers
# under different names. The dropdown's own "krylov" is friendlier than
# either upstream spelling, so both paths need it translated to
# "newton_krylov".
_VJINTERACTION_SOLVER_NAMES = {"krylov": "newton_krylov"}
_VINTERACTION_SOLVER_NAMES = {"error_gradient": "lbfgs", "linear_mixing": "fixed_point",
                               "krylov": "newton_krylov"}

def get_scf_solver_kwargs(h,window,for_vjinteraction):
    """use_jax=True/solver=.../maxite=... kwargs for the SCF solver
    dropdown + max-iterations field, or {} when the solver choice doesn't
    apply. use_jax=True only supports a normal-state (has_eh=False)
    Hamiltonian, and needs the optional jax extra installed (`pip install
    pyqula[jax]`) - a BdG Hamiltonian (swave/pwave pairing added in
    generate_hamiltonian) or a missing jax both silently fall back to the
    existing plain-mixing behavior instead of raising, since the dropdown
    offers no "default" option to fall back to explicitly. maxite is
    always returned (independent of jax/pairing) since it's honored by
    both the jax and plain-mixing SCF loops."""
    maxite = int(window.get("scf_maxite",default=100))
    if h.has_eh: return dict(maxite=maxite)
    import importlib.util
    if importlib.util.find_spec("jax") is None: return dict(maxite=maxite) # optional extra, not installed
    solver = window.getbox("scf_solver")
    if for_vjinteraction: solver = _VJINTERACTION_SOLVER_NAMES.get(solver,solver)
    else: solver = _VINTERACTION_SOLVER_NAMES[solver]
    return dict(use_jax=True,solver=solver,maxite=maxite)


def _scf_has_pairing(qtwrap):
    """Whether the Hamiltonian this page currently describes will end up
    with has_eh=True - mirrors the h.has_eh check get_scf_solver_kwargs()
    makes on a real Hamiltonian, but computed without one (raw form state
    only), for pyqula_code_scf_block() below (which runs before any
    Hamiltonian is actually built). True whenever "Nambu" is selected
    (generate_hamiltonian()/every mode's initialize() unconditionally call
    h.setup_nambu_spinor() under Nambu, setting has_eh=True even with
    swave/pwave both left at zero - see hamiltoniantype.py), or a
    lattice-restricted/non-hamiltoniantype-aware mode still has a nonzero
    swave/pwave field (the pre-hamiltoniantype fallback, kept for modes
    without a hamiltonian_type combobox)."""
    if hamiltoniantype.wants_nambu(qtwrap): return True
    form = qtwrap.form
    for name in ("swave","pwave"):
        field = getattr(form,name,None)
        if field is not None and termhighlight.is_nonzero_value(field.text()):
            return True
    return False


def pyqula_code_scf_block(qtwrap,richer=False):
    """Return the lines of pyqula code that reproduce the mean-field solve
    a "Solve SCF" click would run right now, for codeview.py's "pyqula
    code" tab (called from a mode's own get_pyqula_code() when the SCF
    switch is on) - a literal mirror of solve_scf() above (richer=False,
    used by 0d.py/1d.py, which call this file's own solve_scf()) or of
    2d.py's own richer solve_scf() (richer=True: passes maxerror=<scf_error>
    instead of T=<smearing_scf>, and has no extra_electron term in its
    filling). Branches on hamiltoniantype.wants_spin(qtwrap) the same way
    solve_scf() branches on h.has_spin - meanfield.VJinteraction(...) for a
    spinful Hamiltonian (J1/J2/J3 included, for_vjinteraction=True for the
    solver-name translation below), meanfield.Vinteraction(...) for a
    spinless one (no J1/J2/J3 - VJinteraction itself refuses a spinless h -
    plus load_mf=False, matching solve_scf()'s else branch)."""
    get = qtwrap.get
    getbox = qtwrap.getbox
    has_spin = hamiltoniantype.wants_spin(qtwrap)
    lines = []
    lines.append("")
    lines.append("# --- self-consistent mean field (SCF) ---")
    lines.append("from pyqula import meanfield, scftypes")
    lines.append("mf = scftypes.guess(h, mode=%r)" % getbox("scf_initialization"))
    lines.append("filling = %r %% 1." % get("filling_scf"))
    if not richer:
        lines.append("filling += %r / h.intra.shape[0]" % get("extra_electron"))
    kwargs = [
      "nk=%d" % int(get("nk_scf")), "filling=filling",
      "U=%r" % get("U"), "V1=%r" % get("V1"), "V2=%r" % get("V2"),
    ]
    if has_spin:
        kwargs += ["J1=%r" % get("J1"), "J2=%r" % get("J2"), "J3=%r" % get("J3")]
    kwargs.append("mf=mf")
    if not has_spin: kwargs.append("load_mf=False")
    kwargs.append("mix=%r" % get("mix_scf"))
    if richer: kwargs.append("maxerror=%r" % get("scf_error",default=1e-5))
    else: kwargs.append("T=%r" % get("smearing_scf"))
    kwargs.append("verbose=1")
    kwargs.append("maxite=%d" % int(get("scf_maxite",default=100)))
    import importlib.util
    if importlib.util.find_spec("jax") is not None and not _scf_has_pairing(qtwrap):
        kwargs.append("use_jax=True")
        names = _VJINTERACTION_SOLVER_NAMES if has_spin else _VINTERACTION_SOLVER_NAMES
        solver = names.get(getbox("scf_solver"),getbox("scf_solver"))
        kwargs.append("solver=%r" % solver)
    lines.append("scf = meanfield.%s(h," % ("VJinteraction" if has_spin else "Vinteraction"))
    lines.append("    " + ", ".join(kwargs) + ")")
    lines.append("scf.hamiltonian.save()")
    return lines


def solve_scf(h,window):
  """Perform a selfconsistent calculation"""
  get = window.get # redefine
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
  mix = get("mix_scf")
  T = get("smearing_scf") # thermal smearing of the SCF loop's occupations
  if h.has_spin: # J1/J2/J3 exchange has no meaning without a spin degree
                 # of freedom - meanfield.VJinteraction itself refuses a
                 # spinless h (returns NotImplemented), so route those to
                 # the plain density-density solver below instead
    J1 = get("J1")
    J2 = get("J2")
    J3 = get("J3")
    scf = meanfield.VJinteraction(h,nk=nk,filling=filling,U=U,V1=V1,V2=V2,
                  J1=J1,J2=J2,J3=J3,
                  mf=mf,mix=mix,T=T,verbose=1,
                  **get_scf_solver_kwargs(h,window,for_vjinteraction=True)
                  )
  else:
    scf = meanfield.Vinteraction(h,nk=nk,filling=filling,U=U,V1=V1,V2=V2,
                  mf=mf,load_mf=False,T=T,
                  mix=mix,
                  verbose=1,
                  **get_scf_solver_kwargs(h,window,for_vjinteraction=False)
                  )
  # write atomically (temp name + os.replace): pickup_hamiltonian() treats
  # os.path.exists("hamiltonian.pkl") as "a valid cached solve exists", so a
  # solve killed mid-write (e.g. a cancelled subprocess-based calculation -
  # see qtwrap.run_calculation_subprocess()) must never leave a half-written
  # file there for the next click to mistake for one. os.replace() is an
  # atomic overwrite on both POSIX and Windows, unlike os.rename().
  scf.hamiltonian.save(output_file="hamiltonian.pkl.tmp")
  os.replace("hamiltonian.pkl.tmp","hamiltonian.pkl")
  mark_scf_solved(window)


def solve_scf_identify_symmetry_breaking(h,window):
  """Perform a selfconsistent calculation, converging on a maxerror
  threshold (the "SCF error" field) rather than solve_scf()'s thermal
  smearing, then identify and report the broken symmetry - used by 2d.py
  and 3d.py, which need this richer variant instead of plain solve_scf()."""
  scfin = window.getbox("scf_initialization")
  get = window.get # redefine
  mf = scftypes.guess(h,mode=scfin)
  nk = int(get("nk_scf"))
  U = get("U")
  V1 = get("V1")
  V2 = get("V2")
  filling = get("filling_scf")
  filling = filling%1.
  error = get("scf_error",default=1e-5) # error in the mean field
  mix = get("mix_scf")
  if h.has_spin: # J1/J2/J3 exchange has no meaning without a spin degree
                 # of freedom - see solve_scf(), which this mirrors
    J1 = get("J1")
    J2 = get("J2")
    J3 = get("J3")
    scf = meanfield.VJinteraction(h,nk=nk,filling=filling,U=U,V1=V1,V2=V2,
                  J1=J1,J2=J2,J3=J3,
                  mf=mf,mix=mix,maxerror=error,verbose=1,
                  **get_scf_solver_kwargs(h,window,for_vjinteraction=True)
                  )
  else:
    scf = meanfield.Vinteraction(h,nk=nk,filling=filling,U=U,V1=V1,V2=V2,
                  mf=mf,load_mf=False,
                  mix=mix,maxerror=error,verbose=1,
                  **get_scf_solver_kwargs(h,window,for_vjinteraction=False)
                  )
  mfname = scf.identify_symmetry_breaking(as_string=True)
  window.modify("identified_mean_field",mfname) # window is the qtwrap
                 # module here (not a page object), so this must go
                 # through modify() rather than a page's .set() method
  # write atomically - see solve_scf()'s comment for why
  scf.hamiltonian.save(output_file="hamiltonian.pkl.tmp")
  os.replace("hamiltonian.pkl.tmp","hamiltonian.pkl")
  mark_scf_solved(window)


def mark_scf_solved(qtwrap):
    """Call right after any solve_scf implementation - solve_scf() or
    solve_scf_identify_symmetry_breaking() - saves its converged
    Hamiltonian. Clears page._scf_dirty so pickup_hamiltonian() knows the
    cached result is still valid for the current parameters and won't
    silently re-solve on the next click."""
    page = qtwrap._current_page()
    if hasattr(page,"_scf_dirty"): page._scf_dirty = False



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
        else: raise ValueError("Unknown strain_type: %r" % stype)
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



def get_interactive_ldos(h,window):
    """Open the interactive multi-energy LDOS view (window_ldos/nsuper_ldos/
    nk_ldos/ne_ldos/delta_ldos fields) - shared by hofstader1d/hybridribbon/
    multilayergraphene, whose per-mode files used to carry this verbatim.
    Not the same field convention as get_multildos() above (multildos_*,
    used by 0d/huge_0d/tbg), so kept as a separate function rather than
    merged into it."""
    ewin = window.get("window_ldos")
    nrep = int(window.get("nsuper_ldos"))
    nk = int(window.get("nk_ldos"))
    ne = int(window.get("ne_ldos"))
    delta = window.get("delta_ldos")
    ldos.multi_ldos(h,es=np.linspace(-ewin,ewin,ne),nk=nk,delta=delta,nrep=nrep)
    execute_script("ql-multildos ")


def get_nk(h,delta=1e-2,fac=1.0):
    """Return the number of k-points to be used"""
    delta = delta or 1e-3 # avoid a division by zero below
    n = h.intra.shape[0] # dimension of the Hamiltonian
    d = h.dimensionality # dimensionality
    nk = 1./(delta*n) # number of kpoints
    if d==0: return 0
    elif d==1: return int(nk*fac)
    elif d==2: return int(np.sqrt(nk)*fac)
    elif d==3: return int(nk**(1./3.)*fac)


def build_embedding_hamiltonian(g,window):
    """Build the spinful Hamiltonian from geometry g for the embedding
    modes - shared by impurity_embedding/ribbon_embedding, whose
    initialize() used to carry this verbatim (only get_geometry() and
    LATTICES differ between the two modes)"""
    get = window.get
    h = g.get_hamiltonian(has_spin=True)
    h.add_zeeman(window.get_array("exchange")) # Zeeman fields
    h.add_sublattice_imbalance(get("mAB"))  # sublattice imbalance
    h.add_rashba(get("rashba"))  # Rashba field
    h.add_antiferromagnetism(get("mAF"))  # AF order
    h.shift_fermi(get("fermi")) # shift fermi energy
    h.add_kane_mele(get("kanemele")) # intrinsic SOC
    h.add_haldane(get("haldane")) # intrinsic SOC
    h.add_antihaldane(get("antihaldane"))
    h.add_anti_kane_mele(get("antikanemele"))
    if get("swave")!=0.: h.add_swave(get("swave"))
    p = window.get_array("pwave")
    if np.sum(np.abs(p))>0.0:
        h.add_pairing(d=p,mode="triplet",delta=1.0)
    return h


def get_impurity_matrix(h0,window):
    """Get the impurity matrix: shared by impurity_embedding/ribbon_embedding,
    whose per-mode files used to carry this verbatim"""
    get = window.get
    n = int(get("nsuper_impurity")) # supercell for the impurities
    if n>1: h0 = h0.supercell(n) # create the supercell
    h = h0.copy()*0. # initialize
    v = get("impurity_potential") # (additional) potential in this site
    jv = window.get_array("impurity_exchange") # (additional) Zeeman field
    from pyqula import potentials
    pot_ons = 0. # initialize
    pot_j = 0. # initialize
    try: # many impurities
        inds = np.genfromtxt("IMPURITY_SITES.OUT") # read the indexes
        if inds.shape==(): inds = [inds] # just one number
        print(inds)
    except: inds = [0] # just the first site
    for i in inds:
        i = int(i) # to integer
        imp_ons = potentials.impurity(h.geometry.r[i],v=v) # onsite
        imp_j = potentials.impurity(h.geometry.r[i],v=jv) # exchange
        pot_ons = pot_ons + imp_ons # add contribution
        pot_j = pot_j + imp_j # add contribution
    h.add_onsite(pot_ons) # add the onsite
    h.add_exchange(pot_j) # add the exchange
    return h+h0 # return the defective Hamiltonian


def get_embedding_ldos(h,window):
    """Embed the impurity matrix and compute/plot the LDOS - shared by
    impurity_embedding/ribbon_embedding"""
    get = window.get
    vintra = get_impurity_matrix(h,window)
    ns0 = int(get("nsuper_impurity")) # supercell of the impurity
    eb = embedding.Embedding(h,m=vintra,nsuper=ns0)
    e = get("energy_embedding_ldos") # energy
    delta = get("delta_embedding_ldos") # energy
    ns = int(get("ncells_embedding_ldos"))
    nks = get("nk_scaling_embedding_ldos")
    nk = get_nk(h,delta=delta,fac=20*nks) # number of kpoints
    (x,y,d) = eb.ldos(nsuper=ns,energy=e,delta=delta,nk=nk)
    np.savetxt("LDOS.OUT",np.array([x,y,d]).T)
    execute_script("ql-ldos --input LDOS.OUT")


def get_embedding_ldos_sweep(h,window):
    """Embed the impurity matrix and compute/plot a multi-energy LDOS sweep -
    shared by impurity_embedding/ribbon_embedding"""
    get = window.get
    vintra = get_impurity_matrix(h,window)
    ns0 = int(get("nsuper_impurity")) # supercell of the impurity
    eb = embedding.Embedding(h,m=vintra,nsuper=ns0)
    ewin = get("energy_window_embedding_ldos_sweep") # energy
    ne = int(get("num_energies_embedding_ldos_sweep")) # energy
    es = np.linspace(-ewin,ewin,ne,endpoint=True) # number of energies
    delta = get("delta_embedding_ldos_sweep") # energy
    ns = int(get("ncells_embedding_ldos_sweep"))
    nks = int(get("nk_scaling_embedding_ldos_sweep"))
    nk = get_nk(h,delta=delta,fac=20*nks) # number of kpoints
    eb.multildos(es=es,delta=delta,nk=nk,nsuper=ns) # compute
    execute_script("ql-multildos ")


def select_impurity_sites(g,window):
    """Launch the atom-picker for impurity sites on geometry g - shared by
    impurity_embedding/ribbon_embedding"""
    n = int(window.get("nsuper_impurity")) # supercell for the impurities
    g = g.supercell(n) # supercell
    np.savetxt("POSITIONS_PP.OUT",np.array(g.r)) # write in file
    # select the sites
    execute_script("ql-select-atoms-geometry  --input POSITIONS_PP.OUT --output IMPURITY_SITES.OUT --initially_selected \"0\"  --caption \" Sites with impurities\"")




def pickup_hamiltonian(qtwrap,initialize,do_scf=False,solve=None):
    """Return the working Hamiltonian: if do_scf is enabled for this mode
    and the SCF switch (scfterms.py's "do_scf") is on, (re)run the SCF
    solve first when nothing has been solved yet this session or a
    Hamiltonian-affecting parameter changed since the last solve
    (page._scf_dirty, set by scfterms.py's dirty tracking), then return
    the saved mean-field result - so the user doesn't have to remember to
    click "Solve SCF" by hand every time a term changes. Otherwise build
    fresh every time, as before.

    `solve`, if given, is the mode's own zero-arg "Solve SCF" button
    handler (it calls initialize() itself) - pass it so an automatic
    solve triggered here runs the exact same code a manual click would,
    which matters for 2d.py/3d.py: their own solve_scf() differs from
    this file's solve_scf() (adds maxerror/identify_symmetry_breaking), so
    defaulting to this file's version here would silently give a
    different (and overwrite an already-converged) result for those two
    modes. Falls back to this file's own solve_scf() if not given."""
    if do_scf and qtwrap.is_checked("do_scf"):
        page = qtwrap._current_page()
        if getattr(page,"_scf_dirty",True) or not os.path.exists("hamiltonian.pkl"):
            if solve is not None: solve()
            else: solve_scf(initialize(),qtwrap)
        return hamiltonians.load() # load the Hamiltonian
    return initialize() # generate from scratch



# Button name -> common.get_*(h,window) routine, for the handlers whose
# body is nothing but "h = pickup_hamiltonian(); common.get_X(h,qtwrap)"
# in every mode that uses them. wire_standard_signals() below only wires
# a button through this table when the mode hasn't supplied its own
# implementation in extra={}, so modes with a genuinely different
# calculation behind the same button name (e.g. 3d/hybridribbon's
# show_berry1d, which reads different UI fields) are unaffected.
STANDARD_HANDLERS = {
    "show_bands": get_bands,
    "show_dos": get_dos,
    "show_kdos": get_kdos,
    "show_dosbands": get_kdos_bands,
    "show_iets_qdos": get_iets_qdos,
    "show_iets_ldos": get_iets_ldos,
    "show_berry1d": get_berry1d,
    "show_berry2d": get_berry2d,
    "show_z2": get_z2,
    "show_chern": get_chern,
    "show_fermi_surface": get_fermi_surface,
    "show_qpi": get_qpi,
    "show_multildos": get_multildos,
    "show_site_dos": get_site_dos, # ED by default; overridden to KPM in extra={} for huge_0d/tbg/hofstader1d
}


def wire_standard_signals(qtwrap,pickup_hamiltonian,extra=None):
    """Build a signals dict for window.connect_clicks(): every button
    listed in STANDARD_HANDLERS that exists on this window is wired to
    the matching common.get_*(h,qtwrap) routine, using the mode's own
    pickup_hamiltonian to build h. extra (mode-specific handlers, e.g.
    get_geometry-dependent ones or a button with non-standard behavior)
    is applied last and always wins over the standard wiring."""
    signals = dict()
    for name,fn in STANDARD_HANDLERS.items():
        if hasattr(qtwrap.form,name):
            signals[name] = (lambda fn=fn: fn(pickup_hamiltonian(),qtwrap))
    if extra: signals.update(extra)
    return signals


def finalize_page(qtwrap,window,signals,inipath,robust=True):
    """Standard <mode>.py footer, called once signals is fully built:
    create this page's own scratch folder, wire the shared Save/Load
    Results buttons (every mode calls save_state/load_state identically -
    only wired if this page actually has those buttons), set the
    Hamiltonian-term formulas/tooltips, and connect every button. Every
    mode used to repeat this sequence by hand, byte-for-byte identical
    apart from `robust`.

    `inipath` is the directory the mode was launched from - callers must
    capture it themselves with os.getcwd() *before* calling this (the
    create_folder() below chdirs away from it), since a few modes also
    display it directly (e.g. impurity_embedding's info_tab) and so
    already keep their own copy rather than reading it back out of here."""
    folder = create_folder()
    window.scratch_dir = folder # so qtwrap.connect_clicks() can restore this page's cwd before each handler runs
    tmppath = os.getcwd() # get the initial directory
    signals = dict(signals)
    if hasattr(window,"save_results"):
        signals.setdefault("save_results",lambda: save_state(inipath,tmppath,window))
    if hasattr(window,"load_results"):
        signals.setdefault("load_results",lambda: load_state(inipath,tmppath,window))
    set_formulas(qtwrap) # Hamiltonian-term formula images + tooltips
    window.connect_clicks(signals,robust=robust)
    set_button_tooltips(qtwrap) # hover tooltips on the calculation buttons
    set_calculation_formulas(qtwrap) # formula images on the calculation buttons
    set_param_tooltips(qtwrap) # hover tooltips on the other form fields



def select_atoms_removal(get_geometry,script="ql-remove-atoms-geometry"):
    """Write the unmodified geometry and launch the picker script so the
    user can build REMOVE_ATOMS.INFO for modify_geometry to consume"""
    g = get_geometry(modify=False) # get the unmodified geometry
    g.write() # write geometry
    execute_script(script)
    # sculpting the geometry changes the Hamiltonian modify_geometry()
    # will build next, even though no form field/signal fires for it -
    # invalidate any cached SCF result so it gets recomputed on next use
    page = qtwrap._current_page()
    if hasattr(page,"_scf_dirty"): page._scf_dirty = True



def write_unit_cell(g):
    """Write g's lattice vectors to CELL.OUT, before any --nsuper repetition
    is applied for the on-screen view. The ql-structure-* scripts read this
    (alongside DIMENSIONALITY.OUT, written the same way) to outline the
    primitive unit cell on top of the (possibly enlarged) plotted structure."""
    from pyqula.geometrytk.write import write_lattice
    write_lattice(g,output_file="CELL.OUT")


def _write_and_plot_structure(qtwrap,get_geometry,script):
    """geometry->CELL.OUT->supercell->POSITIONS.OUT->script sequence shared
    by show_structure()/show_structure_3d() below - only the plotting
    `script` itself ever differs between modes (or between the 2D/3D view
    of the same mode)."""
    g = get_geometry() # get the geometry
    write_unit_cell(g) # primitive cell, before the --nsuper repetition
    nsuper = int(qtwrap.get("nsuper_struct"))
    g = g.supercell(nsuper)
    g.write()
    execute_script(script)


def show_structure(qtwrap,get_geometry,script="ql-structure-bond --input POSITIONS.OUT"):
    """Show the lattice of the system"""
    _write_and_plot_structure(qtwrap,get_geometry,script)


def show_structure_3d(qtwrap,get_geometry,script="ql-structure3d POSITIONS.OUT"):
    """Show the lattice of the system in 3D"""
    _write_and_plot_structure(qtwrap,get_geometry,script)



def check_parallel(qtwrap):
  """Set pyqula's core count from the shell-wide serial/parallel switch
  (see qtwrap.set_parallel_execution) - a single process-wide setting
  shared by every mode, rather than a per-mode widget."""
  if qtwrap.is_parallel_execution():
      parallel.set_cores(os.cpu_count())
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
    if g is None: raise ValueError("generate_hamiltonian() needs a geometry (g=...)")
    get = window.get # function
    get_array = window.get_array # function
    has_spin = hamiltoniantype.wants_spin(window)
    h = g.get_hamiltonian(has_spin=has_spin,tij=get_array("hoppings"))
    ts = get_array("hoppings")
    if has_spin: # exchange/kanemele/anti_kane_mele/rashba/antiferromagnetism
        # all unconditionally call turn_spinful() themselves before even
        # looking at the value passed in - see hamiltoniantype.py's
        # docstring - so these must be skipped outright for "Spinless",
        # not just called with a zero-ish value
        h.add_exchange(get_array("exchange")) # Zeeman fields
        h.add_rashba(get("rashba"))  # Rashba field
        h.add_antiferromagnetism(get("mAF"))  # AF order
        h.add_kane_mele(get("kanemele")) # intrinsic SOC
        h.add_anti_kane_mele(get("antikanemele"))
    h.add_sublattice_imbalance(get("mAB"))  # sublattice imbalance
    h.shift_fermi(get("fermi")) # shift fermi energy
    h.add_haldane(get("haldane")) # intrinsic SOC
    h.add_antihaldane(get("antihaldane"))
    if hamiltoniantype.wants_nambu(window):
        h.setup_nambu_spinor() # establish the BdG structure even if
                                # swave/pwave are both left at zero
        if np.abs(get("swave"))>0.0: h.add_swave(get("swave")) # add term
        p = get_array("pwave")
        if np.sum(np.abs(p))>0.0:
            h.add_pairing(d=get_array("pwave"),mode="triplet",delta=1.0)
    h.turn_dense()
    return h


from .labels import set_labels


from .termtooltips import TERM_TOOLTIPS, BUTTON_TOOLTIPS, PARAM_TOOLTIPS, CALC_FORMULAS
from . import termhighlight


def set_button_tooltips(qtwrap):
    """Set a hover tooltip on every calculation PushButton this mode's page
    has, from the shared BUTTON_TOOLTIPS registry (silently skipped for a
    button name this page doesn't have - same convention as set_formulas()
    below) - but only if that button doesn't already carry a more specific,
    hand-authored tooltip set in interface.ui (e.g. huge_0d's show_lattice:
    "Show the geometry created", show_potential: "This shows in which atoms
    the edge potential is added"). Without this check, a human editing a
    button's tooltip in Designer - interface.ui is "the only file a human
    normally edits with a GUI tool" per CLAUDE.md - would see their edit
    silently discarded the next time this page is built, replaced by the
    generic BUTTON_TOOLTIPS text."""
    form = qtwrap.form
    for name, tip in BUTTON_TOOLTIPS.items():
        widget = form.findChild(QtWidgets.QWidget,name)
        if widget is None or widget.toolTip(): continue
        qtwrap.set_tooltip(name, tip)


def set_param_tooltips(qtwrap):
    """Set a hover tooltip on every other form field (a LineEdit/ComboBox/
    CheckBox/RadioButton that isn't a Hamiltonian term or a calculation
    button) this mode's page has, from the shared PARAM_TOOLTIPS registry -
    same skip-if-already-tooltipped convention as set_button_tooltips()
    above, so a hand-authored interface.ui tooltip (or one set by
    scfterms.py/hybridparts.py) is never overwritten."""
    form = qtwrap.form
    for name, tip in PARAM_TOOLTIPS.items():
        widget = form.findChild(QtWidgets.QWidget,name)
        if widget is None or widget.toolTip(): continue
        qtwrap.set_tooltip(name, tip)


def _ensure_formula_image(qtwrap, term):
    """Make sure this page has a "<term>_image" label between the
    "<term>" field and its descriptive label (shifting the field one grid
    column to the right to make room), if interface.ui didn't already
    define one - so modes whose .ui predates the formula-image convention
    (e.g. 2dslab/3d/multilayergraphene/hofstader1d/tbg/tmdc) get it
    automatically just by calling set_formulas(), with no per-mode .ui
    edits needed. Positioned to match where Designer already places the
    image for modes that pre-date this helper (0d/1d/2d/heavyfermion/
    impurity_embedding: label, image, field, left to right) rather than
    after the field - an earlier version of this function put new images
    after the field instead, which looked inconsistent (formula on the
    "wrong" side) next to those modes. Modes that already have a
    Designer-authored "<term>_image" widget are left alone - set_formulas()
    below still sets its pixmap/tooltip either way."""
    form = qtwrap.form
    image_name = term+"_image"
    if form.findChild(QtWidgets.QWidget,image_name) is not None: return
    field = form.findChild(QtWidgets.QWidget,term)
    if field is None: return
    grid = qtwrap.find_layout_of(field)
    if grid is None: return
    idx = grid.indexOf(field)
    row,col,rowspan,colspan = grid.getItemPosition(idx)
    grid.removeWidget(field)
    grid.addWidget(field,row,col+1,rowspan,colspan)
    image = BodyLabel("",field.parentWidget())
    image.setObjectName(image_name)
    grid.addWidget(image,row,col)
    setattr(form,image_name,image)
    # inherit the field's current shown/hidden state - if latticeterms.py
    # already hid this term's field (e.g. Haldane/Kane-Mele on a
    # non-honeycomb lattice) before set_formulas() ran, a freshly-created
    # image defaults to visible and would otherwise show a lone formula
    # next to a hidden, blank row. Later lattice changes stay in sync via
    # latticeterms.py's own "_image" name matching, now that this widget
    # exists and is registered on `form`.
    image.setVisible(not field.isHidden())


def set_formulas(qtwrap):
    """Set all the formulas and their physics tooltips in the interface"""
    terms = ["hopping","fermi","exchange","haldane","kanemele"]
    terms += ["antihaldane","antikanemele","mAB","mAF","swave","pwave"]
    terms += ["rashba","kondo","kexchange"]
    terms += ["exchange_impurity","fermi_impurity"]
    terms += ["crystalfield","peierls","inplaneb","interlayer","tinter"]
    terms += ["interlayer_bias","ising_SOC","cdw","strain"]
    # mean-field (many-body) terms: scfterms.py narrows their number field
    # to give the formula column the room, so render these into a larger
    # box than the single-particle terms above
    meanfield_terms = ["U","V1","V2","J1","J2","J3"]
    form = qtwrap.form
    for t in terms + meanfield_terms:
        width, height = (600,50) if t in meanfield_terms else (400,30)
        if t not in meanfield_terms: _ensure_formula_image(qtwrap,t) # meanfield
             # images are placed by scfterms.build() itself (images=True)
        qtwrap.set_logo(t+"_image",t+".png",width=width,height=height)
        tip = TERM_TOOLTIPS.get(t)
        if tip is not None:
            qtwrap.set_tooltip(t,tip)
            qtwrap.set_tooltip(t+"_image",tip)
        if t not in meanfield_terms: # meanfield fields wire their own
            # highlight in scfterms.py, where the field is already known
            # directly rather than looked up by (possibly mismatched) name
            field = termhighlight.find_term_field(form,t)
            if field is not None: termhighlight.wire_highlight(field)


def _insert_grid_row_below(layout, row, col, colspan, image):
    """Open a new, empty grid row directly below `row` (shifting every
    existing item currently at that row or below down by one) and place
    `image` there, spanning the same columns as the button it documents,
    centered within that span (see set_calculation_formulas())."""
    shifted = []
    for idx in range(layout.count()-1, -1, -1):
        r,c,rs,cs = layout.getItemPosition(idx)
        if r >= row:
            item = layout.takeAt(idx)
            shifted.append((item,r+1,c,rs,cs))
    for item,r,c,rs,cs in shifted:
        w = item.widget()
        if w is not None: layout.addWidget(w,r,c,rs,cs)
        else:
            l = item.layout()
            if l is not None: layout.addLayout(l,r,c,rs,cs)
    layout.addWidget(image,row,col,1,colspan,Qt.AlignHCenter)


def _move_params_above_buttons(layout, calc_button_names):
    """Reorder `layout`'s rows so every "plain parameter" row (a number
    field, combobox, or a nested grid of them) ends up above every row
    that holds one of this page's calculation buttons, preserving the
    relative order within each of those two groups - interface.ui was
    never consistent about which came first (e.g. the Bands tab puts
    show_bands at row 0 with its Operator/kpoints fields below it at row
    1, while the DOS tab already puts its parameter grid first and
    show_dos last), and the button should always read second-to-last with
    its formula (added right after, by _ensure_button_formula_image())
    truly last. A no-op if the layout is already in that order, or holds
    no rows of one kind (e.g. a button-only grid like 2d's "Topology 2D"
    tab, where every row is a button row sharing that tab with a *sibling*
    grid of Operator/kpoints in a different grid layout entirely - nothing
    to reorder there, and the buttons' relative order must stay intact).
    Assumes every row has rowspan 1, true of every calculation button's
    grid across the app currently."""
    entries = [] # (row,col,rowspan,colspan,item)
    for idx in range(layout.count()):
        r,c,rs,cs = layout.getItemPosition(idx)
        entries.append((r,c,rs,cs,layout.itemAt(idx)))
    button_rows = set()
    for r,c,rs,cs,item in entries:
        w = item.widget()
        if w is not None and w.objectName() in calc_button_names:
            button_rows.add(r)
    all_rows = set(r for r,c,rs,cs,item in entries)
    param_rows = all_rows - button_rows
    if not param_rows or not button_rows: return
    if max(param_rows) < min(button_rows): return # already in order
    for idx in range(layout.count()-1, -1, -1): layout.takeAt(idx)
    new_row = {}
    nr = 0
    for r in sorted(param_rows): new_row[r] = nr; nr += 1
    for r in sorted(button_rows): new_row[r] = nr; nr += 1
    for r,c,rs,cs,item in entries:
        target = new_row[r]
        w = item.widget()
        if w is not None: layout.addWidget(w,target,c,rs,cs)
        else:
            l = item.layout()
            if l is not None: layout.addLayout(l,target,c,rs,cs)


def _ensure_button_formula_image(qtwrap, button_name, formula_rows):
    """Make sure this page has a "<button_name>_formula" label directly
    below the named calculation PushButton, creating it on the fly - the
    calculation analog of _ensure_formula_image() above, but for buttons
    rather than term fields. A button has no Designer-authored image
    widget to reuse (unlike a term field, no mode predates this
    convention), so this always creates one. Unlike a term field, a
    button isn't reliably inside a QGridLayout (see find_any_layout_of()'s
    docstring), so this branches on the actual layout type: in a grid, it
    opens a new row directly below the button's row (shifting later rows
    down) rather than placing the formula beside the button, so every
    formula reads consistently below its button rather than some beside
    and some below depending on whether a neighboring cell happened to be
    free. By the time this runs, set_calculation_formulas() has already
    called _move_params_above_buttons() on this same grid, so "directly
    below the button" already means "at the true bottom of the tab" - see
    that function's docstring. Several buttons often share one grid row
    (e.g. 2d's "Topology 2D" tab has show_chern/show_z2/show_berry2d/
    show_berry1d side by side) - `formula_rows` (a dict scoped to one
    set_calculation_formulas() call) remembers the new row already opened
    for a given (layout,row) so those buttons' formulas land together in
    the one shared new row, at their own button's column, instead of each
    button's insertion re-shifting the grid and scattering the formulas at
    different depths. In a box layout (QVBoxLayout - every calculation
    button that isn't in a QGridLayout is in one, never a QHBoxLayout,
    checked across every mode's interface.ui), inserting right after the
    button's own item already stacks the image below it with no extra
    work, and every such box-layout tab already puts its parameter grid
    before the button in interface.ui, so no reordering is needed there
    either."""
    form = qtwrap.form
    image_name = button_name+"_formula"
    if form.findChild(QtWidgets.QWidget,image_name) is not None: return
    button = form.findChild(QtWidgets.QWidget,button_name)
    if button is None: return
    layout = qtwrap.find_any_layout_of(button)
    if layout is None: return
    image = BodyLabel("",button.parentWidget())
    image.setObjectName(image_name)
    if isinstance(layout,QtWidgets.QGridLayout):
        idx = layout.indexOf(button)
        row,col,rowspan,colspan = layout.getItemPosition(idx)
        key = (id(layout),row)
        target_row = formula_rows.get(key)
        if target_row is None:
            target_row = row+rowspan
            _insert_grid_row_below(layout,target_row,col,colspan,image)
            formula_rows[key] = target_row
        else:
            layout.addWidget(image,target_row,col,1,colspan,Qt.AlignHCenter)
    else: # QBoxLayout (vertical - see docstring)
        idx = layout.indexOf(button)
        layout.insertWidget(idx+1,image,0,Qt.AlignHCenter)
    setattr(form,image_name,image)


def set_calculation_formulas(qtwrap):
    """Set a formula image below every calculation button this page has,
    for every button name present in CALC_FORMULAS (silently skipped
    otherwise - same convention as set_formulas()/set_button_tooltips()).
    Several button names share the same formula key (e.g. every kind of
    LDOS button), so the same PNG is reused across them rather than
    re-rendered - see CALC_FORMULAS's docstring in termtooltips.py. First
    reorders each distinct grid layout that holds a calculation button so
    its parameter rows sit above the button row(s) - see
    _move_params_above_buttons() - so the button always reads
    second-to-last and its formula (centered) truly last."""
    form = qtwrap.form
    calc_button_names = set(CALC_FORMULAS.keys())
    reflowed = set()
    for name in CALC_FORMULAS:
        button = form.findChild(QtWidgets.QWidget,name)
        if button is None: continue
        layout = qtwrap.find_any_layout_of(button)
        if layout is None or not isinstance(layout,QtWidgets.QGridLayout): continue
        if id(layout) in reflowed: continue
        reflowed.add(id(layout))
        _move_params_above_buttons(layout,calc_button_names)
    formula_rows = {} # (id(grid layout),source row) -> already-opened new
                       # row below it, shared by buttons in the same row
    for name,key in CALC_FORMULAS.items():
        _ensure_button_formula_image(qtwrap,name,formula_rows)
        qtwrap.set_logo(name+"_formula","calc_"+key+".png",width=500,height=40)
        tip = BUTTON_TOOLTIPS.get(name)
        if tip is not None: qtwrap.set_tooltip(name+"_formula",tip)








def initialize(window):
    """Do various initializations"""
    cs = ["RGB","hot","inferno","plasma","bwr","rainbow","gnuplot"]
    set_colormaps(window.form,"bands_colormap",cs=cs) # set the bands
    # scf_initialization is populated by latticeterms.py instead (exactly
    # the guess modes matching a term this mode/lattice combination
    # actually has, plus "random" - see
    # latticeterms._rebuild_scf_initialization_baseline())
    window.set_combobox("bands_color",operators.operator_list)
    # fs_operator is deliberately NOT populated here: heavyfermion (which
    # calls this initialize()) keeps its own hand-authored fs_operator item
    # list (dispersive_electrons/kondo_sites/None) - overwriting it with
    # operators.operator_list here would clobber that. 2d.py, the only
    # other mode with this field, populates it itself - see
    # latticeterms.py's RESTRICTED_TERMS docstring.
    window.set_combobox("operator_kdos",operators.operator_list)










