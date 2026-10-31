# Aperiodic tilings as pyqula geometries (extras/)

Scripts: `ql_tilings.py` (geometry), `ql_tiling_spectra.py` (spectra), `ql_chair44_chains.py` (1D chains). Needs the
[spectre](https://github.com/brentharts/spectre) repo (`SPECTRE_DIR` or a sibling clone). Labels as in `HOPF_INSULATOR.md`.

![Tiling spectra](screenshots/tiling_spectra.png?raw=true "Spectra, density of states and IPR of Hat, Spectre and Turtle tight-binding models")

*Figure: `cd extras; python3 ql_tiling_spectra.py --png ../screenshots/tiling_spectra.png`.*

## Geometry
Hat, Spectre and Turtle patches (levels of the supertile inflation) become point sets and pyqula `Geometry` objects.
Checks (**Counted**): Euler V−E+F=1 (level 3: V=3734, E=4292, F=559), vertex degrees {2,3,4}, vertex graphs bipartite.
Hat, Spectre and Turtle have **identical vertex graphs** (**Exact**, combinatorics of Tile(a,b)); they differ only in edge lengths.

## Spectra (level 3, 3734 sites)
| model | result |
|---|---|
| unit hopping, all three tilings | identical: E ∈ [−2.434, 2.434], no zero modes, N·IPR 14.7 |
| hopping ∝ 1/length | Hat [−2.133, 2.133] N·IPR 82.4; Turtle [−1.965, 1.965] N·IPR 57.7 |
| Chair44 cells, depth 3 (3584 cells) | E ∈ [−5.864, 5.864], N·IPR 3.5 (≈ extended cube), no zero modes |
Spectre N·IPR vs size: 78→3.1, 518→6.4, 3734→14.7. Three points; no scaling law claimed.

## Chair44 pyramid-height chains (reported as measured)
Onsite energy λ·pyramid/36 ∈ {−λ,0,λ} along a line of the depth-14 Chair44 (16384 cells), 12 random lines, λ = 1, versus the same line shuffled.
| line | max \|partial sum\| (median) | Lyapunov (E = 0.3, 1.0) | N·IPR (4096 sites) |
|---|---|---|---|
| axis, tiling | 1 | 0.039 ± 0.061 | 12.8 ± 20.5 |
| axis, shuffled | 42 | 0.046 ± 0.038 | 350 ± 230 |
| diagonal, tiling | 3072 | 0.031 ± 0.025 | 4.2 ± 1.4 |
| diagonal, shuffled | 3072 | 0.032 ± 0.014 | 323 ± 107 |
Reading: eigenstates on tiling lines are far less localised than on shuffled lines (N·IPR ≈ 4–13 vs 300+). The Lyapunov exponents at two
energies do **not** separate them within their spread, so no mobility-edge or delocalisation claim is made; the IPR difference is the finding.
The diagonal line mean is non-zero (ballistic partial sums, chair stacks; see spectre `CONNECTIONS.md` row 12) yet its states are the least localised, so the line mean alone does not decide localisation.
