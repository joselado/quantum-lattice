#!/usr/bin/env python3
"""ql_chair44_chains.py - 1D tight-binding chains whose onsite energy is the Chair44 pyramid height read along a straight line.

H = -t sum |i><i+1| + h.c. + lam * sum V_i |i><i|,   V_i = pyramid(label at the i-th cell of the line) / 36  in {-1, 0, +1}.

The line is read from the exact depth-n Chair44 supertile (labels by digit inflation, ql_tilings.chair44_labels_at), n = 14 -> 16384 cells.
Lines: 'axis' (along x at a random (y, z)), 'diag' (body diagonal, random offsets), each also SHUFFLED (same multiset of values, order destroyed).
Known background (spectre repo, CONNECTIONS.md row 12): box averages of the pyramid are 0 but along axes the partial sums stay bounded while along
the body diagonal chair stacks give ballistic sums.  What this script adds is only the numerical question: does that change the chain's
localisation?  Measured: line mean, max |partial sum|, Lyapunov exponent at fixed energies (transfer matrix), N*IPR of eigenstates.
The answer is reported as measured; no localisation claim is made beyond the table.

    python3 ql_chair44_chains.py           table
    python3 ql_chair44_chains.py --tests
"""
import sys

import numpy as np
from scipy.linalg import eigh_tridiagonal

import ql_tilings as T


def line_values(kind, j, n, rng):
    L = 2 ** n
    t = np.arange(L)
    st = T._chair44_load()
    if kind == "axis":
        y, z = rng.integers(0, L, 2)
        lab = T.chair44_labels_at(j, n, t, np.full(L, y), np.full(L, z))
    elif kind == "diag":
        o = rng.integers(0, L, 2)
        lab = T.chair44_labels_at(j, n, t, (t + o[0]) % L, (t + o[1]) % L)
    else:
        raise ValueError(kind)
    return np.asarray(st["pyramid"])[lab] / 36.0


def lyapunov(V, E, lam=1.0):
    """Lyapunov exponent of psi_{i+1} = (E - lam V_i) psi_i - psi_{i-1} (hopping 1), by renormalised transfer product."""
    a, b, s = 1.0, 0.0, 0.0
    for v in V:
        a, b = (E - lam * v) * a - b, a
        m = np.hypot(a, b)
        s += np.log(m)
        a /= m
        b /= m
    return s / len(V)


def mean_nipr(V, lam, nsite=4096):
    d = lam * np.asarray(V[:nsite], float)
    w, v = eigh_tridiagonal(d, -np.ones(len(d) - 1))
    return float(len(d) * np.mean(np.sum(np.abs(v) ** 4, axis=0)))


def stats(kind, shuffled, nlines=12, n=14, lam=1.0, energies=(0.3, 1.0), seed=1):
    rng = np.random.default_rng(seed)
    rng2 = np.random.default_rng(seed + 1000)      # separate stream: tiling and shuffled rows use the SAME lines
    out = dict(mean=[], maxsum=[], ly=[], nipr=[])
    for _ in range(nlines):
        j = int(rng.integers(0, 168))
        V = line_values(kind, j, n, rng)
        if shuffled:
            V = rng2.permutation(V)
        out["mean"].append(V.mean())
        out["maxsum"].append(np.abs(np.cumsum(V)).max())
        out["ly"].append(np.mean([lyapunov(V, E, lam) for E in energies]))
        out["nipr"].append(mean_nipr(V, lam))
    return {k: np.array(v) for k, v in out.items()}


def table(verbose=True, **kw):
    res = {}
    for kind in ("axis", "diag"):
        for sh in (False, True):
            r = stats(kind, sh, **kw)
            res[(kind, sh)] = r
            if verbose:
                print("  %-5s %-9s |line mean| %.3f  max|partial sum| median %7.0f  Lyapunov %.4f +- %.4f  N*IPR %.1f +- %.1f"
                      % (kind, "shuffled" if sh else "tiling", np.abs(r["mean"]).mean(), np.median(r["maxsum"]), r["ly"].mean(),
                         r["ly"].std(), r["nipr"].mean(), r["nipr"].std()))
    return res


def run_tests(verbose=True):
    ok = True

    def check(name, cond, extra=""):
        nonlocal ok
        ok &= bool(cond)
        if verbose:
            print("  %-4s %s %s" % ("ok" if cond else "FAIL", name, extra))

    check("Lyapunov exponent of a constant potential inside the band is 0", abs(lyapunov(np.zeros(4000), 0.5)) < 1e-3)
    check("Lyapunov exponent outside the band equals arccosh(|E|/2)", abs(lyapunov(np.zeros(4000), 3.0) - np.arccosh(1.5)) < 2e-3)
    rng = np.random.default_rng(5)
    V = line_values("axis", 3, 10, rng)
    check("line values are in {-1, 0, +1}", set(np.unique(V)) <= {-1.0, 0.0, 1.0})
    r = table(verbose, nlines=8, n=13)
    check("axis lines: partial sums stay tiny (<= 8) compared with the length 8192", r[("axis", False)]["maxsum"].max() <= 8)
    check("diagonal lines: some have a ballistic partial sum (> 500)", r[("diag", False)]["maxsum"].max() > 500)
    check("shuffled rows use the same lines: identical line means", np.allclose(r[("axis", False)]["mean"], r[("axis", True)]["mean"]) and np.allclose(r[("diag", False)]["mean"], r[("diag", True)]["mean"]))
    return ok


if __name__ == "__main__":
    if "--tests" in sys.argv:
        sys.exit(0 if run_tests() else 1)
    table()
