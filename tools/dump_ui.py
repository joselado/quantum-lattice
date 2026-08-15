#!/usr/bin/env python3
"""Dump what a mode's page actually looks like, headless, as text + PNGs.

Reading interface.ui (or the generated interface.py) does NOT tell you what
a mode's page really contains: the Designer XML is only the starting point,
and four separate layers mutate the page at runtime after it's built -
common.set_formulas()'s _ensure_formula_image() injects formula columns,
scfterms.py nests a whole tab widget inside the mean-field tab,
hybridparts.py grows per-part tabs, and latticeterms.connect() hides
widgets that don't apply to the currently selected lattice. So the only
reliable description of a page is a *built* page.

This script builds the real page the same way the shell does (imports
interface-pyqt/<mode>/<mode>.py, whose blocking window.run() is guarded
behind `if __name__ == "__main__"`), under QT_QPA_PLATFORM=offscreen so no
display is needed, and writes:

  <out>/<mode>.txt                      indented widget tree (the primary
                                        artifact - diffable, stable order)
  <out>/png/<mode>__<tabs>__<tab>.png   one render per tab of every tab
                                        widget on the page

Only one tab of a QTabWidget is ever on screen, so a single screenshot
shows a small fraction of a mode. The PNG pass walks every tab of every
tab widget (setting each ancestor tab widget to the page containing it
first, so nested tabs render correctly) and grabs one image per tab.

Visibility in the text tree is reported as `hidden` from QWidget.isHidden(),
i.e. *explicitly* hidden (what latticeterms.connect() does), deliberately
not isVisible(), which is also false for everything on a non-current tab and
would drown that signal. Geometry is recorded during the tab walk, at the
moment each widget is actually laid out and on screen; widgets never
reached (e.g. a page inside a tab that is itself never made current) have
no geometry and are printed without one.

Usage:
    python tools/dump_ui.py                  # every mode, into the default out dir
    python tools/dump_ui.py 2d tmdc          # specific modes
    python tools/dump_ui.py --out DIR 2d     # choose the output directory
    python tools/dump_ui.py --no-png 2d      # text tree only (much faster)

Each mode is dumped in its own subprocess (a mode's import chdirs into its
own scratch folder and takes over qtwrap's active-page pointer, and a mode
that fails to build shouldn't take the rest of the run down with it).
"""
import argparse
import os
import subprocess
import sys

QLROOT = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/..")
DEFAULT_OUT = os.path.join(QLROOT, "ui_dump")

WINDOW_SIZE = (1400, 900)


# ---------------------------------------------------------------- subprocess

def _offscreen_env():
    """Same offscreen setup tools/smoke_test.py uses, including the plugin
    path fallback some installs need to find PySide6's bundled platforms."""
    import PySide6
    env = dict(os.environ)
    env["QT_QPA_PLATFORM"] = "offscreen"
    plugin_dir = os.path.join(os.path.dirname(PySide6.__file__), "Qt", "plugins", "platforms")
    if os.path.isdir(plugin_dir):
        env["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_dir
    return env


def dump_mode_subprocess(mode, outdir, png, theme, timeout=300):
    """Run this same script with --single <mode> in a child process."""
    cmd = [sys.executable, os.path.realpath(__file__), "--single", mode,
           "--out", outdir, "--theme", theme]
    if not png:
        cmd.append("--no-png")
    try:
        proc = subprocess.run(cmd, cwd=QLROOT, env=_offscreen_env(), text=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              timeout=timeout)
    except subprocess.TimeoutExpired:
        return ["%s: timed out after %ds" % (mode, timeout)]
    if proc.returncode != 0:
        tail = (proc.stderr or "").strip().splitlines()[-6:]
        return ["%s: failed (exit %d): %s" % (mode, proc.returncode, " | ".join(tail))]
    sys.stdout.write(proc.stdout)
    return []


# ------------------------------------------------------------- page building

def build_page(mode):
    """Import interface-pyqt/<mode>/<mode>.py and return its built page.

    Mirrors load_mode() in bin/versions/quantum-lattice-pyqt: a unique
    module name per mode, the mode dir on sys.path (for modes with sibling
    modules, e.g. huge_0d's handlers.py), and modobj.window as the page.
    """
    import importlib.util
    moddir = os.path.join(QLROOT, "interface-pyqt", mode)
    script = os.path.join(moddir, mode + ".py")
    if not os.path.exists(script):
        raise SystemExit("no such mode: %s (%s not found)" % (mode, script))
    if moddir not in sys.path:
        sys.path.insert(0, moddir)
    spec = importlib.util.spec_from_file_location("dump_mode_" + mode, script)
    modobj = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = modobj
    spec.loader.exec_module(modobj)
    return modobj.window


# --------------------------------------------------------------- tab walking

def _tab_widgets(root):
    """Every QTabWidget under root, ancestors before descendants, so a
    nested tab widget (e.g. the one scfterms.py puts inside the mean-field
    tab) is only visited after the tab containing it can be made current."""
    from PySide6 import QtWidgets
    tws = root.findChildren(QtWidgets.QTabWidget)

    def depth(w):
        n, p = 0, w.parentWidget()
        while p is not None:
            n, p = n + 1, p.parentWidget()
        return n
    return sorted(tws, key=depth)


def _reveal(tw, root):
    """Make `tw` reachable on screen by pointing every ancestor tab widget
    at the tab page that contains it. Returns the tab-text trail, outermost
    first, used to name the PNGs."""
    from PySide6 import QtWidgets
    trail = []
    chain = []
    w = tw.parentWidget()
    while w is not None and w is not root.parentWidget():
        chain.append(w)
        w = w.parentWidget()
    for anc in reversed(chain):  # outermost first
        if not isinstance(anc, QtWidgets.QTabWidget):
            continue
        # which of anc's pages contains tw?
        for i in range(anc.count()):
            page = anc.widget(i)
            if page is not None and (page is tw or page.isAncestorOf(tw)):
                anc.setCurrentIndex(i)
                trail.append(anc.tabText(i))
                break
    return trail


def _sanitize(s):
    keep = [c if (c.isalnum() or c in "-_") else "-" for c in s.strip()]
    return "".join(keep).strip("-").replace("--", "-") or "untitled"


def walk_tabs(root, on_state):
    """Set every tab of every tab widget current in turn, calling
    on_state(label) once per state with a filename-safe label. Always
    fires at least once, even for a page with no tab widgets."""
    from PySide6 import QtWidgets
    app = QtWidgets.QApplication.instance()
    tws = _tab_widgets(root)
    if not tws:
        app.processEvents()
        on_state("page")
        return
    for tw in tws:
        trail = _reveal(tw, root)
        name = tw.objectName() or tw.metaObject().className()
        for i in range(tw.count()):
            tw.setCurrentIndex(i)
            app.processEvents()
            parts = [_sanitize(t) for t in trail] + [_sanitize(name), _sanitize(tw.tabText(i))]
            on_state("__".join(parts))


# ---------------------------------------------------------------- text tree

def _describe(w):
    """One-line description of a widget's own content: its text, its items,
    its checked state - whatever it actually shows the user."""
    from PySide6 import QtWidgets
    bits = []
    # duck-typed, not isinstance(QComboBox): qfluentwidgets' promoted
    # ComboBox is not a QComboBox subclass (it derives from a button), but
    # it does carry the currentText()/itemText()/count() API that
    # qtwrap.getbox() drives it through.
    if hasattr(w, "currentText") and hasattr(w, "itemText") and not isinstance(w, QtWidgets.QTabWidget):
        items = [w.itemText(i) for i in range(w.count())]
        bits.append("current=%r" % w.currentText())
        if items:
            bits.append("items=[%s]" % ", ".join(repr(i) for i in items))
    elif isinstance(w, (QtWidgets.QCheckBox, QtWidgets.QRadioButton)):
        bits.append("text=%r" % w.text())
        bits.append("checked=%s" % w.isChecked())
    elif isinstance(w, QtWidgets.QLineEdit):
        bits.append("value=%r" % w.text())
        if w.placeholderText():
            bits.append("placeholder=%r" % w.placeholderText())
    elif isinstance(w, QtWidgets.QLabel):
        pm = w.pixmap()
        if pm is not None and not pm.isNull():
            bits.append("pixmap=%dx%d" % (pm.width(), pm.height()))
        if w.text():
            bits.append("text=%r" % w.text())
    elif isinstance(w, QtWidgets.QGroupBox):
        bits.append("title=%r" % w.title())
    elif isinstance(w, QtWidgets.QTabWidget):
        bits.append("tabs=[%s]" % ", ".join(repr(w.tabText(i)) for i in range(w.count())))
    elif isinstance(w, QtWidgets.QAbstractButton):
        bits.append("text=%r" % w.text())
    elif isinstance(w, (QtWidgets.QSpinBox, QtWidgets.QDoubleSpinBox)):
        bits.append("value=%s" % w.value())
    return bits


def _layout_of(w):
    """'grid 3x2' / 'vbox' / 'hbox' - which layout this widget imposes on
    its children. Matters because common.py's _ensure_formula_image() only
    injects a formula column into a QGridLayout."""
    from PySide6 import QtWidgets
    lay = w.layout()
    if lay is None:
        return None
    if isinstance(lay, QtWidgets.QGridLayout):
        return "grid %dx%d" % (lay.rowCount(), lay.columnCount())
    if isinstance(lay, QtWidgets.QVBoxLayout):
        return "vbox"
    if isinstance(lay, QtWidgets.QHBoxLayout):
        return "hbox"
    if isinstance(lay, QtWidgets.QFormLayout):
        return "form"
    return lay.metaObject().className()


def write_tree(root, geoms, path, mode):
    """Emit the indented widget tree. Child order is Qt's own child order,
    which is construction order and therefore stable across runs."""
    from PySide6 import QtWidgets
    lines = [
        "# widget tree for mode %r, built headless by tools/dump_ui.py" % mode,
        "# `hidden` = QWidget.isHidden(), i.e. explicitly hidden (latticeterms.connect()",
        "#   and friends), NOT merely on a non-current tab.",
        "# geometry is x,y,w,h in window coordinates, recorded while the widget was",
        "#   laid out and on screen; widgets never reached during the tab walk have none.",
        "# tab=... marks a widget that is a page of its parent QTabWidget.",
        "",
    ]

    def rec(w, indent, tab_label=None):
        cls = w.metaObject().className()
        name = w.objectName()
        head = "%s%s" % ("  " * indent, cls)
        if name:
            head += " %s" % name
        bits = []
        if tab_label is not None:
            bits.append("tab=%r" % tab_label)
        # a page of a QStackedWidget/QTabWidget is hidden by Qt itself
        # whenever it isn't the current one - structural, not a real
        # "this term doesn't apply here" hide, so don't report it
        stacked = isinstance(w.parentWidget(), QtWidgets.QStackedWidget)
        if w.isHidden() and not stacked:
            bits.append("hidden")
        lay = _layout_of(w)
        if lay:
            bits.append(lay)
        g = geoms.get(id(w))
        if g:
            bits.append("geom=%d,%d %dx%d" % g)
        bits += _describe(w)
        tip = w.toolTip()
        if tip:
            flat = " ".join(tip.split())
            bits.append("tooltip=%r" % (flat[:80] + ("..." if len(flat) > 80 else "")))
        if bits:
            head += "  [%s]" % "; ".join(bits)
        lines.append(head)
        if isinstance(w, QtWidgets.QTabWidget):
            pages = {}
            for i in range(w.count()):
                page = w.widget(i)
                if page is not None:
                    pages[id(page)] = w.tabText(i)
            for c in w.children():
                if isinstance(c, QtWidgets.QWidget):
                    rec(c, indent + 1, pages.get(id(c)))
            return
        for c in w.children():
            if isinstance(c, QtWidgets.QWidget):
                rec(c, indent + 1)

    rec(root, 0)
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return len(lines)


# -------------------------------------------------------------------- single

def dump_single(mode, outdir, png, theme="dark"):
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6 import QtWidgets
    from interfacetk import qtwrap

    qtwrap.ensure_app()
    app = QtWidgets.QApplication.instance()
    # the shell sets both of these once at startup (see
    # bin/versions/quantum-lattice-pyqt); a mode imported on its own
    # doesn't, and would otherwise dump in the stock light theme rather
    # than the one users actually see
    import qfluentwidgets
    qfluentwidgets.setTheme(qfluentwidgets.Theme.DARK if theme == "dark"
                            else qfluentwidgets.Theme.LIGHT)
    os.environ["QL_THEME"] = theme
    if theme == "dark":
        # setTheme() alone gives white ink on a white page here: in the real
        # app the shell makes each page transparent and the FluentWindow
        # behind it paints the dark ground (see quantum-lattice-pyqt's
        # setStyleSheet("QWidget { background: transparent; }")). A page
        # dumped on its own has no such ground, so supply one via the
        # palette, which unstyled QWidgets fall back to.
        from PySide6 import QtGui
        pal = app.palette()
        for role, col in ((QtGui.QPalette.ColorRole.Window, "#272727"),
                          (QtGui.QPalette.ColorRole.Base, "#2b2b2b"),
                          (QtGui.QPalette.ColorRole.Button, "#2b2b2b"),
                          (QtGui.QPalette.ColorRole.WindowText, "#e8e8e8"),
                          (QtGui.QPalette.ColorRole.Text, "#e8e8e8"),
                          (QtGui.QPalette.ColorRole.ButtonText, "#e8e8e8")):
            pal.setColor(role, QtGui.QColor(col))
        app.setPalette(pal)
    window = build_page(mode)
    qtwrap.set_active(window)
    window.resize(*WINDOW_SIZE)
    window.show()
    app.processEvents()

    os.makedirs(outdir, exist_ok=True)
    pngdir = os.path.join(outdir, "png")
    if png:
        os.makedirs(pngdir, exist_ok=True)

    geoms = {}
    shots = []

    def on_state(label):
        for w in window.findChildren(QtWidgets.QWidget):
            if w.isVisible():
                p = w.mapTo(window, w.rect().topLeft())
                geoms[id(w)] = (p.x(), p.y(), w.width(), w.height())
        if png:
            path = os.path.join(pngdir, "%s__%s.png" % (mode, label))
            window.grab().save(path)
            shots.append(path)

    walk_tabs(window, on_state)

    treepath = os.path.join(outdir, mode + ".txt")
    n = write_tree(window, geoms, treepath, mode)
    print("%s: %s (%d lines)%s" % (mode, os.path.relpath(treepath, QLROOT), n,
                                   ", %d png" % len(shots) if png else ""))


# ---------------------------------------------------------------------- main

def _all_modes():
    """The mode list tools/smoke_test.py already keeps in sync with the
    shell's MODES, imported rather than duplicated here."""
    sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
    import smoke_test
    return list(smoke_test.MODES)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("modes", nargs="*", help="modes to dump (default: all)")
    ap.add_argument("--out", default=DEFAULT_OUT, help="output directory (default: %s)" % DEFAULT_OUT)
    ap.add_argument("--no-png", action="store_true", help="text tree only, no screenshots")
    ap.add_argument("--theme", choices=["dark", "light"], default="dark",
                    help="theme to render in (default: dark, as the shell ships)")
    ap.add_argument("--single", help=argparse.SUPPRESS)  # internal: dump one mode in-process
    args = ap.parse_args()

    sys.path.append(os.path.join(QLROOT, "pysrc"))
    outdir = os.path.realpath(args.out)

    if args.single:
        dump_single(args.single, outdir, not args.no_png, args.theme)
        return

    modes = args.modes or _all_modes()
    failures = []
    for mode in modes:
        failures += dump_mode_subprocess(mode, outdir, not args.no_png, args.theme)
    print()
    if failures:
        print("FAILED (%d):" % len(failures))
        for f in failures:
            print(" -", f)
        sys.exit(1)
    print("OK: dumped %d mode(s) into %s" % (len(modes), outdir))


if __name__ == "__main__":
    main()
