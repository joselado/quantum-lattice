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
import matplotlib

# semantic palette - replaces the ad hoc color="black"/"yellow"/"red"/
# "blue" literals scattered across ql-* scripts
PRIMARY = "#222222"    # main data series (was "black")
SECONDARY = "#2c6fbb"  # a second data series (was "blue")
ACCENT = "#c0392b"     # highlighted/comparison series (was "red")
FILL = "#fdf1b8"       # shaded regions, e.g. occupied states (was "yellow"/"lightyellow")


def apply(font_size=18):
    """Apply the shared plot style. Call once before creating figures."""
    matplotlib.rcParams.update({
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
    })
