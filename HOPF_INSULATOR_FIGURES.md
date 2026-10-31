# Four new Hopf-insulator figures, in depth (extras/)

Script: `extras/ql_hopf_figures.py`. It extends `ql_hopf_insulator.py` (see `HOPF_INSULATOR.md`) and reuses its `z_of_k`, `d_of_k`, `phi_grid`,
`spectral_derivative`, `hopf_invariant_degree`. Needs numpy, scipy and matplotlib; pyqula only for one optional cross-check.

    cd extras
    python3 ql_hopf_figures.py --tests                        # 13 checks, about 4 s
    python3 ql_hopf_figures.py --png-dir ../screenshots       # writes the four PNGs, about 7 s
    python3 ql_hopf_figures.py --png-dir out --only A,D

Labels, as in `HOPF_INSULATOR.md`: **Exact** (identity or integer check), **Counted** (numerical, finite grid), **Quoted** (from a paper, not re-derived).
One more is used here: **Argued** (a short derivation given below, then checked numerically).

The model is unchanged: H(k) = d(k)·σ, d = z†σz, z₁ = sin kₓ + i sin k_y, z₂ = sin k_z + i(cos kₓ + cos k_y + cos k_z + h). Its Hopf invariant is the
degree of φ = z/|z| : T³ → S³. Sign conventions are those of `HOPF_INSULATOR.md`: H = 0 for |h| > 3, −1 for 1 < |h| < 3, +2 for |h| < 1.

| figure | file | question it answers |
|---|---|---|
| A | `screenshots/hopf_ins_figA_phase_diagram.png` | *why* are the invariants 0, −1, +2, −1, 0, and why do they jump by 1, 3, 3, 1? |
| B | `screenshots/hopf_ins_figB_degree_density.png` | where in the Brillouin zone does the winding live? |
| C | `screenshots/hopf_ins_figC_hidden_topology.png` | what is actually non-trivial, given that every 2D slice has Chern number 0? |
| D | `screenshots/hopf_ins_figD_preimage_links.png` | can the Hopf invariant be *seen* as two curves that link? |

---

## Figure A — phase diagram and the eight touching points

![phase diagram](screenshots/hopf_ins_figA_phase_diagram.png?raw=true "Hopf invariant, gap and the TRIM masses against h")

**Top.** The Hopf invariant against h. Black dots: the degree integral (1/2π²)∮det[φ, ∂ₓφ, ∂_yφ, ∂_zφ] d³k at N = 40 for 93 values of h that avoid
the gap closings by 0.0137. Orange: the closed formula derived below. The dots sit on the plateaus 0, −1, +2, −1, 0. The handful of dots between plateaus
are the grid being too coarse right next to a gap closing (there the nearest mass is 0.014, so φ varies on a scale far below the 2π/40 ≈ 0.16 grid spacing); they are
a resolution effect that shrinks with N, not an intermediate "fractional phase".

**Middle.** The bulk gap 2·min|d| on a 32³ grid (blue), and 2·min over the eight time-reversal-invariant momenta (TRIM) of mᵢ² (dotted), where
mᵢ = cos kₓ + cos k_y + cos k_z + h evaluated at the TRIM point kᵢ ∈ {0, π}³. The two curves coincide at every h plotted, i.e. the grid minimum is attained at a TRIM
point (the test is weaker: it asserts only gap_grid ≤ gap_TRIM, and exact closing at h = ±1, ±3). The gap has local maxima of exactly 2 at h = 0, ±2, where the
nearest mass is ±1, and grows without bound for |h| > 3 (about 5 at the plot edge). The plot floors the gap at 10⁻³ to stay on a log axis. **Counted.**

**Bottom.** The four distinct masses as straight lines in h, coloured by the sign of the chirality χ introduced next, with the multiplicity of each.

**The closed formula (Argued, Counted).** At a TRIM point kᵢ, z₁ = sin kₓ + i sin k_y vanishes, and writing k = kᵢ + q,

    z ≈ ( cos kₓ·qₓ + i cos k_y·q_y ,  cos k_z·q_z + i mᵢ ),

so near kᵢ the map φ = z/|z| to S³ is a local homeomorphism onto a neighbourhood of the point (0, 0, 0, ±1) (the sign of mᵢ), whose orientation is the sign of the
Jacobian determinant

    χᵢ = cos kₓ · cos k_y · cos k_z  ∈ {+1, −1}.

As h varies and mᵢ passes through zero, that neighbourhood sweeps across the equator of S³, and the degree of φ changes by χᵢ. Starting at h → +∞, where every mass is positive and
H = 0, and lowering h, each TRIM point whose mass turns negative adds its χ:

    H(h) = Σ over TRIM points i of  χᵢ · [ mᵢ(h) < 0 ].

The eight points fall into four groups:

| TRIM points | number | cos kₓ + cos k_y + cos k_z | χ | mass becomes negative at |
|---|---|---|---|---|
| Γ = (0,0,0) | 1 | +3 | +1 | h < −3 |
| X = (π,0,0) and permutations | 3 | +1 | −1 | h < −1 |
| M = (π,π,0) and permutations | 3 | −1 | +1 | h < +1 |
| R = (π,π,π) | 1 | −3 | −1 | h < +3 |

Walking h down from +∞: crossing 3 switches on R (−1) → **−1**; crossing 1 switches on the three M's (+3) → **+2**; crossing −1 switches on the three X's (−3) → **−1**;
crossing −3 switches on Γ (+1) → **0**. The multiplicities 1, 3, 3, 1 of the steps are the binomial coefficients of the three coordinates being 0 or π; they are why the
+2 phase is "three M's minus one R" and not "two of something".

**What was checked.** (i) The sign of the Jacobian determinant at each of the eight points, by finite differences, equals cos kₓ cos k_y cos k_z.
(ii) The formula equals the degree integral at 13 values of h in all five phases: −4.0 → 0, −3.4 → 0, −2.5 → −1, −2.0 → −1, −1.5 → −1, −0.5 → +2, 0.3 → +2, 0.9 → +2,
1.1 → −1, 1.8 → −1, 2.7 → −1, 3.2 → 0, 4.5 → 0. **Counted.** The local argument is the reason the formula holds; it is not a rigorous proof here (it does not treat the
global gluing), and the overall sign is a convention.

---

## Figure B — where the winding lives

![degree density](screenshots/hopf_ins_figB_degree_density.png?raw=true "Degree density accumulated over kz and integrated over ky")

**Top.** ρ(k) = det[φ, ∂ₓφ, ∂_yφ, ∂_zφ]/(2π²) integrated over a layer and accumulated along k_z, for h = 4, 2, 0.5 (N = 48). The curves end at −0.000, −1.000 and +2.000, the
Hopf invariants. For h = 2 the whole −1 is gained in a step centred on k_z = π; for h = 0.5 about +1 is gained around k_z = 0 ≡ 2π (split across the two ends of the
axis) and about +1 around k_z = π. The trivial phase h = 4 stays at zero throughout.

**Bottom.** ρ integrated over k_y, as a map in (kₓ, k_z), for h = 2 and h = 0.5, and the table of the eight TRIM points with χ and mass at h = 0.5.
- h = 2: a single negative blob at (π, π). Only R has a negative mass (−1), with χ = −1.
- h = 0.5: three positive blobs, at (0, π), (π, 0) and (π, π) in (kₓ, k_z), the last one much weaker. These are the projections of the three M points (0,π,π),
  (π,π,0) and (π,0,π), each with mass −0.5 and χ = +1. R = (π,π,π) (mass −2.5, χ = −1) projects onto the same spot (π, π) as the third M point and its negative
  density partly cancels it there, which is why that blob is weak; it is also what reduces the total from +3 to +2.

**Consistency with Figure A.** Count the TRIM points with negative mass on each k_z layer for h = 0.5: the layer k_z = π holds M, M and R, so +1 + 1 − 1 = +1;
the layer k_z = 0 holds one M, so +1. Two layers, +1 each, total +2 — which is what the cumulative curve does. For h = 2 the single R on k_z = π gives −1. The density is a smooth
function, so the steps are not exactly localised; the statement is that the step sizes agree with these sums. **Counted**, and qualitative: the test checks only that the density
integrates to the Hopf invariant (−1.0000 at h = 2, 2.0000 at h = 0.5 on a 40³ grid).

**Why it matters.** A topological invariant that jumps only when a mass changes sign is concentrated, in a precise sense, at the points where |z| is smallest. The
heat maps show that concentration directly, which the single number does not.

---

## Figure C — the topology that the slices cannot see

![hidden topology](screenshots/hopf_ins_figC_hidden_topology.png?raw=true "Chern numbers and Berry curvature of the slices")

`HOPF_INSULATOR.md` states that every k_z-slice has Chern number 0. This figure computes the Berry curvature on slices normal to **all three** axes and shows how it
can be everywhere non-trivial yet integrate to nothing.

For the two-band model the Chern number of a slice is the degree of d̂ = d/|d| on it, so the curvature is F = d̂·(∂ₐd̂ × ∂_b d̂)/(4π), with ∮F = integer. F is computed
spectrally on a 48³ grid for h = 4, 2, 0.5.

**Top left.** The Chern number of every slice (k_z solid, kₓ dashed, k_y dotted), all three h: every line lies on 0. The largest |C| over the 3 × 48 slices is
7·10⁻¹³ at h = 2, 3·10⁻¹³ at h = 4 and 4·10⁻⁷ at h = 0.5 (the sharpest curvature, hence the coarsest convergence). **Counted** — an integer, so unambiguous.

**Top middle.** The largest local value of |F|·4π on the k_z slice. It is not small, and not constant: for h = 4 it ranges from 0.44 to 4.0, for h = 0.5 from 2.3 to 16, and for
h = 2 it is **exactly 4 for every k_z**. The last is an identity. On a line (kₓ, k_y) ∈ {0, π}², z₁ vanishes, d̂ ≈ (2 z̄₁ z₂/|z₂|², −1), and F·4π = 4|cos kₓ cos k_y|/|z₂|².
On kₓ = k_y = π,

    |z₂|² = sin²k_z + (cos k_z + h − 2)² = 1 + (h − 2)² + 2(h − 2) cos k_z,

which is identically 1 at h = 2, and at h = 0.5 equals 0.25 at k_z = 0 (hence the peak 16). The test confirms 4/|z₂|² against the spectral curvature on that line for
h = 2, 0.5, 4 (relative error 2·10⁻⁵ on a 64³ grid, shrinking geometrically with N: 1.7·10⁻³, 4·10⁻⁴, 2·10⁻⁵ for N = 40, 48, 64). **Counted**, for the (π, π) line; the other three
lines follow from the same argument and are not separately tested.

**Top right.** The positive part of the flux through the slice. At k_z = π/2 it is 0.164 (h = 4), 0.547 (h = 2) and 0.966 (h = 0.5), in units of one Chern quantum, and the
negative part cancels it (the integrals over the h = 2 and h = 0.5 slices shown are −2·10⁻¹⁷ and 4·10⁻¹⁷). So a slice carries up to about one quantum of positive and one of negative
Berry flux, which cancel; the trivial phase carries the least.

**Bottom.** The curvature map on the slice k_z = π/2 for h = 2 and h = 0.5: positive (red) and negative (blue) regions with equal integrals.

**What this establishes, and what it does not.** The Hopf invariant is not a stack of Chern layers. Each slice taken alone is a map T² → S² of degree zero, and homotopy classes of
maps T² → S² are classified by the degree, so each slice is, by itself, homotopic to a constant: the non-zero local curvature above is not a topological obstruction on any one slice. What is
non-trivial is how the slices fit together as k_z runs round the circle, which is what the Chern–Simons form of the 3D Berry connection measures (computed in `HOPF_INSULATOR.md`) and what
Figure D makes geometric.

---

## Figure D — the Hopf invariant as two curves that link

![preimage links](screenshots/hopf_ins_figD_preimage_links.png?raw=true "Preimage curves of two points of S2 and their linking")

**The idea (Pontryagin–Thom, Hopf).** The preimage of a regular point b of S² under the band map d̂ : T³ → S² is a collection of closed curves in the Brillouin-zone torus. The
Hopf invariant is the linking number of the preimages of two points (**Quoted**). The curves are the pull-back by φ of the Hopf fibre over b, which is why `HopfFibration` Figure 1
(fibres link once) and Figure 4 (preimages of f_{p,q} link p·q times) are the same statement in a simpler setting: `HOPF_FIGURES.md` there.

**How the curves are obtained.** A lift (a₁, a₂) of b to S³ in *this model's* convention d = (2 Re z̄₁z₂, 2 Im z̄₁z₂, |z₁|²−|z₂|²) is a₁ = sin(el/2), a₂ = cos(el/2)·e^{+i·az} (note the conjugate
on z₁: the Hopf map of the HopfFibration repository differs by the reflection y → −y of S²). Then d̂(k) = b exactly when z(k) is a complex multiple of a, i.e.

    f(k) = a₂ z₁(k) − a₁ z₂(k) = 0        (and z ≠ 0, which holds in every gapped phase).

That is two real equations in three unknowns: a curve. It is found without any marching grid:
1. Newton (with the pseudo-inverse of the analytic 2×3 Jacobian) from the grid minima of |f| on a 40³ grid, to |f| < 10⁻¹²;
2. from each new root, predictor–corrector tracing with step 0.05 along the tangent ∇Re f × ∇Im f (a canonical orientation, fixed along the whole curve);
3. the curve is closed when it returns to its start modulo 2π; the integer vector m of the shift is its **winding** (m = 0: a contractible loop).
Every traced point satisfies d̂(k) = b to 6·10⁻¹⁵ (h = 2) and 1.2·10⁻¹⁵ (h = 0.5). **Exact** up to rounding.

**Linking in a torus.** For contractible loops, the linking number in T³ is the sum, over all lifts of the second family (shifts by 2π·s, s ∈ {−1,0,1}³), of the Gauss integral with the first.
The Gauss integral is the midpoint rule on the traced polygons (**Counted**; the individual pair values print as ±1.000 to three decimals).

**The three panels.** Base points b₁ = (el 2.0, az 0.6) and b₂ = (el 2.4, az 3.5).
- **h = 4 (trivial, H = 0).** No start point is found for either point: they appear to have no preimage. A map of degree zero need not be onto, so this is not a contradiction. **Counted**
  (a search, not a proof of emptiness).
- **h = 2 (H = −1).** One loop over each point (lengths 10.15 and 9.70); they link with Gauss integral **−1.000**; total **−1.000** = the degree integral.
- **h = 0.5 (H = +2).** Two loops over each point (lengths 14.69, 8.84 and 13.10, 7.24). Exactly two pairs link, each with **+1.000**: the first loop over b₁ with the first loop over b₂ in the same cell,
  and the second with the second after lifting the b₂ loop by one zone (2π) in the −k_z direction. Total **+2.000** = the degree integral. In the figure only the linked pairs are drawn, as lifts to ℝ³.

The signs agree with the degree integral phase by phase (−1 ↔ −1, +2 ↔ +2). That agreement is asserted in the test as a consistency between phases (both phases give the same sign relation),
not as an absolute sign convention.

**The fourth panel — a caution.** For some base points the preimage is not a set of contractible loops. At h = 0.5 and the point (el 1.6, az 0.2) it is two closed curves with windings
(−1, 1, 1) and (1, −1, −1): each wraps the zone once, in opposite directions. Their classes cancel, as they must when all slice Chern numbers are zero (Figure C), so the family bounds a surface
and a linking number exists, but it must be computed with that surface and not with the periodic-image Gauss sum used above, so the script reports no number for it. Which base points have
contractible preimages was scanned on a grid of 5 elevations × 6 azimuths:

| | el 0.8 | el 1.2 | el 1.6 | el 2.0 | el 2.4 |
|---|---|---|---|---|---|
| h = 0.5 | wrapping loops at all 6 azimuths | contractible and wrapping loops mixed | wrapping loops only | **two contractible loops** at all 6 | **two contractible loops** at all 6 |
| h = 2 | mixed: one contractible loop plus wrapping loops at 4 azimuths, wrapping loops only at 2 | one contractible loop at all 6 | one contractible loop at all 6 | one contractible loop at all 6 | one contractible loop at all 6 |

**Counted** on that grid. Base points were chosen from the contractible region; that choice is the one non-automatic step in this figure.

**Why this figure.** The Chern–Simons computation of `HOPF_INSULATOR.md` gives a number; this gives two pictures of curves in the Brillouin zone that one can see are linked. The +2 phase is not one double-wound
link but two separate links of +1, in the points tested; the number is the same, the geometry is not.

---

## Optional cross-check against pyqula

If `pyqula` and its imports (numba, jax, multiprocess) are available, the test builds the Hamiltonian through `ql_common.hamiltonian_from_hk` and checks that its bands equal ±|d| at four random k for
h = 2: largest difference 2.7·10⁻¹⁵. If any import is missing the test prints `skip pyqula cross-check` and the other 12 checks still run. `ql_hopf_insulator.py --tests` already contains a
fuller check of the pyqula Hamiltonian; this one is deliberately small.

## What is not claimed

- Surface states and slab spectra are not touched here; whether the in-gap states of `HOPF_INSULATOR.md` are gapless and protected is still **not claimed**.
- Figure A's formula explains the *values* of the invariant in each phase; it does not by itself prove that the degree integral is an integer. That follows from the degree being a degree.
- The preimage search in Figure D is local-Newton-from-grid. It can miss a very small loop, which is why "no preimage" at h = 4 is a **Counted** observation about two points.
- Overall signs (of χ, of the degree, of the linking number) depend on orientation conventions; the magnitudes and the relations between phases are the content.
