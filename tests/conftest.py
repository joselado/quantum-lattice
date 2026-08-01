"""Shared pytest setup: headless Qt platform + the same sys.path bootstrap
every <mode>.py relies on (see CLAUDE.md's "Entry point chain"), done once
here so individual test modules don't have to repeat it. Must run before
PySide6 is imported anywhere in the process, which is why QT_QPA_PLATFORM is
set at collection time (conftest.py is imported before test modules)."""
import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

QLROOT = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
TOOLS_DIR = os.path.join(QLROOT, "tools")
PYSRC_DIR = os.path.join(QLROOT, "pysrc")

for p in (PYSRC_DIR, TOOLS_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)
