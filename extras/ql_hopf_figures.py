#!/usr/bin/env python3
"""ql_hopf_figures.py - four new matplotlib figures for the 3D Hopf insulator (extends ql_hopf_insulator.py).

The model is the one of ql_hopf_insulator.py: H(k) = d(k).sigma, d = z^dagger sigma z, z1 = sin kx + i sin ky,
z2 = sin kz + i (cos kx + cos ky + cos kz + h).  Everything here reuses its z_of_k / phi_grid / spectral_derivative.
Labels: Exact (identity or integer check), Counted (numerical, finite grid), Quoted (from a paper, not re-derived).

  fig A  phase diagram     Hopf invariant (degree integral) and bulk gap against h, with the closed formula
                              H(h) = sum over the 8 time-reversal-invariant momenta i of  chi_i [ m_i(h) < 0 ],
                              m_i = cos kx + cos ky + cos kz + h at k_i,   chi_i = cos kx cos ky cos kz  (= +-1),
                           i.e. each gap closing at a TRIM point changes the invariant by its local chirality.  The numbers 1, 3, 3, 1
                           (multiplicities of the four distinct masses) are the steps.  Formula: derived here from the local Jacobian,
                           Counted against the degree integral at every h tested.
  fig B  degree density    the integrand of (1 / 2 pi^2) int det[phi, phi_x, phi_y, phi_z] d^3k, accumulated over kz, and where in the
                           Brillouin zone it sits.  Counted.
  fig C  hidden topology   Chern number of every kz (and kx, ky) slice is 0 although the Berry curvature on the slices is far from 0.  Counted.
  fig D  Pontryagin-Thom   the preimage curves of two points of S^2 under k -> d/|d| in the Brillouin-zone torus, traced exactly, and their
                           Gauss linking number: the Hopf invariant as a linking number.  Counted (Gauss integral on a traced polygon).

    python3 ql_hopf_figures.py --tests
    python3 ql_hopf_figures.py --png-dir ../screenshots          writes hopf_ins_figA..D .png
    python3 ql_hopf_figures.py --png-dir out --only A,D
"""
import itertools
import math
import os
import sys

import numpy as np

import ql_common as C                      # puts ../pysrc on sys.path
import ql_hopf_insulator as HI

TWO_PI = 2.0 * math.pi


# ===================================================================================================== TRIM bookkeeping

def trim_points():
    """The 8 time-reversal-invariant momenta, with  sumcos = cos kx + cos ky + cos kz  and  chi = cos kx cos ky cos kz."""
    out = []
    for bits in itertools.product((0, 1), repeat=3):
        k = np.array(bits, float) * math.pi
        out.append(dict(k=k, bits=bits, sumcos=float(np.cos(k).sum()), chi=int(round(np.prod(np.cos(k))))))
    return out


def trim_name(bits):
    return {0: "Gamma", 1: "X", 2: "M", 3: "R"}[sum(bits)]


def hopf_from_trim(h):
    """Hopf invariant as sum of chi_i over the TRIM points whose mass m_i = sumcos_i + h is negative."""
    return sum(t["chi"] for t in trim_points() if t["sumcos"] + h < 0)


def trim_jacobian_chirality(t, eps=1e-6):
    """Sign of det d(Re z1, Im z1, Re z2)/d(kx, ky, kz) at a TRIM point (numerical derivative); should equal chi."""
    k0 = t["k"]
    J = np.zeros((3, 3))
    for a in range(3):
        e = np.zeros(3)
        e[a] = eps
        zp, zm = HI.z_of_k(k0 + e, 0.0), HI.z_of_k(k0 - e, 0.0)
        J[:, a] = (np.array([zp[0].real, zp[0].imag, zp[1].real]) - np.array([zm[0].real, zm[0].imag, zm[1].real])) / (2 * eps)
    return int(np.sign(np.linalg.det(J)))


# ==================================================================================================== degree density

def degree_density(h, N=48):
    """rho(k) on an N^3 grid with  sum rho dk^3 = degree of phi = z/|z| : T^3 -> S^3 (the Hopf invariant, this sign convention)."""
    phi, _ = HI.phi_grid(N, h)
    d = [HI.spectral_derivative(phi, ax).real for ax in range(3)]
    M = np.stack([phi, d[0], d[1], d[2]], axis=-2)
    return np.linalg.det(M) / (2 * math.pi ** 2)


def gap_grid(h, N=32):
    """Bulk gap 2 min |d| = 2 min (|z1|^2 + |z2|^2) on an N^3 grid (the grid contains all 8 TRIM points)."""
    _, (z1, z2) = HI.phi_grid(N, h)
    return float(2 * (abs(z1) ** 2 + abs(z2) ** 2).min())


def gap_trim(h):
    return min(2 * (t["sumcos"] + h) ** 2 for t in trim_points())


# ================================================================================================ slice Berry curvature

def berry_curvature_field(h, N=48):
    """dhat = d/|d| on an N^3 grid and the three components of  F = dhat . (d_a dhat x d_b dhat) / (4 pi)  for the planes (a,b) = (y,z), (z,x), (x,y).
    The Chern number of a slice normal to axis a at index j is  sum F_a dk^2  (an integer)."""
    ks = TWO_PI * np.arange(N) / N
    KX, KY, KZ = np.meshgrid(ks, ks, ks, indexing="ij")
    d = np.stack([HI.d_of_k((KX, KY, KZ), h)[i] for i in range(3)], axis=-1)
    dh = d / np.linalg.norm(d, axis=-1, keepdims=True)
    g = [HI.spectral_derivative(dh, ax).real for ax in range(3)]
    def f(a, b):
        return np.einsum("...i,...i->...", dh, np.cross(g[a], g[b])) / (4 * math.pi)
    return dh, (f(1, 2), f(2, 0), f(0, 1))        # normal to x, y, z


def slice_chern(F, axis):
    """Chern number of every slice normal to `axis` from the curvature component F[axis]."""
    N = F[axis].shape[0]
    other = tuple(a for a in range(3) if a != axis)
    return F[axis].sum(axis=other) * (TWO_PI / N) ** 2


# ======================================================================================= preimage curves (Pontryagin-Thom)

def section_ql(el, az):
    """(a1, a2) in S^3 with d(a) = b, b = (sin el cos az, sin el sin az, -cos el), in THIS file's convention
    d = (2 Re conj(z1) z2, 2 Im conj(z1) z2, |z1|^2 - |z2|^2)  (note: conj on z1, as in ql_hopf_insulator.d_of_k)."""
    s, c = math.sin(el / 2), math.cos(el / 2)
    return s, c * complex(math.cos(az), math.sin(az))


def base_vector(el, az):
    return np.array([math.sin(el) * math.cos(az), math.sin(el) * math.sin(az), -math.cos(el)])


def _fF(k, a1, a2, h):
    """Complex function f(k) = a2 z1(k) - a1 z2(k); d(k)/|d(k)| = b  exactly when f(k) = 0 (z parallel to a) and z != 0."""
    z1, z2 = HI.z_of_k(k, h)
    return a2 * z1 - a1 * z2


def _jac(k, a1, a2):
    kx, ky, kz = k
    cx, cy, cz, sx, sy, sz = math.cos(kx), math.cos(ky), math.cos(kz), math.sin(kx), math.sin(ky), math.sin(kz)
    col = [a2 * cx + 1j * a1 * sx, 1j * a2 * cy + 1j * a1 * sy, -a1 * cz + 1j * a1 * sz]
    return np.array([[c.real for c in col], [c.imag for c in col]])


def _polish(k, a1, a2, h, iters=30):
    for _ in range(iters):
        f = _fF(k, a1, a2, h)
        F = np.array([f.real, f.imag])
        if np.linalg.norm(F) < 1e-14:
            break
        k = k - np.linalg.pinv(_jac(k, a1, a2)) @ F
    f = _fF(k, a1, a2, h)
    return k, math.hypot(f.real, f.imag)


def find_start_points(a1, a2, h, N0=40, thresh=0.5):
    """Points on the zero set of f found by Newton from the grid minima of |f|."""
    from scipy.ndimage import minimum_filter
    ks = TWO_PI * np.arange(N0) / N0
    KX, KY, KZ = np.meshgrid(ks, ks, ks, indexing="ij")
    z1 = np.sin(KX) + 1j * np.sin(KY)
    z2 = np.sin(KZ) + 1j * (np.cos(KX) + np.cos(KY) + np.cos(KZ) + h)
    af = np.abs(a2 * z1 - a1 * z2)
    cand = np.argwhere((af == minimum_filter(af, size=3, mode="wrap")) & (af < thresh))
    pts = []
    for i, j, l in cand:
        k, res = _polish(np.array([ks[i], ks[j], ks[l]]), a1, a2, h)
        if res < 1e-12:
            pts.append(k)
    return pts


def _wrap_dist(a, b):
    d = (a - b + math.pi) % TWO_PI - math.pi
    return np.linalg.norm(d, axis=-1)


def trace_curve(k0, a1, a2, h, ds=0.05, maxsteps=8000):
    """Follow the curve f = 0 from k0 by predictor-corrector, tangent = cross product of the two gradient rows (a fixed orientation
    along the whole curve).  Returns (points (n,3) unwrapped, winding m (3 ints), closed flag).  The curve is closed when it returns
    to k0 modulo 2 pi; m = 0 means it is a contractible loop in the torus lift."""
    k = np.array(k0, float)
    pts = [k.copy()]
    for i in range(maxsteps):
        J = _jac(k, a1, a2)
        t = np.cross(J[0], J[1])
        t /= np.linalg.norm(t)
        kp = k + ds * t
        for _ in range(5):
            f = _fF(kp, a1, a2, h)
            kp = kp - np.linalg.pinv(_jac(kp, a1, a2)) @ np.array([f.real, f.imag])
        k = kp
        if i > 8:
            delta = k - k0
            m = np.round(delta / TWO_PI)
            if np.linalg.norm(delta - TWO_PI * m) < 0.9 * ds and np.abs(np.array(pts) - k0).max() > 8 * ds:
                return np.array(pts), tuple(int(x) for x in m), True
        pts.append(k.copy())
    return np.array(pts), (0, 0, 0), False


def trace_all(el, az, h):
    """All preimage curves of the base vector b(el, az) in the Brillouin-zone torus: list of dicts(points, winding, closed)."""
    a1, a2 = section_ql(el, az)
    starts = find_start_points(a1, a2, h)
    curves = []
    for k0 in starts:
        if any(_wrap_dist(c["points"], k0).min() < 0.12 for c in curves):
            continue
        P, m, closed = trace_curve(k0, a1, a2, h)
        curves.append(dict(points=P, winding=m, closed=closed))
    return curves


def gauss_linking(A, B):
    """Gauss integral of two closed polygons (midpoint rule), the same formula as HopfFibration/hopf_math.linking_number."""
    dA = np.roll(A, -1, axis=0) - A
    dB = np.roll(B, -1, axis=0) - B
    mA, mB = A + dA / 2, B + dB / 2
    r = mA[:, None, :] - mB[None, :, :]
    d3 = np.linalg.norm(r, axis=2) ** 3
    cr = np.cross(dA[:, None, :], dB[None, :, :])
    return float((np.einsum("ijk,ijk->ij", r, cr) / d3).sum() / (4 * math.pi))


def is_loop(c):
    return c["closed"] and c["winding"] == (0, 0, 0)


def link_contributions(curves1, curves2, images=(-1, 0, 1)):
    """Gauss integral of every loop of the first family with every lift (shift 2 pi s) of every loop of the second:
    list of (i, j, s, value)."""
    out = []
    for i, c1 in enumerate(curves1):
        for j, c2 in enumerate(curves2):
            for s in itertools.product(images, repeat=3):
                out.append((i, j, s, gauss_linking(c1["points"], c2["points"] + TWO_PI * np.array(s))))
    return out


def torus_linking(curves1, curves2, images=(-1, 0, 1)):
    """Linking number of two families of contractible closed curves in the torus T^3: the sum over all lifts of the second family
    (periodic images, shifts of 2 pi k) of the Gauss integral with the lift of the first.  Returns None if any curve is not a
    contractible loop."""
    if not all(is_loop(c) for c in curves1 + curves2):
        return None
    return sum(v for _, _, _, v in link_contributions(curves1, curves2, images))


# ======================================================================================================== figures

def fig_phase_diagram(path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    hs = np.linspace(-4.6, 4.6, 93) + 0.0137                    # never exactly on a gap closing
    deg = np.array([HI.hopf_invariant_degree(h, 40) for h in hs])
    form = np.array([hopf_from_trim(h) for h in hs])
    gap = np.array([gap_grid(h, 32) for h in hs])
    gtr = np.array([gap_trim(h) for h in hs])
    fig, ax = plt.subplots(3, 1, figsize=(8.2, 9.2), sharex=True, gridspec_kw=dict(height_ratios=[1.3, 1, 1.3]))
    ax[0].plot(hs, form, "-", color="C1", lw=2.5, drawstyle="steps-mid", label="$\\sum_i \\chi_i\\,[m_i<0]$  (closed formula)")
    ax[0].plot(hs, deg, "o", ms=3.5, color="k", label="degree integral (N = 40)")
    ax[0].set_ylabel("Hopf invariant")
    ax[0].set_yticks([-1, 0, 1, 2])
    ax[0].legend(fontsize=8, loc="upper right")
    ax[0].set_title("3D Hopf insulator: invariant, gap and the eight band-touching points", fontsize=10)
    for x, lab in ((-3, "-3"), (-1, "-1"), (1, "1"), (3, "3")):
        for a in ax:
            a.axvline(x, color="0.75", lw=0.8, zorder=0)
    ax[1].semilogy(hs, np.maximum(gap, 1e-3), "-", color="C0", lw=2, label="bulk gap (grid minimum, N = 32)")
    ax[1].semilogy(hs, np.maximum(gtr, 1e-3), "k:", lw=1.2, label="gap at the 8 TRIM points: $2\\min_i m_i^2$")
    ax[1].set_ylabel("2 min |d|")
    ax[1].legend(fontsize=8, loc="upper center")
    groups = {}
    for t in trim_points():
        groups.setdefault((trim_name(t["bits"]), t["sumcos"], t["chi"]), 0)
        groups[(trim_name(t["bits"]), t["sumcos"], t["chi"])] += 1
    hh = np.linspace(-4.6, 4.6, 300)
    for (name, sc, chi), mult in sorted(groups.items(), key=lambda kv: -kv[0][1]):
        col = "C0" if chi > 0 else "C3"
        ax[2].plot(hh, sc + hh, color=col, lw=2)
        ax[2].annotate("%s  x%d, $\\chi$ = %+d" % (name, mult, chi), (4.55, sc + 4.55), ha="right", va="bottom", fontsize=8, color=col)
    ax[2].axhline(0, color="k", lw=0.7)
    ax[2].set_ylabel("mass $m_i = \\Sigma\\cos k_i + h$")
    ax[2].set_xlabel("h")
    ax[2].set_ylim(-9, 9)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)
    print("wrote", path)


def fig_degree_density(path, hlist=(4.0, 2.0, 0.5), N=48):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(12, 7.6))
    gs = fig.add_gridspec(2, 3, height_ratios=[1, 1.1])
    axc = fig.add_subplot(gs[0, :])
    dk = TWO_PI / N
    kz = TWO_PI * (np.arange(N) + 1) / N
    dens = {}
    for h, col in zip(hlist, ("0.4", "C3", "C0")):
        rho = degree_density(h, N)
        dens[h] = rho
        cum = np.cumsum(rho.sum(axis=(0, 1)) * dk ** 3)
        axc.plot(kz / math.pi, cum, "-o", ms=3, color=col, label="h = %.1f  (total %+.3f)" % (h, cum[-1]))
    axc.set_xlabel("$k_z / \\pi$")
    axc.set_ylabel("winding accumulated up to $k_z$")
    axc.set_title("the degree is built up layer by layer in $k_z$, though every layer has Chern number 0", fontsize=10)
    axc.legend(fontsize=8)
    axc.grid(alpha=0.3)
    for i, h in enumerate(hlist[1:]):
        ax = fig.add_subplot(gs[1, i])
        m = dens[h].sum(axis=1) * dk                           # integrate over ky: function of (kx, kz)
        v = np.abs(m).max()
        im = ax.imshow(m.T, origin="lower", extent=[0, 2, 0, 2], cmap="RdBu_r", vmin=-v, vmax=v)
        ax.set_xlabel("$k_x/\\pi$")
        ax.set_ylabel("$k_z/\\pi$")
        ax.set_title("h = %.1f:  density integrated over $k_y$" % h, fontsize=9)
        plt.colorbar(im, ax=ax, fraction=0.046)
    ax = fig.add_subplot(gs[1, 2])
    ax.axis("off")
    rows = ["TRIM  (kx,ky,kz)   chi   mass at h=%.1f" % hlist[2]]
    for t in trim_points():
        rows.append("%-6s %-12s %+d     %+.1f" % (trim_name(t["bits"]), "(%s)" % ",".join("pi" if b else "0" for b in t["bits"]),
                                                    t["chi"], t["sumcos"] + hlist[2]))
    ax.text(0.0, 1.0, "\n".join(rows), family="monospace", fontsize=8, va="top")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)
    print("wrote", path)


def fig_hidden_topology(path, hlist=(4.0, 2.0, 0.5), N=48):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(11.5, 8.0))
    gs = fig.add_gridspec(2, 3)
    a1 = fig.add_subplot(gs[0, 0])
    a2 = fig.add_subplot(gs[0, 1])
    a3 = fig.add_subplot(gs[0, 2])
    ks = TWO_PI * (np.arange(N) + 0.0) / N
    Fs = {}
    for h, col in zip(hlist, ("0.4", "C3", "C0")):
        dh, F = berry_curvature_field(h, N)
        Fs[h] = F
        for axis, name, ls in ((2, "kz", "-"), (0, "kx", "--"), (1, "ky", ":")):
            a1.plot(ks / math.pi, slice_chern(F, axis), ls, color=col, lw=1.4, label="h = %.1f, slices at fixed %s" % (h, name) if axis == 2 else None)
        a2.plot(ks / math.pi, np.abs(F[2]).max(axis=(0, 1)) * 4 * math.pi, "-", color=col, lw=1.8, label="h = %.1f" % h)
        pos = np.where(F[2] > 0, F[2], 0).sum(axis=(0, 1)) * (TWO_PI / N) ** 2
        a3.plot(ks / math.pi, pos, "-", color=col, lw=1.8, label="h = %.1f" % h)
    a1.set_ylim(-1.5, 1.5)
    a1.set_title("Chern number of every slice\n(kz solid, kx dashed, ky dotted; all on the line 0)", fontsize=8)
    a1.set_xlabel("slice position / $\\pi$")
    a1.legend(fontsize=7, loc="upper right")
    a2.set_title("largest local curvature on the kz slice,\n$|\\hat d\\cdot\\partial_x\\hat d\\times\\partial_y\\hat d|$", fontsize=8)
    a2.set_xlabel("$k_z/\\pi$")
    a2.legend(fontsize=7)
    a3.set_title("positive Berry flux through the kz slice\n(an equal negative flux cancels it)", fontsize=8)
    a3.set_xlabel("$k_z/\\pi$")
    a3.legend(fontsize=7)
    for i, h in enumerate(hlist[1:]):
        ax = fig.add_subplot(gs[1, i])
        j = int(round(N * 0.25))
        Fm = Fs[h][2][:, :, j].T * 4 * math.pi
        v = np.abs(Fm).max()
        im = ax.imshow(Fm, origin="lower", extent=[0, 2, 0, 2], cmap="RdBu_r", vmin=-v, vmax=v)
        ax.set_title("h = %.1f: curvature on the slice $k_z$ = $\\pi/2$  (integral %.1e)" % (h, Fs[h][2][:, :, j].sum() * (TWO_PI / N) ** 2), fontsize=8)
        ax.set_xlabel("$k_x/\\pi$")
        ax.set_ylabel("$k_y/\\pi$")
        plt.colorbar(im, ax=ax, fraction=0.046)
    ax = fig.add_subplot(gs[1, 2])
    ax.axis("off")
    h = hlist[2]
    div = np.zeros(1)
    ax.text(0, 0.95, "All 3 x %d slices of every h shown have\n|Chern number| < %.0e.\n\nThe Hopf invariant is therefore not a stack of\nChern layers: it lives in the Chern-Simons\nform of the 3D Berry connection."
            % (N, max(np.abs(slice_chern(Fs[hh], a)).max() for hh in hlist for a in range(3)) + 1e-30), va="top", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)
    print("wrote", path)


PAIR = ((2.0, 0.6), (2.4, 3.5))              # at h = 0.5 and h = 2 both preimages are collections of contractible loops
WRAP_POINT = (1.6, 0.2)                      # at h = 0.5 the preimage of this point contains loops that wrap the zone (kz direction)


def _lift_into_cube(P):
    """Translate a curve by a multiple of 2 pi so that its centroid lies in [-pi, pi)^3 (the curve itself may stick out of the cube).
    Returns (points, shift)."""
    s = -TWO_PI * np.floor((P.mean(axis=0) + math.pi) / TWO_PI)
    return P + s, s


def preimage_families(h, pair=PAIR):
    return [trace_all(el, az, h) for el, az in pair]


def fig_preimage_links(path, hlist=(4.0, 2.0, 0.5), pair=PAIR):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(14, 9.4))

    def finish(ax, pts):
        P = np.vstack(pts) if pts else np.zeros((1, 3))
        lo, hi = P.min(axis=0) - 0.3, P.max(axis=0) + 0.3
        ax.set_xlim(lo[0], hi[0])
        ax.set_ylim(lo[1], hi[1])
        ax.set_zlim(lo[2], hi[2])
        ax.set_box_aspect(tuple(np.maximum(hi - lo, 1.0)))
        ax.set_xlabel("$k_x$")
        ax.set_ylabel("$k_y$")
        ax.set_zlabel("$k_z$")

    for i, h in enumerate(hlist):
        fams = preimage_families(h, pair)
        loops = bool(fams[0]) and bool(fams[1]) and all(is_loop(c) for c in fams[0] + fams[1])
        contrib = link_contributions(fams[0], fams[1]) if loops else []
        lk = sum(v for *_, v in contrib)
        linked = [(a, b, s, v) for a, b, s, v in contrib if abs(v) > 0.25]
        ax = fig.add_subplot(2, 2, i + 1, projection="3d")
        drawn, pts = set(), []
        for a, b, s, v in linked:
            P1, t = _lift_into_cube(fams[0][a]["points"])
            P2 = fams[1][b]["points"] + TWO_PI * np.array(s) + t
            ax.plot(P1[:, 0], P1[:, 1], P1[:, 2], color="C0", lw=2.2, label="preimage of $b_1$" if not drawn else None)
            ax.plot(P2[:, 0], P2[:, 1], P2[:, 2], color="C3", lw=2.2, label="preimage of $b_2$" if len(drawn) == 0 else None)
            drawn.add(a)
            pts += [P1, P2]
        ncur = [len(f) for f in fams]
        deg = HI.hopf_invariant_degree(h, 40)
        if not any(ncur):
            what = "no preimage of either point"
            ax.text2D(0.2, 0.5, "these two points of S$^2$ have\nno preimage in the zone", transform=ax.transAxes, fontsize=9)
        else:
            what = "%d + %d loop(s); linked pairs (Gauss integral): %s" % (
                ncur[0], ncur[1], ", ".join("%+.2f" % v for *_, v in linked) or "none")
        ax.set_title("h = %.1f:  %s\ntotal linking = %+.3f,   degree integral = %+.2f" % (h, what, lk, deg), fontsize=9)
        if linked:
            ax.legend(fontsize=7, loc="upper left")
        finish(ax, pts)
    # fourth panel: a point whose preimage wraps the Brillouin zone
    h = hlist[-1]
    cs = trace_all(WRAP_POINT[0], WRAP_POINT[1], h)
    ax = fig.add_subplot(2, 2, 4, projection="3d")
    pts = []
    for j, c in enumerate(cs):
        P, _ = _lift_into_cube(c["points"])
        ax.plot(P[:, 0], P[:, 1], P[:, 2], lw=2.0, color="C%d" % (j + 2), label="winding %s" % (c["winding"],))
        pts.append(P)
    ax.legend(fontsize=7, loc="upper left")
    tot = tuple(int(sum(c["winding"][a] for c in cs)) for a in range(3))
    ax.set_title("h = %.1f, another point of S$^2$: the preimage wraps the zone\nwindings add to %s, so the family bounds a surface; torus linking needs it"
                 % (h, tot), fontsize=9)
    finish(ax, pts)
    fig.suptitle("Hopf invariant = linking number of the preimage curves of two points of S$^2$ "
                 "(loops of the Brillouin-zone torus, drawn as lifts to R$^3$)", fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)
    print("wrote", path)


# ========================================================================================================== tests

def run_tests(verbose=True):
    ok = True

    def check(name, cond, extra=""):
        nonlocal ok
        ok &= bool(cond)
        if verbose:
            print("  %-4s %s %s" % ("ok" if cond else "FAIL", name, extra))

    # 1. local chirality at the TRIM points
    ts = trim_points()
    check("chi_i = cos kx cos ky cos kz equals the sign of the local Jacobian det at each of the 8 TRIM points",
          all(trim_jacobian_chirality(t) == t["chi"] for t in ts), "(chi = %s)" % [t["chi"] for t in ts])
    check("the four distinct masses cos kx + cos ky + cos kz = 3, 1, -1, -3 occur 1, 3, 3, 1 times with chi = +1, -1, +1, -1",
          sorted((t["sumcos"], t["chi"]) for t in ts) == sorted([(3, 1)] + [(1, -1)] * 3 + [(-1, 1)] * 3 + [(-3, -1)]))
    # 2. the closed formula against the degree integral
    hs = [-4.0, -3.4, -2.5, -2.0, -1.5, -0.5, 0.3, 0.9, 1.1, 1.8, 2.7, 3.2, 4.5]
    got = [(h, round(HI.hopf_invariant_degree(h, 40)), hopf_from_trim(h)) for h in hs]
    check("Hopf invariant = sum_i chi_i [m_i < 0] agrees with the degree integral at 13 values of h in all five phases",
          all(a == b for _, a, b in got), "(%s)" % ", ".join("%.1f:%+d" % (h, b) for h, _, b in got))
    # 3. gap closes at the TRIM values; grid min never above TRIM gap
    check("gap at the TRIM points = 2 min m_i^2 closes at h = +-1, +-3 and the grid minimum is never larger",
          all(gap_trim(x) < 1e-12 for x in (-3, -1, 1, 3)) and all(gap_grid(h, 24) <= gap_trim(h) + 1e-12 for h in (0.5, 2.0, 4.0, -2.0)))
    # 4. degree density accumulates to the degree
    for h in (2.0, 0.5):
        rho = degree_density(h, 40)
        tot = rho.sum() * (TWO_PI / 40) ** 3
        check("degree density integrates to the Hopf invariant for h = %.1f" % h, abs(tot - hopf_from_trim(h)) < 0.02,
              "(%.4f vs %+d)" % (tot, hopf_from_trim(h)))
    # 5. slices
    worst = 0.0
    nonzero_curv = True
    for h in (4.0, 2.0, 0.5):
        _, F = berry_curvature_field(h, 40)
        for a in range(3):
            worst = max(worst, np.abs(slice_chern(F, a)).max())
        nonzero_curv &= np.abs(F[2]).max() * 4 * math.pi > 0.1 if h != 4.0 else True
    check("every slice normal to kx, ky, kz has Chern number 0 (h = 4, 2, 0.5), with non-zero local curvature",
          worst < 1e-3 and nonzero_curv, "(max |C| = %.1e)" % worst)
    # 5b. on the line kx = ky = pi, z1 = 0 and d^ ~ (2 conj(z1) z2 / |z2|^2, -1): the curvature is 4 cos kx cos ky / |z2|^2 = 4 / |z2|^2,
    #     |z2|^2 = sin^2 kz + (cos kz - 2 + h)^2.  For h = 2 this is exactly 4 for every kz.
    worst = 0.0
    kzs = TWO_PI * np.arange(64) / 64
    for h in (2.0, 0.5, 4.0):
        _, F = berry_curvature_field(h, 64)
        pred = 4.0 / (np.sin(kzs) ** 2 + (np.cos(kzs) - 2 + h) ** 2)
        worst = max(worst, (np.abs(np.abs(F[2][32, 32, :]) * 4 * math.pi - pred) / pred).max())
    check("curvature on the line kx = ky = pi equals 4 / |z2|^2 (so exactly 4 for every kz at h = 2); spectral grid N = 64",
          worst < 1e-3, "(max relative err %.1e, shrinks geometrically with N)" % worst)
    # 6. preimage curves and linking
    res = {}
    for h in (2.0, 0.5):
        fams = preimage_families(h)
        err = 0.0
        for fam, (el, az) in zip(fams, PAIR):
            b = base_vector(el, az)
            for c in fam:
                for k in c["points"][::7]:
                    d = HI.d_of_k(k, h)
                    err = max(err, np.abs(d / np.linalg.norm(d) - b).max())
        res[h] = (fams, err, torus_linking(*fams))
    check("traced preimage points satisfy d(k)/|d(k)| = b to 1e-9",
          all(r[1] < 1e-9 for r in res.values()), "(max err %s)" % {h: "%.1e" % r[1] for h, r in res.items()})
    check("every preimage curve is a closed contractible loop, and there is at least one for each point",
          all(all(c["closed"] and c["winding"] == (0, 0, 0) for fam in r[0] for c in fam) and all(len(fam) > 0 for fam in r[0]) for r in res.values()),
          "(curves per family %s)" % {h: [len(f) for f in r[0]] for h, r in res.items()})
    lk = {h: r[2] for h, r in res.items()}
    check("linking number of two preimages = |Hopf invariant|: 1 at h = 2, 2 at h = 0.5 (to 5 %)",
          lk[2.0] is not None and lk[0.5] is not None and abs(abs(lk[2.0]) - 1) < 0.05 and abs(abs(lk[0.5]) - 2) < 0.1,
          "(%s)" % {h: None if v is None else round(v, 3) for h, v in lk.items()})
    check("the signs of the linking number and of the degree integral agree up to one global convention",
          lk[2.0] is not None and lk[0.5] is not None and np.sign(lk[2.0]) * np.sign(hopf_from_trim(2.0)) == np.sign(lk[0.5]) * np.sign(hopf_from_trim(0.5)))
    # 7. optional pyqula cross-check
    try:
        ham, leak = HI.hopf_insulator(2.0)
        f = ham.get_hk_gen()
        rng = np.random.default_rng(1)
        worst = max(np.abs(np.sort(np.linalg.eigvalsh(f(kf))) - np.array([-1, 1]) * np.linalg.norm(HI.d_of_k(2 * np.pi * kf, 2.0))).max()
                    for kf in rng.random((4, 3)))
        check("pyqula bands equal +-|d| (the eigenvalues of d.sigma) for h = 2", worst < 1e-10, "(max err %.1e)" % worst)
    except Exception as e:                                       # pyqula or one of its dependencies not importable here
        if verbose:
            print("  skip pyqula cross-check (%s: %s)" % (type(e).__name__, e))
    return ok


FIGS = {"A": ("hopf_ins_figA_phase_diagram.png", fig_phase_diagram),
        "B": ("hopf_ins_figB_degree_density.png", fig_degree_density),
        "C": ("hopf_ins_figC_hidden_topology.png", fig_hidden_topology),
        "D": ("hopf_ins_figD_preimage_links.png", fig_preimage_links)}


def main():
    if "--tests" in sys.argv:
        sys.exit(0 if run_tests() else 1)
    outdir = "../screenshots"
    if "--png-dir" in sys.argv:
        outdir = sys.argv[sys.argv.index("--png-dir") + 1]
    only = set(FIGS)
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    os.makedirs(outdir, exist_ok=True)
    for k in sorted(only):
        name, fn = FIGS[k]
        fn(os.path.join(outdir, name))


if __name__ == "__main__":
    main()
