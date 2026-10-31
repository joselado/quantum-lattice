#!/usr/bin/env python3
"""ql_hopf_insulator.py - the three-dimensional HOPF INSULATOR in pyqula, and three independent computations of its Hopf invariant.

The model (Moore, Ran, Wen, PRL 100, 186805 (2008); see also Deng, Wang, Yu, Yang, PRB 88, 201105 (2013)) has two bands, H(k) = d(k).sigma,
with d the Hopf map of the spinor  z = (z1, z2):
        z1 = sin kx + i sin ky,      z2 = sin kz + i (cos kx + cos ky + cos kz + h),
        d = z^dagger sigma z   (so |d| = |z1|^2 + |z2|^2 and the bands are E = +- |d|).
The gap closes only where z = 0, i.e. at the 8 points k_i in {0, pi} with cos kx + cos ky + cos kz + h = 0: h in {-3, -1, 1, 3}.
Between those values the map  k -> d/|d|  from the Brillouin-zone torus T^3 to S^2 has an integer Hopf invariant.

Why it is a Hopf fibration problem: d/|d| = hopf(z/|z|) is the composition of  phi = z/|z| : T^3 -> S^3  with the Hopf map S^3 -> S^2, so the
Hopf invariant of the band map is the DEGREE of phi.  The occupied band is the line bundle pulled back from the Hopf (tautological) line
bundle.  Three computations, all independent:
  (1) DEGREE INTEGRAL     deg phi = (1 / 2 pi^2) * integral over T^3 of det[phi, d_x phi, d_y phi, d_z phi]  (pull-back of the S^3 volume form,
                          spectral derivatives on an N^3 grid).
  (2) SIGNED PREIMAGE COUNT   sum over the solutions of phi(k) = w (Newton from many starts) of the sign of the local Jacobian, for a few
                          regular values w.  (Counting preimages of a point is how the degree is defined.)
  (3) CHERN-SIMONS        chi = (1 / 4 pi^2) * integral of A.(curl A) d^3k  for the Berry connection A = i <u | grad u> of the OCCUPIED band, in
                          the explicit smooth global gauge  u = (-conj z2, conj z1)/|z|.  (z itself is the upper-band eigenvector.)
They agree (to the numerical accuracy) and take the values listed by `python3 ql_hopf_insulator.py` for each h.  Sign: there is no
absolute sign for the Hopf invariant without fixing orientation conventions; here it is the degree defined by (1) with the axis order
(kx, ky, kz) and the S^3 coordinates (Re z1, Im z1, Re z2, Im z2), and (3) is reported with the sign that makes it equal (1) (its sign
depends on the convention for A).
Also checked: pyqula's own Bloch Hamiltonian for this model equals d.sigma; every 2D slice kz = const (and kx, ky) is a trivial insulator with
Chern number 0 (pyqula's get_chern) - the Hopf invariant is a genuinely 3D invariant, not a stack of Chern layers.

    python3 ql_hopf_insulator.py              table over h
    python3 ql_hopf_insulator.py --tests
    python3 ql_hopf_insulator.py --png ../screenshots/hopf_insulator.png      (slab surface spectrum)
"""
import itertools
import math
import sys

import numpy as np

import ql_common as C


def z_of_k(k, h):
    kx, ky, kz = k
    return np.array([np.sin(kx) + 1j * np.sin(ky), np.sin(kz) + 1j * (np.cos(kx) + np.cos(ky) + np.cos(kz) + h)])


def d_of_k(k, h):
    z1, z2 = z_of_k(k, h)
    w = np.conj(z1) * z2
    return np.array([2 * w.real, 2 * w.imag, abs(z1) ** 2 - abs(z2) ** 2])


def hk(k, h):
    return sum(d * s for d, s in zip(d_of_k(k, h), C.SIGMA))


def hopf_insulator(h, nmax=2):
    """pyqula Hamiltonian of the Hopf insulator with parameter h (cubic lattice, two orbitals)."""
    ham, leak = C.hamiltonian_from_hk(lambda k: hk(k, h), dim=3, nmax=nmax)
    return ham, leak


def phi_grid(N, h):
    """phi = z/|z| in R^4 on an N^3 periodic grid: array (N, N, N, 4)."""
    ks = 2 * np.pi * np.arange(N) / N
    KX, KY, KZ = np.meshgrid(ks, ks, ks, indexing="ij")
    z1 = np.sin(KX) + 1j * np.sin(KY)
    z2 = np.sin(KZ) + 1j * (np.cos(KX) + np.cos(KY) + np.cos(KZ) + h)
    n = np.sqrt(abs(z1) ** 2 + abs(z2) ** 2)
    return np.stack([z1.real / n, z1.imag / n, z2.real / n, z2.imag / n], axis=-1), (z1, z2)


def spectral_derivative(f, axis):
    """Derivative (w.r.t. angle k) of a periodic grid function along `axis` by FFT."""
    N = f.shape[axis]
    freq = np.fft.fftfreq(N, d=1.0 / N)
    shape = [1] * f.ndim
    shape[axis] = N
    F = np.fft.fft(f, axis=axis)
    return np.fft.ifft(1j * freq.reshape(shape) * F, axis=axis)


def hopf_invariant_degree(h, N=48):
    """(1) degree of phi: T^3 -> S^3 from the pulled-back volume form, (1/2 pi^2) int det[phi, phi_x, phi_y, phi_z]."""
    phi, _ = phi_grid(N, h)
    d = [spectral_derivative(phi, ax).real for ax in range(3)]
    M = np.stack([phi, d[0], d[1], d[2]], axis=-2)                  # (..., 4 rows, 4 comps)
    vol = np.linalg.det(M)
    return float(vol.mean() * (2 * np.pi) ** 3 / (2 * np.pi ** 2))


def _phi_vec(k, h):
    z = z_of_k(k, h)
    v = np.array([z[0].real, z[0].imag, z[1].real, z[1].imag])
    return v / np.linalg.norm(v)


def signed_preimage_count(h, w, starts=7, seed=0):
    """(2) sum of local degrees over the solutions of phi(k) = w, found by Newton's method from starts^3 initial points.
    Returns (degree, number of distinct preimages)."""
    w = np.asarray(w, float) / np.linalg.norm(w)
    # orthonormal basis Q of w-perp with det[w, Q] > 0
    M = np.linalg.qr(np.c_[w, np.eye(4)[:, :3] + 0.1 * np.arange(12).reshape(4, 3)])[0]
    Q = M[:, 1:4]
    if np.linalg.det(np.c_[w, Q]) < 0:
        Q[:, 2] *= -1

    def F(k):
        z = z_of_k(k, h)
        v = np.array([z[0].real, z[0].imag, z[1].real, z[1].imag])
        return Q.T @ v                                              # vanishes where z is parallel to w (either sign)

    def J(k, eps=1e-6):
        return np.array([(F(k + eps * e) - F(k - eps * e)) / (2 * eps) for e in np.eye(3)]).T

    roots = []
    rng = np.random.default_rng(seed)
    for k0 in itertools.product(np.linspace(0, 2 * np.pi, starts, endpoint=False), repeat=3):
        k = np.array(k0) + 0.1 * rng.normal(size=3)
        for _ in range(60):
            f = F(k)
            Jk = J(k)
            try:
                step = np.linalg.solve(Jk, -f)
            except np.linalg.LinAlgError:
                break
            k = k + np.clip(step, -0.5, 0.5)
            if np.linalg.norm(f) < 1e-13:
                break
        if np.linalg.norm(F(k)) < 1e-10:
            phi = _phi_vec(k, h)
            if phi @ w > 0:                                         # phi = +w, not -w
                kk = np.mod(k, 2 * np.pi)
                if not any(np.linalg.norm(np.mod(kk - r[0] + np.pi, 2 * np.pi) - np.pi) < 1e-5 for r in roots):
                    roots.append((kk, int(np.sign(np.linalg.det(J(k))))))
    return sum(s for _, s in roots), len(roots)


def chern_simons(h, N=48):
    """(3) (1 / 4 pi^2) int A . curl A d^3k for the occupied band in the smooth gauge u = (-conj z2, conj z1)/|z|;
    the sign convention of A is fixed in the docstring of the module."""
    _, (z1, z2) = phi_grid(N, h)
    n = np.sqrt(abs(z1) ** 2 + abs(z2) ** 2)
    u = np.stack([-np.conj(z2) / n, np.conj(z1) / n], axis=-1)
    A = []
    for ax in range(3):
        du = spectral_derivative(u, ax)
        A.append((1j * np.einsum("...i,...i->...", np.conj(u), du)).real)
    A = np.stack(A, axis=-1)                                        # (N,N,N,3)
    curl = np.stack([spectral_derivative(A[..., 2], 1).real - spectral_derivative(A[..., 1], 2).real,
                     spectral_derivative(A[..., 0], 2).real - spectral_derivative(A[..., 2], 0).real,
                     spectral_derivative(A[..., 1], 0).real - spectral_derivative(A[..., 0], 1).real], axis=-1)
    return float((A * curl).sum(-1).mean() * (2 * np.pi) ** 3 / (4 * np.pi ** 2))


def bulk_gap(h, N=24):
    ks = 2 * np.pi * np.arange(N) / N
    best = 1e9
    for k in itertools.product(ks, repeat=3):
        z = z_of_k(k, h)
        best = min(best, 2 * (abs(z[0]) ** 2 + abs(z[1]) ** 2))
    return best


def slice_hamiltonian(ham_dict_hop, axis, kfrac):
    """2D pyqula Hamiltonian obtained by fixing the momentum along `axis` (0,1,2) at fractional kfrac: sums hoppings with e^{+i 2 pi k R}."""
    from pyqula import geometry
    from pyqula.multihopping import MultiHopping
    out = {}
    others = [a for a in range(3) if a != axis]
    for R, m in ham_dict_hop.items():
        key = (R[others[0]], R[others[1]], 0)
        out[key] = out.get(key, 0) + m * np.exp(2j * np.pi * kfrac * R[axis])
    g = geometry.square_lattice()
    hh = g.get_hamiltonian(has_spin=True)
    hh.set_multihopping(MultiHopping(out))
    return hh


def slab_spectrum(h, nz=16, nk=61):
    """Open boundary in z with nz layers; spectrum along kx = ky = k (fractional 0..0.5) and along the Gamma-X-M-Gamma path.
    Returns (path labels, k parameter, energies (nk, 2 nz), weight on the outer 2 layers per state (nk, 2 nz))."""
    hop, _ = C.multihopping_from_hk(lambda k: hk(k, h), dim=3, nmax=2)
    nmax = 2

    def Hslab(kx, ky):
        H = np.zeros((2 * nz, 2 * nz), complex)
        for R, m in hop.items():
            ph = np.exp(1j * (kx * R[0] + ky * R[1]))
            for z in range(nz):
                z2 = z + R[2]
                if 0 <= z2 < nz:
                    H[2 * z:2 * z + 2, 2 * z2:2 * z2 + 2] += m * ph
        return H

    pts = [(0, 0), (np.pi, 0), (np.pi, np.pi), (0, 0)]
    path = []
    for (a, b), (c, d) in zip(pts[:-1], pts[1:]):
        for t in np.linspace(0, 1, nk // 3, endpoint=False):
            path.append(((1 - t) * a + t * c, (1 - t) * b + t * d))
    path.append(pts[-1])
    E = np.zeros((len(path), 2 * nz))
    Wt = np.zeros_like(E)
    for i, (kx, ky) in enumerate(path):
        w, v = np.linalg.eigh(Hslab(kx, ky))
        E[i] = w
        dens = (np.abs(v) ** 2).reshape(nz, 2, 2 * nz).sum(1)       # (layer, state)
        Wt[i] = dens[:2].sum(0) + dens[-2:].sum(0)
    return np.arange(len(path)), E, Wt


def run_tests(verbose=True):
    ok = True

    def check(name, cond, extra=""):
        nonlocal ok
        ok &= bool(cond)
        if verbose:
            print("  %-4s %s %s" % ("ok" if cond else "FAIL", name, extra))

    # pyqula's Bloch Hamiltonian = d.sigma
    ham, leak = hopf_insulator(2.0)
    f = ham.get_hk_gen()
    rng = np.random.default_rng(0)
    worst = 0.0
    for _ in range(6):
        kf = rng.random(3)
        worst = max(worst, np.abs(f(kf) - hk(2 * np.pi * kf, 2.0)).max())
    check("pyqula Hamiltonian (hoppings up to 2 cells) reproduces d.sigma", worst < 1e-12 and leak < 1e-12, "(max err %.1e)" % worst)
    # gap closes exactly at h = +-1, +-3
    check("gap closes at the predicted values h = +-1, +-3 and is open between",
          all(bulk_gap(x, 12) < 1e-9 for x in (-3, -1, 1, 3)) and all(bulk_gap(x, 24) > 0.05 for x in (0.5, 2.0, 4.0, -2.0)))
    # three computations of the Hopf invariant
    rows = {}
    for hh in (0.5, 2.0, 4.0, -2.0):
        deg = hopf_invariant_degree(hh, 40)
        cs = chern_simons(hh, 40)
        pc = [signed_preimage_count(hh, w, 5)[0] for w in ([1, 0, 0, 0], [0.3, -0.5, 0.7, 0.2])]
        rows[hh] = (deg, cs, pc)
        if verbose:
            print("       h = %+.1f   degree integral %+.4f   Chern-Simons %+.4f   signed preimage counts %s" % (hh, deg, cs, pc))
    check("the degree is an integer for each h", all(abs(d - round(d)) < 0.02 for d, _, _ in rows.values()))
    check("Hopf invariant (this sign convention): 0 for |h| > 3, -1 for 1 < |h| < 3 (h and -h alike), +2 for |h| < 1",
          [round(rows[x][0]) for x in (4.0, 2.0, -2.0, 0.5)] == [0, -1, -1, 2])
    check("(2) signed preimage counts equal the degree integral for every regular value tested",
          all(all(p == round(d) for p in pc) for d, _, pc in rows.values()))
    check("(3) Chern-Simons equals (1) up to an overall sign convention", all(abs(abs(cs) - abs(d)) < 0.03 for d, cs, _ in rows.values())
          and len({np.sign(round(cs)) * np.sign(round(d)) for d, cs, _ in rows.values() if abs(round(d)) > 0}) == 1)
    # 2D slices are trivial
    hop, _ = C.multihopping_from_hk(lambda k: hk(k, 2.0), dim=3, nmax=2)
    cher = []
    for axis in range(3):
        for kfrac in (0.13, 0.4):
            hs = slice_hamiltonian(hop, axis, kfrac)
            cher.append(round(float(hs.get_chern(nk=40)), 3))
    check("every tested 2D slice has Chern number 0 (pyqula get_chern)", all(abs(c) < 1e-3 for c in cher), "(%s)" % cher)
    # surface states of a finite slab (numpy diagonalisation, 16 layers): in-gap states with weight > 0.7 on the outer four layers
    def n_surface(hh):
        x, E, W = slab_spectrum(hh, 16, 61)
        g = bulk_gap(hh, 16)
        return int(((np.abs(E) < 0.45 * g) & (W > 0.7)).sum())
    ns = {hh: n_surface(hh) for hh in (2.0, 0.5, 4.0)}
    check("slab: surface-localised in-gap states exist in the Hopf phases (h = 2, 0.5) and not in the trivial phase (h = 4)",
          ns[2.0] > 0 and ns[0.5] > 0 and ns[4.0] == 0, "(counts %s; finite slab and k-mesh, gaplessness NOT claimed)" % ns)
    return ok


def figure(path, h=2.0, nz=16):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    x, E, Wt = slab_spectrum(h, nz)
    gap = bulk_gap(h)
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    sc = None
    for j in range(E.shape[1]):
        sc = ax.scatter(x, E[:, j], c=Wt[:, j], cmap="viridis", vmin=0, vmax=1, s=4)
    ax.axhline(0, color="0.7", lw=0.5)
    ax.set_xlabel("Gamma - X - M - Gamma")
    ax.set_ylabel("energy")
    ax.set_title("Hopf insulator slab (%d layers, h=%.1f); colour = weight on the outer 2 layers each side" % (nz, h), fontsize=8)
    plt.colorbar(sc, ax=ax)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    print("wrote", path)


def main():
    if "--tests" in sys.argv:
        sys.exit(0 if run_tests() else 1)
    if "--png" in sys.argv:
        figure(sys.argv[sys.argv.index("--png") + 1])
        return
    print("h        bulk gap    degree     Chern-Simons")
    for hh in (-4.0, -2.0, -0.5, 0.5, 2.0, 4.0):
        print("%+5.1f   %8.4f   %+8.4f   %+8.4f" % (hh, bulk_gap(hh, 16), hopf_invariant_degree(hh, 40), chern_simons(hh, 40)))


if __name__ == "__main__":
    main()
