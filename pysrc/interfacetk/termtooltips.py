"""Physical-meaning tooltips for Hamiltonian terms (TERM_TOOLTIPS),
calculation buttons (BUTTON_TOOLTIPS), and other form parameters
(PARAM_TOOLTIPS), shared across every mode.

Kept as its own module (rather than living inline in common.py) so it can be
imported both by common.py:set_formulas()/set_button_tooltips()/
set_param_tooltips() (which show these as hover text next to a term's
formula image/field, on a calculation's PushButton, or on any other
LineEdit/ComboBox/CheckBox/RadioButton field) and by scfterms.py/
hybridparts.py (which build term fields of their own - the mean-field
U/V1/V2/J1/J2/J3 tabs and the hybrid modes' per-part fields, respectively -
ahead of set_formulas()'s own pass) without any of these modules depending
on each other. This also leaves room to grow each dict's value into
{lang: text} for multi-language support later without touching any caller.

Whenever a new term is added to a mode's interface (see the "Hamiltonian-term
formulas" convention in CLAUDE.md), add its tooltip to TERM_TOOLTIPS too.
Whenever a new calculation button is added, add its tooltip to
BUTTON_TOOLTIPS - button names are reused across modes for the same kind of
calculation (e.g. every mode's "Show bands" button is named show_bands), so
one entry there covers that button in every mode that has it. Whenever a new
non-term, non-button field is added (a numeric parameter, combobox, or
checkbox controlling how a calculation is run rather than a Hamiltonian term
or a calculation trigger), add its tooltip to PARAM_TOOLTIPS the same way -
field names are reused across modes for the same kind of setting (e.g.
"nk_bands", "dos_delta", "scf_initialization") wherever the underlying
meaning is the same, so check whether an existing entry already fits before
adding a near-duplicate.

CALC_FORMULAS (near the end of this file, after BUTTON_TOOLTIPS) is the
calculation-button analog of a term's formula PNG: it maps a button name to
a formula *key*, and tools/gen_calc_formula_logos.py renders one PNG per key
(interface-pyqt/logos/calc_<key>.png) - so if a new button computes a
quantity some other button already has a formula for (e.g. another kind of
LDOS), just map it to that existing key instead of adding a new one.
Consumed by common.py:set_calculation_formulas(), called once per mode from
finalize_page() alongside set_formulas()/set_button_tooltips().
"""

TERM_TOOLTIPS = {
"hopping": "Sets the amplitude t_ij for electrons to tunnel between neighboring orbitals - the kinetic-energy term that turns otherwise isolated atomic levels into dispersive bands. Larger hopping gives wider bands and stronger electron delocalization.",
"fermi": "Shifts the Fermi (chemical potential) energy, controlling how many electron states below it are filled. This is equivalent to doping the system away from half filling, moving the Fermi level through the band structure without changing the bands themselves.",
"exchange": "A Zeeman-like exchange field (Jx,Jy,Jz) that couples to the electron spin, favoring alignment along its direction. It mimics an external magnetic moment or spin polarization, splitting spin-up and spin-down bands.",
"haldane": "A complex second-neighbor hopping that breaks time-reversal symmetry with zero net magnetic flux through the unit cell (Haldane model). It opens a topological gap and can drive the system into a Chern insulator with a quantized anomalous Hall response.",
"kanemele": "Intrinsic spin-orbit coupling that acts like a Haldane term with opposite sign for opposite spins, so time-reversal symmetry is preserved (Kane-Mele model). It opens a topological gap supporting the quantum spin Hall effect, with counter-propagating spin-polarized edge states.",
"antihaldane": "A staggered version of the Haldane coupling that flips sign between the two valleys (K and K') instead of sharing one chirality across the Brillouin zone. It is used to probe valley-contrasting topological physics, such as valley Hall effects, rather than a uniform Chern insulator.",
"antikanemele": "A staggered analogue of the Kane-Mele spin-orbit term, with opposite sign between valleys/sublattices instead of the uniform intrinsic SOC pattern. It lets you explore valley- or sublattice-selective spin-orbit physics beyond the standard quantum spin Hall term.",
"mAB": "A staggered onsite potential that raises one sublattice and lowers the other, breaking inversion symmetry. On a honeycomb lattice this opens a trivial mass gap at the Dirac points, as happens e.g. in hexagonal boron nitride.",
"mAF": "A staggered (Neel) magnetic order parameter that points electron spins in opposite directions on the two sublattices. It represents an antiferromagnetic mean-field state, breaking spin-rotation symmetry while keeping zero net magnetization.",
"swave": "An onsite (s-wave) superconducting pairing amplitude that pairs opposite-spin electrons on the same site, as in conventional BCS superconductivity. It opens a superconducting gap at the Fermi level via electron-hole (Bogoliubov-de Gennes) mixing.",
"pwave": "A spin-triplet (p-wave) pairing amplitude that pairs same-spin electrons on neighboring sites, giving odd-parity superconducting order. Unlike s-wave pairing, it can support topological superconductivity and Majorana bound states at boundaries or vortices.",
"rashba": "Spin-orbit coupling from broken inversion symmetry perpendicular to the lattice plane, e.g. due to a substrate or applied field. It locks electron spin to momentum direction, splitting bands of opposite spin helicity.",
"kondo": "The exchange coupling J_K between a localized (e.g. f-electron) magnetic moment and the spin of itinerant conduction electrons - the defining interaction of the Kondo/heavy-fermion problem. It screens the local moment and gives rise to the emergent heavy quasiparticle bands.",
"kexchange": "An exchange coupling between neighboring localized magnetic moments, distinct from the conduction-electron Kondo coupling above. It sets the strength of direct or RKKY-mediated magnetic interactions between the localized moments, controlling whether they order magnetically.",
"exchange_impurity": "A Zeeman-like exchange field applied only at the embedded impurity site, polarizing its local spin independently of the host lattice. It models a magnetic impurity coupled to a non-magnetic host via Green's-function embedding.",
"fermi_impurity": "An onsite energy shift applied only at the impurity site, detuning its level position relative to the host band structure. It controls the impurity's occupation and its resonance position relative to the Fermi level.",
"U": "The local (onsite) Hubbard repulsion between two opposite-spin electrons occupying the same orbital. It is the basic interaction driving mean-field magnetism (e.g. Neel order) and Mott-insulating behavior at strong coupling.",
"V1": "A density-density interaction between electrons on first-neighbor sites, extending the Hubbard model beyond purely local repulsion. Together with U it can stabilize charge-ordered or charge-density-wave states when strong enough.",
"V2": "A density-density interaction between electrons on second-neighbor sites, a longer-range extension of the Hubbard/V1 terms. It helps stabilize charge-order patterns that a purely local or first-neighbor interaction alone cannot capture.",
"J1": "A first-neighbor Heisenberg exchange coupling between localized spins, J(S_i . S_j), with J>0 antiferromagnetic and J<0 ferromagnetic. It is usually the leading magnetic interaction setting collinear or non-collinear spin order on the lattice.",
"J2": "A second-neighbor Heisenberg exchange coupling, adding a longer-range magnetic interaction on top of J1. Competition between J1 and J2 (frustration) can favor non-collinear, incommensurate, or spiral magnetic order instead of simple Neel order.",
"J3": "A third-neighbor Heisenberg exchange coupling, the next magnetic interaction shell beyond J1 and J2. It is typically weaker but can further stabilize or frustrate a given magnetic ordering pattern depending on the lattice geometry.",
"crystalfield": "An onsite potential shaped by the lattice geometry itself (e.g. by layer/stacking position) rather than a uniform shift. It is used to model effects like a substrate potential or interlayer stacking asymmetry that vary from site to site in a geometry-dependent way.",
"peierls": "An orbital magnetic field applied via Peierls substitution, threading flux through the lattice's loops rather than just coupling to spin. It can generate Landau levels and, at rational flux fractions, Hofstadter-butterfly-like band structures.",
"inplaneb": "An in-plane orbital magnetic field, entering through a Peierls phase that depends on the out-of-plane extent of the system rather than coupling directly to spin. It is the relevant orbital-field geometry for thin films/slabs, as opposed to the perpendicular (out-of-plane) field.",
"interlayer": "The interlayer hopping amplitude between vertically stacked layers, typically decaying with distance away from direct vertical alignment. It sets the strength of interlayer coupling, controlling band splitting and hybridization between the layers.",
"tinter": "The interlayer hopping amplitude between the twisted layers, decaying with in-plane/out-of-plane distance (Slater-Koster-like form). Together with the twist angle it sets the moire bandwidth, including the flat-band regime near the magic angle.",
"interlayer_bias": "A perpendicular electric field (interlayer bias) that shifts onsite energies linearly with height, detuning layers at different z relative to one another. It breaks inversion symmetry between layers and can open or tune a gap at charge neutrality.",
"ising_SOC": "An Ising-type spin-orbit coupling that pins spin out of plane with a sign tied to the valley index, characteristic of monolayer transition-metal dichalcogenides. It locks spin and valley together, suppressing spin-flip scattering within a valley.",
"cdw": "A charge-density-wave order parameter that modulates the onsite energy periodically in space with wavevector Q, as seen in materials like NbSe2. It reflects a lattice/electronic instability that spontaneously breaks translational symmetry.",
"strain": "A local modification of the hopping amplitude along a specific bond direction, mimicking the effect of mechanical strain on that bond. It lets you probe strain-induced band structure changes, such as pseudo-magnetic fields in honeycomb lattices.",
}


# Physical-meaning tooltips for calculation buttons ("Show bands", "Show
# DOS", ...), shared across every mode the same way TERM_TOOLTIPS is:
# keyed by the PushButton's object name, which is the same across modes
# for the standard calculations (STANDARD_HANDLERS in common.py) and for
# most of the mode-specific ones too, since modes reuse the same button
# name whenever they expose the same kind of calculation. Consumed by
# common.py:set_button_tooltips(qtwrap), called once per mode after
# connect_clicks() the same way set_formulas() is.
BUTTON_TOOLTIPS = {
"show_bands": "Diagonalize the Hamiltonian along a k-path through the Brillouin zone and plot the resulting band structure (optionally colored by the selected operator's expectation value).",
"show_dos": "Compute the density of states, either by k-space integration (Green's function) or by the kernel polynomial method (KPM), optionally projected onto the selected operator.",
"show_kdos": "Compute the k-resolved density of states (KDOS) along a path, showing how spectral weight is distributed in both energy and momentum - useful for visualizing surface/edge states.",
"show_dosbands": "Compute the DOS resolved along the band structure path (a smeared version of the bands), useful for seeing where spectral weight concentrates without picking discrete bands.",
"show_iets_qdos": "Compute the momentum-resolved inelastic tunneling spectroscopy (IETS) signal - the RPA spin-excitation response along a q-path - showing the magnon/spin-wave-like dispersion of the converged magnetic state. Requires a mean-field Hamiltonian solved via SCF with an onsite interaction.",
"show_iets_ldos": "Compute the real-space inelastic tunneling spectroscopy (IETS) signal across a sweep of energies, opening an interactive viewer with an energy slider showing the spatial map at that energy next to the total (site-summed) IETS vs energy - the same style of viewer as Multi LDOS. Requires a mean-field Hamiltonian solved via SCF with an onsite interaction.",
"show_berry1d": "Compute the Berry curvature along a 1D path in the Brillouin zone - the same quantity as the 2D Berry curvature map, evaluated along a path instead of over a mesh - the diagnostic used to detect 1D topological invariants such as edge polarization.",
"show_berry2d": "Compute the Berry curvature over a 2D mesh of the Brillouin zone and plot it as a map, showing which k-points contribute most to the system's topological response.",
"show_z2": "Compute the Z2 topological invariant via the Wannier charge center (Vanderbilt) method, distinguishing a trivial insulator from a quantum spin Hall (topological) insulator.",
"show_chern": "Integrate the Berry curvature over the Brillouin zone to compute the Chern number, the topological invariant that predicts a quantized anomalous Hall conductance.",
"show_fermi_surface": "Diagonalize the Hamiltonian on a k-mesh near the chosen energies and plot the resulting constant-energy contours (Fermi surface).",
"show_qpi": "Compute the quasiparticle interference pattern - the Fourier transform of the joint density of states - which mimics the scattering interference seen in STM measurements.",
"show_multildos": "Compute the local density of states at several energies and plot it spatially, showing how the wavefunction weight is distributed across the system at each energy.",
"show_site_dos": "Open an interactive view: click a site in the geometry to recompute and plot the local density of states at that specific site.",
"show_structure": "Write out the current geometry and plot the lattice in 2D (atomic positions and, optionally, bonds).",
"show_structure_3d": "Write out the current geometry and open an interactive 3D view of the lattice (atomic positions and bonds).",
"show_magnetism": "Compute the self-consistent or externally-set magnetic moments at each site and plot them as arrows overlaid on the geometry.",
"solve_scf": "Run the self-consistent mean-field loop (Hubbard/V/J interactions) until the order parameter converges, then save the resulting Hamiltonian for use by the other calculations.",
"compute_sweep": "Repeat the calculation while sweeping one parameter over a range of values, collecting the results into a single sweep plot instead of a single calculation.",
"select_atoms_removal": "Open an interactive picker on the geometry to select which atoms to remove, then rebuild the geometry/Hamiltonian with those atoms excluded.",
"show_hoppings": "Write out the hopping matrix elements and plot them as a network, showing the connectivity and relative strength of the bonds in the lattice.",
"show_interactive_ldos": "Compute the local density of states at several energies and plot it spatially, showing how the wavefunction weight is distributed across the system at each energy.",
"show_local_chern": "Compute a real-space-resolved (local) Chern marker at each site, showing where in real space the topological response is concentrated - useful for finite/disordered systems where the k-space Chern number isn't directly defined.",
"show_time_evolution": "Time-evolve a wavepacket initially localized on the selected atom under the Hamiltonian and plot how its weight spreads through the system over time.",
"select_atom_time_evolution": "Open an interactive picker on the geometry to choose the single atom the wavepacket for the time-evolution calculation starts on.",
"show_ldos": "Compute the local density of states and plot it spatially or as a map, showing how the wavefunction weight is distributed across the system.",
"show_ldos_single": "Compute the local density of states at a single chosen energy and plot it spatially, showing how the wavefunction weight is distributed across the system at that energy.",
"show_band_ldos": "Compute the local density of states resolved along the band structure, showing how spectral weight at each band/momentum is distributed spatially (e.g. bulk vs edge).",
"show_edge_dos": "Compute the density of states projected onto the edge (boundary) of the system, isolating spectral features - such as edge states - that live at the boundary rather than the bulk.",
"show_hofstader": "Diagonalize the Hamiltonian over a range of magnetic field values and plot the resulting Hofstadter butterfly - energy levels as a function of applied flux.",
"select_atoms_dos": "Open an interactive picker on the geometry to select which atoms are included when computing the DOS.",
"select_path": "Draw a path across the geometry with the mouse, defining the line of atoms used by the DOS-along-a-path calculation.",
"show_path": "Plot the path of atoms previously selected on the geometry, showing which sites the DOS-along-a-path calculation will use.",
"show_path_dos": "Compute the density of states along the previously-selected path of atoms and plot it as a function of position along the path.",
"show_eigenvalues": "Diagonalize the Hamiltonian (or estimate the spectrum via KPM for large systems) and plot the resulting eigenvalue spectrum.",
"show_lattice": "Build and write out the current geometry, then plot the resulting lattice/structure.",
"show_potential": "Compute and plot the onsite potential at the edge atoms of the geometry, useful for checking boundary/edge effects before running a calculation.",
"show_spatial_dos": "Compute the local density of states at each site for a set of energies (via KPM) and plot it spatially, e.g. to simulate an STM topography image.",
"show_embedding_ldos": "Compute the local density of states of the host lattice with the impurity embedded (via Green's-function embedding), at the chosen energy.",
"show_embedding_ldos_sweep": "Compute the local density of states of the host lattice with the impurity embedded (via Green's-function embedding), swept over a range of energies.",
"select_impurity_sites": "Open an interactive picker on the geometry to select which sites the embedded impurity terms are applied to.",
"save_results": "Save all the results from this calculation into a named local folder (you'll be asked for a name) - pick a new name to keep multiple saves side by side.",
"load_results": "Load a previously saved interface configuration (parameter values) back into the form - you'll be asked which saved folder to restore.",
"show_configuration": "Build a fresh random configuration at the requested filling, anneal it via Metropolis-annealed discrete swaps if needed (or reuse the last anneal if no parameter has changed since), then plot the occupied (1) vs. empty (0) sites over the lattice.",
"show_relaxation": "Step through the occupation snapshots recorded at intervals during the last anneal, from the initial random configuration to the final one, alongside the energy trajectory with a marker showing the current step.",
"show_correlator_relaxation": "Step through the anneal alongside the energy trace, showing the reciprocal-space structure factor S(q) at each snapshot for a 2D lattice (its ordering wavevector), or the neighbor-shell density-density correlator for the Chain lattice (its ordering length scale).",
"show_spin_configuration": "Build a fresh random spin configuration at the requested initial magnetization, relax it via single-spin-flip Metropolis dynamics if needed (or reuse the last anneal if no parameter has changed since), then plot the up (+1) vs. down (-1) spins over the lattice.",
"show_spin_relaxation": "Step through the spin-configuration snapshots recorded at intervals during the last anneal, from the initial random configuration to the final one, alongside the energy and total-magnetization trajectories with a marker showing the current step.",
"show_spin_correlator_relaxation": "Step through the anneal alongside the energy and magnetization traces, showing the reciprocal-space structure factor S(q) at each snapshot for a 2D lattice (its ordering wavevector - e.g. ferromagnetic order peaks at q=0, checkerboard antiferromagnetic order at the zone corner), or the neighbor-shell spin-spin correlator for the Chain lattice (its ordering length scale).",
}


# Button name -> formula key, for calculation buttons whose result is a
# well-defined physical quantity with a formula worth showing (e.g.
# show_bands). Deliberately excludes buttons that only display/pick
# something rather than computing a physical quantity (show_structure,
# select_atoms_removal, save_results, compute_sweep, ...). Several button
# names across different modes/formulas map to the *same* key - e.g.
# show_ldos/show_multildos/show_embedding_ldos are all just "LDOS via the
# Green's function", so they render the same PNG - the same "reuse across
# modules" convention as BUTTON_TOOLTIPS above, but at the image level: one
# key here is one PNG (tools/gen_calc_formula_logos.py, output
# interface-pyqt/logos/calc_<key>.png), reused by every button mapped to
# it. Consumed by common.py:set_calculation_formulas(), which places the
# image next to the button (see _ensure_button_formula_image()) and reuses
# the matching BUTTON_TOOLTIPS text as its hover tooltip too.
CALC_FORMULAS = {
"show_bands": "bands",
"show_eigenvalues": "eigenvalues",
"show_dos": "dos",
"show_kdos": "kdos",
"show_dosbands": "kdos",
"show_ldos": "ldos",
"show_ldos_single": "ldos",
"show_interactive_ldos": "ldos",
"show_multildos": "ldos",
"show_site_dos": "ldos",
"show_spatial_dos": "ldos",
"show_edge_dos": "ldos",
"show_path_dos": "ldos",
"show_embedding_ldos": "ldos",
"show_embedding_ldos_sweep": "ldos",
"show_band_ldos": "wavefunction",
"show_berry2d": "berry_curvature",
"show_berry1d": "berry_curvature",
"show_chern": "chern",
"show_local_chern": "local_chern",
"show_z2": "z2",
"show_fermi_surface": "fermi_surface",
"show_qpi": "qpi",
"show_iets_qdos": "iets_q",
"show_iets_ldos": "iets_r",
"show_magnetism": "magnetism",
"show_hofstader": "hofstadter",
"show_time_evolution": "time_evolution",
}


# Physical-meaning tooltips for the remaining form parameters - numeric
# fields, comboboxes, and checkboxes that control how a calculation is run
# rather than a Hamiltonian term (TERM_TOOLTIPS) or a calculation trigger
# (BUTTON_TOOLTIPS). Keyed by object name and consumed the same way as
# BUTTON_TOOLTIPS: common.py:set_param_tooltips(qtwrap), called once per
# mode from finalize_page() alongside set_button_tooltips(), skips any
# field that already carries a more specific, hand-authored tooltip set in
# interface.ui (e.g. 2d's "hoppings" field), so this dict only fills in
# fields that would otherwise have none - one entry here covers a field
# name in every mode that has it, since e.g. "nk_bands" or "dos_delta"
# mean the same thing wherever they appear.
PARAM_TOOLTIPS = {
# --- lattice / geometry ---
"lattice": "Selects which lattice geometry family to build (e.g. honeycomb, square, triangular, kagome, ...). This determines the unit cell and coordination number, and which lattice-restricted terms/operators (Haldane, Kane-Mele, valley) are available - changing it rebuilds the geometry and Hamiltonian from scratch.",
"nsuper": "Number of times the unit cell is repeated (supercell size) when building the geometry/Hamiltonian used in the calculation. A larger supercell gives a bigger, more expensive system - needed e.g. to host a real-space defect, impurity, or disorder pattern that wouldn't fit in a single unit cell.",
"nsuper_struct": "Number of times the unit cell is repeated only for the structure/hopping plot (Show lattice/Show hoppings), independent of the supercell actually used in the calculation - lets you visualize a bigger chunk of the lattice without paying the cost of computing on it.",
"ribbon_width": "Number of unit cells across the ribbon's finite (confined) direction, controlling how many parallel rows/chains make up the ribbon and hence how far its two edges are from each other.",
"nsides": "Number of edges of the polygon used to cut a finite island out of the infinite lattice (e.g. 6 for a hexagonal flake).",
"rotation": "Rotation angle applied to the lattice/unit cell before cutting out the finite island, changing which edge terminations end up on its boundary.",
"remove_selected": "If checked, the atoms previously chosen with the atom-removal picker are excluded when the geometry/Hamiltonian is (re)built.",
"hoppings": "Hopping amplitudes for successive neighbor shells, entered as comma-separated numbers - the first number is the 1st-neighbor hopping, the second the 2nd-neighbor hopping, and so on.",
"strain_strength": "Magnitude of the bond-dependent hopping modification applied by the strain term.",
"strain_decay": "Decay length controlling how quickly the strain-induced hopping modification falls off with distance from the strained bond/region.",
"strain_type": "Selects the spatial pattern of the applied strain - a radial scalar modulation, or a radial vector (direction-dependent) modulation of the hoppings.",
"thickness": "Number of atomic layers stacked to build the slab/film.",
"inplaneb_phi": "Angle (in units of pi) of the in-plane magnetic field direction within the layer plane, entering the Peierls phase together with the in-plane field's magnitude.",
"ti": "Interlayer hopping amplitude between the two stacked layers of the bilayer whose Hofstadter spectrum is being computed.",
"cell_size": "Size of the moire/multilayer unit cell (unit cells per side) used when constructing the twisted-multilayer geometry - larger values give a bigger moire supercell at higher computational cost.",
"multilayer_type": "Selects which twisted or aligned multilayer stacking (bilayer, trilayer, ...) is built.",
"nbands": "Number of bands computed and plotted around the Fermi level; leave blank/zero to compute and show every band instead.",
"set_half_filling": "If checked, the Fermi level is shifted so the system sits exactly at half filling before computing, instead of using the fixed Fermi-energy value.",
"nparts": "Number of spatial parts (regions along the film/ribbon's finite direction) the Hamiltonian is split into, each with its own independent set of parameters below - increase it to build a heterostructure/junction out of more than the default two regions.",
# --- huge_0d island construction ---
"geometry_mode": "Selects how the island geometry is generated: from a stored shape recipe, from explicit atomic positions, or from an image used as a mask to cut the island's outline.",
"target_diameter": "If checked, the island is regenerated with a corrected size until its actual diameter matches the desired diameter below, instead of using the raw recipe parameters as-is.",
"desired_dameter": "Target diameter (in units of the lattice constant) the island should have when Target diameter is checked.",
"nedges": "Number of edges of the polygon used to cut the island's outline out of the lattice.",
"clean_island": "If checked, atoms left with only a single bond after cutting the island are removed, avoiding spurious dangling-atom states at the edge.",
"LDOS_num_atom": "Comma-separated indices of the specific atoms whose local density of states is computed and plotted.",
"LDOS_polynomials": "Number of Chebyshev polynomials used in the KPM expansion of the per-atom LDOS - more polynomials resolve finer energy features at higher computational cost.",
"smearing_local_dos": "Energy broadening (smearing) applied when reconstructing the per-atom LDOS from its KPM expansion.",
"num_ene_ldos": "Number of energy points at which the per-atom LDOS is evaluated and plotted.",
"energy_cutoff_local_dos": "Maximum energy shown on the per-atom LDOS energy axis.",
"DOS_polynomials": "Number of Chebyshev polynomials used in the KPM expansion of the total DOS - more polynomials resolve finer spectral features at higher computational cost.",
"DOS_iterations": "Number of random vectors used in the stochastic trace estimate of the KPM density of states - more iterations reduce statistical noise in the result.",
"smearing_dos": "Energy broadening (smearing) applied when reconstructing the total DOS from its KPM expansion.",
"num_ene_dos": "Number of energy points at which the total density of states is evaluated and plotted.",
"mode_dosmap": "Single shot computes and plots the spatial DOS/STM map at one energy; Movie sweeps over a range of energies instead, producing one frame per energy played back as an animation.",
"mode_stm": "Selects the algorithm used to compute the spatial DOS/STM map: Full inverts the Green's function directly (accurate, more expensive), Eigen restricts the calculation to a sparse window of eigenstates found via Arnoldi iteration (faster for large systems).",
"smearing_spatial_DOS": "Energy broadening (smearing) applied when computing the spatial DOS/STM map.",
"nwaves_dos": "Number of eigenstates computed by the sparse Arnoldi solver for the Eigen STM mode - more waves capture a wider energy window around the target energy.",
"energy_spatial_DOS": "Energy at which the spatial DOS/STM map (Single shot mode) is evaluated.",
"mine_movie": "Starting energy of the sweep used to render the spatial-DOS movie.",
"maxe_movie": "Final energy of the sweep used to render the spatial-DOS movie.",
"stepse_movie": "Number of energy steps (frames) in the spatial-DOS movie.",
"pols_path": "Number of Chebyshev polynomials used in the KPM expansion of the DOS along the selected path.",
"ecut_path": "Maximum energy considered in the DOS-along-a-path calculation.",
"num_ene_path": "Number of energy points sampled along the path DOS.",
"smearing_path_dos": "Energy broadening (smearing) applied to the DOS computed along the selected path.",
"initial_atom": "Index of the atom where the selected path begins.",
"final_atom": "Index of the atom where the selected path ends.",
"width_path": "Half-width of the strip of atoms around the drawn path line that are accepted as part of the path.",
# --- Hofstadter butterfly ---
"numb_hofs": "Number of magnetic-field values sampled between the initial and final field for the Hofstadter butterfly.",
"minb_hofs": "Minimum magnetic field (flux) value in the Hofstadter butterfly scan.",
"maxb_hofs": "Maximum magnetic field (flux) value in the Hofstadter butterfly scan.",
"ewindow_hofs": "Energy window shown around the Fermi level at each magnetic field value in the Hofstadter butterfly.",
"nume_hofs": "Number of energy points computed at each magnetic field value in the Hofstadter butterfly.",
"hofstader_mode": "Restricts the Hofstadter spectrum to all states, bulk-projected states, or edge-projected states, letting you distinguish bulk Landau levels from edge/chiral states.",
"nsuper_ldos": "Number of times the unit cell is repeated when plotting the interactive multi-energy LDOS.",
# --- k-point mesh density (Brillouin-zone sampling) for a given calculation ---
"nk_bands": "Number of k-points sampled along the band-structure path (or per KPM stochastic evaluation) - denser sampling gives a smoother band structure at higher computational cost.",
"nk_dos": "Density of the k-point mesh used to compute the density of states - a denser mesh gives a smoother DOS at higher computational cost.",
"dos_nk": "Density of the k-point mesh used to compute the density of states - a denser mesh gives a smoother DOS at higher computational cost.",
"nk_ldos": "Density of the k-point mesh used to compute the local density of states.",
"nk_ldos_single": "Density of the k-point mesh used for the single-energy LDOS calculation.",
"nk_scf": "Density of the k-point mesh used to converge the self-consistent mean-field loop - too coarse a mesh can give an inaccurate, or falsely converged, order parameter.",
"fs_nk": "Density of the k-mesh used to sample the Brillouin zone for the Fermi-surface map.",
"qpi_nk": "Density of the k-mesh used to compute the joint density of states underlying the QPI pattern.",
"topology_nk": "Density of the k-mesh used to integrate the Berry curvature for the Chern number / Berry-curvature map.",
"site_dos_nk": "Density of the k-point mesh used when recomputing the density of states at the clicked site.",
"band_ldos_nk": "Density of the k-point mesh used for the LDOS resolved along the band structure.",
"nk_iets": "Density of the k-mesh (Brillouin-zone sampling) used in the RPA spin-susceptibility calculation underlying the IETS signal.",
"nk_kbands": "Number of k-points used in the KDOS-resolved-along-bands calculation.",
"kdos_mesh": "Number of k-points sampled along the path for the k-resolved density of states.",
"mesh_kdos": "Number of k-points sampled along the path for the k-resolved density of states.",
"nq_iets": "Number of q-points sampled along the path for the momentum-resolved IETS calculation.",
# --- energy broadening (smearing) ---
"delta_kbands": "Energy broadening (smearing) applied to each band when coloring/computing the KPM-based band structure.",
"delta_iets": "Energy broadening (smearing) applied to the excitation spectrum in the IETS calculation.",
"dos_delta": "Energy broadening (smearing) of each computed energy level, controlling how much neighboring states blur together in the plotted density of states.",
"delta_dos": "Energy broadening (smearing) of each computed energy level, controlling how much neighboring states blur together in the plotted density of states.",
"multildos_delta": "Energy broadening (smearing) applied at each of the sampled energies in the multi-energy LDOS calculation.",
"fs_delta": "Energy broadening (smearing) applied when selecting states near each target energy for the Fermi-surface map.",
"qpi_delta": "Energy broadening (smearing) applied to the states entering the QPI joint density of states.",
"delta_ldos": "Energy broadening (smearing) applied when computing the local density of states.",
"delta_ldos_single": "Energy broadening (smearing) applied to the single-energy LDOS calculation.",
"energy_ldos_single": "Energy at which the single-shot LDOS is evaluated.",
"nsuper_ldos_single": "Number of repeated supercells shown around the plotted single-energy LDOS.",
"site_dos_delta": "Energy broadening (smearing) applied when recomputing the density of states at the clicked site.",
"sdos_delta": "Energy broadening (smearing) applied to the spatial density of states calculation.",
"smearing_scf": "Energy broadening (smearing) used for the occupations/Green's functions inside the self-consistent mean-field loop.",
"delta_embedding_ldos": "Energy broadening (smearing) applied to the host+impurity embedding LDOS calculation.",
# --- energy window (range around the Fermi level) ---
"window_kbands": "Energy window (range around the Fermi level) shown in the KPM-based band structure / DOS-along-bands plot.",
"window_iets": "Energy window over which the IETS spectrum is computed and plotted.",
"window_ldos": "Energy window over which the local density of states is computed.",
"dos_ewindow": "Energy window (range around the Fermi level) over which the density of states is computed and plotted.",
"multildos_ewindow": "Energy window from which the set of energies for the multi-energy LDOS calculation is drawn.",
"fs_ewindow": "Energy window around the target energies used when selecting states for the Fermi-surface map.",
"qpi_ewindow": "Energy window over which the QPI pattern is computed.",
"kdos_ewindow": "Energy window (range around the Fermi level) shown in the k-resolved density of states plot.",
"ewindow_kdos": "Energy window (range around the Fermi level) shown in the k-resolved density of states plot.",
"site_dos_ewindow": "Energy window over which the density of states at the clicked site is computed.",
"sdos_ewindow": "Energy window over which the spatial density of states is computed.",
# --- number of energy points sampled within a window ---
"ne_kbands": "Number of energy points sampled within the energy window for the KPM-based band structure / DOS-along-bands plot.",
"ne_iets": "Number of energy points sampled within the energy window for the IETS spectrum.",
"ne_ldos": "Number of energy points sampled within the energy window for the local density of states.",
"num_energies_embedding_ldos_sweep": "Number of energy points sampled in the host+impurity embedding LDOS energy sweep.",
# --- KPM accuracy knobs ---
"nv_kbands": "Number of random vectors used in the stochastic trace estimate for the KPM-based band coloring - more vectors reduce statistical noise at higher computational cost.",
"scale_kbands": "Rescaling factor bringing the Hamiltonian's spectrum within the [-1,1] range the Chebyshev (KPM) expansion requires - increase it if the KPM band plot shows spurious features from an under-rescaled spectrum.",
"fs_numw": "Number of eigenstates computed sparsely around the target energies for the Fermi-surface map, instead of diagonalizing the full Hamiltonian.",
# --- operator/mode selectors ---
"operator_kdos": "Operator whose expectation value colors/weights the k-resolved density of states plot.",
"dos_operator": "Operator whose expectation value the density of states is projected onto (None for the total, unprojected DOS).",
"bands_color": "Operator whose expectation value colors the plotted band structure, letting you see e.g. spin, valley, or edge/bulk character band by band.",
"bands_colormap": "Colormap used to render the operator-colored band structure.",
"fs_operator": "Operator whose expectation value colors the plotted Fermi surface.",
"topology_operator": "Operator used when computing the reciprocal-space Berry curvature map / Chern number, restricting the calculation to a subspace (e.g. one spin or valley) rather than all bands.",
"ldos_operator": "Operator whose expectation value the local density of states is projected onto.",
"operator_chern": "Operator used when computing the real-space (local) Chern marker, restricting it to a particular subspace (e.g. spin or valley) rather than all bands.",
"dos_mode": "Selects the DOS algorithm: exact diagonalization (small systems), k-space Green's function integration, or the kernel polynomial method (KPM, for large systems).",
"mode_dos": "Selects the DOS algorithm: Lowest computes only the states nearest the Fermi level via a sparse eigensolver, KPM expands the full spectrum with Chebyshev polynomials - Lowest is faster when only the moire/flat bands near zero energy matter.",
# --- LDOS basis ---
"basis_ldos": "Chooses the basis the LDOS is expressed in: directly in the tight-binding orbital basis, or projected onto real-space atomic-like orbitals of a chosen radius (Real space atomic orbitals).",
"ratomic_ldos": "Radii of the atomic-like wavefunctions put on every site. Only affects the result for the \"Real space atomic orbitals\" basis.",
# --- magnetism plot ---
"magnetization_nrep": "Number of repeated unit cells shown around the plotted magnetic moments.",
"magnetization_plot_mode": "2D draws the magnetic moments as arrows over a flat view of the lattice; 3D opens an interactive three-dimensional view instead.",
# --- SCF ---
"hamiltonian_type": "Selects the internal shape of the Hamiltonian: Spinless (no spin degree of freedom - spin-dependent terms like exchange, Kane-Mele SOC, Rashba, and antiferromagnetism are unavailable), Spinful (the default - includes real electron spin), or Nambu (spinful plus an electron-hole (BdG) sector, enabling the s-wave/p-wave pairing terms for superconductivity). Hamiltonian terms that don't apply to the current choice are hidden.",
"scf_initialization": "Initial guess for the mean-field order parameter the SCF loop starts from (e.g. an antiferromagnetic or a ferromagnetic axis, or a random configuration) - a poor initial guess can converge to a different, possibly metastable, self-consistent solution.",
"filling_scf": "Target electron filling the SCF loop's chemical potential is adjusted to reach, instead of using the Fermi energy field directly.",
"do_scf": "Turns the self-consistent mean-field loop on, so calculations use the converged interacting Hamiltonian instead of the bare single-particle one - turned on automatically once any interaction term (U/V1/V2/J1/J2/J3) is set nonzero.",
"mix_scf": "Linear mixing fraction between the previous and newly computed order parameter at each SCF iteration - lower values converge more slowly but more stably.",
"scf_maxite": "Maximum number of self-consistency iterations before the SCF loop gives up - a run that hits this limit without converging prints a warning instead of raising an error.",
"extra_electron": "Extra electrons (beyond charge neutrality) added to the SCF target filling - equivalent to doping the system away from half filling.",
# --- parameter sweep ---
"sweep_parameter": "Hamiltonian parameter that is varied over the sweep (e.g. sublattice imbalance, exchange components, Haldane/Kane-Mele coupling, s-wave pairing, Fermi energy).",
"sweep_task": "Quantity recomputed at each sweep point: the indirect gap, the density of states, the Chern number, or the full eigenvalue spectrum.",
"sweep_initial": "Starting value of the swept parameter.",
"sweep_final": "Final value of the swept parameter.",
"sweep_steps": "Number of values sampled between the initial and final value of the sweep.",
# --- time evolution ---
"channel_time_evolution": "Spin channel (up or down) of the initial localized wavepacket used in the time-evolution calculation.",
"tmax_time_evolution": "Maximum simulation time the wavepacket is evolved for.",
# --- impurity embedding ---
"impurity_potential": "Onsite energy shift added at the embedded impurity site(s), detuning them relative to the host lattice.",
"impurity_exchange": "Exchange/Zeeman field added at the embedded impurity site(s), polarizing their local spin independently of the host lattice.",
"nsuper_impurity": "Supercell size used when embedding the impurity/impurities, controlling how many host unit cells surround them.",
"energy_embedding_ldos": "Energy at which the host+impurity local density of states is evaluated.",
"ncells_embedding_ldos": "Number of host unit cells plotted around the embedded impurity in the embedding LDOS map.",
# --- classical lattice models (lattice gas, Ising) ---
"supercell_size": "Number of unit cells per side of the finite patch built to host the classical model (lattice gas / Ising) - a larger patch reduces boundary effects at higher annealing cost.",
"filling": "Fraction of sites occupied (strictly between 0 and 1 - the swap-based anneal needs at least one occupied and one empty site) - the number of occupied sites is fixed at this value and preserved by every swap move during annealing.",
"Jij": "Neighbor-shell coupling strengths (J1, J2, J3, ...), entered as comma-separated numbers, for the classical density-density interaction between occupied sites - positive values are repulsive, negative values attractive.",
"mu_profile": "Site-dependent chemical potential bias, either a single number (uniform - has no effect on the annealed ground state since filling is fixed) or a position-dependent expression 'r[0]', 'r[1]', 'r[2]' being the site's x/y/z coordinates.",
"temp": "Metropolis temperature used during annealing - higher values accept more energy-increasing moves (swaps or spin flips, depending on the model), helping escape local minima at the cost of a noisier final configuration.",
"ntries": "Number of Metropolis move attempts (swaps or spin flips, depending on the model) performed during annealing - more attempts give the search more chances to reach a low-energy configuration, at higher computational cost.",
"n_snapshots": "Number of intermediate configurations captured during the anneal for the relaxation/correlator-relaxation Step slider - more snapshots give a finer-grained view of the relaxation at negligible extra cost (a snapshot itself is cheap to write; only the correlator/structure-factor view recomputes anything expensive, and only once per anneal).",
"magnetization": "Initial average magnetization in [-1,1] used to build the random starting spin configuration (0: half up, half down) - since the default single-spin-flip dynamics does not conserve magnetization, this only sets the starting point, not a constraint on the final annealed state.",
"Jij_ising": "Neighbor-shell coupling strengths (J1, J2, J3, ...), entered as comma-separated numbers, for the classical spin-spin exchange between sites - positive values are ferromagnetic (favor aligned spins), negative values antiferromagnetic. Opposite sign convention from the lattice gas model's Jij.",
"field_profile": "Site-dependent external (Zeeman-like) field bias, either a single number (uniform - unlike the lattice gas model's chemical potential, a uniform field here does matter, since the default single-spin-flip dynamics does not conserve magnetization) or a position-dependent expression 'r[0]', 'r[1]', 'r[2]' being the site's x/y/z coordinates.",
}
