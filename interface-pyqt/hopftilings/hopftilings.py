#!/usr/bin/env python3

from __future__ import print_function

import sys
import os

# main path
qlroot = os.path.dirname(os.path.realpath(__file__))+"/../.."
sys.path.append(qlroot+"/pysrc/") # python libraries
sys.path.append(qlroot+"/extras/") # the standalone scripts this mode wraps

from interfacetk import qtwrap # import the library with simple wrappers to Qt
get = qtwrap.get  # get the value of a certain variable
getbox = qtwrap.getbox  # get the value of a certain variable
window = qtwrap.new_page(os.path.dirname(os.path.realpath(__file__))) # this mode's page

from interfacetk.ql_interface import * # import all the libraries needed
from interfacetk import common # common routines for all the geometries

common.initialize(qtwrap) # do several common initializations

# This mode has no Hamiltonian that the shared pickup_hamiltonian()/STANDARD_HANDLERS machinery could use: every button launches
# utilities/ql-extras.py, which computes with extras/ql_*.py and plots (see that script's docstring for why it does not read .OUT files)

HOPPING = {"Unit": "unit", "Inverse length": "inverse", "Gaussian": "gauss"}
KIND = {"Spectre": "spectre", "Hat": "hat", "Turtle": "turtle"}
LINE = {"Axis": "axis", "Body diagonal": "diag"}


def _int(name,lo,hi):
    v = int(round(get(name)))
    if not lo<=v<=hi: raise ValueError("%s must be between %d and %d (got %d)" % (name,lo,hi,v))
    return v


def _need_spectre():
    """Tilings and Chair44 lines come from the Spectre repository; point extras/ql_tilings.py at it, or fail with a clear message."""
    d = get("spectre_dir",string=True).strip()
    if d: os.environ["SPECTRE_DIR"] = os.path.expanduser(d)
    import ql_tilings
    ql_tilings.refresh() # re-reads SPECTRE_DIR
    if not ql_tilings.available():
        raise RuntimeError("Spectre repository not found: set its folder in the Tiling tab "
                "(a clone of github.com/brentharts/spectre)")


def show_hopf_invariant():
    execute_script("ql-extras.py hopf-invariant --h %g" % get("hopf_h"))


def show_hopf_gap():
    execute_script("ql-extras.py hopf-gap --hmax %g" % max(4.5,abs(get("hopf_h"))+0.5))


def show_hopf_slab():
    execute_script("ql-extras.py hopf-slab --h %g --layers %d" % (get("hopf_h"),_int("hopf_layers",4,40)))


def show_tiling():
    _need_spectre()
    execute_script("ql-extras.py tiling --kind %s --level %d" % (KIND[getbox("tiling_kind")],_int("tiling_level",1,3)))


def show_tiling_spectrum():
    _need_spectre()
    execute_script("ql-extras.py tiling-spectrum --kind %s --level %d --hopping %s" % (KIND[getbox("tiling_kind")],
        _int("tiling_level",1,3),HOPPING[getbox("tiling_hopping")]))


def show_chair44_chain():
    _need_spectre()
    execute_script("ql-extras.py chair44-chain --line %s --depth %d --lam %g --nlines %d" % (LINE[getbox("chain_line")],
        _int("chain_depth",6,16),get("chain_lambda"),_int("chain_nlines",1,40)))


signals = {
  "show_hopf_invariant": show_hopf_invariant,
  "show_hopf_gap": show_hopf_gap,
  "show_hopf_slab": show_hopf_slab,
  "show_tiling": show_tiling,
  "show_tiling_spectrum": show_tiling_spectrum,
  "show_chair44_chain": show_chair44_chain,
}

inipath = os.getcwd() # get the initial directory, before common.finalize_page()'s create_folder() chdirs away
common.finalize_page(qtwrap,window,signals,inipath,robust=False)

if __name__ == "__main__":
    window.run() # show this page as its own standalone window and block
