#!/usr/bin/env python3
"""Headless sanity check for every interface-pyqt/<mode> module.

There is no automated test suite for this repo (see CLAUDE.md) - normally
each mode is verified by launching it and clicking around. This script
gives a fast, scriptable first pass so refactors of the shared toolkit
(pysrc/interfacetk/) can be checked across all modes at once, before doing
the real manual GUI pass. It does not replace that manual pass; it only
catches import errors and wiring mistakes.

Two checks per mode, plus one for the shell:
  1. static  - every QPushButton in interface.ui has a matching entry in
               the module's `signals` dict: either an explicit
               signals["x"] = ... / extra={"x": ...} entry, or one of the
               button names auto-wired by a shared helper the module calls
               (common.wire_standard_signals's STANDARD_HANDLERS, or
               common.finalize_page's save_results/load_results).
               Regex-based, no code execution.
  2. dynamic - `python <mode>.py` (run standalone, its own top-level
               window) builds and reaches the blocking event loop without
               raising, i.e. it is still alive after a short timeout with
               nothing on stderr. Runs under QT_QPA_PLATFORM=offscreen so
               no real display is needed.
  3. shell   - bin/versions/quantum-lattice-pyqt (the single-process
               FluentWindow shell every mode is normally reached through)
               builds its initially-shown page (the rest load lazily on
               first navigation) and reaches the blocking event loop
               without raising. Checked once, not per-mode.

Usage:
    python tools/smoke_test.py            # check all modes + the shell
    python tools/smoke_test.py 2d 1d      # check specific modes only (no shell check)
"""
import os
import re
import subprocess
import sys

import PySide6

QLROOT = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/..")

# Modes wired into the shell (bin/versions/quantum-lattice-pyqt's MODES
# list) - keep in sync with that file.
MODES = [
    "2d", "hybridfilm", "tbg", "1d", "0d", "2dslab", "hybridribbon",
    "hofstader1d", "3d", "heavyfermion", "huge_0d", "multilayergraphene",
    "impurity_embedding", "tmdc", "ribbon_embedding", "latticegas",
    "latticeising",
]

ALIVE_TIMEOUT = 6  # seconds a healthy GUI should stay up (blocked in app.exec())
SHELL_ALIVE_TIMEOUT = 10  # the shell only builds its initially-shown page up
                          # front (the rest are lazy, see _LazyPage in
                          # bin/versions/quantum-lattice-pyqt), so it reaches
                          # the event loop about as fast as a single mode does

# Buttons pysrc/interfacetk/common.py's wire_standard_signals() auto-wires
# for any mode that calls it - keep in sync with common.STANDARD_HANDLERS
AUTO_WIRED_BUTTONS = {
    "show_bands", "show_dos", "show_kdos", "show_dosbands", "show_berry1d",
    "show_berry2d", "show_z2", "show_chern", "show_fermi_surface",
    "show_qpi", "show_multildos", "show_site_dos",
    "show_iets_qdos", "show_iets_ldos",
}

# Buttons pysrc/interfacetk/common.py's finalize_page() auto-wires (if the
# page has them) for any mode that calls it in its footer
FINALIZE_PAGE_BUTTONS = {"save_results", "load_results"}


def _spec_buttons(moddir):
    """Button names of a declaratively-built page (one whose interface.py
    is a formbuilder spec rather than pyside6-uic output - see
    pysrc/interfacetk/formbuilder.py). Returns None if this mode doesn't
    use one. Unlike the interface.ui path this imports the module, which
    is safe: a spec module only builds plain dicts at import time."""
    import importlib.util
    path = os.path.join(moddir, "interface.py")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        if "formbuilder" not in f.read():
            return None
    pysrc = os.path.join(QLROOT, "pysrc")
    if pysrc not in sys.path:
        sys.path.insert(0, pysrc)
    spec_ = importlib.util.spec_from_file_location("specui_" + os.path.basename(moddir), path)
    mod = importlib.util.module_from_spec(spec_)
    spec_.loader.exec_module(mod)
    names = set(n for n, _text in mod.SPEC["footer"])
    for side in ("left", "right"):
        for t in mod.SPEC[side]:
            for row in t["rows"]:
                if row["kind"] == "buttons":
                    names |= set(n for n, _text in row["buttons"])
    return names


def check_signal_wiring(mode):
    """Static check: every button the page defines has a signals[...] entry.

    Buttons come from interface.ui for a Designer-built mode, or from the
    formbuilder spec in interface.py for a declaratively-built one."""
    moddir = os.path.join(QLROOT, "interface-pyqt", mode)
    ui_path = os.path.join(moddir, "interface.ui")
    py_path = os.path.join(moddir, mode + ".py")
    spec_buttons = _spec_buttons(moddir)
    if not os.path.exists(py_path):
        return [f"{mode}: missing {mode}.py"]
    if spec_buttons is None and not os.path.exists(ui_path):
        return [f"{mode}: no interface.ui and no formbuilder spec in interface.py"]
    ui_text = ""
    if os.path.exists(ui_path):
        with open(ui_path) as f: ui_text = f.read()
    with open(py_path) as f: py_text = f.read()
    # strip '#' comments per line so commented-out wiring isn't counted as live
    py_text = "\n".join(line.split("#", 1)[0] for line in py_text.splitlines())
    # QPushButton in an unpromoted .ui, or PushButton after the qfluentwidgets
    # "promote to..." widget swap (see CLAUDE.md's Per-module structure)
    buttons = set(re.findall(r'<widget class="(?:Q?PushButton)" name="([a-zA-Z_0-9]+)"', ui_text))
    if spec_buttons is not None:
        buttons |= spec_buttons
    wired = set(re.findall(r'signals\["([a-zA-Z_0-9]+)"\]', py_text))
    wired |= set(re.findall(r'"([a-zA-Z_0-9]+)"\s*:', py_text))  # extra={"x": ...} dict-literal keys
    if "wire_standard_signals(" in py_text:
        wired |= AUTO_WIRED_BUTTONS
    if "finalize_page(" in py_text:
        wired |= FINALIZE_PAGE_BUTTONS
    missing = sorted(buttons - wired)
    if missing:
        return [f"{mode}: button(s) with no signals[] handler: {', '.join(missing)}"]
    return []


def _offscreen_env():
    env = dict(os.environ)
    env["QT_QPA_PLATFORM"] = "offscreen"
    # some setups don't auto-discover PySide6's bundled Qt plugins otherwise
    plugin_dir = os.path.join(os.path.dirname(PySide6.__file__), "Qt", "plugins", "platforms")
    if os.path.isdir(plugin_dir):
        env["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_dir
    return env


def _check_stays_alive(cmd, cwd, timeout, label):
    """Run cmd; healthy means it's still blocked in app.exec() after
    `timeout` seconds with nothing on stderr, not that it exits cleanly."""
    proc = subprocess.Popen(
        cmd, cwd=cwd,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env=_offscreen_env(), text=True,
    )
    try:
        out, err = proc.communicate(timeout=timeout)
        if proc.returncode != 0 or err.strip():
            tail = err.strip().splitlines()[-8:]
            return [f"{label}: crashed (exit {proc.returncode}): " + " | ".join(tail)]
        return [f"{label}: exited cleanly before reaching the event loop (unexpected)"]
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        return []  # still alive after the timeout = healthy


def check_launches(mode):
    """Dynamic check: the mode script, run standalone, builds its own
    top-level window and blocks without crashing."""
    moddir = os.path.join(QLROOT, "interface-pyqt", mode)
    script = os.path.join(moddir, mode + ".py")
    if not os.path.exists(script):
        return [f"{mode}: {script} not found"]
    return _check_stays_alive([sys.executable, script, QLROOT], moddir, ALIVE_TIMEOUT, mode)


def check_shell():
    """Dynamic check: the shell builds every mode as a page and blocks
    without crashing."""
    script = os.path.join(QLROOT, "bin", "versions", "quantum-lattice-pyqt")
    if not os.path.exists(script):
        return ["shell: bin/versions/quantum-lattice-pyqt not found"]
    return _check_stays_alive([sys.executable, script], QLROOT, SHELL_ALIVE_TIMEOUT, "shell")


def main():
    explicit_modes = bool(sys.argv[1:])
    modes = sys.argv[1:] or MODES
    failures = []
    for mode in modes:
        print(f"checking {mode} ...", flush=True)
        failures += check_signal_wiring(mode)
        failures += check_launches(mode)
    if not explicit_modes:
        print("checking shell ...", flush=True)
        failures += check_shell()
    print()
    if failures:
        print(f"FAILED ({len(failures)}):")
        for f in failures:
            print(" -", f)
        sys.exit(1)
    print(f"OK: {len(modes)} module(s) passed" + ("" if explicit_modes else " + shell"))


if __name__ == "__main__":
    main()
