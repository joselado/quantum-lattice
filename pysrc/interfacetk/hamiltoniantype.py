"""Registry + runtime widget for the "Hamiltonian type" choice (Spinless /
Spinful / Nambu) shared by every mode that has the SCF switch (0d, 1d, 2d,
3d, 2dslab, multilayergraphene, hybridfilm, hybridribbon).

The combobox itself is built by scfterms.py's _nest_scf_tab() (this module
only supplies the row via build_row() - it doesn't touch layout/tab
structure itself), directly above the "do_scf" SwitchButton it already
pins to the bottom of the "Terms in the Hamiltonian" panel, so both
controls that describe "what shape is this Hamiltonian" sit together.
Defaults to "Spinful" (has_spin=True, has_eh=False) - the mode every
<mode>.py's generate/initialize() function already assumed before this
module existed.

Two disjoint groups of single-particle/mean-field term fields are gated by
the current choice:

  - SPIN_TERMS: fields with no meaning for a spinless Hamiltonian
    (exchange, kanemele, antikanemele, rashba, mAF, J1, J2, J3) - hidden
    unless "Spinless" is *not* selected (i.e. shown for Spinful and
    Nambu).
  - PAIRING_TERMS: the BdG pairing fields (swave, pwave) - hidden unless
    "Nambu" is selected.

term_allowed() is the single source of truth both apply_term_restrictions()
consumers (widget visibility, via latticeterms.py - see that module's
apply_term_restrictions(), which combines this module's rule with its own
per-lattice-family rules) and codeview.py's is_active() (so the generated
"pyqula code" preview never shows a call to a term hidden by the current
Hamiltonian-type choice, even if the field still holds a stale nonzero
value from before the type was switched) build on.

A mode's own generate/initialize() Hamiltonian-building code is
responsible for actually skipping the matching add_*() calls, not just
hiding the widget - see wants_spin()/wants_nambu() below. This matters
because several of pyqula's own add_*() methods (add_zeeman/add_exchange,
add_kane_mele, add_anti_kane_mele, add_rashba, add_antiferromagnetism)
unconditionally call self.turn_spinful() *before* even looking at the
value passed in, so calling one of them with a zero-valued field on a
has_spin=False Hamiltonian would silently promote it back to spinful,
defeating the "Spinless" choice regardless of the UI hiding its field.
add_haldane/add_antihaldane/add_sublattice_imbalance carry no such
side effect (they adapt to whatever h.has_spin already is via
spinless2full()), so they stay unconditional in every mode - only the
five SPIN_TERMS above need this guard on the actual add_*() call, on top
of the visibility hide every SPIN_TERMS field also gets.

Nambu is treated as "spinful with an added electron-hole sector"
(pyqula's "spinful_nambu" mode) rather than also offering a
"spinless Nambu" combination - h.setup_nambu_spinor() (equivalent to
h.add_swave(0.0)) is called once a mode's generate/initialize() has
applied every single-particle term, to establish the BdG structure even
when swave/pwave are both left at zero, before the existing (unchanged)
conditional swave/pwave add_*() calls run."""
from PySide6.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import BodyLabel, ComboBox

HAMILTONIAN_TYPES = ["Spinless", "Spinful", "Nambu"]
DEFAULT_TYPE = "Spinful"

SPIN_TERMS = ["exchange", "kanemele", "antikanemele", "rashba", "mAF",
              "J1", "J2", "J3"]
PAIRING_TERMS = ["swave", "pwave"]

# The subset of SPIN_TERMS that are actual single-particle add_*() calls a
# mode's generate/initialize() must skip outright for "Spinless" (rather
# than call with a zero value) - see this module's docstring. J1/J2/J3
# aren't add_*()'d directly; they're SCF interaction parameters already
# routed correctly by the existing `if h.has_spin:` branch in
# common.solve_scf()/pyqula_code_scf_block() and every mode's own
# solve_scf(), once has_spin itself is wired to this combobox.
SPIN_FORCING_TERMS = ["exchange", "kanemele", "antikanemele", "rashba", "mAF"]


def get_type(qtwrap):
    """The currently selected Hamiltonian type, or DEFAULT_TYPE if this
    page has no hamiltonian_type combobox (a mode without the SCF switch)."""
    form = qtwrap.form if hasattr(qtwrap, "form") else qtwrap
    widget = getattr(form, "hamiltonian_type", None)
    if widget is None: return DEFAULT_TYPE
    return widget.currentText() or DEFAULT_TYPE


def wants_spin(qtwrap):
    """Whether the Hamiltonian should be built with has_spin=True - true
    for both "Spinful" and "Nambu" (Nambu here always means spinful
    Nambu/BdG, see this module's docstring)."""
    return get_type(qtwrap) != "Spinless"


def wants_nambu(qtwrap):
    return get_type(qtwrap) == "Nambu"


def term_allowed(hamiltonian_type, name):
    """Whether term `name` should be visible/active for `hamiltonian_type`.
    Terms not in SPIN_TERMS or PAIRING_TERMS (the orbital-only terms:
    hopping, fermi, mAB, haldane, antihaldane, crystalfield, peierls,
    inplaneb, strain, U, V1, V2, ...) are unrestricted - always True."""
    if name in SPIN_TERMS: return hamiltonian_type != "Spinless"
    if name in PAIRING_TERMS: return hamiltonian_type == "Nambu"
    return True


def build_row(form):
    """Build the "Hamiltonian type" label+combobox row. Returned widget is
    placed by scfterms.py's _nest_scf_tab(), directly above the do_scf
    switch row it already builds. Wires currentIndexChanged to
    form._mark_dirty directly (mirroring _build_scf_switch_row()'s own
    switch.checkedChanged wiring) since this widget, like the switch, is
    built after _AppBase._connect_dirty_tracking() already walked the
    page's Designer-authored widgets and so isn't covered by that sweep."""
    combo = ComboBox(form)
    combo.addItems(HAMILTONIAN_TYPES)
    combo.setCurrentText(DEFAULT_TYPE)
    combo.setObjectName("hamiltonian_type")
    setattr(form, "hamiltonian_type", combo)
    combo.currentIndexChanged.connect(form._mark_dirty)

    row = QWidget(form)
    row_layout = QHBoxLayout(row)
    row_layout.setContentsMargins(0, 0, 0, 4)
    row_layout.addWidget(BodyLabel("Hamiltonian type", row))
    row_layout.addStretch(1)
    row_layout.addWidget(combo)
    return row
