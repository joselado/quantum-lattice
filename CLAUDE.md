# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Quantum Lattice is a PyQt5 desktop GUI for the `pyqula` tight-binding/DFT-like physics library. The GUI lets a user pick a lattice type/dimensionality, set physical parameters in form fields, and trigger `pyqula` calculations (band structures, DOS, Berry curvature, Chern numbers, self-consistent mean field, etc.), whose results are plotted by standalone plotting scripts.

`pysrc/pyqula/` is a vendored copy of the `pyqula` library, developed in a separate upstream repository. **Treat it as a black box: do not edit files under `pysrc/pyqula/`.** All work in this repo is on the interface layer that wraps it.

## Running the app

```bash
python install.py            # one-time setup: locate/pin a Python interpreter, add `quantum-lattice` to PATH, create desktop icon
python install.py --full True   # also attempt to install missing dependencies (PyQt5, scipy, numpy, numba, matplotlib, mayavi)
quantum-lattice               # launch the app (runs bin/quantum-lattice -> bin/versions/quantum-lattice-pyqt)
```

There is no test suite, linter, or build step in this repo — verification is manual: launch the app (or a single sub-module, see below) and exercise the UI.

To run a single lattice module directly instead of going through the system-selection menu:

```bash
python interface-pyqt/2d/2d.py <quantum-lattice-root>
```

(each `<mode>.py` script expects the repo root as `sys.argv`, which is how `qlroot` is passed when the system-selection menu spawns it as a subprocess).

## Architecture

### Entry point chain

1. `bin/quantum-lattice` resolves the configured Python interpreter (via `pysrc/interpreter/pycommand.py`) and execs `bin/versions/quantum-lattice-pyqt`, or runs a single utility script if `--utility` is passed.
2. `bin/versions/quantum-lattice-pyqt` opens the **system selection** window (`interface-pyqt/system_selection/`). Each button spawns the corresponding `interface-pyqt/<mode>/<mode>.py` as an independent OS subprocess (`os.system(python + " " + path + ...)`), passing `qlroot` as an argument. This is why each sub-app is its own standalone, closable window rather than a page within one process.

### Per-module structure (`interface-pyqt/<mode>/`)

Every lattice module (`0d`, `1d`, `2d`, `2dslab`, `3d`, `tbg`, `hybridfilm`, `hybridribbon`, `hofstader1d`, `heavyfermion`, `huge_0d`, `multilayergraphene`, `impurity_embedding`, `tmdc`, `system_selection`, `timer`, `quasiperiodic`) follows the same three-file pattern:

- **`interface.ui`** — Qt Designer form; the only file a human normally edits with a GUI tool.
- **`interface.py`** — auto-generated from `interface.ui` via `convert.sh` (`pyuic5 interface.ui -o interface.py`). Never hand-edit; regenerate with `convert.sh` after changing the `.ui` file.
- **`<mode>.py`** — the actual business logic: builds the geometry/Hamiltonian from the form values, defines a `signals` dict mapping UI button names to handler functions, and calls `window.connect_clicks(signals)` then `window.run()`. This is the file to edit when changing what a module *does*.

`quasiperiodic/` is the exception — it has no `interface.ui`/generated `interface.py` (not yet wired into `system_selection`'s menu).

### Shared toolkit (`pysrc/interfacetk/`)

- `qtwrap.py` — PyQt5 glue: `App` class (wraps the generated `interface.Ui_MainWindow`), `get`/`getbox`/`modify`/`is_checked`/`set_combobox`/`set_image` helpers for reading/writing form widgets by name, `connect_clicks`.
- `qlinterface.py` — imports all the `pyqula` submodules used across the GUI, plus process/IO plumbing: `create_folder()` (makes a scratch dir under `/tmp/ql-tmp-N` and chdirs into it — calculations run there so `.OUT` files don't clutter the user's directory), `save_outputs()` (copies results back to `<original dir>/QL_save/`), `execute_script()` (spawns a `utilities/ql-*` plotting script as a background subprocess against the `.OUT` files just written), `running()` (wraps a handler so a "computing..." timer window shows while it executes).
- `qh_interface.py` / `ql_interface.py` — trivial re-export shims (`from .qlinterface import *`, `from .qh_interface import *`); some modules import through these instead of `qlinterface` directly.
- `common.py` — shared business logic reused by most `<mode>.py` files: building operators from a name (`get_operator`), and computing/plotting bands, DOS, KDOS, Berry curvature/phase, Chern numbers, Fermi surfaces, QPI, magnetism, etc. by calling into `pyqula` and then `execute_script`-ing the matching `utilities/ql-*` script.
- `interfacetk.py` — `modify_geometry` (apply atom-removal/sculpting from the UI's saved selection files, shared across modules that build geometries).
- `labels.py`, `saveload.py`, `debugging.py`, `plotpyqt.py` — minor helpers (form label text, save/load interface state to JSON, an error-visibility toggle, matplotlib-in-Qt helpers).

### `utilities/` (`ql-*` scripts)

Standalone executable Python scripts, one per plot/postprocessing task (`ql-bands`, `ql-dos`, `ql-structure-bond`, `ql-berry2d`, `ql-chern-evolution`, ...). They are never imported — they're launched as separate processes by `execute_script()` against the `.OUT`/data files a `<mode>.py` handler just wrote in the scratch folder. When adding a new kind of result to visualize, the usual pattern is: write a `.OUT` file from the handler in `<mode>.py`/`common.py`, then add/extend a `ql-*` script to read and plot it.

### `pysrc/interpreter/`

`pycommand.py` resolves which Python interpreter to use (a pinned Anaconda-style distribution recorded in the git-ignored `pythoninterpreter.py`), and handles first-run dependency installation. `pythoninterpreter.py` is generated at install time and is gitignored — don't expect it to exist in a fresh checkout.

### Data flow summary

`system_selection` → spawn `<mode>.py` → user sets parameters in `interface.ui` fields → handler builds a `pyqula` geometry/Hamiltonian using `get`/`getbox` values → computation runs in a `/tmp/ql-tmp-N` scratch dir → results written as `.OUT` files → matching `utilities/ql-*` script launched in the background to plot them → (optionally) `save_outputs()` copies the scratch dir back to `QL_save/` in the original working directory.
