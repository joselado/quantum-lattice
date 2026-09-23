"""Static check that the same thing is worded the same way on every page.

The pages were written mode by mode, so a k-point count was labelled six
ways ("# kpoints", "# of kpoints", "Number of kpoints", "nkpoints", ...),
and the same button read "Save results" on one page and "Save Results" on
the next. This keeps the one wording each now has: it reads the label and
button text straight from every interface.ui, and the field labels from
the two formbuilder specs (tmdc, spinspiral), so it builds no page.
"""
import collections
import glob
import os
import re
import xml.etree.ElementTree as ET

QLROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Buttons whose text is deliberately different on one page, because the
# button does something different there.
BUTTON_EXCEPTIONS = {
    ("0d", "show_bands"),       # "Eigenvalues": an island has no bands
    ("huge_0d", "show_ldos"),   # DOS on picked atoms, not a spatial LDOS
    ("spinspiral", "show_magnetism"), # the imposed spin texture
}


def _ui_texts():
    """(mode, widget class, object name, text) for every label/button."""
    out = []
    for ui in sorted(glob.glob(os.path.join(QLROOT, "interface-pyqt", "*", "interface.ui"))):
        mode = os.path.basename(os.path.dirname(ui))
        if mode == "quasiperiodic": continue
        for w in ET.parse(ui).iter("widget"):
            if w.get("class") not in ("BodyLabel", "PushButton", "CheckBox"): continue
            for prop in w.findall("property"):
                if prop.get("name") == "text" and prop.find("string") is not None:
                    out.append((mode, w.get("class"), w.get("name"), prop.find("string").text or ""))
    for mode in ["tmdc", "spinspiral"]: # formbuilder specs: field("name", "Label", ...)
        src = open(os.path.join(QLROOT, "interface-pyqt", mode, "interface.py")).read()
        for name, label in re.findall(r'field\("([^"]+)", "([^"]*)"', src):
            out.append((mode, "BodyLabel", name, label))
    return out


TEXTS = _ui_texts()


def test_scan_found_texts():
    assert len(TEXTS) > 500


def test_k_points_are_spelled_one_way():
    bad = [t for t in TEXTS if re.search(r"(?i)\bn?kpoints?\b", t[3])]
    assert not bad, bad


def test_counts_read_number_of():
    bad = [t for t in TEXTS if t[1] == "BodyLabel" and t[3].lstrip().startswith("#")]
    assert not bad, bad


def test_shared_buttons_read_the_same():
    texts = collections.defaultdict(lambda: collections.defaultdict(list))
    for mode, cls, name, text in TEXTS:
        if cls == "PushButton" and (mode, name) not in BUTTON_EXCEPTIONS:
            texts[name][text.strip()].append(mode)
    differing = {name: dict(t) for name, t in texts.items() if len(t) > 1}
    assert not differing, differing
