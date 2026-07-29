#!/usr/bin/env python3
"""Bump the patch component of the version in VERSION.TXT and pyproject.toml.

Both files are kept in sync as the single source of truth for the app's
version: VERSION.TXT is read at runtime by bin/versions/quantum-lattice-pyqt
to show a version label in the app; pyproject.toml's [project].version is
packaging metadata. Run with no arguments to bump X.Y.Z -> X.Y.(Z+1).
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
VERSION_TXT = os.path.join(ROOT, "VERSION.TXT")
PYPROJECT = os.path.join(ROOT, "pyproject.toml")


def _read_version():
    with open(VERSION_TXT) as f:
        return f.read().strip()


def _bump(version):
    parts = version.split(".")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        sys.exit(f"VERSION.TXT does not hold an X.Y.Z version: {version!r}")
    major, minor, patch = parts
    return f"{major}.{minor}.{int(patch) + 1}"


def main():
    old_version = _read_version()
    new_version = _bump(old_version)

    with open(VERSION_TXT, "w") as f:
        f.write(new_version + "\n")

    with open(PYPROJECT) as f:
        pyproject_text = f.read()
    pyproject_text, count = re.subn(
        r'(?m)^version = "[^"]+"$', f'version = "{new_version}"', pyproject_text
    )
    if count != 1:
        sys.exit("Could not find a single version = \"...\" line in pyproject.toml")
    with open(PYPROJECT, "w") as f:
        f.write(pyproject_text)

    print(new_version)


if __name__ == "__main__":
    main()
