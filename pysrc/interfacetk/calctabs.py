"""Runtime regrouping of a mode's wide "calculation tabs" QTabWidget
(Structure/Bands/DOS/LDOS/.../Site DOS - 6 to 14 tabs side by side in the
richer modes, all siblings of one QTabWidget, usually named tabWidget_3 -
see INTERFACE_GUIDE.md's "The QTabWidget naming trap") into a handful of
named categories, each its own inner QTabWidget tab. Generalizes
scfterms.py's _nest_scf_tab() mechanics (grab a tab page by its title,
removeTab, addTab it onto a new inner QTabWidget) from two groups to N,
reducing tab-bar width without hiding or removing anything - every
existing tab is still one or two clicks away, just under a labeled
category instead of scattered in one flat row.

Call nest(qtwrap) once per mode, from common.finalize_page() (so every
mode picks this up for free - see that function) after scfterms.build()
has already run for SCF-capable modes (scfterms.build() is called near
the top of each such <mode>.py, well before finalize_page() at the
bottom) - by the time nest() runs, scfterms.build()'s own _nest_scf_tab()
has already moved the "SCF" tab out of tabWidget_3 and into "Terms in the
Hamiltonian" as "Many-body interactions", so nest() never needs to know
about SCF-capable modes specially: it only ever sees whatever tabs are
still directly on tabWidget_3 at that point.

CATEGORIES is one shared, ordered title->category table covering every
tab title seen across every mode (verified via the setTabText grep in
INTERFACE_GUIDE.md's "The QTabWidget naming trap", one mode at a time).
A mode with fewer than min_tabs tabs total is left untouched (not worth
nesting three tabs into a category of one) - this is what makes
impurity_embedding/ribbon_embedding (3 tabs each) and tbg's real
tabWidget_3 (1 tab, "Hamiltonian" - unrelated to this at all) no-ops.
Any tab whose title isn't in CATEGORIES (a mode-specific "signature" tab
like hofstader1d's "Hofstader spectra", or a deliberately-uncategorized
one like "SCF"/"Sweep"/"Site DOS" - see the comment below) is kept as its
own top-level tab, appended after the grouped ones, so a title this table
doesn't yet know about is never silently buried - just left ungrouped
until CATEGORIES is updated to include it."""
from PySide6.QtWidgets import QTabWidget

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
# Deliberately not categorized, so they always fall through to the
# "leftover" top-level tabs below instead of being buried a click deeper:
# "SCF" (an input/setup step, not a result, and already promoted to its
# own "Many-body interactions" sub-tab for SCF-capable modes before nest()
# even runs - see this module's docstring), "Sweep" (a distinct workflow,
# not a single result), "Site DOS"/"Select ... " picker tabs (interactive
# tools, not passive results), and any mode-specific signature calculation
# (e.g. hofstader1d's "Hofstader spectra") that doesn't share a category
# with anything else.


def _category_for(title):
    for label, titles in CATEGORIES:
        if title in titles: return label
    return None


def nest(qtwrap, tab_widget_attr="tabWidget_3", min_tabs=6):
    """Regroup `tab_widget_attr` (default "tabWidget_3", the wide
    calculation-tabs widget in every mode except tbg - see this module's
    docstring) in place. Safe to call on a mode that doesn't have this
    attribute, or whose tab count is below `min_tabs`: both are silent
    no-ops, so this can be called unconditionally from finalize_page()
    for every mode rather than needing a per-mode opt-in.

    A category with only one matching tab is deliberately left as a
    top-level tab (under its own original title) rather than wrapped in a
    single-tab inner QTabWidget - that would cost an extra click for zero
    grouping benefit. Only categories with 2+ matching tabs actually get
    nested; if none do, this is a no-op (nothing to gain by reshuffling
    tab order with no reduction in tab-bar width)."""
    form = qtwrap.form
    wide = getattr(form, tab_widget_attr, None)
    if wide is None: return
    n = wide.count()
    if n < min_tabs: return

    pages = [(wide.tabText(i), wide.widget(i)) for i in range(n)]
    grouped = {} # category label -> [(title, widget), ...], first-seen order
    for title, widget in pages:
        label = _category_for(title)
        if label is not None:
            grouped.setdefault(label, []).append((title, widget))

    multi = {label: items for label, items in grouped.items() if len(items) >= 2}
    if not multi: return
    nested_titles = {title for items in multi.values() for title, _widget in items}

    while wide.count(): wide.removeTab(0) # widgets themselves survive - removeTab() only unparents, doesn't delete

    for label, _titles in CATEGORIES:
        items = multi.get(label)
        if not items: continue
        inner = QTabWidget()
        for title, widget in items:
            inner.addTab(widget, title)
        wide.addTab(inner, label)

    for title, widget in pages:
        if title not in nested_titles:
            wide.addTab(widget, title)
