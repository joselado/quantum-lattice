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

connect() only manages widgets (building/showing/hiding part-3+ tabs, and
- see _add_formula_column() below - giving every part's field its own
formula image/tooltip from the shared TERM_TOOLTIPS/interface-pyqt/logos
convention, the per-part equivalent of common.py:set_formulas()); the
region_of_factory/part_interpolator/part_check/part_vector_interpolator
helpers below only deal in plain values, so a mode's initialize() stays
free to define its own axis (2/z for hybridfilm, 1/y for hybridribbon)
and its own set of Hamiltonian terms.
"""
import numpy as np
from PySide6.QtWidgets import QWidget, QGridLayout
from qfluentwidgets import BodyLabel, LineEdit
from .termtooltips import TERM_TOOLTIPS

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
    (0..nparts-1), by splitting equal-width bins centered on the
    geometry's own center (coord 0 - get_geometry() already recenters the
    geometry there via geometry.center()), not on the raw
    [coord_min,coord_max] midpoint - generalizing the old hardcoded
    "r[axis]<0.0" two-way split so nparts==2 reproduces it exactly.
    geometry.center() centers on the mean atom position, which isn't the
    same as (coord_min+coord_max)/2 for a lattice whose basis isn't
    symmetric about its own center (e.g. Kagome - the old midpoint-based
    version silently moved the part boundary and reassigned boundary
    atoms/bonds to the wrong part for such lattices)."""
    half_width = max(abs(coord_min), abs(coord_max))
    span = 2*half_width
    def region_of(coord):
        if nparts <= 1 or span <= 0: return 0
        idx = int((coord + half_width) / span * nparts)
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


def _add_formula_column(qtwrap, tab, name, suffix):
    """Add a "<name><suffix>_image" formula label between the label
    (col0) and field (col1) of the row that already holds the
    "<name><suffix>" field - shifting the field to col2 to make room -
    and set its rendered-LaTeX pixmap + physics tooltip from the shared
    TERM_TOOLTIPS/logos. The runtime equivalent of the "<term>_image"
    widgets Designer places for other modes' terms, needed here since
    these per-part rows are discovered at runtime rather than laid out in
    interface.ui; positioned to match where Designer places it for those
    other modes (label, image, field, left to right), the same reasoning
    as common.py:_ensure_formula_image() - both share qtwrap.find_layout_of()
    to locate the field's actual (possibly nested) QGridLayout. Silently
    does nothing if `name` has no field in this tab (params lists differ
    slightly per mode) or no entry in TERM_TOOLTIPS."""
    field = tab.findChild(LineEdit, name + suffix)
    if field is None: return
    grid = qtwrap.find_layout_of(field)
    if grid is None: return
    idx = grid.indexOf(field)
    row, col, rowspan, colspan = grid.getItemPosition(idx)
    grid.removeWidget(field)
    grid.addWidget(field, row, col + 1, rowspan, colspan)
    image = BodyLabel("", tab)
    image.setObjectName(name + suffix + "_image")
    grid.addWidget(image, row, col)
    setattr(qtwrap.form, name + suffix + "_image", image)
    qtwrap.set_logo(name + suffix + "_image", name + ".png", width=400, height=30)
    tip = TERM_TOOLTIPS.get(name)
    if tip is not None:
        qtwrap.set_tooltip(name + suffix, tip)
        qtwrap.set_tooltip(name + suffix + "_image", tip)
    # inherit the field's current shown/hidden state - see the matching
    # comment in common.py:_ensure_formula_image(). latticeterms.connect()
    # always runs before this (part 1/2: before hybridparts.connect();
    # part 3+: on_new_part() re-applies restrictions right before this
    # runs, via ensure_built()), so field.isHidden() already reflects
    # whether this term is allowed on the current lattice.
    image.setVisible(not field.isHidden())


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

    on_new_part, if given, is called with this page's own `form` (not
    read back via qtwrap.form/getbox() - see the "nparts" combobox
    comment below for why: apply_count()/ensure_built() can run from a
    marshaled call already on the GUI thread, where qtwrap.form is the
    shell's currently-*visible* page, not necessarily the page this
    callback belongs to) right after a new tab's fields are added to
    `form` - e.g. so a mode can re-run
    latticeterms.apply_term_restrictions(form,...) and hide the new
    tab's haldane/kanemele fields too if the current lattice isn't
    honeycomb (latticeterms only reacts to the "lattice" combobox
    changing, so without this a newly-built part's restricted fields
    would default to visible until the user touches "lattice" again)."""
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

    # Designer-built part 1/2 tabs are already attached to the page here
    # (interface.ui built them as part of tabWidget_4), so their formula
    # columns can be added immediately - unlike part 3+ below, which have
    # to wait until they're actually addTab()'d into the page's widget
    # tree, since qtwrap.set_logo()/set_tooltip() resolve widgets via
    # page.findChild() and a not-yet-attached QWidget isn't found by that.
    for name, _ in params:
        _add_formula_column(qtwrap, tabs.widget(part1_idx), name, "")
        _add_formula_column(qtwrap, tabs.widget(part2_idx), name, "_2")

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
            if on_new_part is not None: on_new_part(form)
        return extra_tabs[i]

    def apply_count(n):
        n = min(max(n, 2), max_parts)
        current = tabs.count()
        if current > n:
            for idx in range(current - 1, n - 1, -1): tabs.removeTab(idx)
        elif current < n:
            for i in range(current + 1, n + 1):
                newly_built = i not in extra_tabs
                tab = ensure_built(i)
                tabs.addTab(tab, "Part %d" % i)
                if newly_built: # only once - see the part 1/2 comment above
                                 # for why this has to happen after addTab()
                    for name, _ in params:
                        _add_formula_column(qtwrap, tab, name, part_suffix(i))

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
