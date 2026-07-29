"""Shared helper for the ql-structure* scripts to outline the primitive
unit cell on top of a plotted structure.

Not a ql-* command - only imported by sibling scripts via
sys.path.insert(0, dirname), the same pattern every ql-* script already
uses to find its own directory (see e.g. plotstyle.py, _pv3d.py).

common.py:write_unit_cell(g) writes CELL.OUT (the lattice vectors, one
row per dimension) and DIMENSIONALITY.OUT from the *primitive* geometry,
before the --nsuper repetition some show_structure handlers apply for
the on-screen view - so the outline drawn here is always one real unit
cell, not the whole (possibly enlarged) supercell being displayed.
"""
import os
import numpy as np


def read_cell():
    """Read CELL.OUT/DIMENSIONALITY.OUT written by common.py:write_unit_cell.

    Returns (dim, vectors) with vectors shaped (dim,3), or None if the
    files are missing (older result folder, or a script run standalone)
    or the geometry isn't periodic (dim==0, e.g. a finite island)."""
    if not os.path.exists("DIMENSIONALITY.OUT") or not os.path.exists("CELL.OUT"):
        return None
    dim = int(open("DIMENSIONALITY.OUT").read())
    if dim == 0:
        return None
    vecs = np.atleast_2d(np.genfromtxt("CELL.OUT"))
    return dim, vecs


def cell_edges(dim, vecs):
    """Return a list of (start,end) 3-vector pairs outlining one unit cell,
    anchored at the origin - a segment for dim==1, a parallelogram for
    dim==2, a parallelepiped's 12 edges for dim==3."""
    origin = np.zeros(3)
    if dim == 1:
        return [(origin, vecs[0])]
    if dim == 2:
        a1, a2 = vecs[0], vecs[1]
        corners = [origin, a1, a1 + a2, a2, origin]
        return [(corners[i], corners[i + 1]) for i in range(4)]
    if dim == 3:
        a1, a2, a3 = vecs[0], vecs[1], vecs[2]
        corners = {}
        for i in (0, 1):
            for j in (0, 1):
                for k in (0, 1):
                    corners[(i, j, k)] = i * a1 + j * a2 + k * a3
        edges = []
        for (i, j, k) in corners:
            if i == 0: edges.append((corners[(0, j, k)], corners[(1, j, k)]))
            if j == 0: edges.append((corners[(i, 0, k)], corners[(i, 1, k)]))
            if k == 0: edges.append((corners[(i, j, 0)], corners[(i, j, 1)]))
        return edges
    raise ValueError("unexpected dimensionality "+str(dim))


def cell_1d_ticks(vecs, positions):
    """For dim==1, the bare segment along a1 overlaps the row of atoms and
    is hard to see - return two tick segments perpendicular to a1, at each
    cell boundary (0 and a1), that bracket the cell instead. Sized from
    `positions` (the (N,3) atom coordinates being plotted) so each tick
    spans the full width of the ribbon - from its narrowest to its widest
    atom along the in-plane direction perpendicular to a1 - rather than an
    arbitrary fixed length."""
    a1 = vecs[0]
    norm = np.linalg.norm(a1[:2])
    if norm == 0: perp = np.array([0., 1., 0.])
    else: perp = np.array([-a1[1], a1[0], 0.]) / norm
    positions = np.asarray(positions)
    proj = positions[:, 0]*perp[0] + positions[:, 1]*perp[1] + positions[:, 2]*perp[2]
    pmin, pmax = (np.min(proj), np.max(proj)) if len(proj) else (0., 0.)
    if pmax - pmin < 1e-9: pmin, pmax = -0.3, 0.3
    ticks = []
    for p in (np.zeros(3), a1):
        ticks.append((p + perp*pmin, p + perp*pmax))
    return ticks
