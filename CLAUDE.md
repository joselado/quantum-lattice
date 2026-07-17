# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Quantum Lattice is a PyQt5 desktop GUI for the `pyqula` tight-binding/DFT-like physics library. The GUI lets a user pick a lattice type/dimensionality, set physical parameters in form fields, and trigger `pyqula` calculations (band structures, DOS, Berry curvature, Chern numbers, self-consistent mean field, etc.), whose results are plotted by standalone plotting scripts.

`pysrc/pyqula/` is a vendored copy of the `pyqula` library, developed in a separate upstream repository. **Treat it as a black box: do not edit files under `pysrc/pyqula/`.** All work in this repo is on the interface layer that wraps it.

## Running the app

```bash
python install.py                 # checks required packages are importable by this interpreter and
                                   # pip-installs any that are missing (PyQt5, numpy, scipy, numba,
                                   # matplotlib; pyvista for the 3D utilities is best-effort/optional),
                                   # registers the `quantum-lattice` console script (pip install -e .),
                                   # and creates a Linux .desktop entry / Windows .bat launcher
python install.py --python /path/to/python   # run the install steps with a specific interpreter
                                              # instead of the one running install.py
quantum-lattice                    # launch the app; always runs under whichever interpreter it was
                                    # installed into (pip guarantees this on Linux/Mac/Windows alike)
```

There is no persisted "which Python has the right packages" pin anymore — `pysrc/interpreter/pycommand.py::get_python()` just returns `sys.executable`, since the running interpreter is always the one `pip install -e .` registered the console script into.

There is no test suite, linter, or build step in this repo — verification is manual: launch the app (or a single sub-module, see below) and exercise the UI. `tools/smoke_test.py` gives a fast, scriptable first pass across all wired modes (headless, `QT_QPA_PLATFORM=offscreen`): it checks every `QPushButton` in a mode's `interface.ui` has a wired handler, and that the mode script builds its window and reaches the event loop without crashing. Run it after touching `pysrc/interfacetk/` or any `<mode>.py`; it catches import/wiring mistakes but does not replace a manual GUI pass for actual physics correctness.

To run a single lattice module directly instead of going through the system-selection menu:

```bash
python interface-pyqt/2d/2d.py <quantum-lattice-root>
```

(each `<mode>.py` script accepts the repo root as `sys.argv[1]` for backward compatibility with how `system_selection` spawns it, but none of the current mode scripts actually read it — they all compute `qlroot` themselves from `__file__`).

## Architecture

### Entry point chain

1. The `quantum-lattice` console script (registered by `pip install -e .` via `pyproject.toml`/`quantum_lattice_launcher.py`) or, equivalently, `bin/quantum-lattice` run directly, launches `bin/versions/quantum-lattice-pyqt` as a subprocess under the current interpreter (`sys.executable`), or runs a single utility script if `--utility` is passed to `bin/quantum-lattice`.
2. `bin/versions/quantum-lattice-pyqt` opens the **system selection** window (`interface-pyqt/system_selection/`). Each button spawns the corresponding `interface-pyqt/<mode>/<mode>.py` as an independent OS subprocess (`subprocess.Popen([python, script, qlroot])`), passing `qlroot` as an argument. This is why each sub-app is its own standalone, closable window rather than a page within one process.

### Per-module structure (`interface-pyqt/<mode>/`)

Every lattice module (`0d`, `1d`, `2d`, `2dslab`, `3d`, `tbg`, `hybridfilm`, `hybridribbon`, `hofstader1d`, `heavyfermion`, `multilayergraphene`, `impurity_embedding`, `tmdc`, `system_selection`, `timer`) follows the same three-file pattern (`huge_0d` and `quasiperiodic` are exceptions, see below):

- **`interface.ui`** — Qt Designer form; the only file a human normally edits with a GUI tool.
- **`interface.py`** — auto-generated from `interface.ui` via `convert.sh` (`pyuic5 interface.ui -o interface.py`). Never hand-edit; regenerate with `convert.sh` after changing the `.ui` file.
- **`<mode>.py`** — the actual business logic: builds the geometry/Hamiltonian from the form values, defines a `signals` dict mapping UI button names to handler functions, and calls `window.connect_clicks(signals)` then `window.run()`. This is the file to edit when changing what a module *does*.

`quasiperiodic/` is the exception — it has no `interface.ui`/generated `interface.py` (not yet wired into `system_selection`'s menu).

`huge_0d/` is the other exception — its business logic is large enough (KPM-based DOS/spectral calculations, image-to-island geometry construction) that it's split across three files instead of one: `islandbuild.py` (geometry/island construction), `handlers.py` (Hamiltonian building + button handlers), and a thin `huge_0d.py` (bootstrap + signal wiring). `islandbuild.py`/`handlers.py` are plain sibling modules imported with a bare `import islandbuild`/`import handlers` — this works because Python auto-adds a script's own directory to `sys.path` when it's run as `__main__`, the same mechanism `qtwrap.py`'s bare `import interface` already relies on. Their functions take `qtwrap` as an explicit argument rather than reading module-level globals, matching the `common.py` convention.

### Shared toolkit (`pysrc/interfacetk/`)

- `qtwrap.py` — PyQt5 glue: `App` class (wraps the generated `interface.Ui_MainWindow`), `get`/`getbox`/`modify`/`is_checked`/`set_combobox`/`set_image` helpers for reading/writing form widgets by name, `connect_clicks`.
- `qlinterface.py` — imports all the `pyqula` submodules used across the GUI, plus process/IO plumbing: `create_folder()` (makes a scratch dir via `tempfile.mkdtemp()` and chdirs into it — calculations run there so `.OUT` files don't clutter the user's directory; portable to Windows, unlike the hardcoded `/tmp` this used to be), `save_outputs()` (copies results back to `<original dir>/QL_save/`), `execute_script()` (parses a command string like `"ql-bands --dim 2"` with `shlex`, then runs it as a `subprocess.Popen([python, scriptpath, *args], ...)` against the `.OUT` files just written, logging stdout/stderr to `<script>.log` in the scratch dir instead of discarding them), `running()` (wraps a handler so a "computing..." timer window shows while it executes).
- `qh_interface.py` / `ql_interface.py` — trivial re-export shims (`from .qlinterface import *`, `from .qh_interface import *`); some modules import through these instead of `qlinterface` directly.
- `common.py` — shared business logic reused by most `<mode>.py` files: building operators from a name (`get_operator`), and computing/plotting bands, DOS, KDOS, Berry curvature/phase, Chern numbers, Fermi surfaces, QPI, magnetism, etc. by calling into `pyqula` and then `execute_script`-ing the matching `utilities/ql-*` script. Also `pickup_hamiltonian`/`select_atoms_removal` (the "reload if do_scf is checked, else build fresh" / "write geometry then launch the atom-picker script" logic shared across most modes), and `STANDARD_HANDLERS`/`wire_standard_signals(qtwrap,pickup_hamiltonian,extra={...})` — a registry of button names (`show_bands`, `show_dos`, `show_chern`, ...) whose handler is nothing but `h = pickup_hamiltonian(); common.get_X(h,qtwrap)` in every mode that uses them; a `<mode>.py` only needs to list buttons whose behavior actually differs in `extra`, which always overrides the registry.
- `interfacetk.py` — `modify_geometry` (apply atom-removal/sculpting from the UI's saved selection files, shared across modules that build geometries).
- `labels.py`, `saveload.py`, `debugging.py`, `plotpyqt.py` — minor helpers (form label text, save/load interface state to JSON, an error-visibility toggle, matplotlib-in-Qt helpers).

### `utilities/` (`ql-*` scripts)

Standalone executable Python scripts, one per plot/postprocessing task (`ql-bands`, `ql-dos`, `ql-structure-bond`, `ql-berry2d`, `ql-chern-evolution`, ...). They are never imported — they're launched as separate processes by `execute_script()` against the `.OUT`/data files a `<mode>.py` handler just wrote in the scratch folder. When adding a new kind of result to visualize, the usual pattern is: write a `.OUT` file from the handler in `<mode>.py`/`common.py`, then add/extend a `ql-*` script to read and plot it.

The 3D scripts (`ql-moments`, `ql-magnetism`, `ql-structure3d`, `ql-plot3d`, `ql-pick`, ...) use **PyVista** (real VTK rendering: lighting, true spheres/tubes, interactive point picking) via the shared `utilities/_pv3d.py` helper (`new_plotter`, `add_atoms`, `add_bonds`, `add_arrows`, `add_trisurf`, `enable_point_picking`). PyVista replaced mayavi here: mayavi's own `tvtk` wrapper-generation step fails to build on newer Python, whereas PyVista installs from prebuilt wheels. `_pv3d.py` is not a `ql-*` command — it's only imported by sibling scripts via `sys.path.insert(0, dirname)`, same pattern every `ql-*` script uses to find its own directory. PyVista is an optional/best-effort dependency (see `pycommand.py`), so these scripts should fail informatively (import error) rather than silently if it's missing, not crash the whole app.

### `pysrc/interpreter/`

`pycommand.py` is the install/launch toolbox: `get_python()` returns `sys.executable`, `install_requirements()` checks each required package by trying to import it under the target interpreter and pip-installs only what's missing (pyvista and Fortran-acceleration compilation are attempted best-effort and never fail the install), `install_editable()` runs `pip install -e .` to register the `quantum-lattice` console script, `create_icon()`/`get_qh_command()` build a Linux `.desktop` entry or Windows `.bat` launcher, preferring the pip-installed script (found via `shutil.which`) since desktop launchers often run with a minimal `PATH`.

### Packaging

`pyproject.toml` + `quantum_lattice_launcher.py` (a single top-level module, not part of `pysrc/`) register the `quantum-lattice` console script via `pip install -e .`, without restructuring how the rest of the codebase is imported — everything under `pysrc/`/`interface-pyqt/` is still reached at runtime through the existing `sys.path.append(qlroot+"/pysrc/")` bootstrap, unchanged. `requirements.txt` is the source of truth for required packages; `pycommand.py::_required_packages()` reads it directly.

### Data flow summary

`system_selection` → spawn `<mode>.py` → user sets parameters in `interface.ui` fields → handler builds a `pyqula` geometry/Hamiltonian using `get`/`getbox` values → computation runs in a `tempfile.mkdtemp()` scratch dir → results written as `.OUT` files → matching `utilities/ql-*` script launched (logged, non-blocking) to plot them → (optionally) `save_outputs()` copies the scratch dir back to `QL_save/` in the original working directory.
