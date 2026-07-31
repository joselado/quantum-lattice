"""Runtime builder for the "pyqula code" sub-tab: a read-only view of the
pyqula script that reproduces the Hamiltonian currently described by a
mode's form fields, added as a third sibling of "Single particle"/"Many-body
interactions" inside "Terms in the Hamiltonian" (see scfterms.py's
_nest_scf_tab(), which builds and exposes those two as
form._hamiltonian_subtabs - a hard prerequisite for this module).

A mode wires this up with one call, after scfterms.build(qtwrap) and after
its own get_pyqula_code()-equivalent function is defined:

    from interfacetk import codeview
    codeview.build(qtwrap, get_pyqula_code)

`code_fn` is a zero-argument callable that reads the page's own widgets
(via qtwrap.get/getbox/get_array/is_checked, the same functions every other
handler in that mode's <mode>.py already uses) and returns a formatted
Python source string - see 0d.py/1d.py/2d.py's own get_pyqula_code() for
the convention: mirror that mode's get_geometry()/initialize(), but include
a term's line only when is_active() below says it's non-default, so the
generated script stays a short, clean listing of what's actually active
rather than a line-for-line dump of every possible term.

Refreshed whenever this tab becomes the current one (cheap and always
correct, since a sibling tab can't be edited while this one is showing) and
via an explicit Refresh button; a Copy button copies the current text to
the clipboard, since the entire point is to give the user something to
paste elsewhere."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QApplication
from PySide6.QtGui import QFont
from qfluentwidgets import PlainTextEdit, PushButton
from . import termhighlight


def is_active(qtwrap, name):
    """Whether a term field currently holds a non-default (non-zero) value
    - the same test termhighlight.py uses to bold a field the moment it's
    active, reused here so a term appears in the generated code exactly
    when it's shown as active in the UI. False (line omitted) if the field
    doesn't exist on this page."""
    field = getattr(qtwrap.form, name, None)
    if field is None: return False
    return termhighlight.is_nonzero_value(field.text())


def format_value(qtwrap, name):
    """Format a scalar field's raw text as a Python literal suitable for
    embedding directly in generated code: a plain float when the text
    parses as one, otherwise the raw text embedded verbatim as a lambda
    body - mirroring qtwrap.get()'s own fallback
    (eval("lambda r: "+text)) for the handful of fields (e.g.
    crystalfield, strain profiles) that can hold a position-dependent
    expression instead of a plain number."""
    text = getattr(qtwrap.form, name).text().strip()
    try:
        return repr(float(text))
    except ValueError:
        return "lambda r: " + text


def format_array(qtwrap, name):
    """Format an array field's raw comma-separated text (e.g. the
    "hoppings"/"exchange"/"pwave" convention "1st,2nd,3rd") as a Python
    list literal, the same components qtwrap.get_array()'s
    string2array() would parse."""
    text = getattr(qtwrap.form, name).text()
    vals = []
    for part in text.split(","):
        part = part.strip()
        vals.append(float(part) if part else 0.0)
    return "[" + ", ".join(repr(v) for v in vals) + "]"


def build(qtwrap, code_fn):
    """Add the "pyqula code" sub-tab to form._hamiltonian_subtabs (built by
    scfterms.build(qtwrap) - call this after that)."""
    form = qtwrap.form
    tabs = getattr(form, "_hamiltonian_subtabs", None)
    if tabs is None:
        raise RuntimeError(
            "codeview.build: form._hamiltonian_subtabs not found - call "
            "scfterms.build(qtwrap) before codeview.build(qtwrap,...).")

    page = QWidget()
    layout = QVBoxLayout(page)

    text_edit = PlainTextEdit(page)
    text_edit.setReadOnly(True)
    font = QFont("Monospace")
    font.setStyleHint(QFont.TypeWriter)
    text_edit.setFont(font)
    layout.addWidget(text_edit, 1)

    button_row = QWidget(page)
    button_layout = QHBoxLayout(button_row)
    button_layout.setContentsMargins(0, 0, 0, 0)
    refresh_button = PushButton("Refresh", button_row)
    copy_button = PushButton("Copy", button_row)
    button_layout.addWidget(refresh_button)
    button_layout.addWidget(copy_button)
    button_layout.addStretch(1)
    layout.addWidget(button_row)

    def refresh():
        text_edit.setPlainText(code_fn())

    def copy():
        QApplication.clipboard().setText(text_edit.toPlainText())

    refresh_button.clicked.connect(refresh)
    copy_button.clicked.connect(copy)

    idx = tabs.addTab(page, "pyqula code")
    # only recompute when this tab is the one being switched to - a sibling
    # tab can't be edited while this one is on screen, so this is always
    # enough to keep the text current
    tabs.currentChanged.connect(lambda i, idx=idx: refresh() if i == idx else None)
    refresh()  # initial content, so the tab isn't blank before first select
    return page
