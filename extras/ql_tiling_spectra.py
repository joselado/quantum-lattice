#!/usr/bin/env python3
"""ql_tiling_spectra.py - spectra, density of states and inverse participation ratio of the tilings of ql_tilings.py.

What is computed (dense exact diagonalisation of finite patches; the numbers are properties of the PATCH, with its boundary):
  * the graph: bipartite? degree histogram;  * the spectrum, bandwidth, number of exact zero modes;  * the density of states;
  * the inverse participation ratio IPR = sum |psi|^4 of every eigenstate and how N*IPR scales with the patch size
    (extended states: N*IPR stays bounded; localised states: it grows with N).
Facts that are exact consequences of the construction (and are tests):
  * trace identity: sum E^2 = 2 sum_bonds t^2;
  * the three planar tilings Hat, Spectre, Turtle have IDENTICAL vertex graphs (see ql_tilings.py), so with unit hopping their spectra are
    identical to machine precision; they differ only for length-dependent hopping ('inverse', 'gauss');
  * the vertex graphs (including the degree-2 'straight' points) and the Chair44 cell graph are bipartite, so every spectrum is
    symmetric about E = 0.
Everything else is REPORTED, not claimed: there is no prior theory in this project for these spectra, and a finite patch is not the infinite
tiling.

    python3 ql_tiling_spectra.py              table for level 3 (about a minute)
    python3 ql_tiling_spectra.py --tests      level-2 patches (a few seconds)
    python3 ql_tiling_spectra.py --png ../screenshots/tiling_spectra.png
"""
import sys

import numpy as np

import ql_common as C        # noqa: F401  (sets sys.path)
import ql_tilings as T


def bipartite(n, edges):
    A = T.adjacency(n, edges, np.ones(len(edges))).tocsr()
    col = -np.ones(n, int)
    for s in range(n):
        if col[s] >= 0:
            continue
        col[s] = 0
        stack = [s]
        while stack:
            u = stack.pop()
            for v in A.indices[A.indptr[u]:A.indptr[u + 1]]:
                if col[v] < 0:
                    col[v] = 1 - col[u]
                    stack.append(v)
                elif col[v] == col[u]:
                    return False
    return True


def eig(Tm):
    w, v = np.linalg.eigh(Tm.toarray() if hasattr(Tm, "toarray") else Tm)
    return w, (np.abs(v) ** 4).sum(axis=0)


def chair_edges(Tm):
    r, c = Tm.nonzero()
    m = r < c
    return np.c_[r[m], c[m]]


def summary(w, ipr):
    n = len(w)
    return dict(n=n, emin=float(w.min()), emax=float(w.max()), zero=int((abs(w) < 1e-8).sum()), sym=float(abs(w + w[::-1]).max()),
                ipr_mean_n=float(ipr.mean() * n), ipr_med_n=float(np.median(ipr) * n), ipr_max=float(ipr.max()))


def ipr_scaling(kind, hopping="unit", levels=(1, 2, 3)):
    out = []
    for lv in levels:
        p = T.planar_patch(kind, lv)
        w, ipr = eig(T.tight_binding(p, hopping))
        out.append((len(w), float(ipr.mean() * len(w)), float(np.median(ipr) * len(w))))
    return out


def run_tests(verbose=True):
    ok = True

    def check(name, cond, extra=""):
        nonlocal ok
        ok &= bool(cond)
        if verbose:
            print("  %-4s %s %s" % ("ok" if cond else "FAIL", name, extra))

    if not T.available():
        print("  SKIP (the Spectre repository was not found: set SPECTRE_DIR)")
        return True
    spec = {}
    for k in T.FAMILY:
        p = T.planar_patch(k, 2)
        for hop in ("unit", "inverse"):
            Tm = T.tight_binding(p, hop)
            spec[(k, hop)] = (eig(Tm), p, Tm)
    (w_s, _), p_s, T_s = spec[("spectre", "unit")]
    check("planar vertex graph is bipartite", bipartite(len(p_s.vert), p_s.edges))
    check("spectrum symmetric about E = 0 (bipartite)", all(abs(w + w[::-1]).max() < 1e-9 for (w, _), _, _ in spec.values()))
    check("trace identity sum E^2 = 2 sum t^2 for every tiling and hopping",
          all(abs((w ** 2).sum() - (Tm.multiply(Tm).sum())) < 1e-8 for (w, _), _, Tm in spec.values()))
    check("unit hopping: Hat, Spectre and Turtle spectra are identical (same graph)",
          abs(spec[("hat", "unit")][0][0] - w_s).max() < 1e-10 and abs(spec[("turtle", "unit")][0][0] - w_s).max() < 1e-10)
    check("inverse-length hopping: Hat and Turtle differ from the Spectre and from each other",
          abs(spec[("hat", "inverse")][0][0] - spec[("spectre", "inverse")][0][0]).max() > 0.05
          and abs(spec[("turtle", "inverse")][0][0] - spec[("spectre", "inverse")][0][0]).max() > 0.05
          and abs(spec[("hat", "inverse")][0][0] - spec[("turtle", "inverse")][0][0]).max() > 0.05)
    check("1/N <= IPR <= 1 for every state", all(((ipr >= 1.0 / len(w) - 1e-12) & (ipr <= 1 + 1e-12)).all() for (w, ipr), _, _ in spec.values()))
    # pyqula round trip: the spectrum of the pyqula Hamiltonian is the same
    h = T.to_pyqula(p_s.vert, T_s)
    wq = np.linalg.eigvalsh(np.asarray(h.intra.todense()))
    check("pyqula Hamiltonian has the same spectrum", abs(wq - w_s).max() < 1e-10)
    # chair44
    c, l, Tc = T.chair44_cell_model(2)
    wc, iprc = eig(Tc)
    check("Chair44 cell graph is bipartite (subgraph of the cubic lattice) and its spectrum symmetric",
          bipartite(len(c), chair_edges(Tc)) and abs(wc + wc[::-1]).max() < 1e-9)
    check("Chair44 spectrum lies inside [-6, 6] (maximum degree 6)", wc.max() < 6.0 + 1e-9 and wc.min() > -6.0 - 1e-9, "(|E| <= %.3f)" % wc.max())
    return ok


def figure(path, level=3):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(2, 2, figsize=(11, 7))
    for k, col in zip(T.FAMILY, ("tab:blue", "tab:orange", "tab:green")):
        p = T.planar_patch(k, level)
        for j, hop in enumerate(("unit", "inverse")):
            w, ipr = eig(T.tight_binding(p, hop))
            h, e = np.histogram(w, bins=120, density=True)
            ax[0, j].step(0.5 * (e[1:] + e[:-1]), h, color=col, label=k, lw=1.2, alpha=0.9)
            if k == "spectre" and hop == "unit":
                ax[1, 0].scatter(w, ipr * len(w), s=2, color=col)
    ax[0, 0].set_title("DOS, unit hopping (the three curves coincide)")
    ax[0, 1].set_title("DOS, hopping = 1/length")
    ax[0, 0].legend()
    ax[1, 0].set_title("Spectre, unit hopping: N * IPR of each eigenstate")
    ax[1, 0].set_xlabel("E")
    c, l, Tc = T.chair44_cell_model(3)
    w, ipr = eig(Tc)
    h, e = np.histogram(w, bins=120, density=True)
    ax[1, 1].step(0.5 * (e[1:] + e[:-1]), h, color="tab:red")
    ax[1, 1].set_title("Chair44 cell model (depth 3, %d cells): DOS" % len(c))
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    print("wrote", path)


def main():
    if "--tests" in sys.argv:
        sys.exit(0 if run_tests() else 1)
    if "--png" in sys.argv:
        figure(sys.argv[sys.argv.index("--png") + 1])
        return
    if not T.available():
        print("Spectre repository not found (set SPECTRE_DIR)")
        return
    print("level-3 patches (finite, with boundary)")
    for k in T.FAMILY:
        p = T.planar_patch(k, 3)
        for hop in ("unit", "inverse"):
            w, ipr = eig(T.tight_binding(p, hop))
            s = summary(w, ipr)
            print("  %-8s %-8s N=%d  E in [%.3f, %.3f]  zero modes %d  mean N*IPR %.1f  max IPR %.3f" % (k, hop, s["n"], s["emin"], s["emax"], s["zero"], s["ipr_mean_n"], s["ipr_max"]))
    print("N * mean IPR versus size (Spectre, unit hopping), levels 1-3:", [(n, round(m, 1)) for n, m, _ in ipr_scaling("spectre")])
    c, l, Tc = T.chair44_cell_model(3)
    w, ipr = eig(Tc)
    s = summary(w, ipr)
    print("  chair44  cells   N=%d  E in [%.3f, %.3f]  zero modes %d  mean N*IPR %.1f" % (s["n"], s["emin"], s["emax"], s["zero"], s["ipr_mean_n"]))


if __name__ == "__main__":
    main()
