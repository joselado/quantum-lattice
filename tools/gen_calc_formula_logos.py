#!/usr/bin/env python3
"""Batch-generate the LaTeX formula PNGs for calculation buttons (the
show_bands/show_dos/show_chern/... family), analogous to the hand-made
Hamiltonian-term PNGs under interface-pyqt/logos/ but produced by one
reusable script instead of a one-off matplotlib snippet per image - see the
"PNG generation" discussion in the session that added this file.

Each entry in FORMULAS is a *formula*, not a button: several button names
across different modes reuse the same underlying calculation (e.g.
show_ldos/show_multildos/show_embedding_ldos/show_edge_dos are all "local
density of states via the Green's function"), and CALC_FORMULAS in
pysrc/interfacetk/termtooltips.py maps each button name to the formula key
here - so one PNG is shared by every button that needs it, the same "reuse
across modules" convention as the rest of the interface.

Regenerate after editing FORMULAS below:
    python tools/gen_calc_formula_logos.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Match the serif/italic "Computer Modern" look of the hand-made
# Hamiltonian-term PNGs (haldane.png, kanemele.png, ...) - those predate
# this script and were rendered with mathtext's "cm" fontset, whereas this
# script previously left mathtext.fontset at its "dejavusans" default,
# giving calculation-button formulas a visibly different (sans-serif)
# font from the term formulas shown right next to their parameter fields.
matplotlib.rcParams["mathtext.fontset"] = "cm"

QLROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
OUTDIR = os.path.join(QLROOT, "interface-pyqt", "logos")

# formula key -> mathtext LaTeX (matplotlib mathtext, not a full LaTeX
# install - keep to the constructs mathtext supports: no \oint, no
# \substack, etc. Checked convention/prefactors against
# pysrc/pyqula_user_guide.md and the vendored source's docstrings
# (topology.py, embedding.py, topologytk/realspace.py) where applicable,
# same as the Hamiltonian-term PNGs.
FORMULAS = {
"bands": r"$H(\mathbf{k})\,|n,\mathbf{k}\rangle = E_n(\mathbf{k})\,|n,\mathbf{k}\rangle$",
"eigenvalues": r"$\hat H\,|n\rangle = \varepsilon_n\,|n\rangle$",
"dos": r"$\rho(E)=\mathrm{Tr}\,\delta(E-\hat H) = \sum_n \delta(E-E_n)$",
"kdos": r"$\rho(\mathbf{k},E) = \mathrm{Tr}\,\delta(E-\hat H(\mathbf{k})) = \sum_n \delta(E-E_n(\mathbf{k}))$",
"ldos": r"$\rho(\mathbf{r},E) = \sum_n |\psi_n(\mathbf{r})|^2\,\delta(E-E_n)$",
"wavefunction": r"$|\psi_{n\mathbf{k}}(\mathbf{r})|^2$",
"berry_curvature": r"$\mathbf{\Omega}_n(\mathbf{k}) = \nabla_{\mathbf{k}} \times \mathbf{A}_n(\mathbf{k}),\ \ \mathbf{A}_n(\mathbf{k}) = i\langle n\mathbf{k}|\nabla_{\mathbf{k}}|n\mathbf{k}\rangle$",
"chern": r"$C = \frac{1}{2\pi}\int_{BZ} \Omega(\mathbf{k})\, d^2k$",
"local_chern": r"$C(\mathbf{r}) = -4\pi\,\mathrm{Im}\langle \mathbf{r}|\hat P\,\hat x\,\hat Q\,\hat y\,\hat P|\mathbf{r}\rangle$",
"z2": r"$\nu = N_{\mathrm{cross}}\left[\bar x_n(k_y)\right] \ \mathrm{mod}\ 2$",
"fermi_surface": r"$E_n(\mathbf{k}) = E_F$",
"qpi": r"$\mathrm{QPI}(\mathbf{q},E) = \left|\,\mathcal{F}[\rho(\mathbf{r},E)](\mathbf{q})\,\right|$",
"iets_q": r"$\mathrm{Im}\,\chi^{+-}(\mathbf{q},\omega)$",
"iets_r": r"$\mathrm{Im}\,\chi^{+-}(\mathbf{r},\omega)$",
"magnetism": r"$\langle \mathbf{S}(\mathbf{r})\rangle = \langle \Psi|\hat{\mathbf{S}}_{\mathbf{r}}|\Psi\rangle$",
"hofstadter": r"$t_{ij}\rightarrow t_{ij}\,e^{i\phi_{ij}},\ \ \phi = 2\pi\,\Phi/\Phi_0$",
"time_evolution": r"$|\psi(t)\rangle = e^{-i\hat H t/\hbar}\,|\psi(0)\rangle$",
}


def render(key, latex, fontsize=34):
    fig = plt.figure(figsize=(0.1, 0.1))
    fig.text(0, 0, latex, fontsize=fontsize, color="white")
    outpath = os.path.join(OUTDIR, "calc_" + key + ".png")
    fig.savefig(outpath, transparent=True, bbox_inches="tight", pad_inches=0.05, dpi=200)
    plt.close(fig)
    print("wrote", outpath)


if __name__ == "__main__":
    os.makedirs(OUTDIR, exist_ok=True)
    for key, latex in FORMULAS.items():
        render(key, latex)
