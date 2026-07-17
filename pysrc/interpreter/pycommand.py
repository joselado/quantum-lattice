import subprocess
import sys
import os
import platform
import shutil


def get_qh_path():
    """Return the Quantum Lattice repository root, as an absolute path"""
    here = os.path.dirname(os.path.realpath(__file__)) # .../pysrc/interpreter
    return os.path.normpath(os.path.join(here,"..",".."))


def get_python():
    """Return the interpreter this process is running under.

    Quantum Lattice is meant to be launched through the console script
    that `pip install -e .` registers, which pip always points at the
    interpreter it was installed into (the one with PyQt5/numpy/etc.
    already available). So the running interpreter is always the right
    one to use for spawning helper processes (a lattice-mode window, a
    ql-* plotting script, ...); there is no need to persist a separate
    "which python has the right packages" pin to a generated file.
    """
    return sys.executable


def _required_packages():
    """Package names listed in requirements.txt (comments/blank lines skipped)"""
    reqfile = os.path.join(get_qh_path(),"requirements.txt")
    packages = []
    for line in open(reqfile):
        line = line.strip()
        if line=="" or line.startswith("#"): continue
        packages.append(line)
    return packages


def _module_available(python,module):
    """Check whether `module` can be imported by the given interpreter"""
    result = subprocess.run([python,"-c","import "+module],
                             stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    return result.returncode==0


def install_requirements(python=None):
    """Make sure the required packages are available for the given
    interpreter (or the current one). Each package is checked first, and
    only the ones actually missing are installed, with that same
    interpreter's own pip - no separate Python distribution is ever
    downloaded, so this works the same way on Linux, Mac and Windows."""
    if python is None: python = sys.executable
    missing = [p for p in _required_packages() if not _module_available(python,p)]
    if missing:
        print("Installing missing packages:",", ".join(missing))
        try:
            subprocess.check_call([python,"-m","pip","install"]+missing)
        except subprocess.CalledProcessError as e:
            print("Failed to install required packages:",e)
            print("Try installing them manually with:")
            print(" ",python,"-m","pip","install",*missing)
    else:
        print("All required packages are already installed")
    # pyvista is optional: only the 3D plotting utilities need it. It's a
    # much easier install than mayavi (prebuilt VTK wheel, no custom
    # code-generation step at install time), but a failure here is still
    # reported rather than blocking the rest of the install
    if not _module_available(python,"pyvista"):
        try:
            subprocess.check_call([python,"-m","pip","install","pyvista"])
        except subprocess.CalledProcessError:
            print("Optional dependency 'pyvista' could not be installed;")
            print("3D plotting utilities (ql-plot3d, ql-moments, ...) will not work")
    # try to compile the optional Fortran acceleration bundled with pyqula
    try:
        from ..pyqula import compilefortran
        compiler = shutil.which("f2py",path=os.path.dirname(os.path.realpath(python)))
        compilefortran.compile_fortran(compiler=compiler)
    except Exception as e:
        print("Optional Fortran acceleration was not compiled:",e)


def install_editable(python=None):
    """Register the `quantum-lattice` console script with pip, so it ends up
    on PATH pointing at the correct interpreter on Linux, Mac and Windows
    alike (pip handles the OS-specific PATH/launcher mechanics for us)."""
    if python is None: python = sys.executable
    subprocess.check_call([python,"-m","pip","install","-e",get_qh_path()])


def get_qh_command():
    """Return the absolute, PATH-independent command to launch Quantum Lattice.
    Desktop launchers (e.g. a .desktop Exec= line) usually run with a minimal
    PATH, so prefer the pip-installed console script if it can be found, and
    fall back to invoking bin/quantum-lattice directly with this interpreter."""
    installed = shutil.which("quantum-lattice")
    if installed is not None: return installed
    return get_python()+" "+os.path.join(get_qh_path(),"bin","quantum-lattice")


def create_icon():
    """Create a Quantum Lattice launcher: a .desktop entry on Linux, a .bat
    launcher on Windows (double-click, can be pinned to Start/taskbar
    manually). Mac users launch via the `quantum-lattice` command."""
    qhroot = get_qh_path()
    system = platform.system()
    if system=="Linux":
        ls  = "#!/usr/bin/env xdg-open\n"
        ls += "[Desktop Entry]\n"
        ls += "Version=1\n"
        ls += "Type=Application\n"
        ls += "Terminal=false\n"
        ls += "Exec="+get_qh_command()+"\n"
        ls += "Name=Quantum-Lattice\n"
        ls += "Comment=Quantum-Lattice\n"
        ls += "Icon="+os.path.join(qhroot,"screenshots","icon.png")
        name = os.path.join(qhroot,"quantum-lattice.desktop")
        open(name,"w").write(ls)
        # also install it in the launcher folder, best-effort: some distros
        # use a different applications directory or none at all
        iconpath = os.path.join(os.environ["HOME"],".local","share","applications","quantum-lattice.desktop")
        try: open(iconpath,"w").write(ls)
        except OSError as e: print("Could not install the launcher menu entry:",e)
        os.chmod(name,0o755)
    elif system=="Windows":
        installed = shutil.which("quantum-lattice")
        target = installed if installed is not None else get_qh_command()
        bat = "@echo off\r\n\""+target+"\"\r\n"
        name = os.path.join(qhroot,"quantum-lattice.bat")
        open(name,"w").write(bat)
        print("Created",name,"- pin it to the Start menu/taskbar to launch Quantum Lattice")
    else: # Mac: no dock icon automation, use the `quantum-lattice` command
        pass


def run_qh():
    """Run Quantum Lattice"""
    installed = shutil.which("quantum-lattice")
    if installed is not None:
        subprocess.Popen([installed])
    else:
        subprocess.Popen([get_python(),os.path.join(get_qh_path(),"bin","quantum-lattice")])
