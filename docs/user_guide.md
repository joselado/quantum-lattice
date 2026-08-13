# Quantum Lattice — User Guide

Quantum Lattice is a desktop application for tight-binding and mean-field
calculations, built on top of the [pyqula](https://github.com/joselado/pyqula)
library. It lets you pick a lattice geometry, set physical parameters in
form fields, and compute/plot band structures, densities of states, Berry
curvature, Chern numbers, self-consistent mean-field order parameters, and
more — without writing any code.

This guide covers how to use the application. It does not cover installing
or extending it — see `README.md` for installation and a gallery of example
results, and `CLAUDE.md`/`INTERFACE_GUIDE.md` if you are developing the
interface itself rather than using it.

## Contents

- [Launching the app](#launching-the-app)
- [The interface at a glance](#the-interface-at-a-glance)
- [A typical workflow](#a-typical-workflow)
- [Modifying the geometry](#modifying-the-geometry)
- [Hamiltonian type: Spinless, Spinful, Nambu](#hamiltonian-type-spinless-spinful-nambu)
- [Self-consistent mean-field (SCF) calculations](#self-consistent-mean-field-scf-calculations)
- [Saving and loading your work](#saving-and-loading-your-work)
- [While a calculation is running](#while-a-calculation-is-running)
- [Reference: Hamiltonian terms](#reference-hamiltonian-terms)
- [Reference: calculation buttons](#reference-calculation-buttons)
- [Reference: modes](#reference-modes)
- [Updating the application](#updating-the-application)
- [Troubleshooting](#troubleshooting)

## Launching the app

After installing (see `README.md`), start the app from a terminal with:

```bash
quantum-lattice
```

This opens a single window with a navigation sidebar on the left. Every
lattice type ("mode") is a page you switch to from that sidebar — there is
no separate window per calculation, and switching pages never loses the
parameters you've entered on other pages.

## The interface at a glance

**The sidebar** groups modes by physical family rather than raw
dimensionality:

- **Multidimensional models** — Islands (0D), Ribbons (1D), Sheets (2D), 3D
  crystals: the general-purpose building blocks, one per dimensionality.
- **Van der Waals** — multilayer and twisted/moiré graphene, transition
  metal dichalcogenides, and a "huge islands" mode for very large flakes.
- **Embedded impurities** — a clean host lattice (ribbon or sheet) with a
  point impurity embedded via a Green's-function technique.
- **Hybrid systems** — a ribbon or film split into independently-tunable
  spatial parts (e.g. a bilayer with different parameters per layer).
- **Misc** — Hofstadter butterflies, a heavy-fermion Kondo lattice, and
  thin-film slabs.
- **Classical models** — a lattice gas (classical, occupation-based
  particles on a lattice) and an Ising model (classical up/down spins on a
  lattice), no quantum Hamiltonian involved in either.

See [Reference: modes](#reference-modes) below for what's distinctive about
each one. The first time you open a mode's page in a session it takes a
moment to build; after that, switching back to it is instant.

**Every mode's page follows the same layout**, so once you've used one you
can use them all:

1. **Geometry tab** — pick a lattice family from a combobox and set the
   geometry's size/shape (e.g. number of unit cells, island radius, ribbon
   width). This defines the atomic positions the Hamiltonian will be built
   on.
2. **Modify geometry tab** — optionally remove atoms interactively to sculpt
   a shape (see [Modifying the geometry](#modifying-the-geometry)).
3. **Terms in the Hamiltonian tab** — one form field per physical term
   (hopping, exchange field, spin-orbit coupling, pairing, ...), each with a
   rendered formula and a hover tooltip explaining its physical meaning. A
   term set to `0.0` (the default) is simply absent from the Hamiltonian, so
   you only need to touch the fields relevant to what you're studying — a
   field currently set away from `0.0` shows its text in **bold**, so you
   can tell which terms are actually active at a glance without checking
   every field. If
   the mode supports mean-field interactions, this area is itself split into
   two sub-tabs, "Single particle" and "Many-body interactions" — see
   [Self-consistent mean-field calculations](#self-consistent-mean-field-scf-calculations).
   A third sub-tab, **"pyqula code"** (currently in the Islands/Ribbons/Sheets
   modes), shows the equivalent `pyqula` Python script for the terms you've
   set — only the terms currently away from their default `0.0` are listed,
   so it stays a short, clean recipe rather than a dump of every possible
   term. It updates automatically whenever you switch to it (or press
   Refresh), and a Copy button puts the script on your clipboard to paste
   into your own script outside the GUI. If mean-field interactions are
   switched on, the self-consistent solve is included too, and any atoms
   removed on the "Modify geometry" tab are included as well.
4. **Calculation tabs** — one tab per kind of result: Structure, Bands, DOS,
   LDOS, Fermi surface, QPI, Topology, Magnetism, Sweep, ... Each has its own
   button(s) ("Show bands", "Show DOS", ...) plus any options specific to
   that calculation (energy window, k-mesh density, which operator to
   project onto). Most buttons also show the rendered formula for the
   quantity they compute, next to the button, with the same hover tooltip as
   the button itself. Pressing a button runs the calculation and opens a plot
   window with the result; the main window stays responsive.

A progress bar appears in the page's status area while a calculation is
running. Hovering over any field, formula image, or calculation button shows
a short tooltip explaining what it does — when in doubt, hover before you
click.

## A typical workflow

1. Pick a mode from the sidebar (e.g. **Sheets** for a bulk 2D lattice).
2. On the **Geometry** tab, choose a lattice family (e.g. Honeycomb) and set
   the geometry size.
3. On the **Terms in the Hamiltonian** tab, set the physical parameters you
   want (e.g. a hopping amplitude, and an exchange field or spin-orbit term
   if you want to break some symmetry). Leave everything else at `0.0`.
4. Go to the **Bands** tab and click **Show bands** to see the band
   structure with these parameters. A plot window opens; close it and adjust
   parameters to try again, or move to another calculation tab.
5. Try other calculation tabs as needed — **DOS**, **Fermi surface**,
   **Topology** (Chern number, Z2 invariant, Berry curvature), etc. — all
   using the same Hamiltonian you just defined.
6. If you're interested in interaction-driven physics (magnetism, charge
   order), switch on mean-field interactions — see the SCF section below —
   before computing bands/DOS/etc., so those calculations use the
   self-consistent Hamiltonian instead of the bare one.
7. Use **Save results** (present on most modes) to keep a copy of your
   inputs and outputs before changing parameters further — see
   [Saving and loading your work](#saving-and-loading-your-work).

Changing any parameter after computing a result does not retroactively
change an already-open plot — it only affects the *next* calculation you
run.

## Modifying the geometry

On the **Modify geometry** tab, **Select atoms to remove** opens an
interactive picker on the current geometry: click atoms to mark them, then
confirm to rebuild the geometry/Hamiltonian without them. This is how you
sculpt a shape by hand (e.g. carve a notch into an island, or cut a hole in
a sheet) rather than relying only on the presets in the Geometry tab. The
selection is remembered and re-applied automatically the next time this
mode's Hamiltonian is (re)built, so you don't need to redo it after tweaking
an unrelated Hamiltonian term.

## Hamiltonian type: Spinless, Spinful, Nambu

The same modes that have the SCF switch below (see the next section) also
have a **Hamiltonian type** dropdown just above it, at the bottom of the
"Terms in the Hamiltonian" area: **Spinless**, **Spinful** (the default),
or **Nambu**.

- **Spinful** is the ordinary case: the Hamiltonian carries a real electron
  spin degree of freedom, and every spin-dependent term is available.
- **Spinless** removes the spin degree of freedom entirely. Terms that only
  make sense with real spin — Exchange, Kane-Mele SOC, Anti-Kane-Mele,
  Rashba, Antiferromagnetism, and the mean-field J1/J2/J3 exchange fields —
  are hidden and have no effect while Spinless is selected, even if they
  still hold a nonzero value from before you switched. Orbital terms
  (hopping, Fermi level, sublattice imbalance, Haldane/Anti-Haldane,
  crystal field, Peierls/in-plane field, strain, and the U/V1/V2 mean-field
  terms) stay available either way.
- **Nambu** adds an electron-hole (Bogoliubov-de Gennes) sector on top of a
  spinful Hamiltonian, and is the only choice that shows and activates the
  s-wave/p-wave pairing fields — those are hidden under Spinless and
  Spinful, since pairing has no meaning without the Nambu doubling.

Switching this dropdown immediately shows/hides the affected fields, the
same way changing **Lattice** shows/hides Haldane/Kane-Mele/valley terms —
if a term is both lattice-restricted and Hamiltonian-type-restricted (Kane-
Mele SOC, Anti-Kane-Mele, Antiferromagnetism), it stays hidden unless both
the current lattice *and* the current Hamiltonian type allow it. The SCF
tab's **Initial guess** dropdown (see below) is filtered the same way — a
guess tied to a hidden term (e.g. **rashba**, **kanemele**, **swave**) isn't
offered while that term itself is hidden.

## Self-consistent mean-field (SCF) calculations

Modes that support interactions (Islands, Ribbons, Sheets, 3D crystals,
multilayer graphene, hybrid ribbons/films, and films) have a switch at the
bottom of the "Terms in the Hamiltonian" area, next to the "Single
particle"/"Many-body interactions" sub-tabs (below the Hamiltonian type
dropdown described above). The **Many-body interactions**
sub-tab has density-density (U, V1, V2) and spin-spin (J1, J2, J3) fields —
see the [term reference](#reference-hamiltonian-terms) for what each one
means physically.

- The switch starts off. As soon as you set any of the six interaction
  fields away from `0.0`, it turns on automatically — you never have to
  remember to flip it. If you turn it off by hand, though, it stays off
  until you turn it back on yourself.
- With the switch on, a **Solve SCF** button on the SCF tab runs the
  mean-field loop to convergence. You normally don't have to press this
  yourself: any calculation button (bands, DOS, ...) will silently (re-)run
  the SCF loop first if nothing has been solved yet, or if any
  Hamiltonian-affecting parameter changed since the last solve. Pressing
  **Solve SCF** yourself is mainly useful if you want to inspect the SCF
  tab's own convergence output before running anything else, or if your
  mode's Solve SCF button computes extra diagnostics (e.g. automatic
  identification of the resulting symmetry-broken state) that plain
  calculation buttons don't trigger.
- With the switch off, calculations always use the bare (non-interacting)
  Hamiltonian, regardless of what's in the U/V/J fields.
- The SCF tab's **Initial guess** dropdown picks the seed the mean-field
  loop starts iterating from — a poor initial guess can converge to a
  different, possibly metastable, self-consistent solution instead of the
  one you're after. Its list of options is not fixed: it always offers
  **random** (a generic random seed, valid for any Hamiltonian) plus one
  guess per single-particle term this mode/lattice combination actually
  has available, so switching **Lattice** updates it immediately — e.g. a
  **Haldane**/**kanemele**/**antihaldane** guess only appears on a
  honeycomb-derived lattice (plain honeycomb, multilayer/twisted graphene,
  hyperhoneycomb, ...), and **antiferro**/**imbalance** only on a lattice
  with more than one sublattice (those plus Lieb/Diamond). If your current
  selection stops being offered after a lattice change, it falls back to
  the first available option instead of silently keeping an invalid guess.
- The SCF tab's **Solver** dropdown picks the iterative algorithm used to
  converge the mean field: **linear_mixing** (the default) is the classical
  fixed-point mixing scheme, **error_gradient** instead minimizes the
  self-consistency residual directly and can be more robust on systems
  where linear mixing struggles to converge, and **krylov** uses a
  Newton-Krylov root finder, which can converge in fewer iterations on
  larger systems at the cost of a more expensive step. This choice only
  applies to a normal-state (non-superconducting) Hamiltonian, and needs
  the `jax` package that the installer sets up automatically; with
  s-wave/p-wave pairing turned on, or if jax could not be installed on your
  system, Solve SCF silently uses its previous fixed-mixing behavior
  regardless of what's selected here.
- **Max iterations** caps how many SCF steps are attempted before giving up
  (default `100`); a run that hits this limit without converging prints a
  warning instead of raising an error, and you'll see the (unconverged)
  result of whatever iteration it stopped at.

## Saving and loading your work

Each button click runs in a scratch folder that is discarded when you close
the app, so results are not kept automatically. Where a mode has one, the
**Save results** button copies everything computed since your last
parameter change — plus a snapshot of every field/combobox/checkbox value —
into a folder created next to wherever you launched `quantum-lattice` from.
You'll be prompted for a name (defaulting to `QL_save`); pick a new name
each time to keep multiple results side by side instead of overwriting the
previous one. **Load results** prompts you to pick among the saved folders
found there and restores that folder's `interface.json` back into the form
fields (values only — it does not replay the calculations themselves).

## While a calculation is running

Only one calculation can run at a time across the whole application, even
if you switch to a different mode's page while it runs. If you click a
button while another is still running, you'll see a "Please wait" message
instead of the calculation starting — wait for the current one to finish
(or its plot window to appear) and try again.

A **Cancel calculation** button at the bottom of the sidebar stops a
running calculation outright, if it's one of the kinds that support this
(currently: Ribbons' "Solve SCF" button — more will gain this over time).
Clicking it while nothing cancellable is running (either
nothing is running at all, or it's a calculation that doesn't support
cancellation yet) shows a "Nothing to cancel" message and does nothing
else. A cancelled calculation is reported the same way a finished one is
(an info message instead of an error), and any partial result is discarded
rather than left half-written — the next calculation you run starts clean,
as if the cancelled one had never happened.

If a calculation fails (e.g. an invalid parameter combination), you'll see
an error message in the window itself rather than a silent failure, even
when the app was launched from a desktop icon with no terminal attached.

**Serial vs. parallel execution.** A **Parallel execution** switch at the
bottom of the sidebar controls whether calculations use a single CPU core
(serial, the default) or all available cores (parallel). It applies to
every mode — there is one switch for the whole application, not one per
mode. Leave it off on a shared machine to avoid tying up every core; turn
it on for a faster single-user run of anything CPU-heavy (large k-point
meshes, big geometries). Changes take effect on the next calculation you
run, with no restart needed.

## Reference: Hamiltonian terms

Every term below appears as a form field on the modes that support it, with
a rendered formula and this same explanation as its hover tooltip. A term
left at its default (`0.0`) is not included in the Hamiltonian. On the
modes with a [Hamiltonian type](#hamiltonian-type-spinless-spinful-nambu)
dropdown, Exchange/Kane-Mele/Anti-Kane-Mele/Rashba/Antiferromagnetism/J1/
J2/J3 are additionally hidden under Spinless, and s-wave/p-wave pairing are
hidden unless Nambu is selected.

| Term | What it does |
|---|---|
| Hopping (`hopping`) | Sets the amplitude t_ij for electrons to tunnel between neighboring orbitals — the kinetic-energy term that turns otherwise isolated atomic levels into dispersive bands. Larger hopping gives wider bands and stronger electron delocalization. |
| Fermi energy (`fermi`) | Shifts the Fermi (chemical potential) energy, controlling how many electron states below it are filled. Equivalent to doping the system away from half filling, without changing the bands themselves. |
| Exchange field (`exchange`) | A Zeeman-like exchange field (Jx,Jy,Jz) that couples to the electron spin, favoring alignment along its direction. Splits spin-up and spin-down bands. |
| Haldane (`haldane`) | A complex second-neighbor hopping that breaks time-reversal symmetry with zero net flux (Haldane model). Opens a topological gap and can produce a Chern insulator. |
| Kane-Mele (`kanemele`) | Intrinsic spin-orbit coupling acting like a Haldane term with opposite sign per spin, preserving time-reversal symmetry. Opens a quantum-spin-Hall gap with counter-propagating spin-polarized edge states. |
| Anti-Haldane (`antihaldane`) | A staggered Haldane coupling that flips sign between the two valleys instead of sharing one chirality. Used to probe valley-contrasting physics such as valley Hall effects. |
| Anti-Kane-Mele (`antikanemele`) | A staggered analogue of Kane-Mele spin-orbit coupling, opposite sign between valleys/sublattices. For valley- or sublattice-selective spin-orbit physics beyond standard QSH. |
| Sublattice imbalance (`mAB`) | A staggered onsite potential raising one sublattice and lowering the other, breaking inversion symmetry. On honeycomb this opens a trivial mass gap at the Dirac points (as in hBN). |
| Antiferromagnetism (`mAF`) | A staggered (Néel) magnetic order pointing electron spins oppositely on the two sublattices — an antiferromagnetic mean-field state with zero net magnetization. |
| s-wave pairing (`swave`) | An onsite superconducting pairing amplitude pairing opposite-spin electrons on the same site, as in conventional BCS superconductivity. Opens a gap via electron-hole (BdG) mixing. |
| p-wave pairing (`pwave`) | A spin-triplet pairing amplitude pairing same-spin electrons on neighboring sites (odd-parity order). Can support topological superconductivity and Majorana bound states. |
| Rashba spin-orbit (`rashba`) | Spin-orbit coupling from broken inversion symmetry perpendicular to the lattice plane. Locks electron spin to momentum direction, splitting bands of opposite spin helicity. |
| Kondo coupling (`kondo`) | The exchange coupling J_K between a localized (f-electron) moment and itinerant conduction-electron spin — the defining interaction of the Kondo/heavy-fermion problem. |
| Localized exchange (`kexchange`) | An exchange coupling between neighboring localized magnetic moments, distinct from Kondo coupling. Sets the strength of direct/RKKY-mediated magnetic interactions between them. |
| Impurity exchange (`exchange_impurity`) | A Zeeman-like field applied only at the embedded impurity site, polarizing its spin independently of the host. Models a magnetic impurity in a non-magnetic host. |
| Impurity onsite energy (`fermi_impurity`) | An onsite energy shift applied only at the impurity site, detuning its level relative to the host bands and controlling its occupation/resonance position. |
| Hubbard U (`U`) | The local (onsite) repulsion between two opposite-spin electrons in the same orbital. Drives mean-field magnetism (e.g. Néel order) and Mott-insulating behavior at strong coupling. |
| First-neighbor V (`V1`) | A density-density interaction between first-neighbor sites. Together with U, can stabilize charge-ordered/charge-density-wave states. |
| Second-neighbor V (`V2`) | A density-density interaction between second-neighbor sites, a longer-range extension of U/V1. |
| First-neighbor J (`J1`) | Heisenberg exchange J(S_i·S_j) between first-neighbor localized spins (J>0 antiferromagnetic, J<0 ferromagnetic). Usually the leading magnetic interaction. |
| Second-neighbor J (`J2`) | Second-neighbor Heisenberg exchange. Competition with J1 (frustration) can favor non-collinear, incommensurate, or spiral order. |
| Third-neighbor J (`J3`) | Third-neighbor Heisenberg exchange, typically weaker but able to further stabilize or frustrate a given magnetic pattern. |
| Crystal field (`crystalfield`) | An onsite potential shaped by the lattice geometry (e.g. layer/stacking position), used to model a substrate potential or interlayer stacking asymmetry. |
| Peierls field (`peierls`) | An orbital magnetic field via Peierls substitution, threading flux through the lattice's loops. Can generate Landau levels and Hofstadter-butterfly-like spectra. |
| In-plane B field (`inplaneb`) | An in-plane orbital magnetic field entering as a Peierls phase depending on out-of-plane extent — the relevant field geometry for thin films/slabs. |
| Interlayer hopping (`interlayer`) | Hopping amplitude between vertically stacked layers, decaying with distance from direct vertical alignment. Controls band splitting/hybridization between layers. |
| Twisted interlayer hopping (`tinter`) | Interlayer hopping between twisted layers (Slater-Koster-like distance decay). Together with the twist/commensuration index, sets the moiré bandwidth (including the flat-band regime near the magic angle). |
| Interlayer bias (`bias` / `interlayer_bias`) | A perpendicular electric field shifting onsite energies linearly with height, detuning layers relative to each other. Breaks interlayer inversion symmetry, can open/tune a gap. |
| Ising spin-orbit coupling (`ising_SOC`) | Ising-type SOC pinning spin out of plane with a sign tied to valley index, as in monolayer TMDCs. Locks spin and valley together, suppressing intra-valley spin-flip scattering. |
| Charge density wave (`cdw`) | A charge-density-wave order parameter modulating onsite energy periodically with wavevector Q (as in NbSe2), reflecting a translational-symmetry-breaking instability. |
| Strain (`strain`) | A local modification of hopping along a specific bond direction, mimicking mechanical strain — e.g. to probe strain-induced pseudo-magnetic fields in honeycomb lattices. |

## Reference: calculation buttons

Most buttons below also show a rendered formula next to them in the app, with
this same explanation as its hover tooltip - buttons that only pick/view
something rather than computing a physical quantity (Select atoms to remove,
Save results, ...) don't.

| Button | What it computes |
|---|---|
| Show bands | Diagonalizes the Hamiltonian along a k-path through the Brillouin zone and plots the band structure (optionally colored by an operator's expectation value). |
| Show DOS | Computes the density of states (k-space integration or kernel polynomial method), optionally projected onto an operator. |
| Show KDOS | Computes the k-resolved density of states along a path — useful for visualizing surface/edge states. |
| Show DOS-bands | Computes the DOS resolved along the band-structure path (a smeared version of the bands). |
| Show IETS QDOS | Momentum-resolved inelastic tunneling spectroscopy: the RPA spin-excitation response along a q-path, showing the magnon/spin-wave-like dispersion of the converged magnetic state. Needs SCF solved first (mean field with an onsite interaction). 1D/2D/3D modes only. |
| Show IETS LDOS | Real-space inelastic tunneling spectroscopy across a sweep of energies: opens an interactive viewer (energy slider) showing the spatial map at that energy next to the total (site-summed) IETS vs energy - the same style of viewer as Show multi-energy LDOS. Needs SCF solved first (mean field with an onsite interaction). Islands (0D) only. |
| Show Berry curvature (1D) | Berry curvature along a 1D Brillouin-zone path — the same quantity as the 2D map below, evaluated along a path instead of over a mesh; used to diagnose 1D topological invariants such as edge polarization. |
| Show Berry curvature (2D) | Berry curvature over a 2D Brillouin-zone mesh, plotted as a map. |
| Show Z2 | The Z2 topological invariant via the Wannier charge center (Vanderbilt) method — trivial vs. quantum-spin-Hall insulator. |
| Show Chern number | Integrates the Berry curvature over the Brillouin zone to give the (quantized anomalous Hall) Chern number. |
| Show Fermi surface | Diagonalizes on a k-mesh near chosen energies and plots the resulting constant-energy contours. |
| Show QPI | The quasiparticle interference pattern (Fourier transform of the joint DOS) — mimics STM scattering interference. |
| Show multi-energy LDOS | Local density of states at several energies, plotted spatially. |
| Show site DOS | Interactive: click a site in the geometry to compute and plot the LDOS at that site, or drag a lasso around an area to select several sites at once and plot their combined DOS. |
| Show structure (2D) | Writes the geometry and plots the lattice (atomic positions, optionally bonds). |
| Show structure (3D) | Writes the geometry and opens an interactive 3D view (atomic positions and bonds). |
| Show magnetism | Computes self-consistent or externally-set magnetic moments per site and overlays them as arrows on the geometry. |
| Solve SCF | Runs the self-consistent mean-field loop to convergence and saves the result for other calculations to use. |
| Compute sweep | Repeats a calculation while sweeping one parameter over a range, collecting results into one sweep plot. |
| Select atoms to remove | Interactive picker: click atoms to mark them, then rebuilds the geometry/Hamiltonian without them. |
| Show hoppings | Writes the hopping matrix elements and plots them as a network showing bond connectivity/strength. |
| Show local Chern marker | A real-space-resolved Chern marker per site — useful for finite/disordered systems without a well-defined k-space Chern number. |
| Show time evolution | Time-evolves a wavepacket started on a chosen atom and plots how its weight spreads through the system. |
| Select time-evolution atom | Interactive picker to choose the atom the time-evolution wavepacket starts on. |
| Show edge DOS | DOS projected onto the boundary of the system, isolating edge states from the bulk. |
| Show Hofstadter butterfly | Sweeps a magnetic-flux value, recomputing the spectrum at each value, plotted as energy vs. field. |
| Select DOS atoms | Interactive picker to choose which atoms are included when computing DOS. |
| Select path / Show path | Draws (or replots) a path across the geometry with the mouse, defining the atoms used by the DOS-along-a-path calculation. |
| Show path DOS | DOS along a previously-selected path of atoms, as a function of position along the path. |
| Show eigenvalues | Diagonalizes (or KPM-estimates, for large systems) the Hamiltonian and plots the eigenvalue spectrum. |
| Show potential | Onsite potential at the edge atoms of the geometry — useful for checking boundary effects before a calculation. |
| Show spatial DOS | LDOS at each site for a set of energies via KPM — e.g. to simulate an STM topography image. |
| Show embedding LDOS | LDOS of the host lattice with an impurity embedded (Green's-function embedding), at one chosen energy. |
| Show embedding LDOS sweep | The same, swept over a range of energies. |
| Select impurity sites | Interactive picker to choose which sites an embedded impurity's terms apply to. |
| Save results | Copies this session's results into a folder you name (a new name keeps it alongside earlier saves instead of overwriting them). |
| Load results | Prompts you to pick a previously saved folder and restores its parameters back into the form fields. |
| Show configuration | Lattice gas only: plots the occupied/empty sites of the last annealed configuration over the lattice — anneals automatically first (a fresh random occupation at the requested filling, searched for its lowest-energy arrangement via Metropolis swaps) if no anneal has run yet or a parameter has changed since. |
| Show relaxation | Lattice gas only: steps through occupation snapshots recorded at intervals during the last anneal (from the initial random configuration to the final one) via a slider, alongside the energy trace with a marker showing the current step. |
| Show correlator relaxation | Lattice gas only: steps through the anneal via a slider, showing the energy trace (marked at the current step) alongside — for a 2D lattice — the reciprocal-space structure factor S(q) at that step, or — for the Chain lattice, which has no meaningful S(q) — the neighbor-shell density-density correlator instead. |
| Show configuration (Ising) | Ising model only: plots the up/down spins of the last annealed configuration over the lattice — anneals automatically first (a fresh random spin configuration at the requested initial magnetization, relaxed via single-spin-flip Metropolis dynamics) if no anneal has run yet or a parameter has changed since. |
| Show relaxation (Ising) | Ising model only: steps through spin-configuration snapshots recorded at intervals during the last anneal (from the initial random configuration to the final one) via a slider, alongside the energy and total-magnetization traces with a marker showing the current step. |
| Show correlator relaxation (Ising) | Ising model only: steps through the anneal via a slider, showing the energy/magnetization traces (marked at the current step) alongside — for a 2D lattice — the reciprocal-space structure factor S(q) at that step, or — for the Chain lattice — the neighbor-shell spin-spin correlator instead. |

## Reference: modes

### Multidimensional models

These four are the general-purpose building blocks; every other mode is a
variation on one of them.

- **Islands (0D)** — a finite flake cut to a polygon (choose the number of
  edges and a rotation) from a 2D lattice (Chain, Honeycomb, Square, Kagome,
  Lieb, Triangular, plus pre-cut zigzag/armchair honeycomb ribbons).
  Supports interactive single-atom time evolution, a real-space (local)
  Chern-number map, and (after SCF) a real-space IETS LDOS sweep - an
  energy-slider viewer showing the spatial map next to the total IETS vs
  energy, in the same style as Show multi-energy LDOS - in addition to the standard
  calculations. Has SCF.
- **Ribbons (1D)** — infinite in one direction: intrinsically-1D lattices
  (Chain, Bichain) used directly, or 2D lattices cut to a chosen width.
  Adds an interactive band-LDOS view (click a point on the bands, see that
  eigenstate's spatial density), an edge-DOS button, and (after SCF) an
  IETS QDOS view. Has SCF.
- **Sheets (2D)** — a bulk 2D periodic lattice (Honeycomb and several
  variants, Square, Kagome, Lieb, Triangular and variants). Adds a general
  parameter-sweep tool, an explicit pairing-symmetry selector for the
  s-wave term, and (after SCF) an IETS QDOS view. Has the richest SCF
  support (U/V1/V2/J1/J2/J3 with automatic symmetry-breaking
  identification).
- **3D crystals** — a bulk 3D periodic lattice (Cubic, Diamond, Pyrochlore,
  Hyperhoneycomb). Adds a bond-strain field, 3D-native views (slab-style
  LDOS heatmap, Z2 invariant, Berry curvature map), and (after SCF) an IETS
  QDOS view. Has SCF.

### Van der Waals

- **Multilayer graphene** — a stack of honeycomb layers along z; the
  "lattice" combobox picks a stacking sequence (e.g. "ABA") rather than a
  lattice family. Adds interlayer hopping/bias and an in-plane B field. Has
  SCF.
- **Twisted multilayer graphene** — moiré structures; a combobox picks among
  bilayer/trilayer/tetralayer stacking and twist configurations, sized by an
  integer commensuration index rather than a literal angle in degrees. DOS
  and site-DOS are KPM-only (moiré cells are large), with an optional
  multi-core toggle. No SCF.
- **Transition metal dichalcogenides** — not a generic lattice builder: a
  fixed NbSe2 Hamiltonian, with Ising spin-orbit coupling and CDW strength
  as the structural knobs instead of a lattice choice. Adds a 3D magnetism
  viewer alongside the usual 2D one. No SCF.
- **Huge islands** — a large-island geometry engine with three ways to build
  the shape: a polygon "recipe" (like Islands), loading a positions file, or
  tracing a bitmap image into an island outline, plus an iterative
  target-diameter solver. All spectral calculations are KPM-based since
  islands here can be very large. No SCF.

### Embedded impurities

- **Single impurities (ribbon / sheet)** — an otherwise-plain 1D or 2D host
  lattice with a point impurity embedded via a Green's-function technique
  (no full-supercell rebuild). An interactive picker selects which site(s)
  get the impurity; impurity onsite energy and exchange fields apply only
  there. Uses dedicated embedding-LDOS buttons (single-energy and
  energy-sweep) instead of the standard DOS/bands buttons. No SCF.

### Hybrid systems

- **Hybrid ribbons / films** — a ribbon or film split into 2 or more
  independently-parametrized spatial parts (e.g. "Upper"/"Lower"), each with
  its own copy of the usual single-particle terms, interpolated spatially
  across the structure. Useful for e.g. a bilayer where the two layers
  should have different fields. Has SCF.

### Misc

- **Hofstadter butterflies** — a ribbon/bilayer-graphene geometry with a
  magnetic-flux sweep as its defining calculation: the Hamiltonian is
  rebuilt at each field value in a range and plotted as energy vs. field.
  No SCF.
- **Heavy fermion Kondo lattice** — the same conduction-electron lattice
  choices as Islands, promoted to a two-band conduction + localized
  f-electron Kondo-lattice Hamiltonian via the Kondo and localized-exchange
  couplings. No SCF.
- **Films** — a finite-thickness slab cut from a 3D lattice (Cubic,
  Diamond, Pyrochlore, Hyperhoneycomb). Adds the same strain mechanic as 3D
  crystals, plus surface-sensitive KDOS/slab-LDOS views. Has SCF.

### Classical models

- **Lattice gas** — not a quantum tight-binding model: a classical,
  occupation-based model of particles (e.g. adsorbates or vacancies) sitting
  on a fixed fraction of the sites of a lattice (Chain, Square, Triangular,
  Honeycomb, Kagome, Lieb), repelling or attracting their neighbors through a
  real-space coupling. Set the lattice, patch size (Supercell size), and
  **Filling** (fraction of occupied sites) in the Geometry tab; the
  neighbor couplings **J1/J2/J3** (positive = repulsive, negative =
  attractive) and an optional position-dependent **chemical potential
  profile** in the Interactions tab; and the Metropolis **Temperature**,
  **Number of attempts**, and **Number of snapshots** used to search for a
  low-energy configuration in the Anneal settings tab. There is no
  separate "run" step — clicking any Show button below anneals
  automatically first if it hasn't run yet, or if you've changed a
  parameter since the last anneal, starting from a fresh random
  configuration at the requested filling and searching for its
  lowest-energy arrangement, recording **Number of snapshots** occupation
  snapshots at evenly-spaced points along the way; a click that finds
  nothing has changed just reuses the existing results instead. **Show
  configuration** then visualizes the final occupation map, and **Show
  relaxation** steps through every recorded occupation snapshot via a
  slider (with the energy trajectory alongside, marked at the current
  step). **Show correlator relaxation** is a further exception — its own
  data (the neighbor-shell correlator, or for a 2D lattice the
  reciprocal-space structure factor S(q), at every recorded snapshot,
  shown next to the energy trace) is only computed when you click that
  specific button, not as part of the anneal itself, so expect a short
  extra wait the first time you click it for a given anneal — later
  clicks replot the same computed frames instantly. **Load Results**
  restores a saved anneal's parameters and results without triggering a
  fresh (and differently random) anneal on your next click — as long as
  you don't change a parameter first, the restored result is what **Show
  configuration** and **Show relaxation** will show you. **Show
  correlator relaxation** is the exception: its per-snapshot data was
  never part of the save, so clicking it after a Load re-runs the anneal
  anyway, replacing the loaded result (and what the other two buttons now
  show) with a new, differently random one. No SCF, no bands/DOS — none
  of the usual electronic-structure calculations apply here.

- **Ising model** — also not a quantum tight-binding model: a classical
  model of up/down spins ($\pm1$) sitting on every site of a lattice
  (Chain, Square, Triangular, Honeycomb, Kagome, Lieb), aligning or
  anti-aligning with their neighbors through a real-space exchange
  coupling and an optional external field — the same classical-anneal
  mechanic as Lattice gas, applied to spins instead of occupations. Set
  the lattice, patch size (Supercell size), and **Initial magnetization**
  (average spin, $-1$ to $1$, used only to build the random starting
  configuration) in the Geometry tab; the neighbor couplings **J1/J2/J3**
  (positive = ferromagnetic/aligning, negative = antiferromagnetic — the
  opposite sign convention from Lattice gas's couplings) and an optional
  position-dependent **external field profile** in the Interactions tab;
  and the Metropolis **Temperature**, **Number of attempts**, and
  **Number of snapshots** in the Anneal settings tab. As with Lattice gas,
  there is no separate "run" step: clicking any Show button anneals
  automatically first if needed, starting from a fresh random spin
  configuration at the requested initial magnetization and relaxing it
  via single-spin-flip Metropolis dynamics (magnetization is **not**
  conserved during this relaxation — unlike Lattice gas's fixed filling,
  it's free to drift toward whichever value the field and couplings
  favor), recording **Number of snapshots** spin snapshots at
  evenly-spaced points along the way. **Show configuration** visualizes
  the final spin map, and **Show relaxation** steps through every
  recorded snapshot via a slider, alongside the energy and total
  magnetization trajectories (marked at the current step). **Show
  correlator relaxation** works the same way as Lattice gas's — its
  neighbor-shell spin correlator (or, for a 2D lattice, the
  reciprocal-space structure factor S(q)) is only computed the first time
  you click it for a given anneal, so expect a short extra wait then, not
  on later clicks. **Load Results** and the same anneal-freshness/Load
  interaction described above for Lattice gas apply here too. No SCF, no
  bands/DOS.

## Updating the application

The bottom of the sidebar has an **Update Quantum Lattice** entry that pulls
the latest version of the application from its source and restarts it. This
updates the app itself, not the physics parameters or results in your
current session — save any results you want to keep first.

## Troubleshooting

- **Nothing happens when I click a calculation button.** Check the status
  area for a progress bar — another calculation (possibly on a different
  page) may still be running; only one runs at a time application-wide. If
  you see a "Please wait" message, that's why.
- **A calculation failed.** An error message appears in the window itself.
  Common causes are parameter combinations pyqula itself rejects (e.g. an
  empty geometry after removing too many atoms) — check the values you just
  changed.
- **I want to compare two parameter sets.** Use **Save results** before
  changing parameters, giving it a distinct name each time — **Load
  results** lets you pick which saved folder to bring back later.
- **My SCF calculation seems to be reusing an old result.** It shouldn't —
  any Hamiltonian-affecting change automatically invalidates the cached SCF
  solution, so the next calculation re-solves it. If you suspect otherwise,
  press **Solve SCF** yourself to force a fresh solve.
- **I need a calculation not covered here.** Check
  `pysrc/pyqula_user_guide.md` for what the underlying pyqula library
  supports beyond what's currently exposed in the interface.
