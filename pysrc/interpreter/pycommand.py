import subprocess
import os
import sys
import platform


def write_python_exec(name):
    dirname = os.path.dirname(os.path.realpath(__file__)) # this directory
    f = open(dirname+"/pythoninterpreter.py","w") # open file
    f.write("mainpython = \""+name+"\"") # write this one
    f.close() # close the file


def correct_python(install=False):
    """CHeck if a suitable Python is installed"""
    try:
        import PyQt5
        import scipy
        import numpy
        import numba
        import matplotlib
        return True
    except: 
        if install: # if something wrong happened, try to install the libraries
            install_dependencies(executable=sys.executable) # try to install 
            return correct_python(install=False) # try again
        return False # if it still does not work, give up

def install_python():
    """Install a correct Python distribution"""
    if correct_python(install=True): # The current one is the right Python 
        write_python_exec(sys.executable) # write this Python distribution
        print("Found a correct python distribution")
        return # nothing to do
    pwd = os.getcwd() # get the current directory
    dirname = os.path.dirname(os.path.realpath(__file__)) # this directory
    os.system("rm -rf "+dirname+"/python_interpreter") # remove the subfolder
    os.system("mkdir "+dirname+"/python_interpreter") # create the subfolder
    os.chdir(dirname+"/python_interpreter") # go to this directory
    pypath = dirname+"/python_interpreter/python3" # path to Python
    if platform.system()=="Linux":
        anapath = "https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh"
        os.system("wget "+anapath) # download Anaconda Python
        anafile = "Anaconda3-2020.02-Linux-x86_64.sh"
    elif platform.system()=="Windows":
        print("Not compatible with Windows yet")
        exit()
    else: # for Mac
        anapath = "https://repo.anaconda.com/archive/Anaconda3-2020.02-MacOSX-x86_64.sh"
        os.system("curl -LO "+anapath) # download Anaconda Python
        anafile = "Anaconda3-2020.02-MacOSX-x86_64.sh " # file to install
    os.system("bash "+anafile+" -b -p "+pypath) # install anaconda
    os.system("rm "+anafile) # remove the installer
    # now get the executable
    dirname = os.path.dirname(os.path.realpath(__file__)) # this directory
    pyint = dirname +"/python_interpreter/python3/bin/python3" # local one
    write_python_exec(pyint) # write this Python distribution



def install_dependencies(executable=None):
    if executable is None: executable = get_python()
    for l in ["mayavi","numba","scipy","numpy","matplotlib"]:
        try: install_package(l,executable=executable)
        except: pass
    # try to compile fortran
    try:
        from ..pyqula import compilefortran
        compiler = os.path.dirname(os.path.realpath(get_python()))+"/f2py"
        compilefortran.compile_fortran(compiler=compiler) # compile fortran
    except: 
        print("Fortran was not compiled")



def get_python():
  """Return the path for Anaconda Python, which has pyqt by default"""
  try:
      from .pythoninterpreter import mainpython
      if not os.path.isfile(mainpython): # do a sanity check
          print("Python command not found, install manually Anaconda and execute again the quantum-lattice installation script")
          exit()
      return mainpython
      print("Using the interpreter",mainpython)
  except:
      print("No python interpreter found, exiting")
      exit()

def get_qh_path():
    """Return the Quantum Lattice path"""
    return os.path.dirname(os.path.realpath(__file__))+"/../../"

def get_qh_command():
    """Return the Quantum lattice command"""
    return get_python() +" "+get_qh_path()+"/bin/quantum-lattice"


def add_to_path():
    """Add quantum lattice to the PATH"""
    out = os.environ["SHELL"]
    home = os.environ["HOME"]
    if out=="/bin/bash":
        if platform.system()=="Linux":  rcfile = home+"/.bashrc"
        else: rcfile = home+"/.bash_profile"
    elif out=="/bin/zsh": 
        rcfile = home+"/.zshrc"
    qhpath = os.path.dirname(os.path.realpath(__file__))+"/../../bin"
    try: ls = open(rcfile,"r").read() # if the file exists
    except: ls = "" # otherwise
    addrc = "alias quantum-lattice=\"" + get_qh_command() +"\"\n\n"
#    addrc = "\nexport PATH=\""+qhpath+"\":$PATH\n"
    open(rcfile,"w").write(ls+addrc) # add to the bash


def install_package(package,executable=None):
    if executable is None: executable = sys.executable
    subprocess.check_call([executable, "-m", "pip", "install", package])



def run_qh():
    """Run Quantum Lattice"""
    qhpath = os.path.dirname(os.path.realpath(__file__))+"/../../bin"
    os.system(get_python() +" "+qhpath+"/quantum-lattice &")

def create_icon():
    """Create the Quantum Lattice icon"""
    if platform.system()!="Linux": return # nothing to do
    ls = "" # empty string
    ls += "#!/usr/bin/env xdg-open\n" 
    ls += "[Desktop Entry]\n"
    ls += "Version=1\n"
    ls += "Type=Application\n"
    ls += "Terminal=false\n"
    ls += "Exec=" + get_qh_command()+"\n"
    ls += "Name=Quantum-Lattice\n"
    ls += "Comment=Quantum-Lattice\n"
    ls += "Icon="+get_qh_path()+"/screenshots/icon.png"
    name = get_qh_path()+"quantum-lattice.desktop" # icon name
    open(name,"w").write(ls) # write the content
    # and write it in the launcher folder
    iconpath = os.environ["HOME"]+"/.local/share/applications/quantum-lattice.desktop"
    try: # this may not work for some Linux distros
      open(iconpath,"w").write(ls) 
    except: pass
    os.system("chmod +x "+name) # execution permission



def set_utility_interpreter():
    """Set the interpreter for all the utilities"""
    executable = get_python() # get the interpreter
    upath = os.path.dirname(os.path.realpath(__file__))+"/../../utilities"
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(upath) if isfile(join(upath, f))]
    for f in onlyfiles: # loop over files
        ls = open(upath+"/"+f).readlines() # read all the lines
        for i in range(len(ls)):
            if "#!/" in ls[i]: 
                ls[i] = "#!"+get_python()+"\n" # put the right interpreter
                break
        fo = open(upath+"/"+f,"w")
        for l in ls: fo.write(l)
        fo.close()






