#!/usr/bin/env python3
"""ql_tests.py - run the self-tests of every script in extras/ (needs numpy, scipy, matplotlib, numba, jax and the spectre repo for tilings)."""
import importlib
import sys

MODS = ["ql_hopf_insulator", "ql_berry_bundle", "ql_tilings", "ql_tiling_spectra", "ql_chair44_chains"]

if __name__ == "__main__":
    bad = []
    for m in MODS:
        print("==", m)
        if not importlib.import_module(m).run_tests():
            bad.append(m)
    print("ALL PASS" if not bad else "FAILED: %s" % bad)
    sys.exit(1 if bad else 0)
