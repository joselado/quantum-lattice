"""ql_common.py - shared helpers for the extras/ql_*.py scripts (not part of the GUI).

  * puts ../pysrc on sys.path so that `import pyqula` works from anywhere
  * multihopping_from_hk(): turn ANY Bloch Hamiltonian H(k) (a Python function) into the exact real-space hopping dictionary
    pyqula uses, by an FFT over a k-grid; exact whenever the hoppings reach at most nmax cells and N > 2 nmax
  * hamiltonian_from_hk(): a pyqula Hamiltonian with those hoppings on a cubic/square/chain template

Convention (checked in the tests of ql_hopf_insulator.py): pyqula's get_hk_gen()(k) takes k in FRACTIONAL coordinates and returns
sum_R H(R) exp(+i 2 pi k.R); here H(R) = (1/N^d) sum_k H(k) exp(-i k.R) with k = 2 pi (fractional), so the two agree.
"""
import itertools
import os
import sys

import numpy as np

ROOT = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
PYSRC = os.path.join(ROOT, "pysrc")
if PYSRC not in sys.path:
    sys.path.insert(0, PYSRC)

SIGMA = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]], complex), np.array([[1, 0], [0, -1]], complex)]


def multihopping_from_hk(hk, dim=3, nmax=2, N=None, tol=1e-10):
    """Dictionary {R: matrix} with H(R) = (1/N^dim) sum_k H(k) e^{-i k.R}; hk takes a vector of dim angles k (radians)."""
    N = N or (2 * nmax + 3)
    ks = 2 * np.pi * np.arange(N) / N
    grid = np.array(list(itertools.product(ks, repeat=dim)))
    vals = np.array([hk(k) for k in grid])
    n = vals.shape[1]
    vals = vals.reshape((N,) * dim + (n, n))
    four = np.fft.fftn(vals, axes=tuple(range(dim))) / N ** dim
    out = {}
    for R in itertools.product(range(-nmax, nmax + 1), repeat=dim):
        m = four[tuple(r % N for r in R)]
        if np.abs(m).max() > tol:
            out[tuple(R) + (0,) * (3 - dim)] = m
    # completeness check: the part outside |R| <= nmax must vanish (the Nyquist/aliased cells carry the remainder)
    kept = sum(np.sum(np.abs(m) ** 2) for m in out.values())
    total = np.sum(np.abs(four) ** 2)
    return out, float(total - kept)


def hamiltonian_from_hk(hk, dim=3, nmax=2, N=None):
    """pyqula Hamiltonian (two orbitals per site, 'spinful' layout) with the Bloch Hamiltonian hk (2x2 or larger even)."""
    from pyqula import geometry
    from pyqula.multihopping import MultiHopping
    hop, leak = multihopping_from_hk(hk, dim=dim, nmax=nmax, N=N)
    g = {1: geometry.chain, 2: geometry.square_lattice, 3: geometry.cubic_lattice}[dim]()
    h = g.get_hamiltonian(has_spin=True)
    h.set_multihopping(MultiHopping(hop))
    return h, leak
