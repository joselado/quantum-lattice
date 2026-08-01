"""Registry for Hamiltonian terms/operators that only make physical
sense for certain lattice geometries. Two different rules are in play
here, both proxying for pyqula's own per-geometry `has_sublattice` flag
(see geometry.py) by lattice name since the UI only has the name, not
the built geometry object, at restriction time:

  - is_honeycomb_family: the Haldane/Kane-Mele spin-orbit terms and the
    "valley" operator are honeycomb-specific physics (they come from
    graphene's particular next-nearest-neighbor structure), so they're
    restricted to honeycomb-derived lattices only (plain honeycomb,
    multilayer/bilayer/twisted graphene, hyperhoneycomb, ...) even though
    other lattice families also have a sublattice basis.
  - is_sublattice_family: the sublattice imbalance ("mAB") and
    antiferromagnetism ("mAF") mass terms are generic staggered on-site
    terms that make sense on *any* lattice with more than one sublattice,
    so they're restricted more broadly - honeycomb-derived lattices plus
    Lieb and Diamond - not just plain Square/Triangular/Cubic.

A mode wires this up with one call:

    from interfacetk import latticeterms
    latticeterms.connect(qtwrap,lambda: getbox("lattice"))

(or, for a mode whose geometry is always honeycomb-derived regardless of
any UI choice, e.g. tbg/multilayergraphene:

    latticeterms.connect(qtwrap,lambda: "Honeycomb")

This is deliberately explicit per mode rather than auto-detected from a
widget literally named "lattice", since that name isn't always a
lattice-family selector - multilayergraphene's own "lattice" combobox
actually holds a layer-stacking code (e.g. "ABA"), not a family name.
connect() applies the current classification once immediately and again
on every change of the mode's own "lattice" combobox, if it has one.

To restrict a new term to an existing rule in the future: add one entry
to RESTRICTED_TERMS below - no other code needs to change, every mode
that already calls connect() picks it up for free. To add a new rule
(a different geometry family entirely): write a new `is_..._family`
predicate next to is_honeycomb_family and reference it from new entries.

connect() also owns the SCF tab's "Initial guess" (scf_initialization)
dropdown - not a lattice restriction itself, but built from the same
per-term/per-lattice information this module already tracks, so it's
kept here rather than duplicating that logic elsewhere. Every call to
apply_term_restrictions() rebuilds it down to exactly {a
meanfield.guess() mode per Hamiltonian term this mode/lattice
combination actually has} + "random" - see
_rebuild_scf_initialization_baseline() and _UNRESTRICTED_GUESS_TERMS.

apply_term_restrictions()/connect() also fold in hamiltoniantype.py's own
Spinless/Spinful/Nambu-based restrictions (SPIN_TERMS/PAIRING_TERMS), so a
term hidden for either reason - wrong lattice family *or* wrong
Hamiltonian type - stays hidden regardless of the other. This matters
because three terms are governed by both modules at once: kanemele/mAF
are honeycomb-/sublattice-family-restricted here *and* spin-only in
hamiltoniantype.py, so e.g. a Spinless Honeycomb selection must hide
kanemele for the spin reason even though the lattice itself would allow
it. Two independent sequential setVisible() passes would be
order-dependent (whichever module's pass runs last would win, silently
un-hiding what the other just hid) - apply_term_restrictions() avoids
that by computing one AND-combined boolean per widget base name across
both modules' rules before calling setVisible() once."""


from . import hamiltoniantype


def is_honeycomb_family(lattice_name):
    """True for any lattice whose name marks it as honeycomb-derived:
    plain honeycomb (any cell/supercell choice), multilayer/bilayer/
    twisted graphene, hyperhoneycomb, etc. Substring-based rather than an
    exhaustively maintained enumerated list, so a new LATTICES entry
    added to any mode in the future is classified automatically as long
    as it's named the usual way ("... Honeycomb ...","... Graphene..."),
    the convention every mode already follows - no extra wiring needed
    here when a mode grows a new honeycomb-like lattice option."""
    name = (lattice_name or "").lower()
    return "honeycomb" in name or "graphene" in name


def is_sublattice_family(lattice_name):
    """True for any lattice whose geometry has more than one sublattice
    (pyqula's `has_sublattice=True`): honeycomb-family (see
    is_honeycomb_family) plus Lieb and Diamond.
    Substring-based for the same reasons as is_honeycomb_family - a new
    LATTICES entry for one of these families is classified automatically
    as long as it's named the usual way ("... Lieb ...","... Diamond...").
    Plain Square/Triangular/Cubic/Kagome/Pyrochlore lattices are excluded
    here (even though Kagome and Pyrochlore are `has_sublattice=True` in
    geometry.py, they're deliberately excluded from this UI-facing rule
    on request - this is a hand-maintained list, not a live query against
    geometry.py's actual flag, so a *future* lattice family that also has
    a real sublattice basis but isn't named Honeycomb/Graphene/Lieb/
    Diamond will be silently classified as False here and need adding to
    this list by hand)."""
    name = (lattice_name or "").lower()
    return (is_honeycomb_family(lattice_name)
            or "lieb" in name or "diamond" in name)


# Each entry restricts one term/operator to lattices for which
# `rule(lattice_name)` is True.
#
#   "widget"     - base widget names (LineEdit fields, their *_image
#                  formula labels, ...), shown only when the rule holds.
#                  Matched against every attribute on the page whose name
#                  is the base name itself, base+"_image", or base+"_N"
#                  for any digits N - the latter covers hybridfilm/
#                  hybridribbon's per-part fields ("haldane_2", and
#                  "haldane_3"/"haldane_4"/... built at runtime by
#                  hybridparts.py once the user picks more than 2 parts),
#                  without this list needing to enumerate a widget per part.
#   "combo_item" - one specific item text kept in/out of each listed
#                  QComboBox's item list depending on the rule. Item text
#                  is given per combobox since the same term shows up
#                  with different casing depending on where it comes
#                  from: "topology_operator"/"operator_chern" are static
#                  Designer items ("Valley"), while "bands_color"/
#                  "operator_kdos"/"dos_operator" (and 2d.py's own
#                  "fs_operator") are populated at runtime from pyqula's
#                  operators.operator_list, which uses lowercase "valley" -
#                  "fs_operator" is NOT populated generically by any shared
#                  code (common.py:initialize() deliberately leaves it
#                  alone): heavyfermion's own "fs_operator" keeps a
#                  hand-authored, mode-specific item list
#                  (dispersive_electrons/kondo_sites/None) that a generic
#                  operators.operator_list population would silently
#                  clobber, so only 2d.py (the one other mode with this
#                  field) populates it itself.
RESTRICTED_TERMS = [
    {"kind": "widget", "names": ["haldane"], "rule": is_honeycomb_family},
    {"kind": "widget", "names": ["antihaldane"], "rule": is_honeycomb_family},
    {"kind": "widget", "names": ["kanemele"], "rule": is_honeycomb_family},
    {"kind": "widget", "names": ["antikanemele"], "rule": is_honeycomb_family},
    {"kind": "widget", "names": ["mAB"], "rule": is_sublattice_family},
    {"kind": "widget", "names": ["mAF"], "rule": is_sublattice_family},
    {"kind": "combo_item",
     "items": {"topology_operator": "Valley", "operator_chern": "Valley",
               "bands_color": "valley", "fs_operator": "valley",
               "operator_kdos": "valley", "dos_operator": "valley"},
     "rule": is_honeycomb_family},
    {"kind": "combo_item",
     "items": {"sweep_parameter": "Sublattice imbalance"},
     "rule": is_sublattice_family},
    {"kind": "combo_item",
     "items": {"sweep_parameter": "Antiferromagnetism"},
     "rule": is_sublattice_family},
    # scf_initialization ("Initial guess") items for the same three
    # honeycomb-restricted terms and the two sublattice-restricted mass
    # terms above - same rule, same combobox, added/removed the same way.
    # meanfield.guess()'s mode strings, not the term field names
    # themselves (see _rebuild_scf_initialization_baseline()'s docstring).
    {"kind": "combo_item", "items": {"scf_initialization": "Haldane"},
     "rule": is_honeycomb_family},
    {"kind": "combo_item", "items": {"scf_initialization": "kanemele"},
     "rule": is_honeycomb_family},
    {"kind": "combo_item", "items": {"scf_initialization": "antihaldane"},
     "rule": is_honeycomb_family},
    {"kind": "combo_item", "items": {"scf_initialization": "antiferro"},
     "rule": is_sublattice_family},
    {"kind": "combo_item", "items": {"scf_initialization": "imbalance"},
     "rule": is_sublattice_family},
]


# scf_initialization ("Initial guess") items tied 1:1 to a Hamiltonian
# term this mode has, whose availability never changes once the page is
# built (unlike the honeycomb-/sublattice-restricted terms above, which
# can turn on/off after a lattice change): {term field name: the matching
# pyqula meanfield.guess() mode string}. "random" is offered unconditionally
# alongside these, since meanfield.guess(mode="random") is valid for any
# Hamiltonian regardless of which terms exist.
_UNRESTRICTED_GUESS_TERMS = {
    "exchange": "ferro",
    "rashba": "rashba",
    "swave": "swave",
    "pwave": "pwave",
}


# scf_initialization combo_item entries in RESTRICTED_TERMS above whose
# item text names a term that hamiltoniantype.py also restricts by spin
# (kanemele, mAF) - so apply_term_restrictions() can additionally require
# hamiltoniantype.term_allowed() for exactly these two, on top of the
# lattice-family rule already attached to them. "Haldane"/"antihaldane"
# (haldane/antihaldane) and "imbalance" (mAB) are orbital-only and need no
# such extra check.
_GUESS_ITEM_TO_HAMTYPE_TERM = {"kanemele": "kanemele", "antiferro": "mAF"}


def _rebuild_scf_initialization_baseline(form, hamiltonian_type):
    """Fully rebuild the "Initial guess" (scf_initialization) dropdown
    down to exactly {a meanfield.guess() mode per Hamiltonian term this
    mode's page has *and* hamiltoniantype.term_allowed() currently allows,
    from _UNRESTRICTED_GUESS_TERMS} + "random" - discarding any
    Designer-authored placeholder items or a previous rebuild's leftovers.
    Called first, at the top of apply_term_restrictions() below, so its
    own combo_item entries for scf_initialization
    (Haldane/kanemele/antihaldane/antiferro/imbalance) then add back
    exactly the ones the *current* lattice choice allows, on top of this
    always-present baseline. Returns the pre-rebuild selection's text so
    the caller can restore it once the *full* item list (this baseline
    plus the conditional combo_item entries added afterwards) is
    assembled - restoring here would be premature, since e.g. "antiferro"
    (a combo_item entry, not part of this baseline) hasn't been re-added
    yet at this point."""
    combo = getattr(form, "scf_initialization", None)
    if combo is None: return ""
    current = combo.currentText()
    combo.blockSignals(True)
    combo.clear()
    for term, mode in _UNRESTRICTED_GUESS_TERMS.items():
        if getattr(form, term, None) is None: continue
        if not hamiltoniantype.term_allowed(hamiltonian_type, term): continue
        combo.addItem(mode)
    combo.addItem("random")
    combo.blockSignals(False)
    return current


def _matches_base(base, attr_name):
    if attr_name == base or attr_name == base + "_image": return True
    if attr_name.startswith(base + "_"):
        rest = attr_name[len(base)+1:]
        if rest.isdigit(): return True
        # a per-part formula image (hybridparts.py's "<name>_<N>_image",
        # e.g. "haldane_2_image") - the digit-suffixed field itself is
        # already matched above, but its own formula image needs the
        # same treatment or it stays visible/hidden independently of the
        # field it sits next to.
        if rest.endswith("_image") and rest[:-len("_image")].isdigit(): return True
    return False


def _find_layout_item(layout, widget):
    """Recursively search `layout` (and any nested layouts inside it -
    Designer .ui files nest a QGridLayout per "Terms in the Hamiltonian"
    row-group inside an outer one) for `widget`. Returns
    (containing_layout, index) or None."""
    if layout is None: return None
    for i in range(layout.count()):
        item = layout.itemAt(i)
        if item.widget() is widget: return (layout, i)
        found = _find_layout_item(item.layout(), widget)
        if found is not None: return found
    return None


def _row_label_siblings(layout, index):
    """The label(s) Designer placed in the same row as the widget at
    `index` in `layout` - the descriptive text to a term's left (e.g.
    "Haldane"), which doesn't share its field's own widget name (that
    field is "haldane", but its label is "label_haldane" - a different
    attribute name, not one _apply_widget_restriction's name-based
    matching resolves on its own), so this positional walk is still
    needed to find it. Grid layouts: every QLabel sharing this item's
    row. Box layouts (a horizontal "label, field, label, field, ..."
    row): the item immediately before this one, if it's a label."""
    from PySide6.QtWidgets import QGridLayout, QBoxLayout, QLabel
    siblings = []
    if isinstance(layout, QGridLayout):
        row,_col,_rs,_cs = layout.getItemPosition(index)
        for i in range(layout.count()):
            if i == index: continue
            r,_c,_rs2,_cs2 = layout.getItemPosition(i)
            if r == row:
                w = layout.itemAt(i).widget()
                if isinstance(w, QLabel): siblings.append(w)
    elif isinstance(layout, QBoxLayout):
        if index > 0:
            w = layout.itemAt(index - 1).widget()
            if isinstance(w, QLabel): siblings.append(w)
    return siblings


def _apply_widget_restriction(form, base_names, allowed):
    for base in base_names:
        for attr_name, w in list(vars(form).items()):
            if _matches_base(base, attr_name) and hasattr(w, "setVisible"):
                w.setVisible(allowed)
                parent = w.parentWidget()
                found = _find_layout_item(parent.layout() if parent else None, w)
                if found is not None:
                    layout, index = found
                    for label in _row_label_siblings(layout, index):
                        label.setVisible(allowed)


def _apply_combo_item_restriction(form, items, allowed):
    for combo_name, item_text in items.items():
        combo = getattr(form, combo_name, None)
        if combo is None: continue
        idx = combo.findText(item_text)
        if allowed and idx < 0: combo.addItem(item_text)
        elif not allowed and idx >= 0: combo.removeItem(idx)


def apply_term_restrictions(form, lattice_name, hamiltonian_type=hamiltoniantype.DEFAULT_TYPE):
    """Show/hide every registered restricted term on `form` according to
    whether `lattice_name` (this module's own RESTRICTED_TERMS) and
    `hamiltonian_type` (hamiltoniantype.SPIN_TERMS/PAIRING_TERMS) allow it
    - AND-ed together per widget base name (see this module's docstring
    for why a term named by both, e.g. kanemele/mAF, needs a combined
    boolean rather than two independent setVisible() passes). Safe to
    call on any page: entries whose widgets/comboboxes don't exist on
    this particular mode are silently skipped."""
    scf_current = _rebuild_scf_initialization_baseline(form, hamiltonian_type)

    allowed = {} # widget base name -> AND of every rule naming it
    for entry in RESTRICTED_TERMS:
        if entry["kind"] != "widget": continue
        ok = entry["rule"](lattice_name)
        for name in entry["names"]:
            allowed[name] = allowed.get(name, True) and ok
    for name in hamiltoniantype.SPIN_TERMS + hamiltoniantype.PAIRING_TERMS:
        ok = hamiltoniantype.term_allowed(hamiltonian_type, name)
        allowed[name] = allowed.get(name, True) and ok
    for name, ok in allowed.items():
        _apply_widget_restriction(form, [name], ok)

    for entry in RESTRICTED_TERMS:
        if entry["kind"] != "combo_item": continue
        ok = entry["rule"](lattice_name)
        if entry["items"].get("scf_initialization") in _GUESS_ITEM_TO_HAMTYPE_TERM:
            term = _GUESS_ITEM_TO_HAMTYPE_TERM[entry["items"]["scf_initialization"]]
            ok = ok and hamiltoniantype.term_allowed(hamiltonian_type, term)
        _apply_combo_item_restriction(form, entry["items"], ok)

    # Restore the pre-rebuild selection now that the full item list (the
    # unrestricted baseline plus whichever combo_item entries this lattice/
    # Hamiltonian-type combination allows) is assembled - doing this earlier,
    # inside _rebuild_scf_initialization_baseline(), would miss "antiferro"
    # itself, since that's a combo_item entry added by the loop just above,
    # not part of the baseline. On a fresh page this restores the
    # Designer-authored first item in every mode's .ui - "antiferro", the
    # intended default guess; falls back to whatever Qt's combobox
    # defaults to (normally index 0) if the previous selection is no
    # longer offered (e.g. switching away from a sublattice-family
    # lattice while "antiferro" was selected).
    combo = getattr(form, "scf_initialization", None)
    if combo is not None:
        idx = combo.findText(scf_current)
        if idx >= 0: combo.setCurrentIndex(idx)


def connect(qtwrap, get_lattice_name):
    """Wire term restrictions to `get_lattice_name()` (a callable
    returning the mode's current lattice-family name, e.g.
    lambda: getbox("lattice"), or a constant for an always-honeycomb
    mode) and, if this page has one, its "hamiltonian_type" combobox
    (built by scfterms.py, see hamiltoniantype.py). Applies once
    immediately, and again whenever either combobox changes (covers both
    direct user interaction and a saved session being reloaded into it -
    see qtwrap.py's load_interface())."""
    form = qtwrap.form
    def _update(*_args):
        apply_term_restrictions(form, get_lattice_name(), hamiltoniantype.get_type(qtwrap))
    lattice_widget = getattr(form, "lattice", None)
    if lattice_widget is not None:
        lattice_widget.currentTextChanged.connect(_update)
    hamtype_widget = getattr(form, "hamiltonian_type", None)
    if hamtype_widget is not None:
        hamtype_widget.currentTextChanged.connect(_update)
    _update()
