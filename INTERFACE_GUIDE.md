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
- **Change a calculation button's tooltip** — `pysrc/interfacetk/termtooltips.py` (`BUTTON_TOOLTIPS`); see "Adding a calculation button" below.
- **Add/change a calculation button's formula image** — `pysrc/interfacetk/termtooltips.py` (`CALC_FORMULAS`) + `tools/gen_calc_formula_logos.py`; see "Adding a calculation button" below.
- **Change any other form field's tooltip** (a numeric parameter, combobox, or checkbox that isn't a Hamiltonian term or a calculation button) — `pysrc/interfacetk/termtooltips.py` (`PARAM_TOOLTIPS`); see "Tooltip conventions" below.
- **Restrict a term/operator to certain lattice families** — `pysrc/interfacetk/latticeterms.py`.
- **Restrict a term to a Hamiltonian type (Spinless/Spinful/Nambu)** — `pysrc/interfacetk/hamiltoniantype.py` (`SPIN_TERMS`/`PAIRING_TERMS`); see "Runtime dynamic-widget patterns" below.
- **Add a new plot/postprocessing view** — write/extend a `ql-*` script
  under `utilities/`; see "Adding a ql-* script" below.
- **Change how "this term is currently active" is shown** —
  `pysrc/interfacetk/termhighlight.py`.
- **Change the save/load-results naming dialogs** —
  `qtwrap.ask_save_name()`/`ask_load_name()`, called from
  `qlinterface.save_state()`/`load_state()`.
- **Change the standard `<mode>.py` footer (scratch folder, Save/Load
  Results wiring, formulas/tooltips, `connect_clicks`)** —
  `common.finalize_page()`; see "Adding a mode" below.
- **Change the "pyqula code" tab** (the read-only view of the pyqula
  script that reproduces the current Hamiltonian) — `pysrc/interfacetk/codeview.py`
  plus each mode's own `get_pyqula_code()`; see "Adding the 'pyqula code'
  tab to a mode" below.
- **Make a calculation button hard-cancellable** (run in a killable child
  process instead of in-process) — see "Hard-cancelling a calculation"
  below.
- **Run the automated test suite, or add a test for a new mode/term/button** —
  see "Testing" below.
- **See how a specific mode is wired before touching it** (which buttons
  are auto-wired vs. hand-rolled, whether it has SCF, whether it restricts
  terms by lattice family) — see "Per-mode organization map" below, so you
  don't have to re-derive it by reading all sixteen `<mode>.py` files.

## Per-mode organization map

All sixteen modern modes (everything under `interface-pyqt/` except
`quasiperiodic/`, unwired/pre-existing and not part of this architecture —
see `CLAUDE.md` — and `huge_0d/`, the one three-*module* exception, also
covered in `CLAUDE.md`) follow the shared conventions described throughout
this file and `CLAUDE.md`, but differ in *which* of those conventions they
actually use. This section is a reference map of that variation, so
checking a mode's wiring before changing it doesn't mean re-reading all
sixteen `<mode>.py` files from scratch. It reflects the codebase as of the
consistency pass that also fixed the dead code/duplication findings below
it — re-derive it (the same way it was built: grep each `<mode>.py` for
`wire_standard_signals`/`extra=`, `latticeterms.connect`, `scfterms.build`)
rather than trust it blindly once enough new modes/changes have landed
that it might have drifted.

**Signal wiring.** Every mode calls `common.wire_standard_signals(qtwrap,
pickup_hamiltonian,extra={...})` except three that build `signals` fully
by hand, because their button set (or the absence of a Hamiltonian at all)
doesn't fit the `pickup_hamiltonian`-based auto-wiring model: `hofstader1d`
(hand-rolled for historical reasons — its button set does fit the model,
it just predates consistent use of it), `impurity_embedding`/
`ribbon_embedding` (no bands/DOS/Chern/... buttons at all — only
structure, atom removal, and the three embedding-LDOS handlers), and
`latticegas`/`latticeising` (no Hamiltonian to build in the first place —
see "Adding a mode" below). For everyone else, only buttons whose behavior differs from
`common.STANDARD_HANDLERS` need an `extra={}` entry:

| Mode | `extra={}` overrides |
|---|---|
| 0d | solve_scf, show_structure, show_hoppings, show_structure_3d, show_interactive_ldos, show_magnetism, select_atoms_removal, select_atom_time_evolution, show_time_evolution, show_local_chern |
| 1d | show_structure, show_ldos, show_edge_dos, show_band_ldos, show_structure_3d, show_magnetism, solve_scf, select_atoms_removal |
| 2d | solve_scf, show_structure, show_dos, show_dosbands, show_magnetism, compute_sweep→sweep_parameter, show_structure_3d, select_atoms_removal |
| 2dslab | show_structure, show_structure_3d, show_ldos, show_magnetism, solve_scf, select_atoms_removal |
| 3d | show_structure, show_structure_3d, show_magnetism, solve_scf, select_atoms_removal |
| tbg | show_dos, show_site_dos (forced KPM — moiré cells too large for ED), show_ldos_single, show_structure, show_structure_3d, select_atoms_removal |
| hybridfilm | show_structure, show_structure_3d, show_dos, show_ldos, solve_scf, show_magnetism, select_atoms_removal |
| hybridribbon | show_structure, show_structure_3d, show_interactive_ldos, solve_scf, show_magnetism, select_atoms_removal |
| heavyfermion | show_structure, show_structure_3d, select_atoms_removal |
| multilayergraphene | solve_scf, show_structure, show_dos, show_magnetism, compute_sweep→sweep_parameter, show_structure_3d, select_atoms_removal, show_interactive_ldos |
| tmdc | show_structure, show_dos, show_structure_3d |

**`latticeterms.connect()` (honeycomb-only term hiding) + lattice family.**
Every mode with a user-selectable `lattice` combobox calls this; three
don't, because there's nothing to restrict — `tbg`/`tmdc` have no
`lattice` combobox at all (fixed geometry: `specialgeometry.
twisted_multilayer`/`specialhamiltonian.NbSe2`), and `multilayergraphene`
calls it with a constant `lambda: "Honeycomb"` instead of `getbox
("lattice")`, since its own `lattice` combobox is a stacking code
(`"ABA"`, ...) rather than a lattice-family name. `impurity_embedding`/
`ribbon_embedding` do call it (0d island / ribbon host, both
user-selectable). `latticegas`/`latticeising` don't (classical models, no
Hamiltonian-restricted terms to hide).

**SCF.** `0d`/`2dslab`/`hybridfilm`/`hybridribbon`/`multilayergraphene`
call the shared `common.solve_scf(h,qtwrap)`. `2d`/`3d` call the richer
`common.solve_scf_identify_symmetry_breaking(h,qtwrap)` instead — same
V/U/J mean-field solve, but converging on a `scf_error`-driven `maxerror`
rather than `solve_scf()`'s thermal smearing, and additionally identifying
and reporting the broken symmetry via `scf.identify_symmetry_breaking()`.
`1d` is the one mode migrated to hard-cancellable subprocess SCF (see
"Hard-cancelling a calculation" below) — its `solve_scf()` is a thin
`run_calculation_subprocess()` call, with the real math in `1d/calc.py`.
`tbg`/`hofstader1d`/`heavyfermion`/`impurity_embedding`/`ribbon_embedding`/
`tmdc`/`latticegas`/`latticeising` have no SCF at all (no `scfterms.build()`
call, no SCF tab).

**Distinctive mechanic** (one phrase each, beyond the shared conventions):

| Mode | Distinctive mechanic |
|---|---|
| 0d | finite island; time-evolution buttons, local Chern marker |
| 1d | hard-cancellable subprocess SCF (`calc.py`) |
| 2d | parameter-sweep button; richest SCF; has the "pyqula code" tab |
| 2dslab | finite-thickness slab via `films.geometry_film` before supercell |
| 3d | fully 3D bulk lattice; richer SCF mirroring 2d's |
| tbg | twist angle/stacking combos (`specialgeometry.twisted_multilayer`); forces KPM for site-DOS |
| hybridfilm | multi-part z-slab composition via `hybridparts.py` |
| hybridribbon | same `hybridparts.py` composition, along the ribbon cross-section instead of z |
| hofstader1d | Peierls-phase flux field (`peierls`); numba-typing workaround forcing `dos.dos()` over `dos.dos1d()`/`dos.dos2d()` |
| heavyfermion | `H2HFH(h,JK=kondo,J=exchange)` converts a conventional Hamiltonian into a Kondo-lattice one |
| multilayergraphene | stacking-code combobox (`"ABA"`, ...) drives `specialgeometry.multilayer_graphene` |
| impurity_embedding | `embedding.Embedding(...)` Green's-function embedding onto a 0d cluster host; no bands/DOS buttons |
| ribbon_embedding | same embedding mechanic onto a 1d ribbon host |
| tmdc | built-in `specialhamiltonian.NbSe2(...)` — no generic geometry+`get_hamiltonian()` construction at all |
| latticegas | classical occupation model, no Hamiltonian — see "Adding a mode" below |
| latticeising | classical Ising spin model, no Hamiltonian — mirrors latticegas, see "Adding a mode" below |

"pyqula code" tab (`codeview.build`): only `0d`/`1d`/`2d` have it.

The embedding-LDOS calculation (`get_impurity_matrix`/`get_embedding_ldos`/
`get_embedding_ldos_sweep`/`select_impurity_sites`/`build_embedding_hamiltonian`
in `common.py`) is shared between `impurity_embedding`/`ribbon_embedding`
even though neither goes through `wire_standard_signals()` — a mode not
using the standard auto-wiring model doesn't mean its individual
calculations can't still be factored into `common.py` the normal way; it
just means more of its `signals` dict is hand-built. `build_embedding_
hamiltonian(g,qtwrap)` covers the two modes' identical spinful
Zeeman/Rashba/AF/Kane-Mele/Haldane/swave/pwave Hamiltonian construction —
only `get_geometry()`/`LATTICES` differ between them, so their own
`initialize()` is just `return common.build_embedding_hamiltonian
(get_geometry(),qtwrap)`.

`common.get_interactive_ldos(h,qtwrap)` is the same idea for the
`window_ldos`/`nsuper_ldos`/`nk_ldos`/`ne_ldos`/`delta_ldos` interactive-
multi-LDOS convention shared by `hofstader1d`/`hybridribbon`/
`multilayergraphene`'s `show_interactive_ldos` — not the same field
convention as `get_multildos()` (`multildos_*`, used by `0d`/`huge_0d`/
`tbg`), so kept as a separate function.

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

### QTabWidget tab labels don't follow the dark/light theme on their own

Every `QTabWidget` across every mode's `interface.ui` is plain stock
`QTabWidget` - unlike `QPushButton`/`QLineEdit`/`QComboBox`/`QLabel`, it's
never promoted to a qfluentwidgets equivalent (no compatible drop-in
replacement exists to promote it *to*). A promoted widget registers
itself with qfluentwidgets' `FluentStyleSheet.apply()` machinery
(`styleSheetManager`, a `WeakKeyDictionary` in
`qfluentwidgets/common/style_sheet.py`), which is what `setTheme()`/
`updateStyleSheet()` actually iterates - an unpromoted stock widget never
registers, so `setTheme(Theme.DARK)` never touches it at all, and its tab
bar keeps native/OS-default styling regardless of theme. That collided
with `bin/versions/quantum-lattice-pyqt`'s own
`real_page.setStyleSheet("QWidget { background: transparent; }")` (set on
every mode's top-level page so the shell's dark chrome shows through
underneath it): the tab strip's native background went transparent,
letting the dark background show through, while the tab *text* stayed at
its native black - illegible in dark mode, across every mode (confirmed
via an offscreen `shell.grab()` screenshot comparison, not just by
reading the code).

The fix is `pysrc/interfacetk/qtwrap.py`'s `_restyle_tab_bars()`: a single
`QApplication`-wide `app.setStyleSheet("QTabBar::tab { color: %s; }" %
_ink_color().name())` call, wired to `qconfig.themeChanged` the same way
`_retint_theme_images()` (the Hamiltonian-term formula PNG re-tinting,
same file) is - so it applies once at startup and again on every later
flip of the shell's "Dark interface" switch. This covers every mode's
2-5 `QTabWidget`s at once with one small addition to a file every mode
already imports, without touching any `interface.ui`/`interface.py`. If a
future dark-mode legibility bug turns up in some *other* stock
(never-promoted) widget type - `QGroupBox`, `QRadioButton`, `QSpinBox`,
... - this same `app.setStyleSheet()` call in `_restyle_tab_bars()` is
the natural place to add another selector rule, not a new standalone
mechanism.

## Runtime dynamic-widget patterns

Three modules build/rearrange widgets in Python at runtime instead of
(or in addition to) Designer, each replacing or reparenting a whole
placeholder/page rather than editing generated code:

- **`scfterms.py`** — replaces the `scf_terms_container` placeholder
  `QWidget` (Designer already reserves its grid cell) with a real
  `QTabWidget` holding the U/V1/V2 ("Density-density") and J1/J2/J3
  ("Spin-spin") fields (all defaulting to `"0.0"`), then (`_nest_scf_tab`)
  moves the whole "SCF" tab page into a new inner `QTabWidget` alongside
  the "Terms in the Hamiltonian" page, renaming both to "Single particle"
  and "Many-body interactions", and wraps that inner tab widget in a
  container with a `SwitchButton` pinned to the bottom - visible
  regardless of which sub-tab is open. That switch **replaces** (and
  reuses the object name of) `interface.ui`'s Designer-authored `do_scf`
  `CheckBox`, deleting it at runtime (`_retire_old_checkbox()`) - a mode
  retrofitting SCF no longer needs a `do_scf` widget in its `interface.ui`
  at all, `scfterms.build()` builds one unconditionally. The switch starts
  off, is turned on automatically the instant one of the six interaction
  fields leaves zero (never auto-off, so a manual "off" sticks), and
  every Hamiltonian-affecting field on the page (everything except
  calculation/plotting-only tabs under `tabWidget_3` and the switch
  itself) is wired to set `form._scf_dirty = True`
  (`_connect_scf_dirty_tracking()`) - `common.pickup_hamiltonian()` reads
  that flag to decide whether it must silently re-run `solve_scf()` before
  handing back the cached mean-field Hamiltonian, so a stale SCF solution
  is never reused after a parameter changes. Called once per mode, right
  after `qtwrap.new_page()`, before `common.set_formulas()`/
  `connect_clicks()` — see any of
  `interface-pyqt/{0d,1d,2d,3d,2dslab,multilayergraphene,hybridfilm,hybridribbon}/<mode>.py`.
  `scfterms.build()` also places `hamiltoniantype.py`'s "Hamiltonian type"
  (Spinless/Spinful/Nambu) combobox directly above that switch row - see
  the `hamiltoniantype.py` bullet below.
- **`hamiltoniantype.py`** — the Spinless/Spinful/Nambu combobox
  (`hamiltonian_type`, default "Spinful") shared by the same eight modes as
  `scfterms.py` above (built as part of `scfterms.build()`, not a separate
  call a mode needs to make). `term_allowed(hamiltonian_type, name)` is the
  single source of truth for which term fields make sense under each
  choice: `SPIN_TERMS` (exchange, kanemele, antikanemele, rashba, mAF, J1,
  J2, J3) need `has_spin=True` (hidden for "Spinless"); `PAIRING_TERMS`
  (swave, pwave) need Nambu (hidden unless "Nambu" is selected). Widget
  visibility is actually applied by `latticeterms.py`'s
  `apply_term_restrictions()`/`connect()` (see that bullet below) since
  three terms - kanemele, antikanemele, mAF - are restricted by *both*
  modules at once (wrong lattice family *or* wrong Hamiltonian type), and
  the two restrictions have to be combined with AND, not applied as two
  independent `setVisible()` passes (order-dependent - whichever runs last
  would silently win). A mode's own `generate_hamiltonian()`/`initialize()`
  is separately responsible for actually *skipping* the matching
  `add_*()` calls under "Spinless" (not just hiding the widget) - see this
  module's own docstring for why: several of pyqula's `add_*()` methods
  (`add_zeeman`/`add_exchange`, `add_kane_mele`, `add_anti_kane_mele`,
  `add_rashba`, `add_antiferromagnetism`) unconditionally call
  `self.turn_spinful()` on the Hamiltonian *before* even looking at the
  value passed in, so calling one of them with a zero-valued field on a
  `has_spin=False` Hamiltonian would silently re-promote it to spinful.
  "Nambu" is always spinful-Nambu (`h.setup_nambu_spinor()`, called once a
  mode's single-particle terms are applied, establishes the BdG structure
  even when swave/pwave are both left at zero) - there's no
  "spinless Nambu" option, matching the three-way choice as asked for
  rather than a 2x2 spin×Nambu matrix. `codeview.py`'s `is_active()` also
  checks `term_allowed()` so the "pyqula code" preview (0d/1d/2d) never
  shows a call to a term hidden by the current choice, even if its field
  still holds a stale value from before the type was switched.
- **`hybridparts.py`** — grows/shrinks a `tabWidget_4`-style tab widget's
  tab count based on an `nparts` combobox (`addTab`/`removeTab`;
  `removeTab` doesn't delete the widget, so re-adding a part preserves its
  field values), and relabels Designer-built tabs "Part 1"/"Part 2" since
  their index order isn't guaranteed consistent across mode `.ui` files.
  Also injects each part's `<term>_image` formula label at runtime
  (`_add_formula_column()`), for the same reason `common.py:set_formulas()`
  does below - part 3+ tabs don't exist in `interface.ui` at all, so
  there's nothing for Designer to have pre-built an image widget into.
  Most `PARTS_FIELDS` entries are plain scalars (one `LineEdit` reads with
  `qtwrap.get()`), but a field listed in `hybridparts.VECTOR_FIELDS` (just
  `"exchange"` today) instead holds a 0d-style array, e.g. `"0.0, 0.0,
  0.0"`, read per-part with `hybridparts.part_array_interpolator(qtwrap.get_array,
  name,nparts,axis,region_of)` rather than `part_interpolator`/`get()` -
  `_build_tab()`'s part-3+ default text (`_default_text()`) and the
  Designer-authored part 1/2 fields must agree on this (both `"0.0, 0.0,
  0.0"` for a vector field), or a part's exchange field silently reads
  back as a 1-element array instead of a 3-vector.
- **`common.py:set_formulas()`'s `_ensure_formula_image()`** — not a
  standalone module, but the same pattern: creates a mode's `<term>_image`
  label at runtime (next to the term's field, one grid column over) the
  first time `set_formulas()` runs on a page that doesn't already have a
  Designer-authored one. This is what lets *every* mode's terms get a
  formula image/tooltip just by calling `common.set_formulas(qtwrap)`,
  without needing a matching `interface.ui` edit - see "Adding a
  Hamiltonian term" below.
- **`common.py:set_calculation_formulas()`'s `_move_params_above_buttons()`
  and `_ensure_button_formula_image()`** — together these make every
  calculation tab read as parameters, then its button(s) second-to-last,
  then a centered formula truly last, regardless of what order
  `interface.ui` originally put them in (some hand-authored tabs put the
  button first with parameters below it - e.g. 2d's Bands tab had
  `show_bands` at row 0 with its Operator/kpoints fields at row 1 - while
  others already put parameters first). `_move_params_above_buttons()`
  runs once per distinct grid layout (before any button's formula is
  added): it classifies each row as a "button row" (contains a widget
  whose name is a `CALC_FORMULAS` key) or a "parameter row" (everything
  else - a plain field, combobox, or an unrelated result display like
  `solve_scf`'s "Identified Mean field" caption), then rebuilds the grid
  with every parameter row above every button row, preserving relative
  order within each group - a no-op if that's already the order, or if
  the grid holds only one kind of row (e.g. 2d's "Topology 2D" tab, whose
  grid holds only the four Chern/Z2/Berry buttons - its Operator/kpoints
  fields live in a *sibling* grid layout in a different column entirely,
  so there's nothing to reorder and the buttons' relative order is left
  alone). `_ensure_button_formula_image()` then creates a `<button>_formula`
  label at runtime directly below the button, the first time
  `set_calculation_formulas()` runs (every button starts without a
  Designer-authored image - no mode predates this convention, so it always
  creates one, unlike the term version). A button doesn't reliably sit in a
  `QGridLayout` the way a term field does (e.g. 2d's DOS tab's `show_dos`
  is the second item of a plain `QVBoxLayout`), so this branches on the
  actual layout type via `qtwrap.find_any_layout_of()` (not
  `find_layout_of()`, which only searches `QGridLayout`s): in a grid, it
  opens a new row directly below the button's row (shifting later rows
  down via `_insert_grid_row_below()`, centered there via `Qt.AlignHCenter`)
  - by now that already means the true bottom of the tab, since
  `_move_params_above_buttons()` already ran. Several buttons often share
  one grid row (e.g. 2d's "Topology 2D" tab has
  `show_berry1d`/`show_berry2d`/`show_z2`/`show_chern` side by side as
  separate cells of one row) - `set_calculation_formulas()` passes a
  `formula_rows` dict (scoped to that one call) down so those buttons'
  formulas land together in the single new row opened below them, at each
  button's own column, instead of each button's insertion re-shifting the
  grid and scattering the formulas at different depths. In a box layout
  (always `QVBoxLayout` in practice - no calculation button in any mode's
  `interface.ui` sits directly in a `QHBoxLayout`), it just inserts right
  after the button's own item via `insertWidget()` (also centered), which
  already stacks the image below it - every such tab's `interface.ui`
  already puts its parameter grid before the button, so
  `_move_params_above_buttons()` (grid-only) has nothing to do there.
  Several button names map to the same formula PNG (`CALC_FORMULAS` in
  `termtooltips.py` maps button name -> formula key;
  `tools/gen_calc_formula_logos.py` renders one PNG per key, using
  mathtext's `"cm"` fontset to match the serif/italic look of the
  hand-made term formula PNGs) - see "Adding a calculation button" below.
- **`latticeterms.py`** — a registry (`RESTRICTED_TERMS`) of
  lattice-family-only widgets (Haldane/Kane-Mele/valley, honeycomb-only).
  `connect(qtwrap, lambda: getbox("lattice"))` show/hides the registered
  widgets and combobox items on every lattice-combobox change (and, on the
  same page, every `hamiltonian_type` combobox change too - see below).
  Adding a new geometry-restricted term is a one-line registry addition.
  `apply_term_restrictions(form, lattice_name, hamiltonian_type)` also
  folds in `hamiltoniantype.py`'s own restrictions, combining both via AND
  per widget base name before calling `setVisible()` once - see that
  module's bullet above for why a two-pass approach (lattice restrictions,
  then hamiltonian-type restrictions applied independently) would be
  order-dependent for a term named by both (kanemele, antikanemele, mAF).
  A caller that invokes `apply_term_restrictions()` directly instead of via
  `connect()` (`hybridparts.py`'s `on_new_part=`, used by
  `hybridfilm.py`/`hybridribbon.py` to restrict a newly-built part's
  fields) must pass `hamiltoniantype.get_type(form)` as the third argument
  too, or it silently falls back to "Spinful" regardless of the page's
  actual current selection.
- **`termhighlight.py`** — not a widget-building module like the three
  above, but the same "one shared helper called from `common.py`,
  `scfterms.py` and `hybridparts.py`" shape: `wire_highlight(field)` bolds
  a term's `QLineEdit` text while it holds a nonzero value (parsing both a
  plain number and comma-separated vectors like `exchange`'s `"Jx,Jy,Jz"`),
  and keeps it in sync on every `textEdited`. `common.py:set_formulas()`
  calls it once per single-particle term, looking the field up via
  `termhighlight.find_term_field()` (falls back to `FIELD_ALIASES` for the
  handful of terms whose field isn't named after its term key — see the
  "Term key vs. field object name" gotcha below); `scfterms.py`'s
  `_wire_interaction_field()` calls `apply_highlight()` directly instead
  (folded into its own single `textEdited` handler, alongside its
  pre-existing SCF-dirty/do_scf-autotoggle logic, rather than adding a
  second listener), and `hybridparts.py`'s `_add_formula_column()` calls
  `wire_highlight()` on each part's field exactly once (`ensure_built()`
  deliberately does *not* also call it — that field is guaranteed to reach
  `_add_formula_column()` too, once, right after `ensure_built()` returns
  it; wiring in both places double-listens on the same field).
  `qtwrap.load_interface()` also calls `termhighlight.apply_highlight()`
  directly for any field tagged `_term_highlight` (set by both
  `wire_highlight()` and `_wire_interaction_field()`) when restoring a
  saved `interface.json`, since `setText()` there doesn't fire
  `textEdited`.
- **`codeview.py`** — adds a third "pyqula code" sub-tab alongside "Single
  particle"/"Many-body interactions" inside "Terms in the Hamiltonian",
  showing a read-only, copyable pyqula script that reproduces the
  Hamiltonian the page's fields currently describe. Depends on
  `scfterms.build(qtwrap)` having already run (it reads
  `form._hamiltonian_subtabs`, the inner `QTabWidget` `scfterms.py`'s
  `_nest_scf_tab()` builds and saves there). `codeview.build(qtwrap,
  code_fn)` just adds the tab/text box/Refresh+Copy buttons; the actual
  script text comes from `code_fn`, a mode-supplied zero-argument function
  (`get_pyqula_code()` in `0d.py`/`1d.py`/`2d.py`) that mirrors that mode's
  own `get_geometry()`/`initialize()` by hand — see "Adding the 'pyqula
  code' tab to a mode" below for the convention and the checklist for
  keeping it in sync.

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
   convention/prefactor before writing the LaTeX. Add `<term>` to the
   `terms` list in `common.py:set_formulas()` (or `meanfield_terms` for a
   many-body term). **No `interface.ui` edit is needed for the image
   itself** — `set_formulas()`'s `_ensure_formula_image()` creates the
   `<term>_image` label at runtime, next to the field, the first time a
   mode without a Designer-authored one calls `set_formulas()` (see
   `CLAUDE.md`'s "Hamiltonian-term formulas" bullet). The only remaining
   requirement is that the mode actually calls `common.set_formulas(qtwrap)`
   at all — if it doesn't yet, add that call once, near
   `connect_clicks()`, the same way every mode already does. Modes whose
   term fields are built per-part at runtime instead of by Designer
   (`hybridfilm`/`hybridribbon`, see `hybridparts.py`) get this from
   `hybridparts.connect()`/`ensure_built()` automatically instead - no
   extra step needed there either, as long as the term name is in that
   mode's own `PART_FIELDS` list.
3. Add a 2-3 sentence physical-meaning entry to `TERM_TOOLTIPS` in
   `pysrc/interfacetk/termtooltips.py` — this is required independent of
   step 2 (it's shared by `common.py`, `scfterms.py`, and `hybridparts.py`).
   `termhighlight.wire_highlight()` (bolding the field while it's
   non-default) comes for free from the same `terms`-list entry in step 2
   as long as the `interface.ui` field is actually named `<term>` — see
   the "Term key vs. field object name" gotcha below if it isn't.
4. If the term is lattice-family-restricted, register it in
   `latticeterms.py` instead of hand-wiring show/hide logic in the mode.
5. Wire the field into whatever builds the Hamiltonian in `<mode>.py`.
6. Run `tools/smoke_test.py` (catches wiring/import mistakes, not physics
   correctness) and manually exercise the field in the running app.

## Adding a calculation button

1. Add the `PushButton` to `interface.ui` (`tools/convert_ui.sh` after).
2. Wire its handler — either it's one of `common.STANDARD_HANDLERS`'s
   names (nothing to do beyond giving it that exact object name) or it
   needs an entry in the mode's own `signals`/`extra={}` dict. If it's a
   new `STANDARD_HANDLERS` entry, also add its name to
   `tools/smoke_test.py`'s `AUTO_WIRED_BUTTONS` set - that file keeps its
   own copy (it can't import `common.py`'s at check time, see the comment
   above it) and the static wiring check fails a mode with the new button
   otherwise, even though it's genuinely wired at runtime via
   `wire_standard_signals()`.
3. Add a 1-3 sentence "what does this compute/plot" entry to
   `BUTTON_TOOLTIPS` in `pysrc/interfacetk/termtooltips.py`, keyed by the
   button's object name - reused automatically by every mode that has a
   same-named button via `common.set_button_tooltips(qtwrap)` (called
   once per mode, right after `connect_clicks()`). Check whether an
   existing entry already fits (most calculation buttons are named and
   behave the same way across modes) before adding a near-duplicate.
3b. If the button computes a genuine physical quantity worth showing a
   formula for (most calculations - not a picker/viewer button like
   `show_structure`/`select_atoms_removal`/`save_results`), add an entry to
   `CALC_FORMULAS` in `pysrc/interfacetk/termtooltips.py` mapping the
   button's object name to a formula *key*. If an existing key already
   matches the physics (e.g. another kind of LDOS, or another mode's
   identically-computed quantity), reuse it instead of adding a new one -
   that's what makes the same PNG show up for every button that needs it.
   For a genuinely new key, add `{key: r"<mathtext>"}` to `FORMULAS` in
   `tools/gen_calc_formula_logos.py` (check `pysrc/pyqula_user_guide.md` or
   the vendored docstring for the exact convention/prefactor first, same as
   a term formula) and run `python tools/gen_calc_formula_logos.py` to
   render `interface-pyqt/logos/calc_<key>.png` - matplotlib mathtext only
   (no `\oint`/`\big`/`\substack`; test render the string standalone before
   committing if unsure a construct is supported). No `interface.ui` edit is
   needed - `common.set_calculation_formulas(qtwrap)` (called once per mode
   from `finalize_page()`) creates the `<button>_formula` label next to the
   button at runtime for every mode that has it, the same way term formulas
   don't need one either (see `_ensure_button_formula_image()` above).
4. A new calculation doesn't need a new `ql-*` script if its output
   happens to match an existing one's file format: `common.py`'s
   `get_iets_qdos` (momentum-resolved IETS, the magnetic analog of
   `get_kdos_bands`) writes the same 3-column `(path-index, energy,
   intensity)` layout as `get_kdos_bands`'s `KDOS_BANDS.OUT`, so it reuses
   `ql-dosbands`/`ql-dosbands1d` unmodified instead of adding a new
   script. Check whether an existing `ql-*` script's input format already
   fits before writing a new one - see "Adding a `ql-*` script" below for
   when it doesn't. Sometimes the format fits but the script's on-screen
   text doesn't (it was written assuming only one physical quantity would
   ever feed it): `common.py`'s `get_iets_ldos` (0d) writes the same
   `MULTILDOS/` folder layout (`MULTILDOS.TXT` + one `LDOS_<e>_.OUT` per
   energy + `DOS.OUT`) that `get_multildos`'s `ldos.multi_ldos` call
   writes, by hand - `pyqula.ldos.multi_ldos_tb` has no "give me an
   arbitrary per-site quantity at N energies" mode, only real LDOS, so
   there's no pyqula call to reuse, just the file format it produces.
   Rather than duplicate `ql-multildos`'s slider/spatial-map-next-to-
   total-curve viewer wholesale, its previously-hardcoded strings
   ("Spatially resolved DOS", "LDOS", "Density of states", ...) were
   pulled out into `--title`/`--zlabel`/`--dlabel`/`--dtitle` args
   (defaulting to the original text, so `get_multildos`'s own
   `execute_script` calls needed no changes) and `get_iets_ldos` passes
   IETS-appropriate labels instead. Prefer this - generalizing a script's
   hardcoded labels into args with the original text as the default -
   over forking a near-identical copy of a `ql-*` script for a second
   physical quantity.

## Tooltip conventions

Every interactive form field should carry a hover tooltip. There are three
registries in `pysrc/interfacetk/termtooltips.py`, applied by three
`common.py` passes all called from `finalize_page()` (see "Adding a mode"
below) - `TERM_TOOLTIPS`/`set_formulas()` for Hamiltonian terms,
`BUTTON_TOOLTIPS`/`set_button_tooltips()` for calculation `PushButton`s, and
`PARAM_TOOLTIPS`/`set_param_tooltips()` for everything else (a numeric
`LineEdit`, `ComboBox`, or `CheckBox`/`RadioButton` that controls how a
calculation is run rather than being a Hamiltonian term or a calculation
trigger - e.g. `nk_bands`, `dos_delta`, `scf_initialization`). All three work
the same way: keyed by the widget's object name, applied once per mode by
`findChild(name)`, and skipped for a widget that already carries a tooltip
(most commonly a more specific one hand-authored in that mode's
`interface.ui`, but also one `scfterms.py`/`hybridparts.py` already set at
build time) - so adding an entry never overwrites a more specific existing
one, and a mode-specific hand-authored tooltip in Designer always wins.
Field names are reused across modes for the same kind of setting (nearly
every mode has its own `nk_bands`/`dos_delta`/`do_scf`/...), so one
`PARAM_TOOLTIPS` entry typically covers that field in every mode that has
it - check whether an existing entry already fits before adding a
near-duplicate, the same way `TERM_TOOLTIPS`/`BUTTON_TOOLTIPS` already work.
**Whenever a new non-term, non-button field is added to any mode's
interface, add its tooltip to `PARAM_TOOLTIPS`** (2-3 sentences, focused on
what the value controls and any accuracy/cost trade-off it implies) unless
an existing entry with the same name already covers it.

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

Every `<mode>.py`'s tail end follows the same shape, factored into shared
`common.py` helpers so a new mode doesn't have to hand-copy it:

```python
signals = common.wire_standard_signals(qtwrap,pickup_hamiltonian,extra={
  "show_structure": show_structure,
  # ... mode-specific handlers only; save_results/load_results are wired
  # automatically by finalize_page() below, don't list them here
})

inipath = os.getcwd() # before finalize_page()'s create_folder() chdirs away
common.finalize_page(qtwrap,window,signals,inipath)  # add robust=False for a
                                                       # full traceback on
                                                       # handler failure

if __name__ == "__main__":
    window.run()
```

**A mode doesn't have to be a quantum tight-binding model.** `latticegas`
(`interface-pyqt/latticegas/latticegas.py`, wrapping `pyqula.latticegas.
LatticeGas` - a classical, occupation-based lattice-gas model annealed by
Metropolis swaps) is the first mode with no Hamiltonian at all. It still
follows the three-file pattern and still calls `common.finalize_page()` at
the end (which no-ops harmlessly on term/button names it doesn't
recognize), but everything Hamiltonian-shaped is skipped or hand-rolled
instead of shared: no `pickup_hamiltonian`/`STANDARD_HANDLERS`/
`wire_standard_signals` (there's no Hamiltonian to build), no SCF, no
bands/DOS/Berry/Chern - `signals` is built as a plain `{name: handler}`
dict instead. `common.show_structure`/`show_structure_3d` still work
unchanged, since they only need a plain `Geometry`. The occupation
snapshot (`lg.den`, a 0/1 array with one entry per site) is written with
the existing `g.write_profile(d,name=...)` (the same mechanism
`topologytk/realspace.py:real_space_chern` uses for
`REAL_SPACE_CHERN.OUT`) and plotted by the **existing** `ql-potential`
script unchanged (`ql-potential --input PROFILE.OUT --cmap binary`) -
"scatter colored by one scalar per site" doesn't need a mode-specific
script. There used to be a standalone `ql-latticegas-correlator` script
(and `show_correlator`/"Show correlator" button) for the final
snapshot's neighbor-shell correlator alone, following the existing plain
`plotstyle.apply()` + `np.genfromtxt` + `plt.show()` convention (e.g.
`ql-dos-path`) rather than the older, unwired `ql-plot1d`/`ql-multiplot1d`
(which don't call `plotstyle.apply()`, so they wouldn't pick up the
shell's theme) - both were removed once `show_correlator_relaxation`
(below) made a single-snapshot correlator view redundant, and
`CORRELATOR.OUT` is no longer written at all.

`run_anneal()` has no button of its own - there's no explicit "Run" step
in this mode's UI at all. Every Show button calls `_ensure_annealed()`
first, which calls `run_anneal()` automatically, but only if it's never
run (`_anneal_dirty_time is None`) or a parameter has been edited since
the last run (`_needs_live_anneal()`: `window.params_dirty_time()>
_anneal_dirty_time` - the same edit-timestamp/dirty-flag primitive
`huge_0d.py`'s `initialize()`/`_ensure_initialized()` already uses for
its own "rebuild only if something changed" check). `run_anneal()`
itself sets `_anneal_dirty_time = window.params_dirty_time()` as its
last line, once everything else has succeeded - so a click that finds
nothing changed just reuses the existing results instead of
re-annealing.

`_ensure_annealed()` has one more layer beyond `_needs_live_anneal()`,
for **Load Results**: `save_state()`/`load_state()` (`qlinterface.py`)
copy this mode's flat result files (`PROFILE.OUT`, `ENERGY.OUT`, ...) in
and out of a named folder, and `load_state()` ends
with `window.reset_dirty()` - which bumps `params_dirty_time()` forward
exactly the way a live field edit would, since it's the same timestamp.
Naively treating that the same as "the user edited a parameter" would
make the very next Show click discard what was just loaded and silently
replace it with a fresh, differently-random anneal - `_ensure_annealed()`
avoids this with a second check: even when `_needs_live_anneal()` is
`True`, if `PROFILE.OUT` already exists on disk and its mtime is at
least as new as the current `params_dirty_time()` (true right after a
Load, since `load_state()`'s `shutil.copy()` loop runs *after* its
`reset_dirty()` call - false after a real edit, since the file predates
it), that's accepted as already-current and `run_anneal()` is skipped.
`show_correlator_relaxation()` can't use this same bypass, though - it
needs `_anneal_state`'s live `LatticeGas` object (`g`, `lg`, `frames`),
which `save_state()`/`load_state()` never touch (like the
`LATTICEGAS_*_FRAMES/` folders it reads/writes, see below), so it checks
`_needs_live_anneal()` directly and always anneals for real when that's
`True`, regardless of file freshness.

`run_anneal()` also captures intermediate occupation snapshots during the
anneal, not just the final one: `LatticeGas.optimize_energy()` accepts a
`checkpoint_at` kwarg (an iterable of 1-indexed trial-step counts) and
populates `lg.checkpoints` (a `dict[step -> den snapshot]`) - this is
vendored-`pyqula` backend infrastructure that predates the GUI wiring for
it. `run_anneal()` requests `n_snapshots` (a field on the Anneal settings
tab) evenly-spaced steps via `np.linspace(1,ntries,n_snapshots)`, builds
`(step,den)` pairs via `_checkpoint_frames()` (the pre-anneal random
configuration as step 0, plus every requested checkpoint) - shared by
every "across snapshots" writer so their Step sliders all index the same
sequence.

`_write_configuration_frames()` writes each snapshot's occupation map to
`LATTICEGAS_FRAMES/` with an index file
(`LATTICEGAS_FRAMES/LATTICEGAS_FRAMES.TXT`, one frame filename per line) -
the same "indexed folder + `.TXT` filename list" convention
`pyqula.timeevolution.evolve_local_state`'s `MULTITIMEEVOLUTION/` folder
and `pyqula.ldos`'s `MULTILDOS/` folder already use for their own
multi-frame outputs - and `run_anneal()` calls it directly, since writing
an occupation map per snapshot is cheap. The `show_relaxation` button
launches `ql-latticegas-relaxation` to view it (see below).

The neighbor-shell correlator (`LatticeGas.get_correlator()`) per
snapshot is not cheap the same way: its per-shell loop is O(nsites^2),
and multiplied across ~21 frames at the library's default resolution it
measured ~8s extra on a 600-site Kagome supercell - real added latency to
*every* anneal even though most anneals never get their
correlator-across-snapshots viewed. So `run_anneal()` does **not** call
`_write_correlator_frames()` - instead it stashes the objects that
function needs (`g`, `lg`, `frames`, `is_2d`, plus a `correlator_computed`
flag starting `False`) into a module-level `_anneal_state` dict, cleared
right after the cheap `filling` validation at the top of `run_anneal()`
and only repopulated at the very end, once every step in between has
succeeded - so a `run_anneal()` that fails partway through (a bad
parameter, a construction error) leaves `_anneal_state` empty rather than
serving `show_correlator_relaxation()` a stale anneal's frames.
`_write_correlator_frames()` only actually runs inside
`show_correlator_relaxation()`, and only the first time it's clicked for
a given anneal (guarded by `correlator_computed`, set `True` right after)
- a later click just replots the same frames, same as every other Show
button here, rather than recomputing. This is safe as a plain module
global rather than something written to disk: each mode's `.py`
is imported once for the app's lifetime (no page-rebuild/reload path),
and `qtwrap`'s app-wide busy lock serializes every handler, so there's no
concurrent access to worry about - the one case where a parent-process
global like this wouldn't be visible is a handler that runs via
`qtwrap.py`'s "Subprocess-based calculations" path (a `calc.py`-based
handler running in a child OS process, e.g. `1d/calc.py`), which doesn't
apply here since `latticegas` has no `calc.py`. `_write_correlator_frames()`,
per snapshot, writes only whichever of the two is actually plotted (see
`ql-latticegas-correlator-relaxation` below) - never both, since the
other would just be wasted computation: for a 2D lattice (`is_2d =
getbox("lattice")!="Chain"`, since every other `LATTICES` entry is a 2D
Bravais lattice), the reciprocal-space structure factor
(`LatticeGas.get_structure_factor()`, the 2D companion to
`get_correlator()`: `get_correlator()` gives the ordering length scale,
`get_structure_factor()` gives its wavevector) to
`LATTICEGAS_STRUCTURE_FRAMES/`; otherwise (`Chain`, which has no
meaningful `S(q)`) the neighbor-shell correlator itself
(`LatticeGas.get_correlator()`, temporarily pointing `lg.den` at that
snapshot and restoring it afterwards) to `LATTICEGAS_CORRELATOR_FRAMES/`,
capped at `n=8` neighbor shells rather than the library's default (a
quick slider scrub doesn't need 20 shells' worth of resolution to show
the ordering trend, and it keeps `show_correlator_relaxation()` itself
responsive). The `show_correlator_relaxation` button launches
`ql-latticegas-correlator-relaxation` to view whichever folder exists -
unlike the other Show buttons, it checks `_needs_live_anneal()` directly
rather than going through `_ensure_annealed()` (see above), which
guarantees `_anneal_state` is populated and current by the time this
handler's own logic runs.

Both viewer scripts are `plotpyqt`-based (same
`interfacetk.plotpyqt.get_interface()` scaffolding `ql-multildos` uses)
with a "Step" slider - built via `main.add_slider(label="Step",
vs=range(len(frames)))`, which returns the frame index directly rather
than `ql-multildos`'s older `0..100`-then-rescale trick.
`ql-latticegas-relaxation` re-renders `ql-potential`'s binary occupation
scatter for whichever frame is selected, alongside the energy trace
(`ENERGY.OUT`, if present) with a vertical marker at the current step -
this made the old standalone "Show energy trace" button/`ql-latticegas-
energy` script redundant, so both were removed rather than kept alongside
it. Unlike `ql-potential` (which every other mode's "Show configuration"-
style button still uses unchanged, Zoom slider included),
`ql-latticegas-relaxation` itself has no Zoom slider - just "Step" and
"Size" - since this script isn't reused elsewhere, so the slider was cut
directly rather than left in place unused; the scatter just autoscales
to its data's extent on every redraw instead of respecting a
user-controlled x/y limit factor.

`ql-latticegas-correlator-relaxation` puts the same energy trace + marker
on its left panel (also reading `ENERGY.OUT` directly, rather than being
handed it - the two scripts don't share any code) and, on the right,
whichever of `LATTICEGAS_STRUCTURE_FRAMES/`/`LATTICEGAS_CORRELATOR_FRAMES/`
actually exists (exactly one does, per `_write_correlator_frames()`
above - a script reading one should treat the other's absence as "this
lattice doesn't have that kind of correlator", not an error) is
authoritative for the frame count/step sequence, not just an arbitrary
default: for a 2D lattice, an `imshow` of `S(q)` reshaped from its
`nq`x`nq` grid (same "reshape a flattened grid back to 2D" move
`ql-multildos --grid` uses), `aspect="equal"` - `q_x`/`q_y` share the same
physical scale, so a square map is the physically correct rendering, not
a distortion to avoid - with its colorbar drawn into a thin
`mpl_toolkits.axes_grid1.make_axes_locatable(ax).append_axes(
"right",size="5%",pad=0.1)` sibling axes rather than via
`fig.colorbar()`'s own `ax=`/`fraction=` shrinkage, so the "equal" aspect
still keeps as much of the panel's own size as possible rather than
losing more of it to the colorbar's carve-out on top. `ticks=[sq.min(),
sq.max()]` relabeled `["Min","Max"]` (same `cb.ax.set_yticklabels(...)`
move `ql-multildos` uses for its own `[0,'Max']`) rather than showing the
raw `S(q)` values, which aren't individually meaningful - only the
ordering wavevector's location in the map is; for `Chain` (no meaningful
`S(q)`), the correlator line plot instead, with short axis labels
(`"G(r)"`/`"Distance"` rather than `"Density-density correlator"`/
`"Neighbor distance"`) since this panel is only half the figure's width
and the longer labels clipped into the left panel.

`latticeising` (`interface-pyqt/latticeising/latticeising.py`, wrapping
`pyqula.latticeising.LatticeIsing`) is the second mode built on this
Hamiltonian-less pattern, and mirrors `latticegas` almost line for line —
same `_anneal_state`/`_anneal_dirty_time`/`_ensure_annealed()` machinery,
same checkpointed-snapshot/indexed-folder frame writers, same lazy
correlator-frames computation gated on a `correlator_computed` flag, same
`ql-latticeising-relaxation`/`ql-latticeising-correlator-relaxation`
viewer pair (`LATTICEISING_FRAMES/`, `LATTICEISING_STRUCTURE_FRAMES/`,
`LATTICEISING_CORRELATOR_FRAMES/` in place of the `LATTICEGAS_*`
equivalents). Two physics differences ripple through the copy: `LatticeIsing`
uses spins `s` in `{-1,+1}` with the **opposite** `add_interaction()` sign
convention from `LatticeGas` (positive `Jij` is ferromagnetic, not
repulsive — hence the distinct field name `Jij_ising`, so its
`PARAM_TOOLTIPS` entry doesn't collide with `latticegas`'s `Jij`), and its
default dynamics is `li.optimize_energy()` — single-spin-flip Metropolis,
which does **not** conserve magnetization (unlike `LatticeGas.
optimize_energy()`'s fixed-filling swaps) — so the "Initial magnetization"
field (`magnetization`, `-1..1`) is only a starting point, not a
conserved quantity, and the external field (`field_profile`) genuinely
matters even when uniform, unlike `latticegas`'s `mu_profile` (see both
fields' `PARAM_TOOLTIPS` entries). Because `li.optimize_energy()` also
returns a total-magnetization trajectory (`ms`, alongside the energy
trajectory `es`) with no extra cost, `run_anneal()` writes it to
`MAGNETIZATION.OUT` and both viewer scripts plot it as a second trace
(`twinx()`) alongside the energy trace — a small addition beyond
`latticegas`'s pattern, since magnetization is the standard Ising order
parameter and the data was already there for free. Button names are
`show_spin_configuration`/`show_spin_relaxation`/
`show_spin_correlator_relaxation` rather than `latticegas`'s
`show_configuration`/`show_relaxation`/`show_correlator_relaxation` —
distinct names so their `BUTTON_TOOLTIPS` text (up/down spins, not
occupied/empty sites) doesn't collide with `latticegas`'s entries for the
same shared-registry reason as `Jij_ising`. `supercell_size`/`temp`/
`ntries` keep their `latticegas` names and tooltips (generalized to cover
"swap or flip" moves and "lattice gas / Ising" hosts, rather than adding
a duplicate `_ising`-suffixed entry for each) since their meaning doesn't
actually differ between the two models.

`common.finalize_page(qtwrap,window,signals,inipath,robust=True)` replaces
what used to be five separate repeated lines: it calls `create_folder()`
and sets `window.scratch_dir`, wires `save_results`/`load_results` (only if
the page actually has those buttons — via `save_state`/`load_state`, using
`inipath` and its own freshly-captured `tmppath`), calls
`set_formulas(qtwrap)`, `window.connect_clicks(signals,robust=robust)`,
then `set_button_tooltips(qtwrap)`, `set_calculation_formulas(qtwrap)` (see
"Adding a calculation button" above), and `set_param_tooltips(qtwrap)` (see
"Tooltip conventions" above). `inipath` must still be
captured by the caller (with `os.getcwd()`) *before* calling this, since
`create_folder()` chdirs away from it — a few modes
(`impurity_embedding`/`ribbon_embedding`/`huge_0d`) also display it
directly (e.g. in an `info_tab` label) and so keep that same variable
around for their own use, rather than it living only inside the helper.
`tools/smoke_test.py`'s static wiring check knows about this: it treats
`save_results`/`load_results` as wired whenever a mode's source contains
`finalize_page(`, the same way it already treats `wire_standard_signals(`
as auto-wiring `common.STANDARD_HANDLERS`'s button names.

Similarly, a mode's `show_structure`/`show_structure_3d` handlers are
almost always exactly `common.show_structure(qtwrap,get_geometry)` /
`common.show_structure_3d(qtwrap,get_geometry)` — both take an optional
`script=` if the mode plots something other than the default
`ql-structure-bond --input POSITIONS.OUT` / `ql-structure3d POSITIONS.OUT`
(e.g. `tbg.py` passes its own `ql-potential ...`/`ql-structure-tbg ...`
commands). Only write a custom `show_structure()` body by hand if the mode
needs to do something extra before plotting (e.g. `hybridfilm.py` writes a
`PROFILE.OUT` z-sign profile first).

## Adding the "pyqula code" tab to a mode

`0d`/`1d`/`2d` each have a "pyqula code" sub-tab (built by `codeview.py`,
see the "Runtime dynamic-widget patterns" bullet above) showing a
standalone pyqula script that reproduces the Hamiltonian the page's fields
currently describe - copyable, so a user can take it and run it outside
the GUI. Retrofitting this onto another mode:

1. Call `codeview.build(qtwrap, get_pyqula_code)` after
   `scfterms.build(qtwrap)` (hard prerequisite - it builds
   `form._hamiltonian_subtabs`, which `codeview.build()` requires and
   raises a clear `RuntimeError` without) and after `get_pyqula_code` is
   defined - see the end of `0d.py`/`1d.py`/`2d.py` for the exact spot,
   right before the `inipath = os.getcwd()` line.
2. Write `get_pyqula_code()` in that mode's `<mode>.py` by hand-mirroring
   its own `get_geometry()` and `initialize()` (or, for a mode that uses
   `common.generate_hamiltonian()` instead of writing its own `initialize()`
   inline, like `2d.py` does - mirror that function's term list instead).
   This is deliberately **not** a generic call-tracing mechanism over
   `pyqula` objects (`pysrc/pyqula/` is vendored/black-box, so wrapping its
   Hamiltonian/geometry objects to auto-capture every call would be a much
   larger, riskier piece of machinery than this feature needs) - it's a
   second hand-written listing that must be kept in sync with
   `initialize()` by hand, the same way `common.py:set_formulas()`'s
   `terms` list already has to be (see "Adding a Hamiltonian term" above).
   **Whenever you add, remove, or change a term in a mode's `initialize()`
   (or `common.generate_hamiltonian()`), update that mode's
   `get_pyqula_code()` to match** - nothing else enforces they agree.
3. Every optional term line is guarded by `codeview.is_active(qtwrap,name)`
   (a thin wrapper around `termhighlight.is_nonzero_value()`, the same test
   that bolds a term's field) so the generated script only lists terms
   currently away from their zero/default value - a clean, minimal listing
   rather than a line-for-line dump of every possible `add_x(0.0)` no-op.
   Geometry construction and the base `h = g.get_hamiltonian(...)` call are
   always included unconditionally (there's no "zero" geometry or hopping).
   Use `codeview.format_value(qtwrap,name)`/`format_array(qtwrap,name)` to
   turn a field's raw text into the Python literal for that line - `format_value`
   falls back to embedding the raw text verbatim as a `lambda r: <text>`
   body for the handful of fields (e.g. `crystalfield`, strain profiles)
   that can hold a position-dependent expression instead of a plain number,
   mirroring `qtwrap.get()`'s own `eval("lambda r: "+text)` fallback.
   A field the real code casts with `int(...)` (e.g. a mode's `nsides`/
   `nsuper`/ribbon `width`) needs its own `int(get(name))` in the
   generator instead of `format_value()` - the latter always keeps a
   number as a float, which is wrong for a count/index argument.
4. When the SCF switch (`do_scf`) is on, append
   `common.pyqula_code_scf_block(qtwrap, richer=...)` - shared because
   `0d.py`/`1d.py` both call this file's own `common.solve_scf()`
   (`richer=False`) while `2d.py` (and `3d.py`, if/when it gets this
   feature) has its own richer `solve_scf()` that passes `maxerror=`
   instead of `T=` (`richer=True`) - see that function's docstring. This
   only ever needs the `meanfield.VJinteraction(...)` branch, never the
   spinless `meanfield.Vinteraction(...)` branch `solve_scf()` also
   supports, since every mode that has this tab always builds a
   `has_spin=True` Hamiltonian.
5. Manual atom removal (the "Modify geometry" tab) is reproduced via
   `codeview.geometry_removal_code(qtwrap, center=...)`, called right after
   the geometry lines and before `h = g.get_hamiltonian(...)` - mirrors
   `interfacetk.modify_geometry()`'s two checkboxes
   (`remove_selected`/`remove_single_bonded`). `remove_selected`'s actual
   atom indices are read once, from `REMOVE_ATOMS.INFO` in the page's own
   scratch folder, and baked into the generated code as a literal list
   (`sculpt.remove(g, [3, 7, 12])`) rather than the generated script
   re-reading that scratch file itself, so it stays self-contained and
   correct even if run later/elsewhere. This is why `build()`'s `refresh()`
   restores the page's own `scratch_dir` as the process cwd before calling
   `code_fn()` - the Refresh/Copy buttons aren't wired through
   `connect_clicks()`'s own chdir-to-scratch-dir wrapper
   (`qtwrap.py:_with_own_scratch_dir()`), so this module has to do the
   equivalent itself. Pass `center=True` for a mode whose own
   `modify_geometry()` wrapper also calls `g.center()` afterward (`0d.py`
   does; `1d.py`/`2d.py` don't).

## Hard-cancelling a calculation

Normally a handler's actual pyqula computation runs in-process, on
`_HandlerRunner`'s worker `QThread` (see `CLAUDE.md`'s `qtwrap.py` bullet) -
which can never be safely cancelled once started, since `pysrc/pyqula/` is
vendored/black-box with no cancellation hooks and `QThread.terminate()` can
corrupt the interpreter mid numpy/scipy call. A handler can opt into
running its computation in a **child OS process** instead, which the shell
can kill outright with no such risk - only a few handlers are migrated to
this so far (currently: the shared `solve_scf` on `1d`; the same pattern
extends to other modes/handlers over time, mechanically for a handler that
already reads all its widget state before doing any pyqula work, which is
most of them - see the handler-classification notes in the cancellation
plan this was built from).

**The pieces**, all new:

- **`pysrc/run_calculation.py`** - a standalone entry point (`<python>
  run_calculation.py <mode_dir> <handler_key> <inputs_json_path>
  <scratch_dir>`) that chdirs to `scratch_dir`, loads `<mode_dir>`'s own
  `calc.py` (bare `import calc`, via `sys.path.insert(0,mode_dir)` - same
  pattern `huge_0d`'s `islandbuild.py`/`handlers.py` already use) and calls
  `calc.COMPUTE_HANDLERS[handler_key](inputs)`. **Deliberately lives in
  `pysrc/`, not `pysrc/interfacetk/`** - Python auto-prepends a launched
  script's own directory to `sys.path[0]`, and `pysrc/interfacetk/` already
  holds a plain module also named `interfacetk.py` (the `modify_geometry`
  helper); launching a script from inside that directory would make a bare
  `import interfacetk` resolve to that submodule instead of the
  `interfacetk` *package*, shadowing it. Found by symptom, not by
  inspection: the first version of this script lived in
  `pysrc/interfacetk/` and failed with `ImportError: cannot import name
  'image2island' from partially initialized module 'pyqula.sculpt'` - the
  shadowed `interfacetk.py`'s own `from pyqula import sculpt` (its first
  line) became the very first `pyqula` import in the child process,
  tripping a circular-import fragility in an environment with a second,
  editable `pyqula` checkout earlier on `sys.path` than this repo's vendored
  `pysrc/pyqula/`. If you ever need a second top-level script like this
  one, keep it out of any package directory that also contains a
  same-named submodule.
- **A mode's own `calc.py`** (sibling to `<mode>.py`, e.g.
  `interface-pyqt/1d/calc.py`) - the mode's geometry/Hamiltonian-building
  functions (`get_geometry()`/`initialize()` for `1d`), moved out of
  `<mode>.py` and made **accessor-parameterized**: each takes an explicit
  `accessor` parameter (defaulting to the live `qtwrap` module, so every
  existing zero-arg call site in `<mode>.py` keeps working unchanged) and
  calls `accessor.get(...)`/`accessor.getbox(...)`/`accessor.get_array(...)`
  instead of the module-level `get`/`getbox`/`qtwrap.get_array` names
  directly. This is *why* `calc.py` has to be a separate file from
  `<mode>.py`: `<mode>.py` builds its page as a side effect of import
  (`window = qtwrap.new_page(...)`, unconditional, not guarded by
  `if __name__=="__main__"`), so importing it fresh in `run_calculation.py`'s
  child process would try to construct a whole `QMainWindow` there - `calc.py`
  has no such side effect, so it's safe to import on its own. `calc.py`
  also defines one `compute_<handler>(inputs)` per migrated handler (a pure
  reimplementation of that handler's body, reading `inputs` instead of
  `qtwrap`) and a `COMPUTE_HANDLERS = {"<button_name>": compute_<handler>}`
  dict for `run_calculation.py` to dispatch through.
- **`pysrc/interfacetk/dictform.py`**'s `DictForm` - the accessor a
  `compute_<handler>()` function passes to `get_geometry()`/`initialize()`
  in place of `qtwrap`. Reads from a plain dict shaped exactly like
  `qtwrap.save_interface()`'s own output
  (`{name: {"type": "line"/"combo"/"check", "value": ...}}`), so gathering
  a subprocess's inputs is just "call `save_interface()` to a file", not a
  bespoke per-handler field list to keep in sync by hand. Implements
  `get`/`getbox`/`get_array`/`is_checked`/`_current_page()` and a
  `__getattr__` returning a small `_FieldStub` (so
  `hamiltoniantype.get_type()`'s `getattr(form,"hamiltonian_type",
  None).currentText()` works against it the same as a real combobox).
- **`qtwrap.run_calculation_subprocess(mode_dir,handler_key,scratch_dir)`** -
  called from inside a migrated handler (see `1d.py`'s `solve_scf()`) in
  place of doing the work directly. Snapshots the page via
  `save_interface()`, launches `run_calculation.py`, and blocks the calling
  thread on `proc.wait()` - since this runs on the handler's own
  `_HandlerRunner` worker thread, this is just another blocking call as far
  as that thread is concerned, so the GUI stays responsive exactly as it
  already does for any other handler; **no new `Runner`/thread class was
  needed**. Tracks the live `Popen` as module-level
  `qtwrap.current_child_process` (page-agnostic, like `is_busy()`/
  `_busy_lock` - only one calculation ever runs at a time regardless of
  which page started it) so `qtwrap.cancel_current_calculation()` (called
  from the shell's global "Cancel calculation" button, next to the
  Parallel execution switch) can `terminate()`/`kill()` it. Raises
  `qtwrap.CalculationCancelled` (a new exception) when the child died from
  that kill (detected via a negative returncode matching
  `SIGTERM`/`SIGKILL`), which `_HandlerRunner.run()` now catches
  separately from a genuine failure, emitting a new `finished_cancelled`
  signal so the GUI reports "Cancelled" (an info bar) instead of
  "Calculation failed" (an error bar) - see `_on_runner_cancelled()`,
  following the same "report before `release_busy()`" ordering rule as
  `_on_runner_error()` (busy-lock reentrancy gotcha, below).
- **Atomic cache writes.** A migrated handler's compute function must
  write any on-disk cache (`hamiltonian.pkl` in particular) to a temp name
  and `os.replace()` it into place at the end, not write in place -
  `common.py`'s `solve_scf()` now does this
  (`scf.hamiltonian.save(output_file="hamiltonian.pkl.tmp")` then
  `os.replace(...)`) - otherwise a killed subprocess could leave a
  half-written `hamiltonian.pkl` that `pickup_hamiltonian()`'s
  `os.path.exists("hamiltonian.pkl")` check would later mistake for a
  valid cached solve. `os.replace()` is an atomic overwrite on both POSIX
  and Windows, unlike `os.rename()`.

**Migrating a handler, checklist:**

1. Move its geometry/Hamiltonian-building dependencies into that mode's
   `calc.py` (create one, following `1d/calc.py`, if this mode doesn't have
   one yet), parameterizing them on `accessor` as above. Update `<mode>.py`
   to import them from `calc.py` instead of defining them inline
   (`from calc import get_geometry, initialize` or equivalent).
2. Write `compute_<handler>(inputs)` in `calc.py`: build a `DictForm(inputs)`
   accessor, then call the same functions the in-process handler calls,
   passing that accessor through. Add it to `COMPUTE_HANDLERS`.
3. Change the handler in `<mode>.py` to call
   `qtwrap.run_calculation_subprocess(moddir,"<handler_key>",window.scratch_dir)`
   instead of doing the work directly (`moddir` = that mode's own directory,
   captured once near the top of `<mode>.py`, the same way `1d.py` does).
   If the handler needs to update page state the subprocess can't reach
   (e.g. clearing `_scf_dirty` - `DictForm._current_page()` returns itself,
   which has no such attribute, so `common.mark_scf_solved()`'s
   `hasattr(page,"_scf_dirty")` check safely no-ops inside the subprocess),
   do that in `<mode>.py` right after `run_calculation_subprocess()` returns.
4. Run `tools/smoke_test.py`, then manually verify: a normal run still
   produces the same result as before migrating; a mid-run cancel (see the
   shell's Cancel button) reports "Cancelled", releases the busy lock, and
   leaves no corrupt cache file behind (a retry afterward should behave
   like a fresh run, not a resumed/corrupted one).

**Not worth migrating**: interactive picker handlers (`select_atoms_removal`,
"Select path", "Select DOS atoms", "Select impurity sites", "Select
time-evolution atom", ...) open a GUI/matplotlib picker and inherently need
the GUI thread - they're also instant, not long computations, so
cancellation isn't meaningful for them. A handler that interleaves widget
reads with pyqula work across multiple stages (rather than reading
everything up front, then making one call) needs its own restructuring
pass to gather all its inputs first, rather than a mechanical split.

## Retrofitting SCF onto an existing mode

Adding mean-field support to a mode that never had it (done for
`hybridribbon`/`hybridfilm`) means copying a whole "SCF" tab (`Basic`/
`Convergence` sub-tabs: `solve_scf`/`scf_initialization`/
`filling_scf`/`nk_scf`/`mix_scf`/`smearing_scf`/`scf_solver`, plus the `scf_terms_container`
placeholder - **not** `do_scf`, `scfterms.build()` builds that widget itself
at runtime, see the `scfterms.py` bullet above) from an existing SCF+formulas
mode's `interface.ui` (`1d`/`2d`/`0d`)
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
  `scfterms.py` read by exact string (`solve_scf`,
  `scf_initialization`, `filling_scf`, `nk_scf`, `mix_scf`, `smearing_scf`,
  `scf_solver`, `scf_terms_container`), which must stay as-is. If the target mode already
  has its own real `tabWidget_4` for something else (e.g. `hybridparts.py`'s
  per-part tabs, which default to that exact name), rename the SCF block's
  inner Basic/Convergence `QTabWidget` and pass a non-default `grid=` to
  `scfterms.build(qtwrap, grid="...")` instead of leaving the default
  `"gridLayout_10"` - same collision risk, checked the same way.
- **`<customwidget>` declarations.** The copied block's fields are all
  `LineEdit`/`ComboBox`/`PushButton` promotions - if any of those types is
  new to the target mode's `interface.ui`, its `<customwidgets>` block
  won't declare that promotion yet. `pyside6-uic` doesn't error on this -
  it emits `WriteImports::add(): Unknown Qt class <Type>` to stderr and
  silently generates the plain Qt base class instead of the styled one.
  Add the missing `<customwidget>` block (copy the pattern from one of the
  types already declared) and re-run `tools/convert_ui.sh` until the
  warning is gone. (`do_scf` itself needs no such declaration - it's a
  runtime `SwitchButton`, not a Designer-promoted widget at all, see the
  `scfterms.py` bullet above.)

Then wire the mode's `<mode>.py` like `1d.py`: `pickup_hamiltonian =
common.pickup_hamiltonian(qtwrap,initialize,do_scf=True)`, a `solve_scf()`
handler (`h = initialize(); common.solve_scf(h,qtwrap)`), and `"solve_scf":
solve_scf` in the signals dict - `common.finalize_page()` (see "Adding a
mode" above) already calls `common.set_formulas(qtwrap)`,
`common.set_button_tooltips(qtwrap)`, `common.set_calculation_formulas(qtwrap)`,
and `common.set_param_tooltips(qtwrap)`
for you, so nothing extra is needed for those. `common.set_formulas()`
tries every single-particle term's `<term>_image` (`hopping_image`,
`fermi_image`, ...) and creates any that's missing next to its field (see
the "Adding a Hamiltonian term" checklist above) - a term this mode has no
field for at all still prints a harmless `"<name> label not found"` to
stderr from `set_logo()`; that's expected, not a wiring bug.

### The SCF `scf_solver`/`scf_maxite` fields and `use_jax`

`scf_solver` (Convergence sub-tab, right after `smearing_scf`) lists
`linear_mixing`/`error_gradient`/`krylov` (in that order - index 0 is the
combobox default) and, together with `scf_maxite` (a plain `LineEdit`
right after it, default `"100"`), is read by
`common.get_scf_solver_kwargs(h,window,for_vjinteraction)`, called from
every `solve_scf()` (the shared `common.py` one, and `2d.py`/`3d.py`'s own
richer copies) right inside the `meanfield.VJinteraction(...)`/
`meanfield.Vinteraction(...)` call via `**common.get_scf_solver_kwargs(...)`.
Things to know before touching this:

- **`maxite` is unconditional.** Unlike the solver choice below, `maxite`
  (parsed as `int(window.get("scf_maxite",default=100))`) is returned in
  every case - even `h.has_eh` or a missing `jax` - since both
  `VJinteraction`/`Vinteraction`'s plain (non-jax) mixing loops accept
  `maxite` too (`spinspin.py`/`densitydensity.py` both have their own
  `maxite=None`-by-default param, honored independent of `solver=`).
- **The two entry points name the same three algorithms differently.**
  `VJinteraction`'s own `use_jax=True` solver names are `"error_gradient"`/
  `"linear_mixing"` (matching the dropdown verbatim) plus `"newton_krylov"`
  passed straight through unchanged (not one of its renamed pair) - so
  `for_vjinteraction=True` only needs the dropdown's `"krylov"` translated,
  via `_VJINTERACTION_SOLVER_NAMES = {"krylov": "newton_krylov"}`.
  `Vinteraction`'s `use_jax=True` path (`densitydensity_jax.py`) still uses
  the older internal names `"lbfgs"`/`"fixed_point"` for the same
  error_gradient/linear_mixing pair (but likewise accepts `"newton_krylov"`
  verbatim) - `get_scf_solver_kwargs(...,for_vjinteraction=False)`
  translates all three via its own `_VINTERACTION_SOLVER_NAMES` dict. Don't
  pass the dropdown's raw value straight to `Vinteraction` or a `"krylov"`/
  `"error_gradient"`/`"linear_mixing"` choice raises `ValueError:
  unrecognised solver`.
- **The solver choice (not `maxite`) silently no-ops instead of raising**
  when `h.has_eh` (a BdG/superconducting Hamiltonian - swave/pwave pairing
  added in `generate_hamiltonian`) or when the optional `jax` package isn't
  importable (`get_scf_solver_kwargs` returns just `dict(maxite=maxite)` in
  both cases, dropping `use_jax`/`solver`) - `Solve SCF` then just falls
  back to its pre-existing plain-mixing loop, exactly as it behaved before
  this dropdown existed. This is intentional (the dropdown has no explicit
  "default/old behavior" option to fall back to), but it means a solver
  choice can look like it did nothing with no error at all if you're
  testing on a pairing-enabled Hamiltonian or a jax-less interpreter -
  check `h.has_eh` and `importlib.util.find_spec("jax")` first if the
  three solvers ever seem to make no difference.
- Adding a fourth solver later means adding it to all 8 modes'
  `scf_solver` combobox items (`.ui`, then `tools/convert_ui.sh`), and
  adding a translation entry to `_VJINTERACTION_SOLVER_NAMES`/
  `_VINTERACTION_SOLVER_NAMES` for whichever of the two entry points'
  internal solver name differs from the dropdown's friendly spelling -
  `"newton_krylov"` happens to be the same underlying name for both
  entry points, so `"krylov"` needed the identical translation added to
  both dicts, but that won't always be the case (see the
  `"lbfgs"`/`"fixed_point"` vs `"error_gradient"`/`"linear_mixing"` split
  above).

## Adding a ql-* script

`utilities/ql-*` scripts are never imported, only launched as subprocesses
by `execute_script()` against `.OUT` files a handler just wrote in the
scratch dir. Write the `.OUT` file from `<mode>.py`/`common.py`, then
add/extend a script to read and plot it (`utilities/_pv3d.py` if it's a
3D/PyVista view — import it via `sys.path.insert(0, dirname)`, same as
every other `ql-*` script finds its own directory).

### Unit-cell outline on structure plots

Every `show_structure`/`show_structure_3d` handler follows the same
`g = get_geometry(); nsuper = int(get("nsuper_struct")); g =
g.supercell(nsuper); g.write()` pattern — the geometry gets enlarged to
an `nsuper`-repeated supercell *before* `g.write()` runs, purely so the
on-screen plot shows more than one cell. `common.write_unit_cell(g)`,
called on the *primitive* `g` right before that `supercell()` call,
writes `CELL.OUT`/`DIMENSIONALITY.OUT` (via pyqula's own
`geometrytk.write.write_lattice`) from the un-enlarged geometry, so a
plotting script can outline one real unit cell instead of the whole
displayed supercell. `utilities/_cell.py` (`read_cell()`,
`cell_edges()`, `cell_1d_ticks()`) turns those two files into a list of
edges to draw — `cell_edges()` for dim 2/3 (a parallelogram/
parallelepiped anchored at the origin), `cell_1d_ticks()` for dim 1
(two perpendicular tick marks bracketing the cell, since a bare segment
along `a1` would be indistinguishable from the chain of bonds itself).
`read_cell()` returns `None` for a finite/non-periodic geometry
(dimensionality 0, e.g. `0d`/`huge_0d`'s islands) so callers don't need
their own dimensionality check. `ql-structure-bond`/`ql-structure` (flat
and mpl-3D matplotlib views) plot the edges directly in `plotstyle.ACCENT`;
`ql-structure3d`/`ql-structure-tbg` (PyVista views) go through the new
`_pv3d.add_cell()` helper, which tubes the edges the same way
`add_bonds()` tubes atom-atom bonds. **Whenever a new structure-plotting
`ql-*` script is added for a periodic mode, wire it up the same way** —
call `write_unit_cell(g)` on the primitive geometry in the handler (if
not already done for that mode), then `_cell.read_cell()`/`cell_edges()`
in the script — rather than reading `LATTICE.OUT` directly, which (after
`g.write()` on the *supercell*) holds the enlarged, not primitive,
vectors.

## Testing

`tests/` (pytest; `pip install -r requirements-dev.txt`) is the automated
suite. Run it headlessly with `python -m pytest tests/` — `tests/conftest.py`
sets `QT_QPA_PLATFORM=offscreen` and the same `pysrc`/`tools` `sys.path`
bootstrap every mode script relies on, so no display is needed and no
other setup is required. Currently measured at ~25s wall clock and
~760MB peak RSS for the whole suite (115 passed, 5 skipped as of this
writing) — comfortably inside a self-imposed budget of **under 3 minutes
and under 2GB**, which exists because pyqula's numba-jitted kernels are
expensive to touch broadly (see point 3 below); keep both budgets in mind
before widening any layer. It's layered, cheapest/most-general first:

1. **`test_signal_wiring.py`/`test_shell.py`** — thin pytest wrappers
   around `tools/smoke_test.py`'s existing `check_signal_wiring()`/
   `check_shell()` (still also runnable standalone as `python
   tools/smoke_test.py`, including its per-mode dynamic `check_launches()`
   check that this suite deliberately omits - see below). Static
   button-wiring regex check per mode, plus one dynamic "does the shell +
   its initial page reach the Qt event loop without crashing" check.
   `check_launches()` (launching each of the 15 modes standalone and
   waiting out its own 6s "still alive" timeout - ~90s total, by design)
   is *not* wrapped into the pytest suite: it would consume most of the
   time budget on its own for coverage `test_handlers.py`'s `import_mode()`
   already mostly subsumes (same top-level-code-runs-without-crashing
   check, just without waiting out `app.exec()`). Run
   `python tools/smoke_test.py` directly for that full per-mode dynamic
   check when you want it.
2. **`test_term_metadata.py`** — static, source-parsed checks that every
   term `common.py:set_formulas()` renders has a `TERM_TOOLTIPS` entry and
   an `interface-pyqt/logos/<term>.png`, and every `STANDARD_HANDLERS`
   button has a `BUTTON_TOOLTIPS` entry — the two "whenever you add X, add
   Y" rules documented above, enforced instead of just written down.
3. **`test_handlers.py`** (+ helper module `_handler_harness.py`) — the
   layer that actually calls handler functions, which is what catches a
   handler that only breaks once it runs with a real value (see the two
   bugs cited in its module docstring — both were invisible to layers 1-2,
   since neither exercises a button with non-default parameters).
   `import_mode(mode)` imports a mode the same way
   `bin/versions/quantum-lattice-pyqt`'s `load_mode()` does
   (`importlib.util.spec_from_file_location`, a fresh module name per
   call so re-importing the same mode doesn't hit `sys.modules`'s cache);
   `set_field()`/`set_combo()` write UI fields directly (not through
   `qtwrap.modify()`, which silently no-ops on a typo'd widget name —
   a test should fail loudly instead); `run_button()` calls
   `modobj.signals[name]()` directly, skipping `connect_clicks()`'s
   `QThread`/busy-lock wrapping (that machinery exists to keep the GUI
   responsive, not for correctness, so it isn't needed to test a handler
   in-process). Every test stubs `execute_script` (an autouse fixture) so
   these never spawn the real `ql-*` plotting subprocess — that's a
   deliberately separate, lower-value thing to test (needs a
   display/matplotlib backend) from "did the handler compute correctly."

   **This is the layer with a real time/memory cost, and it is easy to
   blow the budget without noticing** — pyqula's numba-jitted
   Hamiltonian-building/diagonalization kernels get freshly JIT-compiled
   *and executed* the first time a genuinely new geometry/dimensionality
   runs through a real `show_bands`/`show_dos`-style call, and that
   compiled code + whatever it allocated is never released for the life
   of the process (importing a mode alone is cheap, ~10-20MB marginal;
   it's calling its handlers for real that costs 100-250MB per *new*
   mode, measured). Two things learned the hard way, both now baked into
   the current design:
   - An earlier version ran every `STANDARD_HANDLERS` button
     (`show_chern`/`show_z2`/`show_qpi`/`show_fermi_surface`/
     `show_multildos`/`show_iets_qdos`/...) across all 15 modes. It ran
     for **hours** (1000%+ CPU, 2.6GB+ RSS) before being killed —
     `show_qpi`/`show_iets_qdos` in particular do real
     BZ-averaged/real-space-summed physics at default resolution (a
     100-point energy mesh times `qpi_nk` k-points for QPI; an RPA
     susceptibility map for IETS-QDOS, which also isn't a meaningful
     target without a converged SCF `H.V` in the first place - see its
     docstring). Not a wiring bug, just genuinely expensive work
     multiplied by 15 modes. `STANDARD_BUTTONS` in `test_handlers.py`
     is deliberately just `["show_bands", "show_dos"]` because of this.
   - A later version tried just those two buttons, but across all 15
     modes in one process — that alone pushed a single test run past a
     hard 2GB cgroup cap before finishing (confirmed via
     `systemd-run --user --scope -p MemoryMax=2G <cmd>`, which actually
     enforces and SIGKILLs on this machine — use this to verify any
     future widening, a plain `timeout` only bounds wall time, not
     memory). `pytest-forked` (each test in its own forked process, so
     JIT memory gets reclaimed between tests) fixes the memory problem
     but makes each test ~3x slower from fork/IPC overhead, which blew
     the time budget instead. Disabling JIT entirely
     (`NUMBA_DISABLE_JIT=1`) made individual calls so much slower it
     couldn't even finish within a few minutes. Neither is the fix here.

   The actual fix: `test_standard_handler_runs`'s generic smoke pass
   (`ALL_MODES` in `test_handlers.py`) only covers modes NOT already
   exercised by a targeted regression test below (`_REGRESSION_COVERED_MODES`)
   — no point paying twice for the same mode's real `show_bands` compile.
   Combined, the whole file now touches real `show_bands`/`show_dos`-class
   compute for every mode at most once. If you need to widen this layer
   (more modes, more buttons, or reintroduce something like `pytest-forked`
   for a specific expensive addition), **re-measure under the cgroup cap
   before trusting it** — a handful of individually-fast timings do not
   predict aggregate cost in one process, twice now.

   Bug-class regression coverage (the actually load-bearing part of this
   file, not the generic sweep): `test_nonzero_strain_does_not_crash`
   covers every mode from the strain-kwarg bug memory (`3d`/`2dslab`/
   `hybridfilm`) plus `test_hofstader1d_ti_changes_hamiltonian` for its
   unconditional variant; `test_kdos_bands_uses_nk_kbands_field` covers
   all 7 modes from the KDOS-bands-field bug memory (cheaply — it
   monkeypatches `kdos.kdos_bands()` itself, so it never pays for the
   real k-mesh sweep, only for `pickup_hamiltonian()`). When adding a new
   targeted regression: prefer asserting on the actual value (like
   `test_hofstader1d_ti_changes_hamiltonian`/
   `test_kdos_bands_uses_nk_kbands_field` do) rather than only "no
   exception raised" whenever the bug could be a wrong-value-not-a-crash
   - the latter would have missed hofstader1d's silent no-op.
4. **`test_pyqula_floor.py`** — a couple of direct-`pyqula` textbook
   tight-binding checks (graphene's Dirac point, etc.), no GUI at all.
   Automated version of the "skim `git diff --stat pysrc/pyqula`" step
   `tools/update_pyqula.sh`'s own instructions already ask for by hand —
   run this after any vendored-pyqula refresh.

No CI currently runs this suite automatically (no `.github/` in this
repo) — for now it's a local/manual `python -m pytest tests/` run, the
same "no test suite, verification is manual" situation `CLAUDE.md`
describes, just with faster/more automatable building blocks than a full
GUI click-through. If that changes, the natural shape is a workflow that
just runs `python -m pytest tests/` under `QT_QPA_PLATFORM=offscreen` (no
`xvfb`/real display needed, same as the suite already runs locally) on
push/PR — ideally still wrapped in a memory cap (e.g. the `systemd-run`
form above, or CI-native equivalent) given how easily layer 3 can regress
past it.

## Known gotchas

- **`qfluentwidgets.ComboBox` is not a `QComboBox` subclass** - it's built
  on `QPushButton` (a custom-drawn Fluent dropdown, not a native Qt combo
  popup); its `ComboBoxBase` mixin provides the familiar
  `currentText()`/`setCurrentText()`/`addItems()`/`activated`/... surface,
  but `isinstance(obj,QtWidgets.QComboBox)` is `False` for one. Three
  places in `pysrc/interfacetk/` used to check only
  `isinstance(obj,QtWidgets.QComboBox)` when scanning a page's widgets by
  type (`qtwrap.py`'s `_connect_dirty_tracking()` and `save_interface()`,
  `scfterms.py`'s SCF-dirty-tracking sweep) - each silently skipped every
  promoted combobox on the page (`lattice`, `hamiltonian_type`,
  `scf_initialization`, `dos_mode`, ...): comboboxes never marked a page
  dirty, never marked an SCF result stale on their own, and were silently
  missing from every `save_interface()` snapshot (so from every "Save
  results", too - a combobox's value was never actually restored by "Load
  results" either, since it was never saved in the first place). Found
  while building the subprocess-based cancellation mechanism above, whose
  `inputs.json` snapshot came back missing `lattice` entirely. Fixed by
  checking `isinstance(obj,(QtWidgets.QComboBox,ComboBox))` (`ComboBox`
  imported from `qfluentwidgets`) at all three sites - a widget-type-by-type
  scan of `inspect.getmembers(...)` anywhere else in this codebase should
  use the same combined check, not just `QtWidgets.QComboBox` alone.
- **Busy-lock signal reentrancy**: `qtwrap.py`'s `release_busy()` fires a
  synchronous same-thread signal — mutate any state that depends on "am I
  busy" *before* releasing the lock, not after, or a handler triggered by
  the release can observe stale state. This also means anything that must
  happen unconditionally (reporting an error, showing an InfoBar) has to
  run *before* `release_busy()`, not after — a reentrant rebuild triggered
  by the release can itself raise and abort whatever comes after it. See
  `qtwrap.py::_on_runner_error()`, `_LazyPage.ensure_built()`, and
  `bin/versions/quantum-lattice-pyqt`'s `_on_update_noop`/`_on_update_error`
  for the established "report, then release" ordering.
- **`qtwrap.form`/`getbox()` resolve against the shell's currently
  *visible* page, not necessarily the page a callback logically belongs
  to** — safe from a live widget signal (only the visible page's widgets
  can receive a click) or during a page's own construction, but not from
  a callback that can run later on the GUI thread after a marshaled
  cross-thread call (`@_gui_thread_only`) or a reentrant busy-lock release
  (previous bullet), by which point the shell may have navigated
  elsewhere. `hybridparts.connect()`'s `on_new_part` callback takes the
  page's own `form` as an explicit argument for exactly this reason — a
  new callback wired through shared per-page state should follow the same
  pattern instead of reading `qtwrap.form`/`getbox()` directly.
- **The QTabWidget naming trap** above — always verify tab parentage via
  generated `interface.py`, never via `.ui` XML adjacency.
- **Term key vs. field object name** — `common.py:set_formulas()`'s
  `terms` list uses a term's logical name (e.g. `"hopping"`,
  `"fermi_impurity"`) to look up tooltip/highlight targets, but several
  `interface.ui` fields aren't actually named that: the hopping field is
  `"hoppings"` everywhere, and `impurity_embedding`/`ribbon_embedding` name
  their impurity fields `"impurity_potential"`/`"impurity_exchange"`
  (reversed word order from `"fermi_impurity"`/`"exchange_impurity"`).
  `termhighlight.find_term_field()` knows about these three via its
  `FIELD_ALIASES` table, so highlighting still reaches the real field —
  but `qtwrap.set_tooltip(term,...)`'s own `form.findChild(...,term)`
  lookup does not use that table, so it still silently no-ops on the field
  itself for these three (only the `<term>_image` label gets the tooltip)
  — a pre-existing gap `FIELD_ALIASES` doesn't attempt to fix. A new term
  with the same kind of mismatch either needs its own `FIELD_ALIASES`
  entry (highlighting only) or, better, should just be named to match its
  term key in `interface.ui` in the first place.
- **Serial vs. parallel execution is a single shell-wide flag, not a
  per-mode widget** — `qtwrap.is_parallel_execution()`/
  `set_parallel_execution()` back a single "Parallel execution" switch in
  the shell's nav panel (`bin/versions/quantum-lattice-pyqt`'s
  `_add_parallel_switch`, same pattern as `_add_interface_theme_switch`/
  `_add_plot_theme_switch`), and `common.py:check_parallel(qtwrap)` reads
  that flag to set `pyqula.parallel.cores` before every calculation that
  calls it. Defaults to serial (`cores = 1`). `tbg` used to have its own
  per-mode "Parallelization" combo box (`use_parallelization`) driving an
  identical local `check_parallel()` in `tbg.py` — that widget was removed
  from `tbg/interface.ui` (regenerate via `tools/convert_ui.sh` after any
  such removal) and `tbg.py`'s `check_parallel()` now just delegates to
  `common.check_parallel(qtwrap)`, so the one shell-wide switch governs
  every mode uniformly. A future mode should never add its own
  parallelization widget — call `common.check_parallel(qtwrap)` instead.
- **Never name an `interface.ui` widget after a `QWidget`/`QObject`
  method** (`width`, `height`, `size`, `font`, `pos`, `parent`, `close`,
  `children`, ...) — `pyside6-uic` generates `self.<name> = <WidgetType>(...)`
  on the page object for every named widget, and a name matching a Qt
  method silently shadows the real bound method on that page instance
  (`self.width` becomes a `LineEdit`, not a bound method returning the
  page's pixel width). This isn't just a theoretical footgun for code in
  this repo that might call `window.width()` — third-party code the page
  gets handed to can hit it too: `qfluentwidgets`' `InfoBar._adjustText()`
  calls `self.parent().width()` to size itself against whatever it's
  parented to, so *any* `InfoBar.warning()/.error()/...` call with
  `parent=<a page with a "width" field>` raised `TypeError: 'LineEdit'
  object is not callable` deep inside `qfluentwidgets`, on every mode
  that had a ribbon-`"width"` field (`1d`, `0d`, `hofstader1d`,
  `hybridribbon`, `ribbon_embedding`) and `huge_0d`'s `"size"` field.
  Because `qtwrap.py`'s `_on_runner_cancelled`/`_on_runner_error` reported
  via `InfoBar` *before* calling `release_busy()` (see the busy-lock
  reentrancy bullet above), that raised exception aborted the handler
  before the busy lock was ever released — so cancelling a calculation
  (or any calculation failing) on one of those modes left the shell-wide
  busy lock stuck forever, silently refusing every future click
  ("Another calculation is currently running") until the app was
  restarted. Fixed by renaming the colliding fields (`width` →
  `ribbon_width`, `size` → `island_size`) and, as defense in depth against
  the same class of bug recurring some other way, wrapping the `InfoBar`
  report call in both handlers in `try/except` so `release_busy()` always
  runs even if the report itself raises. When adding a field to
  `interface.ui`, prefer a more specific name (`ribbon_width`, `nk_bands`,
  ...) over a bare Qt-method-shaped one.
