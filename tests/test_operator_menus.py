"""Every operator a page's menu offers must be one pyqula builds for the
Hamiltonian that page builds - a menu item that can only ever fail is a
bug. common.get_operator() is where pyqula refuses one (a spin operator on
a spinless Hamiltonian, the hole projector outside Nambu, the Berry
operator outside 2d, ...), so this builds each cheap page's default
Hamiltonian once per Hamiltonian type and resolves every offered item.
tbg is left to test_term_restrictions.py: its Hamiltonian takes seconds.
"""
import contextlib
import io

import pytest

from _handler_harness import import_mode, set_combo, activate
from interfacetk import common

MENUS = ["bands_color", "dos_operator", "operator_kdos", "fs_operator",
         "topology_operator", "operator_chern"]
# items a page resolves itself rather than through common.get_operator()
OWN_ITEMS = {"dispersive_electrons", "kondo_sites", "none"}


@pytest.mark.parametrize("mode", ["0d", "1d", "2d", "3d", "hofstader1d",
                                  "heavyfermion", "tmdc", "spinspiral"])
def test_offered_operators_resolve(mode):
    m = import_mode(mode)
    types = ["Spinless", "Spinful", "Nambu"] if hasattr(m.window, "hamiltonian_type") else [None]
    failures = []
    for htype in types:
        if htype: set_combo(m, "hamiltonian_type", htype)
        activate(m)
        with contextlib.redirect_stdout(io.StringIO()):
            h = m.initialize() if mode != "0d" else m.pickup_hamiltonian()
        for menu in MENUS:
            combo = getattr(m.window, menu, None)
            if combo is None: continue
            for i in range(combo.count()):
                item = combo.itemText(i)
                if item.lower() in OWN_ITEMS: continue
                try:
                    common.get_operator(common.hamiltonian_for_operator(h, item), item)
                except Exception as e:
                    failures.append((htype, menu, item, str(e)[:80]))
    assert not failures, failures
