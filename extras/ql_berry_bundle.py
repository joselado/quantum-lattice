#!/usr/bin/env python3
"""ql_berry_bundle.py - the Chern number of a band as the holonomy of a line bundle: a cross-check of pyqula's get_chern.

The occupied bands of a gapped Bloch Hamiltonian H(k) are a complex vector bundle over the Brillouin-zone torus with the inner
product inherited from C^n, exactly the 'structure-first' bundle of HOPF_WITHOUT_PRINCIPAL_BUNDLES.md (HopfFibration repository):
the fibre over k is the occupied subspace, the connection is the projection of the ordinary derivative back into it, and the Chern
number is the winding of the holonomy of that connection.  This script computes the Chern number three ways without using
pyqula's Chern routine, and compares with pyqula:

  (1) WILSON LOOP / winding:  for each kx, transport the occupied space once around ky with the product of overlap matrices
      M_j = <u_j | u_{j+1}> (the discrete connection); theta(kx) = arg det prod_j M_j is the Berry phase of the loop; the Chern number is
      the number of times theta winds as kx goes round (unwrapped continuously).
  (2) PROJECTOR TRANSPORT (Kato), gauge free:  the same holonomy from the product of PROJECTORS P(k_N) ... P(k_1) P(k_0) restricted to the
      occupied space at k_0 (no eigenvector phases enter at all); its eigenphases are the loop phases.
  (3) FUKUI-HATSUGAI-SUZUKI:  sum over plaquettes of the phase of the product of the four overlaps around the plaquette, divided by 2 pi.
and (4) pyqula's own h.get_chern().

Sign conventions differ between codes; the script reports the relation between the three methods and pyqula, and tests that it is the
SAME for every model.  Models: Haldane (honeycomb, pyqula), a Qi-Wu-Zhang square lattice (built with ql_common from its Bloch
Hamiltonian), two decoupled copies of it (two occupied bands, Chern number 2: this exercises the matrix-valued Wilson loop), a trivial
insulator, and kz-slices of the Hopf insulator (Chern number 0).

    python3 ql_berry_bundle.py            table
    python3 ql_berry_bundle.py --tests
"""
import math
import sys

import numpy as np

import ql_common as C


def occupied_frames(f, kx, ky, nocc=None, efermi=0.0):
    w, v = np.linalg.eigh(f([kx, ky]))
    n = int((w < efermi).sum()) if nocc is None else nocc
    return v[:, :n]


def n_occupied(f, efermi=0.0, nk=9):
    ns = {int((np.linalg.eigvalsh(f([a, b])) < efermi).sum()) for a in np.linspace(0, 1, nk, endpoint=False)
          for b in np.linspace(0, 1, nk, endpoint=False)}
    if len(ns) != 1:
        raise ValueError("not gapped at the Fermi level: occupied counts %s" % ns)
    return ns.pop()


def wilson_phase(f, kx, nky, nocc):
    """Berry phase of the loop ky: 0 -> 1 at fixed kx: arg det of the product of overlap matrices (gauge invariant mod 2 pi)."""
    ks = np.arange(nky) / nky
    U = [occupied_frames(f, kx, k, nocc) for k in ks]
    W = np.eye(nocc, dtype=complex)
    for j in range(nky):
        W = W @ (U[j].conj().T @ U[(j + 1) % nky])
    return float(np.angle(np.linalg.det(W)))


def projector_phase(f, kx, nky, nocc):
    """(2) The same loop phase from projectors only: <u_0| P(k_1) P(k_2) ... P(k_{N-1}) |u_0> = prod <u_j|u_{j+1}> (no eigenvector phases enter)."""
    ks = np.arange(nky) / nky
    Ps = []
    for k in ks:
        u = occupied_frames(f, kx, k, nocc)
        Ps.append(u @ u.conj().T)
    u0 = occupied_frames(f, kx, 0.0, nocc)
    T = np.eye(len(Ps[0]), dtype=complex)
    for j in range(1, nky):
        T = T @ Ps[j]                               # P_1 P_2 ... P_{N-1}: <u0|P_1 ... P_{N-1}|u0> = prod <u_j|u_{j+1}>
    M = u0.conj().T @ T @ u0
    return float(np.angle(np.linalg.det(M)))


def chern_from_winding(f, nocc, method="wilson", nkx=48, nky=96):
    fn = wilson_phase if method == "wilson" else projector_phase
    th = np.array([fn(f, kx, nky, nocc) for kx in np.arange(nkx + 1) / nkx])
    th = np.unwrap(th)
    return (th[-1] - th[0]) / (2 * math.pi)


def chern_fhs(f, nocc, nk=40):
    ks = np.arange(nk) / nk
    U = [[occupied_frames(f, a, b, nocc) for b in ks] for a in ks]
    tot = 0.0
    for i in range(nk):
        for j in range(nk):
            u1, u2, u3, u4 = U[i][j], U[(i + 1) % nk][j], U[(i + 1) % nk][(j + 1) % nk], U[i][(j + 1) % nk]
            p = np.linalg.det(u1.conj().T @ u2) * np.linalg.det(u2.conj().T @ u3) * np.linalg.det(u3.conj().T @ u4) * np.linalg.det(u4.conj().T @ u1)
            tot += np.angle(p)
    return tot / (2 * math.pi)


# ------------------------------------------------------------------------------------------------ models

def haldane(m3=0.05):
    from pyqula import geometry
    g = geometry.honeycomb_lattice()
    h = g.get_hamiltonian(has_spin=False)
    h.add_haldane(m3)
    return h, h.get_hk_gen()


def qwz_hk(m):
    def hk(k):
        kx, ky = k
        return np.sin(kx) * C.SIGMA[0] + np.sin(ky) * C.SIGMA[1] + (m + np.cos(kx) + np.cos(ky)) * C.SIGMA[2]
    return hk


def qwz(m=1.0):
    h, leak = C.hamiltonian_from_hk(qwz_hk(m), dim=2, nmax=1)
    return h, h.get_hk_gen()


def double_qwz(m=1.0):
    """Two uncoupled copies of QWZ: 4 orbitals, 2 occupied bands, Chern number +-2 (numpy only: pyqula's 2-orbital template is not used)."""
    hk1 = qwz_hk(m)
    return None, (lambda k: np.kron(np.eye(2), hk1(2 * np.pi * np.asarray(k))))


def hopf_slice(hh=2.0, kz=0.2):
    import ql_hopf_insulator as HI
    hop, _ = C.multihopping_from_hk(lambda k: HI.hk(k, hh), dim=3, nmax=2)
    h = HI.slice_hamiltonian(hop, 2, kz)
    return h, h.get_hk_gen()


def trivial_qwz():
    return qwz(3.0)


def table(verbose=True):
    rows = []
    for name, build, nocc_expected in (("Haldane (m3 = +0.05)", lambda: haldane(0.05), 1), ("Haldane (m3 = -0.05)", lambda: haldane(-0.05), 1),
                                       ("QWZ m = 1", lambda: qwz(1.0), 1), ("QWZ m = -1", lambda: qwz(-1.0), 1),
                                       ("QWZ m = 3 (trivial)", lambda: qwz(3.0), 1), ("Hopf-insulator slice kz = 0.2", lambda: hopf_slice(2.0, 0.2), 1),
                                       ("QWZ m = 1, two copies", lambda: double_qwz(1.0), 2)):
        h, f = build()
        nocc = n_occupied(f)
        cw = chern_from_winding(f, nocc, "wilson", 24, 60)
        cp = chern_from_winding(f, nocc, "projector", 24, 60)
        cf = chern_fhs(f, nocc, 24)
        cq = float(h.get_chern(nk=40)) if h is not None else float('nan')
        rows.append((name, nocc, cw, cp, cf, cq))
        if verbose:
            print("  %-32s nocc=%d  Wilson %+.3f  projector %+.3f  FHS %+.3f  pyqula %+.3f" % (name, nocc, cw, cp, cf, cq))
    return rows


def run_tests(verbose=True):
    ok = True

    def check(name, cond, extra=""):
        nonlocal ok
        ok &= bool(cond)
        if verbose:
            print("  %-4s %s %s" % ("ok" if cond else "FAIL", name, extra))

    rows = table(verbose)
    ints = all(abs(c - round(c)) < 0.05 for _, _, cw, cp, cf, cq in rows for c in (cw, cp, cf) + (() if math.isnan(cq) else (cq,)))
    check("every method gives an integer Chern number", ints)
    check("Wilson-loop winding = projector transport (gauge-free) = Fukui-Hatsugai-Suzuki, same sign",
          all(round(cw) == round(cp) == round(cf) for _, _, cw, cp, cf, cq in rows))
    check("pyqula's get_chern agrees in magnitude with the bundle holonomy for every model", all(abs(round(cw)) == abs(round(cq)) for _, _, cw, cp, cf, cq in rows if not math.isnan(cq)))
    sign = {round(cw) * round(cq) for _, _, cw, cp, cf, cq in rows if not math.isnan(cq) and round(cq) != 0}
    check("the sign relation between the holonomy winding and pyqula is the same for all models", len(sign) == 1,
          "(product of signs: %s; a convention difference, not a disagreement)" % sorted(sign))
    check("two decoupled QWZ copies (2 occupied bands): Chern number magnitude 2, from the matrix-valued Wilson loop",
          abs(round(rows[6][2])) == 2 and abs(round(rows[6][3])) == 2 and abs(round(rows[6][4])) == 2)
    check("Haldane m3 -> -m3 flips the Chern number; the trivial QWZ and the Hopf-insulator slice have Chern number 0",
          round(rows[0][2]) == -round(rows[1][2]) != 0 and round(rows[4][2]) == 0 and round(rows[5][2]) == 0)
    return ok


if __name__ == "__main__":
    if "--tests" in sys.argv:
        sys.exit(0 if run_tests() else 1)
    table()
