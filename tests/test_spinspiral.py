"""Physics tests for the spinspiral mode.

The point of these is that a spin spiral built *wrongly* (a phase read off
the supercell's own lattice vectors instead of the primitive ones, a cone
angle applied to the wrong component, sites grouped by raw Cartesian
coordinate instead of by spiral phase) still produces a perfectly
plausible-looking LDOS colormap. What separates a correct implementation
from a plausible one is a symmetry:

A flat or conical spiral with no spin-orbit coupling is invariant under a
*combined* operation - translate by one lattice vector, then rotate every
spin about the cone axis by the spiral angle. Charge is blind to the spin
rotation, so:

  - the total (unprojected) LDOS must be exactly uniform along the spiral,
    for any wavevector and any cone angle;
  - the same is true of the projection onto the cone axis, and of the
    projection onto each site's own local moment - both are invariant
    under that spin rotation;
  - the projection onto a fixed in-plane axis (Sx, Sy) is *not* invariant,
    and must genuinely oscillate with the spiral period.

Adding Rashba spin-orbit coupling ties spin to real space and breaks the
combined symmetry, so the total LDOS must then stop being uniform.

Kept deliberately small (short chains, few k-points, few energies) - these
assert symmetry relations, which hold at any resolution, not converged
numbers.
"""
import os
import sys

import numpy as np
import pytest

from _handler_harness import import_mode, set_field, set_combo, activate


@pytest.fixture(scope="module")
def mode():
    """One built page shared by every test here: none of them mutate a
    field without setting it again themselves, and building the page is
    the expensive part."""
    return import_mode("spinspiral")


def _configure(modobj, lattice="Chain", qvector="0.25, 0.0", cone_angle=90.0,
               plane="XY", rashba=0.0, kanemele=0.0, nmax=20):
    set_combo(modobj, "lattice", lattice)
    set_combo(modobj, "spiral_plane", plane)
    set_field(modobj, "qvector", qvector)
    set_field(modobj, "cone_angle", cone_angle)
    set_field(modobj, "rashba", rashba)
    set_field(modobj, "kanemele", kanemele)
    set_field(modobj, "max_supercell", nmax)
    set_field(modobj, "spiral_exchange", 0.4)
    set_field(modobj, "hopping", 1.0)
    set_field(modobj, "fermi", 0.0)
    # back to the page defaults: the `mode` fixture is module-scoped, so a
    # test that changes either of these must not leak into whichever runs
    # next
    modobj.window.spiral_ldos_subtract_average.setChecked(True)
    set_field(modobj, "spiral_ldos_nrep", 3)


def _ldos_profile(modobj, projection="None", ne=6, nk=6, delta=0.3, ewindow=3.0):
    """Return the LDOS map as an (energy, position-along-the-spiral) array,
    computed through the mode's own code path (its operator builder, its
    phase grouping) rather than a reimplementation of it here."""
    set_combo(modobj, "spiral_ldos_projection", projection)
    activate(modobj)
    h = modobj.initialize()
    es, ds = modobj.compute_spiral_ldos(
        h, energies=np.linspace(-ewindow, ewindow, ne), delta=delta, nk=nk)
    # subtract_average=False: the symmetry assertions below are about the
    # LDOS itself, and subtracting each energy's mean would make a
    # "uniform along the spiral" assertion pass trivially - including for a
    # wrong implementation
    # nrep=1: one copy of the profile, so the assertions below are about
    # the physics and not about the repetition the plot adds on top
    modobj.write_spiral_ldos(es, ds, h.geometry, subtract_average=False, nrep=1)
    return _read_map(len(es))[1]


def _read_map(nenergies):
    """SPIRAL_LDOS.OUT as (positions, profile[energy, position]).

    The file is written position-outermost (column 0 is the position, which
    is what ql-map2d reshapes on), so it draws with position across the
    bottom; the tests below reason per energy, hence the transpose."""
    m = np.genfromtxt("SPIRAL_LDOS.OUT").transpose()
    positions = np.unique(np.round(m[0], 8))
    return positions, m[2].reshape(len(positions), nenergies).T


def _spread(profile):
    """Relative variation of the LDOS along the spiral, worst over energies"""
    scale = np.max(np.abs(profile))
    if scale < 1e-12: return 0.0
    return np.max(np.ptp(profile, axis=1)) / scale


# ---------------------------------------------------------------------
# The symmetry that defines a correct spiral
# ---------------------------------------------------------------------

@pytest.mark.parametrize("lattice,qvector", [
    ("Chain", "0.25, 0.0"),
    ("Chain", "0.2, 0.0"),
    ("Triangular", "0.25, 0.0"),
    ("Triangular", "0.25, 0.5"),
])
@pytest.mark.parametrize("cone_angle", [90.0, 55.0])
def test_total_ldos_is_uniform_along_the_spiral(mode, lattice, qvector, cone_angle):
    """No SOC: charge cannot see the spiral, whatever q or cone angle."""
    _configure(mode, lattice=lattice, qvector=qvector, cone_angle=cone_angle)
    assert _spread(_ldos_profile(mode)) < 1e-8


@pytest.mark.parametrize("projection", ["Sz", "Local moment"])
def test_symmetric_projections_are_uniform(mode, projection):
    """The cone axis (here z) and each site's own moment are both invariant
    under the spiral's spin rotation, so neither resolves the texture."""
    _configure(mode, cone_angle=55.0)
    assert _spread(_ldos_profile(mode, projection=projection)) < 1e-8


@pytest.mark.parametrize("projection", ["Sx", "Sy"])
def test_inplane_projections_follow_the_spiral(mode, projection):
    """A fixed in-plane axis is not invariant - it must see the texture,
    and see it turning at exactly the spiral wavevector."""
    _configure(mode, qvector="0.25, 0.0", cone_angle=90.0)
    profile = _ldos_profile(mode, projection=projection)
    assert profile.shape[1] == 4, "q=1/4 should give a four-site supercell"
    assert _spread(profile) > 1e-3
    # one full turn across the supercell: opposite sides of the spiral
    # carry opposite in-plane spin density
    ie = int(np.argmax(np.ptp(profile, axis=1))) # the most modulated energy
    row = profile[ie]
    assert np.allclose(row, -np.roll(row, 2), atol=1e-8 + 1e-6 * np.max(np.abs(row)))


@pytest.mark.parametrize("lattice,qvector,cone_angle,rashba,kanemele", [
    ("Chain", "0.25, 0.0", 55.0, 0.5, 0.0),  # conical, Rashba
    ("Chain", "0.2, 0.0", 90.0, 0.5, 0.0),   # flat, Rashba
    ("Triangular", "0.25, 0.0", 90.0, 0.5, 0.0),
    ("Triangular", "0.25, 0.0", 90.0, 0.0, 0.4),  # intrinsic SOC
])
def test_soc_breaks_the_spiral_symmetry(mode, lattice, qvector, cone_angle,
                                        rashba, kanemele):
    """Spin-orbit coupling ties spin to real space, so the total LDOS stops
    being blind to the texture.

    Not every combination does: a *flat* q=1/4 spiral on a chain keeps a
    uniform charge LDOS even with Rashba, because its four moments (+x, +y,
    -x, -y) are still permuted among themselves by a combined
    translation/spin-rotation the Rashba term happens to respect. Tilting
    the cone or moving off q=1/4 removes that accident, which is why the
    cases below vary both."""
    _configure(mode, lattice=lattice, qvector=qvector, cone_angle=cone_angle,
               rashba=rashba, kanemele=kanemele)
    assert _spread(_ldos_profile(mode)) > 1e-3


# ---------------------------------------------------------------------
# Commensurability: what the user asked for vs. what was built
# ---------------------------------------------------------------------

@pytest.mark.parametrize("asked,realized,nsuper", [
    ("0.25, 0.0", 0.25, 4),
    ("0.2, 0.0", 0.2, 5),
    ("0.3333333, 0.0", 1. / 3., 3),
    ("0.5, 0.0", 0.5, 2),
])
def test_wavevector_is_snapped_to_a_commensurate_value(mode, asked, realized, nsuper):
    _configure(mode, qvector=asked)
    q, ns = mode.get_commensurate()
    assert np.isclose(q[0], realized)
    assert ns[0] == nsuper
    assert len(mode.get_geometry().r) == nsuper


def test_max_supercell_caps_the_supercell(mode):
    """An awkward wavevector is approximated, not honoured exactly."""
    _configure(mode, qvector="0.2857142857, 0.0", nmax=4) # 2/7, denominator too big
    q, ns = mode.get_commensurate()
    assert ns[0] <= 4
    assert abs(q[0] - 0.2857142857) < 0.05 # still the closest such fraction


def test_spiral_phases_advance_by_the_wavevector(mode):
    """The phase must be read off the *primitive* lattice, so that one
    primitive lattice vector advances it by exactly 2*pi*q."""
    _configure(mode, lattice="Chain", qvector="0.25, 0.0")
    activate(mode)
    phases = np.sort(mode.get_phases())
    steps = np.diff(phases)
    assert np.allclose(steps, 2 * np.pi * 0.25)


def test_cone_angle_sets_the_out_of_plane_moment(mode):
    """0 degrees is a ferromagnet along the cone axis, 90 a flat spiral,
    and in between a cone with a uniform axial component."""
    for angle in (0.0, 30.0, 90.0):
        _configure(mode, cone_angle=angle, plane="XY")
        activate(mode)
        moments = mode.get_moments()
        assert np.allclose(moments[:, 2], np.cos(np.radians(angle)))
        assert np.allclose(np.linalg.norm(moments, axis=1), 1.0)


def test_custom_plane_matches_the_named_one(mode):
    """A custom cone axis of z must describe the same spiral plane as XY,
    up to where the spiral starts (a global phase offset)."""
    _configure(mode, plane="XY", cone_angle=40.0)
    activate(mode)
    named = mode.get_moments()
    _configure(mode, plane="Custom", cone_angle=40.0)
    set_field(mode, "spiral_axis", "0.0, 0.0, 1.0")
    activate(mode)
    custom = mode.get_moments()
    assert np.allclose(named[:, 2], custom[:, 2]) # same canting
    # same in-plane magnitude, and the same relative turn from site to site
    inplane = lambda m: np.arctan2(m[:, 1], m[:, 0])
    assert np.allclose(np.diff(inplane(named)) % (2 * np.pi),
                       np.diff(inplane(custom)) % (2 * np.pi))


# ---------------------------------------------------------------------
# The buttons themselves, end to end (minus the ql-* plotting subprocess)
# ---------------------------------------------------------------------

@pytest.fixture
def calls(monkeypatch, mode):
    """Replace execute_script with a recorder, so the handlers below run
    for real without spawning the ql-* plotting subprocess (same approach
    as tests/test_handlers.py)."""
    from interfacetk import qlinterface, common as common_mod
    recorded = []

    def _stub(command, background=True):
        recorded.append(command)

    monkeypatch.setattr(qlinterface, "execute_script", _stub)
    monkeypatch.setattr(common_mod, "execute_script", _stub)
    monkeypatch.setattr(mode, "execute_script", _stub, raising=False)
    return recorded


def test_show_spiral_ldos_writes_a_map_ql_map2d_can_read(mode, calls):
    """ql-map2d reshapes its input into a (n_energies, n_positions) grid,
    which only works if every energy carries the same, uniformly spaced set
    of positions - the reason sites are grouped by spiral phase rather than
    by raw coordinate."""
    from _handler_harness import run_button
    _configure(mode, lattice="Triangular", qvector="0.25, 0.5")
    set_field(mode, "spiral_ldos_ne", 8)
    set_field(mode, "spiral_ldos_nk", 4)
    set_combo(mode, "spiral_ldos_projection", "Local moment")
    run_button(mode, "show_spiral_ldos")

    assert any("ql-map2d" in c for c in calls)
    m = np.genfromtxt("SPIRAL_LDOS.OUT").transpose()
    positions = np.unique(np.round(m[0], 8))
    energies = np.unique(np.round(m[1], 8))
    assert len(energies) == 8
    assert len(m[2]) == len(energies) * len(positions)  # a full rectangular grid
    assert np.allclose(np.diff(positions), np.diff(positions)[0])  # uniformly spaced
    # position is column 0, i.e. the axis ql-map2d puts across the bottom
    command = [c for c in calls if "ql-map2d" in c][-1]
    assert '--xlabel "Position along the spiral"' in command
    assert "--ylabel Energy" in command


def test_zero_wavevector_is_refused_rather_than_plotted(mode, calls):
    """With no spiral there is no direction to resolve the LDOS along; that
    has to be said, not silently plotted as a one-row map."""
    from _handler_harness import run_button
    _configure(mode, qvector="0.0, 0.0")
    set_field(mode, "spiral_ldos_ne", 4)
    set_field(mode, "spiral_ldos_nk", 2)
    with pytest.raises(ValueError, match="wavevector is zero"):
        run_button(mode, "show_spiral_ldos")


def test_spin_texture_button_reports_the_imposed_spiral(mode, calls):
    """show_magnetism extracts the moments back out of the built
    Hamiltonian, so it is also a check that the exchange field really went
    in with the shape get_moments() describes."""
    from _handler_harness import run_button
    _configure(mode, lattice="Chain", qvector="0.25, 0.0", cone_angle=60.0)
    set_field(mode, "magnetization_nrep", 1)
    run_button(mode, "show_magnetism")

    m = np.genfromtxt("MAGNETISM.OUT").transpose()
    moments = np.array([m[3], m[4], m[5]]).T
    activate(mode)
    # extract("m*") reports the coefficient of the Pauli matrices, i.e. the
    # exchange field itself, so this is the field that went in
    expected = mode.get_moments() * mode.window.get("spiral_exchange")
    assert np.allclose(np.sort(moments[:, 2]), np.sort(expected[:, 2]))
    assert np.allclose(np.linalg.norm(moments, axis=1).std(), 0.0, atol=1e-8)


@pytest.mark.parametrize("button", ["show_bands", "show_dos"])
def test_standard_handlers_run_on_the_triangular_lattice(mode, calls, button):
    """tests/test_handlers.py's blanket matrix only ever exercises a mode at
    its page defaults, i.e. Chain here - but the triangular lattice reaches
    those handlers with a 2D, non-square supercell geometry (four cells along
    a1, one along a2), which is the shape their k-path/BZ-mesh code has to
    cope with."""
    from _handler_harness import run_button
    _configure(mode, lattice="Triangular", qvector="0.25, 0.0")
    set_field(mode, "nk_bands", 20)
    set_field(mode, "dos_nk", 4)
    set_field(mode, "dos_delta", 0.2)
    run_button(mode, button)
    assert calls  # the matching ql-* plot was launched


def test_subtracting_the_average_leaves_the_spatial_variation(mode):
    """The default map shows each energy's deviation from its own mean, so
    that the modulation is visible on top of a much larger uniform LDOS."""
    from pyqula import ldos  # noqa: F401  (keeps the import cost with this test)
    _configure(mode, lattice="Chain", qvector="0.2, 0.0", cone_angle=55.0, rashba=0.5)
    set_combo(mode, "spiral_ldos_projection", "None")
    activate(mode)
    h = mode.initialize()
    es, ds = mode.compute_spiral_ldos(h, energies=np.linspace(-3, 3, 6),
                                      delta=0.3, nk=6)

    mode.write_spiral_ldos(es, ds, h.geometry, subtract_average=False)
    raw2d = _read_map(len(es))[1]
    mode.write_spiral_ldos(es, ds, h.geometry, subtract_average=True)
    dev2d = _read_map(len(es))[1]
    assert np.allclose(dev2d.mean(axis=1), 0.0)           # each energy centered
    assert np.allclose(dev2d, raw2d - raw2d.mean(axis=1, keepdims=True))
    assert np.max(np.abs(dev2d)) < np.max(np.abs(raw2d))  # the offset really was removed
    assert np.ptp(dev2d) > 1e-6                           # and the variation survives


def test_checkbox_drives_the_default(mode):
    """With no explicit argument, write_spiral_ldos follows the page's own
    "Subtract the average" checkbox."""
    _configure(mode, lattice="Chain", qvector="0.2, 0.0", cone_angle=55.0, rashba=0.5)
    activate(mode)
    h = mode.initialize()
    es, ds = mode.compute_spiral_ldos(h, energies=np.linspace(-3, 3, 6),
                                      delta=0.3, nk=6)
    for checked in (True, False):
        mode.window.spiral_ldos_subtract_average.setChecked(checked)
        mode.write_spiral_ldos(es, ds, h.geometry)
        profile = _read_map(len(es))[1]
        centered = bool(np.allclose(profile.mean(axis=1), 0.0))
        assert centered is checked


def test_noise_is_floored_away_when_there_is_no_real_variation(mode):
    """With no spin-orbit coupling the LDOS is exactly uniform along the
    spiral, so subtracting the average leaves only float64 rounding (~1e-16).
    That must come out as a flat zero map: a colormap rescales whatever it is
    given to its full range, so unfloored noise would be drawn as vivid,
    entirely meaningless structure."""
    _configure(mode, lattice="Chain", qvector="0.2, 0.0", cone_angle=55.0)
    set_combo(mode, "spiral_ldos_projection", "None")
    activate(mode)
    h = mode.initialize()
    es, ds = mode.compute_spiral_ldos(h, energies=np.linspace(-3, 3, 6),
                                      delta=0.3, nk=6)

    mode.write_spiral_ldos(es, ds, h.geometry, subtract_average=False)
    raw = np.genfromtxt("SPIRAL_LDOS.OUT").transpose()[2]
    assert np.max(np.abs(raw)) > 1e-3  # there is a real LDOS to speak of

    mode.write_spiral_ldos(es, ds, h.geometry, subtract_average=True)
    dev = np.genfromtxt("SPIRAL_LDOS.OUT").transpose()[2]
    assert np.all(dev == 0.0)  # exactly zero, not merely small


def test_real_variation_survives_the_floor(mode):
    """The floor must only remove noise - a genuine modulation is orders of
    magnitude above it and has to come through untouched."""
    _configure(mode, lattice="Chain", qvector="0.2, 0.0", cone_angle=55.0, rashba=0.5)
    set_combo(mode, "spiral_ldos_projection", "None")
    activate(mode)
    h = mode.initialize()
    es, ds = mode.compute_spiral_ldos(h, energies=np.linspace(-3, 3, 6),
                                      delta=0.3, nk=6)
    mode.write_spiral_ldos(es, ds, h.geometry, subtract_average=True)
    dev = np.genfromtxt("SPIRAL_LDOS.OUT").transpose()[2]
    assert np.max(np.abs(dev)) > 1e4 * mode.LDOS_NOISE_FLOOR


def test_marks_sit_at_whole_turns_of_the_spiral(mode):
    """The dashed guide lines mark where the spiral completes a full turn -
    not where a unit cell ends. On a chain with q = 1/5 the two coincide
    every fifth cell; the next test covers the case where they do not."""
    _configure(mode, lattice="Chain", qvector="0.2, 0.0")
    set_field(mode, "spiral_ldos_nrep", 3)
    activate(mode)
    h = mode.initialize()
    es, ds = mode.compute_spiral_ldos(h, energies=np.linspace(-3, 3, 4),
                                      delta=0.3, nk=4)
    marks = mode.write_spiral_ldos(es, ds, h.geometry)
    positions = _read_map(len(es))[0]
    wavelength = mode.spiral_positions(h.geometry)[2]

    assert len(positions) == 15                 # 5 cells per turn, 3 turns shown
    assert np.isclose(wavelength, 5.0)          # q = 1/5 on a unit-spaced chain
    assert len(marks) == 3                      # one per turn in view
    assert np.allclose(marks, [0.0, 5.0, 10.0])


def test_marks_follow_the_wavelength_not_the_unit_cell(mode):
    """With several turns per supercell the wavelength is not a whole number
    of cells, and a turn ends partway through one - which is exactly what the
    marks have to show. q = 3/10 gives a 10-cell supercell holding 3 turns,
    so the wavelength is 10/3 lattice constants."""
    _configure(mode, lattice="Chain", qvector="0.3, 0.0")
    set_field(mode, "spiral_ldos_nrep", 1)
    activate(mode)
    h = mode.initialize()
    es, ds = mode.compute_spiral_ldos(h, energies=np.linspace(-3, 3, 4),
                                      delta=0.3, nk=4)
    marks = mode.write_spiral_ldos(es, ds, h.geometry, nrep=1)
    positions = _read_map(len(es))[0]

    # the axis is real-space position: one supercell, ten unit cells
    assert len(positions) == 10
    assert np.allclose(np.diff(positions), 1.0)
    # three turns inside it, at non-integer positions
    assert np.allclose(marks, [0.0, 10. / 3., 20. / 3.])


def test_marks_are_dropped_for_too_many_turns(mode):
    """Past MAX_MARKED_PERIODS the lines would be a hatch over the map."""
    assert mode.wavelength_marks(0.0, 10.0, 1.0) == pytest.approx(
        [float(i) for i in range(11)])
    assert mode.wavelength_marks(0.0, 1e4, 1.0) == []      # far too many
    assert mode.wavelength_marks(0.0, 10.0, 0.0) == []     # no spiral at all


def test_the_plot_command_carries_the_guide_lines(mode, calls):
    from _handler_harness import run_button
    _configure(mode, lattice="Chain", qvector="0.25, 0.0", rashba=0.4)
    set_field(mode, "spiral_ldos_ne", 6)
    set_field(mode, "spiral_ldos_nk", 4)
    run_button(mode, "show_spiral_ldos")
    import shlex
    command = shlex.split([c for c in calls if "ql-map2d" in c][-1])
    vlines = [a for a in command if a.startswith("--vlines")]
    assert len(vlines) == 1
    marks = vlines[0].split("=", 1)[1].split(",")
    assert len(marks) == 3  # three turns of the spiral shown by default


def test_the_emitted_plot_command_actually_parses(mode, calls):
    """Run the real ql-map2d's argument parser against the exact command the
    handler emits.

    This is not a formality: the unit-cell guide lines start half a cell
    *before* the origin, so the list of positions begins with a minus sign.
    Passed as a separate token, argparse reads that as another option name
    and rejects the whole command ("expected one argument") - the plot simply
    never opened, with the error going only to the script's log. Asserting on
    the command string alone would not have caught it; only the real parser
    does.

    Pointed at an input file that does not exist, so the script parses its
    arguments and then dies reading the file, without ever opening a window.
    """
    import shlex
    import subprocess

    from _handler_harness import QLROOT, run_button

    _configure(mode, lattice="Chain", qvector="0.25, 0.0", rashba=0.4)
    set_field(mode, "spiral_ldos_ne", 6)
    set_field(mode, "spiral_ldos_nk", 4)
    run_button(mode, "show_spiral_ldos")

    command = shlex.split([c for c in calls if "ql-map2d" in c][-1])
    script = os.path.join(QLROOT, "utilities", command[0])
    args = ["no_such_file.OUT" if a == "SPIRAL_LDOS.OUT" else a for a in command[1:]]
    proc = subprocess.run([sys.executable, script] + args,
                          capture_output=True, text=True)

    assert proc.returncode != 2, "ql-map2d rejected its arguments:\n" + proc.stderr
    assert "expected one argument" not in proc.stderr
    assert "unrecognized arguments" not in proc.stderr
