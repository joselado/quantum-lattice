"""Physical-meaning tooltips for Hamiltonian terms, shared across every mode.

Kept as its own module (rather than living inline in common.py) so it can be
imported both by common.py:set_formulas() (which shows these as hover text
next to a term's formula image and its form field) and by scfterms.py (which
builds the U/V1/V2/J1/J2/J3 fields for modes, e.g. 3d/2dslab/multilayergraphene,
that never call set_formulas() at all) without either module depending on the
other. This also leaves room to grow TERM_TOOLTIPS[term] into
TERM_TOOLTIPS[term][lang] for multi-language support later without touching
any caller.

Whenever a new term is added to a mode's interface (see the "Hamiltonian-term
formulas" convention in CLAUDE.md), add its tooltip here too.
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
"bfield": "An orbital magnetic field applied via Peierls substitution, threading flux through the lattice's loops rather than just coupling to spin. It can generate Landau levels and, at rational flux fractions, Hofstadter-butterfly-like band structures.",
"kondo": "The exchange coupling J_K between a localized (e.g. f-electron) magnetic moment and the spin of itinerant conduction electrons - the defining interaction of the Kondo/heavy-fermion problem. It screens the local moment and gives rise to the emergent heavy quasiparticle bands.",
"kexchange": "An exchange coupling between neighboring localized magnetic moments, distinct from the conduction-electron Kondo coupling above. It sets the strength of direct or RKKY-mediated magnetic interactions between the localized moments, controlling whether they order magnetically.",
"cf": "The crystal-field splitting that lifts the degeneracy of otherwise equivalent localized orbital levels (e.g. f-orbitals) due to the symmetry of their local environment. It sets the energy separation between crystal-field-split levels entering the low-energy heavy-fermion physics.",
"exchange_impurity": "A Zeeman-like exchange field applied only at the embedded impurity site, polarizing its local spin independently of the host lattice. It models a magnetic impurity coupled to a non-magnetic host via Green's-function embedding.",
"fermi_impurity": "An onsite energy shift applied only at the impurity site, detuning its level position relative to the host band structure. It controls the impurity's occupation and its resonance position relative to the Fermi level.",
"U": "The local (onsite) Hubbard repulsion between two opposite-spin electrons occupying the same orbital. It is the basic interaction driving mean-field magnetism (e.g. Neel order) and Mott-insulating behavior at strong coupling.",
"V1": "A density-density interaction between electrons on first-neighbor sites, extending the Hubbard model beyond purely local repulsion. Together with U it can stabilize charge-ordered or charge-density-wave states when strong enough.",
"V2": "A density-density interaction between electrons on second-neighbor sites, a longer-range extension of the Hubbard/V1 terms. It helps stabilize charge-order patterns that a purely local or first-neighbor interaction alone cannot capture.",
"J1": "A first-neighbor Heisenberg exchange coupling between localized spins, J(S_i . S_j), with J>0 antiferromagnetic and J<0 ferromagnetic. It is usually the leading magnetic interaction setting collinear or non-collinear spin order on the lattice.",
"J2": "A second-neighbor Heisenberg exchange coupling, adding a longer-range magnetic interaction on top of J1. Competition between J1 and J2 (frustration) can favor non-collinear, incommensurate, or spiral magnetic order instead of simple Neel order.",
"J3": "A third-neighbor Heisenberg exchange coupling, the next magnetic interaction shell beyond J1 and J2. It is typically weaker but can further stabilize or frustrate a given magnetic ordering pattern depending on the lattice geometry.",
}
