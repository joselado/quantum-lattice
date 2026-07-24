#!/bin/bash
# Regenerate every interface-pyqt/<mode>/interface.py from its interface.ui
# via pyside6-uic. Replaces the old per-mode convert.sh scripts (pyuic5/PyQt5).
#
# Usage: tools/convert_ui.sh
set -euo pipefail

qlroot="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

for ui in "$qlroot"/interface-pyqt/*/interface.ui; do
    moddir="$(dirname "$ui")"
    # quasiperiodic/ is dead/unwired code (predates this script) - leave it alone.
    [[ "$(basename "$moddir")" == "quasiperiodic" ]] && continue
    pyside6-uic "$ui" -o "$moddir/interface.py"
    echo "converted $ui"
done
