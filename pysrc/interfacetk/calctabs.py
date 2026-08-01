"""Category filter for a mode's wide "calculation tabs" QTabWidget
(Structure/Bands/DOS/LDOS/.../Site DOS - 6 to 14 tabs side by side in the
richer modes, all siblings of one QTabWidget, usually named tabWidget_3 -
see INTERFACE_GUIDE.md's "The QTabWidget naming trap"). All tabs stay at
the same level (one click away, nothing nested inside another QTabWidget)
- a ComboBox dropped in the tab widget's top-right corner lets the user
pick a category and hide every tab that doesn't match it, via
QTabBar.setTabVisible() (Qt 6). Picking "All" (the default) shows every
tab again.

Call add_selector(qtwrap) once per mode, from common.finalize_page() (so
every mode picks this up for free - see that function) after
scfterms.build() has already run for SCF-capable modes (scfterms.build()
is called near the top of each such <mode>.py, well before finalize_page()
at the bottom) - by the time add_selector() runs, scfterms.build()'s own
_nest_scf_tab() has already moved the "SCF" tab out of tabWidget_3 and
into "Terms in the Hamiltonian" as "Many-body interactions", so
add_selector() never needs to know about SCF-capable modes specially: it
only ever sees whatever tabs are still directly on tabWidget_3 at that
point.

CATEGORIES is one shared, ordered title->category table covering every
tab title seen across every mode (verified via the setTabText grep in
INTERFACE_GUIDE.md's "The QTabWidget naming trap", one mode at a time). A
mode with fewer than min_tabs tabs total is left untouched (not worth
adding a filter for three tabs) - this is what makes
impurity_embedding/ribbon_embedding (3 tabs each) and tbg's real
tabWidget_3 (1 tab, "Hamiltonian" - unrelated to this at all) no-ops.
Any tab whose title isn't in CATEGORIES (a mode-specific "signature" tab
like hofstader1d's "Hofstader spectra", or a deliberately-uncategorized
one like "SCF"/"Sweep"/"Site DOS" - see the comment below) is a tool/setup
step rather than a result, so it stays visible no matter which category is
picked, instead of being hideable at all."""
from PySide6.QtCore import Qt
from qfluentwidgets import ComboBox

CATEGORIES = [
    ("Spectral", [
        "Structure", "Bands", "DOS Bands", "DOS", "LDOS", "Eigenvalues",
        "Band LDOS", "E-y map", "Total DOS", "Local DOS", "DOS map",
        "DOS in a line", "Pristine structure", "Single LDOS",
    ]),
    ("Scattering & Fermi surface", ["FS", "QPI"]),
    ("Topology & edges", ["Topology", "Topology 2D", "SDOS", "Edeg DOS"]),
    ("Real space & dynamics", [
        "Magnetism", "Time evolution", "IETS LDOS", "IETS QDOS",
    ]),
]
# Deliberately not categorized, so they're always visible regardless of the
# selected filter: "SCF" (an input/setup step, not a result, and already
# promoted to its own "Many-body interactions" sub-tab for SCF-capable
# modes before add_selector() even runs - see this module's docstring),
# "Sweep" (a distinct workflow, not a single result), "Site DOS"/
# "Select ... " picker tabs (interactive tools, not passive results), and
# any mode-specific signature calculation (e.g. hofstader1d's "Hofstader
# spectra") that doesn't share a category with anything else.


def _category_for(title):
    for label, titles in CATEGORIES:
        if title in titles: return label
    return None


def add_selector(qtwrap, tab_widget_attr="tabWidget_3", min_tabs=6):
    """Drop a category-filter ComboBox into `tab_widget_attr`'s (default
    "tabWidget_3", the wide calculation-tabs widget in every mode except
    tbg - see this module's docstring) top-right corner, in place. Safe to
    call on a mode that doesn't have this attribute, whose tab count is
    below `min_tabs`, or none of whose tabs match any known category: all
    are silent no-ops, so this can be called unconditionally from
    finalize_page() for every mode rather than needing a per-mode opt-in."""
    form = qtwrap.form
    wide = getattr(form, tab_widget_attr, None)
    if wide is None: return
    n = wide.count()
    if n < min_tabs: return

    titles = [wide.tabText(i) for i in range(n)]
    present = [label for label, cat_titles in CATEGORIES
               if any(t in cat_titles for t in titles)]
    if not present: return

    combo = ComboBox(wide)
    combo.setObjectName(tab_widget_attr+"_category_filter")
    combo.addItem("All")
    for label in present: combo.addItem(label)

    def _apply(index):
        chosen = combo.itemText(index)
        bar = wide.tabBar()
        for i in range(wide.count()):
            cat = _category_for(wide.tabText(i))
            bar.setTabVisible(i, chosen == "All" or cat is None or cat == chosen)

    combo.currentIndexChanged.connect(_apply)
    wide.setCornerWidget(combo, Qt.TopRightCorner)
