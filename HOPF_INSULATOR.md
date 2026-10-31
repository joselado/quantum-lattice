# Hopf insulator and Berry-bundle cross-check (extras/)

Scripts: `ql_hopf_insulator.py`, `ql_berry_bundle.py`, `ql_common.py`. Run `python3 ql_tests.py` for all self-tests.
Labels: **Exact** (identity / integer check), **Counted** (numerical, finite grid), **Quoted** (from a paper, not re-derived).

![Hopf insulator](screenshots/hopf_insulator.png?raw=true "Hopf insulator: Hopf invariant versus h, gap, and slab spectrum")

*Figure: `cd extras; python3 ql_hopf_insulator.py --png ../screenshots/hopf_insulator.png`.*

## The model
A 3D two-band insulator H(k) = d(k)·σ with d = z†σz, z₁ = sin kx + i sin ky, z₂ = sin kz + i(cos kx + cos ky + cos kz + h)
(Moore–Ran–Wen, PRL 100, 186805 (2008); Deng et al., PRB 88, 201105 (2013) — **Quoted**). The Bloch Hamiltonian is turned into real-space
hoppings (FFT, `ql_common.multihopping_from_hk`) and loaded into pyqula as an ordinary `Hamiltonian`; it reproduces d·σ to 7e-15 (**Counted**).

## Results (this sign convention)
| h | Hopf invariant | status |
|---|---|---|
| \|h\| > 3 | 0 | **Counted**, three independent methods agree |
| 1 < \|h\| < 3 | −1 | same |
| \|h\| < 1 | +2 | same |
The gap closes at h = ±1, ±3. Methods: degree of φ = z/|z| : T³→S³ by an integral; signed count of preimages (Newton); Chern–Simons form in a smooth gauge.
Sign depends on orientation convention; magnitudes are the content.

## Slices and surfaces
Every kz-slice has Chern number 0 (**Counted**), so the nontrivial topology is not visible as layered Chern insulators.
Slab spectra show in-gap states (counts in the test output). Whether they are gapless protected surface bands is **not claimed**.

## Berry-bundle check
`ql_berry_bundle.py` computes the Chern number of the occupied bundle by Wilson-loop winding, gauge-free projector transport and
Fukui–Hatsugai–Suzuki, and compares with `h.get_chern()` of pyqula for Haldane, Qi–Wu–Zhang, two QWZ copies (C = 2) and Hopf slices.
All integers agree; pyqula's sign is opposite to the holonomy winding, consistently for all models (a convention, **Counted**).
Background: `HOPF_WITHOUT_PRINCIPAL_BUNDLES.md` in the HopfFibration repository.
