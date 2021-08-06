## QUANTUM LATTICE ##

# Aim #

This program allows to perform tight binding calculations with a user friendly interface
![Alt text](screenshots/quantum_lattice.png?raw=true "Quantum Lattice System selection")


# How to install #

## Linux and Mac ##

The program runs in Linux and Mac machines. 

Clone the github repository
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
instructions. Alternatively, you can try
[this version](https://github.com/TheGreatFox/quantum-lattice) 
that was adapted for a Windows system (latest updates may not be included in
it).

# Examples
This program allows to study a variety of electronic states by means of tight binding models as shown below.

## Quantum anomalous Hall state
Honeycomb lattice with Rashba spin-orbit coupling and exchange field, giving rise to a net Chern number and chiral edge states
https://journals.aps.org/prb/abstract/10.1103/PhysRevB.82.161414
![Alt text](screenshots/qah.png?raw=true "QAH state")


## Quantum Spin Hall state
Honeycomb lattice with Kane-Mele spin-orbit coupling and Rashba spin-orbit coupling, giving rise to a gapped spectra with a non-trivial Z2 invariant and helical edge states https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.95.226801
![Alt text](screenshots/qsh.png?raw=true "QSH state")

## Magnetism in graphene zigzag nanoribbons
Self-consistent mean field calculation of a zigzag graphene ribbon, with electronic interactions included as a mean field Hubbard model. Interactions give rise to an edge magnetization in the ribbon, with an antiferromagnetic alignment between edges
![Alt text](screenshots/zzscf.png?raw=true "Magnetism in zigzag nanoribbons")


## Nodal line semimetals
Band structure of a slab of a 3D nodal line semimetal in a diamond lattice, showing the emergence of topological zero energy drumhead states in the surface of the slab https://link.springer.com/article/10.1007%2Fs10909-017-1846-3
![Alt text](screenshots/nodalline.png?raw=true "Magnetism in zigzag nanoribbons")


## Confined modes in 0D systems
Spectra and spatially resolved density of states of a triangular graphene island, showing the emergence of confined modes
![Alt text](screenshots/island.png?raw=true "Confined modes in a graphene island")


## Colossal graphene quantum dots
Density of states and spatially resolved density of states of a bg graphene quantum dot. The huge islands module uses special techniques to efficiently solve systems with hundreds of thousands of atoms.
![Alt text](screenshots/giant_island.png?raw=true "Big graphene island")



## Landau levels
Electronic spectra of a massive honeycomb lattice in the presence of an off-plane magnetic field, giving rise to Landau levels and chiral edge states
![Alt text](screenshots/zzqh.png?raw=true "Landau levels in a massive zigzag honeycomb ribbon")


## Artificial topological superconductors
Bogoliuvov de Gennes band structructure of a two-dimensional gas in a square lattice with Rashba spin-orbit coupling, off-plane exchange field and s-wave superconducting proximity effect. When superconductivity is turned on, a gap opens up in the spectra hosting a non-trivial Chern number, giving rise to propagating Majorana modes in the system
![Alt text](screenshots/topologicalSC.png?raw=true "Artificial topological superconductor in a square lattice")


## Quantum Valley Hall effect
Band structure of Bernal stacked bilayer graphene, showing the emergence of a gap when an interlayer bias is applied. The previous gap hosts a non-trivial valley Chern number, giving rise to the emergence of pseudo-helical states in the edge of the system
![Alt text](screenshots/qvh.png?raw=true "Quantum valley Hall state in biased bilayer AB graphene")


## Twisted bilayer graphene
Bandstructure and local density of states of twisted bilayer graphene at the magic angle, showing the emergence of a flat band, with an associated triangular density of states
https://journals.aps.org/prb/abstract/10.1103/PhysRevB.82.121407
![Alt text](screenshots/tbg.png?raw=true "Magic angle twisted bilayer graphene")

# Capabilities #
- Tight binding models in different lattices (triangular, square, honeycomb, Kagome, Lieb, diamond, pyrochlore)
- Possibility of crafting your own lattice interactively
- Tunable parameters in the Hamiltonian (Fermi energy, magnetic order, sublattice imbalance, magnetic field,  Rashba spin-orbit coupling, intrinsic spin-orbit coupling, Haldane coupling, anti-Haldane coupling, s-wave superconductivity)
- Different results are automatically plotted from the interface
- Band structure of 0d,1d,2d systems
- Density of states of 0d,1d,2d systems
- Selfconsistent mean-field Hubbard calculations of 0d,1d,2d systems
- Berry curvature, Chern number and Z2 invariant in 2d systems
- Special module to deal with systems with more than 100000 atoms using the Kernel polynomial method
- Special modules to study 1d and 2d study interfaces between different systems
- Special module for single impurities in pristine infinite systems using the embedding technique

