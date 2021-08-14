## QUANTUM LATTICE ##

# Summary #

This program allows to perform tight binding calculations with a user friendly interface in a variety of lattices and dimensionalities, using [pyqula](https://github.com/joselado/pyqula).

![Alt text](screenshots/quantum_lattice.png?raw=true "Quantum Lattice System selection")

# Video examples #

[Here](https://youtu.be/g2YAE9Kpd9c) 
you can see four simultaneous examples of the
usage of Quantum Lattice.

Below you can see videos showing the real-time usage of this program for
individual examples
- [Confined modes in graphene nanoislands](https://youtu.be/YFIpONVQinc)
- [Superlattices](https://youtu.be/cPx2tOFxdyI)
- [Interaction-induced magnetism](https://youtu.be/RrPWVqJ7VS4)
- [Artificial Chern insulators](https://youtu.be/zEwywwQprNY)

# How to install #

## Linux and Mac ##

The program runs in Linux and Mac machines. 

Clone the GitHub repository
```bash
git clone https://github.com/joselado/quantum-lattice
```

and execute the script install as
```bash
python install.py
```

The script will install all the required dependencies if they are not already
present for the python command used. Afterwards, you can run the program by 
executing in a terminal

```bash
quantum-lattice
```

## Windows ##

For using this program in Windows, the easiest solution is to create a virtual
machine using [Virtual Box](https://www.virtualbox.org/), installing
a version of [Ubuntu](https://releases.ubuntu.com/20.04/) 
in that virtual machine, and following the previous
instructions. 

# FUNCTIONALITIES #
## Single particle Hamiltonians ##
- Spinless, spinful and Nambu basis for orbitals
- Full non-collinear electron and Nambu formalism
- Include magnetism, spin-orbit coupling and superconductivity
- Band structures with state-resolved expectation values
- Momentum-resolved spectral functions
- Local and full operator-resolved density of states
- 0d, 1d, 2d and 3d tight binding models

## Interacting mean-field Hamiltonians ##
- Selfconsistent mean-field calculations with local/non-local interactions
- Both collinear and non-collinear formalism
- Anomalous mean-field for non-collinear superconductors
- Full selfconsistency with all Wick terms for non-collinear superconductors
- Automatic identification of order parameters for symmetry broken states

## Topological characterization ##
- Berry phases, Berry curvatures, Chern numbers and Z2 invariants
- Operator-resolved Chern numbers and Berry density

## Spectral functions ##
- Surface spectral functions for semi-infinite systems
- Single impurities in infinite systems
- Operator-resolved spectral functions

## Chebyshev kernel polynomial based-algorithms ##
- Local and full spectral functions
- Operator resolved spectral functions
- Reaching system sizes up to 1000000 atoms on a single-core laptop


# Screenshot examples #

## Unconventional superconductivity ##
Electronic band structure, Berry curvature and momentum resolved surface
spectral function of a px + ipy spin-triplet topological
superconductor with d-vector (0,0,1).
![Alt text](screenshots/chiral_superconductor.png?raw=true "Spin-triplet chiral topological superconductor")

## Interaction-driven non-collinear magnetism ##
Electronic band structure and selfconsistent local magnetization
of a square lattice with an applied Zeeman field
and local Hubbard interactions.
![Alt text](screenshots/non_collinear_scf.png?raw=true "Non-collinear magnetization with Hubbard interactions and Zeeman field")


## Superlattices ##
Electronic band structure, Fermi surface and local density of states
of a superlattice built from a defective triangular lattice
![Alt text](screenshots/2d_superlattice.png?raw=true "Triangular superlattice")


## Scanning tunnel spectroscopy of nanographene islands ##
Real space simulation of the STS spectra, using atomic-like orbitals
for a nanographene island
![Alt text](screenshots/nanographene.png?raw=true "STS nanographene")



## Kagome lattice with first and second neighbor hopping ##
Fermi surface and band structure of a two-dimensional lattice,
including both first and second neighbor hoppings. In the absence
of second neighbor hopping, the lowest band is flat. Only first
neighbor hoppings are shown in the 3D structure plot.
![Alt text](screenshots/kagome_lattice_second.png?raw=true "Kagome lattice with NN and NNN hopping")

## Interaction-induced symmetry breaking in the Lieb lattice ##
Non-interacting and interacting band structure of a two-dimensional
Lieb lattice. When repulsive 
local Hubbard interactions are included, an spontaneously
ferromagnetic state appears in the system, leading to a real-space
magnetic distribution.
![Alt text](screenshots/lieb_scf.png?raw=true "Interacting Lieb lattice")


## Artificial Chern insulators ##
Kagome lattice with Rashba spin-orbit coupling and exchange field, giving rise to a net Chern number and chiral edge states
![Alt text](screenshots/qah.png?raw=true "QAH state in the Kagome lattice")


## Two-dimensional quantum Spin Hall state ##
Honeycomb lattice with Kane-Mele spin-orbit coupling and Rashba spin-orbit coupling, giving rise to a gapped spectra with a non-trivial Z2 invariant and helical edge states https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.95.226801
![Alt text](screenshots/qsh.png?raw=true "QSH state")

## Magnetism in graphene zigzag nanoribbons ##
Self-consistent mean field calculation of a zigzag graphene ribbon, with electronic interactions included as a mean field Hubbard model. Interactions give rise to an edge magnetization in the ribbon, with an antiferromagnetic alignment between edges
![Alt text](screenshots/zzscf.png?raw=true "Magnetism in zigzag nanoribbons")


## Three-dimensional quantum spin Hall insulators ##
Three-dimensional quantum spin-Hall insulator, engineered by intrinsic
spin-orbit coupling in the diamond lattice. the top and bottom of the
slab show an emergent helical electron gas.
![Alt text](screenshots/3D_QSL.png?raw=true "3D QSH state")


## Scanning tunnel spectroscopy of graphene nanoribbons ##
Real space simulation of the STS spectra, using atomic-like orbitals
for a graphene nanoribbon 
![Alt text](screenshots/sts_nanoribbon.png?raw=true "STS graphene nanoribbon")



## Nodal line semimetals ##
Band structure of a slab of a 3D nodal line semimetal in a diamond lattice, showing the emergence of topological zero energy drumhead states in the surface of the slab https://link.springer.com/article/10.1007%2Fs10909-017-1846-3
![Alt text](screenshots/nodalline.png?raw=true "Magnetism in zigzag nanoribbons")


## Confined modes in quantum dots ##
Spectra and spatially resolved density of states of square quantum dot, showing the emergence of confined modes
![Alt text](screenshots/island.png?raw=true "Confined modes in square quantum dot")


## Colossal quantum dots ##
Density of states and spatially resolved density of states of a big graphene quantum dot. The huge islands module uses special techniques to efficiently solve systems with hundreds of thousands of atoms.
![Alt text](screenshots/giant_island.png?raw=true "Big graphene island")



## Landau levels ##
Electronic spectra of a graphene lattice in the presence of an off-plane magnetic field and antiferromagnetic order, giving rise to Landau levels and chiral edge states
![Alt text](screenshots/honeycomb_qh.png?raw=true "Landau levels in an antiferromagnetic graphene ribbon")


## Artificial topological superconductors ##
Bogoliuvov de Gennes band structure of a two-dimensional gas in a square lattice with Rashba spin-orbit coupling, off-plane exchange field and s-wave superconducting proximity effect. When superconductivity is turned on, a gap opens up in the spectra hosting a non-trivial Chern number, giving rise to propagating Majorana modes in the system
![Alt text](screenshots/topologicalSC.png?raw=true "Artificial topological superconductor in a square lattice")


## Quantum Valley Hall effect ##
Band structure of Bernal stacked bilayer graphene, showing the emergence of a gap when an interlayer bias is applied. The previous gap hosts a non-trivial valley Chern number, giving rise to the emergence of pseudo-helical states in the edge of the system
![Alt text](screenshots/qvh.png?raw=true "Quantum valley Hall state in biased bilayer AB graphene")


## Twisted bilayer graphene ##
Bandstructure and local density of states of twisted bilayer graphene at the magic angle, showing the emergence of a flat band, with an associated triangular density of states
https://journals.aps.org/prb/abstract/10.1103/PhysRevB.82.121407
![Alt text](screenshots/tbg.png?raw=true "Magic angle twisted bilayer graphene")


## Twisted trilayer graphene ##
Structure and band structure of a twisted graphene trilayer at the magic angle.
![Alt text](screenshots/TTG.png?raw=true "Twisted trilayer graphene")


