#!/usr/bin/env python3
"""Headless sanity check for every interface-pyqt/<mode> module.

There is no automated test suite for this repo (see CLAUDE.md) - normally
each mode is verified by launching it and clicking around. This script
gives a fast, scriptable first pass so refactors of the shared toolkit
(pysrc/interfacetk/) can be checked across all modes at once, before doing
the real manual GUI pass. It does not replace that manual pass; it only
catches import errors and wiring mistakes.

Two checks per mode:
  1. static  - every QPushButton in interface.ui has a matching entry in
               the module's `signals` dict: either an explicit
               signals["x"] = ... / extra={"x": ...} entry, or (if the
               module calls common.wire_standard_signals) one of the
               button names common.py's STANDARD_HANDLERS auto-wires.
               Regex-based, no code execution.
  2. dynamic - `python <mode>.py <qlroot>` builds its window and reaches
               the blocking event loop without raising, i.e. it is still
               alive after a short timeout with nothing on stderr. Runs
               under QT_QPA_PLATFORM=offscreen so no real display is needed.

Usage:
    python tools/smoke_test.py            # check all modes wired into system_selection
    python tools/smoke_test.py 2d 1d      # check specific modes only
"""
import os
import re
import subprocess
import sys

QLROOT = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/..")

# Modes wired into system_selection (bin/versions/quantum-lattice-pyqt's
# call_mode(...) list) - keep in sync with that file.
MODES = [
    "2d", "hybridfilm", "tbg", "1d", "0d", "2dslab", "hybridribbon",
    "hofstader1d", "3d", "heavyfermion", "huge_0d", "multilayergraphene",
    "impurity_embedding", "tmdc",
]

ALIVE_TIMEOUT = 6  # seconds a healthy GUI should stay up (blocked in app.exec_())

# Buttons pysrc/interfacetk/common.py's wire_standard_signals() auto-wires
# for any mode that calls it - keep in sync with common.STANDARD_HANDLERS
AUTO_WIRED_BUTTONS = {
    "show_bands", "show_dos", "show_kdos", "show_dosbands", "show_berry1d",
    "show_berry2d", "show_z2", "show_chern", "show_fermi_surface",
    "show_qpi", "show_multildos",
}


def check_signal_wiring(mode):
    """Static check: every QPushButton in interface.ui has a signals[...] entry."""
    moddir = os.path.join(QLROOT, "interface-pyqt", mode)
    ui_path = os.path.join(moddir, "interface.ui")
    py_path = os.path.join(moddir, mode + ".py")
    if not os.path.exists(ui_path) or not os.path.exists(py_path):
        return [f"{mode}: missing interface.ui or {mode}.py"]
    with open(ui_path) as f: ui_text = f.read()
    with open(py_path) as f: py_text = f.read()
    # strip '#' comments per line so commented-out wiring isn't counted as live
    py_text = "\n".join(line.split("#", 1)[0] for line in py_text.splitlines())
    buttons = set(re.findall(r'<widget class="QPushButton" name="([a-zA-Z_0-9]+)"', ui_text))
    wired = set(re.findall(r'signals\["([a-zA-Z_0-9]+)"\]', py_text))
    wired |= set(re.findall(r'"([a-zA-Z_0-9]+)"\s*:', py_text))  # extra={"x": ...} dict-literal keys
    if "wire_standard_signals(" in py_text:
        wired |= AUTO_WIRED_BUTTONS
    missing = sorted(buttons - wired)
    if missing:
        return [f"{mode}: button(s) with no signals[] handler: {', '.join(missing)}"]
    return []


def check_launches(mode):
    """Dynamic check: the mode script builds its window and blocks without crashing."""
    moddir = os.path.join(QLROOT, "interface-pyqt", mode)
    script = os.path.join(moddir, mode + ".py")
    if not os.path.exists(script):
        return [f"{mode}: {script} not found"]
    env = dict(os.environ)
    env["QT_QPA_PLATFORM"] = "offscreen"
    proc = subprocess.Popen(
        [sys.executable, script, QLROOT],
        cwd=moddir,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env=env, text=True,
    )
    try:
        out, err = proc.communicate(timeout=ALIVE_TIMEOUT)
        # exiting before the timeout is only ok if it was clean (rc 0, no stderr);
        # a mode window is expected to block in app.exec_() until closed
        if proc.returncode != 0 or err.strip():
            tail = err.strip().splitlines()[-8:]
            return [f"{mode}: crashed (exit {proc.returncode}): " + " | ".join(tail)]
        return [f"{mode}: exited cleanly before reaching the event loop (unexpected)"]
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        return []  # still alive after the timeout = healthy


def main():
    modes = sys.argv[1:] or MODES
    failures = []
    for mode in modes:
        print(f"checking {mode} ...", flush=True)
        failures += check_signal_wiring(mode)
        failures += check_launches(mode)
    print()
    if failures:
        print(f"FAILED ({len(failures)}):")
        for f in failures:
            print(" -", f)
        sys.exit(1)
    print(f"OK: {len(modes)} module(s) passed")


if __name__ == "__main__":
    main()
