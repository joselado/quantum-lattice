#!/usr/bin/env python3
"""Shared matplotlib style for every ql-* plotting script in this folder.

Not a ql-* command - only imported by sibling scripts via
sys.path.insert(0, dirname), the same pattern every ql-* script already
uses to find its own directory (see e.g. _pv3d.py).

Centralizes what used to be a 2-3 line rcParams block copy-pasted into
~65 ql-* scripts (a font size, and in about half of them a
font.family = "Bitstream Vera Serif" that isn't installed on this
system - matplotlib was silently falling back to its own default font
on every one of those plots). Also provides a small named color
palette so scripts stop hardcoding ad hoc color strings ("black",
"yellow", "red", ...) individually.

Usage - near the top of a ql-* script, before creating any figure:

    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
    import plotstyle
    plotstyle.apply()
    ...
    plt.plot(x,y,color=plotstyle.PRIMARY)

No global grid is set: several ql-* scripts render heatmaps/colormaps
(imshow, pcolormesh, contourf) where grid lines would draw on top of
the image data rather than make the plot nicer.
"""
import os
import matplotlib

# semantic palette - replaces the ad hoc color="black"/"yellow"/"red"/
# "blue" literals scattered across ql-* scripts. Light-theme values; see
# PRIMARY_DARK etc below for the dark-theme counterparts apply() switches
# to. Scripts should keep referencing plotstyle.PRIMARY etc by attribute
# (not `from plotstyle import PRIMARY`), since apply() rebinds these
# module-level names when dark mode is active - a few ql-* scripts using
# the by-value import form would not pick up the switch.
PRIMARY = "#222222"    # main data series (was "black")
SECONDARY = "#2c6fbb"  # a second data series (was "blue")
ACCENT = "#c0392b"     # highlighted/comparison series (was "red")
FILL = "#fdf1b8"       # shaded regions, e.g. occupied states (was "yellow"/"lightyellow")
BACKGROUND = "white"   # figure/axes background - many ql-* scripts call
                        # fig.set_facecolor(plotstyle.BACKGROUND) explicitly
                        # after creating a figure, since matplotlib doesn't
                        # consistently pick up rcParams["figure.facecolor"]
                        # for figures created via the shared plotpyqt.py
                        # interactive-dialog path

PRIMARY_DARK = "#e8e8e8"
SECONDARY_DARK = "#6fa8dc"
ACCENT_DARK = "#e74c3c"
FILL_DARK = "#7a6a2e"

BACKGROUND_DARK = "#1e1e1e"
FOREGROUND_DARK = "#e8e8e8"


def _env_wants_dark():
    """The shell (bin/versions/quantum-lattice-pyqt) sets QL_THEME=dark
    once in its own process env before building any page; every ql-*
    script is launched from there via qlinterface.execute_script(), which
    inherits that environment, so no per-script wiring is needed to know
    which theme is active."""
    return os.environ.get("QL_THEME","").lower() == "dark"


def apply(font_size=18,dark=None):
    """Apply the shared plot style. Call once before creating figures.
    dark: True/False to force a theme, or None (default) to follow
    QL_THEME from the environment."""
    global PRIMARY,SECONDARY,ACCENT,FILL,BACKGROUND
    if dark is None: dark = _env_wants_dark()
    rc = {
        "font.size": font_size,
        # matplotlib's actual default font - the previous
        # "Bitstream Vera Serif" wasn't installed on this system and
        # every script setting it was silently falling back to this
        # anyway; set explicitly so that's no longer accidental
        "font.family": "DejaVu Sans",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
    }
    if dark:
        PRIMARY,SECONDARY,ACCENT,FILL,BACKGROUND = PRIMARY_DARK,SECONDARY_DARK,ACCENT_DARK,FILL_DARK,BACKGROUND_DARK
        rc.update({
            "figure.facecolor": BACKGROUND_DARK,
            "axes.facecolor": BACKGROUND_DARK,
            "savefig.facecolor": BACKGROUND_DARK,
            "axes.edgecolor": FOREGROUND_DARK,
            "axes.labelcolor": FOREGROUND_DARK,
            "text.color": FOREGROUND_DARK,
            "xtick.color": FOREGROUND_DARK,
            "ytick.color": FOREGROUND_DARK,
            "grid.color": "#444444",
            "legend.facecolor": BACKGROUND_DARK,
            "legend.edgecolor": FOREGROUND_DARK,
        })
    else:
        PRIMARY,SECONDARY,ACCENT,FILL,BACKGROUND = "#222222","#2c6fbb","#c0392b","#fdf1b8","white"
    matplotlib.rcParams.update(rc)
