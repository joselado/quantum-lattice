"""Runtime builder for the mean-field terms' "Density-density"
(U/V1/V2)/"Spin-spin" (J1/J2/J3) sub-tabs, shared by every mode that has
them (2d, 0d, 1d, 3d, 2dslab, multilayergraphene) instead of duplicating
the same QTabWidget block in each mode's interface.ui.

A mode wires this up with one call, after new_page() builds the page and
before common.set_formulas(qtwrap) (which needs the "<term>_image"
labels built below to already exist) / window.connect_clicks():

    from interfacetk import scfterms
    scfterms.build(qtwrap)  # images=False for 3d/2dslab/multilayergraphene,
                             # which don't use the formula-image convention
                             # for any of their other terms either

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
pre-existing fields renamed "Single particle" - see _nest_scf_tab()."""
from PySide6.QtWidgets import QWidget, QGridLayout, QTabWidget
from qfluentwidgets import BodyLabel, LineEdit
from .termtooltips import TERM_TOOLTIPS  # single source of truth for term
                                    # tooltips, shared with common.py's
                                    # set_formulas() - needed here too since
                                    # 3d/2dslab/multilayergraphene build these
                                    # fields but never call set_formulas()

DENSITY_DENSITY = [
    ("U", "U", TERM_TOOLTIPS["U"], "2.0"),
    ("V1", "V1", TERM_TOOLTIPS["V1"], "0.0"),
    ("V2", "V2", TERM_TOOLTIPS["V2"], "0.0"),
]
SPIN_SPIN = [
    ("J1", "J1", TERM_TOOLTIPS["J1"], "0.0"),
    ("J2", "J2", TERM_TOOLTIPS["J2"], "0.0"),
    ("J3", "J3", TERM_TOOLTIPS["J3"], "0.0"),
]


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
        layout.addWidget(field, row, 1)
        setattr(form, name, field)
        field.textEdited.connect(form._mark_dirty)

        if images:
            image = BodyLabel("", parent)
            image.setObjectName(f"{name}_image")
            layout.addWidget(image, row, 2)
            setattr(form, f"{name}_image", image)


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
    return tabs


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
    ham_tabs.insertTab(ham_idx, inner, "Terms in the Hamiltonian")
