"""DictForm: a qtwrap-like accessor that reads from a plain JSON snapshot
instead of live Qt widgets.

A mode's get_geometry()/initialize() (and common.py helpers like
solve_scf()) are written against a "window"/"qtwrap" object exposing
get()/getbox()/get_array()/is_checked() - normally the real qtwrap module,
resolving against whichever page is currently active. To let the exact
same functions run unmodified inside run_calculation.py's child process
(which never builds a QApplication/page - see that script's docstring),
DictForm implements that same surface reading from a dict instead.

The dict shape is exactly what qtwrap.save_interface() already writes -
{name: {"type": "line"/"combo"/"check", "value": ...}} - so gathering
inputs for a subprocess-based calculation is just "call save_interface()
to a file" (see qtwrap.run_calculation_subprocess()), not a bespoke
per-handler field list to keep in sync by hand.
"""
from .qtwrap import string2array
import numpy as np


class _FieldStub:
    """Enough of a widget's surface for hamiltoniantype.get_type() (which
    does getattr(form,"hamiltonian_type",None).currentText()) to work
    against a DictForm the same way it would against a real ComboBox."""
    def __init__(self,value):
        self._value = value
    def currentText(self):
        return self._value
    def isChecked(self):
        return bool(self._value)
    def text(self):
        return str(self._value)


class DictForm:
    def __init__(self,snapshot):
        self._snapshot = snapshot
        self.form = self # hamiltoniantype.get_type() does
                          # `form = qtwrap.form if hasattr(qtwrap,"form")
                          # else qtwrap`, then getattr(form,name,None) -
                          # so self.form must resolve through __getattr__
                          # the same way a real page object would

    def _raw(self,name,default=None):
        entry = self._snapshot.get(name)
        return default if entry is None else entry["value"]

    def get(self,name,string=False,default=0.0,call=True):
        # mirrors qtwrap.get()'s own contract exactly: never raises to the
        # caller, always falls back to `default` on anything unparseable -
        # including a malformed position-dependent expression (haldane/
        # peierls/mAF/crystalfield/strain can hold "r: <expr>" instead of a
        # plain number) that fails its own sanity test-call below. Without
        # this, such a field would silently work for every in-process
        # handler (which already tolerates it this way) but blow up here -
        # the one path currently routed through DictForm - with an
        # inconsistent, harder-to-explain failure.
        v = self._raw(name,default)
        try:
            if string: return str(v)
            try:
                return float(v)
            except (TypeError,ValueError):
                if not call: raise
                out = str(v).replace("\n","")
                if "import os" in out: raise ValueError("suspicious field value: %r"%out)
                a = eval("lambda r: "+out)
                a([0.,0.,0.]) # sanity-check, same test-call qtwrap.get() makes
                return a
        except Exception:
            return default

    def getbox(self,name):
        return self._raw(name)

    def get_array(self,name,v0=(0.,0.,0.),**kwargs):
        v = self._raw(name)
        if v is None: return np.array(v0)
        return string2array(v)

    def is_checked(self,name,default=False):
        return bool(self._raw(name,default))

    def _current_page(self):
        # common.mark_scf_solved()'s hasattr(page,"_scf_dirty") check is
        # False for this object, so it correctly no-ops here - the real
        # page's _scf_dirty is cleared by the caller after a successful
        # subprocess run instead (see qtwrap.run_calculation_subprocess()'s
        # callers).
        return self

    def __getattr__(self,name):
        if name.startswith("_"): raise AttributeError(name)
        entry = self._snapshot.get(name)
        if entry is None: raise AttributeError(name)
        return _FieldStub(entry["value"])
