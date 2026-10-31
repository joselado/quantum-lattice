# -*- coding: utf-8 -*-
"""The hopftilings mode's page, a declarative spec (see INTERFACE_GUIDE.md, "Declarative pages").

Three small studies built on the scripts in extras/ (HOPF_INSULATOR.md, TILINGS.md): the 3D Hopf insulator, tight-binding models on
the Hat/Spectre/Turtle tilings, and 1D chains whose onsite energy is read along a line of the Chair44 tiling.  Field and button names
are the contract with hopftilings.py.
"""
from interfacetk.formbuilder import (build, button, button_row, check, combo,
                                     field, note, page, tab)

SPEC = page(
    size=(1308, 653),
    left=[
        tab("Hopf insulator",
            field("hopf_h", "Mass parameter h", 2.0),
            field("hopf_layers", "Number of layers", 12),
            note("Two-band 3D insulator H(k) = d(k).sigma with Hopf invariant 0, -1 or +2 depending on h (gap closes at |h| = 1, 3).",
                 name="hopf_info"),
            name="tab_hopf"),
        tab("Tiling",
            combo("tiling_kind", "Tiling", ("Spectre", "Hat", "Turtle")),
            field("tiling_level", "Substitution level (1 to 3)", 2),
            combo("tiling_hopping", "Hopping", ("Unit", "Inverse length", "Gaussian")),
            field("spectre_dir", "Spectre repository folder (blank = auto)", ""),
            note("Hat, Spectre and Turtle share one vertex graph: with unit hopping their spectra coincide.", name="tiling_info"),
            name="tab_tiling"),
        tab("Chair44 chain",
            combo("chain_line", "Line", ("Axis", "Body diagonal")),
            field("chain_depth", "Depth (6 to 16)", 12),
            field("chain_lambda", "Onsite strength", 1.0),
            field("chain_nlines", "Number of lines", 6),
            note(
                "Onsite energy = Chair44 pyramid height along the line, compared with the same line shuffled. Needs the Spectre repository folder set in the Tiling tab.",
                name="chain_info"),
            name="tab_chain"),
    ],
    right=[
        tab("Hopf insulator",
            button("show_hopf_invariant", "Hopf invariant"),
            button("show_hopf_gap", "Bulk gap"),
            button("show_hopf_slab", "Slab spectrum"),
            name="tab_hopf_calc"),
        tab("Tiling",
            button("show_tiling", "Show tiling"),
            button("show_tiling_spectrum", "Spectrum and IPR"),
            name="tab_tiling_calc"),
        tab("Chair44 chain",
            button("show_chair44_chain", "Localisation of the chain"),
            name="tab_chain_calc"),
    ],
    footer=[],
)


class Ui_MainWindow(object):
    """Same shape as the pyside6-uic-generated class: qtwrap composes it into the page type and calls setupUi()."""

    def setupUi(self, MainWindow):
        build(self, MainWindow, SPEC)

    def retranslateUi(self, MainWindow):
        """Kept for interface compatibility; build() sets every text inline."""
