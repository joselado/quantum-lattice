"""Bold a Hamiltonian-term field's text while it holds a nonzero (active)
value, so which terms are actually contributing to the built Hamiltonian
is visible at a glance across a tab mostly full of untouched "0.0"
fields, without opening every tab to check.

Shared by common.py:set_formulas() (the single-particle terms),
scfterms.py (the mean-field U/V1/V2/J1/J2/J3 fields) and hybridparts.py
(hybrid modes' per-part fields) - kept as its own module, like
termtooltips.py, so none of these need to depend on each other. qtwrap.py
also imports it (see load_interface()) to refresh highlighting on fields
restored from a saved interface.json, since setText() there doesn't fire
the textEdited signal wire_highlight() relies on for live edits.
"""


def is_nonzero_value(text):
    """Whether a term field's raw text represents a nonzero value. Handles
    both a plain number and the comma-separated vector format used by
    fields like "exchange" (Jx,Jy,Jz) or "hoppings" (1st NN, 2nd NN, ...) -
    any component that fails to parse as a float counts as nonzero too, so
    an unrecognized value stays highlighted rather than being silently
    treated as the zero default."""
    for part in text.split(","):
        part = part.strip()
        if not part: continue
        try:
            if float(part) != 0.0: return True
        except ValueError:
            return True
    return False


def apply_highlight(field, nonzero):
    """Bold `field`'s text if `nonzero`, plain otherwise. Idempotent (skips
    the no-op case) so it's cheap to call on every keystroke; a plain bold
    QFont, rather than a stylesheet color/border, is used deliberately - it
    can't clash with qfluentwidgets' own QSS the way setStyleSheet() would
    (see the LineEdit/BodyLabel theming machinery this app already relies
    on for formula images), and it reads correctly in both light and dark
    theme with no accent-color bookkeeping."""
    nonzero = bool(nonzero)
    font = field.font()
    if font.bold() == nonzero: return
    font.setBold(nonzero)
    field.setFont(font)


def wire_highlight(field):
    """Tag `field` as a Hamiltonian-term field (checked by
    qtwrap.load_interface() to know which restored fields need their
    highlight refreshed) and keep its highlight in sync with live edits."""
    field._term_highlight = True
    apply_highlight(field, is_nonzero_value(field.text()))
    field.textEdited.connect(lambda text, field=field: apply_highlight(field, is_nonzero_value(text)))


# A term's logical key (as used in common.py:set_formulas()'s `terms`
# list, TERM_TOOLTIPS, ...) doesn't always match its interface.ui field's
# actual object name - see INTERFACE_GUIDE.md's "Term key vs. field object
# name" gotcha. find_term_field() below falls back to these known cases so
# highlighting still reaches the actual input field instead of silently
# finding nothing; qtwrap.set_tooltip()'s equivalent lookup does not use
# this table and still only tooltips the "<term>_image" label for these
# three (a separate, pre-existing gap this doesn't attempt to fix).
FIELD_ALIASES = {
    "hopping": "hoppings",
    "fermi_impurity": "impurity_potential",
    "exchange_impurity": "impurity_exchange",
}


def find_term_field(form, term):
    """Find `term`'s QLineEdit on `form` by its exact name, falling back
    to FIELD_ALIASES for the handful of terms whose field is named
    differently. Returns None if neither name is found (e.g. this mode
    doesn't have this term at all - the normal, silent-skip case)."""
    from PySide6 import QtWidgets
    field = form.findChild(QtWidgets.QLineEdit,term)
    if field is not None: return field
    alias = FIELD_ALIASES.get(term)
    if alias is not None: return form.findChild(QtWidgets.QLineEdit,alias)
    return None
