"""Registry for Hamiltonian terms/operators that only make physical
sense for certain lattice geometries - e.g. the Haldane and Kane-Mele
spin-orbit terms, and the "valley" operator, are only meaningful for
honeycomb-derived lattices (plain honeycomb, multilayer/bilayer/twisted
graphene, hyperhoneycomb, ...), not for square/kagome/lieb/triangular/
cubic/diamond/pyrochlore ones. A mode wires this up with one call:

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
"""


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


# Each entry restricts one term/operator to lattices for which
# `rule(lattice_name)` is True.
#
#   "widget"     - plain widgets (LineEdit fields, their *_image formula
#                  labels, ...), shown only when the rule holds.
#   "combo_item" - one specific item text kept in/out of each listed
#                  QComboBox's item list depending on the rule. Item text
#                  is given per combobox since the same term shows up
#                  with different casing depending on where it comes
#                  from: "topology_operator"/"operator_chern" are static
#                  Designer items ("Valley"), while "bands_color"/
#                  "fs_operator"/"operator_kdos"/"dos_operator" are
#                  populated at runtime from pyqula's
#                  operators.operator_list, which uses lowercase "valley".
RESTRICTED_TERMS = [
    {"kind": "widget", "names": ["haldane", "haldane_image", "haldane_2"],
     "rule": is_honeycomb_family},
    {"kind": "widget", "names": ["antihaldane", "antihaldane_image", "antihaldane_2"],
     "rule": is_honeycomb_family},
    {"kind": "widget", "names": ["kanemele", "kanemele_image", "kanemele_2"],
     "rule": is_honeycomb_family},
    {"kind": "widget", "names": ["antikanemele", "antikanemele_image", "antikanemele_2"],
     "rule": is_honeycomb_family},
    {"kind": "combo_item",
     "items": {"topology_operator": "Valley", "operator_chern": "Valley",
               "bands_color": "valley", "fs_operator": "valley",
               "operator_kdos": "valley", "dos_operator": "valley"},
     "rule": is_honeycomb_family},
]


def _apply_widget_restriction(form, names, allowed):
    for name in names:
        w = getattr(form, name, None)
        if w is not None: w.setVisible(allowed)


def _apply_combo_item_restriction(form, items, allowed):
    for combo_name, item_text in items.items():
        combo = getattr(form, combo_name, None)
        if combo is None: continue
        idx = combo.findText(item_text)
        if allowed and idx < 0: combo.addItem(item_text)
        elif not allowed and idx >= 0: combo.removeItem(idx)


def apply_term_restrictions(form, lattice_name):
    """Show/hide every registered restricted term on `form` according to
    whether `lattice_name` satisfies each entry's rule. Safe to call on
    any page: entries whose widgets/comboboxes don't exist on this
    particular mode are silently skipped."""
    for entry in RESTRICTED_TERMS:
        allowed = entry["rule"](lattice_name)
        if entry["kind"] == "widget":
            _apply_widget_restriction(form, entry["names"], allowed)
        elif entry["kind"] == "combo_item":
            _apply_combo_item_restriction(form, entry["items"], allowed)


def connect(qtwrap, get_lattice_name):
    """Wire term restrictions to `get_lattice_name()` (a callable
    returning the mode's current lattice-family name, e.g.
    lambda: getbox("lattice"), or a constant for an always-honeycomb
    mode). Applies once immediately, and again whenever this page's own
    "lattice" combobox changes (covers both direct user interaction and
    a saved session being reloaded into it - see saveload.py)."""
    form = qtwrap.form
    def _update(*_args):
        apply_term_restrictions(form, get_lattice_name())
    lattice_widget = getattr(form, "lattice", None)
    if lattice_widget is not None:
        lattice_widget.currentTextChanged.connect(_update)
    _update()
