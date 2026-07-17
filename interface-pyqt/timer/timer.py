#!/usr/bin/env python3

import sys
import os
import signal

qhroot = os.path.dirname(os.path.realpath(__file__))+"/../.."
sys.path.append(qhroot+"/interface-pyqt/qtwrap")
sys.path.append(qhroot+"/pysrc/") # python libraries


import qtwrap # import the library with simple wrappaers to qt4
get = qtwrap.get  # get the value of a certain variable
getbox = qtwrap.getbox  # get the value of a certain variable
window = qtwrap.main() # this is the main interface

# PID of the process actually running the calculation (passed in by
# qlinterface.computing()), so the kill button can stop it directly -
# this window is its own subprocess and cannot reach it any other way
parent_pid = int(sys.argv[1]) if len(sys.argv)>1 else None


def kill_calculation():
    if parent_pid is not None:
        try: os.kill(parent_pid,signal.SIGTERM)
        except ProcessLookupError: pass # already finished
    window.close()


window.kill_button.clicked.connect(kill_calculation)

window.run()

