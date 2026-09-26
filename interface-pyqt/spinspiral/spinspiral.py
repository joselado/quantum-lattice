#!/usr/bin/env python3

from __future__ import print_function

import sys
import os
from fractions import Fraction

# main path
qlroot = os.path.dirname(os.path.realpath(__file__))+"/../.."
sys.path.append(qlroot+"/pysrc/") # python libraries


from interfacetk import qtwrap # import the library with simple wrappers to Qt
get = qtwrap.get  # get the value of a certain variable
getbox = qtwrap.getbox  # get the value of a certain variable
window = qtwrap.new_page(os.path.dirname(os.path.realpath(__file__))) # this mode's page

from interfacetk.ql_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries
from pyqula import algebra # dense/sparse-agnostic matrix helpers

common.initialize(qtwrap) # do several common initializations

qtwrap.set_combobox("bands_color",operators.operator_list)
qtwrap.set_combobox("dos_operator",operators.operator_list)

pickup_hamiltonian = lambda: common.pickup_hamiltonian(qtwrap,initialize)

# Only lattices with a single site per unit cell, so that "one site = one
# spiral phase" holds exactly (see get_phases() below, which relies on
# every site's fractional coordinate differing by an integer). Adding a
# multi-site lattice later means deciding whether the basis sites share
# their cell's phase or carry their own - see INTERFACE_GUIDE.md.
LATTICES = {
  "Chain": geometry.chain,
  "Triangular": geometry.triangular_lattice,
}

# latticeterms.connect() only filters this mode's operator menus here
# (restrict_widgets=False): its "kanemele" field is a generic intrinsic-SOC
# term, and latticeterms' RESTRICTED_TERMS would hide it outright on any
# non-honeycomb lattice, i.e. on both lattices this mode offers
from interfacetk import latticeterms
latticeterms.connect(qtwrap,lambda: getbox("lattice"),restrict_widgets=False,
    dimensionality=lambda: LATTICES[getbox("lattice")]().dimensionality)


def get_qvector():
    """Return the spiral wavevector the user asked for, in fractional units
    of the reciprocal lattice vectors, padded/truncated to one component per
    periodic direction (a chain user types a single number)."""
    dim = LATTICES[getbox("lattice")]().dimensionality
    q = np.array(qtwrap.get_array("qvector")).real # get_array returns complex
    q = np.concatenate([q,np.zeros(dim)])[0:dim] # pad with zeros / truncate
    return q


def get_commensurate():
    """Snap the requested wavevector to the nearest commensurate one and
    return (q, nsuper): the realized fractional wavevector and the number of
    primitive cells along each periodic direction needed to accommodate it.

    A spin spiral of wavevector q is only periodic in real space when every
    q component is rational; pyqula has no twisted boundary conditions here
    (the texture is imposed as an explicit site-dependent exchange field, see
    initialize()), so the supercell has to contain a whole number of spiral
    periods. Each component is rationalized independently with
    Fraction.limit_denominator, which gives the closest fraction whose
    denominator - and hence supercell length along that direction - stays
    within the user's "Max. supercell"."""
    nmax = max([int(get("max_supercell")),1])
    fs = [Fraction(float(qi)).limit_denominator(nmax) for qi in get_qvector()]
    q = np.array([float(f) for f in fs])
    nsuper = [max([f.denominator,1]) for f in fs]
    return q,nsuper


def get_geometry():
    """Return the commensurate supercell hosting the spiral"""
    g = LATTICES[getbox("lattice")]() # primitive geometry
    nsuper = get_commensurate()[1]
    if g.dimensionality==1: g = g.supercell(nsuper[0])
    else: g = g.supercell(nsuper)
    return g


def get_spiral_frame():
    """Return (u1,u2,u3): an orthonormal frame in which the moments rotate
    in the u1-u2 plane and cant towards u3 (the cone axis, normal to the
    spiral plane)."""
    plane = getbox("spiral_plane")
    if plane=="XY": u1,u2 = np.array([1.,0.,0.]),np.array([0.,1.,0.])
    elif plane=="YZ": u1,u2 = np.array([0.,1.,0.]),np.array([0.,0.,1.])
    elif plane=="ZX": u1,u2 = np.array([0.,0.,1.]),np.array([1.,0.,0.])
    else: # "Custom": the user gives the cone axis, build a plane around it
        u3 = np.array(qtwrap.get_array("spiral_axis")).real
        if u3.dot(u3)<1e-8: u3 = np.array([0.,0.,1.]) # degenerate input
        u3 = u3/np.sqrt(u3.dot(u3))
        # any vector not parallel to u3 gives a valid in-plane direction
        seed = np.array([1.,0.,0.])
        if abs(u3.dot(seed))>0.9: seed = np.array([0.,1.,0.])
        u1 = np.cross(seed,u3) ; u1 = u1/np.sqrt(u1.dot(u1))
        return u1,np.cross(u3,u1),u3
    return u1,u2,np.cross(u1,u2)


def get_qcartesian():
    """Return the spiral wavevector in Cartesian units, i.e. the vector Q
    for which the spiral phase of a site is exactly Q.r.

    The phase is defined from the *primitive* lattice's fractional
    coordinates (a site n1 cells along a1 has phase 2*pi*q1*n1), so Q is
    built from the primitive lattice vectors, not from the supercell's -
    reading it off the supercell instead would make the spiral turn N times
    too slowly, while still looking like a perfectly ordinary spiral."""
    g = LATTICES[getbox("lattice")]() # primitive geometry
    q = get_commensurate()[0]
    a = np.array([g.a1,g.a2,g.a3][0:len(q)]) # primitive vectors, one per q component
    # fractional coordinates of r are pinv(a.T)@r, hence phase = 2*pi*q.(pinv(a.T)@r)
    return 2.*np.pi*np.array(np.linalg.pinv(a.T)).T.dot(q)


def get_phases(g=None):
    """Return the spiral phase (in radians) of every site of the supercell"""
    if g is None: g = get_geometry()
    Q = get_qcartesian()
    return np.array([Q.dot(ri) for ri in g.r])


def get_moments(g=None):
    """Return the unit moment direction of every site: a conical spiral,
    rotating in the u1-u2 plane at the spiral wavevector and canted by the
    cone angle towards the cone axis u3 (90 degrees = flat, in-plane
    spiral; 0 degrees = collinear ferromagnet along u3)."""
    u1,u2,u3 = get_spiral_frame()
    theta = get("cone_angle")*np.pi/180.
    ps = get_phases(g=g)
    return np.array([np.sin(theta)*(np.cos(p)*u1 + np.sin(p)*u2)
                     + np.cos(theta)*u3 for p in ps])


def get_exchange_field(g):
    """Return the callable h.add_zeeman() takes: the site-dependent exchange
    field imposing the conical spiral, evaluated from a site's position."""
    u1,u2,u3 = get_spiral_frame()
    theta = get("cone_angle")*np.pi/180.
    J = get("spiral_exchange")
    Q = get_qcartesian()
    def field(r):
        p = Q.dot(np.array(r)) # spiral phase at this site
        return J*(np.sin(theta)*(np.cos(p)*u1 + np.sin(p)*u2)
                  + np.cos(theta)*u3)
    return field


def spiral_report_text():
    """The text of the page's read-only "spiral_info" line: the wavevector
    and supercell actually built, since the requested wavevector is snapped
    to a commensurate one."""
    q,nsuper = get_commensurate()
    fs = [str(Fraction(int(round(qi*n)),n)) for qi,n in zip(q,nsuper)]
    txt = "Using q = ("+", ".join(fs)+") in a supercell of "
    txt += "x".join([str(n) for n in nsuper])+" cells ("
    txt += str(len(get_geometry().r))+" sites).\n\n"
    txt += ("The wavevector is given in fractional units of the reciprocal "
            "lattice vectors, and is snapped to the nearest commensurate "
            "value whose supercell fits within \"Max. supercell\".")
    return txt


def report_spiral():
    """Show spiral_report_text() on the page. Goes through qtwrap.modify()
    because initialize() - its only caller - runs on a handler's worker
    thread, and modify() marshals the widget write back onto the GUI thread.
    Not usable during this module's own import: modify() ends in
    app.processEvents(), which would dispatch a queued navigation click
    mid-construction and re-point qtwrap's active page out from under the
    rest of the import (see INTERFACE_GUIDE.md's "Known gotchas"). The
    import-time call at the bottom of this file writes the label directly
    instead."""
    qtwrap.modify("spiral_info",spiral_report_text())


def initialize():
    """Initialize the calculation: build the commensurate supercell and
    impose the conical spin spiral on it as an explicit, site-dependent
    exchange field."""
    g = get_geometry() # get the geometry
    h = g.get_hamiltonian(has_spin=True,tij=qtwrap.get_array("hopping"))
    h.add_zeeman(get_exchange_field(g)) # impose the spiral texture
    h.add_rashba(get("rashba")) # Rashba SOC
    h.add_kane_mele(get("kanemele")) # intrinsic (Kane-Mele) SOC - identically
        # zero on a chain, whose two-hop paths are collinear
    h.shift_fermi(get("fermi")) # shift the Fermi energy
    h.turn_dense()
    report_spiral() # tell the user what was actually built
    return h


def get_site_spin_matrices(h):
    """Return one 2x2 spin matrix per site, defining what the LDOS is
    projected onto: the identity for the total (charge) LDOS, n.sigma for a
    fixed global spin axis, or S_i.sigma - a different matrix on every site -
    for the projection onto each site's own moment.

    Returned as a plain (nsites,2,2) array rather than as a pyqula Operator
    because the projection has to act *per site*: pyqula's own
    ldos.ldosmap(operator=...) multiplies each eigenstate's spatial density
    by that eigenstate's global expectation value <psi|O|psi>, which is
    identically zero for any in-plane spin component of a spiral (the
    texture averages out over the supercell) - it would report an empty map
    for exactly the projections this mode exists to show. See
    compute_spiral_ldos() below, which does the site-resolved sum instead."""
    from pyqula.rotate_spin import sx,sy,sz
    paulis = np.array([np.array(sx.todense()),np.array(sy.todense()),
                       np.array(sz.todense())])
    n = len(h.geometry.r)
    name = getbox("spiral_ldos_projection")
    if name in (None,"None"):
        return np.array([np.identity(2,dtype=np.complex128) for i in range(n)])
    if name in ("Sx","Sy","Sz"):
        ns = np.zeros((n,3)) ; ns[:,"xyz".index(name[1])] = 1.0
    elif name=="Custom axis":
        v = np.array(qtwrap.get_array("spiral_ldos_axis")).real
        if v.dot(v)<1e-8: v = np.array([0.,0.,1.]) # degenerate input
        ns = np.array([v/np.sqrt(v.dot(v)) for i in range(n)])
    elif name=="Local moment": ns = get_moments(g=h.geometry)
    else: raise ValueError("Unknown spin projection "+str(name))
    return np.einsum("ij,jab->iab",ns.astype(np.complex128),paulis)


def get_kmesh(dim,nk):
    """Return a regular k-mesh with nk points per periodic direction"""
    nk = max([int(nk),1])
    ks1 = np.linspace(0.,1.,nk,endpoint=False)
    if dim==1: return [np.array([k,0.,0.]) for k in ks1]
    return [np.array([k1,k2,0.]) for k1 in ks1 for k2 in ks1]


def compute_spiral_ldos(h,energies=None,delta=0.1,nk=20):
    """Return (energies, ldos) with ldos[ie,isite] the local density of
    states at that energy and site, projected onto the per-site spin matrix
    get_site_spin_matrices() returns.

    Same Lorentzian-broadened eigenstate sum pyqula's own ldos.ldosmap()
    performs, with one difference: the projection is applied to each site's
    own two spin components separately (a site's weight is
    psi_i^dagger M_i psi_i) instead of to the eigenstate as a whole, so an
    in-plane projection resolves the spiral instead of averaging it away.
    The k-mesh is a regular grid rather than ldosmap()'s random sampling,
    so that the same parameters always give the same map."""
    if energies is None: energies = np.linspace(-4.,4.,100)
    ms = get_site_spin_matrices(h) # one 2x2 projection matrix per site
    hkgen = h.get_hk_gen() # Bloch Hamiltonian generator
    nsites = len(h.geometry.r)
    if h.intra.shape[0]!=2*nsites: # the (site,spin) reshape below assumes this
        raise ValueError("The spiral LDOS needs a plain spinful Hamiltonian "
                "(two components per site), got one of dimension "
                +str(h.intra.shape[0])+" for "+str(nsites)+" sites")
    ks = get_kmesh(h.dimensionality,nk)
    out = np.zeros((len(energies),nsites))
    for k in ks:
        eig,evec = np.linalg.eigh(np.array(algebra.todense(hkgen(k))))
        # (site, spin, state) view of the eigenvectors, since pyqula orders
        # a spinful basis as (site0 up, site0 down, site1 up, ...)
        psi = evec.reshape(nsites,2,evec.shape[1])
        w = np.einsum("ias,iab,ibs->is",np.conjugate(psi),ms,psi).real
        # Lorentzian of every level, at every energy
        lor = delta/((energies[:,None]-eig[None,:])**2 + delta**2)/np.pi
        out += lor@w.T
    return energies,out/len(ks)


# Deviations smaller than this are treated as exactly zero once the average
# has been subtracted. Where the spiral has a symmetry that forbids any
# spatial variation at all (no spin-orbit coupling: see the module docstring
# of tests/test_spinspiral.py), the subtraction leaves only float64 rounding:
# measured at most ~1e-15 across both lattices, every spin projection, and up
# to 20-cell supercells at 3600 k-points. Left alone, that noise would be
# rescaled to the full color range by the colormap and drawn as vivid,
# entirely meaningless structure. Set three orders of magnitude above that
# measured rounding and far below the ~0.01-1 scale of the LDOS itself, so a
# genuinely small but real modulation still gets plotted rather than erased.
LDOS_NOISE_FLOOR = 1e-12

# Above this many spiral periods in view, the wavelength guide lines stop
# being a guide and become a hatch pattern over the map, so they are dropped
# instead.
MAX_MARKED_PERIODS = 40


def spiral_positions(g):
    """Return (positions, index, wavelength): where each distinct point of
    the map sits along the spiral direction, which of those points each site
    of `g` belongs to, and the spiral wavelength in the same length units.

    Two coordinates are possible here and the difference matters:

      * the site's actual distance along q (its unwrapped spiral phase over
        |q|). This is real-space position: the axis then spans the whole
        supercell, which holds as many spiral wavelengths as the numerator
        of q. It is the coordinate we want - but ql-map2d's imshow needs a
        uniformly spaced grid, and on a 2D lattice with a generic wavevector
        the sites' projections onto q are not uniformly spaced (they are the
        set {q1*n1 + q2*n2}, which has gaps).
      * the phase folded into a single turn. That set is always uniform (it
        is the cyclic subgroup generated by the reduced fractions q1, q2), at
        the cost of wrapping a supercell holding several wavelengths back
        onto one.

    So: use the unwrapped, real-space one whenever it comes out uniform -
    always on a chain, and on a triangular lattice for many wavevectors -
    and fall back to the folded phase otherwise. They coincide whenever the
    supercell holds exactly one wavelength, which is the usual case."""
    Q = get_qcartesian()
    qmod = np.sqrt(Q.dot(Q))
    if qmod<1e-8:
        raise ValueError("The spiral wavevector is zero: there is no spiral "
                "direction to resolve the LDOS along. Set a non-zero "
                "\"Spiral wavevector\".")
    wavelength = 2.*np.pi/qmod
    nphase = np.lcm.reduce([int(n) for n in get_commensurate()[1]])
    turns = get_phases(g=g)/(2.*np.pi) # spiral phase of each site, in turns
    turns = turns - np.min(turns) # measured from the first site
    kk = np.round(turns*nphase).astype(int) # phase in units of one map point
    if np.max(np.abs(turns*nphase-kk))>1e-6: # not on the expected grid
        raise ValueError("The spiral phases do not fall on a regular grid; "
                "this lattice is not supported by the spiral LDOS.")
    unique = np.unique(kk)
    steps = np.diff(unique)
    if len(unique)>1 and np.all(steps==steps[0]): pass # unwrapped is uniform
    else: # fall back to the folded phase, which always is
        kk = kk%nphase
        unique = np.unique(kk)
        steps = np.diff(unique)
    index = np.searchsorted(unique,kk) # which map point each site falls on
    return unique*wavelength/nphase, index, wavelength


def write_spiral_ldos(es,ds,g,subtract_average=None,nrep=None):
    """Write the LDOS as a function of position *along the spiral* and of
    energy, in the (position, energy, LDOS) column layout ql-map2d reads -
    position first, so the map is drawn with position across the bottom and
    energy up the side. Returns the positions at which the spiral completes
    a turn, for show_spiral_ldos() to mark on the plot.

    Sites landing on the same point of the spiral are averaged together (see
    spiral_positions() for what that coordinate is), and the whole profile
    is then repeated `nrep` times along the axis. The repetition is exact
    rather than cosmetic - the system really is periodic with what one copy
    covers - and it is what makes the wavelength readable: a commensurate
    supercell often holds exactly one turn of the spiral, so a single copy
    would have nothing to mark inside it.

    With `subtract_average` on (the page's own checkbox by default), each
    energy's row has its mean over positions removed, leaving the *spatial
    variation* alone. That is what the map is for: the uniform part of the
    LDOS is just the density of states at that energy, typically orders of
    magnitude larger than the modulation the spiral imprints on top of it,
    so an absolute map is a flat wash in which the interesting structure is
    invisible. The result is signed, hence the diverging colormap
    show_spiral_ldos() asks for, and is floored at LDOS_NOISE_FLOOR so that
    a map with no real variation comes out flat rather than as amplified
    rounding noise."""
    pos,index,wavelength = spiral_positions(g)
    npos = len(pos)
    if subtract_average is None:
        subtract_average = qtwrap.is_checked("spiral_ldos_subtract_average")
    if nrep is None: nrep = int(get("spiral_ldos_nrep"))
    nrep = max([int(nrep),1])
    # rows[ie][ip]: one value per (energy, position), averaging the sites
    # that land on the same point of the spiral
    rows = []
    for ie in range(len(es)):
        row = np.array([np.mean(ds[ie][index==ip]) for ip in range(npos)])
        if subtract_average:
            row = row - np.mean(row) # keep only the variation
            row[np.abs(row)<LDOS_NOISE_FLOOR] = 0.0 # ... and not the rounding noise
        rows.append(row)
    step = (pos[-1]-pos[0])/(npos-1) if npos>1 else wavelength
    period = npos*step # what one copy of the profile covers
    f = open("SPIRAL_LDOS.OUT","w")
    f.write("# position along q, energy, LDOS\n")
    for t in range(nrep): # position outermost: ql-map2d reshapes on column 0
        for ip in range(npos):
            # from the integer grid index rather than by accumulating
            # `period`, so the axis stays exactly uniform for any nrep
            x = pos[0]+(ip+t*npos)*step
            for ie in range(len(es)):
                f.write(str(x)+"  "+str(es[ie])+"  "+str(rows[ie][ip])+"\n")
    f.close()
    return wavelength_marks(pos[0],pos[0]+nrep*period-step,wavelength)


def wavelength_marks(first,last,wavelength):
    """Positions at which the spiral completes a full turn, across the
    plotted range.

    The spiral's phase is zero at the first site, so the marks sit at whole
    multiples of the wavelength from there - which is *not* generally a
    unit-cell boundary: when the supercell holds several turns, a turn ends
    partway through a cell, and that is exactly what the marks are there to
    show. Returns [] for a range holding more turns than can be told apart."""
    if wavelength<=0.: return []
    n = int(np.floor((last-first)/wavelength+1e-9))
    if n+1>MAX_MARKED_PERIODS: return []
    return [first+i*wavelength for i in range(n+1)]


def show_spiral_ldos():
    """Compute the LDOS as a function of energy and of position along the
    spiral, optionally projected onto a spin direction, and plot it as a
    colormap."""
    h = pickup_hamiltonian() # get the Hamiltonian
    ew = abs(get("spiral_ldos_ewindow"))
    ne = max([int(get("spiral_ldos_ne")),2])
    delta = get("spiral_ldos_delta") or 1e-3
    nk = max([int(get("spiral_ldos_nk")),1])
    energies = np.linspace(-ew,ew,ne)
    es,ds = compute_spiral_ldos(h,energies=energies,delta=delta,nk=nk)
    marks = write_spiral_ldos(es,ds,h.geometry) # where the spiral completes a turn
    name = getbox("spiral_ldos_projection")
    zlabel = "LDOS" if name in (None,"None") else "LDOS ("+name+")"
    signed = qtwrap.is_checked("spiral_ldos_subtract_average") or name not in (None,"None")
    if qtwrap.is_checked("spiral_ldos_subtract_average"): zlabel += " - mean"
    # a signed map (the average removed, or a spin projection) wants a
    # diverging colormap centered on zero; a plain LDOS is positive-definite
    # and reads better on a sequential one
    command = ('ql-map2d --input SPIRAL_LDOS.OUT '
            '--xlabel "Position along the spiral" --ylabel Energy '
            '--zlabel "'+zlabel+'" --title "LDOS along the spiral"')
    command += ' --cmap coolwarm --center True' if signed else ' --cmap inferno'
    # a dashed line at every full turn of the spiral, so its wavelength can
    # be read straight off the plot. Written as --vlines=... rather than as
    # two separate tokens: a mark can sit at a negative position, and
    # argparse would read a leading minus as another option name
    # ("expected one argument") instead of as this one's value.
    if marks: command += " --vlines="+",".join([str(c) for c in marks])
    execute_script(command)


def show_magnetism():
    """Show the spin texture of the system"""
    h = pickup_hamiltonian() # get the Hamiltonian
    common.show_exchange(h,qtwrap)


def show_structure():
    """Show the lattice of the system"""
    common.show_structure(qtwrap,get_geometry)


def show_structure_3d():
    """Show the lattice of the system"""
    common.show_structure_3d(qtwrap,get_geometry)


# fill the "spiral_info" line before anything is computed, so the page shows
# what it will build rather than a blank line. Written straight onto the
# widget rather than through qtwrap.modify(): we are on the GUI thread and
# own this page, and modify()'s app.processEvents() would pump events in the
# middle of building it (see report_spiral()'s docstring).
window.spiral_info.setText(spiral_report_text())

# create signals: STANDARD_HANDLERS covers the plain "pickup_hamiltonian
# + common.get_X" buttons automatically; only the buttons with mode-specific
# behavior need to be listed explicitly here (save_results/load_results are
# wired automatically by common.finalize_page())
signals = common.wire_standard_signals(qtwrap,pickup_hamiltonian,extra={
  "show_structure": show_structure,
  "show_structure_3d": show_structure_3d,
  "show_magnetism": show_magnetism,
  "show_spiral_ldos": show_spiral_ldos,
})

inipath = os.getcwd() # get the initial directory, before common.finalize_page()'s create_folder() chdirs away
common.finalize_page(qtwrap,window,signals,inipath,robust=False)

if __name__ == "__main__":
    window.run() # show this page as its own standalone window and block
