# -*- coding: utf-8 -*-
"""The spinspiral mode's page, written as a declarative spec instead of
generated from interface.ui (the second mode built this way, after tmdc -
see INTERFACE_GUIDE.md, "Declarative pages").

Object names here are the contract with spinspiral.py and the shared
toolkit: every field name is one qtwrap.get()/getbox()/get_array() reads,
and every button name is one common.wire_standard_signals()/spinspiral.py's
`signals` dict wires. The labels' own names are generated and referenced by
nothing.
"""
from interfacetk.formbuilder import (build, button, button_row, check, combo,
                                     field, note, page, tab)

# operators.operator_list, set at runtime by spinspiral.py's set_combobox()
# calls - left empty here rather than duplicated
OPERATORS = ()

SPEC = page(
    size=(1308, 653),
    left=[
        tab("Terms in the Hamiltonian",
            field("hopping", "Hopping", 1.0),
            field("fermi", "Fermi energy", 0.0),
            field("spiral_exchange", "Spiral exchange", 0.3),
            field("rashba", "Rashba SOC", 0.0),
            field("kanemele", "Intrinsic SOC", 0.0),
            name="tab_terms"),
        tab("Spin spiral",
            combo("lattice", "Lattice", ("Chain", "Triangular")),
            field("qvector", "Spiral wavevector", "0.25, 0.0"),
            field("max_supercell", "Max. supercell", 20),
            combo("spiral_plane", "Spiral plane", ("XY", "YZ", "ZX", "Custom")),
            field("spiral_axis", "Custom cone axis", "0.0, 0.0, 1.0"),
            field("cone_angle", "Cone angle (deg)", 90.0),
            # filled in by spinspiral.py's report_spiral(), which appends
            # the wavevector/supercell actually built to this same line
            note("", name="spiral_info"),
            name="tab_spiral"),
    ],
    right=[
        tab("Structure",
            field("nsuper_struct", "Supercell", 2),
            field("magnetization_nrep", "Texture replicas", 3),
            combo("magnetization_plot_mode", "Texture plot mode", ("3D", "2D")),
            button_row(("show_structure", "Show structure"),
                       ("show_structure_3d", "Show structure 3D")),
            button("show_magnetism", "Show spin texture"),
            name="tab_structure"),
        tab("Bands",
            combo("bands_color", "Operator", OPERATORS),
            field("nk_bands", "# kpoints", 200),
            field("nbands", "# bands (0 = all)", 0),
            button("show_bands", "Band structure"),
            name="tab_bands"),
        tab("DOS",
            field("dos_nk", "Number of kpoints", 40),
            field("dos_ewindow", "Energy window", 4.0),
            field("dos_delta", "Smearing", 0.05),
            combo("dos_mode", "Mode", ("ED", "Green", "KPM")),
            combo("dos_operator", "Operator", OPERATORS),
            button("show_dos", "Density of states"),
            name="tab_dos"),
        tab("Spiral LDOS",
            field("spiral_ldos_ewindow", "Energy window", 4.0),
            field("spiral_ldos_ne", "# of energies", 100),
            field("spiral_ldos_delta", "Smearing", 0.1),
            field("spiral_ldos_nk", "Number of kpoints", 20),
            combo("spiral_ldos_projection", "Spin projection",
                  ("None", "Sx", "Sy", "Sz", "Custom axis", "Local moment")),
            field("spiral_ldos_axis", "Custom projection axis", "0.0, 0.0, 1.0"),
            field("spiral_ldos_nrep", "Spiral periods to show", 3),
            check("spiral_ldos_subtract_average", "Subtract the average", True),
            button("show_spiral_ldos", "LDOS along the spiral"),
            name="tab_spiral_ldos"),
    ],
    footer=[("save_results", "Save results"),
            ("load_results", "Load results")],
)


class Ui_MainWindow(object):
    """Same shape as the pyside6-uic-generated class it replaces: qtwrap's
    _load_ui_module() imports this module and new_page() composes this
    class into the page type, then calls setupUi() on the instance."""

    def setupUi(self, MainWindow):
        build(self, MainWindow, SPEC)

    def retranslateUi(self, MainWindow):
        """Kept for interface compatibility with the generated files -
        every label/button text is set inline by build() above, so there
        is nothing to re-apply."""
