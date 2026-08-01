"""A small, cheap sanity floor directly against pyqula (pysrc/pyqula/),
no GUI/interfacetk involved. pysrc/pyqula/ is vendored and refreshed
wholesale by tools/update_pyqula.sh (see CLAUDE.md's "Updating vendored
pyqula") rather than hand-edited, so this isn't meant to validate the
physics - it's an automated version of the "skim git diff --stat
pysrc/pyqula for anything alarming" step that update already asks for by
hand: a couple of textbook tight-binding results that would only change
if a refresh silently altered default hopping conventions or broke
get_hamiltonian()/get_hk_gen() in a way this repo's interface layer
depends on.
"""
import numpy as np

from pyqula import geometry


def test_honeycomb_dirac_point_is_degenerate():
    """Plain nearest-neighbor graphene: the two bands touch (E=0) at the
    K point, the hallmark massless-Dirac-fermion result."""
    h = geometry.honeycomb_lattice().get_hamiltonian()
    hk = h.get_hk_gen()
    ev = np.linalg.eigvalsh(hk([1. / 3., 1. / 3., 0.]))
    assert np.allclose(ev, 0., atol=1e-6)


def test_honeycomb_bandwidth_at_gamma():
    """At Gamma, nearest-neighbor graphene's bands split to +-3t (t=1
    default), from the 3-fold coordination."""
    h = geometry.honeycomb_lattice().get_hamiltonian()
    hk = h.get_hk_gen()
    ev = np.linalg.eigvalsh(hk([0., 0., 0.]))
    assert np.allclose(sorted(ev), [-3., -3., 3., 3.], atol=1e-6)


def test_square_lattice_bandwidth():
    """Simple-cubic-style nearest-neighbor square lattice: single band
    E(k) = -2t(cos(kx)+cos(ky)), so Gamma and the zone corner sit at
    +-4t (t=1 default, 4-fold coordination)."""
    h = geometry.square_lattice().get_hamiltonian()
    hk = h.get_hk_gen()
    assert np.allclose(np.linalg.eigvalsh(hk([0., 0., 0.])), 4., atol=1e-6)
    assert np.allclose(np.linalg.eigvalsh(hk([0.5, 0.5, 0.])), -4., atol=1e-6)
