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
to RESTRICTED_TERMS below (a dropdown item: to ITEM_RULES) - no other code
needs to change, every mode that already calls connect() picks it up for
free. To add a new rule
(a different geometry family entirely): write a new `is_..._family`
predicate next to is_honeycomb_family and reference it from new entries.

connect() also filters the items of the operator, parameter-sweep and
SCF "Initial guess" dropdowns (RESTRICTED_COMBOS) by ITEM_RULES: each item
follows a lattice rule or a term field's shown/hidden rule, so e.g. the
spin operators disappear for a Spinless Hamiltonian and the "antiferro"
guess wherever the Antiferromagnetism field does. Every call rebuilds each
dropdown from its full list in its original order and keeps the user's
last pick selected whenever it is offered (_restrict_combo_items()).

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
both modules' rules before calling setVisible() once. That boolean is
term_shown(), which the generated code preview (codeview.is_active())
and add_staggered_term() also use, so a hidden term is off everywhere.

add_staggered_term() is how a mode builds the mAB/mAF terms: pyqula
refuses add_sublattice_imbalance/add_antiferromagnetism on a geometry
without the sublattice structure they stagger, even for a zero value."""


from collections import namedtuple

import numpy as np

from . import hamiltoniantype


# Lattice options named like a honeycomb lattice whose geometry pyqula
# builds without sublattice labels (multilayers.get_geometry() sets
# has_sublattice=False), so Haldane/Kane-Mele add nothing there, the valley
# operator reads zero and mAB/mAF have nothing to stagger. Exact names, from
# hofstader1d, the only mode offering them; a mode that builds a lattice of
# the same name *with* labels should name it differently.
UNLABELLED_LATTICES = {"Bilayer graphene AB", "Bilayer graphene AA"}


def is_honeycomb_family(lattice_name):
    """True for any lattice whose name marks it as honeycomb-derived:
    plain honeycomb (any cell/supercell choice), multilayer/bilayer/
    twisted graphene, hyperhoneycomb, etc. Substring-based rather than an
    exhaustively maintained enumerated list, so a new LATTICES entry
    added to any mode in the future is classified automatically as long
    as it's named the usual way ("... Honeycomb ...","... Graphene..."),
    the convention every mode already follows - no extra wiring needed
    here when a mode grows a new honeycomb-like lattice option."""
    if lattice_name in UNLABELLED_LATTICES: return False
    name = (lattice_name or "").lower()
    return "honeycomb" in name or "graphene" in name


def is_sublattice_family(lattice_name):
    """True for any lattice whose geometry has more than one sublattice
    (pyqula's `has_sublattice=True`): honeycomb-family (see
    is_honeycomb_family) plus Lieb, Diamond and the two-site chain
    ("Bichain"), and never an UNLABELLED_LATTICES entry.
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
    if lattice_name in UNLABELLED_LATTICES: return False
    name = (lattice_name or "").lower()
    return (is_honeycomb_family(lattice_name)
            or "lieb" in name or "diamond" in name or "bichain" in name)


# Each entry restricts term fields to lattices for which
# `rule(lattice_name)` is True: base widget names (LineEdit fields, their
# *_image formula labels, ...), shown only when the rule holds. Matched
# against every attribute on the page whose name is the base name itself,
# base+"_image", or base+"_N" for any digits N - the latter covers
# hybridfilm/hybridribbon's per-part fields ("haldane_2", and
# "haldane_3"/"haldane_4"/... built at runtime by hybridparts.py once the
# user picks more than 2 parts), without this list needing to enumerate a
# widget per part. Dropdown items are restricted through ITEM_RULES below.
RESTRICTED_TERMS = [
    {"kind": "widget", "names": ["haldane"], "rule": is_honeycomb_family},
    {"kind": "widget", "names": ["antihaldane"], "rule": is_honeycomb_family},
    {"kind": "widget", "names": ["kanemele"], "rule": is_honeycomb_family},
    {"kind": "widget", "names": ["antikanemele"], "rule": is_honeycomb_family},
    {"kind": "widget", "names": ["mAB"], "rule": is_sublattice_family},
    {"kind": "widget", "names": ["mAF"], "rule": is_sublattice_family},
]


# What the dropdown rules below are evaluated against: the page's lattice
# name (None: the page doesn't restrict by lattice), its Hamiltonian type
# (hamiltoniantype.HAMILTONIAN_TYPES) and the dimensionality of the
# Hamiltonian it builds (None: not stated). connect() builds one per call.
Context = namedtuple("Context", ["lattice_name", "hamiltonian_type", "dimensionality"])


def _follows(term):
    """An item offered exactly where the term field `term` is shown."""
    return lambda c: term_shown(term, c.lattice_name, c.hamiltonian_type)


def _on_lattice(rule):
    """An item offered on lattices for which `rule(lattice_name)` holds."""
    return lambda c: c.lattice_name is None or rule(c.lattice_name)


def _in_dimensions(*dims):
    """An item offered only for a Hamiltonian of one of these dimensionalities."""
    return lambda c: c.dimensionality is None or c.dimensionality in dims


# Dropdown items that only apply to some pages: {item text, lower-cased:
# rule(Context)}. Matched case-insensitively, since the same operator is
# "Valley" in some Designer lists and "valley" in pyqula's
# operators.operator_list (common.get_operator() accepts both). Operators
# pyqula refuses on the wrong Hilbert space follow a term with the same
# requirement: the spin operators follow the (spin-only) exchange field,
# and the hole projector the (Nambu-only) s-wave pairing. pyqula defines
# the Berry-curvature operators only in 2d, and the bulk/surface projectors
# up to 2d. The SCF initial guesses are pyqula meanfield.guess() modes,
# each following the term it seeds.
ITEM_RULES = {
    "valley": _on_lattice(is_honeycomb_family),
    "sublattice": _on_lattice(is_sublattice_family),
    "sx": _follows("exchange"),
    "sy": _follows("exchange"),
    "sz": _follows("exchange"),
    "hole": _follows("swave"),
    "berry": _in_dimensions(2),
    "valleyberry": _in_dimensions(2),
    "bulk": _in_dimensions(0, 1, 2),
    "surface": _in_dimensions(0, 1, 2),
    "sublattice imbalance": _follows("mAB"),
    "antiferromagnetism": _follows("mAF"),
    "ferro": _follows("exchange"),
    "rashba": _follows("rashba"),
    "swave": _follows("swave"),
    "pwave": _follows("pwave"),
    "haldane": _follows("haldane"),
    "kanemele": _follows("kanemele"),
    "antihaldane": _follows("antihaldane"),
    "antiferro": _follows("mAF"),
    "imbalance": _follows("mAB"),
}


# The dropdowns ITEM_RULES filters. Each is rebuilt from its full item
# list - whatever qtwrap.set_combobox() last filled it with, else its
# Designer items as first seen - so an item that comes back returns to its
# own place rather than the end. heavyfermion's own bands_color/fs_operator
# lists (dispersive_electrons/kondo_sites/None) contain no ITEM_RULES item,
# so they pass through unchanged.
RESTRICTED_COMBOS = ["bands_color", "dos_operator", "operator_kdos",
                     "fs_operator", "topology_operator", "operator_chern",
                     "sweep_parameter", "scf_initialization"]


# scf_initialization's full list is built here rather than taken from
# Designer: a guess mode per term field this page has ({term: mode}, in
# this order), "random" (valid for any Hamiltonian), then the guesses for
# the lattice-restricted terms, which are offered whether or not the page
# has the field itself.
_GUESS_FOR_TERM = {"exchange": "ferro", "rashba": "rashba", "swave": "swave",
                   "pwave": "pwave"}
_LATTICE_GUESSES = ["Haldane", "kanemele", "antihaldane", "antiferro", "imbalance"]


def _scf_guess_items(form):
    items = [mode for term, mode in _GUESS_FOR_TERM.items()
             if getattr(form, term, None) is not None]
    return items + ["random"] + _LATTICE_GUESSES


def _item_allowed(item, context, exclude=()):
    if item.lower() in exclude: return False
    rule = ITEM_RULES.get(item.lower())
    return rule is None or rule(context)


def _restrict_combo_items(combo, all_items, allowed):
    """Rebuild `combo` as `all_items` filtered by allowed(item), keeping the
    user's choice: the item last selected by anything but this rebuild (a
    click, or a saved session being loaded) is selected again as soon as it
    is offered again - Sz after a Spinless -> Spinful round trip, say - and
    until then the current item if still offered, else the first."""
    if not hasattr(combo, "_wanted"):
        combo._wanted = combo.currentText()
        combo._restricting = False
        combo.currentTextChanged.connect(
            lambda text, c=combo: None if c._restricting else setattr(c, "_wanted", text))
    items = [t for t in all_items if allowed(t)]
    current = combo.currentText()
    target = (combo._wanted if combo._wanted in items
              else current if current in items else (items[0] if items else ""))
    if items == [combo.itemText(i) for i in range(combo.count())] and target == current:
        return
    combo._restricting = True
    try:
        combo.blockSignals(True)
        combo.clear()
        combo.addItems(items)
        combo.blockSignals(False)
        if target: combo.setCurrentIndex(items.index(target))
    finally:
        combo._restricting = False


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


def term_shown(name, lattice_name, hamiltonian_type=hamiltoniantype.DEFAULT_TYPE):
    """Whether the term field `name` is shown for `lattice_name` and
    `hamiltonian_type`: the AND of every RESTRICTED_TERMS widget rule
    naming it and hamiltoniantype.term_allowed(). The one definition
    apply_term_restrictions() (what the page shows), add_staggered_term()
    (what gets built) and codeview.is_active() (what the generated code
    shows) all share, so a hidden term is off in all three. A
    `lattice_name` of None means the mode does not restrict terms by
    lattice (it never calls connect()), so only the Hamiltonian type
    counts."""
    ok = hamiltoniantype.term_allowed(hamiltonian_type, name)
    if lattice_name is None: return ok
    for entry in RESTRICTED_TERMS:
        if entry["kind"] == "widget" and name in entry["names"]:
            ok = ok and entry["rule"](lattice_name)
    return ok


def apply_term_restrictions(form, lattice_name, hamiltonian_type=hamiltoniantype.DEFAULT_TYPE):
    """Show/hide every registered restricted term on `form` according to
    term_shown() - whether `lattice_name` (this module's own
    RESTRICTED_TERMS) and `hamiltonian_type`
    (hamiltoniantype.SPIN_TERMS/PAIRING_TERMS) allow it, AND-ed together
    per widget base name (see this module's docstring for why a term named
    by both, e.g. kanemele/mAF, needs a combined boolean rather than two
    independent setVisible() passes) - and filter every RESTRICTED_COMBOS
    dropdown's items by ITEM_RULES the same way. The rest of the page's
    setup (dimensionality, restrict_widgets, exclude_items) is what
    connect() recorded on it. Safe to call on any page: widgets/comboboxes
    this particular mode doesn't have are skipped."""
    config = getattr(form, "_term_config", {})
    if config.get("restrict_widgets", True):
        names = set(hamiltoniantype.SPIN_TERMS + hamiltoniantype.PAIRING_TERMS)
        for entry in RESTRICTED_TERMS:
            if entry["kind"] == "widget": names.update(entry["names"])
        for name in names:
            _apply_widget_restriction(form, [name],
                                      term_shown(name, lattice_name, hamiltonian_type))
        for name in hamiltoniantype.SPIN_BUTTONS:
            button = getattr(form, name, None)
            if button is not None:
                button.setEnabled(hamiltonian_type != "Spinless")

    dimensionality = config.get("dimensionality")
    if callable(dimensionality): dimensionality = dimensionality()
    context = Context(lattice_name, hamiltonian_type, dimensionality)
    exclude = {item.lower() for item in config.get("exclude_items", ())}
    def allowed(item):
        return _item_allowed(item, context, exclude)
    for combo_name in RESTRICTED_COMBOS:
        combo = getattr(form, combo_name, None)
        if combo is None: continue
        if combo_name == "scf_initialization":
            all_items = _scf_guess_items(form)
        else:
            if not hasattr(combo, "_all_items"): # Designer items, as first seen
                combo._all_items = [combo.itemText(i) for i in range(combo.count())]
            all_items = combo._all_items
        _restrict_combo_items(combo, all_items, allowed)


def connect(qtwrap, get_lattice_name, dimensionality=None, hamiltonian_type=None,
            restrict_widgets=True, exclude_items=(), watch=()):
    """Wire term restrictions to `get_lattice_name()` (a callable
    returning the mode's current lattice-family name, e.g.
    lambda: getbox("lattice"), or a constant for an always-honeycomb
    mode) and, if this page has one, its "hamiltonian_type" combobox
    (built by scfterms.py, see hamiltoniantype.py). Applies once
    immediately, and again whenever either combobox changes (covers both
    direct user interaction and a saved session being reloaded into it -
    see qtwrap.py's load_interface()).

      dimensionality   - of the Hamiltonian the page builds (an int, or a
                         callable for a page where it depends on the
                         lattice), for the dimension-limited dropdown items
                         (ITEM_RULES' _in_dimensions()).
      hamiltonian_type - a callable returning the page's Hamiltonian type,
                         for a page without the hamiltonian_type combobox
                         whose Hamiltonian isn't simply spinful (tbg is
                         always spinless, tmdc becomes Nambu with pairing).
      restrict_widgets - False for a page whose term fields must not be
                         hidden by these rules, which then only filter its
                         dropdowns (spinspiral names its intrinsic SOC field
                         kanemele, which RESTRICTED_TERMS would hide on
                         both of its non-honeycomb lattices).
      exclude_items    - dropdown items this page never offers, for what
                         no general rule captures (tbg's valleyberry, which
                         pyqula can't compute on a sparse Hamiltonian).
      watch            - more field names whose edits re-apply the rules
                         (tmdc's swave, which decides its Hamiltonian type)."""
    form = qtwrap.form
    form._term_config = dict(dimensionality=dimensionality,
                             restrict_widgets=restrict_widgets,
                             exclude_items=tuple(exclude_items))
    # kept on the page so codeview.is_active() can ask term_shown() the
    # same question for the generated code preview - only where the rules
    # also decide which term fields the page shows
    if restrict_widgets: form._term_lattice_name = get_lattice_name
    get_type = hamiltonian_type or (lambda: hamiltoniantype.get_type(qtwrap))
    def _update(*_args):
        apply_term_restrictions(form, get_lattice_name(), get_type())
    # qtwrap.set_combobox() re-applies through this after refilling a
    # dropdown, for a mode that fills one only after calling connect()
    form._reapply_term_restrictions = _update
    lattice_widget = getattr(form, "lattice", None)
    if lattice_widget is not None:
        lattice_widget.currentTextChanged.connect(_update)
    hamtype_widget = getattr(form, "hamiltonian_type", None)
    if hamtype_widget is not None:
        hamtype_widget.currentTextChanged.connect(_update)
    for name in watch:
        widget = getattr(form, name, None)
        if widget is not None: widget.textChanged.connect(_update)
    _update()


# The two staggered terms whose pyqula method needs a particular
# sublattice structure in the *built* geometry: {field name: (Hamiltonian
# method, the field's label in the UI, whether geometry g supports it,
# what it needs, in words)}. pyqula raises on a geometry without that
# structure - even for a zero value - rather than quietly adding nothing,
# so a mode never calls these two methods directly: it goes through
# add_staggered_term() below.
_STAGGERED_TERMS = {
    "mAB": ("add_sublattice_imbalance", "Sublattice imbalance",
            lambda g: g.has_sublattice and g.sublattice_number == 2,
            "exactly two sublattices"),
    "mAF": ("add_antiferromagnetism", "Antiferromagnetism",
            lambda g: g.has_sublattice,
            "a sublattice structure"),
}


def _is_zero(value):
    """A field value that adds nothing. A callable (a position-dependent
    "r: <expr>" field, or hybridparts' per-part interpolator) counts as
    nonzero."""
    if callable(value): return False
    return bool(np.all(np.asarray(value) == 0))


def add_staggered_term(h, name, value, lattice_name=None):
    """Add the staggered term `name` ("mAB" or "mAF", see _STAGGERED_TERMS)
    with `value` to h, the way every mode's Hamiltonian builder should:

      - a zero value adds nothing;
      - a field term_shown() hides for `lattice_name` adds nothing either,
        so a stale value left in a field the user can no longer see is
        off, as it is in the generated code (codeview.is_active());
      - a shown, nonzero field on a geometry that supports the term is
        added;
      - a shown, nonzero field on a geometry that does not raises a
        ValueError worded for the error InfoBar, instead of the term
        silently doing nothing. No lattice option does that today (the
        lattice rules follow the built geometries, UNLABELLED_LATTICES
        included), so this is the guard for a new lattice whose name the
        rules misclassify, e.g. after atoms are removed.

    `lattice_name` is the same name the mode passes to connect() -
    getbox("lattice"), or a constant for an always-honeycomb mode - passed
    in rather than read off the page so this also works through a
    DictForm accessor in a subprocess calculation. None means the mode
    does not restrict terms by lattice. The spin side of term_shown()
    (mAF on a Spinless Hamiltonian) is not checked here: callers already
    skip every spin term for Spinless, since pyqula's add_antiferromagnetism
    would turn the Hamiltonian spinful (see hamiltoniantype.py)."""
    method, label, supports, needs = _STAGGERED_TERMS[name]
    if _is_zero(value): return
    if not term_shown(name, lattice_name): return
    g = h.geometry
    if not supports(g):
        have = str(g.sublattice_number) if g.has_sublattice else "none"
        where = "the selected lattice (%s)" % lattice_name if lattice_name else "this geometry"
        raise ValueError("%s needs a lattice with %s, and %s has %s. Set it "
                         "to 0, or choose a lattice with two sublattices, such "
                         "as a honeycomb one." % (label, needs, where, have))
    getattr(h, method)(value)
