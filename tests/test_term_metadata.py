"""Static consistency checks for the two "whenever you add X, also add Y"
rules CLAUDE.md documents by hand for common.py's set_formulas()/
set_button_tooltips():

  - every Hamiltonian term set_formulas() renders needs a TERM_TOOLTIPS
    entry and a white-on-transparent interface-pyqt/logos/<term>.png
  - every button STANDARD_HANDLERS wires (the shared, reused-across-modes
    calculation buttons) needs a BUTTON_TOOLTIPS entry

These are regex/text checks over the source, not an execution of the code -
same style as tools/smoke_test.py's signal-wiring check - so a forgotten
tooltip/logo fails here without needing to build any page.
"""
import os
import re

import pytest
from interfacetk.termtooltips import TERM_TOOLTIPS, BUTTON_TOOLTIPS
from interfacetk.common import STANDARD_HANDLERS

QLROOT = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
LOGOS_DIR = os.path.join(QLROOT, "interface-pyqt", "logos")
COMMON_PY = os.path.join(QLROOT, "pysrc", "interfacetk", "common.py")


def _formula_terms():
    """Parse set_formulas()'s `terms`/`meanfield_terms` list literals
    straight out of common.py's source - they're local variables inside
    the function body, not module-level constants, so this can't just
    import them."""
    src = open(COMMON_PY).read()
    m = re.search(r"def set_formulas\(qtwrap\):.*?\n\n\n", src, re.S)
    assert m, "set_formulas() not found in common.py - has it moved/been renamed?"
    body = m.group(0)
    terms, meanfield_terms = [], []
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("terms") and "=" in line:
            terms += re.findall(r'"([a-zA-Z_0-9]+)"', line)
        elif line.startswith("meanfield_terms") and "=" in line:
            meanfield_terms += re.findall(r'"([a-zA-Z_0-9]+)"', line)
    assert terms and meanfield_terms, "failed to parse terms/meanfield_terms out of set_formulas()"
    return terms, meanfield_terms


TERMS, MEANFIELD_TERMS = _formula_terms()
ALL_FORMULA_TERMS = TERMS + MEANFIELD_TERMS


@pytest.mark.parametrize("term", ALL_FORMULA_TERMS)
def test_term_has_tooltip(term):
    assert term in TERM_TOOLTIPS, (
        f'"{term}" is rendered by set_formulas() but has no TERM_TOOLTIPS '
        f"entry in pysrc/interfacetk/termtooltips.py"
    )


@pytest.mark.parametrize("term", ALL_FORMULA_TERMS)
def test_term_has_logo(term):
    path = os.path.join(LOGOS_DIR, term + ".png")
    assert os.path.isfile(path), (
        f'"{term}" is rendered by set_formulas() but interface-pyqt/logos/{term}.png is missing'
    )


@pytest.mark.parametrize("button", sorted(STANDARD_HANDLERS))
def test_standard_button_has_tooltip(button):
    assert button in BUTTON_TOOLTIPS, (
        f'"{button}" is wired via common.STANDARD_HANDLERS but has no BUTTON_TOOLTIPS '
        f"entry in pysrc/interfacetk/termtooltips.py"
    )
