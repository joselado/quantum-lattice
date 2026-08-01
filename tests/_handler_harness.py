"""Shared machinery for tests/test_handlers.py: import a mode headlessly
the same way the shell does (bin/versions/quantum-lattice-pyqt's
load_mode()) and drive its handler functions directly, without going
through connect_clicks()'s QThread/busy-lock wrapping - a handler is a
plain zero-arg callable (see common.py:wire_standard_signals()), so
calling it in-process is enough to exercise the same code a button click
runs, and is far simpler to assert on than clicking-and-waiting.

Leading underscore keeps pytest from collecting this as a test module.
"""
import importlib.util
import os
import sys

QLROOT = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))

_import_counter = 0


def import_mode(mode):
    """Import interface-pyqt/<mode>/<mode>.py fresh, under a name unique
    to this call (so re-importing the same mode across tests doesn't hit
    sys.modules's cache and skip its top-level build/wiring). Mirrors
    bin/versions/quantum-lattice-pyqt:load_mode() - same spec_from_file_location
    dance, needed because every mode's generated interface.py defines the
    same Ui_MainWindow class name (see qtwrap.py:_load_ui_module's
    docstring)."""
    global _import_counter
    _import_counter += 1
    moddir = os.path.join(QLROOT, "interface-pyqt", mode)
    if moddir not in sys.path:
        sys.path.insert(0, moddir)  # e.g. huge_0d's sibling handlers.py/islandbuild.py
    modname = "test_handler_mode_%s_%d" % (mode, _import_counter)
    spec = importlib.util.spec_from_file_location(modname, os.path.join(moddir, mode + ".py"))
    modobj = importlib.util.module_from_spec(spec)
    sys.modules[modname] = modobj
    spec.loader.exec_module(modobj)
    return modobj


def activate(modobj):
    """Point qtwrap's get()/getbox()/modify() at this mode's page, and
    restore its own scratch dir as cwd (same thing qtwrap._AppBase's
    connect_clicks wrapper does before a real click-driven handler runs -
    see qtwrap.py:_with_own_scratch_dir) - needed because importing a
    second mode re-points qtwrap's global `form` at the newer page."""
    from interfacetk import qtwrap
    qtwrap.set_active(modobj.window)
    if getattr(modobj.window, "scratch_dir", None):
        os.chdir(modobj.window.scratch_dir)


def set_field(modobj, name, value):
    """Set a LineEdit-style field's text directly. Deliberately bypasses
    qtwrap.modify(), which silently no-ops on a missing/mistyped widget
    name (see modify()'s try/except) - a test should fail loudly instead
    if the field it means to exercise doesn't exist."""
    activate(modobj)
    widget = getattr(modobj.window, name)
    widget.setText(str(value))


def set_combo(modobj, name, value):
    """Set a ComboBox-style field's current selection directly."""
    activate(modobj)
    widget = getattr(modobj.window, name)
    widget.setCurrentText(value)


def run_button(modobj, button):
    """Call the handler wired to `button` (a key of modobj.signals)
    directly, with this mode's page active and its own scratch dir as
    cwd - the same two things connect_clicks()'s wrapping guarantees for
    a real click, minus the QThread/busy-lock machinery, which exists to
    keep the GUI responsive and isn't needed to test the handler itself."""
    activate(modobj)
    fn = modobj.signals[button]
    return fn()
