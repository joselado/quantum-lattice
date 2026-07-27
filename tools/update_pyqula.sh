#!/bin/bash
# Update the vendored pysrc/pyqula/ (and its paired pysrc/pyqula_user_guide.md)
# from the upstream pyqula repository, wholesale - not a patch/merge.
#
# See CLAUDE.md's "Updating vendored pyqula" section for when to run this.
#
# Usage: tools/update_pyqula.sh
set -euo pipefail

qlroot="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
upstream="https://github.com/joselado/pyqula.git"
clonedir="$(mktemp -d)"
trap 'rm -rf "$clonedir"' EXIT

echo "Cloning $upstream ..."
git clone --depth 1 "$upstream" "$clonedir"
commit="$(git -C "$clonedir" rev-parse --short HEAD)"
subject="$(git -C "$clonedir" log -1 --format=%s)"

rm -rf "$qlroot/pysrc/pyqula"
cp -r "$clonedir/src/pyqula" "$qlroot/pysrc/pyqula"
cp "$clonedir/documentation/user_guide.md" "$qlroot/pysrc/pyqula_user_guide.md"

echo
echo "Updated pysrc/pyqula to upstream master ($commit): $subject"
echo "Re-run tools/smoke_test.py, then review 'git status'/'git diff --stat pysrc/pyqula' before committing."
