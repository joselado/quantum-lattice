"""Runtime builder for the mean-field terms' "Density-density"
(U/V1/V2)/"Spin-spin" (J1/J2/J3) sub-tabs, shared by every mode that has
them (2d, 0d, 1d, 3d, 2dslab, multilayergraphene, hybridfilm, hybridribbon)
instead of duplicating the same QTabWidget block in each mode's interface.ui.

A mode wires this up with one call, after new_page() builds the page and
before common.set_formulas(qtwrap) (which needs the "<term>_image"
labels built below to already exist - unlike single-particle terms, whose
missing image widget set_formulas() creates itself, see
common.py:_ensure_formula_image(); mean-field terms don't get that
treatment since scfterms.build() already places one, images=True by
default) / window.connect_clicks():

    from interfacetk import scfterms
    scfterms.build(qtwrap)  # images=False only if a mode wants the plain
                             # (image-less) mean-field fields, e.g. for a
                             # narrower layout

build() replaces interface.ui's "scf_terms_container" placeholder (a bare
QWidget Designer already places at the mean-field terms' row) with the
QTabWidget. Every label/field/image widget is set as a plain attribute of
the page (`form`) - qtwrap.get()/getbox()/set_logo() resolve widgets with
getattr(form,name) (or QObject.findChild by name, for images) regardless
of whether they came from Designer or here - and each field's textEdited
is wired to form._mark_dirty, since _AppBase._connect_dirty_tracking()
only walks the widgets that exist at page-construction time, before this
runs (same reasoning as hybridparts.py's part 3+ fields).

build() also nests interface.ui's top-level "SCF" tab inside "Terms in
the Hamiltonian" as a "Many-body interactions" sub-tab, alongside the
pre-existing fields renamed "Single particle" - see _nest_scf_tab().

build() also replaces interface.ui's Designer-authored "do_scf" CheckBox
(buried inside Many-body interactions -> Basic) with a SwitchButton
pinned to the bottom of the whole "Terms in the Hamiltonian" panel -
visible regardless of which sub-tab is open - see _build_scf_switch_row().
It keeps the "do_scf" name, so every existing qtwrap.is_checked("do_scf")
call keeps resolving correctly with no other file needing a change. The
switch starts off; it's turned on automatically the moment one of the six
interaction fields (U/V1/V2/J1/J2/J3) leaves zero (see
_wire_interaction_field()), but never turned off automatically - a
manual "off" is expected to stick even if those fields stay non-zero.

Finally, build() wires _scf_dirty tracking (_connect_scf_dirty_tracking()):
any field that affects Hamiltonian construction - i.e. everything on the
page except the do_scf switch itself and calculation/plotting-only
settings (all of which live as sibling tabs of tabWidget_3, alongside the
"SCF" tab this module already moves out of it) - marks form._scf_dirty
True. common.pickup_hamiltonian() checks this flag (and whether
hamiltonian.pkl exists yet) to decide whether it must (re)run solve_scf()
before handing back the cached mean-field Hamiltonian, so a stale SCF
solution is never silently reused after a Hamiltonian parameter changes."""
import inspect
from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget, QGridLayout, QTabWidget, QHBoxLayout, QVBoxLayout
from qfluentwidgets import BodyLabel, LineEdit, SwitchButton
from .termtooltips import TERM_TOOLTIPS  # single source of truth for term
                                    # tooltips, shared with common.py's
                                    # set_formulas() - needed here too since
                                    # these mean-field fields are built (and
                                    # tooltipped, via DENSITY_DENSITY/SPIN_SPIN
                                    # below) before set_formulas() runs

DENSITY_DENSITY = [
    ("U", "U", TERM_TOOLTIPS["U"], "0.0"),
    ("V1", "V1", TERM_TOOLTIPS["V1"], "0.0"),
    ("V2", "V2", TERM_TOOLTIPS["V2"], "0.0"),
]
SPIN_SPIN = [
    ("J1", "J1", TERM_TOOLTIPS["J1"], "0.0"),
    ("J2", "J2", TERM_TOOLTIPS["J2"], "0.0"),
    ("J3", "J3", TERM_TOOLTIPS["J3"], "0.0"),
]


def _is_nonzero(text):
    try: return float(text) != 0.0
    except ValueError: return False


def _wire_interaction_field(form, field):
    """Mark the SCF result stale on every edit, and turn the do_scf switch
    on the moment this field leaves zero - but never turn it back off,
    so a manual "off" sticks even if the field stays non-zero afterwards
    (see this module's docstring)."""
    field._scf_was_nonzero = _is_nonzero(field.text())
    def on_edit(text, field=field):
        form._mark_scf_dirty()
        now_nonzero = _is_nonzero(text)
        if now_nonzero and not field._scf_was_nonzero:
            form.do_scf.setChecked(True)
        field._scf_was_nonzero = now_nonzero
    field.textEdited.connect(on_edit)


def _build_grid(form, parent, terms, images):
    layout = QGridLayout(parent)
    for row, (name, text, tooltip, default) in enumerate(terms):
        label = BodyLabel(text, parent)
        label.setObjectName(f"label_{name}")
        layout.addWidget(label, row, 0)
        setattr(form, f"label_{name}", label)

        field = LineEdit(parent)
        field.setObjectName(name)
        field.setToolTip(tooltip)
        field.setText(default)
        # kept narrow so the formula column (below) gets the space to
        # render its LaTeX image bigger, instead of the two splitting the
        # row's width evenly
        field.setMaximumWidth(60)
        layout.addWidget(field, row, 1)
        setattr(form, name, field)
        field.textEdited.connect(form._mark_dirty)
        _wire_interaction_field(form, field)

        if images:
            image = BodyLabel("", parent)
            image.setObjectName(f"{name}_image")
            layout.addWidget(image, row, 2)
            setattr(form, f"{name}_image", image)

    if images:
        layout.setColumnStretch(1, 0)
        layout.setColumnStretch(2, 1)


def build(qtwrap, container="scf_terms_container", grid="gridLayout_10", images=True):
    """Replace `container` with a QTabWidget with "Density-density"
    (U/V1/V2) and "Spin-spin" (J1/J2/J3) tabs, in the same grid cell.

    `grid` is the containing QGridLayout's own object name, not derived
    from placeholder.parentWidget().layout() - `grid` is a *nested*
    sub-layout (added to its parent layout via addLayout(), the way
    Designer nests one QGridLayout inside another for each "Basic" tab),
    not the layout actually set on any widget via setLayout(), so
    parentWidget().layout() returns the wrong (outer) layout entirely,
    silently making every indexOf()/getItemPosition() below operate on
    the wrong object - this was the actual cause of a prior bug where the
    tab widget ended up somewhere row/col (-1,-1) of the wrong layout,
    collapsing every row to zero height."""
    form = qtwrap.form
    _init_scf_state(form)
    placeholder = getattr(form, container)
    parent_widget = placeholder.parentWidget()
    layout = getattr(form, grid)
    idx = layout.indexOf(placeholder)
    row, col, rowspan, colspan = layout.getItemPosition(idx)
    layout.removeWidget(placeholder)
    placeholder.setParent(None)
    placeholder.deleteLater()

    tabs = QTabWidget(parent_widget)
    dd_tab, ss_tab = QWidget(tabs), QWidget(tabs)
    _build_grid(form, dd_tab, DENSITY_DENSITY, images)
    _build_grid(form, ss_tab, SPIN_SPIN, images)
    tabs.addTab(dd_tab, "Density-density")
    tabs.addTab(ss_tab, "Spin-spin")
    tabs.setObjectName(container)

    layout.addWidget(tabs, row, col, rowspan, colspan)
    setattr(form, container, tabs)
    _nest_scf_tab(qtwrap)
    _connect_scf_dirty_tracking(form)
    return tabs


def _init_scf_state(form):
    """form._scf_dirty starts True (nothing has been solved yet this
    session - see common.pickup_hamiltonian()); form._mark_scf_dirty is
    the callback every Hamiltonian-affecting widget gets wired to."""
    form._scf_dirty = True
    form._mark_scf_dirty = lambda *a: setattr(form, "_scf_dirty", True)


def _retire_old_checkbox(form):
    """Remove interface.ui's Designer-authored "do_scf" CheckBox - it's
    being replaced by the SwitchButton built in _build_scf_switch_row(),
    which reuses the same "do_scf" attribute name."""
    old = getattr(form, "do_scf", None)
    if old is None: return
    layout = old.parentWidget().layout()
    if layout is not None: layout.removeWidget(old)
    old.setParent(None)
    old.deleteLater()


def _build_scf_switch_row(form):
    """Build the SwitchButton pinned to the bottom of the whole "Terms in
    the Hamiltonian" panel (see _nest_scf_tab()), replacing the old
    "do_scf" CheckBox that used to live three levels deep inside Many-body
    interactions -> Basic."""
    _retire_old_checkbox(form)
    switch = SwitchButton(form)
    switch.setOnText("SCF: on")
    switch.setOffText("SCF: off")
    switch.setChecked(False)
    switch.setObjectName("do_scf")
    setattr(form, "do_scf", switch)

    row = QWidget(form)
    row_layout = QHBoxLayout(row)
    row_layout.setContentsMargins(0, 4, 0, 0)
    row_layout.addWidget(BodyLabel("Include mean field (SCF)", row))
    row_layout.addStretch(1)
    row_layout.addWidget(switch)
    return row


def _connect_scf_dirty_tracking(form):
    """Wire every widget that affects Hamiltonian construction to
    form._mark_scf_dirty - everything on the page except the do_scf
    switch itself (toggling SCF on/off doesn't, by itself, invalidate a
    Hamiltonian already solved for the current parameters) and anything
    inside tabWidget_3 (calculation/plotting-only settings: Bands, DOS,
    Berry, Chern, QPI, LDOS, ... - the "SCF" tab _nest_scf_tab() already
    moved out of it, so by this point tabWidget_3 holds only those).
    Mirrors _AppBase._connect_dirty_tracking()'s isinstance-based walk,
    but scoped narrower so tweaking a plot setting doesn't force an
    expensive SCF re-solve on the next click."""
    exclude = getattr(form, "tabWidget_3", None)
    switch = getattr(form, "do_scf", None)
    def excluded(widget):
        if widget is switch: return True
        w = widget
        while w is not None:
            if w is exclude: return True
            w = w.parentWidget()
        return False
    for name, obj in inspect.getmembers(form):
        if not isinstance(obj, QtWidgets.QWidget) or excluded(obj): continue
        if isinstance(obj, QtWidgets.QLineEdit):
            obj.textEdited.connect(form._mark_scf_dirty)
        elif isinstance(obj, QtWidgets.QComboBox):
            obj.activated.connect(form._mark_scf_dirty)
        elif isinstance(obj, (QtWidgets.QCheckBox, QtWidgets.QRadioButton)):
            obj.clicked.connect(form._mark_scf_dirty)


def _nest_scf_tab(qtwrap):
    """Move the "SCF" tab inside "Terms in the Hamiltonian", as a sibling
    sub-tab of the pre-existing single-particle fields, instead of two
    separate tabs - renaming both in the process ("Terms in the
    Hamiltonian"'s own fields -> "Single particle", "SCF" -> "Many-body
    interactions"). In every mode's interface.ui, "Terms in the
    Hamiltonian" is a tab of its own QTabWidget ("tabWidget_2" - in some
    modes, e.g. 0d, a sibling "Additional terms" tab lives there too),
    while "SCF" is one of several sibling tabs (Bands/DOS/...) of a
    different QTabWidget ("tabWidget_3") - they are not tabs of the same
    QTabWidget, despite both nesting under the shell's top-level
    "tabWidget". This reuses the two existing tab-page widgets whole (each
    already has its own self-contained layout/content from interface.ui),
    so it only ever reparents whole widgets via QTabWidget.addTab(), never
    touches their internal layouts."""
    form = qtwrap.form
    ham_tabs = form.tabWidget_2
    scf_tabs = form.tabWidget_3

    ham_idx = next((i for i in range(ham_tabs.count())
                     if ham_tabs.tabText(i) == "Terms in the Hamiltonian"), None)
    scf_idx = next((i for i in range(scf_tabs.count())
                     if scf_tabs.tabText(i) == "SCF"), None)
    if ham_idx is None or scf_idx is None:
        raise RuntimeError(
            "scfterms._nest_scf_tab: expected a 'Terms in the Hamiltonian' "
            "tab in tabWidget_2 and a 'SCF' tab in tabWidget_3 - one of "
            "these tab titles/parents has changed, update this function "
            "(and INTERFACE_GUIDE.md) to match.")

    ham_widget = ham_tabs.widget(ham_idx)
    scf_widget = scf_tabs.widget(scf_idx)

    scf_tabs.removeTab(scf_idx)
    ham_tabs.removeTab(ham_idx)

    inner = QTabWidget()
    inner.addTab(ham_widget, "Single particle")
    inner.addTab(scf_widget, "Many-body interactions")

    # Wrap `inner` so the SCF switch sits below both sub-tabs, visible
    # regardless of which one is open, instead of being buried inside
    # Many-body interactions -> Basic like the CheckBox it replaces.
    wrapper = QWidget()
    outer_layout = QVBoxLayout(wrapper)
    outer_layout.setContentsMargins(0, 0, 0, 0)
    outer_layout.addWidget(inner, 1)
    outer_layout.addWidget(_build_scf_switch_row(form))

    ham_tabs.insertTab(ham_idx, wrapper, "Terms in the Hamiltonian")
    # removeTab() above can leave a sibling tab (e.g. 0d's "Additional
    # terms") focused instead of the one we just reinserted - insertTab()
    # does not auto-select unless the tab widget was empty, so restore it
    # explicitly rather than silently opening on the wrong tab.
    ham_tabs.setCurrentIndex(ham_idx)
