"""What latticeterms.connect() does to a built page's dropdowns: the items
of the operator, parameter-sweep and SCF "Initial guess" menus follow the
lattice and the Hamiltonian type (latticeterms.ITEM_RULES), so a user
can't pick one that pyqula refuses - a spin operator on a Spinless
Hamiltonian, the hole projector outside Nambu, the sublattice operator on
a lattice without sublattices.

Items used to be removed and appended one by one, which moved an item
that came back to the end of its menu, lost the user's choice after a
Spinless -> Spinful round trip, and doubled hofstader1d's valley operator
(a Designer "Valley" next to an appended "valley").
"""
from _handler_harness import import_mode, set_combo, activate


def items(combo):
    return [combo.itemText(i) for i in range(combo.count())]


def test_operators_follow_the_hamiltonian_type():
    m = import_mode("2d")
    w = m.window
    full = items(w.bands_color)
    assert "Sz" in full and "hole" not in full # Spinful by default
    set_combo(m, "hamiltonian_type", "Spinless")
    assert not {"Sx", "Sy", "Sz", "hole"} & set(items(w.bands_color))
    set_combo(m, "hamiltonian_type", "Nambu")
    assert {"Sz", "hole"} <= set(items(w.bands_color))
    set_combo(m, "hamiltonian_type", "Spinful")
    assert items(w.bands_color) == full # same items, same order


def test_operators_follow_the_lattice():
    m = import_mode("2d")
    w = m.window
    full = items(w.dos_operator)
    set_combo(m, "lattice", "Square")
    assert "valley" not in items(w.dos_operator)
    assert "sublattice" not in items(w.dos_operator)
    set_combo(m, "lattice", "Lieb") # sublattices, but not honeycomb
    assert "sublattice" in items(w.dos_operator)
    assert "valley" not in items(w.dos_operator)
    set_combo(m, "lattice", "Honeycomb")
    assert items(w.dos_operator) == full # valley back in its own place


def test_choice_survives_a_round_trip():
    m = import_mode("2d")
    w = m.window
    activate(m)
    w.bands_color.setCurrentText("Sz") # as a click would
    assert w.scf_initialization.currentText() == "antiferro" # the default
    set_combo(m, "hamiltonian_type", "Spinless")
    assert w.bands_color.currentText() == "None"
    assert w.scf_initialization.currentText() != "antiferro"
    set_combo(m, "hamiltonian_type", "Spinful")
    assert w.bands_color.currentText() == "Sz"
    assert w.scf_initialization.currentText() == "antiferro"


def test_no_duplicate_items():
    # hofstader1d's Designer bands_color has "Valley"; pyqula's spelling is
    # "valley", which the old add/remove pass appended next to it
    m = import_mode("hofstader1d")
    for name in ["bands_color", "dos_operator"]:
        combo = getattr(m.window, name, None)
        if combo is None: continue
        lowered = [t.lower() for t in items(combo)]
        assert len(lowered) == len(set(lowered)), (name, items(combo))


def test_dropdown_filled_after_connect_is_restricted():
    # hybridribbon fills dos_operator (qtwrap.set_combobox) only after
    # latticeterms.connect(); set_combobox re-applies the restrictions
    m = import_mode("hybridribbon")
    set_combo(m, "hamiltonian_type", "Spinless")
    assert "Sz" not in items(m.window.dos_operator)
    assert "hole" not in items(m.window.dos_operator)


def test_saved_choice_restored_whatever_the_widget_order(tmp_path):
    # a session saved as Nambu with the hole projector selected, restored
    # with bands_color coming before the hamiltonian_type that offers it
    import json
    from interfacetk import qtwrap
    m = import_mode("2d")
    saved = {"bands_color": {"type": "combo", "value": "hole"},
             "hamiltonian_type": {"type": "combo", "value": "Nambu"}}
    path = tmp_path / "interface.json"
    path.write_text(json.dumps(saved))
    activate(m)
    qtwrap.load_interface(m.window, str(path))
    assert m.window.hamiltonian_type.currentText() == "Nambu"
    assert m.window.bands_color.currentText() == "hole"
