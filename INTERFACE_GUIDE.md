# Interface Guide

This is a practical, mechanics-level companion to `CLAUDE.md`. `CLAUDE.md`
explains the overall architecture and entry-point chain; this file exists
so that *modifying* the interface — adding a term, moving a tab, wiring a
new mode — doesn't require re-deriving structure that isn't obvious from
just reading a `.ui` file or `common.py`. It records things that were
surprising or costly to discover, so they don't have to be rediscovered.

**Keep this file up to date.** Whenever a change touches how the
interface is built or wired (a new dynamic-widget pattern, a new shared
convention in `pysrc/interfacetk/`, a newly-discovered structural quirk in
how `interface.ui` files are laid out, a new per-mode checklist item),
add or correct a section here in the same change. This is a living
maintenance doc, not a one-time snapshot.

## Quick task index

- **Add a new Hamiltonian term (with a form field) to a mode** — see
  "Adding a Hamiltonian term" below.
- **Add a new mode/lattice type** — see "Adding a mode" below.
- **Move/rename/restructure tabs** — read "The QTabWidget naming trap"
  first. It is very easy to grab the wrong `QTabWidget` by guessing an
  object name.
- **Change the mean-field (U/V1/V2/J1/J2/J3) fields** — `pysrc/interfacetk/scfterms.py`.
- **Change a term's tooltip** — `pysrc/interfacetk/termtooltips.py` (`TERM_TOOLTIPS`).
- **Restrict a term/operator to certain lattice families** — `pysrc/interfacetk/latticeterms.py`.
- **Add a new plot/postprocessing view** — write/extend a `ql-*` script
  under `utilities/`; see "Adding a ql-* script" below.

## The QTabWidget naming trap

Every mode's `interface.ui` was hand-built in Qt Designer by copy-pasting
an earlier mode, so tab structure looks uniform but the object names of
the *containing* `QTabWidget`s are not what a naive reading suggests, and
they do **not** all share one parent tab widget:

- `tabWidget` (top-level) holds only **Geometry** / **Modify geometry**.
- `tabWidget_2` holds "Terms in the Hamiltonian" (now a nested
  `QTabWidget` itself — see below) — in most modes as its only tab, but
  **not always**: in `0d` it has a sibling "Additional terms" tab too.
  Don't assume tab count/position from one mode generalizes to all six.
- `tabWidget_3` holds most of the functional tabs side by side: Structure,
  Bands, DOS, LDOS, FS, QPI, SCF, Topology, SDOS, Magnetism, Sweep, Site
  DOS, ...
- `tabWidget_4` is nested *inside* the SCF tab's page, holding "Basic" /
  "Convergence".

So "Terms in the Hamiltonian" and "SCF" look like siblings when skimming
the `.ui` XML (both nest somewhere under the same window), but they
actually live in two different `QTabWidget`s. **Never assume tab
adjacency or a shared parent from XML indentation alone.** Before writing
code that finds/moves/renames a tab, grep the *generated* `interface.py`
for the authoritative parent — `addTab`/`setTabText` calls are unambiguous:

```bash
grep -n 'setTabText(self\.tabWidget[A-Za-z_0-9]*\.indexOf' interface-pyqt/<mode>/interface.py
```

This is exactly the mistake made (and caught by testing, not by reading)
while nesting the SCF tab inside the Hamiltonian-terms tab: the first
attempt assumed both were tabs of the same `form.tabWidget` and silently
built an empty nested tab widget. `pysrc/interfacetk/scfterms.py`'s
`_nest_scf_tab()` is the corrected version and a template for this kind of
change — it hardcodes `tabWidget_2`/`tabWidget_3` because those object
names were verified consistent across all six SCF-capable modes via the
grep above, rather than searched for generically.

## Runtime dynamic-widget patterns

Three modules build/rearrange widgets in Python at runtime instead of
(or in addition to) Designer, each replacing or reparenting a whole
placeholder/page rather than editing generated code:

- **`scfterms.py`** — replaces the `scf_terms_container` placeholder
  `QWidget` (Designer already reserves its grid cell) with a real
  `QTabWidget` holding the U/V1/V2 ("Density-density") and J1/J2/J3
  ("Spin-spin") fields, then (`_nest_scf_tab`) moves the whole "SCF" tab
  page into a new inner `QTabWidget` alongside the "Terms in the
  Hamiltonian" page, renaming both to "Single particle" and "Many-body
  interactions". Called once per mode, right after `qtwrap.new_page()`,
  before `common.set_formulas()`/`connect_clicks()` — see any of
  `interface-pyqt/{0d,1d,2d,3d,2dslab,multilayergraphene}/<mode>.py`.
- **`hybridparts.py`** — grows/shrinks a `tabWidget_4`-style tab widget's
  tab count based on an `nparts` combobox (`addTab`/`removeTab`;
  `removeTab` doesn't delete the widget, so re-adding a part preserves its
  field values), and relabels Designer-built tabs "Part 1"/"Part 2" since
  their index order isn't guaranteed consistent across mode `.ui` files.
- **`latticeterms.py`** — a registry (`RESTRICTED_TERMS`) of
  lattice-family-only widgets (Haldane/Kane-Mele/valley, honeycomb-only).
  `connect(qtwrap, lambda: getbox("lattice"))` show/hides the registered
  widgets and combobox items on every lattice-combobox change. Adding a
  new geometry-restricted term is a one-line registry addition.

When a field's visibility/tab membership needs to change based on other
UI state or needs to be shared identically across many modes without
duplicating a Designer block, prefer this pattern (placeholder + runtime
build, keyed off an object name looked up via `getattr(form, name)`) over
hand-editing six near-identical `.ui` files in parallel.

## Adding a Hamiltonian term

(See `CLAUDE.md`'s `common.py` bullet for the full picture; this is the
checklist form.)

1. Add the form field to every mode's `interface.ui` that should have it
   (`tools/convert_ui.sh` after any `.ui` edit — never hand-edit
   `interface.py`).
2. Add a formula image: white-on-transparent PNG via matplotlib
   `mathtext` (`color="white", transparent=True`) under
   `interface-pyqt/logos/<term>.png`; check `pysrc/pyqula_user_guide.md`
   or the relevant vendored docstring
   (`selfconsistency/spinspin.py::VJinteraction`,
   `selfconsistency/densitydensity.py::Vinteraction`) for the exact
   convention/prefactor before writing the LaTeX. Add `<term>_image` next
   to the field in `interface.ui`, and add `<term>` to the `terms` list in
   `common.py:set_formulas()`. Only do this for modes that already use the
   image convention for other terms (`grep -l '_image' interface-pyqt/*/interface.ui`);
   leave others alone rather than adding it piecemeal.
3. Add a 2-3 sentence physical-meaning entry to `TERM_TOOLTIPS` in
   `pysrc/interfacetk/termtooltips.py` — this is required independent of
   step 2 (it's shared by both `common.py` and `scfterms.py`).
4. If the term is lattice-family-restricted, register it in
   `latticeterms.py` instead of hand-wiring show/hide logic in the mode.
5. Wire the field into whatever builds the Hamiltonian in `<mode>.py`.
6. Run `tools/smoke_test.py` (catches wiring/import mistakes, not physics
   correctness) and manually exercise the field in the running app.

## Adding a mode

Follow the three-file pattern in `CLAUDE.md`'s "Per-module structure"
section (`interface.ui`/`interface.py`/`<mode>.py`), add the mode to the
shell's `MODES` list in `bin/versions/quantum-lattice-pyqt`, and add it to
`tools/smoke_test.py`'s coverage. If it needs mean-field terms, wire
`scfterms.build(qtwrap)` right after `qtwrap.new_page()` and give its
`interface.ui` an `scf_terms_container` placeholder inside a
`gridLayout_10`-named grid, matching the six existing SCF modes — the
object names matter, they're not derived dynamically (see `scfterms.build()`'s
`container`/`grid` args).

## Retrofitting SCF onto an existing mode

Adding mean-field support to a mode that never had it (done for
`hybridribbon`/`hybridfilm`) means copying a whole "SCF" tab (`Basic`/
`Convergence` sub-tabs: `do_scf`/`solve_scf`/`scf_initialization`/
`filling_scf`/`nk_scf`/`mix_scf`/`smearing_scf`, plus the `scf_terms_container`
placeholder) from an existing SCF+formulas mode's `interface.ui` (`1d`/`2d`/`0d`)
into the target mode's `tabWidget_3`, as raw XML - Designer isn't used for
this. Two gotchas found doing it:

- **Object-name collisions.** Designer auto-names (`tab`, `tab_11`,
  `tabWidget_4`, `gridLayout_10`, `gridLayout_12`, `label_22`, `label_32`,
  ...) are very likely already used elsewhere in the target mode's own
  `interface.ui` for unrelated widgets. Two identically-named widgets in one
  `.ui` doesn't error at `pyside6-uic` time - `setupUi()` just assigns
  `self.<name>` twice and the second silently wins, leaving the first
  widget's Python handle pointing at nothing meaningful. Grep every name in
  the block you're copying against the target file first
  (`grep -c 'name="X"' interface.ui`) and rename every colliding one to
  something unique before inserting - except the names `common.py`/
  `scfterms.py` read by exact string (`do_scf`, `solve_scf`,
  `scf_initialization`, `filling_scf`, `nk_scf`, `mix_scf`, `smearing_scf`,
  `scf_terms_container`), which must stay as-is. If the target mode already
  has its own real `tabWidget_4` for something else (e.g. `hybridparts.py`'s
  per-part tabs, which default to that exact name), rename the SCF block's
  inner Basic/Convergence `QTabWidget` and pass a non-default `grid=` to
  `scfterms.build(qtwrap, grid="...")` instead of leaving the default
  `"gridLayout_10"` - same collision risk, checked the same way.
- **Missing `<customwidget>` declaration.** If the target mode never had a
  `CheckBox`-promoted widget before (`do_scf` is one), its `interface.ui`
  `<customwidgets>` block won't declare the `CheckBox`→`QCheckBox` promotion
  yet, even though other promoted types (`BodyLabel`, `ComboBox`, `LineEdit`,
  `PushButton`) are already there. `pyside6-uic` doesn't error on this - it
  emits `WriteImports::add(): Unknown Qt class CheckBox` to stderr and
  silently generates a plain `QCheckBox` instead of the styled one. Add the
  missing `<customwidget>` block (copy the pattern from any of the other four)
  and re-run `tools/convert_ui.sh` until the warning is gone.

Then wire the mode's `<mode>.py` like `1d.py`: `pickup_hamiltonian =
common.pickup_hamiltonian(qtwrap,initialize,do_scf=True)`, a `solve_scf()`
handler (`h = initialize(); common.solve_scf(h,qtwrap)`), `"solve_scf":
solve_scf` in the signals dict, and `common.set_formulas(qtwrap)` once at
the end. `common.set_formulas()` also tries every single-particle term's
`<term>_image` (`hopping_image`, `fermi_image`, ...) - if the mode doesn't
use the image convention for those (see the "Adding a Hamiltonian term"
checklist above), each one prints a harmless `"<name> label not found"` to
stderr; that's expected, not a wiring bug.

## Adding a ql-* script

`utilities/ql-*` scripts are never imported, only launched as subprocesses
by `execute_script()` against `.OUT` files a handler just wrote in the
scratch dir. Write the `.OUT` file from `<mode>.py`/`common.py`, then
add/extend a script to read and plot it (`utilities/_pv3d.py` if it's a
3D/PyVista view — import it via `sys.path.insert(0, dirname)`, same as
every other `ql-*` script finds its own directory).

## Known gotchas

- **Busy-lock signal reentrancy**: `qtwrap.py`'s `release_busy()` fires a
  synchronous same-thread signal — mutate any state that depends on "am I
  busy" *before* releasing the lock, not after, or a handler triggered by
  the release can observe stale state.
- **The QTabWidget naming trap** above — always verify tab parentage via
  generated `interface.py`, never via `.ui` XML adjacency.
