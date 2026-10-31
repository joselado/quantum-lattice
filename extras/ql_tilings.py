#!/usr/bin/env python3
"""ql_tilings.py - aperiodic monotile tilings as tight-binding lattices for pyqula.

  * Spectre / Hat / Turtle (planar, from the Spectre repository's tile family Tile(a,b)): vertex model, one site per tiling vertex, one bond per
    tile edge.   * Chair44 (3D, Tsiokos; from the Spectre repository): cell model, one site per unit cell of a depth-n supertile, one bond per
    shared face.
They need the Spectre repository (https://github.com/brentharts/spectre), found through the environment variable SPECTRE_DIR, ../../spectre
or /home/claude/spectre.  The patches can be exported to a plain text file (export_points) so that the later scripts run without it.

IMPORTANT FACT (checked in the tests): Hat = Tile(1, sqrt3), Spectre = Tile(1, 1) and Turtle = Tile(sqrt3, 1) have the SAME combinatorics: for
a given substitution level the three vertex graphs are identical (same number of tiles, vertices and edges, same adjacency), and they differ
only in edge LENGTHS.  A tight-binding model with unit hopping on every edge therefore has IDENTICAL spectra for the three tilings; they differ
only if the hopping depends on the edge length, which is what hopping='inverse' (t = t0 / length) and hopping='gauss' implement.

    python3 ql_tilings.py --tests
    python3 ql_tilings.py                 sizes of the patches
"""
import math
import os
import sys

import numpy as np

import ql_common as C

_HERE = os.path.dirname(os.path.realpath(__file__))


def _find_spectre():
    cands = [os.environ.get("SPECTRE_DIR", ""), os.path.join(_HERE, "..", "..", "spectre"), "/home/claude/spectre"]
    return next((p for p in cands if p and os.path.isfile(os.path.join(p, "symchair44.py"))), None)


SPECTRE_DIR = _find_spectre()


def refresh():
    """Look for the Spectre repository again (after SPECTRE_DIR was set or changed, e.g. by the GUI mode)."""
    global SPECTRE_DIR
    SPECTRE_DIR = _find_spectre()
    return SPECTRE_DIR


FAMILY = {"hat": (1.0, math.sqrt(3.0)), "spectre": (1.0, 1.0), "turtle": (math.sqrt(3.0), 1.0)}


def available():
    return SPECTRE_DIR is not None


def _spectre_path():
    if SPECTRE_DIR is None:
        raise RuntimeError("the Spectre repository was not found; set SPECTRE_DIR")
    if SPECTRE_DIR not in sys.path:
        sys.path.insert(0, SPECTRE_DIR)


# ------------------------------------------------------------------------------------------------ planar tilings

class Patch(object):
    """A planar patch: vert (n,2), edges (m,2) int, length (m,), polys (list of vertex-index lists), centroid (t,2), area (t,)."""
    def __init__(self, vert, edges, length, polys, centroid, area, kind="", level=0):
        self.vert, self.edges, self.length, self.polys = vert, edges, length, polys
        self.centroid, self.area, self.kind, self.level = centroid, area, kind, level

    def degree(self):
        d = np.zeros(len(self.vert), int)
        for a, b in self.edges:
            d[a] += 1
            d[b] += 1
        return d


def planar_patch(kind="spectre", level=3):
    """Vertex graph of the level-n Delta supertile of the Hat ('hat'), Spectre ('spectre') or Turtle ('turtle') tiling."""
    _spectre_path()
    import spectre_energy as E
    a, b = FAMILY[kind]
    P = E.Patch(a, b, level)
    edges = {}
    for ids in P.owner:
        for i in range(len(ids)):
            u, v = ids[i], ids[(i + 1) % len(ids)]
            if u != v:
                edges[frozenset((u, v))] = (min(u, v), max(u, v))
    E_ = np.array(sorted(edges.values()), int)
    L = np.hypot(*(P.vert[E_[:, 0]] - P.vert[E_[:, 1]]).T)
    return Patch(P.vert.copy(), E_, L, [list(ids) for ids in P.owner], P.centroid.copy(), P.area.copy(), kind, level)


def hopping_values(length, hopping="unit", t0=1.0, kappa=1.0):
    length = np.asarray(length, float)
    if hopping == "unit":
        return t0 * np.ones_like(length)
    if hopping == "inverse":
        return t0 / length
    if hopping == "gauss":
        return t0 * np.exp(-kappa * (length ** 2 - 1.0))
    raise ValueError(hopping)


def adjacency(n, edges, values):
    import scipy.sparse as sp
    e = np.asarray(edges)
    r = np.r_[e[:, 0], e[:, 1]]
    c = np.r_[e[:, 1], e[:, 0]]
    return sp.csr_matrix((np.r_[values, values], (r, c)), shape=(n, n))


def tight_binding(patch, hopping="unit", t0=1.0, kappa=1.0, onsite=None):
    """Sparse Hamiltonian matrix (-t on each bond by the physics convention would flip the spectrum; here +t, as in pyqula)."""
    T = adjacency(len(patch.vert), patch.edges, hopping_values(patch.length, hopping, t0, kappa))
    if onsite is not None:
        import scipy.sparse as sp
        T = T + sp.diags(onsite)
    return T


def to_pyqula(points, T):
    """pyqula Hamiltonian (finite, spinless) with the given positions (n, 2 or 3) and sparse hopping matrix T."""
    import scipy.sparse as sp
    from pyqula import geometry
    pts = np.asarray(points, float)
    if pts.shape[1] == 2:
        pts = np.c_[pts, np.zeros(len(pts))]
    g = geometry.Geometry()
    g.dimensionality = 0
    g.r, g.x, g.y, g.z = pts, pts[:, 0], pts[:, 1], pts[:, 2]
    h = g.get_hamiltonian(has_spin=False)
    h.intra = sp.csc_matrix(T).astype(complex)
    return h


def export_points(path, points, edges, weights=None):
    """Plain text export: first the positions (x y [z]), then 'edge i j t' lines."""
    pts = np.asarray(points)
    with open(path, "w") as f:
        f.write("# positions: %d, edges: %d\n" % (len(pts), len(edges)))
        for p in pts:
            f.write("p " + " ".join("%.10g" % c for c in p) + "\n")
        for k, (a, b) in enumerate(edges):
            f.write("e %d %d %.10g\n" % (a, b, 1.0 if weights is None else weights[k]))


# ------------------------------------------------------------------------------------------------ Chair44

_STATE = {}


def _chair44_load():
    """Labels (frame, native cell), the cell substitution sigma (168 x 8) and per-label observables. Same construction as the Spectre repository's
    chair44_twoadic / qgl_tiling in the Quantum_Gravity_Lab repository."""
    if not _STATE:
        _spectre_path()
        import symchair44 as S
        import chair44_twoadic as TA
        labels, sigma = TA.labels_and_sigma()
        notch = np.array([S.frame_apply(f, (1, 1, 1)) for f, _ in labels], dtype=np.int8)
        h = np.zeros(len(S.CELLS))
        lab = S.label_table(S.CHILDREN)
        for pi, (ax, k) in enumerate(S.PANELS):
            sd = S.PANEL_SIGN[pi]
            cell = [(k[i] - 1 - (sd if i == ax else 0)) // 2 for i in range(3)]
            h[S.CELLS.index(tuple(cell))] += sum(lab[pi * 8 + j] for j in range(8))
        native = np.array([k for _, k in labels])
        _STATE.update(S=S, labels=labels, sigma=np.array(sigma, dtype=np.int16), notch=notch, pyramid=h[native],
                      index={l: i for i, l in enumerate(labels)})
    return _STATE


def chair44_labels_at(j, n, X, Y, Z):
    """Label of the cell (X, Y, Z) (integer arrays, 0 <= . < 2^n) of sigma^n(j), by reading the binary digits from the top: exact, vectorised,
    and valid for any n (no cube is built)."""
    st = _chair44_load()
    sg = st["sigma"]
    X, Y, Z = (np.asarray(a, np.int64) for a in (X, Y, Z))
    lab = np.full(X.shape, j, dtype=np.int64)
    for k in range(n - 1, -1, -1):
        b = ((X >> k) & 1) * 4 + ((Y >> k) & 1) * 2 + ((Z >> k) & 1)
        lab = sg[lab, b]
    return lab


def chair44_supertile(depth):
    """Occupied cells of the depth-n supertile of the root chair: (coords (N,3) int, labels (N,)); N = 7 * 8^depth."""
    st = _chair44_load()
    S = st["S"]
    root = S.IDENTITY
    n = depth
    side = 2 ** n
    g = np.arange(side)
    X, Y, Z = np.meshgrid(g, g, g, indexing="ij")
    coords, labs = [], []
    for k, c in enumerate(S.CELLS):
        j = st["index"][(root, k)]
        lab = chair44_labels_at(j, n, X.ravel(), Y.ravel(), Z.ravel())
        off = np.array(c) * side
        coords.append(np.c_[X.ravel(), Y.ravel(), Z.ravel()] + off)
        labs.append(lab)
    return np.concatenate(coords), np.concatenate(labs)


def chair44_cell_model(depth, onsite="none", lam=1.0, t0=1.0):
    """(coords, labels, sparse H): face-adjacent occupied cells of the depth-n supertile, hopping t0; onsite = 'none' | 'pyramid'
    (lam * height/36)."""
    import scipy.sparse as sp
    st = _chair44_load()
    coords, labs = chair44_supertile(depth)
    side = int(coords.max()) + 1
    idx = -np.ones((side,) * 3, dtype=np.int64)
    idx[coords[:, 0], coords[:, 1], coords[:, 2]] = np.arange(len(coords))
    rows, cols = [], []
    for ax in range(3):
        sl_a = [slice(None)] * 3
        sl_b = [slice(None)] * 3
        sl_a[ax], sl_b[ax] = slice(0, side - 1), slice(1, side)
        a, b = idx[tuple(sl_a)].ravel(), idx[tuple(sl_b)].ravel()
        m = (a >= 0) & (b >= 0)
        rows.append(a[m])
        cols.append(b[m])
    r, c = np.concatenate(rows), np.concatenate(cols)
    T = sp.csr_matrix((t0 * np.ones(2 * len(r)), (np.r_[r, c], np.r_[c, r])), shape=(len(coords),) * 2)
    if onsite == "pyramid":
        T = T + sp.diags(lam * st["pyramid"][labs] / 36.0)
    return coords, labs, T


def run_tests(verbose=True):
    ok = True

    def check(name, cond, extra=""):
        nonlocal ok
        ok &= bool(cond)
        if verbose:
            print("  %-4s %s %s" % ("ok" if cond else "FAIL", name, extra))

    if not available():
        print("  SKIP (the Spectre repository was not found: set SPECTRE_DIR)")
        return True
    patches = {k: planar_patch(k, 3) for k in FAMILY}
    sp_ = patches["spectre"]
    V, E, F = len(sp_.vert), len(sp_.edges), len(sp_.polys)
    check("planar graph of a simply connected patch: V - E + F = 1 (F = tiles)", V - E + F == 1, "(V=%d E=%d F=%d)" % (V, E, F))
    check("Hat, Spectre and Turtle graphs are identical (same edges after the same vertex numbering)",
          all(np.array_equal(patches[k].edges, sp_.edges) for k in patches) and all(len(p.vert) == V for p in patches.values()))
    s3 = math.sqrt(3)
    check("edge lengths: Spectre all 1; Hat and Turtle only 1 and sqrt3",
          np.allclose(sp_.length, 1.0, atol=1e-4)
          and all(np.all(np.isclose(patches[k].length, 1.0, atol=1e-4) | np.isclose(patches[k].length, s3, atol=1e-4)) for k in ("hat", "turtle"))
          and all(np.isclose(patches[k].length, s3, atol=1e-4).any() for k in ("hat", "turtle")))
    d = sp_.degree()
    check("vertex degrees are 2, 3 or 4 only (straight points of edges are degree 2)", set(d) <= {2, 3, 4}, "(%s)" % sorted(set(d)))
    # pyqula round trip
    T = tight_binding(sp_)
    h = to_pyqula(sp_.vert, T)
    A = np.abs(np.asarray(h.intra.todense()) - T.toarray()).max()
    check("pyqula Hamiltonian holds exactly the vertex hopping matrix", A < 1e-12)
    # chair44
    st = _chair44_load()
    coords, labs = chair44_supertile(2)
    check("Chair44 depth-2 supertile has 7 * 8^2 = 448 cells", len(coords) == 448 and len({tuple(c) for c in coords}) == 448)
    nt = st["notch"][labs].astype(int).sum(axis=0)
    check("its notch vectors sum to 7 * 2^2 * (1,1,1) = (28,28,28)", tuple(nt) == (28, 28, 28), "(%s)" % (tuple(nt),))
    check("the 192 signed pyramid heights sum to 0 (per native cell sums add up to 0)", abs(_pyr_total()) < 1e-9)
    c3, l3, T3 = chair44_cell_model(3)
    deg = np.asarray(T3.sum(axis=1)).ravel()
    from scipy.sparse.csgraph import connected_components
    ncomp = connected_components(T3, directed=False)[0]
    check("Chair44 cell graph is connected with degrees 1..6", ncomp == 1 and deg.max() <= 6 and deg.min() >= 1,
          "(N=%d, degree range %d-%d, components %d)" % (len(c3), deg.min(), deg.max(), ncomp))
    # label function agrees with an explicit inflation
    sg = st["sigma"]
    A = np.array([[[5]]])
    for _ in range(3):
        N = A.shape[0]
        out = np.empty((2 * N,) * 3, dtype=np.int64)
        for b in range(8):
            out[(b >> 2) & 1::2, (b >> 1) & 1::2, b & 1::2] = sg[A, b]
        A = out
    g = np.arange(8)
    X, Y, Z = np.meshgrid(g, g, g, indexing="ij")
    check("digit-by-digit labels agree with explicit inflation of a cube (depth 3)",
          np.array_equal(chair44_labels_at(5, 3, X, Y, Z), A))
    return ok


def _pyr_total():
    st = _chair44_load()
    S = st["S"]
    lab = S.label_table(S.CHILDREN)
    return float(sum(lab))


if __name__ == "__main__":
    if "--tests" in sys.argv:
        sys.exit(0 if run_tests() else 1)
    if not available():
        print("Spectre repository not found (set SPECTRE_DIR)")
        sys.exit(0)
    for k in FAMILY:
        p = planar_patch(k, 3)
        print("%-8s level 3: %d tiles, %d vertices, %d edges, lengths %s" % (k, len(p.polys), len(p.vert), len(p.edges), sorted(set(np.round(p.length, 4)))))
    c, l, T = chair44_cell_model(3)
    print("chair44 depth 3: %d cells, %d bonds" % (len(c), T.nnz // 2))
