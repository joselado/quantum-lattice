# -*- coding: utf-8 -*-
"""The tmdc mode's page, written as a declarative spec instead of
generated from interface.ui.

This is the pilot for retiring the Qt Designer XML path (see
INTERFACE_GUIDE.md, "Declarative pages"). Everything below describes what
the page contains; pysrc/interfacetk/formbuilder.py turns it into the same
widgets the promoted-Designer path built, and exposes it through the same
Ui_MainWindow/setupUi interface qtwrap.new_page() expects, so nothing else
in the app knows the difference.

Object names here are the contract with tmdc.py and the shared toolkit:
every field name is one qtwrap.get()/getbox() reads, and every button name
is one common.wire_standard_signals()/tmdc.py's `signals` dict wires. The
labels' own names are generated and referenced by nothing.
"""
from interfacetk.formbuilder import (build, button, button_row, combo, field,
                                     note, page, tab)

# operators.operator_list, set at runtime by tmdc.py's set_combobox() calls -
# left empty here rather than duplicated
OPERATORS = ()

SPEC = page(
    size=(1308, 653),
    left=[
        tab("Terms in the Hamiltonian",
            field("fermi", "Fermi energy", 0.0),
            field("ising_SOC", "Ising SOC", 0.0),
            field("cdw", "Charge density wave", 0.0),
            field("exchange", "Exchange field", "0.0, 0.0, 0.0"),
            field("rashba", "Rashba", 0.0),
            field("swave", "swave pairing", 0.0),
            name="tab_terms"),
    ],
    right=[
        tab("Structure",
            field("nsuper_struct", "Supercell", 5),
            button_row(("show_structure", "Show structure"),
                       ("show_structure_3d", "Show structure 3D")),
            name="tab_structure"),
        tab("Bands",
            combo("bands_color", "Operator", OPERATORS),
            field("nk_bands", "# kpoints", 300),
            button("show_bands", "Band structure"),
            name="tab_bands"),
        tab("DOS Bands",
            field("delta_kbands", "Smearing", 0.01),
            field("ne_kbands", "# of energies", 400),
            field("window_kbands", "Energy window", 3.0),
            field("scale_kbands", "KPM scale", 10.0),
            field("nv_kbands", "# vectors", 10),
            field("nk_kbands", "# of kpoints", 100),
            button("show_dosbands", "Show DOS Bands"),
            name="tab_dosbands"),
        tab("DOS",
            field("dos_nk", "Number of kpoints", 100),
            field("dos_ewindow", "Energy window", 4.0),
            field("dos_delta", "Smearing", 0.01),
            combo("dos_mode", "Mode", ("ED", "Green", "KPM")),
            combo("dos_operator", "Operator", OPERATORS),
            button("show_dos", "Density of states"),
            name="tab_dos"),
        tab("LDOS",
            field("multildos_ewindow", "Energy window", 1.5),
            field("multildos_nk", "Number of kpoints", 10),
            field("multildos_nrep", "Number of unit cells", 5),
            field("multildos_delta", "Smearing", 0.2),
            combo("basis_ldos", "Basis for the LDOS",
                  ("TB", "Real space atomic orbitals")),
            field("ratomic_ldos", "Atomic radii", 1.5),
            button("show_multildos", "Show LDOS"),
            name="tab_ldos"),
        tab("FS",
            field("fs_ewindow", "Energy window", 4.0),
            field("fs_delta", "Smearing", 0.2),
            field("fs_nk", "Number of kpoints", 30),
            button("show_fermi_surface", "Show Fermi surface"),
            name="tab_fs"),
        tab("Topology 2D",
            field("topology_nk", "# kpoints", 400),
            combo("topology_operator", "Operator", ("None", "Sz", "Valley")),
            button("show_berry1d", "1D Berry curvature"),
            button("show_berry2d", "2D Berry curvature"),
            button("show_z2", "Z2 invariant"),
            button("show_chern", "Chern number"),
            name="tab_topology"),
        tab("SDOS",
            field("kdos_ewindow", "Energy window", 0.5),
            field("kdos_mesh", "# of points", 100),
            button("show_kdos", "Show Surface DOS"),
            name="tab_sdos"),
        tab("Site DOS",
            note("Click a site in the structure plot to compute the DOS there",
                 name="label_site_dos_info"),
            field("site_dos_ewindow", "Energy window", 4.0),
            field("site_dos_delta", "Smearing", 0.03),
            field("site_dos_nk", "Number of kpoints", 30),
            button("show_site_dos", "Site DOS"),
            name="tab_site_dos"),
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
