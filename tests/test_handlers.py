"""Handler-execution tests: actually call a mode's button handlers, rather
than only checking (like test_signal_wiring.py) that a handler exists.
This is the layer that would have caught the two bug classes recorded in
project memory - both only break when the handler actually runs with a
realistic, non-default parameter:

  - 3d/2dslab/hybridfilm/hofstader1d passed the wrong kwarg name to
    pyqula's get_hamiltonian() for a custom hopping function, so a
    nonzero "strain" field (or, for hofstader1d, its unconditional "ti"
    interlayer-coupling path) either crashed or silently no-opped.
  - common.get_kdos_bands() read the wrong UI field ("ne_ldos" instead of
    "nk_kbands") for its k-point count, across 7 modes.

`execute_script` is stubbed for every test here (see `_stub_execute_script`
below) so these tests exercise handler correctness, not whether the
matching ql-* plotting subprocess renders - that's a separate, lower-value
thing to test and would need a display/matplotlib backend.
"""
import numpy as np
import pytest
import smoke_test

from _handler_harness import import_mode, set_field, set_combo, run_button, activate
from interfacetk import common


@pytest.fixture(autouse=True)
def _stub_execute_script(monkeypatch):
    """Replace execute_script everywhere it's already been bound by value
    (common.py's `from .qlinterface import execute_script`, and every
    mode's `from interfacetk.qlinterface import *`) with a no-op recorder,
    so these tests never spawn the real ql-* plotting subprocess."""
    from interfacetk import qlinterface
    calls = []

    def _stub(command, background=True):
        calls.append(command)
        return None

    monkeypatch.setattr(qlinterface, "execute_script", _stub)
    monkeypatch.setattr(common, "execute_script", _stub)
    return calls


def _stub_in(modobj, monkeypatch, calls):
    """Extra safety net for a mode module that already bound its own
    `execute_script` name (via `from interfacetk.qlinterface import *`)
    before the autouse fixture patched qlinterface - patch it there too."""
    if hasattr(modobj, "execute_script"):
        monkeypatch.setattr(modobj, "execute_script", lambda c, background=True: calls.append(c), raising=False)


# ---------------------------------------------------------------------
# Broad, shallow smoke pass: show_bands/show_dos, the two cheapest and
# most universal STANDARD_HANDLERS buttons, across the modes NOT already
# exercised by a targeted regression test below (those already pay for a
# real show_bands/show_dosbands call on their own mode - see each test's
# own comment for exactly what it does and doesn't compute). Modes
# without a given button (e.g. impurity_embedding has neither) are
# skipped for that combination rather than failing.
#
# Deliberately NOT all 15 modes, and NOT the full STANDARD_HANDLERS
# button set. Both dimensions matter and neither is free:
#   - show_bands/show_dos each do a REAL k-path diagonalization/DOS sweep
#     (unlike test_kdos_bands_uses_nk_kbands_field below, which stubs out
#     the actual kdos.kdos_bands() call - it only needs pickup_hamiltonian()
#     to run for real, not a full k-mesh sweep). Each *new* mode's first
#     real show_bands call costs on the order of 100-250MB (measured) -
#     pyqula's numba-jitted Hamiltonian-building/diagonalization kernels
#     get freshly compiled+run per distinct geometry/dimensionality, and
#     that memory isn't released for the life of the process. All 15
#     modes through show_bands+show_dos alone (no other buttons) already
#     pushed a single test process past a 2GB cgroup cap before finishing;
#     restricting this smoke pass to the handful of modes regression tests
#     don't already touch keeps total real-compute mode count (regression
#     + this pass) around 7, which measured well under 1.5GB.
#   - the other STANDARD_HANDLERS buttons (show_chern/show_z2/show_qpi/
#     show_fermi_surface/show_multildos/show_iets_qdos/...) are their own,
#     separate cost dimension on top of that: an earlier version of this
#     test tried every standard button across all 15 modes and it ran for
#     *hours* before being killed (1000%+ CPU, 2.6GB+ RSS) - these do real
#     BZ-averaged/real-space-summed physics at default resolution, not a
#     wiring bug, and cost isn't predictable enough from a handful of
#     single-button timings to widen without profiling each addition
#     individually and re-measuring peak RSS/wall time under a hard cap
#     (e.g. `systemd-run --user --scope -p MemoryMax=2G <cmd>`, confirmed
#     to actually enforce and kill on this machine) - never just trust
#     that "it seemed fine for a couple of modes."
# If a specific mode/button combination needs its own coverage, add it as
# its own targeted test (with cheap field overrides/monkeypatched-out
# expensive calls, like the regression tests below) rather than growing
# this blanket matrix.
#
# One import per mode (cached in _matrix_page, below) rather than one per
# (mode,button) pair - safe because this group never mutates a field, so
# reusing the same built page across many independent read/compute calls
# is equivalent to importing fresh each time, just far cheaper. Contrast
# with the targeted regression tests further down, which each do their
# own fresh, unshared import specifically because they mutate fields.
# ---------------------------------------------------------------------

# Modes touched by a targeted regression test below (3d/2dslab/hybridfilm
# via strain; hofstader1d via its own initialize()-only check;
# 2dslab/tmdc/tbg/multilayergraphene/1d/hybridfilm/hybridribbon via the
# KDOS-bands field test - though that one stubs out the real computation,
# so it's cheap regardless) are excluded here to avoid paying for a second
# real show_bands/show_dos compile of the same mode.
_REGRESSION_COVERED_MODES = {
    "3d", "2dslab", "hybridfilm", "hofstader1d",
    "tmdc", "tbg", "multilayergraphene", "1d", "hybridribbon",
}
ALL_MODES = [m for m in smoke_test.MODES if m not in _REGRESSION_COVERED_MODES]
STANDARD_BUTTONS = ["show_bands", "show_dos"]

_matrix_pages = {}


def _matrix_page(mode, monkeypatch):
    if mode not in _matrix_pages:
        _matrix_pages[mode] = import_mode(mode)
    modobj = _matrix_pages[mode]
    _stub_in(modobj, monkeypatch, [])
    return modobj


@pytest.mark.parametrize("button", STANDARD_BUTTONS)
@pytest.mark.parametrize("mode", ALL_MODES)
def test_standard_handler_runs(mode, button, monkeypatch):
    modobj = _matrix_page(mode, monkeypatch)
    if button not in modobj.signals:
        pytest.skip(f"{mode} has no {button} button")
    run_button(modobj, button)


# ---------------------------------------------------------------------
# Targeted regression: strain-triggered custom hopping (bug_strain_custom_hopping_fun_kwarg)
# ---------------------------------------------------------------------

@pytest.mark.parametrize("mode", ["3d", "2dslab", "hybridfilm"])
def test_nonzero_strain_does_not_crash(mode, monkeypatch):
    modobj = import_mode(mode)
    _stub_in(modobj, monkeypatch, [])
    set_field(modobj, "strain", "0.3")  # part 1's field for hybridfilm (part_suffix(1)=="")
    run_button(modobj, "show_bands")  # pickup_hamiltonian() -> initialize() takes the strain branch


# ---------------------------------------------------------------------
# Targeted regression: hofstader1d's unconditional custom hopping
# (same bug_strain_custom_hopping_fun_kwarg memory entry - this one is a
# *silent* no-op rather than a crash, so "no exception" alone wouldn't
# catch a regression: assert the interlayer coupling actually changes the
# built Hamiltonian instead.
# ---------------------------------------------------------------------

def test_hofstader1d_ti_changes_hamiltonian(monkeypatch):
    modobj = import_mode("hofstader1d")
    _stub_in(modobj, monkeypatch, [])
    set_combo(modobj, "lattice", "Bilayer graphene AB")
    set_field(modobj, "width", "2")
    activate(modobj)

    set_field(modobj, "ti", "0.0")
    h_off = modobj.initialize()

    set_field(modobj, "ti", "0.8")
    h_on = modobj.initialize()

    assert not np.allclose(h_off.intra, h_on.intra), (
        "changing hofstader1d's interlayer coupling 'ti' had no effect on the built "
        "Hamiltonian - get_hamiltonian() may be silently dropping the tij= custom "
        "hopping function again (see bug_strain_custom_hopping_fun_kwarg memory)"
    )


# ---------------------------------------------------------------------
# Targeted regression: KDOS-bands wrong nk field (bug_kdos_bands_wrong_nk_field),
# across every mode that relies on common.get_kdos_bands() rather than
# supplying its own show_dosbands override (2d/hofstader1d/heavyfermion
# have their own and are unaffected - see that memory entry).
# ---------------------------------------------------------------------

@pytest.mark.parametrize("mode", [
    "2dslab", "tmdc", "tbg", "multilayergraphene", "1d", "hybridfilm", "hybridribbon",
])
def test_kdos_bands_uses_nk_kbands_field(mode, monkeypatch):
    modobj = import_mode(mode)
    _stub_in(modobj, monkeypatch, [])

    from pyqula import kdos as kdos_mod
    captured = {}

    def _fake_kdos_bands(h, **kwargs):
        captured.update(kwargs)
        # write the file get_kdos_bands()'s execute_script call expects, in
        # case a future change starts reading it back
        open("KDOS_BANDS.OUT", "w").close()

    monkeypatch.setattr(kdos_mod, "kdos_bands", _fake_kdos_bands)

    set_field(modobj, "nk_kbands", "17")
    run_button(modobj, "show_dosbands")

    assert captured.get("nk") == 17, (
        f"{mode}: get_kdos_bands() called kdos.kdos_bands with nk={captured.get('nk')!r}, "
        f"expected 17 (the 'nk_kbands' field) - is it reading the wrong UI field again?"
    )
