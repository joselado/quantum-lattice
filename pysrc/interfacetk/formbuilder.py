"""Build a mode's page from a declarative Python spec, instead of from
Qt Designer XML.

Background: the normal path for a mode's page is `interface.ui` (Designer
XML) compiled to `interface.py` by `pyside6-uic`. That path has two
problems - the XML is ~10x the size of the information it carries and is
not readable by a human or an agent, and the generated `interface.py` is
another several hundred lines of the same content again. A mode's page is
in fact very regular: two tab widgets side by side, each tab a column of
(label, field) rows followed by one or more calculation buttons.

This module expresses exactly that, so a mode can define its whole page as
a short list of `field(...)` / `combo(...)` / `button(...)` calls (see
`interface-pyqt/tmdc/interface.py` for the worked example). It builds the
same widget classes the promoted-Designer path builds (qfluentwidgets'
`LineEdit`/`ComboBox`/`PushButton`/`BodyLabel`), sets the same object
names, and exposes the result through a `Ui_MainWindow`-shaped class, so
`qtwrap.new_page()`'s `_load_ui_module` + dynamic class composition works
against it unchanged and no other code has to know the difference.

Two structural rules it deliberately preserves, because shared toolkit code
depends on them:

  * consecutive parameter rows go into their own nested `QGridLayout`, with
    the label in column 0 and the field in column 1. `common.py`'s
    `_ensure_formula_image()` walks the field's *containing* grid to add a
    formula column to its right, and `latticeterms.py`'s
    `_row_label_siblings()` finds a term's label by grid row rather than by
    object name - both need a grid, laid out this way.
  * parameters come before buttons in a tab. `common.py`'s
    `_move_params_above_buttons()` enforces this at runtime anyway (the
    Designer files were never consistent about it), so specs are simply
    written in the order that already wins.

Object names are the contract with the rest of the app: field/button names
are what `qtwrap.get()`/`getbox()`/`connect_clicks()` look up, so they must
match what `<mode>.py` asks for. Label names are *not* - nothing looks a
label up by name (`latticeterms` finds them positionally, `scfterms` names
its own), so this module generates them as `label_<field>` for readability.
"""
from PySide6 import QtWidgets

from qfluentwidgets import BodyLabel, CheckBox, ComboBox, LineEdit, PushButton


# --------------------------------------------------------------- spec pieces
# Each returns a plain dict - a spec is data, inspectable and diffable, not
# a tree of half-built widgets.

def field(name, label, default=""):
    """A labelled text-entry parameter (the LineEdit every get() reads)."""
    return {"kind": "field", "name": name, "label": label, "default": str(default)}


def combo(name, label, items=()):
    """A labelled dropdown. Most modes fill the items at runtime instead
    (qtwrap.set_combobox), so `items` is usually left empty here."""
    return {"kind": "combo", "name": name, "label": label, "items": list(items)}


def check(name, label, checked=False):
    """A checkbox parameter (is_checked() reads these)."""
    return {"kind": "check", "name": name, "label": label, "checked": checked}


def note(text, name=None):
    """A full-width explanatory line of text."""
    return {"kind": "note", "name": name, "text": text}


def button(name, text):
    """A full-width calculation button."""
    return {"kind": "buttons", "buttons": [(name, text)]}


def button_row(*pairs):
    """Several calculation buttons side by side on one row."""
    return {"kind": "buttons", "buttons": [tuple(p) for p in pairs]}


def tab(title, *rows, **kwargs):
    """One tab: a title plus the rows above, parameters first."""
    return {"title": title, "name": kwargs.get("name"), "rows": list(rows)}


def page(left=(), right=(), footer=(), size=(1308, 653)):
    """The whole page: the terms tab widget on the left, the calculation
    tab widget on the right, and full-width buttons underneath both."""
    return {"left": list(left), "right": list(right),
            "footer": list(footer), "size": tuple(size)}


# ------------------------------------------------------------------ building

def _add_param(grid, row, spec, parent):
    """One (label, widget) row of a nested parameter grid."""
    label = BodyLabel(parent)
    label.setObjectName("label_" + (spec.get("name") or "row%d" % row))
    label.setText(spec["label"])
    grid.addWidget(label, row, 0)

    kind = spec["kind"]
    if kind == "field":
        w = LineEdit(parent)
        w.setText(spec["default"])
    elif kind == "combo":
        w = ComboBox(parent)
        for item in spec["items"]:
            w.addItem(item)
    elif kind == "check":
        w = CheckBox(parent)
        w.setChecked(spec["checked"])
    else:
        raise ValueError("not a parameter row: %r" % kind)
    w.setObjectName(spec["name"])
    grid.addWidget(w, row, 1)
    return w


def _build_tab(tabwidget, spec, index, owner):
    """Build one tab and add it to `tabwidget`. Widgets are also set as
    attributes on `owner` (the Ui_MainWindow instance), which is what
    qtwrap's getattr-based lookup resolves against once new_page() has
    composed it into the page class."""
    tab_w = QtWidgets.QWidget()
    tab_w.setObjectName(spec["name"] or ("tab_%d" % index))
    outer = QtWidgets.QGridLayout(tab_w)

    params = None   # the nested grid consecutive parameter rows accumulate in
    prow = 0
    orow = 0
    for row in spec["rows"]:
        kind = row["kind"]
        if kind in ("field", "combo", "check"):
            if params is None:
                params = QtWidgets.QGridLayout()
                outer.addLayout(params, orow, 0, 1, 1)
                orow += 1
                prow = 0
            w = _add_param(params, prow, row, tab_w)
            setattr(owner, row["name"], w)
            prow += 1
            continue
        params = None  # a non-parameter row closes the current grid
        if kind == "note":
            lab = BodyLabel(tab_w)
            lab.setObjectName(row["name"] or ("note_%d" % orow))
            lab.setText(row["text"])
            outer.addWidget(lab, orow, 0, 1, 1)
            if row["name"]:
                setattr(owner, row["name"], lab)
        elif kind == "buttons":
            for col, (name, text) in enumerate(row["buttons"]):
                b = PushButton(tab_w)
                b.setObjectName(name)
                b.setText(text)
                outer.addWidget(b, orow, col, 1, 1)
                setattr(owner, name, b)
        else:
            raise ValueError("unknown row kind: %r" % kind)
        orow += 1

    tabwidget.addTab(tab_w, spec["title"])
    setattr(owner, tab_w.objectName(), tab_w)


def build(owner, MainWindow, spec):
    """Populate `MainWindow` from `spec`, setting every named widget as an
    attribute on `owner`. Called from a mode's Ui_MainWindow.setupUi()."""
    if not MainWindow.objectName():
        MainWindow.setObjectName("MainWindow")
    MainWindow.resize(*spec["size"])

    central = QtWidgets.QWidget(MainWindow)
    central.setObjectName("centralwidget")
    grid = QtWidgets.QGridLayout(central)
    owner.centralwidget = central

    # "tabWidget_2"/"tabWidget_3" are Designer's auto-generated names, but
    # they are load-bearing: scfterms.py reaches the terms and calculation
    # tab widgets as form.tabWidget_2/form.tabWidget_3 (see
    # INTERFACE_GUIDE.md's "QTabWidget naming trap"). Keeping them means a
    # declaratively-built page is a drop-in for an SCF mode too. The
    # readable aliases are set alongside, for spec-side code.
    for col, (key, name, alias) in enumerate(
            (("left", "tabWidget_2", "terms_tabs"),
             ("right", "tabWidget_3", "calc_tabs"))):
        tabs = spec[key]
        if not tabs:
            continue
        tw = QtWidgets.QTabWidget(central)
        tw.setObjectName(name)
        for i, t in enumerate(tabs):
            _build_tab(tw, t, i, owner)
        tw.setCurrentIndex(0)
        grid.addWidget(tw, 0, col, 1, 1)
        setattr(owner, name, tw)
        setattr(owner, alias, tw)

    for i, (bname, btext) in enumerate(spec["footer"]):
        b = PushButton(central)
        b.setObjectName(bname)
        b.setText(btext)
        grid.addWidget(b, 1 + i, 0, 1, 2)
        setattr(owner, bname, b)

    MainWindow.setCentralWidget(central)
    # the Designer path emits both of these; qtwrap's progress bar lives in
    # the status bar, and QMainWindow would otherwise create one lazily
    owner.menubar = QtWidgets.QMenuBar(MainWindow)
    owner.menubar.setObjectName("menubar")
    MainWindow.setMenuBar(owner.menubar)
    owner.statusbar = QtWidgets.QStatusBar(MainWindow)
    owner.statusbar.setObjectName("statusbar")
    MainWindow.setStatusBar(owner.statusbar)
