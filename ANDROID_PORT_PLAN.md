# Android port plan

Goal: a distributable Android app (Play Store / APK) other researchers can install,
built from this codebase, targeting `pysrc/pyqula` as the unchanged compute engine.

## Why this can't be a direct port

Three parts of the current stack have no path to Android at all:

- **PyQt5** has no Android backend.
- **`numba`** JIT-compiles via `llvmlite`/LLVM, which has no viable Android build.
- **PyVista/VTK** (used by the `ql-moments`/`ql-magnetism`/`ql-structure3d`/`ql-plot3d`
  utilities) would require cross-compiling VTK for Android — a project of its own.

The app's control flow also assumes a desktop multi-process OS: `system_selection`
spawns each mode as an independent `Popen` subprocess, and `execute_script()` shells
out to `ql-*` scripts against `.OUT` files written to a scratch directory. Android is
one sandboxed process per app, so this handoff pattern has to be replaced, not just
the widgets.

## Recommended architecture

**Native Android front end (Kotlin + Jetpack Compose) + embedded Python compute layer
via Chaquopy.**

Chaquopy runs a real CPython inside the Android app, so `pyqula` stays untouched (per
the "treat it as a black box" rule) and directly callable, while the UI is genuinely
native — real widgets, native charts, normal Play Store packaging — rather than a
Kivy-style "Python app that happens to run on Android," which tends to look and behave
non-native and has historically had rougher Play Store compliance.

Division of labor:

- **Kotlin/Compose** — forms replacing each `interface.ui`, navigation, native charts
  (e.g. MPAndroidChart) for bands/DOS/Berry curvature/etc.
- **Python (Chaquopy)** — a new UI-agnostic compute package that calls `pyqula`
  directly and returns arrays/dicts. No file writing, no subprocess, no
  matplotlib-as-a-subprocess. This replaces the "handler → `common.py` → `ql-*`
  script" chain with a plain function call.

## Phase 0 — feasibility spikes (go/no-go gate, do first)

1. **scipy on Chaquopy** — the single biggest risk. Stand up a bare Chaquopy project,
   install numpy+scipy, run one real `pyqula` diagonalization headless on an emulator
   or device. If scipy wheels aren't usable on Chaquopy for the target ABI, this whole
   architecture collapses back to a thin-client design (phone renders/sends params,
   a server or desktop runs `pyqula`).
2. **numba shim** — stub the `numba` module (no-op `njit`/`jit` decorators,
   `prange = range`) before `pysrc/pyqula` imports it, and see what actually breaks.
   Works only if pyqula's numba usage is simple decorators rather than deeper numba
   internals (types module, etc.).
3. **matplotlib Agg → bitmap** — render one plot to PNG bytes inside Chaquopy and
   display it in Compose, as the fallback path for anything not worth a native chart.

Do not proceed past this phase until all three spikes pass on a real device/emulator.

## Phase 1 — extract a UI-agnostic compute layer

Pull the physics logic currently smeared across each `<mode>.py` and `common.py` into
a plain Python package with no PyQt5 imports and no file-based handoff:

- `build_geometry(params) -> geometry`
- `compute_bands(geometry, params) -> arrays`
- `compute_dos(geometry, params) -> arrays`
- etc., mirroring the existing `common.get_X(h, qtwrap)` handlers but returning data
  instead of writing `.OUT` files and launching a `ql-*` script.

Mechanical but large — do it one lattice mode at a time. Start with `2d` and `0d` as
the MVP; defer `tbg`, `hybridfilm`, `hybridribbon`, `heavyfermion`,
`multilayergraphene`, `impurity_embedding`, `tmdc`, `hofstader1d`, `huge_0d`,
`quasiperiodic` until the pattern is proven.

## Phase 2 — Android shell

Build native Compose screens mirroring each `interface.ui`, wired to the Phase 1
functions via Chaquopy, with native charts fed by the returned arrays.

## Phase 3 — decide fate of 3D features

`ql-moments`, `ql-magnetism`, `ql-structure3d`, `ql-plot3d` are PyVista-only. Decide
per feature:

- drop from mobile v1,
- replace with a lightweight native 3D view (e.g. Filament/SceneView) fed atom/bond
  positions computed in Python, or
- mark as desktop-only within the app.

## Phase 4 — packaging

Signed AAB, Play Store listing, real-device testing. Chaquopy's bundled numpy/scipy
meaningfully inflate APK size and cold-start time — measure this early, not at the
end.

## Biggest open risk

Phase 0 spike 1 (scipy under Chaquopy). If it fails, fall back to a thin-client
architecture: the phone app sends parameters and displays results, while the actual
`pyqula` computation runs on a server or desktop the phone talks to over the network.
