"""Support for the "hybrid" modes (hybridfilm, hybridribbon) whose
Hamiltonian parameters are set separately for each of several spatial
parts of the system - originally a fixed Upper/Lower two-way split
(parameter `name` for part 1, `name+"_2"` for part 2), generalized here to
a user-chosen number of parts (2..MAX_PARTS), picked with a "nparts"
combobox already present in each mode's interface.ui next to its
tabWidget_4. Part i's field for parameter `name` is named `name` (i==1)
or `name+"_%d"%i` (i>=2) - matching the existing Designer-authored
Upper/Lower fields exactly, so nparts==2 needs no new widgets at all.

A mode wires this up with two calls:

    from interfacetk import hybridparts
    PARTS_FIELDS = [("strain","Strain"), ("fermi","Fermi energy"), ...]
    hybridparts.connect(qtwrap,PARTS_FIELDS)

    ... inside initialize():
    nparts = hybridparts.current_nparts(qtwrap)
    region_of = hybridparts.region_of_factory(g.z.min(),g.z.max(),nparts)
    fint = lambda name: hybridparts.part_interpolator(get,name,nparts,2,region_of)
    check = lambda name: hybridparts.part_check(get,name,nparts)

connect() only manages widgets (building/showing/hiding part-3+ tabs);
the region_of_factory/part_interpolator/part_check/part_vector_interpolator
helpers below only deal in plain values, so a mode's initialize() stays
free to define its own axis (2/z for hybridfilm, 1/y for hybridribbon)
and its own set of Hamiltonian terms.
"""
import numpy as np
from PySide6.QtWidgets import QWidget, QGridLayout
from qfluentwidgets import BodyLabel, LineEdit

MAX_PARTS = 6


def part_suffix(i):
    """Widget-name suffix for 1-indexed part i, matching the existing
    Designer-authored "_2" convention for part 2."""
    return "" if i == 1 else "_%d" % i


def _parse_nparts(text):
    try: return int(text)
    except (TypeError, ValueError): return 2


def current_nparts(qtwrap, nparts_box="nparts"):
    return _parse_nparts(qtwrap.getbox(nparts_box))


def region_of_factory(coord_min, coord_max, nparts):
    """Return a function mapping one coordinate value to a 0-indexed part
    (0..nparts-1), by splitting [coord_min,coord_max] into nparts equal
    bins - generalizing the old hardcoded "r[axis]<0.0" two-way split
    (equivalent to it when nparts==2 and the geometry is centered, as
    get_geometry() already leaves it)."""
    span = coord_max - coord_min
    def region_of(coord):
        if nparts <= 1 or span <= 0: return 0
        idx = int((coord - coord_min) / span * nparts)
        return min(max(idx, 0), nparts - 1)
    return region_of


def part_interpolator(get, name, nparts, axis, region_of):
    """Build a fun(r1,r2=None) returning parameter `name`'s value for
    whichever part the (bond-averaged) position falls into - the N-part
    generalization of the old get_interpolator(p1,p2)."""
    vals = [get(name + part_suffix(i)) for i in range(1, nparts + 1)]
    def fun(r1, r2=None):
        r = (r1 + r2) / 2. if r2 is not None else r1
        return vals[region_of(r[axis])]
    return fun


def part_vector_interpolator(get, names, nparts, axis, region_of):
    """Same as part_interpolator, but for a vector parameter (e.g. the
    Zeeman field Bx/By/Bz) made of several same-part-suffixed fields."""
    vals = [np.array([get(n + part_suffix(i)) for n in names]) for i in range(1, nparts + 1)]
    def fun(r1, r2=None):
        r = (r1 + r2) / 2. if r2 is not None else r1
        return vals[region_of(r[axis])]
    return fun


def part_check(get, name, nparts):
    """True if any part has a nonzero value for parameter `name`."""
    return any(abs(get(name + part_suffix(i))) > 0.0 for i in range(1, nparts + 1))


def _build_tab(params, i):
    """A plain grid of (BodyLabel,LineEdit) rows for part i, one row per
    entry in params=[(field_name,display_label),...] - the same rows
    Designer laid out for parts 1/2, reproduced for part i>=3."""
    tab = QWidget()
    layout = QGridLayout(tab)
    suffix = part_suffix(i)
    for row, (name, label_text) in enumerate(params):
        layout.addWidget(BodyLabel(label_text, tab), row, 0)
        field = LineEdit(tab)
        field.setText("0.0")
        field.setObjectName(name + suffix)
        layout.addWidget(field, row, 1)
    return tab


def connect(qtwrap, params, tabs_widget="tabWidget_4", nparts_box="nparts", max_parts=MAX_PARTS, on_new_part=None):
    """Wire the "nparts" combobox (items "2".."max_parts", already built
    by interface.ui) so changing it keeps exactly that many part-tabs in
    tabs_widget - a QTabWidget whose first two tabs (part 1/2) already
    exist, built by Designer. Tabs for part 3+ are built here on first
    use and kept alive afterwards (removeTab() doesn't delete the child),
    so toggling nparts back and forth doesn't lose values already typed
    in. Every field is set as a plain attribute of the page (`form`) -
    qtwrap.get()/getbox() resolve widgets with getattr(form,name)
    regardless of whether they came from Designer or here.

    on_new_part, if given, is called (no args) right after a new tab's
    fields are added to `form` - e.g. so a mode can re-run
    latticeterms.apply_term_restrictions() and hide the new tab's
    haldane/kanemele fields too if the current lattice isn't honeycomb
    (latticeterms only reacts to the "lattice" combobox changing, so
    without this a newly-built part's restricted fields would default to
    visible until the user touches "lattice" again)."""
    form = qtwrap.form
    tabs = getattr(form, tabs_widget)
    base_name = params[0][0]
    # Designer's two tabs ("Upper"/"Lower") aren't in the same order in
    # every mode's .ui - detect which index actually holds the unsuffixed
    # (part 1) fields so labeling below is correct either way.
    if tabs.widget(0).findChild(LineEdit, base_name) is not None:
        part1_idx, part2_idx = 0, 1
    else:
        part1_idx, part2_idx = 1, 0
    tabs.setTabText(part1_idx, "Part 1")
    tabs.setTabText(part2_idx, "Part 2")

    extra_tabs = {} # part index (>=3) -> QWidget, built lazily and kept

    def ensure_built(i):
        if i not in extra_tabs:
            tab = _build_tab(params, i)
            for name, _ in params:
                field = tab.findChild(LineEdit, name + part_suffix(i))
                setattr(form, name + part_suffix(i), field)
                # Designer-built part 1/2 fields get this wired once, for
                # every QLineEdit on the page, by _AppBase's own
                # _connect_dirty_tracking() at page-construction time -
                # these part 3+ fields are built later, here, so without
                # this line an edit to one would never mark results stale
                # (params_dirty_time() would stay at its pre-edit value).
                field.textEdited.connect(form._mark_dirty)
            extra_tabs[i] = tab
            if on_new_part is not None: on_new_part()
        return extra_tabs[i]

    def apply_count(n):
        n = min(max(n, 2), max_parts)
        current = tabs.count()
        if current > n:
            for idx in range(current - 1, n - 1, -1): tabs.removeTab(idx)
        elif current < n:
            for i in range(current + 1, n + 1): tabs.addTab(ensure_built(i), "Part %d" % i)

    combo = getattr(form, nparts_box)
    # Read the new value directly off the signal (the text the combobox
    # just changed to), not via current_nparts(qtwrap,nparts_box) -
    # qtwrap.getbox() resolves through the shell's single global "active
    # page" pointer, which is only guaranteed to be *this* page while the
    # combobox change is a live user click (the only page whose widgets
    # can receive one). A programmatic change - e.g. load_interface()
    # restoring a saved session onto a page that isn't currently shown -
    # would otherwise read the wrong (currently active) page's nparts
    # value while still mutating this page's own `tabs`/`extra_tabs`.
    combo.currentTextChanged.connect(lambda text: apply_count(_parse_nparts(text)))
    apply_count(current_nparts(qtwrap, nparts_box))
