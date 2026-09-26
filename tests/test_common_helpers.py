"""Direct calls into common.py's calculation helpers on tiny Hamiltonians,
through a DictForm accessor instead of a built page.

test_handlers.py clicks real buttons on real pages, which is the faithful
check but costs seconds per button; the buttons here take tens of seconds
each at their page defaults. What broke in them was the call contract -
the keyword names handed to pyqula, and the accessor methods a helper
expects - which a tiny system exercises just as well:

  - get_multildos()/get_interactive_ldos() passed es=/numw=, which the old
    pyqula swallowed (so the energy window was silently the default) and
    the current one rejects; they are energies=/num_bands=.
  - impurity_embedding/ribbon_embedding handed their page object to
    get_embedding_ldos(), which then needed get_array() - a method only
    qtwrap and DictForm had.
  - a 3d density of states at the page's default of 1000 k-points per
    direction built a 10**9-point mesh and ran the machine out of memory.
  - an SCF that hit its iteration cap surfaced as "'NoneType' object has
    no attribute 'save'", and the Z2 invariant of a metal as a numpy
    array-shape error.
"""
import os

import numpy as np
import pytest

from pyqula import geometry
from interfacetk import common, qtwrap
from interfacetk.dictform import DictForm


class Form(DictForm):
    """A DictForm built from plain keyword values, plus the one shell-wide
    setting (serial/parallel) the helpers read from qtwrap itself."""
    def __init__(self, **fields):
        super().__init__({k: {"type": "line", "value": v} for k, v in fields.items()})
    def is_parallel_execution(self):
        return False


@pytest.fixture(autouse=True)
def _scratch(tmp_path, monkeypatch):
    """Run each helper in its own folder, without launching ql-* plots."""
    monkeypatch.chdir(tmp_path)
    scripts = []
    monkeypatch.setattr(common, "execute_script", lambda c, background=True: scripts.append(c))
    return scripts


def _honeycomb(has_spin=False):
    return geometry.honeycomb_lattice().get_hamiltonian(has_spin=has_spin)


def test_multildos_passes_the_energy_window(_scratch):
    h = _honeycomb()
    common.get_multildos(h, Form(multildos_ewindow="0.5", multildos_nrep="1",
        multildos_nk="1", multildos_numw="4", multildos_delta="0.1",
        basis_ldos="Tight binding", ratomic_ldos="1.0"))
    names = open("MULTILDOS/MULTILDOS.TXT").read().split()
    energies = [float(n.split("_")[1]) for n in names]
    assert np.isclose(min(energies), -0.5) and np.isclose(max(energies), 0.5)
    assert _scratch == ["ql-multildos "]


def test_interactive_ldos_passes_the_energy_window():
    h = _honeycomb()
    common.get_interactive_ldos(h, Form(window_ldos="0.3", nsuper_ldos="1",
        nk_ldos="1", ne_ldos="3", delta_ldos="0.1"))
    names = open("MULTILDOS/MULTILDOS.TXT").read().split()
    assert len(names) == 3
    assert np.isclose(max(float(n.split("_")[1]) for n in names), 0.3)


def test_page_accessor_surface_matches_qtwrap():
    # a page (qtwrap._AppBase) and a DictForm both stand in for qtwrap as
    # the `window` a common.py helper reads from
    for name in ["get", "getbox", "get_array", "is_checked"]:
        assert callable(getattr(qtwrap, name))
        assert callable(getattr(qtwrap._AppBase, name, None)), name
        assert callable(getattr(DictForm, name, None)), name


def test_embedding_ldos_runs():
    g = geometry.honeycomb_lattice()
    h = common.build_embedding_hamiltonian(g, Form(exchange="0.0,0.0,0.0",
        lattice="Honeycomb"))
    common.get_embedding_ldos(h, Form(nsuper_impurity="1",
        impurity_potential="1.0", impurity_exchange="0.0,0.0,0.0",
        energy_embedding_ldos="0.0", delta_embedding_ldos="0.5",
        ncells_embedding_ldos="1", nk_scaling_embedding_ldos="0.05"))
    assert os.path.exists("LDOS.OUT")


def test_kmesh_guard():
    common.check_kmesh(1000, 2, "density of states") # 10**6: allowed
    common.check_kmesh(10**9, 0, "density of states") # 0d: no mesh at all
    with pytest.raises(ValueError, match=r"1000\^3 = 1e\+09 k-points .* Use 100 or less"):
        common.check_kmesh(1000, 3, "density of states")


def test_3d_dos_refuses_a_runaway_mesh_before_computing():
    h = geometry.cubic_lattice().get_hamiltonian(has_spin=False)
    with pytest.raises(ValueError, match="per direction"):
        common.get_dos(h, Form(dos_nk="1000", dos_delta="0.1", dos_ewindow="1.0",
            dos_operator="None", dos_mode="ED"))
    assert not os.path.exists("DOS.OUT")


def test_unconverged_scf_is_kept_with_a_warning():
    # through a DictForm (a subprocess calculation), the warning is left in
    # the scratch dir for run_calculation_subprocess() to show
    h = _honeycomb(has_spin=True)
    common.solve_scf(h, Form(scf_initialization="antiferro", nk_scf="2",
        U="3.0", V1="0.0", V2="0.0", J1="0.0", J2="0.0", J3="0.0",
        filling_scf="0.5", extra_electron="0.0", mix_scf="0.1",
        smearing_scf="0.01", scf_maxite="1", scf_solver="linear_mixing"))
    assert os.path.exists("hamiltonian.pkl")
    title, content = open(qtwrap.WARNINGS_FILE).read().strip().split("\t")
    assert title == "SCF not converged"
    assert "stopped after 1 iterations" in content


def test_z2_of_a_metal_says_so():
    h = geometry.square_lattice().get_hamiltonian(has_spin=True)
    with pytest.raises(ValueError, match="needs a gap at the Fermi level"):
        common.get_z2(h, Form(topology_nk="16"))


def test_subprocess_warnings_are_shown_once(tmp_path, monkeypatch):
    # run_calculation_subprocess() shows the warnings its child left in the
    # scratch dir - only that child's: a file left by an earlier child that
    # warned and then failed is cleared before launching the next one
    import subprocess
    from _handler_harness import import_mode, activate
    m = import_mode("1d")
    activate(m)
    shown = []
    monkeypatch.setattr(qtwrap, "notify_warning", lambda p, t, c: shown.append(t))
    scratch = str(tmp_path)
    def child(warns):
        class Proc:
            def __init__(self, cmd, cwd, **kw):
                if warns:
                    with open(os.path.join(cwd, qtwrap.WARNINGS_FILE), "a") as f:
                        f.write("Fresh\tfrom this run\n")
            def wait(self): return 0
        return Proc
    open(os.path.join(scratch, qtwrap.WARNINGS_FILE), "w").write("Stale\tfrom a failed run\n")
    monkeypatch.setattr(subprocess, "Popen", child(warns=False))
    qtwrap.run_calculation_subprocess("unused", "solve_scf", scratch)
    assert shown == []
    monkeypatch.setattr(subprocess, "Popen", child(warns=True))
    qtwrap.run_calculation_subprocess("unused", "solve_scf", scratch)
    assert shown == ["Fresh"]
    assert not os.path.exists(os.path.join(scratch, qtwrap.WARNINGS_FILE))


def test_spin_projected_dos_without_spin_terms():
    # get_dos() used to reduce() before building the operator, which drops
    # the spin of a Hamiltonian with no spin term set - so Sz failed
    h = _honeycomb(has_spin=True)
    common.get_dos(h, Form(dos_nk="4", dos_delta="0.2", dos_ewindow="1.0",
        dos_operator="Sz", dos_mode="ED"))
    assert os.path.exists("DOS.OUT")


def test_spin_operator_on_a_reduced_hamiltonian():
    # hofstader1d reduce()s the Hamiltonian it builds; a spin operator then
    # needs a spinful copy, and the cached original must stay untouched
    h = _honeycomb(has_spin=True).reduce()
    assert not h.has_spin
    h2 = common.hamiltonian_for_operator(h, "Sz")
    assert h2.has_spin and not h.has_spin
    common.get_operator(h2, "Sz")
    assert common.hamiltonian_for_operator(h, "IPR") is h
