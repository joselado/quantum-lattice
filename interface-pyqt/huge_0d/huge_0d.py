#!/usr/bin/env python3

from __future__ import print_function

import sys
import os

# main path
qlroot = os.path.dirname(os.path.realpath(__file__))+"/../.."
sys.path.append(qlroot+"/pysrc/") # python libraries


from interfacetk import qtwrap # import the library with simple wrappaers to qt4
get = qtwrap.get  # get the value of a certain variable
getbox = qtwrap.getbox  # get the value of a certain variable
window = qtwrap.main() # this is the main interface

from interfacetk.qh_interface import * # import all the libraries needed

import islandbuild
import handlers


inipath = os.getcwd() # get the initial directory

def initialize():  handlers.initialize(qtwrap)
def show_ldos():  handlers.show_ldos(qtwrap)
def show_full_spectrum():  handlers.show_full_spectrum()
def show_dos():  handlers.show_dos(qtwrap)
def show_spatial_dos():  handlers.show_spatial_dos(qtwrap)
def show_potential():  handlers.show_potential(qtwrap)
def show_lattice():  handlers.show_lattice(qtwrap)
def show_path_dos():  handlers.show_path_dos(qtwrap)
def show_path():  handlers.show_path(qtwrap)
def show_eigenvalues():  handlers.show_eigenvalues(qtwrap)
def clear_removal():  handlers.clear_removal()
def select_atoms():  handlers.select_atoms()
def select_atoms_dos():  handlers.select_atoms_dos()

def save_results():  save_state(inipath,tmppath,window) # function to save
def load_results():  load_state(inipath,tmppath,window) # function to load


# create signals
signals = dict()
signals["initialize"] = initialize  # initialize and run
signals["show_ldos"] = show_ldos  # show LDOS
signals["show_dos"] = show_dos  # show DOS
signals["show_spatial_dos"] = show_spatial_dos  # show DOS
signals["show_lattice"] = show_lattice  # show magnetism
#signals["show_full_spectrum"] = show_full_spectrum  # show all the eigenvalues
signals["show_path"] = show_path  # show the path
signals["show_eigenvalues"] = show_eigenvalues  # show the path
signals["show_path_dos"] = show_path_dos  # show the path
signals["show_potential"] = show_potential  # show the potential added
signals["save_results"] = save_results  # save the results
signals["load_results"] = load_results  # load the results
#signals["clear_removal"] = clear_removal  # clear the file
#signals["select_atoms"] = select_atoms  # select_atoms
signals["select_atoms_dos"] = select_atoms_dos  # select_atoms



window.connect_clicks(signals)
folder = create_folder()
tmppath = os.getcwd() # get the initial directory
initialize() # do it once
window.run()
