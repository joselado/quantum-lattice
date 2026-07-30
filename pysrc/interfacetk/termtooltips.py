"""Physical-meaning tooltips for Hamiltonian terms (TERM_TOOLTIPS) and
calculation buttons (BUTTON_TOOLTIPS), shared across every mode.

Kept as its own module (rather than living inline in common.py) so it can be
imported both by common.py:set_formulas()/set_button_tooltips() (which show
these as hover text next to a term's formula image/field, or on a
calculation's PushButton) and by scfterms.py/hybridparts.py (which build
term fields of their own - the mean-field U/V1/V2/J1/J2/J3 tabs and the
hybrid modes' per-part fields, respectively - ahead of set_formulas()'s own
pass) without any of these modules depending on each other. This also
leaves room to grow each dict's value into {lang: text} for multi-language
support later without touching any caller.

Whenever a new term is added to a mode's interface (see the "Hamiltonian-term
formulas" convention in CLAUDE.md), add its tooltip to TERM_TOOLTIPS too.
Whenever a new calculation button is added, add its tooltip to
BUTTON_TOOLTIPS - button names are reused across modes for the same kind of
calculation (e.g. every mode's "Show bands" button is named show_bands), so
one entry there covers that button in every mode that has it.
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
"bias": "A perpendicular electric field (interlayer bias) that shifts onsite energies linearly with height, detuning layers at different z relative to one another. It breaks inversion symmetry between layers and can open or tune a gap at charge neutrality.",
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
"show_berry1d": "Compute the Berry curvature/phase along a 1D path in the Brillouin zone, the diagnostic used to detect 1D topological invariants such as edge polarization.",
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
}
