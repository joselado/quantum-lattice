"""Console-script entry point for the `quantum-lattice` command.

Registered by pyproject.toml via `pip install -e .`. pip always points the
installed console script at the interpreter it was installed into, so this
module can simply assume `sys.executable` has every dependency it needs -
no interpreter-detection or pinning logic required.

This is a thin shim over the existing bin/versions/quantum-lattice-pyqt
launcher; it deliberately does not restructure how the rest of the codebase
is organized/imported.
"""
import os
import sys
import subprocess


def _repo_root():
    return os.path.dirname(os.path.realpath(__file__))


def main():
    launcher = os.path.join(_repo_root(),"bin","versions","quantum-lattice-pyqt")
    subprocess.run([sys.executable,launcher])


if __name__=="__main__":
    main()
