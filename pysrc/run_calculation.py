#!/usr/bin/env python3
"""Standalone entry point for running one calculation's pure compute
function in a child OS process, launched by
qtwrap.run_calculation_subprocess() in place of running it in-process on a
_HandlerRunner QThread. Killing this process (see
qtwrap.cancel_current_calculation()) is safe; killing a Python thread
mid pyqula/numpy call is not - see CLAUDE.md/INTERFACE_GUIDE.md for the
full design.

This script itself never builds a QApplication or any widget - unlike a
normal `python <mode>.py` launch, which does that as a side effect of
import. The mode's own calc.py (imported below) may still pull in PySide6
via its own imports (e.g. hamiltoniantype.py, common.py); that's harmless
on its own, since merely importing those modules doesn't construct
anything - only qtwrap.new_page()/ensure_app(), never called here, does.

Usage: run_calculation.py <mode_dir> <handler_key> <inputs_json_path> <scratch_dir>
"""
import sys
import os
import json


def main():
    mode_dir,handler_key,inputs_path,scratch_dir = sys.argv[1:5]
    # this file's own directory (pysrc/) is already sys.path[0] - Python
    # auto-prepends a launched script's own directory - so `import
    # interfacetk` already resolves correctly with no explicit append
    # needed (see qtwrap.py's run_calculation_subprocess() docstring for
    # why this script deliberately does NOT live inside pysrc/interfacetk/
    # itself). Appended anyway, matching every <mode>.py/ql-* script's own
    # bootstrap, in case this is ever invoked some other way (e.g. via -m).
    qlroot = os.path.dirname(os.path.realpath(__file__))+"/.."
    sys.path.append(qlroot+"/pysrc/")
    sys.path.insert(0,mode_dir) # so `import calc` finds this mode's own calc.py
                                 # (bare-import-via-sys.path, same pattern
                                 # huge_0d's islandbuild.py/handlers.py already use)
    os.chdir(scratch_dir) # every compute function writes/reads files cwd-relative,
                           # matching the convention every in-process handler already uses
    with open(inputs_path) as f:
        inputs = json.load(f)
    import calc
    fn = calc.COMPUTE_HANDLERS[handler_key]
    fn(inputs)


if __name__ == "__main__":
    main()
