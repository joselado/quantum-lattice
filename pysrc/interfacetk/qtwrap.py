###############################################
###############################################
###############################################
#### This file has simple wrappers to Qt (PySide6) ####
###############################################
###############################################
###############################################



import os

# This app's widgets (QDialog/QMainWindow/...) are always PySide6. matplotlib's
# Qt-based backends (backend_qtagg, used by plotpyqt.py to embed figures in
# those same dialogs) pick their own Qt binding via the QT_API env var, and a
# user may have QT_API=pyqt5 set globally in their shell (e.g. to make plain,
# non-quantum-lattice matplotlib scripts work against a conda-installed PyQt5 -
# see the qt.conf note below). Mixing a PyQt5-backed canvas into a PySide6
# QDialog doesn't work, so force this process to PySide6 unconditionally
# (plain assignment, not setdefault) regardless of what's set outside it.
os.environ["QT_API"] = "pyside6"

# Some systems (notably conda envs that also have PyQt5/Qt5 installed
# alongside PySide6) ship a stray qt.conf next to the Python executable
# (e.g. <conda-prefix>/bin/qt.conf) that redirects Qt's plugin search path
# to that other, incompatible Qt install ("Could not find the Qt platform
# plugin xcb/wayland" even though the plugin files are physically present,
# because Qt refuses to load a plugin built against a different Qt version).
# Force PySide6's own bundled plugins to take priority, before QApplication
# is ever constructed. os.environ.setdefault so an explicit user override
# of these variables is still respected.
try:
    import PySide6 as _PySide6
    _plugins_dir = os.path.join(os.path.dirname(_PySide6.__file__), "Qt", "plugins")
    if os.path.isdir(_plugins_dir):
        os.environ.setdefault("QT_PLUGIN_PATH", _plugins_dir)
        _platforms_dir = os.path.join(_plugins_dir, "platforms")
        if os.path.isdir(_platforms_dir):
            os.environ.setdefault("QT_QPA_PLATFORM_PLUGIN_PATH", _platforms_dir)
except ImportError:
    pass

from PySide6 import QtWidgets  # Import the PySide6 module we'll need
from PySide6.QtGui import QPixmap, QPainter, QColor
from PySide6.QtCore import Qt, QThread, QObject, Signal
import sys  # We need sys so that we can pass argv to QApplication
import numpy as np
import time
import inspect
import json
import importlib.util
import threading
import traceback

from numpy import * # this may not be a good idea
from .debugging import holler
from . import termhighlight
from qfluentwidgets import InfoBar, InfoBarPosition, IndeterminateProgressBar
from qfluentwidgets import qconfig, isDarkTheme
from qfluentwidgets import SwitchButton
from qfluentwidgets import MessageBoxBase, MessageBox, SubtitleLabel, LineEdit, ComboBox

QtGui = QtWidgets
app = None  # the single QApplication for the whole process, built lazily
form = None  # the currently *active* page - the one whose widgets get/getbox/
             # modify/etc. resolve against. Only one page can be visible/
             # clickable at a time (whether it's a standalone mode window or
             # the page currently shown by the shell's navigation), so a
             # single "active page" pointer is enough even with several
             # pages' widgets alive in the same process.


def ensure_app():
    """Return the process-wide QApplication, creating it on first use.
    Every mode shares this same instance instead of each constructing its
    own, since several pages/modes can now live in one process. Also
    builds the singleton used to marshal widget access back onto this
    thread (see _MainThreadCaller below) - always safe to do here since
    ensure_app() is only ever called from the main thread, before any
    worker thread (see _HandlerRunner) can exist."""
    global app,_main_caller
    if app is None:
        existing = QtWidgets.QApplication.instance()
        app = existing if existing is not None else QtWidgets.QApplication(sys.argv)
    if _main_caller is None:
        _main_caller = _MainThreadCaller()
    return app


# --- Background execution & thread-safe widget access -------------------
#
# connect_clicks() (below) runs each button's handler on its own worker
# QThread instead of blocking the GUI thread, so the shell (and every
# other open page) stays responsive during a calculation instead of
# freezing solid until it finishes.
#
# Handler code (interfacetk/common.py, every <mode>.py) freely calls
# get()/getbox()/modify()/is_checked()/... at arbitrary points in its
# body, interleaved with the actual computation - rewriting every handler
# to gather inputs up front would be a much bigger change. Instead, each
# of those free functions detects when it has been called off the GUI
# thread and transparently re-runs itself on the GUI thread through a
# blocking queued Qt signal, waiting for the result - so handler code
# keeps working unmodified regardless of which thread it happens to run
# on.
class _MainThreadCaller(QObject):
    """Lives on the GUI thread. Runs an arbitrary callable there on behalf
    of a worker thread and blocks the caller until it's done."""
    _request = Signal(object,object,object,object) # fn,args,kwargs,box - kept as
    # plain `object` (not typed tuple/dict) so PySide6 passes the exact same
    # Python objects through, not a marshaled copy: `box` must stay the same
    # dict instance so call() sees _handle()'s writes into it after emit()
    # returns.
    def __init__(self):
        super().__init__()
        self._request.connect(self._handle,Qt.ConnectionType.BlockingQueuedConnection)
    def _handle(self,fn,args,kwargs,box):
        try: box["result"] = fn(*args,**kwargs)
        except Exception as e: box["error"] = e
    def call(self,fn,*args,**kwargs):
        box = {}
        self._request.emit(fn,args,kwargs,box) # blocks until _handle returns
        if "error" in box: raise box["error"]
        return box.get("result")


_main_caller = None # built by ensure_app(), always on the GUI thread


def _gui_thread_only(fn):
    """Decorator for a free function that already receives its target page
    explicitly (save_interface/load_interface - see below), so no page
    substitution is needed here: run it directly if already on the GUI
    thread (the common case - no overhead beyond one thread-identity
    check), otherwise marshal the call onto the GUI thread and block the
    calling worker thread until it returns."""
    def wrapper(*args,**kwargs):
        if QThread.currentThread() is app.thread():
            return fn(*args,**kwargs)
        return _main_caller.call(fn,*args,**kwargs)
    return wrapper


# get()/getbox()/modify()/... (unlike save_interface/load_interface) don't
# take their target page as an explicit argument - they resolve it
# implicitly, historically always via the single module-global `form`.
# That's correct for direct GUI-thread calls (page construction, a
# handler's own page while nothing else is happening), but not for a
# handler running on its worker thread: handler code calls get()/getbox()
# at arbitrary points "interleaved with the actual computation" (see
# _HandlerRunner below), and if the user navigates the shell to a
# different page while that handler is still running, set_active() (used
# by the shell's own navigation, see bin/versions/quantum-lattice-pyqt's
# _on_page_changed()) repoints the global `form` at the newly-shown page -
# so the running handler's *later* get()/getbox() calls would silently
# start reading that other page's widgets instead of its own.
#
# _handler_local (set for the duration of one _HandlerRunner.run(), see
# below) records which page a worker thread's in-flight handler belongs
# to. _current_page() prefers that over the global `form` when present.
# Resolution has to happen on the CALLING thread (via _form_thread_only,
# not inside the wrapped function itself) because a marshaled call's body
# actually executes on the GUI thread inside _MainThreadCaller._handle(),
# by which point the identity of the worker thread that asked is already
# lost - reading _handler_local there would just see the GUI thread's own
# (always-empty) thread-local storage.
_handler_local = threading.local()


def _current_page():
    return getattr(_handler_local,"page",None) or form


def _form_thread_only(fn):
    """Like _gui_thread_only, but for the free functions that implicitly
    resolve their target page (see _current_page() above): resolves the
    page on the calling thread before any marshaling, and passes it into
    `fn` as an explicit leading argument, so a handler's widget access
    stays pinned to the page it belongs to even if the shell navigates
    elsewhere on the GUI thread while it's still running."""
    def wrapper(*args,**kwargs):
        page = _current_page()
        if QThread.currentThread() is app.thread():
            return fn(page,*args,**kwargs)
        return _main_caller.call(fn,page,*args,**kwargs)
    return wrapper


# Only one handler - across every mode/page in the shell - may run at a
# time. pyqula's own I/O is cwd-relative (see qlinterface.create_folder()),
# so letting two handlers, or a handler and the chdir a not-yet-built
# page performs once at construction time, run concurrently on different
# threads would let their os.chdir() calls race and write results into
# the wrong page's scratch folder. A single process-wide flag is enough
# since only one click (or one page build) needs to hold it at a time.
_busy_lock = threading.Lock()


class _BusySignals(QObject):
    became_free = Signal()


_busy_signals = _BusySignals()


def is_busy():
    """Whether some handler (or page build - see try_acquire_busy()) is
    currently running somewhere in the shell."""
    return _busy_lock.locked()


def try_acquire_busy():
    """Attempt to claim the process-wide busy lock without blocking.
    Returns True if it was free and is now held by the caller (who must
    call release_busy() when done), False if something else already holds
    it. Used both by a handler's click-starter (below) and by
    _LazyPage.ensure_built() (bin/versions/quantum-lattice-pyqt) before
    building a not-yet-visited page - building one chdirs into its own
    scratch folder just like a handler does, so the two must be mutually
    exclusive. Doing the check and the acquire as one atomic call (instead
    of is_busy() followed by a separate acquire) is what closes the race
    where both could pass a plain "is it free?" check at the same instant
    and then chdir concurrently."""
    return _busy_lock.acquire(blocking=False)


def release_busy():
    """Release the busy lock claimed by try_acquire_busy(), if held, and
    notify anything waiting on it via on_busy_free()."""
    if _busy_lock.locked():
        _busy_lock.release()
        _busy_signals.became_free.emit()


def on_busy_free(slot):
    """Connect `slot` (no args) to fire once the busy lock next becomes
    free - used by the shell to retry a page whose first-navigation build
    was deferred by ensure_built() because something else was running at
    the time (see _LazyPage in bin/versions/quantum-lattice-pyqt)."""
    _busy_signals.became_free.connect(slot)


def try_acquire_busy_or_warn(parent):
    """try_acquire_busy(), and if something else already holds the lock,
    show the same "please wait" InfoBar every busy-rejection uses - a
    button click via connect_clicks() below, and the shell's own "Update
    Quantum Lattice" nav item - so the wording can't drift between call
    sites. Returns whether the lock was acquired."""
    if try_acquire_busy():
        return True
    InfoBar.warning(title="Please wait",
        content="Another calculation is currently running - try again once it finishes",
        parent=parent,duration=4000,position=InfoBarPosition.TOP)
    return False


class _HandlerRunner(QThread):
    """Runs one button handler on a worker thread. Any widget access
    inside the handler hops back to the GUI thread transparently (see
    _gui_thread_only above) - the handler itself is unaware it isn't
    running on the GUI thread. Emits onto the page's own bound slots
    (_on_runner_ok/_on_runner_error) rather than plain closures so Qt
    recognizes the cross-thread call and auto-queues it back to the GUI
    thread instead of running the slot on this worker thread."""
    finished_ok = Signal(object) # emits self, so the page knows which runner finished
    finished_error = Signal(object,str) # emits self, full traceback text
    def __init__(self,fn,owner_page):
        super().__init__()
        self._fn = fn
        self.owner_page = owner_page # see _handler_local above
        self.robust = True # overwritten by the caller before start()
    def run(self):
        _handler_local.page = self.owner_page
        try:
            self._fn()
            self.finished_ok.emit(self)
        except Exception:
            self.finished_error.emit(self,traceback.format_exc())
        finally:
            del _handler_local.page



class _AppBase:
    """Mixin with all the behavior a mode's page needs, independent of
    which mode's generated Ui_MainWindow it's combined with (see
    new_page() below, which composes this with QMainWindow and a specific
    mode's interface.Ui_MainWindow per call)."""
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # this is defined in interface.py, generated by Qt Designer
        # It sets up layout and widgets that are defined
        self._params_dirty_time = time.time() # results are stale before this
        self._connect_dirty_tracking()
        self._runners = [] # worker threads kept alive (see connect_clicks) until they finish
        self._progress_bar = None
        self._progress_label = None
    def _connect_dirty_tracking(self):
        """Mark parameters as changed only on genuine user interaction,
        never on programmatic updates (e.g. a handler writing a computed
        value into a QLineEdit), so freshly computed results aren't
        mistaken for stale ones."""
        for name,obj in inspect.getmembers(self):
            if isinstance(obj,QtWidgets.QLineEdit):
                obj.textEdited.connect(self._mark_dirty)
            elif isinstance(obj,QtWidgets.QComboBox):
                obj.activated.connect(self._mark_dirty)
            elif isinstance(obj,(QtWidgets.QCheckBox,QtWidgets.QRadioButton)):
                obj.clicked.connect(self._mark_dirty)
    def _mark_dirty(self,*args):
        self._params_dirty_time = time.time()
    def reset_dirty(self):
        """Mark current results as valid for the current parameters"""
        self._params_dirty_time = time.time()
    def params_dirty_time(self):
        return self._params_dirty_time
    def save_interface(self,**kwargs):
        save_interface(self,**kwargs)
    def load_interface(self,*args,**kwargs):
        load_interface(self,*args,**kwargs)
    def run(self):
        """Show this page as its own standalone top-level window and block
        until it's closed - used only when a mode is launched directly
        (python interface-pyqt/<mode>/<mode>.py), not when it's embedded
        as a page in the shell."""
        set_active(self)
        self.show()
        ensure_app().exec()
    def get(self,*args,**kwargs):
        return get(*args,**kwargs)
    def set(self,*args):
        set_value(*args)
    def is_checked(self,*args,**kwargs):
        return is_checked(*args,**kwargs)
    def getbox(self,*args,**kwargs):
        return getbox(*args,**kwargs)
    def connect_clicks(self,ds,robust=True):
      """Connect the different functions. Each one now runs on its own
      worker thread (_HandlerRunner) instead of blocking the GUI, so the
      shell stays responsive and other pages remain usable while a
      calculation is in flight. Only one handler across the whole app may
      run at a time (see is_busy()/_busy_lock above) - a second click
      while one is running is refused with an InfoBar rather than queued,
      since queuing would just mean a second unpredictable wait.
      `robust` only controls how much detail reaches stdout on failure,
      matching each mode's existing choice (True: generic message, False:
      full traceback) - either way an InfoBar is now always shown in the
      window itself, so a failure is visible even without a terminal
      attached (e.g. launched from the desktop icon)."""
      for name,fn in ds.items():
          bu = getattr(self,name) # widget for this button
          bu.clicked.connect(self._make_click_starter(self._with_own_scratch_dir(fn),robust))

    def _make_click_starter(self,fn,robust):
        def start():
            if not try_acquire_busy_or_warn(self):
                return
            self._show_progress()
            runner = _HandlerRunner(fn,self) # self: the page this button belongs to
            runner.robust = robust
            self._runners.append(runner) # keep a live reference so Qt doesn't GC it mid-run
            runner.finished_ok.connect(self._on_runner_ok)
            runner.finished_error.connect(self._on_runner_error)
            runner.start()
        return start

    def _on_runner_ok(self,runner):
        self._cleanup_runner(runner)
        release_busy()

    def _on_runner_error(self,runner,tb):
        # report before release_busy(), not after: release_busy() fires a
        # synchronous same-thread signal that can reenter
        # _retry_pending_page()->ensure_built()->load_mode() right here
        # (see the busy-lock-reentrancy gotcha, and
        # bin/versions/quantum-lattice-pyqt's _on_update_noop/_on_update_error
        # which follow the same order for the same reason) - if that
        # reentrant call ever raises, it must not be able to swallow this
        # handler's own error report.
        self._cleanup_runner(runner)
        self._report_error(tb,runner.robust)
        release_busy()

    def _cleanup_runner(self,runner):
        self._hide_progress()
        if runner in self._runners: self._runners.remove(runner)

    def _ensure_progress_widgets(self):
        if self._progress_bar is not None: return
        bar = IndeterminateProgressBar(self)
        bar.setFixedWidth(140)
        bar.hide()
        label = QtWidgets.QLabel("")
        self.statusBar().addWidget(label)
        self.statusBar().addPermanentWidget(bar)
        self._progress_bar = bar
        self._progress_label = label

    def _show_progress(self):
        self._ensure_progress_widgets()
        self._progress_label.setText("Computing...")
        self._progress_bar.show()
        self._progress_bar.start()

    def _hide_progress(self):
        if self._progress_bar is None: return
        self._progress_bar.stop()
        self._progress_bar.hide()
        self._progress_label.setText("")

    def _report_error(self,tb,robust):
        stripped = tb.strip()
        last_line = stripped.splitlines()[-1] if stripped else "Something went wrong"
        InfoBar.error(title="Calculation failed",content=last_line,parent=self,
                      duration=6000,position=InfoBarPosition.TOP)
        if robust:
            if holler(): print("Something wrong happened")
        else:
            print(tb)
    def _with_own_scratch_dir(self,f):
        """Wrap a handler so it always runs with this page's own scratch
        folder as the process cwd. Several pages/modes can be loaded in
        the same process (the shell), and pyqula's own I/O is cwd-relative
        (see qlinterface.create_folder()), so the page that owns the
        button just clicked must re-establish its own folder before its
        handler runs, in case another page's handler (or another page's
        own construction, which also calls create_folder()) moved the
        process elsewhere in the meantime."""
        def wrapped(*args,**kwargs):
            if getattr(self,"scratch_dir",None):
                os.chdir(self.scratch_dir)
            return f(*args,**kwargs)
        return wrapped


def _load_ui_module(moddir):
    """Load a mode's generated interface.py under a name unique to that
    mode. Needed because every mode's interface.py defines the same class
    name (Ui_MainWindow); a plain `import interface` (as before the
    single-shell rewrite) only worked because each mode ran in its own
    process, so only one such module was ever loaded at a time."""
    modname = "_ql_interface_" + os.path.basename(os.path.normpath(moddir))
    spec = importlib.util.spec_from_file_location(modname,os.path.join(moddir,"interface.py"))
    ui_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ui_module)
    return ui_module


def new_page(moddir):
    """Build the page for the mode whose generated interface.py lives in
    moddir (typically os.path.dirname(__file__) of that mode's <mode>.py),
    and make it the active page - the one get()/getbox()/modify()/etc.
    below act on - until set_active() points elsewhere. Replaces the old
    main(), which built the sole App() for the whole (per-mode) process."""
    ensure_app()
    ui_module = _load_ui_module(moddir)
    cls = type("Page_"+ui_module.__name__,(_AppBase,QtGui.QMainWindow,ui_module.Ui_MainWindow),{})
    page = cls()
    set_active(page)
    return page


def set_active(page):
    """Point get()/getbox()/modify()/is_checked()/... at `page`. Called
    whenever a page is (re)built and whenever the shell switches which
    page is currently shown, since only the currently visible page's
    widgets can receive a click - so one active pointer is always enough."""
    global form
    form = page


def string2array(v):
    """Convert a string in an array"""
    try:
        v = complex(v) # if it is a number
        v = np.array([v])
        return v
    except:
        v = [complex(iv) for iv in v.split(",")]
        return np.array(v)
    return None


def array2string(v):
    """Convert an array to a string"""
    ss = ""
    ss += str(v[0])
    for i in range(1,len(v)): ss += ","+str(v[i])
    return ss


@_form_thread_only
def get_array(page,name,v0=[0.,0.,0.],**kwargs):
    """Get an array from a cell"""
    v = getattr(page,name).text() # get the text
    v = string2array(v) # convert to array
    if v is not None: return v # return the array
    else: # something wrong happened
        _modify_impl(page,name,array2string(v0)) # overwrite
        return np.array(v0) # return the default value


@_form_thread_only
def get(page,name,string=False,default=0.0,call=True):
  """Return a certain value"""
  try:
      obj = getattr(page,name) # get the object
      out = obj.text()
      if string: return out # return as string
      try: # if it is a number
          return float(out) # return as float
      except: # execute
          if call:
              if "import os" in out: raise # silly sanity check
              out = out.replace("\n","")
              a = eval("lambda r: "+out) # execute the string
              # try the function
              try:
                  a([0.,0.,0.])
                  return a
              except: raise
          else: raise
  except:
      if holler(): print(name,"not found, set to ",default)
      _modify_impl(page,name,default) # set this value
      return default



@_form_thread_only
def getbox(page,name):
  try:
    obj = getattr(page,name) # get the object
    return str(obj.currentText()) # return the text
  except:
    if holler(): print(name,"not found, set to None")
    return None


@_form_thread_only
def set_combobox(page,name,cs=[]):
    """Add the different colormaps to a combox"""
    try: cb = getattr(page,name)
    except:
        if holler(): print("Combobox",name,"not found")
        return
    cb.clear() # clear the items
    cb.addItems(cs)



def _modify_impl(page,name,text):
  """Raw implementation, called directly (bypassing the @_form_thread_only
  wrapper's page-resolution) by get()/get_array() above, which already
  know the right `page` and are guaranteed to already be running on the
  GUI thread at that point - re-resolving via _current_page() there would
  wrongly fall back to the global `form` instead of reusing the same page
  (see _form_thread_only's docstring)."""
  try:
    obj = getattr(page,name) # get the object
    out = obj.setText(str(text))
    app.processEvents() # update the interface
  except: pass

modify = _form_thread_only(_modify_impl)
set_value = modify

@_form_thread_only
def is_checked(page,name,default=False):
    try:
        obj = getattr(page,name) # get the object
        return obj.isChecked()
    except: return default



# set_image()/set_logo() are only ever used for the white-ink-on-transparent
# Hamiltonian-term formula PNGs (CLAUDE.md's formula-image convention,
# common.py:set_formulas()) - unlike the home page banner logo, which
# bin/versions/quantum-lattice-pyqt sets directly via QPixmap/setPixmap and
# never goes through here. Those PNGs are static bitmaps: setTheme() restyles
# every promoted qfluentwidgets widget's stylesheet live, but a baked-white
# pixmap doesn't participate in that, so on the light theme the "font" (it
# reads as text but is actually an image) stayed white and unreadable. Tint
# on every set_image() call, and re-tint every previously-set image label
# when the theme switch (bin/versions/quantum-lattice-pyqt's "Dark
# interface" switch) fires.
_themed_image_labels = [] # [(label, untinted-but-scaled pixmap), ...]


def _ink_color():
    return QColor(255,255,255) if isDarkTheme() else QColor(0,0,0)


def _tint_pixmap(pixmap,color):
    """Recolor every non-transparent pixel of `pixmap` to `color`, keeping
    its alpha channel - the source ink color doesn't matter going in."""
    tinted = QPixmap(pixmap.size())
    tinted.fill(Qt.transparent)
    painter = QPainter(tinted)
    painter.drawPixmap(0,0,pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(tinted.rect(),color)
    painter.end()
    return tinted


def _retint_theme_images(*_):
    color = _ink_color()
    for label,base in list(_themed_image_labels):
        try:
            label.setPixmap(_tint_pixmap(base,color))
        except RuntimeError:
            pass # underlying C++ QLabel already destroyed (page rebuilt)


qconfig.themeChanged.connect(_retint_theme_images)


def find_layout_of(widget):
  """Find whichever QGridLayout under `widget`'s parent actually contains
  `widget` - Designer nests one QGridLayout inside another for each term
  block (e.g. 2d/interface.ui's "gridLayout" inside "gridLayout_24"), so
  parentWidget().layout() alone can silently return the wrong, outer
  layout. Shared by common.py:_ensure_formula_image() and
  hybridparts.py:_add_formula_column(), which both need to insert a
  formula-image label into the exact row/column a term's field already
  occupies - kept here rather than duplicated in both so a future fix to
  this lookup (or a bug in it) only has one place to apply."""
  parent = widget.parentWidget()
  if parent is None: return None
  for grid in parent.findChildren(QtWidgets.QGridLayout):
    if grid.indexOf(widget) != -1:
      return grid
  return None


@_form_thread_only
def set_image(page,name,path,width=None,height=None):
  """Set a certain image"""
  label = page.findChild(QtWidgets.QLabel,name) # get the object
  if label is None:
      print(name,"label not found")
      return
  pixmap = QPixmap(path)
  if width and height:
        # Scale to exact size, keeping aspect ratio (optional)
    pixmap = pixmap.scaled(width, height,
            Qt.KeepAspectRatio, Qt.SmoothTransformation)
  _themed_image_labels.append((label,pixmap))
  label.setPixmap(_tint_pixmap(pixmap,_ink_color()))
  # deliberately not label.show(): a term whose field latticeterms.py has
  # already hidden (e.g. Haldane on a non-honeycomb lattice) would
  # otherwise have its formula image forced back to visible right here,
  # independent of the field it sits next to - a label is visible by
  # Qt's own default anyway, so nothing needs this to become shown that
  # wasn't already.


def set_logo(name,image,**kwargs):
  """Set a certain logo"""
  qlroot = os.path.dirname(os.path.realpath(__file__))+"/../../"
  path = qlroot+"/interface-pyqt/logos/"+image
  set_image(name,path,**kwargs)


@_form_thread_only
def set_tooltip(page,name,text):
  """Set a hover tooltip on a widget by object name, if it exists on this
  page (silently skipped otherwise - not every mode has every term, same
  convention as set_image's missing-label handling above)."""
  obj = page.findChild(QtWidgets.QWidget,name)
  if obj is None: return
  obj.setToolTip(text)




@_gui_thread_only
def save_interface(self,output=None):
    """Save all the parameter widgets (text fields, comboboxes, checkboxes
    and radio buttons) of the interface to a JSON file"""
    if output is None: output = os.getcwd() + "/QL_save/interface.json"
    out = dict() # dictionary
    for name,obj in inspect.getmembers(self): # all the different objects
        if isinstance(obj,QtWidgets.QLineEdit):
            out[name] = {"type":"line","value":obj.text()}
        elif isinstance(obj,QtWidgets.QComboBox):
            out[name] = {"type":"combo","value":obj.currentText()}
        elif isinstance(obj,(QtWidgets.QCheckBox,QtWidgets.QRadioButton,SwitchButton)):
            out[name] = {"type":"check","value":obj.isChecked()}
    with open(output, 'w') as outf: # write as json file
        json.dump(out, outf)


@_gui_thread_only
def load_interface(self,inputfile):
    """Restore parameter widgets previously written by save_interface()"""
    with open(inputfile, "r") as inf:
        out = json.load(inf) # dictionary of saved widgets
    for name in out: # loop over saved widgets
        try: obj = getattr(self,name) # get this object
        except AttributeError: continue # widget no longer exists
        entry = out[name]
        try:
            if entry["type"]=="line":
                obj.setText(entry["value"])
                # setText() doesn't fire textEdited (only real user
                # keystrokes do - see wire_highlight()), so a Hamiltonian-
                # term field restored here would otherwise keep showing
                # whatever highlight state it had before this load
                if getattr(obj,"_term_highlight",False):
                    termhighlight.apply_highlight(obj,termhighlight.is_nonzero_value(entry["value"]))
            elif entry["type"]=="combo": obj.setCurrentText(entry["value"])
            elif entry["type"]=="check": obj.setChecked(entry["value"])
        except Exception: pass # widget type changed since the save


# --- Naming a saved-results folder ---------------------------------------
#
# save_state()/load_state() (qlinterface.py) used to always write/read a
# single hardcoded "QL_save" folder, silently overwriting whatever was
# there before - the user_guide.md workaround was "rename or move QL_save
# in between" if you wanted to keep two results. ask_save_name()/
# ask_load_name() below let a save be given its own name instead, via a
# small Fluent-styled modal dialog. Both are called from save_state()/
# load_state() while running on a handler's worker thread (see
# _HandlerRunner), so - like save_interface/load_interface above - they're
# @_gui_thread_only: the dialog itself always has to run on the GUI
# thread, and marshaling blocks the worker thread until the user answers,
# which is fine since only one handler runs at a time anyway.

_WINDOWS_RESERVED_CHARS = set('<>:"|?*')
_WINDOWS_RESERVED_NAMES = ({"CON","PRN","AUX","NUL"}
    | {"COM%d"%i for i in range(1,10)} | {"LPT%d"%i for i in range(1,10)})


def _sanitize_save_name(name):
    """Turn free-form dialog text into a safe, flat folder name - reject
    anything empty, anything that would escape the save directory (a path
    separator or '..' component), and anything that's a legal folder name
    on Linux/Mac but not on Windows (this app explicitly supports all
    three - see pysrc/pyqula/filesystem.py's own docstring) - rather than
    letting an illegal name reach fs.mkdir() and surface as an opaque
    OSError."""
    name = name.strip()
    if not name or name in (".",".."): return None
    if os.sep in name or (os.altsep and os.altsep in name): return None
    # not any(c in ... for c in name): this module does `from numpy import
    # *` above, which shadows the builtin any() with numpy.any() - given a
    # generator expression (rather than an array), numpy.any() just tests
    # the generator object's own (always-truthy) boolean value instead of
    # iterating it, so it would reject every name unconditionally
    if set(name) & _WINDOWS_RESERVED_CHARS: return None
    if name.endswith(".") or name.upper() in _WINDOWS_RESERVED_NAMES: return None
    return name


class _SaveNameDialog(MessageBoxBase):
    def __init__(self,parent,default):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel("Save results as",self)
        self.nameEdit = LineEdit(self)
        self.nameEdit.setText(default)
        self.nameEdit.setPlaceholderText("Folder name")
        self.nameEdit.selectAll()
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.nameEdit)
        self.widget.setMinimumWidth(320)

    def validate(self):
        return _sanitize_save_name(self.nameEdit.text()) is not None


class _LoadNameDialog(MessageBoxBase):
    def __init__(self,parent,options):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel("Load saved results",self)
        self.nameCombo = ComboBox(self)
        self.nameCombo.addItems(options)
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.nameCombo)
        self.widget.setMinimumWidth(320)


@_gui_thread_only
def ask_save_name(parent,default="QL_save"):
    """Prompt for a name for the results folder about to be saved.
    Returns the sanitized name, or None if the user cancelled."""
    dlg = _SaveNameDialog(parent,default)
    if dlg.exec():
        return _sanitize_save_name(dlg.nameEdit.text())
    return None


@_gui_thread_only
def ask_load_name(parent,options):
    """Prompt which previously-saved results folder to load, from
    `options` (folder names found under the launch directory). Returns the
    chosen name, or None if the user cancelled or there was nothing to
    choose from (an InfoBar explains which, in the latter case)."""
    if not options:
        InfoBar.warning(title="Nothing to load",
            content="No saved results were found",
            parent=parent,duration=4000,position=InfoBarPosition.TOP)
        return None
    dlg = _LoadNameDialog(parent,options)
    if dlg.exec():
        return dlg.nameCombo.currentText()
    return None


@_gui_thread_only
def notify_success(parent,title,content):
    """Same InfoBar convention as the "Please wait"/"Calculation failed"
    bars above, for save_state()/load_state() (qlinterface.py) to confirm
    a save/load actually happened - neither had any success feedback
    before, so it was easy to miss whether a click did anything."""
    InfoBar.success(title=title,content=content,parent=parent,
        duration=4000,position=InfoBarPosition.TOP)


@_gui_thread_only
def notify_cancelled(parent,content):
    """Same idea as notify_success(), for the "nothing happened" path
    (dialog dismissed, overwrite declined) - printing to stdout alone,
    the previous behavior, is invisible when launched with no terminal
    attached (e.g. the desktop icon)."""
    InfoBar.warning(title="Cancelled",content=content,parent=parent,
        duration=4000,position=InfoBarPosition.TOP)


@_gui_thread_only
def confirm_overwrite(parent,name):
    """Ask before save_state() (qlinterface.py) deletes and replaces a
    folder named `name` that doesn't look like a previous save of its own
    (see qlinterface._looks_like_prior_save()) - True lets the overwrite
    proceed, False (Cancel, or the dialog closed) aborts it. Deliberately
    not asked when `name` *does* look like a prior save: repeatedly saving
    under the same name to update it in place is the expected, common
    case (matches the old always-overwrite "QL_save" behavior), so only
    the surprising case - a name that collides with something else
    entirely - needs a confirmation click."""
    box = MessageBox("Overwrite existing folder?",
        'A folder named "%s" already exists here and does not look like a '
        'previous "Save results" - overwrite it anyway?'%name,parent)
    return box.exec()






